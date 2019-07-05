import numpy as np
from ta import TAAttacker
from metrics import guessing_entropy, subkey_success_rate
import csv
import time
import pandas as pd
import matplotlib.pyplot as plt


TEMPLATE_SIZES = [10000, 15000, 20000]
ATTACK_SIZES = [25, 50, 75, 100]
SAMPLE_STEPS = [1, 2, 3]
ITERATIONS = 10
TOTAL_EXPIREMENTS = len(TEMPLATE_SIZES) * len(ATTACK_SIZES) * \
                    len(SAMPLE_STEPS) * ITERATIONS
CM = False

if CM:
    CM_DIR = "cm"
else:
    CM_DIR = "no-cm"
results = pd.DataFrame(columns=['TEMPLATE_SIZE', 'ATTACK_SIZE', 'SAMPLE_STEP',
                                'GE', 'KEY_SR', 'SUBKEY_SR'], dtype=int)
traces = np.load(f'data/{CM_DIR}/traces.npy')
ptext = np.load(f'data/{CM_DIR}/plain.npy')
key = np.load(f'data/{CM_DIR}/key.npy')

tempTraces = traces[:20000]
tempPText = ptext[:20000]
tempKey = key[:20000]
atkTraces = traces[-1000:]
atkPText = ptext[-1000:]
atkKey = key[-1000:]


known_key = atkKey[0]

np.random.seed(42)
i = 0
for _ in range(ITERATIONS):
    for temp_size in TEMPLATE_SIZES:
        for step in SAMPLE_STEPS:
            temp_indices = np.random.choice(
                np.arange(len(tempTraces)), temp_size, replace=False)

            sampled_tempTraces = tempTraces[temp_indices, ::step]
            sampled_tempPText = tempPText[temp_indices, :]
            sampled_tempKey = tempKey[temp_indices, :]

            ta = TAAttacker(5, pooled=False)
            print(f"Profiling using {temp_size} traces...")
            ta.profile(sampled_tempTraces, sampled_tempPText, sampled_tempKey)

            for atk_size in ATTACK_SIZES:
                print(f"Experiment {i+1}/{TOTAL_EXPIREMENTS}(sample step: {step})")

                atk_indices = np.random.choice(
                    np.arange(len(atkTraces)), atk_size, replace=False)
                sampled_atkTraces = atkTraces[atk_indices, ::step]
                sampled_atkPText = atkPText[atk_indices, :]

                # try:
                print(f"Attacking using {atk_size} traces...")
                refs = ta.attack(sampled_atkTraces, sampled_atkPText)
                best_guess = ta.bestguess

                ge = guessing_entropy(known_key, refs)
                key_sr = int(ge == 0)
                subkey_sr = subkey_success_rate(
                    known_key, best_guess)
                # except Exception as e:
                #     ge = np.nan
                #     key_sr = np.nan
                #     subkey_sr = np.nan
                #     print('Singular table found!')
                results.loc[i] = [temp_size, atk_size,
                                  step, ge, key_sr, subkey_sr]
                i += 1
                print(f"RESULTS\t-->\tGE: {ge}\tKEY SR: {key_sr}\tSUBKEY SR: {subkey_sr}")

results.to_csv(f"ta_results.csv")
