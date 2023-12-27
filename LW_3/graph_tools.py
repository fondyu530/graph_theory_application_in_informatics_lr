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
                if el: adjacency_list[i+1].add(j+1)
        return adjacency_list

    @staticmethod
    def define_graph_type(adjacency_matrix: np.array) -> str:
        return "non-digraph" if (adjacency_matrix == adjacency_matrix.T).all() else "digraph"

    @staticmethod
    def define_graph_vertex_degrees(adjacency_matrix: np.array, mode="in") -> np.array:
        axis = None
        if mode == "in": axis = 1
        elif mode == "out": axis = 0
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
