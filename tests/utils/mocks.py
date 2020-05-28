from copy import deepcopy

from algorithms.maching import Matching

females = ["W0", "W1", "W2", "W3", "W4"]
males = ["M0", "M1", "M2", "M3", "M4"]


####################################
# Mock functions
####################################

def mock_matching_smti(mock_nr=0):
    if mock_nr == 0:
        return Matching(deepcopy(males), deepcopy(females), deepcopy(males_pref_smti), deepcopy(females_pref_smti))
    elif mock_nr == 1:
        return Matching(deepcopy(males), deepcopy(females), deepcopy(males_pref_smti_1), deepcopy(females_pref_smti_1))
    elif mock_nr == 2:
        return Matching(deepcopy(males[:2]), deepcopy(females[:2]),
                        deepcopy(males_pref_smti_2),
                        deepcopy(females_pref_smti_2))
    else:
        raise Exception(f"unknown mock nr {mock_nr}")


def mock_matching_smp():
    return Matching(deepcopy(males), deepcopy(females), deepcopy(males_pref_smp), deepcopy(females_pref_smp))


####################################
#      SMTI MOCK #1
####################################

smti_instance_solution = {'M0': 'W3', 'M1': 'W0', 'M4': 'W2'}

females_pref_smti = {
    "W0": {
        "M4": 0,
        "M2": 1,
        "M1": 2,
        "M0": 3
    },
    "W1": {
        "M3": 0,
        "M1": 1,
        "M0": 1
    },
    "W2": {
        "M1": 0,
        "M4": 1
    },
    "W3": {
        "M0": 0,
        "M4": 1,
        "M2": 1
    },
    "W4": {
        "M3": 0,
        "M4": 0
    }
}

males_pref_smti = {
    "M0": {
        "W4": 0,
        "W3": 0
    },
    "M1": {
        "W0": 0,
        "W4": 0,
        "W1": 2
    },
    "M2": {
        "W1": 0
    },
    "M3": {
        "W0": 0,
        "W3": 0
    },
    "M4": {
        "W2": 0,
        "W3": 1,
        "W0": 2,
        "W1": 2
    }
}

####################################
#      SMTI MOCK #2
####################################

smti_instance_solution_1 = {'M0': 'W3', 'M1': 'W0', 'M4': 'W2'}

females_pref_smti_1 = {
    "W0": {
        "M4": 0,
        "M2": 0,
        "M1": 1,
        "M0": 2
    },
    "W1": {
        "M3": 0,
        "M1": 1,
        "M0": 1
    },
    "W2": {
        "M1": 0,
        "M4": 1
    },
    "W3": {
        "M0": 0,
        "M4": 1,
        "M2": 1
    },
    "W4": {
        "M3": 0,
        "M4": 0
    }
}

males_pref_smti_1 = {
    "M0": {
        "W4": 0,
        "W3": 1,
        "W2": 2
    },
    "M1": {
        "W0": 0,
        "W4": 1,
        "W1": 2
    },
    "M2": {
        "W1": 0
    },
    "M3": {
        "W0": 0,
        "W3": 1
    },
    "M4": {
        "W2": 0,
        "W3": 1,
        "W0": 2,
        "W1": 3
    }
}

####################################
#       SMTI MOCK #3
####################################

females_pref_smti_2 = {
    "W0": {
        "M0": 0,
        "M1": 0,
    },
    "W1": {
        "M0": 0,
        "M1": 0
    }
}

males_pref_smti_2 = {
    "M0": {
        "W0": 0,
        "W1": 0
    },
    "M1": {
        "W0": 0,
        "W1": 0
    }
}

####################################
#      SMP MOCKS
####################################

smp_solution = {'M0': 'W1', 'M1': 'W2', 'M2': 'W4', 'M3': 'W3', 'M4': 'W0'}

females_pref_smp = {
    "W0": {
        "M1": 0,
        "M2": 1,
        "M0": 2,
        "M3": 3,
        "M4": 4
    },
    "W1": {
        "M3": 0,
        "M1": 1,
        "M0": 2,
        "M4": 3,
        "M2": 4
    },
    "W2": {
        "M3": 0,
        "M2": 1,
        "M0": 2,
        "M4": 3,
        "M1": 4
    },
    "W3": {
        "M3": 0,
        "M2": 1,
        "M4": 2,
        "M0": 3,
        "M1": 4
    },
    "W4": {
        "M1": 0,
        "M4": 1,
        "M0": 2,
        "M3": 3,
        "M2": 4
    }
}

males_pref_smp = {
    "M0": {
        "W3": 0,
        "W1": 1,
        "W0": 2,
        "W4": 3,
        "W2": 4
    },
    "M1": {
        "W2": 0,
        "W1": 1,
        "W4": 2,
        "W3": 3,
        "W0": 4
    },
    "M2": {
        "W4": 0,
        "W3": 1,
        "W2": 2,
        "W1": 3,
        "W0": 4
    },
    "M3": {
        "W3": 0,
        "W4": 1,
        "W1": 2,
        "W0": 3,
        "W2": 4
    },
    "M4": {
        "W0": 0,
        "W3": 1,
        "W4": 2,
        "W2": 3,
        "W1": 4
    }
}
