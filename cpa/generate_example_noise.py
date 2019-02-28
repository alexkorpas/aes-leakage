import os
import random

import pandas as pd
import numpy as np


def files_in_dir(dir_name):
    """
    Returns the amount of files in a directory.

    :rtype: int the amount of files in a directory.
    """
    return len(os.listdir(dir_name))


def next_filename(dir_name, name_prefix, name_suffix):
    return dir_name + name_prefix + str(files_in_dir(dir_name)) + name_suffix


def generate_examples(dir_name, samples, datapoints, amount_noise=.5):
    for _ in range(samples):
        wave = np.sin(2 * np.pi * (np.arange(datapoints) / datapoints))
        noise = np.random.rand(datapoints) * amount_noise

        res = wave + noise
        df = pd.DataFrame(res)
        df.to_csv(next_filename(dir_name, 'example_sin_', '.csv'), index=False)


if __name__ == "__main__":
    generate_examples('data/example_noise/', 10, 500)
