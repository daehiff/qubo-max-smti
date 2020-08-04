import time
import sys
from algorithms.create_templates import create_smp_instance
from algorithms.solver.SMP.backtrack_smp import BACKTRACK_SMP
from algorithms.solver.SMP.mcvitie import MCVITIE
from algorithms.solver.SMP.std_smp import StandardSMP
from algorithms.solver.SMTI.qubo_smti import QUBO_SMTI
from algorithms.storage import get_smp
import numpy as np


def test_main():
    index_f = 1
    sys.setrecursionlimit(200000)
    size = 15
    matching = get_smp(index_f, size)
    start = time.time()
    solutions_mv = MCVITIE(matching).solve()
    print(time.time() - start)
    print(len(solutions_mv))
    solutions_b = BACKTRACK_SMP(matching).solve()
    print(len(solutions_b))
    return
    for size in range(5, 20):
        matching = get_smp(index_f, size)
        # solutions_b = BACKTRACK_SMP(matching).solve()
        start = time.time()
        solutions_mv = MCVITIE(matching).solve()
        time_mv = time.time() - start
        print("Time MV:", time_mv, "SIZE: ", size)
        # print(list(map(lambda x: (x.solution_m, x.is_stable(), x.get_male_loss()), solutions_b)))
        print(list(map(lambda x: (x.solution_m, x.is_stable(), x.get_male_loss()), solutions_mv)))

    # print(list(map(lambda x: x.solution_m, solutions_b)))
    # for solution in solutions_b:
    #    print(solution.solution_m, "male loss", solution.get_male_loss(), "female loss", solution.get_female_loss())
