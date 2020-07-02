import logging
import random

import matplotlib.pyplot as plt

from algorithms.create_templates import create_and_save_smti, create_and_save_smp
from algorithms.storage import get_smti
from computations.config import *
import algorithms.utils as ut

log = logging.getLogger()


def main_generation():
    ut.init_log()
    log.info("Generating datasets for SMP and SMTI")
    # generate_smti_set(sizes_smti, samples_per_size_smti)
    # generate_smp_set(sizes_smp, samples_per_size_smp)
    log.info("DONE! Plotting the distributions of sizes and preferencelists")
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
            g1 = round(random.uniform(0.01, 1), 2)
            g2 = round(random.uniform(0.01, 1), 2)
            create_and_save_smti(index_f, size, g1, g2)


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
    A plot that shows the distribution of sizes/ties per size category for smti dataset
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
    plt.xlim((0, sizes_smti[-1]))
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
    plt.xlim((0, sizes_smti[-1]))
    plt.xlabel("average tie size per instance")
    plt.ylabel("Matching size")
    plt.show()
