import sys
# evaluations
from evaluations.evaluate_accuracity import main as main_plot_acc
from evaluations.evaluate_runtime import main as main_plot_rt
# computations
from computations.accuracity_measurements import main as main_comp_accuracy
from computations.duration_measurement import main as main_comp_duration
from computations.example_presentation import main as main_presentation

if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(sys.argv)
        if sys.argv[1] == "-p":
            print("Plotting to ./figures")
            main_plot_acc()
            main_plot_rt()
        elif sys.argv[1] == "-c":
            main_comp_accuracy()
            main_comp_duration()
        elif sys.argv[1] == "-pr":
            main_presentation()
        else:
            print("unspecified argument")
    else:
        print("Please specify:")
        print("\t -p: to plot the computational results")
        print("\t -c: to run the computational evaluation")

