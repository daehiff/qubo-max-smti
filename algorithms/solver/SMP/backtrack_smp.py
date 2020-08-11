import time


class BACKTRACK_SMP:
    def __init__(self, matching):
        self.matching = matching

    def solve(self, time_limit=None):
        start = time.time()
        solutions = []
        q = [-2 for _ in range(self.matching.size)]
        c = 0
        from_backtrack = False

        while True:
            while c < self.matching.size:
                if not from_backtrack:
                    q[c] = -1
                from_backtrack = False

                while q[c] < self.matching.size:
                    if time_limit is not None and time.time() - start >= time_limit:
                        from algorithms.solution import Solution
                        return list(map(lambda x: Solution(self.matching, x), solutions))
                    q[c] = q[c] + 1
                    if q[c] == self.matching.size:
                        c = self.backtrack(c)
                        if c is None:
                            from algorithms.solution import Solution
                            return list(map(lambda x: Solution(self.matching, x), solutions))
                        from_backtrack = True
                        break
                    if self.is_ok(c, q[c], q):
                        from_backtrack = False
                        c += 1
                        break
            solutions.append(self.convert_matching(q))
            c = self.backtrack(c)
            from_backtrack = True
            if c is None:
                return solutions

    def convert_matching(self, q):
        match = {}
        for m_idx, w_idx in enumerate(q):
            m = self.matching.males[m_idx]
            w = self.matching.females[w_idx]
            match[m] = w
        return match

    def backtrack(self, current_idx):
        if current_idx == 0:
            return None
        else:
            return current_idx - 1

    def is_ok(self, m_idx, w_idx, q):
        m = self.matching.males[m_idx]

        w = self.matching.females[w_idx]

        for m1_idx in range(0, m_idx):
            m1 = self.matching.males[m1_idx]
            if q[m_idx] == q[m1_idx]:
                return False
            w1 = self.matching.females[q[m1_idx]]
            if self.matching.prefers(m, w1, w) and self.matching.prefers(w1, m, m1):
                return False
            if self.matching.prefers(m1, w, w1) and self.matching.prefers(w, m1, m):
                return False
        return True

    def get_next(self, m, w):
        idx = self.matching.get_index(w, m, fallback=-1)
        m_pref = self.matching.get_preference_list(m)
        for w, idx_ in m_pref.items():
            if idx_ == idx + 1:
                return w

    def is_next(self, m, w):
        prf_list = self.matching.get_preference_lists_len(m)
        return prf_list[w] < self.matching.size
