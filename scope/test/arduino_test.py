import unittest

from arduino.arduino import Arduino


class ArduinoTest(unittest.TestCase):
    def test_init(self):
        a = Arduino()
        a.run_acquisition_loop()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
