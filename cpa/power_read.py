import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

TEST_NOISE = "data/example_noise/example_sin_1.csv"
OUTPUT_PLOT = "data/out_plot.jpg"


class PowerReport:
    def __init__(self, input_file=TEST_NOISE):
        self.data = pd.read_csv(input_file)

    def create_figure(self, filename=OUTPUT_PLOT):
        """
        Displays the data contained by this power report.
        """
        plt.figure()
        self.data.plot()
        plt.title("Power consumption analysis")

        wheel = plt.rcParams['axes.prop_cycle'].by_key()['color']
        spread_legend = mpatches.Patch(color=wheel[0], label='Power consumption')
        plt.legend(handles=[spread_legend])

        plt.ylabel('Power')
        plt.xlabel("Time")

        plt.savefig(filename)

    def get_bytes(self):
        rec = self.data.to_records(index=False)

def main():
    p = PowerReport()
    p.get_bytes()


if __name__ == '__main__':
    main()