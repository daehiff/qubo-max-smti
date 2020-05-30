import sys

# evaluations
from computations.dataset_generation import main_generation
from computations.test import main_test

if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(sys.argv)
        if sys.argv[1] == "-g":
            main_generation()
        elif sys.argv[1] == "-t":
            main_test()
        else:
            print("unspecified argument")
    else:
        print("Please specify:")
        print("\t -g: to generate a new dataset")
        print("\t -t: if you want to run your testfile")
