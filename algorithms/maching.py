import collections
import itertools
import operator
from copy import deepcopy
import algorithms.utils as ut


class Matching:
    def __init__(self, males, females, males_pref, females_pref, solutions=None):
        self.size = len(males)
        self.males = males
        self.females = females
        self.males_pref = males_pref
        self.females_pref = females_pref
        if solutions is None:
            self.solutions = []
        else:
            self.solutions = solutions

    def get_preference_list(self, person):
        """
        Get the preference list of a Person
        :param person:
        :return:
        """
        if person in self.males:
            return self.males_pref[person]
        else:
            return self.females_pref[person]

    def prefers(self, p_1, p_2, p_3, mode="STRICT", sc_2=0, sc_3=0):
        """
        determine if p_1 prefers p_2 over p_3
        The mode decides wether to use strict or not strict preferences
        :param sc_3: score of person 3 for scored mode, else it will not have any effekt
        :param sc_2: score of p2  - "" -
        :param mode: STRICT | NOT_STRICT | SCORE
        :param p_1:
        :param p_2:
        :param p_3:
        :return:
        """
        index_p1_p2 = self.get_index(p_2, p_1, fallback=None)
        index_p1_p3 = self.get_index(p_3, p_1, fallback=None)
        if index_p1_p2 is None and index_p1_p3 is None:
            return False
        elif index_p1_p2 is None:
            return False
        elif index_p1_p3 is None:
            return True

        if mode == "STRICT":
            return index_p1_p2 < index_p1_p3
        elif mode == "NOT_STRICT":
            return index_p1_p2 <= index_p1_p3
        elif mode == "SCORE":
            if index_p1_p2 < index_p1_p3:
                return True
            elif index_p1_p2 == index_p1_p3:
                return sc_2 > sc_3
            elif index_p1_p2 > index_p1_p3:
                return False
            else:
                raise Exception(f"un allowed condition")  # should ob not happen, just to verify
        else:
            raise Exception(f"unknown mode: {mode}")

    def is_acceptable(self, p1, p2):
        """
        check if two persons are acceptable
        both have the opposite on the preference list
        :param p1:
        :param p2:
        :return:
        """
        return self.get_index(p1, p2) is not None and self.get_index(p2, p1) is not None

    def get_index(self, person_1, person_2, fallback=None):
        """
        get the pref index of person_1 on person_2s preflist

        :param fallback: fallback value
        :param person_1:
        :param person_2:
        :return:
        """
        pref_p2 = self.get_preference_list(person_2)
        if person_1 in pref_p2.keys():
            return self.get_preference_list(person_2)[person_1]
        else:
            return fallback

    def prepare_sat_smti(self):
        """
        Little helper that sorts perference lists by values
        :return:
        """
        self.males_pref = {m: dict(sorted(x.items(), key=operator.itemgetter(1))) for m, x in self.males_pref.items()}
        self.females_pref = {m: dict(sorted(x.items(), key=operator.itemgetter(1))) for m, x in
                             self.females_pref.items()}

    def get_prefered(self, person, person_1):
        """
        get all persons that person perfers over person_1
        :param person:
        :param person_1:
        :return:
        """
        if person in self.males:
            assert person_1 in self.females
            return {female: index for index, female in enumerate(self.females) if
                    self.prefers(person, female, person_1, mode="NOT_STRICT")
                    and self.is_acceptable(female, person)}
        elif person in self.females:
            assert person_1 in self.males
            return {male: index for index, male in enumerate(self.males)
                    if self.prefers(person, male, person_1, mode="NOT_STRICT")
                    and self.is_acceptable(male, person)}

    def get_at_index(self, person, index):
        """
        get the person, that is currently at the index (enumeration of keys)
        of the perf-list
        :param person: m/w, owner of the perflist
        :param index: index where the person is supposed to be
        :return: None if the idx references the last element of the preflist
        :raise: Exeption if the index >= the pref list len
        """
        pref_list = self.get_preference_list(person)
        if index >= len(pref_list):
            raise Exception("Index must be <= the current preflist len")
        for w, idx in pref_list.items():
            if idx == index:
                return w, idx
        return None, len(pref_list)

    def get_rank(self, p_1, p_2):
        """
        get the rank of p_2 on p_1s preference list
        (rank can vary for ties in difference to index)
        asserted:
            - p_2 in p_1s preflist
            - preflist is sorted TODO matching internal state?
            - get rank of an acceptable pair should never return None
        :param p_1:
        :param p_2:
        :return:
        """
        pref_list = self.get_preference_list(p_1)
        assert p_2 in pref_list.keys()

        if not ut.is_sorted(list(pref_list.values())):
            raise Exception(f"Preflist should be presorted: {pref_list}")
        for p_2_, rank in pref_list.items():
            if p_2_ == p_2:
                return rank

        if self.is_acceptable(p_1, p_2):
            raise Exception(f"Acceptable Pairs should always match: {p_1, p_2}")
        return None

    def get_next_strictly_preferred(self, p_1, p_2):
        """
        Get the next person, that is strclty not pre
        :param p_1:
        :param p_2:
        :return:
        """
        index = self.get_rank(p_2, p_1)
        for p_2_ in (self.get_preference_list(p_1).keys()):
            index_plus = self.get_index(p_2_, p_1)
            if self.prefers(p_1, p_2, p_2_, mode="STRICT"):
                assert (index < index_plus)
                return index_plus
        index_plus = len(self.get_preference_list(p_1))
        assert (index < index_plus)
        return index_plus

    def get_next_after_index(self, person, index, p_mode="STRICT"):
        """
        :param p_mode: Preference Mode: See prefers@
        :param person:
        :param index:
        :return:
        """
        (w, idx) = self.get_at_index(person, index)
        if w is None:
            return w, idx  # was last element in preflist
        else:
            pref_list = self.get_preference_list(person)
            for w_idx, w_ in enumerate(pref_list.keys()):
                if self.prefers(person, w, w_, mode=p_mode):
                    return w_, w_idx
            return None, len(pref_list)

    def get_max_tie_len(self):
        male_max_size = 1
        female_max_size = 1
        for male in self.males:
            prev_val = None
            max_size = 0
            for value in self.males_pref[male].values():
                if prev_val is None or value == prev_val:
                    max_size += 1
                else:
                    if male_max_size < max_size:
                        male_max_size = max_size
                    max_size = 1
                prev_val = value
            if male_max_size < max_size:
                male_max_size = max_size

        for female in self.females:
            prev_val = None
            max_size = 0
            for value in self.females_pref[female].values():
                if prev_val is None or value == prev_val:
                    max_size += 1
                else:
                    if female_max_size < max_size:
                        female_max_size = max_size
                    max_size = 1
                prev_val = value
            if female_max_size < max_size:
                female_max_size = max_size
        return male_max_size, female_max_size

    def clone(self):
        return Matching(deepcopy(self.males), deepcopy(self.females), deepcopy(self.males_pref),
                        deepcopy(self.females_pref))

    def get_preference_lists_len(self, mode):
        assert mode == "m" or mode == "w"
        pref_len = []
        for person in self.males if mode == "m" else self.females:
            pref_len.append(len(self.get_preference_list(person).keys()))
        return pref_len

    def get_preference_tie_lenght(self, mode):
        tie_lenght = []
        for person in self.males if mode == "m" else self.females:
            tie_len = 0
            prev_index = None
            pref_list = dict(sorted(self.get_preference_list(person).items(), key=lambda x: x[1]))
            for other_p, index in pref_list.items():
                if prev_index == index:
                    tie_len += 1
                elif prev_index != index:
                    prev_index = index
                    tie_lenght.append(tie_len)
            tie_lenght.append(tie_len)
        return tie_lenght

    def compute_all_solutions(self, mode="SMTI"):
        from algorithms.solution import Solution
        if mode == "SMTI":
            all_matches = ut.get_all_matches(self.males, self.females, self.size, mode="SMTI")
            all_solutions = []
            for match in all_matches:
                (stable, size) = Solution(self, match).is_stable()
                if stable:
                    all_solutions.append(match)

            self.solutions = [dict(s) for s in set(frozenset(d.items()) for d in all_solutions)]
        elif mode == "SMP":
            all_comb = ut.get_all_matches(self.males, self.females, self.size, mode="SMP")
            all_solutions = []
            for match in all_comb:
                (stable, size) = Solution(self, match).is_stable()
                if stable:
                    all_solutions.append(match)
            self.solutions = all_solutions

        else:
            raise Exception(f"Mode: {mode} not implemented jet")
