import logging

from algorithms.solution import Solution
from algorithms.solver.SMTI.kiraly.kiralySMTI import Kirialy2
from algorithms.solver.SMTI.lp_smti import LP_smti
from algorithms.solver.SMTI.qubo_smti import QUBO_SMTI
from algorithms.solver.SMTI.shift_brk.shift_brk import ShiftBrk
from algorithms.storage import get_smti, store_qa_solution, get_solution_qa, store_computation_result
import algorithms.utils as ut
import pandas as pd
from computations.config import *

log = logging.getLogger()


def main_accuracy(max_qubo_size=8):
    ut.init_log()
    log.info("Starting Accurcay Measurement for SMTI")
    log.info("Evaluating against other algorithms..")
    df_acc = pd.DataFrame()
    for size in sizes_smti:
        for index_f in range(samples_per_size_smti):
            log.info(f"At: {size}, {index_f}")
            out = compute_accuracy_measurement(size, index_f, use_qa=(size < max_qubo_size))
            df_acc = df_acc.append(out, ignore_index=True)

    store_computation_result(df_acc, "accuracy_results")
    log.info("DONE!")
    log.info("Checking Energy")

    df_acc = pd.DataFrame()
    for size in sizes_smti:
        for index_f in range(samples_per_size_smti):
            log.info(f"At: {size}, {index_f}")
            out = compute_qubo_en(size, index_f, use_qa=(size < max_qubo_size))
            if out is not None:
                df_acc = df_acc.append(out, ignore_index=True)
    log.info("Done!")
    store_computation_result(df_acc, "qbsolv_en_results")


def eval_algorithm(size, index_f, solver_type):
    matching = get_smti(index_f, size)
    if solver_type == "qbsolv":
        return QUBO_SMTI(matching).solve().is_stable()
    elif solver_type == "qa":
        solutions = QUBO_SMTI(matching).solve_qa(verbose=False)
        store_qa_solution(solutions, size, index_f, "smti")
        min_solution = solutions[solutions.energy == solutions.energy.min()]
        log.info(solutions)
        log.info(min_solution)
        return Solution(matching, min_solution["match"].to_numpy()[0]).is_stable()
    elif solver_type == "lp":
        return LP_smti(matching).solve().is_stable()
    elif solver_type == "shiftbrk":
        return ShiftBrk(matching).solve().is_stable()
    elif solver_type == "kiraly":
        return Kirialy2(matching).solve().is_stable()
    else:
        raise Exception(f"unknown solver_type: {solver_type}")


def compute_accuracy_measurement(size, index_f, use_qa=False):
    solver_types = ["qbsolv", "qa", "lp", "shiftbrk", "kiraly"]
    out = {"size": size, "index_f": index_f}
    for solver_type in solver_types:
        if solver_type == "qa" and not use_qa:
            continue
        stable, res_size = eval_algorithm(size, index_f, solver_type)
        out[f"{solver_type}_stable"] = stable
        out[f"{solver_type}_size"] = res_size

    return out


def compute_qubo_en(size, index_f, use_qa=False):
    matching = get_smti(index_f, size)
    lp_en = compute_lp_energy(matching)
    if use_qa:
        qa_solution = get_solution_qa(size, index_f, "smti")
        qa_en = min(qa_solution["energy"])
    else:
        qa_en = 0.0
    solution = QUBO_SMTI(matching).solve()
    qbsolv_en = solution.energy

    return {"size": size, "index_f": index_f, "qa_en": qa_en, "lp_en": lp_en, "qbsolv_en": qbsolv_en}


def compute_lp_energy(matching):
    solver = QUBO_SMTI(matching, mode="np").pre_process()
    solution_lp = LP_smti(matching).solve()
    x = ut.compute_qubo_vector_lp(solution_lp, solver)
    return solver.compute_energy(x)
