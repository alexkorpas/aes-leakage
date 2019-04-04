import sys

from attacker import Attacker


def main(plaintexts, traces):    
    cpa_attacker = Attacker(plaintexts)
    skey = cpa_attacker.obtain_full_private_key(traces)

    print(f"Found the follow secret key:\n{skey}")


if __name__ == '__main__':
    args = sys.argv
    if len(sys.argv) < 3:
        print("Usage: python3 run_cpa.py plaintexts_input traces_input")

    plaintexts = sys.argv[1]
    raw_traces = sys.argv[2]

    # Convert traces
    traces = []
    for line in file: 
        points = line.strip("\n").strip("(").strip(")").split(",")
        trace = [int(point) for point in points]
        traces.append(trace)

    main(plaintexts, traces)
