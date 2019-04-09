import matplotlib.pyplot as plt
import numpy as np

import run_cpa
from attack_analyser import AttackAnalyser
from attacker import Attacker

# For several amounts of traces, test the guessing entropy with which the CPA
# attacker is able to guess the first subkey.
TRACES_AMOUNTS = [1, 10, 100, 1000]
TEST_DATA_LOC = "./../test_data"

# Load the 1000 required plaintexts
plaintexts = np.load("./../data/1000_ptext.npy")

cpa_attacker = Attacker(plaintexts)
atk_analyser = AttackAnalyser()

for trace_amnt in TRACES_AMOUNTS:
    # Load and convert the traces
    traces = []
    traces_file = open(f"{TEST_DATA_LOC}/{trace_amnt}_traces", "r")
    for line in traces_file:
        points = line.strip("\n").strip("(").strip(")").split(",")
        trace = [int(point) for point in points]
        traces.append(trace)
    traces_file.close()

    skey = cpa_attacker.obtain_full_private_key(traces)
    full_guessing_entropy = atk_analyser.compute_guessing_entropy(attacker.subkey_coeffs)

if __name__ == '__main__':
    pass
