import numpy as np


class Graph:
    def __init__(self):
        self.adjacency_matrix = None
        self.adjacency_list = None
        self.type = None

    def read_adjacency_matrix_from_file(self, file_obj):
        self.adjacency_matrix = []
        for line in file_obj.readlines():
            row = [int(el) for el in line.strip().split(" ")]
            self.adjacency_matrix.append(row)

        self.adjacency_matrix = np.array(self.adjacency_matrix)
        self.adjacency_list = self.get_adjacency_list(self.adjacency_matrix)
        self.type = self.define_graph_type(self.adjacency_matrix)

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


# def graph_is_connected(adjacency_list, start_vertex=1, visited=None) -> bool:
#     if visited is None:
#         visited = set()
#     visited.add(start_vertex)
#     for vertex in adjacency_list[start_vertex] - visited:
#         graph_is_connected(adjacency_list, vertex, visited)
#     return len(visited) == len(adjacency_list.keys())
#
#
# def define_graph_vertex_degrees(adjacency_matrix):
#     return np.sum(adjacency_matrix, axis=1)
#
#
# def graph_is_euler_cycle(adjacency_matrix) -> bool:
#     adjacency_list = get_adjacency_list(adjacency_matrix)
#     if graph_is_connected(adjacency_list):
#         vertex_degrees = define_graph_vertex_degrees(adjacency_matrix)
#         return sum(vertex_degrees % 2 == 1) == 0
#     return False
#
#
# def graph_is_full(adjacency_matrix) -> bool:
#     return 0 in adjacency_matrix
#
#
# def graph_is_reflective(adjacency_matrix) -> bool:
#     return 0 not in np.diag(adjacency_matrix)
#
#
# def graph_is_transitive(adjacency_matrix) -> bool:
#     adjacency_list = get_adjacency_list(adjacency_matrix)
#     for base_vertex in adjacency_list.keys():
#         for secondary_vertex in adjacency_list[base_vertex]:
#             if len(adjacency_list[secondary_vertex] - adjacency_list[base_vertex] - {base_vertex}) != 0:
#                 return False
#     return True
#
#
# def graph_is_tree(adjacency_matrix) -> bool:
#     adjacency_list = get_adjacency_list(adjacency_matrix)
#     if graph_is_connected(adjacency_list):



with open("graphs/graph_1.txt", "r") as file:
    graph = Graph()
    graph.read_adjacency_matrix_from_file(file)
    print(graph.adjacency_matrix == graph.adjacency_matrix.T)
    print(graph.adjacency_list)
    print(graph.type)