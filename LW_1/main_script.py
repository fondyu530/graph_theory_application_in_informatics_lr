from graph_tools import *


for file_num in range(1, 6):
    graph_path = f"graphs/graph_{file_num}.txt"
    graph = Graph()
    with open(graph_path, "r") as file_obj:
        print(f"Граф N = {file_num}")
        graph.read_adjacency_matrix_from_file(file_obj)
        print("Матрица смежности:", end="\n")
        print(graph.adjacency_matrix, end="\n")
        print(f"Список смежности: {graph.adjacency_list}")
        print(f"Тип графа (орграф / неограф): {graph.type}")
        print(f"Порядок графа: {graph.order}")

        res = "Классы, которым принадлежит граф: "

        full = "Полный, " if graph_is_full(graph) else ""
        euler = "Эйлеров цикл, " if graph_is_euler_cycle(graph) else ""
        reflective = "Рефлексивный, " if graph_is_reflective(graph) else ""
        transitive = "Транзитивный, " if graph_is_transitive(graph) else ""
        connected = "Связный" if graph_is_connected(graph) else "Не связный"

        res += full + euler + reflective + transitive + connected

        print(res, end="\n\n")
