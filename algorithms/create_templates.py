import random
import statistics
from copy import deepcopy
import algorithms.storage as store
from algorithms.maching import Matching


def compute_header(matching, num, p1, p2, index_f):
    """
    compute a header for a smti instance
    :param matching:
    :param num:
    :param p1:
    :param p2:
    :param index_f:
    :return:
    """
    pref_len_m = (matching.get_preference_lists_len("m"))
    pref_len_w = (matching.get_preference_lists_len("w"))
    tie_len_m = matching.get_preference_tie_lenght("m")
    tie_len_w = matching.get_preference_tie_lenght("w")

    return {
        "meta": {
            "p1": p1,
            "p2": p2,
            "num": num,
            "index_f": index_f
        },
        "male": {
            "pref": {
                "min": min(pref_len_m),
                "max": max(pref_len_m),
                "med": statistics.median(pref_len_m),
                "mean": statistics.mean(pref_len_m)
            },
            "tie": {
                "min": min(tie_len_m),
                "max": max(tie_len_m),
                "med": statistics.median(tie_len_m),
                "mean": statistics.mean(tie_len_m)
            }
        },
        "female": {
            "pref": {
                "min": min(pref_len_w),
                "max": max(pref_len_w),
                "med": statistics.median(pref_len_w),
                "mean": statistics.mean(pref_len_w)
            },
            "tie": {
                "min": min(tie_len_w),
                "max": max(tie_len_w),
                "med": statistics.median(tie_len_w),
                "mean": statistics.mean(tie_len_w)
            }
        }}


def compute_and_store_header(matching, num, p1, p2, index_f):
    """
    compute and store a header for a smti instance
    :param matching:
    :param num:
    :param p1:
    :param p2:
    :param index_f:
    :return:
    """
    header = compute_header(matching, num, p1, p2, index_f)
    store.store_header(matching.size, num, p1, p2, index_f, header)


def create_males_and_females(size):
    """
    helper to create default males and female
    :param size: how many are required
    :return:
    """
    males = ["M" + str(index) for index in range(size)]
    females = ["W" + str(index) for index in range(size)]
    return males, females


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


def create_smti_preference(persons, other_persons, size, p1, p2):
    """
    create all preferences for one gender
    :param persons: either males list or females list
    :param other_persons:  vice versa list to persons
    :param size: how many males females <=> size
    :param p1: (0,1] => possibility that an element will be IN the preflist => determines the lenght
    :param p2: (0,1] => possibility of a tie
    :return:
    """
    assert 0 < p1 <= 1 and 0 < p2 <= 1
    persons_pref = {}
    other_persons_1 = deepcopy(other_persons)
    for person in persons:
        new_len = 1
        for _ in range(size - 1):
            if random.uniform(0, 1) < p1:
                new_len += 1
        random.shuffle(other_persons_1)
        persons_pref[person] = {other_p: index for index, other_p in enumerate(other_persons_1[:new_len])}
        last_person = other_persons_1[0]
        for other_person in other_persons_1[:new_len]:
            random_p2 = random.uniform(0, 1)
            if p2 < random_p2:
                persons_pref[person][other_person] = persons_pref[person][last_person]
            last_person = other_person
    return persons_pref


def create_smti_instance(size, p1, p2):
    """
    create one instance for SMTI
    :param size: how many males females <=> size
    :param p1: (0,1] => possibility that an element will be IN the preflist => determines the lenght
    :param p2: (0,1] => possibility of a tie
    :return:
    """
    assert 0 < p1 <= 1 and 0 < p2 <= 1
    males, females = create_males_and_females(size)
    males_pref = create_smti_preference(males, females, size, p1, p2)
    females_pref = create_smti_preference(females, males, size, p1, p2)
    return Matching(males, females, males_pref, females_pref)


def create_smp_instance(size):
    males, females = create_males_and_females(size)
    males_pref, females_pref = _create_sm_preferences(males, females)
    return Matching(males, females, males_pref, females_pref)


def create_and_save_smti(num, index_f, size, p1, p2):
    """
    create one instance for SMTI
    :param num:
    :param index_f:
    :param size: how many males females <=> size
    :param p1: (0,1] => possibility that an element will be IN the preflist => determines the lenght
    :param p2: (0,1] => possibility of a tie
    :return:
    """
    tmp_match = create_smti_instance(size, p1, p2)
    store.store_smti(tmp_match, num, p1, p2, index_f)
    return tmp_match


def create_and_save_smp(num, size, index_f):
    """
    creates and stores one instance of smp, in the corresponding folder
    :param num:
    :param size:
    :param index_f:
    :return:
    """
    tmp_match = create_smp_instance(size)
    store.store_smp(tmp_match, num, index_f)
    return tmp_match


def create_random_smp(size):
    """
    create a random smp instance
    :param size: size of the instance
    :return:
    """
    males, females = create_males_and_females(size)
    males_pref, females_pref = _create_sm_preferences(males, females)
    return Matching(males, females, males_pref, females_pref)
