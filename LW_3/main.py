import math
from graph_tools import Graph, read_adjacency_matrix_from_file


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
    edges_set.add(((-1, -1), math.inf))
    skeleton_set = set()
    while len(vertices) < graph_obj.order:
        min_edge = ((-1, -1), math.inf)
        for vertex in vertices:
            found_min_edge = min(edges_set,
                                 key=lambda x: x[1] if (x[0][0] == vertex or x[0][1] == vertex) and
                                                       (x[0][0] not in vertices or x[0][1] not in vertices) else
                                 math.inf)
            if found_min_edge[1] < min_edge[1]:
                min_edge = found_min_edge
        skeleton_set.add(min_edge)
        vertices.add(min_edge[0][0])
        vertices.add(min_edge[0][1])
    chords_set = edges_set - skeleton_set - {((-1, -1), math.inf)}
    return skeleton_set, chords_set


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
