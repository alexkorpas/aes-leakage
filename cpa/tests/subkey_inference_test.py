import unittest

from attacker import Attacker


class MockAttacker(Attacker):
    def pearson_correlation_coeff(self, actual_consumptions,
                                  modeled_consumptions):
        # TODO
        pass


class SubKeyInferenceTest(unittest.TestCase):
    def test_bruh(self):
        self.assertEqual(0, 1)


if __name__ == '__main__':
    unittest.main()
