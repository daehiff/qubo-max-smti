import dimod
import numpy as np
from dimod import BinaryQuadraticModel
from dwave_qbsolv import QBSolv

from algorithms.solution import Solution


class QbsolvSMP:

    def __init__(self, matching, mode="bqm"):
        self.matching = matching
        self.mode = mode
        self.p = None
        self.p1 = None
        self.p2 = None
        self.qubo = None
        self.encoding = {}
        self.__create_encoding()

    def create_qubo(self):
        self.p, self.p1, self.p2 = self.get_default_penalties()
        assert self.p is not None and self.p1 is not None and self.p2 is not None

        length = self.matching.size ** 2
        if self.mode == "np":
            self.qubo = np.zeros((length, length), dtype=np.object)
        elif self.mode == "bqm":
            self.qubo = BinaryQuadraticModel({}, {}, 0.0, dimod.BINARY)
        else:
            raise Exception(f"unknown mode: {self.mode}")
        for j in range(length):
            for i in range(j + 1):
                if i == j:
                    self.__assign_qubo(j, i, - 2 * (self.matching.size - 1) * self.p1)
                else:
                    self.__assign_qubo(j, i, 1)
                    # match of current line  == current "selected" matched pair
                    w_j = self.encoding[j][1]
                    m_j = self.encoding[j][0]
                    # match of current column == current match under review
                    w_i = self.encoding[i][1]
                    m_i = self.encoding[i][0]
                    if m_j == m_i or w_j == w_i:
                        self.__assign_qubo(j, i, self.p)
                        continue

                    prefs_m_j = self.matching.prefers(m_j, w_i, w_j) and self.matching.prefers(w_i, m_j, m_i)
                    prefs_w_j = self.matching.prefers(w_j, m_i, m_j) and self.matching.prefers(m_i, w_j, w_i)

                    if prefs_m_j and prefs_w_j:
                        self.__assign_qubo(j, i, 2 * self.p2)
                    elif prefs_m_j:
                        self.__assign_qubo(j, i, self.p2)
                    elif prefs_w_j:
                        self.__assign_qubo(j, i, self.p2)

    def solve(self, verbose=False, num_repeats=100, target=None):
        if self.qubo is None:
            self.create_qubo()

        if self.mode == "np":  # more memory intensive
            response = QBSolv().sample(BinaryQuadraticModel.from_numpy_matrix(self.qubo), target=target)
        elif self.mode == "bqm":
            response = QBSolv().sample(self.qubo, num_repeats=num_repeats, target=target)
        else:
            raise Exception(f"mode: {self.mode} cannot be solved yet")
        if verbose:
            print(response)
        energies = list(response.data_vectors['energy'])
        min_en = min(energies)
        ret_match = self.encode(list(response.samples())[energies.index(min_en)])

        return Solution(self.matching, ret_match)

    def solve_multi(self, verbose=True, num_repeats=100, target=None):
        if self.qubo is None:
            self.create_qubo()
        if self.mode == "np":  # more memory intensive
            response = QBSolv().sample(BinaryQuadraticModel.from_numpy_matrix(self.qubo), target=target)
        elif self.mode == "bqm":
            response = QBSolv().sample(self.qubo, num_repeats=num_repeats, target=target)
        else:
            raise Exception(f"mode: {self.mode} cannot be solved yet")
        if verbose:
            print(response)
        n = self.matching.size
        stable_energy = -3 / 2 * self.p1 * (n - 1) * n
        energies = list(response.data_vectors['energy'])
        samples = enumerate(list(response.samples()))
        allowed_samples = [sample for idx, sample in samples if energies[idx] == stable_energy]
        return [Solution(self.matching, self.encode(sample)) for sample in allowed_samples]

    def __create_encoding(self):
        qubo_size = 0
        for male in self.matching.males:
            for female in self.matching.females:
                self.encoding[qubo_size] = (male, female)
                qubo_size += 1

    def encode(self, sample):
        match = {}
        for index, element in enumerate(sample.keys()):
            if index >= len(self.encoding):
                return match
            if sample[element] == 1:
                match[self.encoding[index][0]] = self.encoding[index][1]
        return match

    def get_default_penalties(self):
        p1 = 1
        p2 = p1 + 1
        p = 2 * (p1 * self.matching.size + p2) + 1
        return p, p1, p2

    def __assign_qubo(self, i, j, val):
        if self.mode == "np":
            self.qubo[j][i] += val
        elif self.mode == "bqm":
            if i == j:
                self.qubo.add_variable(j, val)
            else:
                self.qubo.add_interaction(j, i, val)
        else:
            raise Exception(f"Unknown mode: {self.mode}")
