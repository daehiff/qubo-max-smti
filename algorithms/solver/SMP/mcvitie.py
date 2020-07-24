from copy import deepcopy

import numpy as np


class MCVITIE:
    def __init__(self, matching):
        self.matching = matching

        self.unchanged = [True for _ in range(matching.size)]

        self.solutions = []

        self.malechoice = np.zeros((matching.size, matching.size), dtype=int)
        self.femalechoice = np.zeros((matching.size, matching.size), dtype=int)
        self.fc = np.zeros((matching.size, matching.size + 1))

        for idx, m in enumerate(matching.males):
            self.malechoice[idx] = [self.matching.females.index(w) for w, idx in
                                    matching.get_preference_list(m).items()]

        for idx, w in enumerate(matching.females):
            self.femalechoice[idx] = [self.matching.males.index(m) for m, idx in
                                      matching.get_preference_list(w).items()]

        for i in range(0, matching.size):
            for j in range(1, matching.size):
                self.fc[i][self.femalechoice[i][j] + 1] = j
            self.fc[i][0] = self.matching.size + 1

    def solve(self):
        malec = [1 for _ in range(self.matching.size)]
        marriage = [0 for _ in range(self.matching.size)]
        for i in range(1, self.matching.size + 1):
            self.proposal(i, malec, marriage)
        self.store_stable_marrigae(marriage)
        for i in range(1, self.matching.size):
            self.breakmarriage(malec, marriage, i)
        return self.solutions

    def breakmarriage(self, malec: list, marriage: list, i: int):
        marriage[self.malechoice[i - 1][malec[i - 1] - 2]] = 0
        sucess = self.proposal(i, malec, marriage)
        if not sucess:  # GOTO EXIT
            self.unchanged[i - 1] = False
            return
        self.store_stable_marrigae(marriage)
        malec_ = deepcopy(malec)
        for j in range(i, self.matching.size):
            self.breakmarriage(malec_, marriage, j)

        for j in range(i + 1, self.matching.size):
            self.unchanged[j - 1] = True

    def proposal(self, i: int, malec: list, marriage: list):
        if i < 0:
            return True
        elif i == 0 or malec[i - 1] == self.matching.size + 1 or (not self.unchanged[i - 1]):
            return False

        else:
            j = malec[i - 1]
            malec[i - 1] = j + 1
            return self.refusal(i, self.malechoice[i - 1][j - 1] + 1, malec, marriage)

    def refusal(self, i: int, j: int, malec: list, marriage: list):
        if self.fc[j - 1][abs(marriage[j - 1])] > self.fc[j - 1][i]:
            k = marriage[j - 1]
            marriage[j - 1] = i
            return self.proposal(k, malec, marriage)
        else:
            return self.proposal(i, malec, marriage)

    def store_stable_marrigae(self, marriage):
        match = {}
        for index, i in enumerate(marriage):
            m = self.matching.males[i - 1]
            w = self.matching.females[index]
            match[m] = w

        self.solutions.append(match)
