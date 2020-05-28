import unittest

import tests.mocks as mock
from algorithms.create_templates import create_smti_instance
from algorithms.maching import Matching
from algorithms.solver.SMTI.kiraly.kiralySMTI import Kirialy1, Kirialy2
from algorithms.solver.SMTI.kiraly.RGS import RGS
from algorithms.solver.SMTI.lp_smti import LP_smti


class SMTITest(unittest.TestCase):
    def test_new_prefers(self):
        matching = mock.mock_matching_smti()
        solver = RGS(matching, "m")
        self.assertEqual(matching.prefers("M0", "W4", "W3", mode="SCORE", sc_2=1, sc_3=3), False)
        self.assertEqual(matching.prefers("M0", "W3", "W4", mode="SCORE", sc_2=3, sc_3=1), True)
        self.assertEqual(matching.prefers("M0", "W4", "W3", mode="SCORE", sc_2=3, sc_3=1), True)
        self.assertEqual(matching.prefers("M4", "W2", "W3", mode="SCORE", sc_2=3, sc_3=1), True)
        self.assertEqual(matching.prefers("M4", "W2", "W3", mode="SCORE", sc_2=0, sc_3=0), True)
        self.assertEqual(matching.prefers("M4", "W3", "W2", mode="SCORE", sc_2=0, sc_3=0), False)

        self.assertEqual(solver.is_better_partner("M0", "W2", "W3"), False)
        self.assertEqual(solver.is_better_partner("M0", "W4", "W3"), False)

    def test_kirialy_1(self):
        matching = mock.mock_matching_smti(mock_nr=1)
        self.assertEqual(Kirialy1(matching).solve().is_stable(), (True, 3))

    def test_kirialy_2(self):
        for size in [5, 10, 15]:
            matching = create_smti_instance(size, 0.5, 0.5)
            solution = Kirialy2(matching).solve().is_stable()
            solution_lp = LP_smti(matching).solve().is_stable()
            self.assertTrue(solution[0])
            self.assertTrue(solution_lp[0])
            self.assertTrue(solution[1] <= solution_lp[1])
