from graph_tools import Graph, read_adjacency_matrix_from_file


for file_num in range(1, 6):
    graph_file_path = f"graphs/graph_{file_num}.txt"
    matrix = read_adjacency_matrix_from_file(graph_file_path)
    graph = Graph()
    graph.load_graph_from_adjacency_matrix(matrix)
    print(f"Граф N = {file_num}", end="\n")
    print("Матрица минимальных расстояний до каждой из вершин:")
    print(graph.distance_matrix, end="\n")
    print(f"Эксцентриситеты вершин: {'  '.join([f'{i+1}: {el}' for i, el in enumerate(graph.eccentricity_vector)])}")
    print(f"Радиус: {graph.radius}")
    print(f"Диаметр: {graph.diameter}", end="\n\n")
