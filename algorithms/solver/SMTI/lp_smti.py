from __future__ import print_function
from ortools.linear_solver import pywraplp
import numpy as np

from algorithms.solution import Solution


class LP_smti:
    def __init__(self, matching):
        self.matching = matching
        self.solver: pywraplp.Solver = None
        self.variables = None

    def pre_process(self):
        n = self.matching.size
        self.solver = pywraplp.Solver('Anything', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
        self.variables = np.empty((n, n), dtype=np.object)
        females = males = range(n)
        # mi_wj in {0,1}
        for index_m in males:
            for index_w in females:
                self.variables[index_m][index_w] = self.solver.IntVar(0, 1, f"m{index_m}_w{index_w}")
        # all males sum(x_m,j;n) <= 1
        for index_m in males:
            tmp_male_sum = 0
            for j in females:
                tmp_male_sum += self.variables[index_m][j]
            self.solver.Add(tmp_male_sum <= 1)
        # all females sum(x_i,w;n) <= 1
        for index_w in females:
            tmp_female_sum = 0
            for i in males:
                tmp_female_sum += self.variables[i][index_w]
            self.solver.Add(tmp_female_sum <= 1)

        for index_m, male in enumerate(self.matching.males):
            for index_w, female in enumerate(self.matching.females):
                if self.matching.is_acceptable(male, female):
                    females_sum = 0
                    for k, w in enumerate(self.matching.females):
                        if self.matching.is_acceptable(male, w) and \
                                self.matching.prefers(male, w, female, mode="NOT_STRICT"):
                            females_sum += self.variables[index_m][k]
                    males_sum = 0
                    for h, m in enumerate(self.matching.males):
                        if self.matching.is_acceptable(m, female) and \
                                self.matching.prefers(female, m, male, mode="NOT_STRICT"):
                            males_sum += self.variables[h][index_w]
                    self.solver.Add(males_sum + females_sum >= 1)
                else:
                    self.solver.Add(self.variables[index_m][index_w] == 0)
        objective_function = 0
        for index_w, male in enumerate(self.matching.females):
            for index_m, female in enumerate(self.matching.males):
                objective_function += self.variables[index_m][index_w]
        self.solver.Maximize(objective_function)

    def get_solutions_match(self) -> Solution:
        match = {}
        for index_m, male in enumerate(self.matching.males):
            for index_w, female in enumerate(self.matching.females):
                if self.variables[index_m][index_w].solution_value() == 1:
                    assert male not in match
                    match[male] = female
        return Solution(self.matching, match)

    def solve(self, verbose=False):
        if self.solver is None:
            self.pre_process()
        self.solver.Solve()
        solution = self.get_solutions_match()
        if verbose:
            print("Solution: ")
            print(solution.solution_m)
        return solution

    def solve_mult(self, verbose=True):
        if self.solver is None:
            self.pre_process()
        solutions = []
        solution_count = 1
        self.solver.Solve()
        while True:
            if verbose:
                print(f"Got {solution_count} Solution(s)")
            solutions.append(self.get_solutions_match())
            if not self.solver.NextSolution():
                return solutions
