import random
import time

import matplotlib.pyplot as plt
import numpy as np

from algorithms.create_templates import create_smti_instance, create_and_save_smti, create_and_save_smp


def main_generation():
    index_f = 0
    size = 11
    matching = create_and_save_smp(index_f, size, compute_solutions=False)

    start = time.time()
    matching.compute_all_solutions(mode="SMP", m_processing=True)
    end = time.time()
    print("Elapsed: ", end - start)

    start = time.time()
    matching.compute_all_solutions(mode="SMP", m_processing=False)
    end = time.time()
    print("Elapsed: ", end - start)
    # plot_equidistribution()


def plot_equidistribution():
    sizes = [i for i in range(3, 31)]
    average_sizes = {size: [] for size in sizes}
    num_samples = 0
    samples_per_size = 20
    for size in sizes:
        for _ in range(samples_per_size):
            num_samples += 1
            p1 = round(random.uniform(0.01, 1), 2)
            p2 = round(random.uniform(0.01, 1), 2)
            matching = create_smti_instance(size, p1, p2)
            average_sizes[size].append(matching.average_pref_list_len())
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


def generate_dataset_smti():
    sizes = [i for i in range(3, 31)]
    num_samples = 0
    samples_per_size = 20
    for size in sizes:
        for index_f in range(samples_per_size):
            num_samples += 1
            p1 = round(random.uniform(0.01, 1), 2)
            p2 = round(random.uniform(0.01, 1), 2)
            create_and_save_smti(index_f, size, p1, p2)
        print(f"size: {size} has num_samples:{num_samples}")


def generate_dataset_smp():
    sizes = [i for i in range(3, 31)]
    num_samples = 0
    samples_per_size = 20
    for size in sizes:
        for index_f in range(samples_per_size):
            create_and_save_smp(index_f, size, compute_solutions=(size < 8))
