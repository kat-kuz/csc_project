import assignments
import unittest


class AssignmentTestCase(unittest.TestCase):
    def test_ys_1(self):
        test_profile = [[1, 2, 3], [2, 3, 1], [1, 2, 3]]
        self.assertEqual(assignments.get_yankee_swap_result(test_profile, 3), (7, [2, 3, 1]),
                         'wrong yankee swap result')

    def test_ys_2(self):
        test_profile = [[2, 3, 1], [1, 2, 3], [2, 1, 3]]
        self.assertEqual(assignments.get_yankee_swap_result(test_profile, 3), (8, [3, 1, 2]),
                         'wrong yankee swap result')

    def test_ys_3(self):
        test_profile = [[2, 1, 3], [3, 2, 1], [1, 2, 3]]
        self.assertEqual(assignments.get_yankee_swap_result(test_profile, 3), (9, [2, 3, 1]),
                         'wrong yankee swap result')

    def test_ys_4(self):
        test_profile = [[3, 2, 1], [1, 3, 2], [1, 3, 2]]
        self.assertEqual(assignments.get_yankee_swap_result(test_profile, 3), (7, [2, 3, 1]),
                         'wrong yankee swap result')

    def test_ys_5(self):
        test_profile = [[2, 3, 1], [1, 3, 2], [3, 2, 1]]
        self.assertEqual(assignments.get_yankee_swap_result(test_profile, 3), (9, [2, 1, 3]),
                         'wrong yankee swap result')

    def test_ys_6(self):
        test_profile = [[2, 4, 1, 3], [2, 4, 1, 3], [4, 1, 2, 3], [2, 1, 4, 3]]
        self.assertEqual(assignments.get_yankee_swap_result(test_profile, 4), (7, [3, 1, 2, 4]),
                         'wrong yankee swap result')

    def test_ys_7(self):
        test_profile = [[3, 2, 1, 4], [1, 2, 3, 4], [4, 3, 2, 1], [1, 3, 2, 4]]
        self.assertEqual(assignments.get_yankee_swap_result(test_profile, 4), (15, [3, 2, 4, 1]),
                         'wrong yankee swap result')

    def test_ys_8(self):
        test_profile = [[4, 3, 1, 2], [1, 3, 2, 4], [2, 3, 4, 1], [2, 1, 4, 3]]
        self.assertEqual(assignments.get_yankee_swap_result(test_profile, 4), (15, [4, 1, 3, 2]),
                         'wrong yankee swap result')

    def test_ys_9(self):
        test_profile = [[1, 4, 3, 2], [1, 4, 3, 2], [1, 2, 4, 3], [2, 3, 1, 4]]
        self.assertEqual(assignments.get_yankee_swap_result(test_profile, 4), (12, [3, 1, 4, 2]),
                         'wrong yankee swap result')

    def test_ys_10(self):
        test_profile = [[2, 4, 3, 1], [2, 3, 4, 1], [3, 4, 1, 2], [1, 3, 4, 2]]
        self.assertEqual(assignments.get_yankee_swap_result(test_profile, 4), (15, [4, 2, 3, 1]),
                         'wrong yankee swap result')

    def test_max_welfare_1(self):
        test_profile = [[1, 2, 3], [2, 3, 1], [1, 2, 3]]
        self.assertEqual(assignments.get_best_welfare_result(test_profile, 3), (7, [1, 2, 3]),
                         'wrong max welfare result')

    def test_max_welfare_2(self):
        test_profile = [[2, 3, 1], [1, 2, 3], [2, 1, 3]]
        self.assertEqual(assignments.get_best_welfare_result(test_profile, 3), (8, [3, 1, 2]),
                         'wrong max welfare result')

    def test_max_welfare_3(self):
            test_profile = [[2, 1, 3], [3, 2, 1], [1, 2, 3]]
            self.assertEqual(assignments.get_best_welfare_result(test_profile, 3), (9, [2, 3, 1]),
                             'wrong max welfare result')

    def test_max_welfare_4(self):
        test_profile = [[3, 2, 1], [1, 3, 2], [1, 3, 2]]
        self.assertEqual(assignments.get_best_welfare_result(test_profile, 3), (7, [2, 1, 3]),
                         'wrong max welfare result')

    def test_max_welfare_5(self):
        test_profile = [[2, 3, 1], [1, 3, 2], [3, 2, 1]]
        self.assertEqual(assignments.get_best_welfare_result(test_profile, 3), (9, [2, 1, 3]),
                         'wrong max welfare result')

    def test_max_welfare_6(self):
        test_profile = [[2, 4, 1, 3], [2, 4, 1, 3], [4, 1, 2, 3], [2, 1, 4, 3]]
        self.assertEqual(assignments.get_best_welfare_result(test_profile, 4), (12, [2, 3, 4, 1]),
                         'wrong max welfare result')

    def test_max_welfare_7(self):
        test_profile = [[3, 2, 1, 4], [1, 2, 3, 4], [4, 3, 2, 1], [1, 3, 2, 4]]
        self.assertEqual(assignments.get_best_welfare_result(test_profile, 4), (15, [3, 2, 4, 1]),
                         'wrong max welfare result')

    def test_max_welfare_8(self):
        test_profile = [[4, 3, 1, 2], [1, 3, 2, 4], [2, 3, 4, 1], [2, 1, 4, 3]]
        self.assertEqual(assignments.get_best_welfare_result(test_profile, 4), (15, [4, 1, 3, 2]),
                         'wrong max welfare result')

    def test_max_welfare_9(self):
        test_profile = [[1, 4, 3, 2], [1, 4, 3, 2], [1, 2, 4, 3], [2, 3, 1, 4]]
        self.assertEqual(assignments.get_best_welfare_result(test_profile, 4), (13, [1, 4, 2, 3]),
                         'wrong max welfare result')

    def test_max_welfare_10(self):
        test_profile = [[2, 4, 3, 1], [2, 3, 4, 1], [3, 4, 1, 2], [1, 3, 4, 2]]
        self.assertEqual(assignments.get_best_welfare_result(test_profile, 4), (15, [4, 2, 3, 1]),
                         'wrong max welfare result')
