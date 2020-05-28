from pprint import pprint

from algorithms.create_templates import create_smti_instance, create_and_save_smti
from algorithms.solver.SMTI.lp_smti import LP_smti
from algorithms.solver.SMTI.qubo_smti import QbsolvSMTI
from algorithms.storage import get_smti


def main_test():
    size = 5
    p1 = 0.5
    p2 = 0.5
    num = 10
    for index_f in range(num):
        matching = create_and_save_smti(num, index_f, size, p1, p2)

    for index_f in range(num):
        matching = get_smti(size, num, p1, p2, index_f)
        solver = QbsolvSMTI(matching, mode="np")
        solver.create_qubo()
        solution = solver.solve(verbose=False)
        solution_ref = LP_smti(matching).solve()
        print("---")
        print(solution.is_stable())
        print(solution_ref.is_stable())
