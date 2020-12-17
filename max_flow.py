import random
import numpy as np


def hung_matrix(profile, n):
    m = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j, x in enumerate(profile[i]):
            m[i + 1][x] = j
    return m


def hungarian(a, n):
    u = [0]*(n+1)
    v = [0]*(n+1)
    p = [0]*(n+1)
    way = [0]*(n+1)
    for i in range(1, n+1):
        p[0] = i
        j0 = 0
        minv = [n+1]*(n+1)
        used = [False]*(n+1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = n+1
            for j in range(1, n+1):
                if not used[j]:
                    cur = a[i0][j] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(n+1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1

            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1

            if not j0:
                break

    ans = [0]*(n+1)
    for j in range(1, n+1):
        ans[p[j]] = j
    return n * n + v[0], ans[1:]


# n = 4
# np.random.seed(42)
# profile = [[1, 4, 3, 2], [1, 4, 3, 2], [1, 2, 4, 3], [2, 3, 1, 4]]
# profile_with_ind = [(profile[i], i) for i in range(n)]
# best_result = [[0] * n for _ in range(n)]
# size = 10
# for i in range(size):
#     new_profile_with_ind = np.random.permutation(profile_with_ind)
#     new_profile = [x[0] for x in new_profile_with_ind]
#     perm_result = hungarian(hung_matrix(new_profile, n), n)
#     new_result = [0]*n
#     for i in range(n):
#         best_result[new_profile_with_ind[i][1]][perm_result[1][i] - 1] += 1
#         new_result[new_profile_with_ind[i][1]] = perm_result[1][i]
#     print(new_result, best_result)
# best_result = [[best_result[i][j] / size for j in range(n)] for i in range(n)]
# print(best_result)

