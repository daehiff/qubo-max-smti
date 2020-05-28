import unittest

from algorithms.solver.SMTI.shift_brk.shiftbrkmatching import ShiftBrkMatching
from algorithms.solver.SMP.std_smp import StandardSMP
from algorithms.solver.SMTI.shift_brk.shift_brk import ShiftBrk
from tests.mocks import mock_matching_smti


class ModelTest(unittest.TestCase):

    def test_shift_brk(self):
        matching = mock_matching_smti()
        brk_matching = ShiftBrkMatching(matching).break_preflists()
        self.assertEqual(StandardSMP(brk_matching).solve().is_stable(mode="smti"), (True, 3))
        self.assertEqual(ShiftBrk(matching).solve().is_stable(mode="smti"), (True, 3))

    def test_new_shiftbrk_model(self):
        matching = mock_matching_smti()
        brk_matching = ShiftBrkMatching(matching).break_preflists()

        ################################
        # std break
        ################################

        self.assertEqual(brk_matching.all_ties_m["M0"], [["W4", "W3"]])
        self.assertEqual(brk_matching.all_ties_m["M1"], [["W0", "W4"]])
        self.assertEqual(brk_matching.all_ties_m["M2"], [])
        self.assertEqual(brk_matching.all_ties_m["M4"], [["W0", "W1"]])
        self.assertEqual(brk_matching.all_ties_w["W0"], [])
        self.assertEqual(brk_matching.all_ties_w["W1"], [["M1", "M0"]])

        ################################
        # male shift
        ################################

        brk_matching_m = brk_matching.shift("m")
        self.assertEqual(brk_matching_m.males_pref["M0"], {'W4': 1, 'W3': 0})
        self.assertEqual(brk_matching_m.males_pref["M1"], {'W0': 1, 'W4': 0, 'W1': 2})
        self.assertEqual(brk_matching_m.females_pref, brk_matching.females_pref)
        self.assertEqual(brk_matching_m.females_pref.keys(), brk_matching.females_pref.keys())
        self.assertEqual(brk_matching_m.males_pref.keys(), brk_matching.males_pref.keys())
        self.assertNotEqual(brk_matching_m.males_pref, brk_matching.males_pref)

        ################################
        # female shift
        ################################

        brk_matching_w = brk_matching.shift("w")
        self.assertEqual(brk_matching_w.females_pref["W0"], {'M4': 0, 'M2': 1, 'M1': 2, 'M0': 3})
        self.assertEqual(brk_matching_w.females_pref["W1"], {'M3': 0, 'M1': 2, 'M0': 1})
        self.assertEqual(brk_matching_w.males_pref, brk_matching.males_pref)
        self.assertNotEqual(brk_matching_w.females_pref, brk_matching.females_pref)

        ################################
        # male shift #2
        ################################

        brk_matching_m_1 = brk_matching_m.shift("m")
        self.assertEqual(brk_matching_m_1.males_pref["M0"], {'W4': 0, 'W3': 1})
        self.assertEqual(brk_matching_m_1.males_pref["M1"], {'W0': 0, 'W4': 1, 'W1': 2})
        self.assertEqual(brk_matching_m_1.females_pref, brk_matching_m.females_pref)
        self.assertEqual(brk_matching_m_1.females_pref.keys(), brk_matching_m.females_pref.keys())
        self.assertEqual(brk_matching_m_1.males_pref.keys(), brk_matching_m.males_pref.keys())
        self.assertNotEqual(brk_matching_m_1.males_pref, brk_matching_m.males_pref)

        ################################
        # female shift #2
        ################################

        brk_matching_w_1 = brk_matching_w.shift("w")
        self.assertEqual(brk_matching_w_1.females_pref["W0"], {'M4': 0, 'M2': 1, 'M1': 2, 'M0': 3})
        self.assertEqual(brk_matching_w_1.females_pref["W1"], {'M3': 0, 'M1': 1, 'M0': 2})
        self.assertEqual(brk_matching_w_1.males_pref, brk_matching_w.males_pref)
        self.assertNotEqual(brk_matching_w_1.females_pref, brk_matching_w.females_pref)
