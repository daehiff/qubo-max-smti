from pprint import pprint

from algorithms.create_templates import create_smti_instance, create_and_save_smti, create_and_save_smp
from algorithms.solver.SMTI.lp_smti import LP_smti
from algorithms.solver.SMTI.qubo_smti import QbsolvSMTI
from algorithms.storage import get_smti


def main_test():
    size = 6
    p1 = 1
    p2 = 0.8
    for index_f in range(1000):
        matching = create_and_save_smti(index_f, size, p1, p2)

    solver = QbsolvSMTI(matching)
    print(solver.solve(verbose=True))
