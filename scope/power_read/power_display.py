import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

TEST_NOISE = "../data/images/trace"
OUTPUT_PLOT = "../data/images/trace.png"


def trace_parser(trace_line):
    trace_line = trace_line[1:len(trace_line) - 2]
    return [int(x) for x in trace_line.split(",")]


class PowerReport:
    def __init__(self, input_file=TEST_NOISE):
        with open(input_file, "r") as file:
            first_line = file.readline()
            self.data = pd.DataFrame(trace_parser(first_line))

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
        plt.ylim((-100, 300))

        if filename is not None:
            plt.savefig(filename)
        else:
            plt.show()


def main():
    p = PowerReport()
    p.create_figure()


if __name__ == '__main__':
    main()
