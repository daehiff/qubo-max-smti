import matplotlib.pyplot as plt

from algorithms.storage import get_computation_result


def plot_accuracy_main():
    plot_accuracy_algorithms()
    plot_smp_accuracy()
    plot_qubo_qa_vs_lp()


def plot_qubo_qa_vs_lp():
    pass


def plot_smp_accuracy():
    df = get_computation_result("smp_result")
    df["qa_opt_en"] = df["qa_opt_en"] / df["matching_count"]
    df["qa_stable"] = df["qa_stable"] / df["matching_count"]
    df["qbsolv_opt_en"] = df["qbsolv_opt_en"] / df["matching_count"]
    df["qbsolv_stable"] = df["qbsolv_stable"] / df["matching_count"]
    sizes = df["size"].unique()
    df = df.groupby(["size"]).mean()
    df["size"] = sizes

    plt.plot(df["size"], 100 * df["qa_stable"], label="qa")
    plt.plot(df["size"], 100 * df["qbsolv_stable"], label="qbsolv")
    plt.xticks(df["size"])
    plt.ylabel('accuracy [%]')
    plt.xlabel('problem size')
    plt.legend()
    plt.show()


def plot_accuracy_algorithms():
    solver_types = ["qbsolv", "qa", "shiftbrk", "kiraly"]
    df = get_computation_result("accuracy_results")
    df["qa_size"] = list(map(lambda x: 0 if x == -1 else x, df["qa_size"]))
    df["qbsolv_size"] = list(map(lambda x: 0 if x == -1 else x, df["qbsolv_size"]))
    del df["index_f"]
    for solver_type in solver_types:
        del df[f"{solver_type}_stable"]
        df[f"{solver_type}_size"] = df[f"{solver_type}_size"] / df["lp_size"]
    df[f"lp_size"] = df[f"lp_size"] / df["lp_size"]
    del df["lp_stable"]
    sizes = df["size"].unique()
    df = df.groupby(["size"]).mean()
    df["size"] = sizes

    plt.plot(df["size"], 100 * df["qbsolv_size"], label="QUBO-MAX-SMTI (qbsolv)")
    plt.plot(df["size"], 100 * df["qa_size"], label="QUBO-MAX-SMTI (qa)")
    plt.plot(df["size"], 100 * df["shiftbrk_size"], label="SHIFTBRK")
    plt.plot(df["size"], 100 * df["kiraly_size"], label="Krialy2")
    plt.xticks(df["size"])
    plt.ylabel('accuracy [%]')
    plt.xlabel('problem size')
    plt.legend()
    plt.show()
