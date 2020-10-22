import numpy as np
import itertools


def calc_welfare(profile, result, n):
    welfare = 0
    for i in range(n):
        welfare += n - 1 - profile[i].index(result[i])
    return welfare


def get_yankee_swap_result(profile, n):
    res = [0]*n
    held = [set() for _ in range(n)]
    for i in range(n):
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
        held[curr_agent].add(item)
    return calc_welfare(profile, res, n), res


def get_best_welfare_result(profile, n):
    max_welfare = 0
    best_result = [i + 1 for i in range(n)]
    for res in itertools.permutations([i+1 for i in range(n)]):
        if calc_welfare(profile, res, n) > max_welfare:
            max_welfare = calc_welfare(profile, res, n)
            best_result = res
    return max_welfare, list(best_result)


def iterate_over_profiles(n):
    ys = 0
    best = 0
    ys_strategic = 0
    best_strategic = 0
    for i, profile in enumerate(itertools.product(itertools.permutations([i + 1 for i in range(n)]), repeat=n)):
        # print(profile)
        for agent in range(n):
            ys += get_yankee_swap_result(profile, n)[0]
            best += get_best_welfare_result(profile, n)[0]
            ys_strategic += strategic_behavior(profile, n, manipulator=agent)[0]
            best_strategic += strategic_behavior(profile, n, ys=False, manipulator=agent)[0]
    return "Yankee Swap: " + str(ys), "Max Welfare: " + str(best), "Yankee Swap with strategy: " + str(ys_strategic), \
           "Max Welfare with strategy: " + str(best_strategic)


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
    profile = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
    print(get_yankee_swap_result(profile, 3))
    print(get_best_welfare_result(profile, 3))
    print(strategic_behavior(profile, 3, manipulator=0))
    print(strategic_behavior(profile, 3, ys=False, manipulator=0))
    # print(strategic_behavior_best(profile, 3, manipulator=0))
    # print(strategic_behavior_best(profile, 3, ys=False, manipulator=0))
    # print(iterate_over_profiles(3))


if __name__ == "__main__":
    main()
