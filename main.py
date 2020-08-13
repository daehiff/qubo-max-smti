import sys
import os
# evaluations
import time

from algorithms.solver.SMP.backtrack_smp import BACKTRACK_SMP
from algorithms.solver.SMP.std_smp import StandardSMP
from algorithms.solver.SMTI.qubo_smti import QUBO_SMTI
from algorithms.storage import get_solution_qa, get_smp
from computations.accuracy_measurements import main_accuracy, compute_qubo_en
from computations.dataset_generation import main_generation
from computations.smp_acc_runtime import smp_acc_runtime_main, compare_runtime
from computations.smp_measurements import main_smp_measurements
from computations.time_measurements import main_time_measure, measure_qubo_vs_backtracking
from evaluations.accuracy_evaluation import plot_accuracy_main
from evaluations.runtime_evaluation import plot_time_evaluation_main

if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(sys.argv)
        if sys.argv[1] == "-g":
            main_generation()
        elif sys.argv[1] == "-ca":
            main_accuracy()
        elif sys.argv[1] == "-ct":
            main_time_measure()
        elif sys.argv[1] == "-csmp":
            # main_smp_measurements()
            # out = compare_runtime(7, 0)
            smp_acc_runtime_main()
        elif sys.argv[1] == "-p":
            plot_accuracy_main()
            plot_time_evaluation_main()
        elif sys.argv[1] == "-t":
            print("Insert Test Main")
            import numpy as np

            matching = get_smp(1, 17)

            start = time.time()
            solver = BACKTRACK_SMP(matching)
            solutions = solver.solve(time_limit=None)
            print(time.time() - start)
            print(len(solutions))
            # print(matching.solutions)
            # solver = QUBO_SMTI(matching).pre_process()
            # solver.solve_qa(num_reads=1400, verbose=True)
            # print(solution_qa["stable"])
        else:
            print(f"unspecified argument: {sys.argv[1]}")
    else:
        print("Please specify:")
        print("\t -g: to generate a new dataset")
        print("\t -ca: to run the accuracy computations")
        print("\t -ca: to run the time computations")
        print("\t -csmp: to run the smp computations")
