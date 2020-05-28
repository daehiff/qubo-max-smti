import itertools
import logging
import sys


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


def get_all_matches(males, females, size, mode="SMTI"):
    if mode == "SMTI":
        all_matches = []
        all_combinations = list(itertools.product(males, females))
        for i in range(1, size + 1):
            tmp = list(map(lambda x: {m: w for m, w in x}, itertools.combinations(all_combinations, i)))
            all_matches = all_matches + tmp
        # all_matches = [dict(s) for s in set(frozenset(d.items()) for d in all_matches)]
        return all_matches
    elif mode == "SMP":
        all_comb = [list(zip(x, females)) for x in itertools.permutations(males, size)]
        all_comb = [{m: w for m, w in t} for t in all_comb]
        return all_comb
    else:
        raise Exception(f"unimplemented mode: {mode}")
