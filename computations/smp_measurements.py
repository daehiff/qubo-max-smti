from pprint import pprint

import pandas as pd
from algorithms.solution import Solution
from algorithms.solver.SMTI.qubo_smti import QUBO_SMTI
from algorithms.storage import get_smp, store_smp, store_qa_solution, get_solution_qa
import numpy as np


def generate_and_save_all_solutions():
    for size in range(3, 10):
        for index_f in range(10):
            matching = get_smp(index_f, size)
            matching.compute_all_solutions(mode="SMP", m_processing=(size > 7))
            store_smp(matching, index_f)


def _count_unique_stable_matchings(solution_df, opt_en):
    unique = pd.DataFrame()
    matchings = []
    for index, row in solution_df.iterrows():
        matching = row["match"]
        if len(list(filter(lambda x: x == matching, matchings))) == 0:
            matchings.append(matching)
            unique = unique.append(row, ignore_index=True)
    stable_matchings = unique.shape[0]
    print(unique)
    unique = unique[unique.energy == opt_en]
    correct_energy = unique.shape[0]
    return stable_matchings, correct_energy


def compute_smp_results(size, index_f):
    matching = get_smp(index_f, size)

    solver = QUBO_SMTI(matching).pre_process()

    solution_qa = solver.solve_qa(verbose=False, num_reads=100)
    store_qa_solution(solution_qa, size, index_f, "smp_qa")

    solution_qbsolv = solver.solve_multi()
    store_qa_solution(solution_qbsolv, size, index_f, "smp_qbsolv")

    stable_solution_qa = solution_qa[solution_qa.stable == 1.0]
    stable_solution_qbsolv = solution_qbsolv[solution_qbsolv.stable == 1.0]
    opt_en = solver.get_optimal_energy(matching.size)

    qa_unique_stable, qa_opt_en = _count_unique_stable_matchings(stable_solution_qa, opt_en)
    qbsolv_unique_stable, qbsolv_opt_en = _count_unique_stable_matchings(stable_solution_qbsolv, opt_en)
    return {"qa_stable": qa_unique_stable, "qa_opt_en": qa_opt_en,
            "qbsolv_stable": qbsolv_unique_stable, "qbsolv_opt_en": qbsolv_opt_en}


def main_smp_measurements(generate_solutions=False):
    if generate_solutions:
        generate_and_save_all_solutions()
    size = 4
    index_f = 0
    compute_smp_results(size, index_f)
