from algorithms.solver.SMP.std_smp import StandardSMP


class RGS(StandardSMP):
    def __init__(self, matching, mode):
        assert mode == "m" or mode == "w"
        super().__init__(matching, mode="m_opt" if mode == "m" else "w_opt")
        self.matching = matching
        self.extraScore = {}
        for male in self.matching.males:
            self.extraScore[male] = 0.0
        for female in self.matching.females:
            self.extraScore[female] = 0.0

        self.reactivated_persons = self.matching.males  # if matching is w_opt, males are females

    def is_better_partner(self, p_1, p_2, p_3):
        """
        Check if p_2 would be a better partner for p_1 in comparison to p_3
        :param p_1:
        :param p_2:
        :param p_3:
        :return:
        """
        return self.matching.prefers(p_1, p_2, p_3) and self.matching.is_acceptable(p_1, p_2)

    def get_active(self):
        return self.reactivated_persons

    def get_reactivated(self, solution):
        self.reactivated_persons = []
        for man in self.matching.males:
            if man not in solution.get_solution().keys() and self.extraScore[man] == 0:
                self.reactivated_persons.append(man)

        return self.reactivated_persons

    def reactive_persons(self, persons):
        """
        Reactivate the persons under a matching condition either men or woman
        :param persons:
        :return:
        """
        for person in persons:
            if self.extraScore[person] > 0:
                raise Exception("Person has already reativated")
            self.extraScore[person] = 0.5 if self.mode == "m_opt" else 0.25
