import dimod
from dimod import BinaryQuadraticModel
from dwave_qbsolv import QBSolv, SOLUTION_DIVERSITY, ENERGY_IMPACT
import numpy as np

from algorithms.solution import Solution


class QbsolvSMTI:

    def __init__(self, matching, mode="bqm"):
        self.p = None
        self.p1 = None
        self.p2 = None

        self.qubo = None

        self.encoding = None
        self.rev_encoding = None

        self.qubo_size = 0
        self.matching = matching
        self.pre_evaluated_solution = None

        self.mode = mode

    def create_encoding(self):
        encoding = {}
        rev_encoding = {}
        qubo_size = 0
        for male in self.matching.males:
            for female in self.matching.females:
                if self.matching.is_acceptable(male, female):
                    encoding[qubo_size] = (male, female)
                    rev_encoding[(male, female)] = qubo_size
                    qubo_size += 1
        if self.qubo_size == 0 or self.qubo_size == 1:
            self.pre_evaluated_solution = {}
            for m, w in encoding.values():
                self.pre_evaluated_solution[m] = w
        self.encoding = encoding
        self.rev_encoding = rev_encoding
        self.qubo_size = qubo_size

    def encode(self, sample):
        match = {}
        for index, element in enumerate(sample.keys()):
            if index >= len(self.encoding):
                return match
            if sample[element] == 1:
                match[self.encoding[index][0]] = self.encoding[index][1]
        return match

    def __create_qubo_matrix(self, length):
        if self.mode == "np":
            self.qubo = np.zeros((length, length))
        elif self.mode == "bqm":
            self.qubo = BinaryQuadraticModel({}, {}, 0.0, dimod.BINARY)
        else:
            raise Exception(f"unknown mode: {self.mode}")

    def __assign_qubo(self, j, i, val):
        """
        helper function to assign values to the qubo
        :param j:
        :param i:
        :param val:
        :return:
        """
        if self.mode == "np":
            self.qubo[j][i] += val
        elif self.mode == "bqm":
            if i == j:
                self.qubo.add_variable(j, val)
            else:
                self.qubo.add_interaction(j, i, val)
        else:
            raise Exception(f"Unknown mode: {self.mode}")

    def create_qubo(self):
        self.create_encoding()
        assert self.encoding is not None

        self.p, self.p1, self.p2 = self.get_default_penalties()
        assert self.p is not None and self.p2 is not None

        length = self.qubo_size
        is_acceptable = self.matching.is_acceptable
        prefers = self.matching.prefers
        self.__create_qubo_matrix(length)
        for i in range(self.qubo_size):
            m = self.encoding[i][0]
            w = self.encoding[i][1]
            self.__assign_qubo(i, i, -self.p1)
            for j in range(i):
                m_j = self.encoding[j][0]
                w_j = self.encoding[j][1]
                if m == m_j or w == w_j:
                    self.__assign_qubo(j, i, self.p)

            for w_i in self.matching.females:
                if not prefers(m, w, w_i) and is_acceptable(m, w_i):
                    m_w_i = self.rev_encoding[(m, w_i)]
                    self.__assign_qubo(m_w_i, m_w_i, -self.p2)

            for m_i in self.matching.males:
                if not prefers(w, m, m_i) and is_acceptable(m_i, w):
                    m_i_w = self.rev_encoding[(m_i, w)]
                    self.__assign_qubo(m_i_w, m_i_w, -self.p2)

            for m_i in self.matching.males:
                for w_i in self.matching.females:
                    if is_acceptable(m_i, w) and is_acceptable(w_i, m):
                        m_w_i = self.rev_encoding[(m, w_i)]  # note that in the equation i and j were used
                        w_m_i = self.rev_encoding[(m_i, w)]

                        if not (prefers(m, w, w_i) or prefers(w, m, m_i)):
                            if m_w_i <= w_m_i:
                                self.__assign_qubo(m_w_i, w_m_i, self.p2)
                            else:
                                self.__assign_qubo(w_m_i, m_w_i, self.p2)

        return self

    def solve(self, verbose=False, num_repeats=200, target=None, debug=False):
        if self.qubo is None:
            self.create_qubo()
        if self.qubo_size == 0 or self.qubo_size == 1:
            if debug:
                return None
            return Solution(self.matching, self.pre_evaluated_solution)
        if self.mode == "np":  # more memory intensive
            response = QBSolv().sample(BinaryQuadraticModel.from_numpy_matrix(self.qubo), num_repeats=num_repeats,
                                       target=target)
        elif self.mode == "bqm":
            response = QBSolv().sample(self.qubo, num_repeats=num_repeats, target=target)
        else:
            raise Exception(f"mode: {self.mode} cannot be solved yet")
        if debug:
            return response
        if verbose:
            print(response)
            for index, sample in enumerate(list(response.samples())):
                print(index, ":", Solution(self.matching, self.encode(sample)).is_stable(), self.encode(sample))
        energies = list(response.data_vectors['energy'])
        min_en = min(energies)
        ret_match = self.encode(list(response.samples())[energies.index(min_en)])
        return Solution(self.matching, ret_match)

    def get_default_penalties(self):
        p1 = 1
        p2 = self.matching.size
        p = self.matching.size * p2 + p1
        return p, p1, p2
