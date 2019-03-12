import unittest  # Run tests from this folder's parent directory

import numpy as np

from attacker import Attacker


class MockAttacker(Attacker):
    pass


class FullAttackTest(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
