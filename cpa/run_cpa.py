import numpy as np
import sys

from attacker import Attacker


def main(plaintexts, traces):
    cpa_attacker = Attacker(plaintexts)
    skey = cpa_attacker.obtain_full_private_key(traces, only_first_byte=True)

    # Our AES key:
    # {166, 40, 136, 9, 43, 171, 174, 207, 79, 210, 21, 22, 247, 60, 126}

    print(f"First found subkey: {skey[0]}")
    # print(f"Found full key: {skey}")


if __name__ == '__main__':
    args = sys.argv
    if len(sys.argv) < 3:
        print("Usage: python3 run_cpa.py plaintexts_input traces_input npy_traces_bool")

    # Our ptexts should be stored in ./../data/1000_ptext.npy
    plaintexts_file = sys.argv[1]
    raw_traces_file = sys.argv[2]
    used_npy_traces = sys.argv[3]

    # If we used npy files for traces and ptexts, call the attacker right away
    if used_npy_traces:
        ptexts = np.load(plaintexts_file)
        traces = np.load(traces)
        ptexts = ptexts[:len(traces)]

        main(ptexts, traces)
        return

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