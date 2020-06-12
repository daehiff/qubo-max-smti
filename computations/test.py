import time
import gc

from algorithms.create_templates import create_smp_instance
from algorithms.solution import Solution
from algorithms.solver.SMP.backtrack_smp import BACKTRACK_SMP
from algorithms.solver.SMP.mcvitie import MCVITIE
from algorithms.solver.SMTI.qubo_smti import QUBO_SMTI


def test_main():
    run_size(4)


def run_size(size):
    matching = create_smp_instance(size)
    solutions_b = (BACKTRACK_SMP(matching).solve())
    solutions_mv = MCVITIE(matching).solve()
    print(list(map(lambda x: Solution(matching, x).is_stable(), solutions_mv)))
    print(len(solutions_b), len(solutions_mv))
