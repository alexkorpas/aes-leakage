import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json

TEST_NOISE = "../data/2019-04-02_1/trace_100"
OUTPUT_PLOT = "../data/out_plot.jpg"


class PowerReport:
    def __init__(self, input_file=TEST_NOISE):
        with open(input_file, "r") as file:
            first_line = file.readline()
            self.data = pd.DataFrame(json.loads(first_line))

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

        plt.show()
        plt.savefig(filename)

    # def get_bytes(self):
    #     rec = self.data.to_records(index=False)

def main():
    p = PowerReport()
    p.create_figure()


if __name__ == '__main__':
    main()
