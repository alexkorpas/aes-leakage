import unittest

import numpy as np

from attacker import Attacker
from helpers import *


class FullAttackTest(unittest.TestCase):

    TEST_DATA_LOC = "./../test_data/"

    def test_obtain_full_private_key(self):
        # Import power traces for which we know the used key.
        keys = np.load(self.TEST_DATA_LOC + "key.npy")
        template_traces = np.load(self.TEST_DATA_LOC + "traces.npy")[:-1]
        template_plaintexts = np.load(self.TEST_DATA_LOC + "plain.npy")

        atk_traces = np.load(self.TEST_DATA_LOC + "traces.npy")[:30]
        atk_plaintexts = np.load(self.TEST_DATA_LOC + "plain.npy")[:30]

        # "key.npy" is stored as an array of identical keys, so get key[0]
        known_key_bytes = np.load(self.TEST_DATA_LOC + "key.npy")[0][:1]
        print(known_key_bytes)

        # Create the templates based on a set of known traces/plaintexts/keys
        # and use them to find the key for another set of traces/plaintexts.
        attacker = Attacker(template_plaintexts, keys)
        attacker.construct_hammweight_templates(template_traces)
        computed_key_bytes = \
            attacker.obtain_full_private_key(atk_traces, atk_plaintexts)

        self.assertEqual(list(known_key_bytes), computed_key_bytes)
