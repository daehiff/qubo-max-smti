from algorithms.storage import get_computation_result
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_time_evaluation_main():
    compare_runtime_algorithms()


def compare_runtime_algorithms():
    solver_types = ["qubo", "lp", "shiftbrk", "kiraly"]
    df = get_computation_result("time_result")
    for solver_type in solver_types:
        del df[f"{solver_type}_stable"]
        del df[f"{solver_type}_size"]
    del df["index_f"]
    sizes = df["size"].unique()
    df = df.groupby(["size"]).mean()
    # convert to ms
    mean_qbsolv = list(map(lambda x: 1000 * x, df["qubo_dt[s]"]))
    mean_lp = list(map(lambda x: 1000 * x, df["lp_dt[s]"]))
    mean_shiftbrk = list(map(lambda x: 1000 * x, df["shiftbrk_dt[s]"]))
    mean_kirialy = list(map(lambda x: 1000 * x, df["kiraly_dt[s]"]))

    plt.plot(sizes, mean_qbsolv, label="QUBO-MAX-SMTI")
    plt.plot(sizes, mean_lp, label="MAX-SMTI-LP")
    plt.plot(sizes, mean_shiftbrk, label="SHIFTBRK")
    plt.plot(sizes, mean_kirialy, label="Krialy2")
    plt.xticks(sizes)
    plt.ylabel('time [ms]')
    plt.xlabel('problem size')
    plt.legend()
    plt.show()
