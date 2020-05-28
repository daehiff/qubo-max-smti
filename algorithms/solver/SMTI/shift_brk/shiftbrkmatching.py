from copy import deepcopy

from algorithms.maching import Matching


class ShiftBrkMatching(Matching):
    def __init__(self, matching, all_ties_m=None, all_ties_w=None):
        super().__init__(deepcopy(matching.males), deepcopy(matching.females), deepcopy(matching.males_pref),
                         deepcopy(matching.females_pref))
        self.all_ties_m = {} if all_ties_m is None else all_ties_m
        self.all_ties_w = {} if all_ties_w is None else all_ties_w

    def break_preflists(self):
        for male in self.males:
            p_list, ties = self.__get_broken_preflist(male)
            self.males_pref[male] = p_list
            self.all_ties_m[male] = ties

        for female in self.females:
            p_list, ties = self.__get_broken_preflist(female)
            self.females_pref[female] = p_list
            self.all_ties_w[female] = ties
        return self

    def shift(self, mode):
        if mode == "m":
            new_pref_list, new_ties = self.__shift(mode)
            return self.from_shiftbrk(self.males, self.females, new_pref_list, self.females_pref,
                                      new_ties, self.all_ties_w)
        elif mode == "w":
            new_pref_list, new_ties = self.__shift(mode)
            return self.from_shiftbrk(self.males, self.females, self.males_pref, new_pref_list,
                                      self.all_ties_m, new_ties)

        else:
            raise Exception(f"unknown mode {mode}")

    def get_ties(self, mode):
        if mode == "m":
            return self.all_ties_m
        elif mode == "w":
            return self.all_ties_w
        else:
            raise Exception(f"unknown mode {mode}")

    def get_preferences(self, mode):
        if mode == "m":
            return self.males_pref
        elif mode == "w":
            return self.females_pref
        else:
            raise Exception(f"unknown mode {mode}")

    def __shift(self, mode):
        preference_list = deepcopy(self.get_preferences(mode))
        new_ties = {}
        for person, ties in self.get_ties(mode).items():
            for tie in ties:
                tmp_ties = deepcopy(tie)
                tmp = tmp_ties.pop(0)
                tmp_idx = preference_list[person][tmp]

                for other_p in tmp_ties:
                    tmp_idx_1 = preference_list[person][other_p]
                    preference_list[person][other_p] = tmp_idx
                    tmp_idx = tmp_idx_1
                tmp_ties.append(tmp)
                preference_list[person][tmp] = tmp_idx
            new_ties[person] = ties

        return preference_list, new_ties

    def __get_broken_preflist(self, person):
        new_prev_list = {}
        current_tie = []
        all_ties = []
        prev_index = None
        prev_person = None
        n_index = 0
        for other_p, index in self.get_preference_list(person).items():
            if index == prev_index:
                if prev_person is not None:
                    current_tie.append(prev_person)
                    prev_person = None
                current_tie.append(other_p)
                new_prev_list[other_p] = n_index
            else:

                new_prev_list[other_p] = n_index
                if len(current_tie) > 0:
                    all_ties.append(current_tie)
                current_tie = []
                prev_person = other_p
            prev_index = index
            n_index += 1
        if len(current_tie) > 0:
            all_ties.append(current_tie)
        return new_prev_list, all_ties

    @staticmethod
    def from_shiftbrk(males, females, males_pref, females_pref, all_ties_m, all_ties_w):
        tmp = Matching(males, females, males_pref, females_pref)
        return ShiftBrkMatching(tmp, all_ties_m=all_ties_m, all_ties_w=all_ties_w)
