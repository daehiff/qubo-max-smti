import time

from algorithms.solver.SMP.backtrack_smp import BACKTRACK_SMP
from algorithms.storage import get_smp


def test_main():
    matching = get_smp(0, 18)
    start = time.time()
    BACKTRACK_SMP(matching).solve()
    end = time.time()
    print(end - start)
