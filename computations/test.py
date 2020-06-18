from algorithms.solver.SMP.backtrack_smp import BACKTRACK_SMP
from algorithms.storage import get_smp


def test_main():
    matching = get_smp(20, 0)
    BACKTRACK_SMP(matching).solve()
