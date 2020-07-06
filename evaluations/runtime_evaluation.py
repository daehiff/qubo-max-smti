from algorithms.storage import get_computation_result, show_store_plot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_time_evaluation_main():
    compare_runtime_algorithms(plot_preprocessing=False)
    compare_qbsolv_preprocessing()
    compare_runtime_algorithms(plot_preprocessing=True)


def compare_runtime_algorithms(plot_preprocessing=False):
    solver_types = ["qubo", "lp", "shiftbrk", "kiraly"]
    df = get_computation_result("time_result")
    df_1 = get_computation_result("qubo_lp_time_result")
    df_1 = df_1.groupby(["size"]).mean()
    for solver_type in solver_types:
        del df[f"{solver_type}_stable"]
        del df[f"{solver_type}_size"]
    del df["index_f"]
    sizes = df["size"].unique()
    df = df.groupby(["size"]).mean()
    # convert to ms
    conv = 1000

    df_1["qubo_dt"] = df_1["qubo_pp[s]"] * conv

    df["qubo_dt"] = df["qubo_dt[s]"] * conv
    df["qubo_dt_var"] = df["qubo_dt_var[%]"] / 100 * df["qubo_dt"]

    df["lp_dt"] = df["lp_dt[s]"] * conv
    df["lp_dt_var"] = df["lp_dt_var[%]"] / 100 * df["lp_dt"]

    df["shiftbrk_dt"] = df["shiftbrk_dt[s]"] * conv
    df["shiftbrk_dt_var"] = df["shiftbrk_dt_var[%]"] / 100 * df["shiftbrk_dt"]

    df["kiraly_dt"] = df["kiraly_dt[s]"] * conv
    df["kiraly_dt_var"] = df["kiraly_dt_var[%]"] / 100 * df["kiraly_dt"]

    if plot_preprocessing:
        pass
        plt.plot(sizes, df_1["qubo_dt"], label="QUBO (only preprocessing")
    else:
        plt.plot(sizes, df["qubo_dt"], label="QUBO")
    plt.plot(sizes, df["lp_dt"], label="MAX-SMTI-LP")
    plt.plot(sizes, df["shiftbrk_dt"], label="SHIFTBRK")
    plt.plot(sizes, df["kiraly_dt"], label="Krialy2")

    plt.ylabel('time [ms]')
    plt.xlabel('problem size')
    plt.legend()
    if plot_preprocessing:
        show_store_plot("runtime_qubo_preprocessing")
    else:
        show_store_plot("runtime")


def compare_qbsolv_preprocessing():
    df = get_computation_result("qubo_lp_time_result")
    df["qubo_total_time"] = df["qubo_pp[s]"] + df["qubo_solving[s]"]
    sizes = df["size"].unique()
    df = df.groupby(["size"]).mean()
    plt.plot(sizes, df["qubo_total_time"])
    plt.plot(sizes, df["qubo_pp[s]"])
    plt.fill_between(sizes, df["qubo_pp[s]"], df["qubo_total_time"], alpha=0.30, label="time to solve QUBO")
    plt.fill_between(sizes, 0, df["qubo_pp[s]"], alpha=0.30, label="time for preprocessing")
    plt.margins(x=0.01, y=0.01)
    plt.legend()
    show_store_plot("qubo_pp_runtime")
