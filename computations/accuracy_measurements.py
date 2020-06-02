from copy import deepcopy

from algorithms.solution import Solution
from algorithms.solver.SMTI.kiraly.kiralySMTI import Kirialy2
from algorithms.solver.SMTI.lp_smti import LP_smti
from algorithms.solver.SMTI.qubo_smti import QUBO_SMTI
from algorithms.solver.SMTI.shift_brk.shift_brk import ShiftBrk
from algorithms.storage import get_smti, store_qa_solution, get_solution_qa, store_computation_result
import algorithms.utils as ut
import pandas as pd
from computations.config import *


def main_accuracy():
    df_acc = pd.DataFrame()
    for size in sizes_smti:
        for index_f in range(samples_per_size_smti):
            out = compute_accuracy_measurement(size, index_f)
            df_acc = df_acc.append(out, ignore_index=True)

    store_computation_result(df_acc, "accuracy_results")

    df_acc = pd.DataFrame()
    for size in sizes_smti:
        for index_f in range(samples_per_size_smti):
            out = compute_qubo_en(size, index_f)
            df_acc = df_acc.append(out, ignore_index=True)

    store_computation_result(df_acc, "qbsolv_en_results")


def eval_algorithm(size, index_f, solver_type):
    matching = get_smti(index_f, size)
    if solver_type == "qbsolv":
        return QUBO_SMTI(matching).solve().is_stable()
    elif solver_type == "qa":
        solutions = QUBO_SMTI(matching).solve_qa(verbose=False)
        store_qa_solution(solutions, size, index_f, "smti")
        min_solution = solutions[solutions.energy == solutions.energy.min()]
        return Solution(matching, min_solution["match"][0]).is_stable()
    elif solver_type == "lp":
        return LP_smti(matching).solve().is_stable()
    elif solver_type == "shiftbrk":
        return ShiftBrk(matching).solve().is_stable()
    elif solver_type == "kiraly":
        return Kirialy2(matching).solve().is_stable()
    else:
        raise Exception(f"unknown solver_type: {solver_type}")


def compute_accuracy_measurement(size, index_f):  # TODO test
    solver_types = ["qbsolv", "qa", "lp", "shiftbrk", "kiraly"]
    out = {}
    for solver_type in solver_types:
        stable, size = eval_algorithm(size, index_f, solver_type)
        out[f"{solver_type}_stable"] = stable
        out[f"{solver_type}_size"] = size
    return out


def compute_qubo_en(size, index_f):
    matching = get_smti(index_f, size)
    lp_en = compute_lp_energy(matching)

    qa_solution = get_solution_qa(size, index_f, "smti")
    qa_en = min(qa_solution["energy"])  # todo find correct index

    solution = QUBO_SMTI(matching).solve()
    qbsolv_en = solution.energy

    return {"qa_en": qa_en, "lp_en": lp_en, "qbsolv_en": qbsolv_en}


def compute_lp_energy(matching):
    solver = QUBO_SMTI(matching, mode="np").pre_process()
    solution_lp = LP_smti(matching).solve()
    x = ut.compute_qubo_vector_lp(solution_lp, solver)
    return solver.compute_energy(x)
