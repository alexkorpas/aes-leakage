import csv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Import the result-containing data frames and store them in a dictionary
no_cm_df = pd.read_csv("ta_results.csv", index_col=0)
cm_df = pd.read_csv("ta_results_cm.csv", index_col=0)
dfs = {
    "no-cm": no_cm_df,
    "cm": cm_df
}

# When evaluating one variable, the others will be constant. We define these
# constants based on each variable's value in the run with the lowest GE on
# the traces that resulted from AES without countermeasures.
best_run_results = no_cm_df[no_cm_df.GE == no_cm_df.GE.min()]
const_tempsize = int(best_run_results.TEMPLATE_SIZE)
const_atksize = int(best_run_results.ATTACK_SIZE)
const_step = int(best_run_results.SAMPLE_STEP)

for (cm_id, df) in dfs.items():
    # Construct the DFs that will be evaluated for each value, respectively
    eval_dfs = {
        "TEMPLATE_SIZE": df[(df.ATTACK_SIZE == const_atksize) & (df.SAMPLE_STEP == const_step)],
        "ATTACK_SIZE": df[(df.TEMPLATE_SIZE == const_tempsize) & (df.SAMPLE_STEP == const_step)],
        "SAMPLE_STEP": df[(df.TEMPLATE_SIZE == const_tempsize) & (df.ATTACK_SIZE == const_atksize)]
    }

    # Constructs box plots to evaluate the influence of #traces and #points on GE.
    for var in ["TEMPLATE_SIZE", "ATTACK_SIZE", "SAMPLE_STEP"]:
        # When evaluating one variable, keep the other variables constant
        sub_df = eval_dfs[var]

        data = [sub_df[sub_df[var] == v].GE for v in sub_df[var].unique()]
        # Set whis=inf to force the whiskers to extend to min and max values
        plt.boxplot(data, labels=sub_df[var].unique().astype(int))
        plt.xlabel(var)
        plt.ylabel("Guessing entropy (GE)")
        plt.title(f"{var} ~ GE for TA {'with' if cm_id == 'cm' else 'without'} countermeasures")
        plt.savefig(f"./figs/{var}-vs-ge-box-{cm_id}.png")
        plt.show()

# Create a scatter plot showing the GE for severl param combinations
