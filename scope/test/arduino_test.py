import unittest

from arduino import arduino


class ArduinoTest(unittest.TestCase):
    def test_init(self):
        arduino.init()
        arduino.test_loop()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
