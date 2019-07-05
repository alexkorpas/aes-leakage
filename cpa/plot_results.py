import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_nocm = pd.read_csv('cpa_full_results.csv', index_col=0)
df_cm = pd.read_csv('cpa_cm_full_results.csv', index_col=0)

df_nocm = df_nocm[['TRACES_AMOUNT', 'SAMPLE_STEP', 'GE']]
df_cm = df_cm[['TRACES_AMOUNT', 'SAMPLE_STEP', 'GE']]


common = ['SAMPLE_STEP', 'TRACES_AMOUNT']
df = df_nocm.merge(df_cm, how='left', left_index=True, right_index=True,
                   on=common, suffixes=['_NO_CM', '_CM'])

corr = df.corr().loc[['GE_NO_CM', 'GE_CM'], ['TRACES_AMOUNT', 'SAMPLE_STEP']]
sns.heatmap(corr, annot=True)
plt.savefig('img/cpa_heatmap.png')
plt.close()

avg = df.groupby(common).mean()
std = df.groupby(common).std()

TRACES_AMOUNTS = [2, 3, 12, 48, 192, 768, 1000]
SAMPLE_STEPS = [1, 4, 16]

for step in SAMPLE_STEPS:
    ax = avg.loc[step].plot(yerr=std.loc[step], xticks=TRACES_AMOUNTS)
    ax.set_xscale('log', basex=4)
    plt.xlabel('Amount of traces')
    plt.ylabel('Guessing Entropy')
    plt.title(f'Guessing Entropy with step={step}')
    plt.legend(['No countermeasure', 'Hiding countermeasure'])
    plt.savefig(f'img/cpa_ge_step{step}.png')
    plt.close()
