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

        # Set up the attacker and find the private key as a list of bytes.
        attacker = Attacker(plaintexts)
        computed_key_bytes = attacker.obtain_full_private_key(power_samples)

        # "key.npy" is stored as an array of identical keys, so get key[0]
        known_key_bytes = key[0]

        self.assertEqual(known_key_bits, computed_key_bits)


if __name__ == '__main__':
    unittest.main()
