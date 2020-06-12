import numpy as np


class MCVITIE:
    def __init__(self, matching):
        self.matching = matching
        self.unchanged = [True for _ in range(matching.size)]
        self.malecounter = [1 for _ in range(matching.size)]
        self.solutions = []
        self.malechoice = np.zeros((matching.size, matching.size), dtype=int)
        self.femalechoice = np.zeros((matching.size, matching.size), dtype=int)
        self.fc = np.zeros((matching.size, matching.size + 1))
        self.success = False

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
        marriage = [0 for _ in range(self.matching.size)]
        for i in range(1, self.matching.size + 1):
            self.proposal(i, marriage)
        self.store_stable_marrigae(marriage)
        for i in range(1, self.matching.size):
            self.breakmarriage(marriage, i)
        return self.solutions

    def breakmarriage(self, marriage: list, i: int):
        print(self.malecounter[i - 1])
        marriage[self.malechoice[i - 1][self.malecounter[i - 1] - 1]] = -i
        self.proposal(i, marriage)
        if not self.success:
            self.unchanged[i - 1] = False
            return
        self.store_stable_marrigae(marriage)
        for j in range(i, self.matching.size - 1):
            self.breakmarriage(marriage, j)
        for j in range(i + 1, self.matching.size - 1):
            self.unchanged[j] = True

    def proposal(self, i: int, marriage: list):
        if i < 0:
            self.success = True
        elif i == 0 or self.malecounter[i - 1] == self.matching.size + 1 or not self.unchanged[i - 1]:
            self.success = False
        else:
            j = self.malecounter[i - 1]
            self.malecounter[i - 1] = j + 1
            self.refusal(i, self.malechoice[i - 1][j - 1] + 1, marriage)

    def refusal(self, i: int, j: int, marriage: list):
        if self.fc[j - 1][abs(marriage[j - 1])] > self.fc[j - 1][i]:  # todo abs here
            k = marriage[j - 1]
            marriage[j - 1] = i
            self.proposal(k, marriage)
        else:
            self.proposal(i, marriage)

    def store_stable_marrigae(self, marriage):
        match = {}
        for index, i in enumerate(marriage):
            i = abs(i)
            m = self.matching.males[i - 1]
            w = self.matching.females[index]
            match[m] = w

        self.solutions.append(match)
