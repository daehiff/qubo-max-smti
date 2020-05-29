import unittest

from algorithms.create_templates import create_and_save_smp, create_and_save_smti
from algorithms.storage import get_smti, get_smp


class SMTITest(unittest.TestCase):
    def test_storage_smti(self):
        size = 5
        p1 = 0.5
        p2 = 0.5
        num = 100

        for index_f in range(num):
            m_created = create_and_save_smti(index_f, size, p1, p2)
            m_read = get_smti(index_f, size)
            self.assertEqual(m_created.males, m_read.males)
            self.assertEqual(m_created.females, m_read.females)
            self.assertEqual(m_created.males_pref, m_read.males_pref)
            self.assertEqual(m_created.females_pref, m_read.females_pref)
            self.assertEqual(m_created.solutions, m_read.solutions)
            self.assertEqual(m_created.size, m_read.size)
            self.assertEqual(m_read.meta, {"p1": p1, "p2": p2})

    def test_storage_smp(self):
        size = 5
        num = 100

        for index_f in range(num):
            m_created = create_and_save_smp(index_f, size)
            m_read = get_smp(index_f, size)
            self.assertEqual(m_created.males, m_read.males)
            self.assertEqual(m_created.females, m_read.females)
            self.assertEqual(m_created.males_pref, m_read.males_pref)
            self.assertEqual(m_created.females_pref, m_read.females_pref)
            self.assertEqual(m_created.solutions, m_read.solutions)
            self.assertEqual(m_created.size, m_read.size)
