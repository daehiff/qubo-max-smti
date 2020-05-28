import os
import shutil
import algorithms.utils as ut

from algorithms.maching import Matching
import json
import csv

from algorithms.solution import Solution

base_dir = "./storage"


def store_response(lp_res, response, solver, size, num, p1, p2, index_f, num_rep, retry):
    resp_data = compute_qubo_response(lp_res, response, solver)
    resp_folder = f"{base_dir}/results/qubo_responses/size_{size}_num_{num}/p1_{p1}_p2_{p2}/numrep_{num_rep}_sample_{index_f}"
    update_dir(resp_folder, do_remove=False)
    with open(f"{resp_folder}/response_{retry}.json", "w") as fp:
        json.dump(resp_data, fp)


def compute_sample(sample, energy, solver):
    ret_match = solver.encode(sample)
    stability = Solution(solver.matching, ret_match).is_stable(mode="smti")
    return {
        "sample": f"{sample}",
        "energy": energy,
        "stability": stability
    }


def compute_qubo_response(lp_res, response, solver):
    if response is None:
        return {"none": True}
    energies = list(response.data_vectors['energy'])
    min_en = min(energies)
    samples = list(response.samples())
    min_sample = samples[energies.index(min_en)]
    min_sample_data = compute_sample(min_sample, min_en, solver)
    return {
        "lp_out": {
            "en": lp_res[0],
            "stability": lp_res[1]
        },
        "min": min_sample_data,
        "samples": [compute_sample(samples[i], energy, solver) for i, energy in enumerate(energies)]
    }


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


def get_smti(size, num, p1, p2, index_f):
    """
    Get a smti matching
    :param m_type:
    :param size:
    :param num:
    :param p1:
    :param p2:
    :param index_f:
    :return:
    """
    dir_name = get_smti_folder(size, num, p1, p2, index_f)
    if not os.path.isdir(dir_name):
        raise Exception(f"folder{dir_name} was not found, check your Storage")
    males, females = ut.create_males_and_females(size)
    with open(f"{dir_name}/females_pref.json", 'r') as fp:
        females_pref = json.load(fp)
    with open(f"{dir_name}/males_pref.json", 'r') as fp:
        males_pref = json.load(fp)
    return Matching(males, females, males_pref, females_pref)


def store_smp(matching, num, index_f):
    dir_name = get_smp_folder(matching.size, num, index_f)
    update_dir(dir_name)
    with open(f"{dir_name}/females_pref.json", 'w') as fp:
        json.dump(matching.females_pref, fp)
    with open(f"{dir_name}/males_pref.json", 'w') as fp:
        json.dump(matching.males_pref, fp)


def create_results(solution_vector, results_path, file_name):
    """
    create a brand new file, deletes the old one (most likely used by creating a header)
    :param solution_vector:
    :param results_path:
    :param file_name:
    :return:
    """
    dir_name = f"{base_dir}/results/{results_path}"
    update_dir(dir_name, do_remove=False)
    with open(f"{dir_name}/{file_name}", 'w') as f:
        wr = csv.writer(f)
        wr.writerow(solution_vector)


def store_results(solution_vector, results_path, file_name):
    """
    append a solution vector to a given filename
    :param solution_vector:
    :param results_path: the path in the results folder
    :param file_name: how the files gonna called
    :return:
    """
    dir_name = f"{base_dir}/results/{results_path}"
    update_dir(dir_name, do_remove=False)
    with open(f"{dir_name}/{file_name}", 'a') as f:
        wr = csv.writer(f)
        wr.writerow(solution_vector)


def store_smti(matching, num, p1, p2, index_f):
    """
    Store a smti matching
    :param matching: 
    :param num: 
    :param p1: 
    :param p2: 
    :param index_f: 
    :return: 
    """
    dir_name = get_smti_folder(matching.size, num, p1, p2, index_f)
    update_dir(dir_name)
    with open(f"{dir_name}/females_pref.json", 'w') as fp:
        json.dump(matching.females_pref, fp)
    with open(f"{dir_name}/males_pref.json", 'w') as fp:
        json.dump(matching.males_pref, fp)


def get_smti_folder(size, num, p1, p2, index_f):
    """
    Get the naming convention for a matching smti folder by its variables
    """
    dir_name = f"{base_dir}/samples/smti/size_{size}_num_{num}/p1_{p1}_p2_{p2}/index_{index_f} "
    return dir_name


def get_smp_folder(size, num, index_f):
    """
    Get the naming convention for a matching smti folder by its variables
    """
    dir_name = f"{base_dir}/samples/smp/size_{size}_num_{num}/index_{index_f} "
    return dir_name


def get_results_csv(path_name):
    out = []
    with open(path_name, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            out.append(list(row))
    return out


def store_header(size, num, p1, p2, index_f, header):
    dir_name = get_smti_folder(size, num, p1, p2, index_f)
    with open(f"{dir_name}/header.json", 'w') as fp:
        json.dump(header, fp)
    return None


def store_object(object, filename, type="JSON"):
    update_dir(f"{base_dir}/other", do_remove=False)
    dir_name = f"{base_dir}/other/{filename}"

    with open(f"{dir_name}", 'w') as fp:
        if type == "JSON":
            json.dump(object, fp)
        elif type == "LIST":
            wr = csv.writer(fp)
            wr.writerow(object)
        else:
            raise Exception(f"unknown type: {type}")


def get_object(filename, type="JSON"):
    dir_name = f"{base_dir}/other/{filename}"

    with open(f"{dir_name}", 'r') as fp:
        if type == "JSON":
            return json.load(fp)
        elif type == "LIST":
            out = []
            reader = csv.reader(fp)
            for row in reader:
                out.append(list(row))
            return out
        else:
            raise Exception(f"unknown type: {type}")


def get_smti_computational_time(size, p1, p2):
    named_dir = f"{base_dir}/results/size_{size}_num_50"
    file_name = f"p1_{p1}p2_{p2}.csv"
    out = []
    with open(f"{named_dir}/{file_name}", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            out.append(list(map((lambda el: el), row)))
    return out
