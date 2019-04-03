import numpy as np


class AttackAnalyser:
    def __init__(self):
        pass

    def compute_guessing_entropy(self, known_key, subkey_corr_coeffs):
        """Computes the guessing entropy for a fully computed key of 16 bytes
        by computing the average of each subkey's guessing entropy.

        Arguments:
            known_key {[int]} -- The full, actual secret key as a list of ints.
            subkey_corr_coeffs { {{}} } -- A dictionary that contains a nested
            dictionary for each of the 16 subkeys. Each of these nested dicts
            contains the computed absolute correlation coefficient for each
            subkey guess that was computed in the attack on the subkey.

        Returns:
            float -- The average guessing entropy of all subkeys.
        """
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
        """Computes the guessing entropy for one subkey (known as the partial
        guessing entropy) by sorting the computed subkey guess correlations and
        finding the index at which the correct subkey is found.

        Arguments:
            known_subkey {int} -- The known subkey as an integer 0 <= i <= 255.
            subkey_guess_corr_coeffs { {} } -- A dictionary that contains the
            absolute computed Pearson correlation coefficient for each subkey
            guess that was made in the attack.

        Returns:
            int -- The guessing entropy for the given subkey to which the
            given correlation coefficients belong.
        """
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
        """Find the index of the tuple element that contains the given int key.

        Arguments:
            int_key {int} -- The integer of which we want to find the tuple
            containing it.
            pairs {[()]} -- A list of tuples of which the first element is an
            integer.

        Raises:
            ValueError -- This error is raised when the given int key is not
            present in the given pair array.

        Returns:
            int -- The index at which the given int key's tuple is present.
        """
        for i in range(len(pairs)):
            pair = pairs[i]
            if pair[0] == int_key:
                return i

        raise ValueError(f"Key {int_key} was not found in the list of pairs.")
