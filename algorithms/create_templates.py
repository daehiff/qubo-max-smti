import random
import statistics
from copy import deepcopy
import algorithms.storage as store
from algorithms.maching import Matching
import algorithms.utils as ut


def _create_sm_preferences(males, females):
    """
    default sm preferece creation
    :param males:
    :param females:
    :return:
    """
    fem_1 = deepcopy(females)
    male_1 = deepcopy(males)
    males_pref = {}
    females_pref = {}
    for male in males:
        random.shuffle(fem_1)
        males_pref[male] = {fem: index for index, fem in enumerate(fem_1)}
    for female in females:
        random.shuffle(male_1)
        females_pref[female] = {male: index for index, male in enumerate(male_1)}
    return males_pref, females_pref


def _create_smti_preference(persons, other_persons, size, g1, g2):
    """
    create all preferences for one gender
    Preflists currently start at size: 2
    :param persons: either males list or females list
    :param other_persons:  vice versa list to persons
    :param size: how many males females <=> size
    :param g1: (0,1] => possibility that an element will be IN the preflist => determines the lenght
    :param g2: (0,1] => possibility of a tie
    :return:
    """
    assert 0 < g1 <= 1 and 0 < g2 <= 1
    persons_pref = {}
    other_persons_1 = deepcopy(other_persons)
    for person in persons:
        new_len = 2
        for _ in range(size - 2):
            if random.uniform(0, 1) < g1:
                new_len += 1
        random.shuffle(other_persons_1)
        persons_pref[person] = {other_p: index for index, other_p in enumerate(other_persons_1[:new_len])}
        last_person = other_persons_1[0]
        for other_person in other_persons_1[:new_len]:
            random_p2 = random.uniform(0, 1)
            if g2 < random_p2:
                persons_pref[person][other_person] = persons_pref[person][last_person]
            last_person = other_person
    return persons_pref


def create_smti_instance(size: int, g1: float, g2: float):
    """
    create one instance for SMTI
    :param size: how many males females <=> size
    :param g1: (0,1] => possibility that an element will be IN the preflist => determines the lenght
    :param g2: (0,1] => possibility of a tie
    :return:
    """
    assert 0 < g1 <= 1 and 0 < g2 <= 1
    males, females = ut.create_males_and_females(size)
    males_pref = _create_smti_preference(males, females, size, g1, g2)
    females_pref = _create_smti_preference(females, males, size, g1, g2)
    return Matching(males, females, males_pref, females_pref)


def create_and_save_smti(index_f: int, size: int, g1: float, g2: float, compute_solutions=False):
    """
    create one instance for SMTI
    :param index_f: unique sample index
    :param size: how many males females <=> size
    :param g1: (0,1] => possibility that an element will be IN the preflist => determines the lenght
    :param g2: (0,1] => possibility of a tie
    :param compute_solutions: wether or not you want to compute all possible solutions
    :return:
    """
    tmp_match = create_smti_instance(size, g1, g2)
    if compute_solutions:
        tmp_match.compute_all_solutions(mode="SMTI")
    store.store_smti(tmp_match, g1, g2, index_f)
    return tmp_match


def create_and_save_smp(index_f: int, size: int, compute_solutions=False):
    """
    creates and stores one instance of smp, in the corresponding folder
    :param compute_solutions: compute all possible solutions
    :param size: how many males females <=> size
    :param index_f:unique index of this instance, if not unique it will
    :return:
    """
    tmp_match = create_smp_instance(size)
    if compute_solutions:
        tmp_match.compute_all_solutions(mode="SMP")
    store.store_smp(tmp_match, index_f)
    return tmp_match


def create_smp_instance(size: int):
    """
    create a random smp instance
    :param size: size of the instance
    :return:
    """
    males, females = ut.create_males_and_females(size)
    males_pref, females_pref = _create_sm_preferences(males, females)
    return Matching(males, females, males_pref, females_pref)
