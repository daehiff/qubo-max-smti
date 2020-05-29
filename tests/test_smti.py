import unittest

from algorithms.create_templates import create_smp_instance, create_smti_instance
import numpy as np

from algorithms.solver.SMP.qubo_smp import QbsolvSMP
from algorithms.solver.SMTI.lp_smti import LP_smti


class SMTITest(unittest.TestCase):

    def test_smp_qubo(self):
        sizes = [3, 4, 5, 6]
        for size in sizes:
            matching = create_smp_instance(size)
            solver = QbsolvSMP(matching)
            solver.create_qubo()
            n = solver.matching.size
            solution = solver.solve(verbose=False, num_repeats=300)

            print(size, solution.is_stable())
            self.assertTrue(solution.is_stable(mode="smp")[0])
            self.assertEqual(solution.is_stable()[1], solution.size)

    def test_smp_qubo_np_bqm(self):
        sizes = [5]
        for size in sizes:
            matching = create_smp_instance(size)
            solver = QbsolvSMP(matching, mode="np")
            solver.create_qubo()
            solver_1 = QbsolvSMP(matching, mode="bqm")
            solver_1.create_qubo()
            self.assertTrue(np.array_equal(solver.qubo, solver_1.qubo.to_numpy_matrix()))

    def test_smp_qubo_target(self):
        sizes = [10, 15, 20]
        for size in sizes:
            matching = create_smp_instance(size)
            solver = QbsolvSMP(matching)
            solver.create_qubo()
            n = solver.matching.size
            solution = solver.solve(verbose=False, target=-1.5 * n * (n - 1))

            print(size, solution.is_stable())
            self.assertTrue(solution.is_stable(mode="smp")[0])
            self.assertEqual(solution.is_stable()[1], solution.size)

    def test_lp_smti(self):
        sizes = [5, 6, 7, 8, 9, 10, 11, 12]
        for size in sizes:
            matching = create_smp_instance(size)
            solver = LP_smti(matching)
            solver.pre_process()
            solution = solver.solve(verbose=False)
            self.assertTrue(solution.is_stable()[0])
            self.assertEqual(solution.is_stable()[1], solution.size)
