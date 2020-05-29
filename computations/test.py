import random
import time
import timeit
from pprint import pprint

from algorithms.create_templates import create_smti_instance, create_and_save_smti, create_and_save_smp
from algorithms.maching import Matching
from algorithms.solver.SMTI.lp_smti import LP_smti
from algorithms.solver.SMTI.qubo_smti import QbsolvSMTI
from algorithms.storage import get_smti
from scipy.special import comb
import numpy as np
import matplotlib.pyplot as plt


def main_test():
    # size 6: ~5min
    # size 7: ~20min
    # size 8:
    start = time.time()
    create_and_save_smp(0, 15, compute_solutions=True)
    end = time.time()
    print("Elapsed: ", end - start)
    return
    sizes = [i for i in range(3, 31)]
    print(round(random.uniform(0.1, 0.5), 2))
    average_sizes = {size: [] for size in sizes}
    num_samples = 0
    for size in sizes:
        for _ in range(100):
            num_samples += 1
            p1_ = round(random.uniform(0.01, 1), 2)
            p2_ = round(random.uniform(0.01, 1), 2)
            matching = create_smti_instance(size, p1_, p2_)
            average_sizes[size].append(calculate_average_size(matching))
        print(f"size: {size}, {num_samples}")
    index = 3
    fig, ax = plt.subplots()
    for size in sizes:
        ax.scatter(average_sizes[size], [index for _ in average_sizes[size]])
        index += 1
    plt.xlim((0, 32))
    plt.xlabel("average preflist size")
    plt.ylabel("Matching size")
    plt.show()
    print(num_samples)


def calculate_average_size(matching: Matching):
    size = []
    for male in matching.males:
        size.append(len(matching.get_preference_list(male)))

    for female in matching.females:
        size.append(len(matching.get_preference_list(female)))

    return np.average(np.array(size))
