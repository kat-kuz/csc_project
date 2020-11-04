import numpy as np
import itertools


def calc_welfare(profile, result, n):
    welfare = 0
    for i in range(n):
        welfare += n - profile[i].index(result[i])
    return welfare


def calc_egal_welfare(profile, result, n):
    welfare = n
    for i in range(n):
        welfare = min(welfare, n - profile[i].index(result[i]))
    return welfare


def get_yankee_swap_result(profile, n, egal=False):
    res = [0] * n
    for i in range(n):
        held = [set() for _ in range(n)]
        for j in range(n):
            if res[j] != 0:
                held[j].add(res[j])
        item = profile[i][0]
        curr_agent = i
        while item in res:
            next_agent = res.index(item)
            res[curr_agent] = item
            held[curr_agent].add(item)
            curr_agent = next_agent
            for pref in profile[curr_agent]:
                if pref not in held[curr_agent]:
                    item = pref
                    break
        res[curr_agent] = item
    if egal:
        return calc_egal_welfare(profile, res, n), res
    else:
        return calc_welfare(profile, res, n), res


def get_best_welfare_result(profile, n, egal=False):
    max_welfare = 0
    best_result = [i + 1 for i in range(n)]
    for res in itertools.permutations([i+1 for i in range(n)]):
        if calc_welfare(profile, res, n) > max_welfare:
            max_welfare = calc_welfare(profile, res, n)
            best_result = res
    if egal:
        return calc_egal_welfare(profile, best_result, n), list(best_result)
    else:
        return max_welfare, list(best_result)


def iterate_over_profiles(n, egal=False):
    ys = 0
    best = 0
    for i, profile in enumerate(itertools.product(itertools.permutations([i + 1 for i in range(n)]), repeat=n)):
        best_result = get_best_welfare_result(profile, n, egal)
        ys_result = get_yankee_swap_result(profile, n, egal)
        with open('best_result_3.txt', 'a') as f:
            f.write('\n'.join(map(str, list(profile))) + '\n')
            f.write(str(best_result[1]) + ' ' + str(best_result[0]) + '\n\n')
        with open('ys_result_3.txt', 'a') as f:
            f.write('\n'.join(map(str, list(profile))) + '\n')
            f.write(str(ys_result[1]) + ' ' + str(ys_result[0]) + '\n\n')
        best += best_result[0]
        ys += ys_result[0]
    return ys, best


def strategic_behavior(profile, n, ys=True, manipulator=0):
    if ys:
        curr_result = get_yankee_swap_result(profile, n)
    else:
        curr_result = get_best_welfare_result(profile, n)
    manipulator_utility = n - 1 - profile[manipulator].index(curr_result[1][manipulator])
    welfare = curr_result[0]
    best_strategy = profile[manipulator]
    for strategy in itertools.permutations([i + 1 for i in range(n)]):
        new_profile = list(profile)
        new_profile[manipulator] = strategy
        if ys:
            new_result = get_yankee_swap_result(new_profile, n)
        else:
            new_result = get_best_welfare_result(new_profile, n)
        if manipulator_utility < n - 1 - profile[manipulator].index(new_result[1][manipulator]):
            welfare = new_result[0]
            curr_result = new_result
            best_strategy = strategy
            break
    return welfare, curr_result[1], list(best_strategy)


def strategic_behavior_best(profile, n, ys=True, manipulator=0):
    if ys:
        best_result = get_yankee_swap_result(profile, n)
    else:
        best_result = get_best_welfare_result(profile, n)
    manipulator_utility = n - 1 - profile[manipulator].index(best_result[1][manipulator])
    welfare = best_result[0]
    best_strategy = profile[manipulator]
    for strategy in itertools.permutations([i + 1 for i in range(n)]):
        new_profile = list(profile)
        new_profile[manipulator] = strategy
        if ys:
            new_result = get_yankee_swap_result(new_profile, n)
        else:
            new_result = get_best_welfare_result(new_profile, n)
        if manipulator_utility < n - 1 - profile[manipulator].index(new_result[1][manipulator]):
            manipulator_utility = n - 1 - profile[manipulator].index(new_result[1][manipulator])
            welfare = new_result[0]
            best_result = new_result
            best_strategy = strategy
    return welfare, best_result[1], list(best_strategy)


def main():
    print(iterate_over_profiles(3))


if __name__ == "__main__":
    main()