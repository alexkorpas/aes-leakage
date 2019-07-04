import glob
import re
import numpy as np
from tqdm import tqdm

es_folder = "../data/traces"
trace_length = 20480
files = [f for f in glob.glob(f"{es_folder}/*.csv") if not re.search('(unnamed_.*)', f)]
num_files = len(files)

traces = np.empty((num_files, trace_length))
plaintexts = [""] * num_files

for i in tqdm(range(num_files)):
    reading = False
    trace = np.zeros(trace_length)
    filename = files[i]

    j = 0
    with open(filename, 'r') as file:
        for line in file:
            if not reading:
                reading = re.search('ch1_time\(s\),ch1_value\(V\),ch2_time\(s\),ch2_value\(V\)', line)
                continue

            e = line.rstrip().split(',')

            ch1 = float(e[1])
            ch2 = float(e[3])

            trace[j] = ch1 - ch2
            j += 1

    traces[i] = np.array(trace)
    plaintext = re.match('.*\\\(.*)\.csv', filename).group(1)
    plaintexts[i] = plaintext
    i += 1

plaintexts = np.array(plaintexts)

np.save('traces.npy', traces)
np.save('plaintexts.npy', plaintexts)
