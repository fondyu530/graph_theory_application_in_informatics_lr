import numpy as np
from graph_tools import Graph, read_adjacency_matrix_from_file


def define_max_flow(graph_obj: Graph, start_vertex, end_vertex):
    residual_adjacency_matrix = graph_obj.adjacency_matrix.copy()
    flows_list = []
    while True:
        current_vertex = start_vertex - 1
        trace_list = [(np.inf, current_vertex)]
        child_vertices = residual_adjacency_matrix[current_vertex]
        tmp_residual_adjacency_matrix = residual_adjacency_matrix.copy()
        while current_vertex != end_vertex - 1:
            max_flow = np.max(child_vertices)
            if max_flow == 0:
                bad_vertex = trace_list.pop()[1]
                if len(trace_list) == 0:
                    break
                current_vertex = trace_list[-1][1]
                tmp_residual_adjacency_matrix[current_vertex][bad_vertex] = 0
                child_vertices = tmp_residual_adjacency_matrix[current_vertex]
                continue
            else:
                for row_num in range(len(tmp_residual_adjacency_matrix)):
                    tmp_residual_adjacency_matrix[row_num][current_vertex] = 0
                current_vertex = np.argmax(child_vertices)
                child_vertices = tmp_residual_adjacency_matrix[current_vertex]
            trace_list.append((max_flow, current_vertex))
        if not trace_list:
            break
        min_flow = min(trace_list, key=lambda x: x[0])[0]
        for trace_num in range(len(trace_list) - 1):
            i = trace_list[trace_num][1]
            j = trace_list[trace_num + 1][1]
            residual_adjacency_matrix[i][j] -= min_flow
            residual_adjacency_matrix[j][i] += min_flow
        flows_list.append(min_flow)
    return sum(flows_list)


for file_num in [1, 2]:
    graph_file_path = f"graphs_flow/graph_{file_num}.txt"
    matrix = read_adjacency_matrix_from_file(graph_file_path)
    graph = Graph()
    graph.load_graph_from_adjacency_matrix(matrix)
    start, end = 1, matrix.shape[0]
    flow_max = define_max_flow(graph_obj=graph, start_vertex=start, end_vertex=end)
    print(f"Матрица смежноти графа N = {file_num}:")
    print(matrix)
    print(f"Максимальный поток: {flow_max}", end="\n\n")
