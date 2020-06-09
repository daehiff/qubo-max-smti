import matplotlib.pyplot as plt

from algorithms.storage import get_computation_result


def plot_accuracy_main():
    #plot_accuracy_algorithms()
    #plot_smp_accuracy()
    plot_qubo_qa_vs_lp()


def plot_qubo_qa_vs_lp():
    df = get_computation_result("qbsolv_en_results")
    print(df)


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
    def filter_unique_columns(data):
        out = {solver_t: 0 for solver_t in solver_types}
        print(data)
        return (out)

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
    print(results)
    plt.plot(results["qbsolv"], label="QUBO-MAX-SMTI (qbsolv)")
    # plt.plot(results["qa"], label="QUBO-MAX-SMTI (qa)")
    plt.plot(results["shiftbrk"], label="SHIFTBRK")
    plt.plot(results["kiraly"], label="Krialy2")
    # plt.xticks(sizes)
    plt.ylabel('accuracy [%]')
    plt.xlabel('problem size')
    plt.legend()
    plt.show()
