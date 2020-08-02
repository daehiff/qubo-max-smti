from algorithms.solver.SMP.backtrack_smp import BACKTRACK_SMP
from algorithms.solver.SMP.mcvitie import MCVITIE
from algorithms.storage import get_smp


def test_main():
    size = 5
    index_f = 1
    matching = get_smp(index_f, size)

    # solutions_b = BACKTRACK_SMP(matching).solve()

    solutions_mv = MCVITIE(matching).solve()
    # print(list(map(lambda x: x.solution_m, solutions_b)))
    # for solution in solutions_b:
    #    print(solution.solution_m, "male loss", solution.get_male_loss(), "female loss", solution.get_female_loss())
    print(list(map(lambda x: (x.solution_m, x.is_stable(), x.get_male_loss()), solutions_mv)))
