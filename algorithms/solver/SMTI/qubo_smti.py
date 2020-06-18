import os

import dimod
from dimod import BinaryQuadraticModel
from dwave_qbsolv import QBSolv, SOLUTION_DIVERSITY, ENERGY_IMPACT
import numpy as np

from algorithms.solution import Solution

import networkx as nx
from dwave.system import DWaveSampler, LeapHybridSampler
from dwave.system import FixedEmbeddingComposite
from dimod import qubo_to_ising
from minorminer import minorminer
import pandas as pd

SOLVER = 'DW_2000Q_6'
ENDPOINT = 'https://cloud.dwavesys.com/sapi'


class QUBO_SMTI:

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

        self.token = os.getenv('TOKEN', "")

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

    def encode_qa(self, sample):
        valid = True
        match = {}
        for index, element in enumerate(sample):
            if element == 1:
                if self.encoding[index][0] in match.keys():
                    valid = False
                match[self.encoding[index][0]] = self.encoding[index][1]
        return match, valid

    def encode(self, sample):
        match = {}
        valid = True
        for index, element in enumerate(sample.keys()):
            if index >= len(self.encoding):
                return match
            if sample[element] == 1:
                if self.encoding[index][0] in match.keys():
                    valid = False
                match[self.encoding[index][0]] = self.encoding[index][1]
        return match, valid

    def __create_qubo_matrix(self, length):
        if self.mode == "np":
            self.qubo = np.zeros((length, length))
        elif self.mode == "bqm":
            self.qubo = BinaryQuadraticModel({}, {}, 0.0, dimod.BINARY)
        elif self.mode == "qa":
            self.qubo = {}
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
        elif self.mode == "qa":
            if (i, j) not in self.qubo.keys():
                self.qubo[(j, i)] = val
            else:
                self.qubo[(j, i)] = self.qubo[(j, i)] + val
        else:
            raise Exception(f"Unknown mode: {self.mode}")

    def pre_process(self):
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

    def get_chain_stength(self):
        assert self.mode == "bqm"
        qubo_np = self.qubo.to_numpy_matrix()
        return np.amax(qubo_np)

    def solve_qa(self, verbose=True, num_reads=100):
        assert self.token is not None
        assert self.mode == "bqm"
        if self.qubo is None:
            self.pre_process()
        if verbose:
            print(f"Solving SMTI with: {SOLVER}")
            print(f"Optimal Solution: {-(len(self.encoding) * self.p2 + self.matching.size * self.p1)}")

        chain_strength = self.get_chain_stength() + 1  # max element in qubo matrix + epsilon
        solver_limit = len(self.encoding)  # solver_limit => size of qubo matrix

        G = nx.complete_graph(solver_limit)
        dw_solver = DWaveSampler(solver=SOLVER, token=self.token, endpoint=ENDPOINT)
        embedding = minorminer.find_embedding(G.edges, dw_solver.edgelist)
        fixed_embedding = FixedEmbeddingComposite(dw_solver, embedding)
        result = fixed_embedding.sample(self.qubo, num_reads=num_reads, chain_strength=chain_strength)

        dw_solver.client.close()  # clean up all the thread mess the client creates so it does not block my code
        if verbose:
            print(result)
            for index, (sample, energy, occ, chain) in enumerate(result.record):
                match_, _ = self.encode_qa(sample.tolist())
                stable_, size_ = Solution(self.matching, match_).is_stable()
                print(f"{index}: ", match_, size_, stable_)

        samples = pd.DataFrame()
        for sample, energy, occ, chain in result.record:
            match, valid = self.encode_qa(sample.tolist())
            stable, size = Solution(self.matching, match).is_stable()
            samples = samples.append({"match": match, "sample": sample.tolist(),
                                      "energy": energy, "occ": occ, "chain": chain,
                                      "valid": valid, "stable": stable, "size": size}, ignore_index=True)
        return samples

    def compute_energy(self, vector):
        assert len(vector) == len(self.qubo)
        assert self.mode == "np"
        vector = np.array(vector)
        return vector.dot(self.qubo).dot(vector.T)

    def solve(self, verbose=False, num_repeats=50, target=None, debug=False):
        if self.qubo is None:
            self.pre_process()
        if verbose:
            print("Solving MAX-SMTI with Qbsolv")
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
                match, valid = self.encode(sample)
                print(index, ":", Solution(self.matching, match).is_stable(), match, valid)
        energies = list(response.data_vectors['energy'])
        min_en = min(energies)
        ret_match, valid = self.encode(list(response.samples())[energies.index(min_en)])
        return Solution(self.matching, ret_match, energy=min_en)

    def get_optimal_energy(self, size):
        return -(len(self.encoding) * self.p2 + size * self.p1)

    def solve_multi(self, verbose=False, target=None, num_repeats=200):
        if self.qubo is None:
            self.pre_process()
        if verbose:
            print("Solving multiple solutions of MAX-SMTI with Qbsolv")
        if self.qubo_size == 0 or self.qubo_size == 1:
            return [Solution(self.matching, self.pre_evaluated_solution)]

        if self.mode == "np":  # more memory intensive
            response = QBSolv().sample(BinaryQuadraticModel.from_numpy_matrix(self.qubo), num_repeats=num_repeats,
                                       target=target, algorithm=SOLUTION_DIVERSITY)
        elif self.mode == "bqm":
            response = QBSolv().sample(self.qubo, num_repeats=num_repeats, target=target, algorithm=SOLUTION_DIVERSITY)
        else:
            raise Exception(f"mode: {self.mode} cannot be solved yet")

        if verbose:
            print(response)
            for index, sample in enumerate(list(response.samples())):
                match, valid = self.encode(sample)
                print(index, ":", Solution(self.matching, match).is_stable(), match, valid)

        samples = pd.DataFrame()
        for sample, energy, occ in response.record:
            match, valid = self.encode_qa(sample.tolist())
            stable, size = Solution(self.matching, match).is_stable()
            samples = samples.append({"match": match, "sample": sample.tolist(),
                                      "energy": energy, "occ": occ,
                                      "valid": valid, "stable": stable, "size": size}, ignore_index=True)
        return samples

    def get_default_penalties(self):
        p1 = 1
        p2 = self.matching.size
        p = self.matching.size * p2 + p1
        return p, p1, p2
