import time
import gc

from algorithms.create_templates import create_smp_instance, create_and_save_smp
from algorithms.solution import Solution
from algorithms.solver.SMP.backtrack_smp import BACKTRACK_SMP
from algorithms.solver.SMP.mcvitie import MCVITIE
from algorithms.solver.SMP.std_smp import StandardSMP
from algorithms.solver.SMTI.qubo_smti import QUBO_SMTI
from algorithms.storage import get_smp


def test_main():
    # for _ in range(100):
    run_size(4)


def check_soltution(to_check, ground_truth):
    for solution in to_check:
        correct_solution = False
        for solution_b in ground_truth:
            tmp = True
            for m, w in solution.items():
                if not solution_b[m] == w:
                    tmp = False
                    break
            if tmp:
                correct_solution = True
        assert correct_solution


def run_size(size):
    # uid = 101
    matching = create_smp_instance(size)

    start = time.time()
    solutions_b = BACKTRACK_SMP(matching).solve()
    end = time.time()

    b_elapsed = end - start

    start = time.time()
    solutions_q = QUBO_SMTI(matching).solve_multi()
    solutions_q = solutions_q[solutions_q.stable == True]
    end = time.time()
    q_elapsed = end - start

    print("All stable: ")
    print(all(list(map(lambda x: x.is_stable()[0], solutions_b))))
    print(all(list(map(lambda x: bool(x), solutions_q["stable"]))))
    print("Time: ")
    print(b_elapsed)
    print(q_elapsed)
    print("Solution Count")
    print(len(solutions_b))
    print(len(solutions_q))
    print()
