import sys
import os
# evaluations
from algorithms.solver.SMTI.qubo_smti import QUBO_SMTI
from algorithms.storage import get_solution_qa, get_smp
from computations.accuracy_measurements import main_accuracy, compute_qubo_en
from computations.dataset_generation import main_generation
from computations.smp_measurements import main_smp_measurements
from computations.time_measurements import main_time_measure
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
            main_smp_measurements()
        elif sys.argv[1] == "-p":
            plot_accuracy_main()
            plot_time_evaluation_main()
        elif sys.argv[1] == "-t":
            print("Insert Test Main")
            for index_f in range(20):
                solution_qa = get_solution_qa(5, index_f, "smp_qa")
                # print(solution_qa["stable"])
                assert all([0.0 == solution for solution in solution_qa["stable"]])
            # matching = get_smp(1, 5)
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
