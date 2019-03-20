import numpy as np


class AttackAnalyser:
    def __init__(self):
        pass

    def compute_guessing_entropy(self, known_key, subkey_corr_coeffs):
        partial_guessing_entropies = []
        for (subkey_index, subkey_guess_corr_coeffs) in subkey_corr_coeffs:
            known_subkey = known_key[subkey_index]
            pge = self.compute_subkey_guessing_entropy(
                known_subkey,
                subkey_guess_corr_coeffs
            )

            partial_guessing_entropies.append(pge)

        return np.mean(partial_guessing_entropies)

    def compute_subkey_guessing_entropy(self, known_subkey,
                                        subkey_guess_corr_coeffs):
        # Sort the keys descendingly by absolute correlation. This actually
        # produced a list of (k, v) pairs instead of a dictionary.
        sorted_coeffs = [
            (key, subkey_guess_corr_coeffs[key])
            for key
            in sorted(subkey_guess_corr_coeffs,
                      key=subkey_guess_corr_coeffs.get,
                      reverse=True)
        ]

        partial_guessing_entropy = \
            self.get_int_key_index_from_kv_pairs(known_subkey, sorted_coeffs)
        return partial_guessing_entropy

    def get_int_key_index_from_kv_pairs(self, int_key, pairs):
        for i in range(len(pairs)):
            pair = pairs[i]
            if pair[0] == int_key:
                return i

        raise ValueError(f"Key {int_key} was not found in the list of pairs.")
