import matplotlib.pyplot as plt

from algorithms.solver.SMTI.qubo_smti import QUBO_SMTI
from algorithms.storage import get_computation_result, get_smti


def plot_accuracy_main():
    plot_accuracy_algorithms()
    plot_smp_accuracy()
    plot_qubo_qa_vs_lp()


def _barplot_en_results(qbsolv_results, sizes):
    width = 0.5
    fig, ax = plt.subplots()
    lp_worse = [100 * qbsolv_results[size]["lw"] / 50.0 for size in sizes]
    lp_equal = [100 * qbsolv_results[size]["eq"] / 50.0 for size in sizes]
    lp_better = [100 * qbsolv_results[size]["lb"] / 50.0 for size in sizes]
    ax.bar(sizes, lp_worse, width, label="qa en is better")
    ax.bar(sizes, lp_equal, bottom=lp_worse, width=width, label="correct solution")
    ax.bar(sizes, lp_better, bottom=lp_equal, width=width, label="lp en is better")

    plt.xlabel("problem size")
    plt.ylabel("portion of a instance [%]")
    plt.legend()
    plt.show()


def plot_qubo_qa_vs_lp():
    solvers = ["lp", "qa", "qbsolv"]
    df = get_computation_result("qbsolv_en_results")
    sizes = df["size"].unique()
    qa_results = {size: {"eq": 0, "lb": 0, "lw": 0} for size in sizes}
    qbsolv_results = {size: {"eq": 0, "lb": 0, "lw": 0} for size in sizes}
    for index, row in df.iterrows():
        matching = get_smti(int(row["index_f"]), int(row["size"]))
        solver_q = QUBO_SMTI(matching).pre_process()

        # more negative energy is better
        size = row["size"]
        if row["lp_en"] < row["qa_en"]:
            qa_results[size]["lb"] += 1
        elif row["lp_en"] > row["qa_en"]:
            qa_results[size]["lw"] += 1
        else:
            qa_results[size]["eq"] += 1

    _barplot_en_results(qa_results, sizes)


def plot_smp_accuracy():
    df = get_computation_result("smp_result")
    df["qa_opt_en"] = df["qa_opt_en"] / df["matching_count"]
    df["qa_stable"] = df["qa_stable"] / df["matching_count"]
    df["qbsolv_opt_en"] = df["qbsolv_opt_en"] / df["matching_count"]
    df["qbsolv_stable"] = df["qbsolv_stable"] / df["matching_count"]
    sizes = df["size"].unique()
    df = df.groupby(["size"]).mean()
    df["size"] = sizes

    plt.title("Acurracy for SMP")
    plt.plot(df["size"], 100 * df["qa_stable"], label="qa")
    plt.plot(df["size"], 100 * df["qbsolv_stable"], label="qbsolv")
    plt.xticks(df["size"])
    plt.ylabel('accuracy [%]')
    plt.xlabel('problem size')
    plt.legend()
    plt.show()


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
    plt.plot(sizes, results["qa"], label="QUBO-MAX-SMTI (qa)")
    plt.plot(sizes, results["shiftbrk"], label="SHIFTBRK")
    plt.plot(sizes, results["kiraly"], label="Krialy2")
    # plt.xticks(sizes)
    plt.ylabel('accuracy [%]')
    plt.xlabel('problem size')
    plt.legend()
    plt.show()
