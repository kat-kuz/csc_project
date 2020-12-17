import itertools
import numpy as np
from ttc import *
from max_flow import *


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


def calc_prob_welfare(profile, result, n):
    welfare = 0
    for i in range(n):
        utility = 0
        for j in range(n):
            utility += result[i][j] * (n - profile[i].index(j + 1))
        welfare += utility
    return welfare


def calc_egal_prob_welfare(profile, result, n):
    welfare = n
    for i in range(n):
        utility = 0
        for j in range(n):
            utility += result[i][j] * (n - profile[i].index(j + 1))
        welfare = min(utility, welfare)
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


def get_serial_dictatorship_result(profile, n, egal=False):
    res = [0] * n
    items = set()
    for i in range(n):
        for elem in profile[i]:
            if elem not in items:
                res[i] = elem
                items.add(elem)
                break
    if egal:
        return calc_egal_welfare(profile, res, n), res
    else:
        return calc_welfare(profile, res, n), res


def get_ys_ttc_result(profile, n, egal=False):
    w, res = get_yankee_swap_result(profile, n)
    ttc_res = ttc(profile, res, n)
    if egal:
        return calc_egal_welfare(profile, ttc_res, n), ttc_res
    else:
        return calc_welfare(profile, ttc_res, n), ttc_res


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


def get_best_welfare_max_flow_random_result(profile, n, egal=False):
    np.random.seed(42)
    profile_with_ind = [(profile[i], i) for i in range(n)]
    new_profile_with_ind = np.random.permutation(profile_with_ind)
    new_profile = [x[0] for x in new_profile_with_ind]
    perm_result = hungarian(hung_matrix(new_profile, n), n)
    new_result = [0] * n
    for i in range(n):
        new_result[new_profile_with_ind[i][1]] = perm_result[1][i]
    if egal:
        return calc_egal_welfare(profile, new_result, n), new_result
    else:
        return perm_result[0], new_result


def get_best_welfare_max_flow_result(profile, n, egal=False):
    res = hungarian(hung_matrix(profile, n), n)
    if egal:
        return calc_egal_welfare(profile, res[1], n), res[1]
    else:
        return res


def get_best_welfare_anonymous_result(profile, n, egal=False):
    max_welfare = 0
    best_result = [[0] * n for _ in range(n)]
    equal_results = 0
    for res in itertools.permutations([i+1 for i in range(n)]):
        curr_welfare = calc_welfare(profile, res, n)
        if curr_welfare == max_welfare:
            for i in range(n):
                best_result[i][res[i]-1] += 1
            equal_results += 1
        if calc_welfare(profile, res, n) > max_welfare:
            best_result = [[0] * n for _ in range(n)]
            equal_results = 1
            for i in range(n):
                best_result[i][res[i] - 1] = 1
            max_welfare = curr_welfare
    best_result = [[best_result[i][j] / equal_results for j in range(n)] for i in range(n)]
    if egal:
        return calc_egal_prob_welfare(profile, best_result, n), best_result
    else:
        return calc_prob_welfare(profile, best_result, n), best_result


def iterate_over_profiles(n, algo=get_yankee_swap_result, egal=False):
    total = 0
    total_strategic = 0
    total_strategic_pre_random = 0
    count = float(np.prod([i for i in range(1, n+1)])) ** n
    for i, profile in enumerate(itertools.product(itertools.permutations([i + 1 for i in range(n)]), repeat=n)):
        if i % 1000 == 0:
            print(i)
        total += algo(profile, n, egal)[0]
        if algo == get_best_welfare_anonymous_result:
            total_strategic_pre_random += pre_randomization_strategy_prob(profile, n, algo, egal=egal)[0]
        else:
            total_strategic_pre_random += pre_randomization_strategy(profile, n, algo, egal=egal)[0]
        for man in range(n):
            if algo == get_best_welfare_anonymous_result:
                total_strategic += post_randomization_strategy_prob(profile, n, algo, man, egal=egal)[0]
            else:
                total_strategic += post_randomization_strategy(profile, n, algo, man, egal=egal)[0]
    avg_result = total / count
    avg_post_random = total_strategic / count / n
    avg_pre_random = total_strategic_pre_random / count / np.prod([i for i in range(1, n+1)])
    return avg_result, avg_post_random, avg_pre_random


def generate_profile_ic(n):
    profile = [list(np.random.permutation(range(1, n+1))) for _ in range(n)]
    return profile


def iterate_over_random_profiles(n, count, algo=get_yankee_swap_result, egal=False):
    np.random.seed(42)
    avg_result = 0
    avg_result_strategic = 0
    avg_pre_random = 0
    for i in range(count):
        if i % 100 == 0:
            print(i)
        profile = generate_profile_ic(n)
        avg_result += algo(profile, n, egal)[0]
        if algo == get_best_welfare_anonymous_result:
            avg_pre_random += pre_randomization_strategy_prob(profile, n, algo, egal=egal)[0]
        else:
            avg_pre_random += pre_randomization_strategy(profile, n, algo, egal=egal)[0]
        for man in range(n):
            if algo == get_best_welfare_anonymous_result:
                avg_result_strategic += post_randomization_strategy_prob(profile, n, algo, egal=egal)[0]
            else:
                avg_result_strategic += post_randomization_strategy(profile, n, algo, egal=egal)[0]
    avg_result /= float(count)
    avg_result_strategic /= (float(count) * n)
    avg_pre_random /= (float(count) * np.prod([i for i in range(1, n+1)]))
    return avg_result, avg_result_strategic, avg_pre_random


def post_randomization_strategy(profile, n, algo=get_yankee_swap_result, manipulator=0, egal=False):
    best_result = algo(profile, n, egal)
    manipulator_utility = n - profile[manipulator].index(best_result[1][manipulator])
    welfare = best_result[0]
    best_strategy = profile[manipulator]
    for strategy in itertools.permutations([i + 1 for i in range(n)]):
        new_profile = list(profile)
        new_profile[manipulator] = strategy
        new_result = algo(new_profile, n, egal)
        if manipulator_utility < n - profile[manipulator].index(new_result[1][manipulator]):
            manipulator_utility = n - profile[manipulator].index(new_result[1][manipulator])
            if egal:
                welfare = calc_egal_welfare(profile, new_result[1], n)
            else:
                welfare = calc_welfare(profile, new_result[1], n)
            # welfare1 = new_result[0]
            best_result = new_result
            best_strategy = strategy
    return welfare, best_result[1], list(best_strategy)


def post_randomization_strategy_prob(profile, n, algo=get_best_welfare_anonymous_result, manipulator=0, egal=False):
    best_result = 0
    manipulator_utility = 0
    welfare = 0
    best_strategy = profile[manipulator]
    for strategy in itertools.permutations([i + 1 for i in range(n)]):
        new_profile = list(profile)
        new_profile[manipulator] = strategy
        new_result = algo(new_profile, n, egal)
        new_utility = 0
        for j in range(n):
            new_utility += new_result[1][manipulator][j] * (n - profile[manipulator].index(j + 1))
        if manipulator_utility < new_utility:
            manipulator_utility = new_utility
            if egal:
                welfare = calc_egal_prob_welfare(profile, new_result[1], n)
            else:
                welfare = calc_prob_welfare(profile, new_result[1], n)
            best_result = new_result
            best_strategy = strategy
    return welfare, best_result[1], list(best_strategy)


def pre_randomization_strategy(profile, n, algo=get_yankee_swap_result, egal=False):
    welfare = 0
    best_utility = 0
    best_strategy = profile[0]
    for strategy in itertools.permutations([i + 1 for i in range(n)]):
        curr_utility = 0
        profile_with_ind = [(x, i) if i != 0 else (strategy, 0) for i, x in enumerate(profile)]
        curr_welfare = 0
        for profile_order in itertools.permutations(profile_with_ind):
            curr_profile = [x[0] for x in profile_order]
            manipulator = profile_order.index((strategy, 0))
            curr_result = algo(curr_profile, n, egal)
            curr_utility += n - profile[0].index(curr_result[1][manipulator])
            curr_welfare += curr_result[0] - (n - curr_profile[manipulator].index(curr_result[1][manipulator])) \
                            + (n - profile[0].index(curr_result[1][manipulator]))
        if curr_utility > best_utility:
            best_utility = curr_utility
            best_strategy = strategy
            welfare = curr_welfare

        # print(strategy, curr_utility, curr_welfare)
    return welfare, list(best_strategy), best_utility


def pre_randomization_strategy_prob(profile, n, algo=get_best_welfare_anonymous_result, egal=False):
    welfare = 0
    best_utility = 0
    best_strategy = profile[0]
    for strategy in itertools.permutations([i + 1 for i in range(n)]):
        curr_utility = 0
        profile_with_ind = [(x, i) if i != 0 else (strategy, 0) for i, x in enumerate(profile)]
        curr_welfare = 0
        for profile_order in itertools.permutations(profile_with_ind):
            curr_profile = [x[0] for x in profile_order]
            manipulator = profile_order.index((strategy, 0))
            curr_result = algo(curr_profile, n, egal)
            true_utility = 0
            false_utility = 0
            for j in range(n):
                true_utility += curr_result[1][manipulator][j] * (n - profile[0].index(j + 1))
                false_utility += curr_result[1][manipulator][j] * (n - curr_profile[manipulator].index(j + 1))
            curr_utility += true_utility
            curr_welfare += curr_result[0] - false_utility + true_utility
        if curr_utility > best_utility:
            best_utility = curr_utility
            best_strategy = strategy
            welfare = curr_welfare

        # print(strategy, curr_utility, curr_welfare)
    return welfare, list(best_strategy), best_utility



def main():
    example_profile = [[1, 4, 3, 2], [1, 4, 3, 2], [1, 2, 4, 3], [2, 3, 1, 4]]

    egal = False
    n = 4
    sample_size = 10000

    print(iterate_over_random_profiles(n, sample_size, get_best_welfare_max_flow_result, egal))
    print(iterate_over_random_profiles(n, sample_size, get_yankee_swap_result, egal))
    print(iterate_over_random_profiles(n, sample_size, get_ys_ttc_result, egal))
    print(iterate_over_random_profiles(n, sample_size, get_serial_dictatorship_result, egal))

    print(iterate_over_profiles(n, get_best_welfare_max_flow_result, egal))
    print(iterate_over_profiles(n, get_yankee_swap_result, egal))
    print(iterate_over_profiles(n, get_ys_ttc_result, egal))
    print(iterate_over_profiles(n, get_serial_dictatorship_result, egal))




if __name__ == "__main__":
    main()
