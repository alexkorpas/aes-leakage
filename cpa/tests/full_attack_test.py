import unittest  # Run tests from this folder's parent directory

import numpy as np

from attacker import Attacker
from helpers import *


class FullAttackTest(unittest.TestCase):
    TEST_DATA_LOC = "./../test_data/"

    def test_obtain_full_private_key(self):
        # Import power traces for which we know the used key.
        key = np.load(self.TEST_DATA_LOC + "key.npy")
        power_samples = np.load(self.TEST_DATA_LOC + "traces.npy")[:-1]
        plaintexts = np.load(self.TEST_DATA_LOC + "plain.npy")

        # Set up the attacker. Plaintext format conversion is handled there.
        attacker = Attacker(plaintexts)
        computed_key_bits = attacker.obtain_full_private_key(power_samples)

        # Convert the known skey so it can be compared to our output.
        known_key_bits = bytes_to_bits(key)

        self.assertEqual(known_key_bits, known_key_bits)


if __name__ == '__main__':
    unittest.main()
