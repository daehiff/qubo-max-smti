from copy import deepcopy

from algorithms.maching import Matching


class Solution(Matching):

    def __init__(self, matching, matches, energy=0):
        super().__init__(matching.males, matching.females, matching.males_pref, matching.females_pref)
        self.solution_m = matches
        self.solution_w = {w: m for m, w in matches.items()}
        self.size = len(matches.keys())
        self.energy = energy

    def get_solution(self):
        return self.solution_m

    def is_free(self, person):
        if self.solution_m is None:
            raise Exception("Only can check for Free Persons, if you set a solution")
        if person in self.males:
            return person not in self.solution_m.keys()
        else:
            return person not in self.solution_w.keys()

    def get_partner(self, person):
        if person in self.males:
            if person in self.solution_m.keys():
                return self.solution_m[person]
        else:
            if person in self.solution_w.keys():
                return self.solution_w[person]
        return None

    def is_blocking(self, male, female, mode):
        if self.solution_m is None:
            raise Exception("Only can check for blocking pairs, if you set a solution")
        if mode == "smti":
            acceptable = self.is_acceptable(male, female)
            male_pref = self.is_free(male) or self.prefers(male, female, self.get_partner(male))
            female_pref = self.is_free(female) or self.prefers(female, male, self.get_partner(female))
            return acceptable and male_pref and female_pref
        elif mode == "smp":
            male_pref = self.prefers(male, female, self.get_partner(male))
            female_pref = self.prefers(female, male, self.get_partner(female))
            return male_pref and female_pref
        else:
            raise Exception(f"unknown mode: {mode}")

    def get_blocking_pairs(self, mode):
        blocking_pairs = []
        for male in self.males:
            for female in self.females:
                if self.is_blocking(male, female, mode):
                    blocking_pairs.append((male, female))
        return blocking_pairs

    def is_stable(self, mode="smti"):
        if mode == "smti":
            if not len(self.solution_w) == len(self.solution_m):
                return False, -1
            for male, female in self.solution_m.items():
                if not self.is_acceptable(male, female):
                    return False, len(self.solution_m)
            for male in self.males:
                for female in self.females:
                    if self.is_blocking(male, female, mode):
                        return False, len(self.solution_w)
            return True, len(self.solution_w)
        elif mode == "smp":
            for male in self.males:
                for female in self.get_prefered(male, self.get_partner(male)):
                    if self.prefers(female, male, self.get_partner(female)):
                        return False, len(self.solution_w)
            return True, len(self.solution_w)
        else:
            raise Exception(f"Unknown mode: {mode}")

    def get_male_loss(self):
        loss = 0
        for m in self.males:
            w = self.solution_m[m]
            loss += self.get_index(w, m)
        return loss

    def get_female_loss(self):
        loss = 0
        for w in self.females:
            m = self.solution_w[w]
            loss += self.get_index(m, w)
        return loss
