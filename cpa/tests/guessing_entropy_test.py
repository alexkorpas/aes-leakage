import unittest  # Run tests from this folder's parent directory

import numpy as np

from attacker import Attacker
from attack_analyser import AttackAnalyser
from helpers import *


class GuessingEntropyTest(unittest.TestCase):
    TEST_DATA_LOC = "./../test_data/"

    def test_guessing_entropy_calc(self):
        subkey_corr_coeffs = {}
        pass


if __name__ == '__main__':
    unittest.main()
