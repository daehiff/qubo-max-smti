import logging
import sys

from algorithms.maching import Matching


def init_log():
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    fh = logging.FileHandler('log.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    logging.getLogger().addHandler(sh)
    logging.getLogger().addHandler(fh)


def create_males_and_females(size):
    males = ["M" + str(index) for index in range(size)]
    females = ["W" + str(index) for index in range(size)]
    return males, females


def deepcopy_matching(matching):
    return Matching(matching.males, matching.females, matching.males_pref, matching.females_pref)


def compute_qubo_vector_lp(lp_solution, solver):
    ret_match = [0.0 for i in range(solver.qubo_size)]
    if len(ret_match) == 0:
        return ret_match
    for m, w in lp_solution.solution_m.items():
        i = solver.rev_encoding[(m, w)]
        ret_match[i] = 1
    return ret_match


def is_sorted(list: list):
    return all(list[i] <= list[i + 1] for i in range(len(list) - 1))
