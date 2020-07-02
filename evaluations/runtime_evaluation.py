from algorithms.storage import get_computation_result, show_store_plot
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
    conv = 1000
    df["qubo_dt"] = df["qubo_dt[s]"] * conv
    df["qubo_dt_var"] = df["qubo_dt_var[%]"] / 100 * df["qubo_dt"]

    df["lp_dt"] = df["lp_dt[s]"] * conv
    df["lp_dt_var"] = df["lp_dt_var[%]"] / 100 * df["lp_dt"]

    df["shiftbrk_dt"] = df["shiftbrk_dt[s]"] * conv
    df["shiftbrk_dt_var"] = df["shiftbrk_dt_var[%]"] / 100 * df["shiftbrk_dt"]

    df["kiraly_dt"] = df["kiraly_dt[s]"] * conv
    df["kiraly_dt_var"] = df["kiraly_dt_var[%]"] / 100 * df["kiraly_dt"]

    # plt.errorbar(sizes, df["qubo_dt"], df["qubo_dt_var"], fmt='-,', capsize=0.1, label="QUBO")
    # plt.errorbar(sizes, df["lp_dt"], df["lp_dt_var"], fmt='-,', barsabove=True, label="LP")
    # plt.errorbar(sizes, df["shiftbrk_dt"], df["shiftbrk_dt_var"], fmt='-,', barsabove=True, label="SHIFTBRK")
    # plt.errorbar(sizes, df["kiraly_dt"], df["kiraly_dt_var"], fmt='-,', barsabove=True, label="kiraly")

    plt.plot(sizes, df["qubo_dt"], label="QUBO")
    plt.plot(sizes, df["lp_dt"], label="MAX-SMTI-LP")
    plt.plot(sizes, df["shiftbrk_dt"], label="SHIFTBRK")
    plt.plot(sizes, df["kiraly_dt"], label="Krialy2")

    plt.ylabel('time [ms]')
    plt.xlabel('problem size')
    plt.legend()
    show_store_plot("runtime")
