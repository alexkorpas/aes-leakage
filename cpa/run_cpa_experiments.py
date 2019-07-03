import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import run_cpa
from attack_analyser import AttackAnalyser
from attacker import Attacker

# For several amounts of traces, test the guessing entropy with which the CPA
# attacker is able to guess the first subkey.
TEST_DATA_LOC = "./input"
# TRACES_AMOUNTS = [3, 12, 48, 192, 768]  
# SAMPLE_STEPS = [1, 4, 16]
TRACES_AMOUNTS = [12, 96, 768]
SAMPLE_STEPS = [16]
FULL = True
ITERATIONS = 10
TOTAL_EXPIREMENTS = len(TRACES_AMOUNTS) * len(SAMPLE_STEPS) * ITERATIONS
# Load the 1000 required plaintexts
# plaintexts = np.load("./../data/1000_ptext.npy")
# Our implementation's ptexts
plaintexts = np.load(f"{TEST_DATA_LOC}/no-cm/bytes_plain.npy")

# Load the acquired traces
traces = np.load(f"{TEST_DATA_LOC}/no-cm/traces.npy")

cpa_attacker = Attacker(plaintexts)
atk_analyser = AttackAnalyser()

results = pd.DataFrame(columns=['TRACES_AMOUNTS', 'SAMPLE_STEPS', 'GE',
                                'KEY_SR', 'SUBKEY_SR', 'FULL'], dtype=int)

known_key = [43, 126, 21, 22, 40, 174, 210, 166,
             171, 247, 21, 136, 9, 207, 79, 60]

np.random.seed(42)
i = 0
for _ in range(1):
    for trace_amnt in TRACES_AMOUNTS:
        for step in SAMPLE_STEPS:
            sampled_traces = traces[np.random.choice(traces.shape[0], trace_amnt,
                                                    replace=False), :]
            sampled_traces = sampled_traces[:, ::step]
            import ipdb; ipdb.set_trace()
            # If we only obtain the first subkey, it is returned
            # as a singleton list.
            best_guess = cpa_attacker.obtain_full_private_key(
                traces, only_first_byte=False)

            ge = atk_analyser.compute_guessing_entropy(
                known_key, cpa_attacker.subkey_corr_coeffs)
            key_sr = (ge == 0)
            subkey_sr = atk_analyser.compute_subkey_success_rate(known_key, best_guess)
            results.loc[i] = [trace_amnt, step, ge, key_sr, subkey_sr, FULL]
            i += 1
            print(f"Experiement {i}/{TOTAL_EXPIREMENTS} [trace amount:{trace_amnt}, step: {step}]:"
                  f"GE: {ge}\tKEY SR: {key_sr}\tSUBKEY SR: {subkey_sr}")

results.to_csv(f"cpa_{'full' if FULL else 'cropped'}_results.csv")

# print(f"Final guessing entropies: {guessing_entropies}")

# # Plot amount of traces vs. guessing entropy
# plt.title("Subkey guessing entropy ~ Trace amount")
# plt.xlabel("Trace amount")
# plt.ylabel("Guessing entropy")
# plt.grid(True)
# plt.semilogx(guessing_entropies.keys(), guessing_entropies.values(), basex=10)
# plt.savefig("./data/cpa-traceAmnt-vs-guessingEntropy.png")

# print("Stored output plot in ./data/cpa-traceAmnt-vs-guessingEntropy.png")

# if __name__ == '__main__':
#     pass
