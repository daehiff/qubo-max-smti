import itertools
import unittest

from algorithms.create_templates import create_smp_instance, create_smti_instance
from algorithms.solution import Solution
from algorithms.solver.SMP.qubo_smp import QbsolvSMP
from algorithms.solver.SMP.std_smp import StandardSMP
from algorithms.solver.SMTI.lp_smti import LP_smti
from algorithms.solver.SMTI.qubo_smti import QbsolvSMTI
from tests.utils import mocks as mock
import algorithms.utils as ut
from tests.utils.mocks import mock_matching_smti, mock_matching_smp
import math


class ModelTest(unittest.TestCase):

    def test_matching_model(self):
        #####################################################################
        # SMTI TESTS
        #####################################################################
        matching = mock_matching_smti()
        self.assertTrue(matching.prefers("W0", "M4", "M1"))
        self.assertTrue(matching.prefers("M0", "W4", "W3", mode="NOT_STRICT"))
        self.assertFalse(matching.prefers("M0", "W4", "W3"))
        self.assertEqual(matching.get_index("W4", "M0"), 0)
        self.assertEqual(matching.get_index("M0", "W4"), None)
        self.assertEqual(matching.get_index("M0", "W4", fallback=-1), -1)
        self.assertTrue(matching.is_acceptable("M1", "W0"))
        self.assertTrue(matching.is_acceptable("W0", "M1"))
        self.assertFalse(matching.is_acceptable("W2", "M0"))
        self.assertFalse(matching.is_acceptable("M0", "W2"))
        self.assertEqual(matching.get_preference_list("W0"), mock.females_pref_smti["W0"])
        self.assertEqual(matching.get_preference_list("M0"), mock.males_pref_smti["M0"])
        self.assertEqual(matching.get_max_tie_len(), (2, 2))
        with self.assertRaises(Exception):
            self.assertRaises(matching.get_at_index("M0", 10))
            self.assertRaises(matching.get_next_after_index("M0", 10))

        #####################################################################
        # SMP TESTS
        #####################################################################
        matching = mock_matching_smp()
        self.assertEqual(matching.get_max_tie_len(), (1, 1))

        self.assertEqual(matching.get_at_index("M1", 0), ("W2", 0))
        self.assertEqual(matching.get_at_index("M1", 3), ("W3", 3))
        for w_index_m in range(len(matching.males)):
            (_, next_index) = (matching.get_next_after_index("M1", w_index_m))
            self.assertEqual(w_index_m + 1,
                             next_index)  # in SMP get_next_after_index should always return the partner one better

    def test_smp_gs(self):
        sizes = [5, 6, 7, 8, 9, 10]
        for size in sizes:
            matching = create_smp_instance(size)

            solution_m = StandardSMP(matching).solve()
            solution_w = StandardSMP(matching, mode="w_opt").solve()
            self.assertTrue(solution_m.is_stable()[0])
            self.assertTrue(solution_w.is_stable()[0])
            self.assertEqual(solution_m.is_stable()[1], solution_m.size)
            self.assertEqual(solution_w.is_stable()[1], solution_w.size)

    def test_matching_and_solution(self):
        matching = mock_matching_smti()
        solution = Solution(matching, mock.smti_instance_solution)
        self.assertEqual(solution.get_partner("M0"), "W3")
        self.assertEqual(solution.get_partner("M1"), "W0")
        self.assertEqual(solution.get_partner("M2"), None)
        self.assertEqual(solution.is_free("M2"), True)
        self.assertEqual(solution.is_free("M1"), False)
        self.assertEqual(solution.is_acceptable("M1", "W0"), True)
        self.assertEqual(solution.is_acceptable("M1", "M2"), False)
        self.assertEqual(solution.is_blocking("M1", "M2", "smti"), False)
        self.assertEqual(solution.get_blocking_pairs("smti"), [])
        self.assertEqual(solution.is_stable("smti"), (True, 3))
        self.assertTrue(solution.is_stable()[0])
        matching = mock_matching_smp()

        matches = mock.smp_solution
        solution = Solution(matching, matches)
        gs_solution = StandardSMP(matching).solve()
        qubo_solution = QbsolvSMP(matching).solve()
        qubo_smti_solution = QbsolvSMTI(matching).solve()
        qubo_lp_solution = LP_smti(matching).solve()
        self.assertEqual(solution.is_stable("smp"), (True, 5))
        self.assertEqual(solution.is_stable("smti"), (True, 5))  # for smp instances, both methods are supposed to work
        self.assertEqual(solution.get_solution(), gs_solution.get_solution())
        self.assertEqual(qubo_solution.is_stable("smp"), (True, 5))

        # self.assertEqual(qubo_smti_solution.is_stable("smp"), (True, 5))
        self.assertEqual(qubo_smti_solution.is_stable("smti"), (True, 5))

        # self.assertEqual(qubo_lp_solution.is_stable("smp"), (True, 5))
        self.assertEqual(qubo_lp_solution.is_stable("smti"), (True, 5))

    def test_generate_all_solutions_smti(self):
        def compute_solution_count(n):
            return sum([math.comb((n * n), i) for i in range(1, n + 1)])

        for size in range(5):
            matching = create_smti_instance(size, 0.5, 0.5)
            all_possibilites = ut.get_all_matches(matching.males, matching.females, matching.size)
            self.assertEqual(compute_solution_count(size), len(all_possibilites))
            matching.compute_all_solutions()
            for match in matching.solutions:
                (stable, s_size) = Solution(matching, match).is_stable()
                self.assertTrue(stable, "solution was not stable")
                self.assertTrue(s_size <= size, "solution size was bigger then expected")
                self.assertTrue(size != -1, "solution had somebody matched twice")

        matching = mock_matching_smti(2)
        matching.compute_all_solutions()
        self.assertEqual(2, len(matching.solutions))

    def test_generate_all_solutions_smp(self):
        for size in range(5):
            matching = create_smp_instance(size)
            all_possibilites = ut.get_all_matches(matching.males, matching.females, matching.size, mode="SMP")
            self.assertEqual(math.factorial(size), len(all_possibilites))
            matching.compute_all_solutions(mode="SMP")
            for match in matching.solutions:
                (stable, s_size) = Solution(matching, match).is_stable()
                self.assertTrue(stable, "solution was not stable")
                self.assertTrue(s_size == size, "solution differed in size")
                self.assertTrue(size != -1, "solution had somebody matched twice")

        matching = mock_matching_smp()
        matching.compute_all_solutions()
        self.assertEqual(2, len(matching.solutions))
