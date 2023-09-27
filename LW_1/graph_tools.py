import numpy as np


class Graph:
    def __init__(self):
        self.adjacency_matrix = None
        self.adjacency_list = None
        self.type = None
        self.in_vertex_degrees = None
        self.out_vertex_degrees = None
        self.order = None

    def read_adjacency_matrix_from_file(self, file_obj):
        adj_matrix = []
        for line in file_obj.readlines():
            row = [int(el) for el in line.strip().split(" ")]
            adj_matrix.append(row)

        self.adjacency_matrix = np.array(adj_matrix)
        self.adjacency_list = self.get_adjacency_list(self.adjacency_matrix)
        self.type = self.define_graph_type(self.adjacency_matrix)
        self.order = self.adjacency_matrix.shape[0]
        self.in_vertex_degrees = self.define_graph_vertex_degrees(self.adjacency_matrix, mode="in")
        self.out_vertex_degrees = self.define_graph_vertex_degrees(self.adjacency_matrix, mode="out")

    @staticmethod
    def get_adjacency_list(adjacency_matrix) -> dict:
        adjacency_list = {}
        for i, row in enumerate(adjacency_matrix):
            adjacency_list[i+1] = set()
            for j, el in enumerate(row):
                if el: adjacency_list[i+1].add(j+1)
        return adjacency_list

    @staticmethod
    def define_graph_type(adjacency_matrix) -> str:
        return "non-digraph" if (adjacency_matrix == adjacency_matrix.T).all() else "digraph"

    @staticmethod
    def define_graph_vertex_degrees(adjacency_matrix, mode="in"):
        axis = None
        if mode == "in": axis = 1
        elif mode == "out": axis = 0
        return np.sum(adjacency_matrix, axis=axis)


def graph_is_full(graph_obj) -> bool:
    return (graph_obj.in_vertex_degrees == graph_obj.order - 1).all()


def graph_is_reflective(graph_obj) -> bool:
    return 0 not in np.diag(graph_obj.adjacency_matrix)


def graph_is_connected(graph_obj, start_vertex=1, visited=None) -> bool:
    if visited is None:
        visited = set()
    visited.add(start_vertex)
    for vertex in graph_obj.adjacency_list[start_vertex] - visited:
        graph_is_connected(graph_obj, vertex, visited)
    return len(visited) == len(graph_obj.adjacency_list.keys())


def graph_is_euler_cycle(graph_obj) -> bool:
    if graph_is_connected(graph_obj):
        if graph_obj.type == "non-digraph":
            return sum(graph_obj.in_vertex_degrees % 2 == 1) == 0
        elif graph_obj.type == "digraph":
            return (graph_obj.in_vertex_degrees == graph_obj.out_vertex_degrees).all()
    return False


def graph_is_transitive(graph_obj) -> bool:
    for base_vertex in graph_obj.adjacency_list.keys():
        for secondary_vertex in graph_obj.adjacency_list[base_vertex]:
            if len(graph_obj.adjacency_list[secondary_vertex] - graph_obj.adjacency_list[base_vertex] - {base_vertex}) != 0:
                return False
    return True
