
def get_cycle_vertex(graph, i, visited):
    visited[i] = 1
    if visited[graph[i][0]] == 0:
        return get_cycle_vertex(graph, graph[i][0], visited)
    else:
        return i


def update_state(res, graph, items_set, v, profile):
    items = items_set.copy()
    new_res = res.copy()
    w = graph[v][0]
    items.remove(w)
    new_res[graph[w][1]] = graph[w][0]
    while w != v:
        w = graph[w][0]
        items.remove(w)
        new_res[graph[w][1]] = graph[w][0]
    new_graph = {}
    for x in items:
        agent = new_res.index(x)
        for i in range(len(res)):
            if profile[agent][i] in items:
                new_graph[x] = (profile[agent][i], agent)
                break
    return new_res, new_graph, items


def ttc(profile, result, n):
    items_set = set(range(1, n+1))
    graph = {result[i]: (profile[i][0], i) for i in range(n)}
    while len(items_set) > 0:
        visited = [0] * (n + 1)
        v = get_cycle_vertex(graph, next(iter(items_set)), visited)
        result, graph, items_set = update_state(result, graph, items_set, v, profile)
    return result
