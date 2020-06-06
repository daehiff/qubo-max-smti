import sys
import os
# evaluations
from computations.accuracy_measurements import main_accuracy
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
            # plot_time_evaluation_main()
        elif sys.argv[1] == "-t":
            print(os.getenv('TOKEN', ""))
        else:
            print(f"unspecified argument: {sys.argv[1]}")
    else:
        print("Please specify:")
        print("\t -g: to generate a new dataset")
        print("\t -ca: to run the accuracy computations")
        print("\t -ca: to run the time computations")
        print("\t -csmp: to run the smp computations")
