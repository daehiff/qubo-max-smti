import os
import shutil
import algorithms.utils as ut

from algorithms.maching import Matching
import json
import csv

from algorithms.solution import Solution

base_dir = "./storage"


def update_dir(dir_name, do_remove=True, do_replace=True):
    """
    update the current directory
    :param dir_name:
    :param do_replace: if exists do replace
    :param do_remove: if the folder does exitst remove it?
    :return:
    """
    if do_replace:
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        else:
            if do_remove:
                shutil.rmtree(dir_name)
                os.makedirs(dir_name)
    else:
        index = 0
        new_dir = dir_name  # TODO
        while os.path.isdir(new_dir):
            new_dir = f"{dir_name}({index})"
        shutil.rmtree(dir_name)
        os.makedirs(dir_name)


def store_smp(matching, num, index_f):
    """
    Store one smp instance
    :param matching:
    :param num:
    :param index_f:
    :return:
    """
    dir_name = get_smp_folder(matching.size, num, index_f)
    update_dir(dir_name)
    with open(f"{dir_name}/females_pref.json", 'w') as fp:
        json.dump(matching.females_pref, fp)
    with open(f"{dir_name}/males_pref.json", 'w') as fp:
        json.dump(matching.males_pref, fp)


def store_smti(matching: Matching, p1, p2, index_f):
    """
    Store a smti matching
    :param matching: 
    :param num: 
    :param p1: 
    :param p2: 
    :param index_f: 
    :return: 
    """
    dir_name = get_smti_folder(matching.size, p1, p2)
    update_dir(dir_name, do_replace=True, do_remove=False)
    meta = {
        "size": matching.size,  # get paricipants: males = females[ M/W_i for i in range(size) ]
        "males_pref": matching.males_pref,
        "females_pref": matching.females_pref,
        "possible_solutions": matching.solutions

    }
    with open(f"{dir_name}/index_{index_f}.json", 'w') as fp:
        json.dump(meta, fp)


def get_smti(size, p1: float, p2: float, index_f: int) -> Matching:
    """
    Get one stored SMTI instance, by its size, p1, p2, index_f
    :param size: the size of the smp instance
    :param p1: (0,1] => possibility that an element will be IN the preflist => determines the lenght
    :param p2: (0,1] => possibility of a tie
    :param index_f: index of the SMTI instance (unique int)
    :return:
    """
    dir_name = get_smti_folder(size, p1, p2)
    with open(f"{dir_name}/index_{index_f}.json", 'r') as fp:
        meta = json.load(fp)
        males, females = ut.create_males_and_females(meta["size"])
        matching = Matching(males, females, meta["males_pref"], meta["females_pref"],
                            solutions=meta["possible_solutions"])
    assert matching is not None
    return matching


def get_smti_folder(size: int, p1: float, p2: float):
    """
    Get the naming convention for a matching smti folder by its variables
    """
    dir_name = f"{base_dir}/samples/smti/size_{size}_p1_{p1}_p2_{p2}/"
    return dir_name


def get_smp_folder(size: int, num: int, index_f: int):
    # TODO adjust
    """
    Get the naming convention for a matching smti folder by its variables
    """
    dir_name = f"{base_dir}/samples/smp/size_{size}_num_{num}/index_{index_f} "
    return dir_name
