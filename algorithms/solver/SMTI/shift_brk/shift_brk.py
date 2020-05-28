from algorithms.solver.SMTI.shift_brk.shiftbrkmatching import ShiftBrkMatching
import numpy as np

from algorithms.solver.SMP.std_smp import StandardSMP


class ShiftBrk:
    def __init__(self, matching):
        self.matching = matching
        self.max_tie_size = None
        self.max_male_tie_size = None
        self.max_female_tie_size = None
        self.instances = None

    def solve(self):
        self.create_max_ties()
        self.instances = np.empty((self.max_tie_size, self.max_tie_size), dtype=object)
        prev_instance = ShiftBrkMatching(self.matching).break_preflists()
        self.instances[0][0] = prev_instance
        for i in range(1, self.max_tie_size):
            self.instances[i][0] = self.instances[i - 1][0].shift("m")

        for i in range(0, self.max_tie_size):
            for j in range(1, self.max_tie_size):
                self.instances[i][j] = self.instances[i][j - 1].shift("w")
        general_solution = None
        for i in range(0, self.max_tie_size):
            for j in range(0, self.max_tie_size):
                solution = StandardSMP(self.instances[i][j]).solve()
                if general_solution is None or solution.size > general_solution.size:
                    general_solution = solution

        return general_solution

    def create_max_ties(self):
        self.max_male_tie_size, self.max_female_tie_size = self.matching.get_max_tie_len()
        self.max_tie_size = max(self.max_male_tie_size, self.max_female_tie_size)
        assert self.max_tie_size is not None
        assert self.max_male_tie_size is not None
        assert self.max_female_tie_size is not None
