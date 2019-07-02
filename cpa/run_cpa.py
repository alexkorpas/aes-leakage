import numpy as np
import sys

from attacker import Attacker


def main(plaintexts, traces):    
    cpa_attacker = Attacker(plaintexts)
    skey = cpa_attacker.obtain_full_private_key(traces, only_first_byte=True)

    # Our AES key:
    # {166, 40, 136, 9, 43, 171, 174, 207, 79, 210, 21, 22, 247, 60, 126}
    # Our ptexts should be stored in ./../data/1000_ptext.npy

    print(f"First found subkey: {skey[0]}")


if __name__ == '__main__':
    args = sys.argv
    if len(sys.argv) < 3:
        print("Usage: python3 run_cpa.py plaintexts_input traces_input")

    plaintexts_file = sys.argv[1]
    raw_traces_file = sys.argv[2]

    # Convert traces
    traces = []
    file = open(raw_traces_file, "r")
    for line in file:
        points = line.strip("\n").strip("(").strip(")").split(",")
        trace = [int(point) for point in points]
        traces.append(trace)
    file.close()

    # Load 1000 plaintexts and only take the amount we need.
    plaintexts = np.load(plaintexts_file)
    traces_amnt = len(traces)
    plaintexts = plaintexts[:traces_amnt]

    main(plaintexts, traces)
