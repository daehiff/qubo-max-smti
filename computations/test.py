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
    for _ in range(100):
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
    # matching = create_and_save_smp(uid, size)
    # matching = get_smp(uid, size)
    matching = create_smp_instance(size)

    solutions_b = (BACKTRACK_SMP(matching).solve())
    solutions_b = list(map(lambda x: x.solution_m, solutions_b))

    solutions_mv = MCVITIE(matching).solve()
    solutions_mv = list(filter(lambda x: len(x) == size, solutions_mv))
    print(solutions_b)
    print(solutions_mv)
    print("B, male: ", list(map(lambda x: Solution(matching, x).get_male_loss(), solutions_b)))
    print("B, female: ", list(map(lambda x: Solution(matching, x).get_female_loss(), solutions_b)))
    print("MV, male: ", list(map(lambda x: Solution(matching, x).get_male_loss(), solutions_mv)))
    print("MV, female: ", list(map(lambda x: Solution(matching, x).get_female_loss(), solutions_mv)))
    print()
    assert all(list(map(lambda x: Solution(matching, x).is_stable()[0], solutions_mv)))
    assert all(list(map(lambda x: Solution(matching, x).is_stable()[0], solutions_b)))

    # print(StandardSMP(matching).solve().solution_m)
    # print(solutions_mv[0])
    assert (len(solutions_mv) == len(solutions_b))
    # check_soltution(solutions_b, solutions_mv)
    # check_soltution(solutions_mv, solutions_b)
