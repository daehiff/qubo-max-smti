from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np

from algorithms.solver.SMTI.qubo_smti import QUBO_SMTI
from algorithms.storage import get_computation_result, get_smti, show_store_plot


def plot_accuracy_main():
    plot_accuracy_algorithms()
    plot_smp_accuracy()
    plot_qubo_qa_vs_lp()


def _barplot_en_results(qbsolv_results, sizes, solver_t="qa"):
    width = 0.5
    fig, ax = plt.subplots()

    opt = [100 * qbsolv_results[size]["opt"] / 50.0 for size in sizes]
    stable = [100 * qbsolv_results[size]["stable"] / 50.0 for size in sizes]
    invalid = [100 * qbsolv_results[size]["invalid"] / 50.0 for size in sizes]
    # assert all([x == 0.0 for x in lp_worse])
    ax.bar(sizes, opt, bottom=0, width=width, label=f"en_qubo = en_opt (optimal)")
    ax.bar(sizes, stable, bottom=opt, width=width, label="en_opt < en_qubo < en_valid (valid)")
    ax.bar(sizes, invalid, bottom=np.array(stable) + np.array(opt), width=width, label="en_qubo > en_valid (invalid)")

    plt.xlabel("problem size")
    # plt.ylabel("portion of a instance [%]")
    plt.legend()
    # plt.title(f"Energy Comparison")
    show_store_plot(f"{solver_t}")


def plot_qubo_qa_vs_lp():
    solvers = ["lp", "qa", "qbsolv"]
    df = get_computation_result("qbsolv_en_results")
    sizes = df["size"].unique()
    qbsolv_results = {size: {"opt": 0, "stable": 0, "invalid": 0} for size in sizes}
    qa_results = {size: {"opt": 0, "stable": 0, "invalid": 0} for size in sizes}
    for index, row in df.iterrows():
        # more negative energy is better
        size = row["size"]

        assert row["opt_en"] == row["lp_en"]
        if row["opt_en"] == row["qbsolv_en"]:
            qbsolv_results[size]["opt"] += 1
        elif row["opt_en"] < row["qbsolv_en"] < row["min_valid_en"]:
            qbsolv_results[size]["stable"] += 1
        else:
            qbsolv_results[size]["invalid"] += 1

        if size < 8:
            if row["opt_en"] == row["qa_en"]:
                qa_results[size]["opt"] += 1
            elif row["opt_en"] < row["qa_en"] < row["min_valid_en"]:
                qa_results[size]["stable"] += 1
            else:
                qa_results[size]["invalid"] += 1

    _barplot_en_results(qbsolv_results, sizes, solver_t="qbsolv")
    _barplot_en_results(qa_results, sizes[:5], solver_t="qa")


def plot_smp_accuracy():
    df = get_computation_result("smp_bt_time_qa_qbsolv")
    sizes = df["size"].unique()
    df["bt_stable"] = df["bt_stable"] / df["matching_count"]
    df["qa_stable"] = df["qa_stable"] / df["matching_count"]
    df["qbsolv_stable"] = df["qbsolv_stable"] / df["matching_count"]
    dfvar = df.groupby(["size"]).var()
    df = df.groupby(["size"]).mean()

    plt.title("Accuracy for SMP")
    width = 0.75
    plt.bar(sizes - width / 3, 100 * df["qa_stable"], label="qa", width=width / 3, align="center")
    plt.bar(sizes, 100 * df["qbsolv_stable"], label="qbsolv", width=width / 3, align="center")
    plt.bar(sizes + width / 3, 100 * df["bt_stable"], label="backtracking", width=width / 3, align="center")
    plt.xticks(sizes)
    plt.ylabel('portion of available solutions [%]')
    plt.xlabel('problem size')
    plt.legend()
    show_store_plot("smp_accuracy")


def plot_accuracy_algorithms():
    solver_types = ["qbsolv", "shiftbrk", "kiraly", "qa"]
    df = get_computation_result("accuracy_results")
    df["qa_size"] = list(map(lambda x: 0 if x == -1 else x, df["qa_size"]))
    df["qbsolv_size"] = list(map(lambda x: 0 if x == -1 else x, df["qbsolv_size"]))
    del df["index_f"]
    sizes = df["size"].unique()
    results = {solver: {size: 0 for size in sizes} for solver in solver_types}
    for index, row in df.iterrows():
        for solver_type in solver_types:
            if row[f"{solver_type}_stable"] == 1.0 and row[f"{solver_type}_size"] == row["lp_size"]:
                size = int(row["size"])
                results[solver_type][size] = results[solver_type][size] + 1
    results = {k: list(v.values()) for k, v in results.items()}
    results = {k: list(map(lambda x: x / 50.0, v)) for k, v in results.items()}
    plt.title("Accuracy of approximation algorithms vs QA vs qbsolv")
    plt.plot(sizes, results["qbsolv"], label="QUBO-MAX-SMTI (qbsolv)")
    plt.plot(sizes[:5], results["qa"][:5], label="QUBO-MAX-SMTI (qa)")
    plt.plot(sizes, results["shiftbrk"], label="SHIFTBRK")
    plt.plot(sizes, results["kiraly"], label="Krialy2")
    # plt.xticks(sizes)
    plt.ylabel('accuracy [%]')
    plt.xlabel('problem size')
    plt.legend()
    show_store_plot("accuracy_qbsolv_vs_apx")
