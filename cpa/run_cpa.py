import numpy as np
import sys

from attacker import Attacker


def main(plaintexts, traces):
    cpa_attacker = Attacker(plaintexts)
    skey = cpa_attacker.obtain_full_private_key(traces, only_first_byte=False)

    # Our AES key:
    # [43, 126, 21, 22, 40, 174, 210, 166, 171, 247, 21, 136, 9, 207, 79, 60]

    # print(f"First found subkey: {skey[0]}")
    print(f"Found full key: {skey}")


if __name__ == '__main__':
    args = sys.argv
    if len(sys.argv) < 3:
        print("Usage: python3 run_cpa.py plaintexts_input traces_input npy_traces_bool")

    # Our ptexts should be stored in ./../data/1000_ptext.npy
    plaintexts_file = sys.argv[1]
    raw_traces_file = sys.argv[2]
    used_npy_traces = bool(sys.argv[3])

    # If we used npy files for traces and ptexts, call the attacker right away
    if used_npy_traces:
        ptexts = np.load(plaintexts_file)
        traces = np.load(raw_traces_file)

        length = min(len(ptexts), len(traces))
        ptexts = ptexts[:length]
        traces = traces[:length]

        main(ptexts, traces)
        exit()

    # Convert traces
    traces = []
    file = open(raw_traces_file, "r")
    for line in file:
        points = line.strip("\n").strip("(").strip(")").split(",")
        trace = [int(point) for point in points]
        traces.append(trace)
    file.close()
    # traces = traces[5:]  # Omit the two non-encryption traces

    # Load 1000 plaintexts and only take the amount we need.
    plaintexts = np.load(plaintexts_file)
    traces_amnt = len(traces)
    plaintexts = plaintexts[:traces_amnt]
    # plaintexts = plaintexts[5:traces_amnt + 5] # Take the corresponding PTXTs

    main(plaintexts, traces)


# # Convert traces
# traces = []
# raw_traces_file = "./trace_math_100"
# file = open(raw_traces_file, "r")
# for line in file:
#     points = line.strip("\n").strip("(").strip(")").split(",")
#     trace = [int(point) for point in points]
#     traces.append(trace)
# file.close()
# traces = traces[5:]  # Omit the two non-encryption traces
