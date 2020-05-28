import sys

# evaluations
from computations.test import main_test

if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(sys.argv)
        if sys.argv[1] == "-p":
            main_test()
        else:
            print("unspecified argument")
    else:
        print("Please specify:")
        print("\t -p: to plot the computational results")
        print("\t -c: to run the computational evaluation")
