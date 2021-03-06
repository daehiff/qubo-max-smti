import logging
from pprint import pprint

import pandas as pd
from algorithms.solver.SMTI.qubo_smti import QUBO_SMTI
from algorithms.storage import get_smp, store_smp, store_qa_solution, get_solution_qa, store_computation_result

from computations.config import *
import algorithms.utils as ut
import multiprocessing
from multiprocessing import Pool

log = logging.getLogger()


def main_smp_measurements(generate_solutions=True):
    """
    Main Method to measure the QUBO Formulation against the SMP results:
    #1
    :param generate_solutions:
    :return:
    """
    ut.init_log()
    log.info("Sarting SMP Evaluation")
    if generate_solutions:
        generate_and_save_all_solutions()
    log.info("Starting SMP Evaluation")

    ###########################################################
    # compare the count of found matches
    # by qbsolv vs the quantum annealer
    ###########################################################
    df_smp = pd.DataFrame()
    for size in sizes_smp:
        if size >= smp_solve_max:
            continue
        for index_f in range(samples_per_size_smp):
            log.info(f"At: {size}, {index_f}")
            tmp = compare_solution_count_qbsolv_smp(size, index_f)
            df_smp = df_smp.append(tmp, ignore_index=True)
    store_computation_result(df_smp, "smp_qbsolv_count_result")
    log.info("DONE")

    ###########################################################
    # check how many stable pairs have found by qbsolv in the range
    # of the QA
    ###########################################################
    df_smp = pd.DataFrame()
    for size in sizes_smp_qa:
        for index_f in range(samples_per_size_smp):
            log.info(f"At: {size}, {index_f}")
            out = compute_smp_results(size, index_f)
            df_smp = df_smp.append(out, ignore_index=True)
    store_computation_result(df_smp, "smp_result")
    log.info("DONE")

    ###########################################################
    # compare the counts of the Qbsolv on a large scale by (previously)
    # finding all stable matchings by backtracking
    ###########################################################
    df_smp = pd.DataFrame()
    for size in sizes_smp:
        for index_f in range(samples_per_size_smp):
            log.info(f"At: {size}, {index_f}")
            out = compute_smp_results_qbsolv(size, index_f)
            df_smp = df_smp.append(out, ignore_index=True)
    store_computation_result(df_smp, "smp_result_qbsolvpure")
    log.info("DONE ALL")


def compare_solution_count_qbsolv_smp(size, index_f):
    matching = get_smp(index_f, size)
    solutions_q = QUBO_SMTI(matching).solve_multi()
    solutions_q = list(filter(lambda x: x.is_stable()[0], solutions_q))
    all_solutions = matching.solutions
    return {"size": size, "index_f": index_f, "stable_solutions_q": len(solutions_q),
            "all_solutions": len(all_solutions)}


def _generate_singe_solutions(size, index_f):
    matching = get_smp(index_f, size)
    matching.compute_all_solutions(mode="SMP")
    store_smp(matching, index_f)
    return (matching, index_f)


def generate_and_save_all_solutions():
    log.info("Computing all possible solutions")
    tasks = [(size, index_f)
             for index_f in range(samples_per_size_smp)
             for size in list(filter(lambda x: x < smp_solve_max, sizes_smp))]
    p = Pool(multiprocessing.cpu_count())
    all_solutions = p.starmap(_generate_singe_solutions, tasks)
    for matching, index_f in all_solutions:
        store_smp(matching, index_f)
    log.info("Done!")


def _count_unique_stable_matchings(solution_df, opt_en):
    unique = pd.DataFrame()
    matchings = []
    for index, row in solution_df.iterrows():
        matching = row["match"]
        if len(list(filter(lambda x: x == matching, matchings))) == 0:
            matchings.append(matching)
            unique = unique.append(row, ignore_index=True)
    stable_matchings = unique.shape[0]
    if "energy" in unique.columns:
        unique = unique[unique["energy"] == opt_en]
        correct_energy = unique.shape[0]
    else:
        correct_energy = 0  # zero times correct en
    return stable_matchings, correct_energy


def compute_smp_results_qbsolv(size, index_f):
    matching = get_smp(index_f, size)
    solver = QUBO_SMTI(matching).pre_process()
    opt_en = solver.get_optimal_energy(matching.size)

    solution = solver.solve()
    stable, size_match = solution.is_stable()

    solution_qbsolv = solver.solve_multi_data()
    stable_solution_qbsolv = solution_qbsolv[solution_qbsolv.stable == 1.0]
    qbsolv_unique_stable, qbsolv_opt_en = _count_unique_stable_matchings(stable_solution_qbsolv, opt_en)

    return {"qbsolv_stable": qbsolv_unique_stable, "qbsolv_opt_en": qbsolv_opt_en,
            "stable": stable, "size_match": size_match,
            "size": size, "index_f": index_f}


def compute_smp_results(size, index_f):
    matching = get_smp(index_f, size)

    solver = QUBO_SMTI(matching).pre_process()

    solution_qa = solver.solve_qa(verbose=False, num_reads=100)
    store_qa_solution(solution_qa, size, index_f, "smp_qa")

    solution_qbsolv = solver.solve_multi_data()
    store_qa_solution(solution_qbsolv, size, index_f, "smp_qbsolv")

    stable_solution_qa = solution_qa[solution_qa.stable == 1.0]
    stable_solution_qbsolv = solution_qbsolv[solution_qbsolv.stable == 1.0]
    opt_en = solver.get_optimal_energy(matching.size)

    qa_unique_stable, qa_opt_en = _count_unique_stable_matchings(stable_solution_qa, opt_en)
    qbsolv_unique_stable, qbsolv_opt_en = _count_unique_stable_matchings(stable_solution_qbsolv, opt_en)
    return {"qa_stable": qa_unique_stable, "qa_opt_en": qa_opt_en,
            "qbsolv_stable": qbsolv_unique_stable, "qbsolv_opt_en": qbsolv_opt_en,
            "matching_count": len(matching.solutions), "size": size, "index_f": index_f}
