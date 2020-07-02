import matplotlib.pyplot as plt

from algorithms.solver.SMTI.qubo_smti import QUBO_SMTI
from algorithms.storage import get_computation_result, get_smti, show_store_plot


def plot_accuracy_main():
    plot_accuracy_algorithms()
    plot_smp_accuracy()
    plot_qubo_qa_vs_lp()


def _barplot_en_results(qbsolv_results, sizes, solver_t="qa"):
    width = 0.5
    fig, ax = plt.subplots()

    lp_worse = [100 * qbsolv_results[size]["lw"] / 50.0 for size in sizes]
    lp_equal = [100 * qbsolv_results[size]["eq"] / 50.0 for size in sizes]
    lp_better = [100 * qbsolv_results[size]["lb"] / 50.0 for size in sizes]
    assert all([x == 0.0 for x in lp_worse])
    # ax.bar(sizes, lp_worse, width, label=f"{solver_t} en is better")
    ax.bar(sizes, lp_equal, width=width, label="correct solutions found by the quantum annealer")
    ax.bar(sizes, lp_better, bottom=lp_equal, width=width, label="lp-energy was better")

    plt.xlabel("problem size")
    plt.ylabel("portion of a instance [%]")
    plt.legend()
    # plt.title(f"Energy Comparison")
    show_store_plot(f"{solver_t}")


def plot_qubo_qa_vs_lp():
    solvers = ["lp", "qa", "qbsolv"]
    df = get_computation_result("qbsolv_en_results")
    sizes = df["size"].unique()
    qa_results = {size: {"eq": 0, "lb": 0, "lw": 0} for size in sizes}
    qbsolv_results = {size: {"eq": 0, "lb": 0, "lw": 0} for size in sizes}
    for index, row in df.iterrows():
        # more negative energy is better
        size = row["size"]
        if row["lp_en"] < row["qa_en"]:
            qa_results[size]["lb"] += 1
        elif row["lp_en"] > row["qa_en"]:
            qa_results[size]["lw"] += 1
        else:
            qa_results[size]["eq"] += 1

        if row["lp_en"] < row["qbsolv_en"]:
            qbsolv_results[size]["lb"] += 1
        elif row["lp_en"] > row["qbsolv_en"]:
            qbsolv_results[size]["lw"] += 1
        else:
            qbsolv_results[size]["eq"] += 1

    _barplot_en_results(qbsolv_results, sizes, solver_t="qbsolv")
    _barplot_en_results(qa_results, sizes[:5], solver_t="qa")


def plot_smp_accuracy():
    df_1 = get_computation_result("smp_qbsolv_count_result")
    df_1["stable_solutions_q"] = df_1["stable_solutions_q"] / df_1["all_solutions"]
    sizes_1 = df_1["size"].unique()
    df_1var = df_1.groupby(["size"]).var()
    df_1 = df_1.groupby(["size"]).mean()

    df = get_computation_result("smp_result")
    sizes = df["size"].unique()
    df["qa_opt_en"] = df["qa_opt_en"] / df["matching_count"]
    df["qa_stable"] = df["qa_stable"] / df["matching_count"]
    df["qbsolv_opt_en"] = df["qbsolv_opt_en"] / df["matching_count"]
    df["qbsolv_stable"] = df["qbsolv_stable"] / df["matching_count"]
    dfvar = df.groupby(["size"]).var()
    df = df.groupby(["size"]).mean()

    plt.title("Accuracy for SMP")
    width = 0.3
    plt.bar(sizes - width / 2, 100 * df["qa_stable"], label="qa", width=width, align="center")
    plt.bar(sizes_1 + width / 2, 100 * df_1["stable_solutions_q"], label="qbsolv", width=width, align="center")
    plt.xticks(sizes_1)
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
