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
# plaintexts = np.load("./../data/1000_ptext.npy")  # Our implementation's ptexts
plaintexts = np.load(f"{TEST_DATA_LOC}/plain.npy")

# Load the given ChipWhisperer test traces if we use them
cw_traces = np.load(f"{TEST_DATA_LOC}/traces.npy")

cpa_attacker = Attacker(plaintexts)
atk_analyser = AttackAnalyser()

# Change this boolean to use either the CW data or our own data
using_chipwhisp_data = True

guessing_entropies = {}  # For each trace amount, store the corresponding GE
for trace_amnt in TRACES_AMOUNTS:
    # Load and convert the traces
    traces = []
    if not using_chipwhisp_data:
        traces_file = open(f"{TEST_DATA_LOC}/{trace_amnt}_traces", "r")
        for line in traces_file:
            points = line.strip("\n").strip("(").strip(")").split(",")
            trace = [int(point) for point in points]
            traces.append(trace)
        traces_file.close()
    else:
        traces = cw_traces[:trace_amnt]

    # If we only obtain the first subkey, it is returned as a singleton list.
    skey = cpa_attacker.obtain_full_private_key(traces, only_first_byte=True)

    # Compute and store the first subkey's guessing entropy
    known_first_subkey = 43
    first_subkey_guessing_entropy = \
        atk_analyser.compute_subkey_guessing_entropy(known_first_subkey, cpa_attacker.subkey_corr_coeffs[0])
    print(f"First subkey guessing entropy for {trace_amnt} traces: {first_subkey_guessing_entropy}")
    guessing_entropies[trace_amnt] = first_subkey_guessing_entropy
    # full_guessing_entropy = atk_analyser.compute_guessing_entropy(cpa_attacker.subkey_coeffs)

print(f"Final guessing entropies: {guessing_entropies}")

# Plot amount of traces vs. guessing entropy
plt.title("Subkey guessing entropy ~ Trace amount")
plt.xlabel("Trace amount")
plt.ylabel("Guessing entropy")
plt.grid(True)
plt.semilogx(guessing_entropies.keys(), guessing_entropies.values(), basex=10)
plt.savefig("./data/cpa-traceAmnt-vs-guessingEntropy.png")

print("Stored output plot in ./data/cpa-traceAmnt-vs-guessingEntropy.png")

if __name__ == '__main__':
    pass
