import unittest

from attacker import Attacker


class MockAttacker(Attacker):
    def pearson_correlation_coeff(self, actual_consumptions, modeled_consumptions):
        # TODO
        pass


class SimpleCorrelationTest(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
