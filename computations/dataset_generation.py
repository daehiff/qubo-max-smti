import random

import matplotlib.pyplot as plt

from algorithms.create_templates import create_and_save_smti, create_and_save_smp
from algorithms.storage import get_smti


def main_generation(generate=False):
    sizes_smti = [i for i in range(3, 31)]
    samples_per_size_smti = 20
    sizes_smp = [i for i in range(3, 21)]
    samples_per_size_smp = 10
    if generate:
        generate_smti_set(sizes_smti, samples_per_size_smti)
        generate_smp_set(sizes_smp, samples_per_size_smp)
    plot_equidistribution_smti(sizes_smti, samples_per_size_smti)


def generate_smti_set(sizes, samples_per_size):
    """
    Code that generates our test dataset for SMTI:
        - sizes: [3, 30]
        - per size p1 and p2 are random drawn
        - instances per size: 20

    :return:
    """
    for size in sizes:
        for index_f in range(samples_per_size):
            p1 = round(random.uniform(0.01, 1), 2)
            p2 = round(random.uniform(0.01, 1), 2)
            create_and_save_smti(index_f, size, p1, p2)


def generate_smp_set(sizes, samples_per_size):
    """
    Code that generates our SMP test set:
        - sizes: [3;20]                 (SMP-QUBO gets inaccurate for n >~ 15)
        - instances per size: 10
    :return:
    """
    for size in sizes:
        for index_f in range(samples_per_size):
            create_and_save_smp(index_f, size)


def plot_equidistribution_smti(sizes, samples_per_size):
    """
    A plot that shows the equidistribution of sizes/ties per size category for smti dataset
    """

    ###########################################
    # Plot SIZES
    ###########################################
    average_sizes = {size: [] for size in sizes}
    for size in sizes:
        for index_f in range(samples_per_size):
            matching = get_smti(index_f, size)
            average_sizes[size].append(matching.average_pref_list_len())
    index = 3
    fig, ax = plt.subplots()
    for size in sizes:
        ax.scatter(average_sizes[size], [index for _ in average_sizes[size]])
        index += 1
    plt.xlim((0, 32))
    plt.xlabel("average preflist size")
    plt.ylabel("Matching size")
    plt.show()

    ###########################################
    # Plot TIES
    ###########################################
    average_ties = {size: [] for size in sizes}
    for size in sizes:
        for index_f in range(samples_per_size):
            matching = get_smti(index_f, size)
            average_ties[size].append(matching.average_tie_len())
    index = 3
    fig, ax = plt.subplots()
    for size in sizes:
        ax.scatter(average_ties[size], [index for _ in average_sizes[size]])
        index += 1
    plt.xlim((0, 32))
    plt.xlabel("average tie size per instance")
    plt.ylabel("Matching size")
    plt.show()
