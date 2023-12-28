from graph_tools import (Graph, read_adjacency_matrix_from_file, find_chords,
                         find_bridges, find_hinges, graph_is_connected)


for file_num in range(6, 8):
    graph_file_path = f"graphs/graph_{file_num}.txt"
    matrix = read_adjacency_matrix_from_file(graph_file_path)
    graph = Graph()
    graph.load_graph_from_adjacency_matrix(matrix)
    found_bridges = find_bridges(graph_obj=graph)
    found_hinges = find_hinges(graph_obj=graph)
    chords = skeleton = None
    if graph_is_connected(graph_obj=graph):
        skeleton, chords = find_chords(graph_obj=graph)
    print(f"Граф N = {file_num}")
    print(f"Мосты: {found_bridges}")
    print(f"Шарниры: {found_hinges}")
    print(f"Хорды: {chords}")
    print(f"Остов: {skeleton}", end="\n\n")
