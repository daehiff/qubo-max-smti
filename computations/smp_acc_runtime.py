import logging
import time

from algorithms.solver.SMP.backtrack_smp import BACKTRACK_SMP
from algorithms.solver.SMTI.qubo_smti import QUBO_SMTI
from algorithms.storage import get_smp, get_solution_qa, store_computation_result
from computations.config import *
import algorithms.utils as ut
import pandas as pd
from computations.smp_measurements import _count_unique_stable_matchings

log = logging.getLogger()


def smp_acc_runtime_main():
    ut.init_log()
    df_smp = pd.DataFrame()
    for size in range(3, 19):
        for index_f in range(samples_per_size_smp):
            log.info(f"At: {size}, {index_f}")
            out = compare_runtime(size, index_f)
            df_smp = df_smp.append(out, ignore_index=True)
            store_computation_result(df_smp, "smp_bt_time_qa_qbsolv")
    store_computation_result(df_smp, "smp_bt_time_qa_qbsolv")


def compare_runtime(size, index_f):
    # TODO 1) SEGEV auch auf 'großem rechner'?
    # TODO 2) plot erstellen?
    # TODO 3) rödeln lassen

    matching = get_smp(index_f, size)

    start = time.time()
    solver = QUBO_SMTI(matching).pre_process()
    solution_qbsolv = solver.solve_multi_data()
    time_qbsolv = time.time() - start

    opt_en = solver.get_optimal_energy(matching.size)

    stable_solution_qbsolv = solution_qbsolv[solution_qbsolv.stable == 1.0]
    qbsolv_unique_stable, _ = _count_unique_stable_matchings(stable_solution_qbsolv, opt_en)

    if size <= 7:
        solution_qa = get_solution_qa(size, index_f, "smp_qa")
        stable_solution_qa = solution_qa[solution_qa.stable == 1.0]
        qa_unique_stable, _ = _count_unique_stable_matchings(stable_solution_qa, opt_en)
    else:
        qa_unique_stable = 0

    solutions_bt = BACKTRACK_SMP(matching).solve(time_limit=time_qbsolv)

    return {"size": size, "index_f": index_f, "qa_stable": qa_unique_stable,
            "qbsolv_stable": qbsolv_unique_stable, "bt_stable": len(solutions_bt),
            "matching_count": len(matching.solutions)}
