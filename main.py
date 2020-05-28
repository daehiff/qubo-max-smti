import sys

# evaluations
from computations.test import main_test

if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(sys.argv)
        if sys.argv[1] == "-g":
            main_test()
        else:
            print("unspecified argument")
    else:
        print("Please specify:")
        print("\t -g: to generate a new dataset")
