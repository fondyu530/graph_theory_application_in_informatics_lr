from graph_tools import *


graph_path = "graphs/graph_5.txt"
graph = Graph()

with open(graph_path, "r") as file_obj:
    graph.read_adjacency_matrix_from_file(file_obj)
    print("Матрица смежности:", end="\n")
    print(graph.adjacency_matrix, end="\n\n")

    print("Список смежности:")
    print(graph.adjacency_list, end="\n\n")

    print(f"Тип графа (орграф / неограф): {graph.type}\n")

    print(f"Порядок графа: {graph.order}")

    res = "Классы, которым принадлежит граф:\n\n"

    full = "Полный\n" if graph_is_full(graph) else ""
    euler = "Эйлеров цикл\n" if graph_is_euler_cycle(graph) else ""
    reflective = "Рефлексивный\n" if graph_is_reflective(graph) else ""
    transitive = "Транзитивный\n" if graph_is_transitive(graph) else ""
    connected = "Связный\n" if graph_is_connected(graph) else "Не связный"

    res += full + euler + reflective + transitive + connected

    print(res)

