import numpy as np


class Graph:
    def __init__(self):
        self.adjacency_matrix = None
        self.adjacency_list = None
        self.type = None
        self.edges_set = None
        self.in_vertex_degrees = None
        self.out_vertex_degrees = None
        self.order = None
        self.size = None
        self.distance_matrix = None
        self.eccentricity_vector = None
        self.radius = None
        self.diameter = None

    def load_graph_from_adjacency_matrix(self, adj_matrix: np.array):
        self.adjacency_matrix = adj_matrix
        self.adjacency_list = self.get_adjacency_list(adj_matrix)
        self.type = self.define_graph_type(adj_matrix)
        self.edges_set = self.get_edges_set(adj_matrix) if self.type != "digraph" else None
        self.order = adj_matrix.shape[0]
        self.in_vertex_degrees = self.define_graph_vertex_degrees(adj_matrix, mode="in")
        self.out_vertex_degrees = self.define_graph_vertex_degrees(adj_matrix, mode="out")
        self.size = np.sum(adj_matrix) if self.type == "digraph" else np.sum(adj_matrix) // 2
        self.distance_matrix = self.define_distance_matrix(adj_matrix)
        self.eccentricity_vector = np.max(self.distance_matrix, axis=1)
        self.radius = self.eccentricity_vector.min()
        self.diameter = self.eccentricity_vector.max()

    @staticmethod
    def get_adjacency_list(adjacency_matrix: np.array) -> dict:
        adjacency_list = {}
        for i, row in enumerate(adjacency_matrix):
            adjacency_list[i+1] = set()
            for j, el in enumerate(row):
                if el:
                    adjacency_list[i+1].add(j+1)
        return adjacency_list

    @staticmethod
    def define_graph_type(adjacency_matrix: np.array) -> str:
        return "non-digraph" if (adjacency_matrix == adjacency_matrix.T).all() else "digraph"

    @staticmethod
    def define_graph_vertex_degrees(adjacency_matrix: np.array, mode="in") -> np.array:
        axis = None
        if mode == "in":
            axis = 1
        elif mode == "out":
            axis = 0
        return np.sum(adjacency_matrix, axis=axis)

    @staticmethod
    def define_distance_matrix(adjacency_matrix: np.array) -> np.array:
        # floyd-warshall algorithm
        vertices_num = adjacency_matrix.shape[0]
        distance_matrix = adjacency_matrix.astype(float)
        distance_matrix[distance_matrix == 0] = np.inf
        np.fill_diagonal(distance_matrix, 0)

        for k in range(vertices_num):
            for i in range(vertices_num):
                for j in range(vertices_num):
                    new_distance = distance_matrix[i, k] + distance_matrix[k, j]
                    if new_distance < distance_matrix[i, j]:
                        distance_matrix[i, j] = new_distance
        return distance_matrix

    @staticmethod
    def get_edges_set(adjacency_matrix: np.array) -> set:
        """Works correctly only for non-digraph"""
        edges = set()
        for i in range(len(adjacency_matrix)):
            for j in range(i, len(adjacency_matrix[i])):
                if adjacency_matrix[i][j]:
                    edge, weight = (i+1, j+1), adjacency_matrix[i][j]
                    edges.add((edge, weight))
        return edges


def read_adjacency_matrix_from_file(path: str) -> np.array:
    adj_matrix = []
    with open(path) as file_obj:
        for line in file_obj.readlines():
            row = [int(el) for el in line.strip().split(" ")]
            adj_matrix.append(row)
    return np.array(adj_matrix)


def graph_is_connected(graph_obj, start_vertex=1, visited=None) -> bool:
    if visited is None:
        visited = set()
    visited.add(start_vertex)
    for vertex in graph_obj.adjacency_list[start_vertex] - visited:
        graph_is_connected(graph_obj, vertex, visited)
    return len(visited) == len(graph_obj.adjacency_list.keys())


def find_bridges(graph_obj: Graph):
    visited = [False] * graph_obj.order
    ret, enter = [0] * graph_obj.order, [0] * graph_obj.order
    timer = 0
    bridges = []

    def dfs(current_vertex, prev_vertex):
        nonlocal timer
        visited[current_vertex-1] = True
        enter[current_vertex-1] = ret[current_vertex-1] = timer
        timer += 1
        for neighbour_vertex in graph_obj.adjacency_list[current_vertex]:
            if neighbour_vertex != prev_vertex:
                if visited[neighbour_vertex-1]:
                    ret[current_vertex-1] = min(ret[current_vertex-1], enter[neighbour_vertex-1])
                else:
                    dfs(neighbour_vertex, current_vertex)
                    ret[current_vertex-1] = min(ret[current_vertex-1], ret[neighbour_vertex-1])
                    if ret[neighbour_vertex-1] > enter[current_vertex-1]:
                        bridges.append((current_vertex, neighbour_vertex))
    dfs(current_vertex=1, prev_vertex=-1)
    return bridges


def find_hinges(graph_obj: Graph):
    visited = [False] * graph_obj.order
    ret, enter = [0] * graph_obj.order, [0] * graph_obj.order
    timer = 0
    hinges = set()

    def dfs(current_vertex, prev_vertex):
        nonlocal timer
        visited[current_vertex-1] = True
        enter[current_vertex-1] = ret[current_vertex-1] = timer
        children_num = 0
        timer += 1
        for neighbour_vertex in graph_obj.adjacency_list[current_vertex]:
            if neighbour_vertex != prev_vertex:
                if visited[neighbour_vertex-1]:
                    ret[current_vertex-1] = min(ret[current_vertex-1], enter[neighbour_vertex-1])
                else:
                    dfs(neighbour_vertex, current_vertex)
                    ret[current_vertex-1] = min(ret[current_vertex-1], ret[neighbour_vertex-1])
                    if (ret[neighbour_vertex-1] >= enter[current_vertex-1]) and prev_vertex != -1:
                        hinges.add(current_vertex)
                    children_num += 1
        if (prev_vertex == -1) and (children_num > 1):
            hinges.add(current_vertex)
    dfs(current_vertex=1, prev_vertex=-1)
    return hinges


def find_chords(graph_obj: Graph):
    vertices = {1}
    edges_set = graph_obj.edges_set
    edges_set.add(((-1, -1), np.inf))
    skeleton_set = set()
    while len(vertices) < graph_obj.order:
        min_edge = ((-1, -1), np.inf)
        for vertex in vertices:
            found_min_edge = min(edges_set,
                                 key=lambda x: x[1] if (x[0][0] == vertex or x[0][1] == vertex) and
                                                       (x[0][0] not in vertices or x[0][1] not in vertices) else
                                 np.inf)
            if found_min_edge[1] < min_edge[1]:
                min_edge = found_min_edge
        skeleton_set.add(min_edge)
        vertices.add(min_edge[0][0])
        vertices.add(min_edge[0][1])
    chords_set = edges_set - skeleton_set - {((-1, -1), np.inf)}
    return skeleton_set, chords_set
