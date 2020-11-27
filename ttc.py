
def dfs(graph, i, visited):
    visited[i] = 1
    if visited[graph[i][0]] == 0:
        return dfs(graph, graph[i][0], visited)
    elif visited[graph[i][0]] == 1 and i != graph[i][0]:
        return True, i
    else:
        return False, 0


def update_result(result, graph, v):
    new_graph = graph.copy()
    new_result = result.copy()
    w = graph[v][0]
    new_result[graph[w][1]] = graph[w][0]
    new_graph[w] = (w, graph[w][1])

    while w != v:
        w = graph[w][0]
        new_result[graph[w][1]] = graph[w][0]
        new_graph[w] = (w, graph[w][1])
    return new_result, new_graph


def ttc(profile, result, n):
    graph = {result[i]: (profile[i][0], i) for i in range(n)}
    new_result = result.copy()
    new_graph = graph.copy()
    for j in range(n):
        any_cycles = False
        for i in range(1, n+1):
            visited = [0] * (n + 1)
            has_cycle, v = dfs(new_graph, i, visited)
            if has_cycle:
                any_cycles = True
                new_result, new_graph = update_result(new_result, new_graph, v)
                break
        if not any_cycles:
            break
    return new_result