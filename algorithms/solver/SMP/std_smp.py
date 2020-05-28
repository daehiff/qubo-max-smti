from copy import deepcopy

from algorithms.maching import Matching
from algorithms.solution import Solution
from collections import deque


def _get_most_desired(pref_list, proposed):
    m_most_desired = None
    for m_prefs in pref_list.keys():
        if m_most_desired is None or pref_list[m_prefs] < pref_list[m_most_desired]:
            if m_prefs not in proposed:
                m_most_desired = m_prefs
    return m_most_desired


class StandardSMP:
    def __init__(self, matching, mode="m_opt"):
        self.mode = mode
        if mode == "m_opt":
            self.matching = matching
        elif mode == "w_opt":
            self.matching = Matching(matching.females, matching.males, matching.females_pref, matching.males_pref)
        else:
            raise Exception(f"unknown mode: {mode}")

    def get_active(self):
        return self.matching.males

    def is_better_partner(self, p_1, p_2, p_3):
        """
        Check if p_2 would be a better partner for p_1 in comparison to p_3
        :param p_1:
        :param p_2:
        :param p_3:
        :return:
        """
        return self.matching.prefers(p_1, p_2, p_3) and self.matching.is_acceptable(p_1, p_2)

    def solve(self):
        matches_m = {}
        matches_w = {}
        proposal_m = {m: [] for m in self.matching.males}
        unmatched_males = deque(self.get_active())

        m_pref = deepcopy(self.matching.males_pref)
        while not len(unmatched_males) == 0:
            m_alone = unmatched_males[0]
            most_desired = _get_most_desired(m_pref[m_alone], proposal_m[m_alone])
            if most_desired is None:
                unmatched_males.remove(m_alone)
                continue
            proposal_m[m_alone].append(most_desired)
            if most_desired not in matches_w.keys():
                if self.matching.is_acceptable(m_alone, most_desired):
                    matches_w[most_desired] = m_alone
                    matches_m[m_alone] = most_desired
                    unmatched_males.remove(m_alone)

            else:
                if self.is_better_partner(most_desired, m_alone, matches_w[most_desired]):
                    unmatched_males.remove(m_alone)
                    unmatched_males.append(matches_w[most_desired])
                    proposal_m[matches_w[most_desired]].append(most_desired)
                    del matches_m[matches_w[most_desired]]
                    matches_w[most_desired] = m_alone
                    matches_m[m_alone] = most_desired
                else:
                    unmatched_males.rotate(1)
        if self.mode == "m_opt":
            return Solution(self.matching, matches_m)
        elif self.mode == "w_opt":
            matching = Matching(self.matching.females, self.matching.males, self.matching.females_pref,
                                self.matching.males_pref)
            return Solution(matching, matches_w)

        else:
            raise Exception(f"unknown mode: {self.mode}")
