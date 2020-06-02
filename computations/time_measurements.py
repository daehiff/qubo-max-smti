import logging
import timeit

from algorithms.solver.SMTI.kiraly.kiralySMTI import Kirialy2
from algorithms.solver.SMTI.lp_smti import LP_smti
from algorithms.solver.SMTI.qubo_smti import QUBO_SMTI
from algorithms.solver.SMTI.shift_brk.shift_brk import ShiftBrk
from algorithms.storage import get_smti, store_computation_result
import numpy as np
import pandas as pd
import algorithms.utils as ut

from computations.config import *

log = logging.getLogger()


def create_setup(size, index_f):
    return f"""
from algorithms.solver.SMTI.kiraly.kiralySMTI import Kirialy2
from algorithms.solver.SMTI.lp_smti import LP_smti
from algorithms.solver.SMTI.qubo_smti import QUBO_SMTI
from algorithms.solver.SMTI.shift_brk.shift_brk import ShiftBrk
from algorithms.storage import get_smti
matching = get_smti(index_f={index_f},size={size} )
    """


def get_solver(solver_type):
    if solver_type == "qubo":
        return "QUBO_SMTI(matching)"
    elif solver_type == "lp":
        return "LP_smti(matching)"
    elif solver_type == "shiftbrk":
        return "ShiftBrk(matching)"
    elif solver_type == "kiraly":
        return "Kirialy2(matching)"
    else:
        raise Exception(f"unknown solver_type: {solver_type}")


def eval_algorithm(matching, solver_type):
    if solver_type == "qubo":
        return QUBO_SMTI(matching).solve()
    elif solver_type == "lp":
        return LP_smti(matching).solve()
    elif solver_type == "shiftbrk":
        return ShiftBrk(matching).solve()
    elif solver_type == "kiraly":
        return Kirialy2(matching).solve()
    else:
        raise Exception(f"unknown solver_type: {solver_type}")


def measure_solving(solver_type, setup, times_repeat=10):
    solver = get_solver(solver_type)
    times = timeit.repeat(f"{solver}.solve()", setup=setup, repeat=times_repeat, number=1)
    return np.mean(times), np.var(times)


def measure_preprocessing(solver_type, setup, times_repeat=10):
    solver = get_solver(solver_type)
    times = timeit.repeat(f"{solver}.pre_process()", setup=setup, repeat=times_repeat, number=1)
    return np.mean(times), np.var(times)


def measure_time_instance(size, index_f, times_repeat=10):
    """
    Measure one instance with all available algorithms:
        - qubo
        - lp
        - shiftbrk
        - kiraly2
    time gets measured by timeit in seconds
    :param size:
    :param index_f:
    :param times_repeat:
    :return:
    """
    solver_types = ["qubo", "lp", "shiftbrk", "kiraly"]  # TODO zeit messung QA, ist das überhaupt sinvoll?
    setup = create_setup(size, index_f)
    result = {"size": size, "index_f": index_f}
    for solver_type in solver_types:
        d_t, d_t_var = measure_solving(solver_type, setup, times_repeat=times_repeat)
        solution = eval_algorithm(get_smti(index_f=index_f, size=size), solver_type)
        (stable, size_res) = solution.is_stable()
        result[f"{solver_type}_dt[s]"] = d_t
        result[f"{solver_type}_dt_var[%]"] = 100 * d_t_var / d_t
        result[f"{solver_type}_stable"] = stable
        result[f"{solver_type}_size"] = size_res
    return result


def measure_lp_qubo_preprocessing(size, index_f, times_repeat=10):
    """
    Compare the solving/preprocessing part of QUBO-MAX-SMTI with LP-MAX-SMTI
    :param size:
    :param index_f:
    :param times_repeat:
    :return:
    """
    solver_types = ["qubo", "lp"]
    setup = create_setup(size, index_f)
    result = {"size": size, "index_f": index_f}
    for solver_type in solver_types:
        solver = get_solver(solver_type)
        preprocessed_setup = setup + f"\n{solver}.pre_process()"
        d_t_solving, d_t_var_solving = measure_solving(solver_type, preprocessed_setup, times_repeat=times_repeat)
        d_t_preprocessing, d_t_var_preprocessing = measure_preprocessing(solver_type, setup, times_repeat=times_repeat)
        result[f"{solver_type}_solving[s]"] = d_t_solving
        result[f"{solver_type}_solving_var[%]"] = d_t_var_solving
        result[f"{solver_type}_pp[s]"] = d_t_preprocessing
        result[f"{solver_type}_pp_var[%]"] = d_t_var_preprocessing
    return result


def main_time_measure():
    ut.init_log()
    log.info(f"Starting Time Measurement")
    df_time = pd.DataFrame()
    for size in sizes_smti:
        for index_f in range(samples_per_size_smti):
            log.info(f"At: {size}, {index_f}")
            out = measure_time_instance(size, index_f, times_repeat=10)
            df_time = df_time.append(out, ignore_index=True)
    log.info("Done!")
    store_computation_result(df_time, "time_result")
