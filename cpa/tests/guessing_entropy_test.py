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
        guess_coeffs[7] = 0.0
        guess_coeffs[64] = 0.94
        guess_coeffs[77] = 0.95
        guess_coeffs[123] = 0.731683
        guess_coeffs[243] = 0.99
        guess_coeffs[255] = 1.00

        entropy = analyser.compute_subkey_guessing_entropy(77, guess_coeffs)

        self.assertEqual(entropy, 2)

    def test_full_guessing_entropy_calc(self):
        analyser = AttackAnalyser()

        known_key = [43, 126, 21, 22, 40, 174, 210, 166, 171, 247, 21, 136, 9,
                     207, 79, 60]

        subkey_coeffs = {}
        # For each subkey, manually create the guessing entropy coeffs to test
        for subkey_i in range(16):
            subkey_coeffs[subkey_i] = {}

        # Set some arbitrary coefficients for several guessed subkeys, which
        # should include the known subkey byte. The coefficients are abs vals.

        # PGE = 0
        subkey_coeffs[0][43] = 0.9
        subkey_coeffs[0][2] = 0.44
        subkey_coeffs[0][127] = 0.1
        pge1 = analyser.compute_subkey_guessing_entropy(43, subkey_coeffs[0])
        self.assertEqual(pge1, 0)

        # PGE = 0
        subkey_coeffs[1][126] = 1.00
        subkey_coeffs[1][12] = 0.00
        subkey_coeffs[1][253] = 0.00
        pge2 = analyser.compute_subkey_guessing_entropy(126, subkey_coeffs[1])
        self.assertEqual(pge2, 0)

        # PGE = 1
        subkey_coeffs[2][21] = 0.1
        subkey_coeffs[2][0] = 0.03
        subkey_coeffs[2][12] = 0.15
        pge3 = analyser.compute_subkey_guessing_entropy(21, subkey_coeffs[2])
        self.assertEqual(pge3, 1)

        # PGE = 2
        subkey_coeffs[3][22] = 0.05
        subkey_coeffs[3][20] = 0.4
        subkey_coeffs[3][40] = 0.06
        pge4 = analyser.compute_subkey_guessing_entropy(22, subkey_coeffs[3])
        self.assertEqual(pge4, 2)

        # PGE = 0
        subkey_coeffs[4][40] = 0.9
        subkey_coeffs[4][0] = 0.4
        subkey_coeffs[4][0] = 0.1
        pge5 = analyser.compute_subkey_guessing_entropy(40, subkey_coeffs[4])
        self.assertEqual(pge5, 0)

        # PGE = 0
        subkey_coeffs[5][174] = 1.00
        subkey_coeffs[5][210] = 0.5
        subkey_coeffs[5][0] = 0.75
        pge6 = analyser.compute_subkey_guessing_entropy(174, subkey_coeffs[5])
        self.assertEqual(pge6, 0)

        # PGE = 0
        subkey_coeffs[6][210] = 1.00
        subkey_coeffs[6][3] = 0.00
        subkey_coeffs[6][0] = 0.00
        pge7 = analyser.compute_subkey_guessing_entropy(210, subkey_coeffs[6])

        # PGE = 1
        subkey_coeffs[7][166] = 0.4
        subkey_coeffs[7][0] = 0.2
        subkey_coeffs[7][100] = 0.8
        pge8 = analyser.compute_subkey_guessing_entropy(166, subkey_coeffs[7])

        # PGE = 0
        subkey_coeffs[8][171] = 0.5
        subkey_coeffs[8][0] = 0.00
        subkey_coeffs[8][100] = 0.00
        pge9 = analyser.compute_subkey_guessing_entropy(171, subkey_coeffs[8])

        # PGE = 0
        subkey_coeffs[9][247] = 1.00
        subkey_coeffs[9][0] = 0.00
        subkey_coeffs[9][255] = 0.5
        pge10 = analyser.compute_subkey_guessing_entropy(247, subkey_coeffs[9])

        # PGE = 1
        subkey_coeffs[10][21] = 0.7
        subkey_coeffs[10][136] = 0.8
        subkey_coeffs[10][2] = 0.5
        pge11 = analyser.compute_subkey_guessing_entropy(21, subkey_coeffs[10])

        # PGE = 1
        subkey_coeffs[11][136] = 0.9
        subkey_coeffs[11][0] = 0.95
        subkey_coeffs[11][100] = 0.00
        pge12 = analyser.compute_subkey_guessing_entropy(136, subkey_coeffs[11])

        # PGE = 0
        subkey_coeffs[12][9] = 0.872323
        subkey_coeffs[12][0] = 0.00
        subkey_coeffs[12][100] = 0.05
        pge13 = analyser.compute_subkey_guessing_entropy(9, subkey_coeffs[12])

        # PGE = 2
        subkey_coeffs[13][207] = 0.213144
        subkey_coeffs[13][0] = 0.5
        subkey_coeffs[13][100] = 0.3
        pge14 = analyser.compute_subkey_guessing_entropy(207, subkey_coeffs[13])

        # PGE = 0
        subkey_coeffs[14][79] = 1.00
        subkey_coeffs[14][80] = 0.5
        subkey_coeffs[14][81] = 0.25
        pge15 = analyser.compute_subkey_guessing_entropy(79, subkey_coeffs[14])

        # PGE = 1
        subkey_coeffs[15][60] = 0.85
        subkey_coeffs[15][0] = 0.9
        subkey_coeffs[15][254] = 0.05
        pge16 = analyser.compute_subkey_guessing_entropy(60, subkey_coeffs[15])

        # Compute the full guessing entropy
        entropy = analyser.compute_guessing_entropy(
            known_key, subkey_coeffs
        )

        expected_aggregate_entropy = \
            0 + 0 + 1 + 2 + 0 + 0 + 0 + 1 + 0 + 0 + 1 + 1 + 0 + 2 + 0 + 1
        expected_avg_entropy = expected_aggregate_entropy/16

        self.assertEqual(entropy, expected_avg_entropy)


if __name__ == '__main__':
    unittest.main()
