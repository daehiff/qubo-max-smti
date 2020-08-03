from algorithms.solver.SMP.backtrack_smp import BACKTRACK_SMP
from algorithms.solver.SMP.mcvitie import MCVITIE
from algorithms.storage import get_smp


def test_main():
    size = 6
    index_f = 0
    for size in range(5, 15):
        for index_f in range(20):
            matching = get_smp(index_f, size)
            print(size, index_f)
            solutions_b = BACKTRACK_SMP(matching).solve()

            solutions_mv = MCVITIE(matching).solve()
            for solution in solutions_mv:
                (stable, size_) = solution.is_stable()
                assert stable and size == size_
            assert len(solutions_b) == len(solutions_mv)

    matching = get_smp(index_f, size)
    print(size, index_f)
    solutions_b = BACKTRACK_SMP(matching).solve()

    solutions_mv = MCVITIE(matching).solve()

    # print(list(map(lambda x: x.solution_m, solutions_b)))
    # for solution in solutions_b:
    #    print(solution.solution_m, "male loss", solution.get_male_loss(), "female loss", solution.get_female_loss())
    print(list(map(lambda x: (x.solution_m, x.is_stable(), x.get_male_loss()), solutions_mv)))
    print(list(map(lambda x: (x.solution_m, x.is_stable(), x.get_male_loss()), solutions_b)))
