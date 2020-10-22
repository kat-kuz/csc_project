import assignments
import unittest


class AssignmentTestCase(unittest.TestCase):
    def test_ys(self):
        test_profile = ((2, 1, 3), (1, 2, 3), (1, 2, 3))
        self.assertEqual(assignments.get_yankee_swap_result(test_profile, 3), (2, [1, 3, 2]),
                         'wrong yankee swap result')

    def test_max_welfare(self):
        test_profile = ((2, 1, 3), (1, 2, 3), (1, 2, 3))
        self.assertEqual(assignments.get_best_welfare_result(test_profile, 3), (4, [2, 1, 3]),
                         'wrong max welfare result')

    def test_ys_after_manipulation(self):
        test_profile = ((1, 2, 3), (1, 2, 3), (1, 2, 3))
        self.assertEqual(assignments.strategic_behavior_best(test_profile, 3, manipulator=0, ys=True), (2, [1, 3, 2], [2, 1, 3]),
                         'wrong ys with manipulation result')

    def test_max_welfare_after_manipulation(self):
        test_profile = ((1, 2, 3), (1, 2, 3), (1, 2, 3))
        self.assertEqual(assignments.strategic_behavior_best(test_profile, 3, manipulator=0, ys=False), (3, [1, 2, 3], [1, 2, 3]),
                         'wrong max welfare with manipulation result')
