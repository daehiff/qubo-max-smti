from copy import deepcopy

from algorithms.maching import Matching
from algorithms.solver.SMTI.kiraly.RGS import RGS


class Kirialy1:
    def __init__(self, matching):
        self.matching = matching
        self.rm_gs = RGS(matching, "m")

    def solve(self):
        solution = self.rm_gs.solve()
        reactivated_men = self.rm_gs.get_reactivated(solution)
        while not len(self.rm_gs.reactivated_persons) == 0:
            self.rm_gs.reactive_persons(reactivated_men)
            solution = self.rm_gs.solve()
            reactivated_men = self.rm_gs.get_reactivated(solution)

        return solution

    def get_extra_score(self):
        return self.rm_gs.extraScore


class Kirialy2:
    def __init__(self, matching):
        self.matching = matching
        self.rm_gs = RGS(matching, "m")
        self.rw_gs = None

    def solve(self):
        kiri1 = Kirialy1(self.break_men_ties())
        kiri1.solve()
        self.rw_gs = RGS(self.get_woman_strict(kiri1.get_extra_score()), "w")
        solution = self.rw_gs.solve()
        reactivated_woman = self.rw_gs.get_reactivated(solution)
        while not len(reactivated_woman) == 0:
            self.rw_gs.reactive_persons(reactivated_woman)
            solution = self.rw_gs.solve()
            reactivated_woman = self.rw_gs.get_reactivated(solution)
        return solution

    def break_men_ties(self):
        new_mens_pref = {}
        for man in self.matching.males:
            mans_pref = dict(sorted(self.matching.males_pref[man].items(), key=lambda x: x[1]))
            new_m_pref = {}  # of single man
            new_index = 0
            for w, index in mans_pref.items():
                new_m_pref[w] = new_index
                new_index += 1

            new_mens_pref[man] = new_m_pref
        return Matching(deepcopy(self.matching.males), deepcopy(self.matching.females), new_mens_pref,
                        deepcopy(self.matching.females_pref))

    def get_woman_strict(self, ex_score):
        clone = self.matching.clone()
        for person, score in ex_score.items():
            if person in self.matching.males and score == 0.5:
                for w in clone.females:
                    clone.females_pref[w] = self.promote(clone.females_pref[w], person)

        return self.break_woman_ties(clone)

    def break_woman_ties(self, matching):
        for w in matching.females:
            new_index = 0
            new_pref = {}
            for m, index in matching.females_pref[w].items():
                new_pref[m] = new_index
                new_index += 1
            matching.females_pref[w] = new_pref

        return matching

    def promote(self, pref_list, person):
        tie = self.get_tie(pref_list, person)
        pref_list_sorted = dict(sorted(pref_list.items(), key=lambda x: x[1]))
        state = 0
        new_pref = {}
        for m, index in pref_list_sorted.items():
            if m in tie and state == 0:
                new_pref[person] = index
                new_pref[m] = index + 1
                state = 1
            elif state == 1:
                new_pref[m] = index + 1
            else:
                new_pref[m] = index
        return new_pref

    def get_tie(self, pref_list, person):
        if person not in pref_list.keys():
            return []
        person_index = pref_list[person]
        tie = []
        for p, index in pref_list.items():
            if index == person_index and not person == p:
                tie.append(p)
        return tie
