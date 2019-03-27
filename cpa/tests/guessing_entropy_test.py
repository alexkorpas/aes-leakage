import unittest  # Run tests from this folder's parent directory

import numpy as np

from attacker import Attacker
from attack_analyser import AttackAnalyser
from helpers import *


class GuessingEntropyTest(unittest.TestCase):
    TEST_DATA_LOC = "./../test_data/"

    def test_subkey_guessing_entropy_calc(self):
        analyser = AttackAnalyser()

        known_key_byte = 77

        # Create arbitrary subkey guess correlation coefficients.
        # Our third best guess will correspond to the known key byte, which
        # should result in a guessing entropy of 2.
        guess_coeffs = {}
        guess_coeffs[0] = 0.1
        guess_coeffs[64] = 0.94
        guess_coeffs[77] = 0.95
        guess_coeffs[123] = 0.731683
        guess_coeffs[243] = 0.99
        guess_coeffs[255] = 1.00

        entropy = analyser.compute_subkey_guessing_entropy(77, guess_coeffs)

        self.assertEqual(entropy, 2)

    def test_full_guessing_entropy_calc(self):
        known_key = [43, 126, 21, 22, 40, 174, 210, 166, 171, 247, 21, 136, 9,
                     207, 79, 60]

        subkey_corr_coeffs = {}
        # For each subkey, manually create the guessing entropy coeffs to test
        for subkey_i in range(16):
            subkey_corr_coeffs[subkey_i] = {}

        # Set some arbitrary coefficients for several guessed subkeys, which
        # should include the known subkey byte. The coefficients are abs vals.
        subkey_corr_coeffs[0][2] = 0.44
        subkey_corr_coeffs[0][43] = 0.9
        subkey_corr_coeffs[0][127] = 0.1

        subkey_corr_coeffs[1][126] = 1.00
        subkey_corr_coeffs[1][0] = 0.00
        subkey_corr_coeffs[1][0] = 0.00

        subkey_corr_coeffs[2][0] = 0.00
        subkey_corr_coeffs[2][0] = 0.00
        subkey_corr_coeffs[2][0] = 0.00

        subkey_corr_coeffs[3][0] = 0.00
        subkey_corr_coeffs[3][0] = 0.00
        subkey_corr_coeffs[3][0] = 0.00

        subkey_corr_coeffs[4][0] = 0.00
        subkey_corr_coeffs[4][0] = 0.00
        subkey_corr_coeffs[4][0] = 0.00

        subkey_corr_coeffs[5][0] = 0.00
        subkey_corr_coeffs[5][0] = 0.00
        subkey_corr_coeffs[5][0] = 0.00

        subkey_corr_coeffs[6][0] = 0.00
        subkey_corr_coeffs[6][0] = 0.00
        subkey_corr_coeffs[6][0] = 0.00

        subkey_corr_coeffs[7][0] = 0.00
        subkey_corr_coeffs[7][0] = 0.00
        subkey_corr_coeffs[7][0] = 0.00

        subkey_corr_coeffs[8][0] = 0.00
        subkey_corr_coeffs[8][0] = 0.00
        subkey_corr_coeffs[8][0] = 0.00

        subkey_corr_coeffs[9][0] = 0.00
        subkey_corr_coeffs[9][0] = 0.00
        subkey_corr_coeffs[9][0] = 0.00

        subkey_corr_coeffs[10][0] = 0.00
        subkey_corr_coeffs[10][0] = 0.00
        subkey_corr_coeffs[10][0] = 0.00

        subkey_corr_coeffs[11][0] = 0.00
        subkey_corr_coeffs[11][0] = 0.00
        subkey_corr_coeffs[11][0] = 0.00

        subkey_corr_coeffs[12][0] = 0.00
        subkey_corr_coeffs[12][0] = 0.00
        subkey_corr_coeffs[12][0] = 0.00

        subkey_corr_coeffs[13][0] = 0.00
        subkey_corr_coeffs[13][0] = 0.00
        subkey_corr_coeffs[13][0] = 0.00

        subkey_corr_coeffs[14][0] = 0.00
        subkey_corr_coeffs[14][0] = 0.00
        subkey_corr_coeffs[14][0] = 0.00

        subkey_corr_coeffs[15][0] = 0.00
        subkey_corr_coeffs[15][0] = 0.00
        subkey_corr_coeffs[15][0] = 0.00


if __name__ == '__main__':
    unittest.main()
