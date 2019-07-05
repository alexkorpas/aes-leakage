import unittest

from power_read.scope import Scope


class SDSTest(unittest.TestCase):
    def test_run(self):
        # noinspection PyUnusedLocal
        scope = Scope()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
