import time
import gc

from algorithms.create_templates import create_smp_instance
from algorithms.solver.SMP.backtrack_smp import BACKTRACK_SMP
from algorithms.solver.SMTI.qubo_smti import QUBO_SMTI


def test_main():
    for size in range(4, 20):
        gc.collect()
        run_size(size)
    gc.collect()


def run_size(size):
    print(size, ": ")
    matching = create_smp_instance(size)
    # matching.compute_all_solutions(mode="SMP", m_processing=(size > 7), verbose=False)
    start = time.time()
    solutions_b = (BACKTRACK_SMP(matching).solve())
    end = time.time()
    elaspsed = end - start

    start = time.time()
    solver = QUBO_SMTI(matching, mode="bqm").pre_process()
    end = time.time()
    solutions = solver.solve_multi()
    solutions = solutions[solutions.energy == solver.get_optimal_energy(matching.size)]
    print("\tQUBO Solutions: ", solutions.shape[0])
    print("\tBACK Solution:  ", len(solutions_b))
    # print("\tAll Solutions: ", len(matching.solutions))
    print()
    print("\tQUBO Elapsed: ", end - start)
    print("\tBACK Elapsed: ", elaspsed)
