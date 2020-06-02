import sys

# evaluations
from computations.dataset_generation import main_generation
from computations.smp_measurements import main_smp_measurements
from computations.time_measurements import main_time_measure

if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(sys.argv)
        if sys.argv[1] == "-g":
            main_generation()
        elif sys.argv[1] == "-t":
            main_time_measure()
        elif sys.argv[1] == "-s":
            main_smp_measurements()
        else:
            print("unspecified argument")
    else:
        print("Please specify:")
        print("\t -g: to generate a new dataset")
        print("\t -t: for time measurement")
