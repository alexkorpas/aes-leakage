import numpy as np


def guessing_entropy(key, guess):
    size = len(key)
    pge = [256] * size
    for bnum in range(size):
        pge[bnum] = np.where(guess[bnum] == key[bnum])[0][0]

    return np.mean(pge)


def key_success_rate(known_key, guess):
    return int(known_key == guess)


def subkey_success_rate(known_key, guess):
    size = len(known_key)
    correct = sum([1 for i in range(size) if known_key[i] == guess[i]])

    return correct / size
