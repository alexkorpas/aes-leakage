import time
import serial


class Arduino:
    SERIAL_RATE = 9600
    PULSE_ARDUINO = "COM5"
    INIT_MSG = b"i"
    PULSE_MSG = b"p"

    def __init__(self, port=PULSE_ARDUINO):
        self.ser = serial.Serial(port, self.SERIAL_RATE)

    def send(self, msg):
        self.ser.write(msg)

    def init(self):
        print("Resetting Arduino.")
        self.send(self.INIT_MSG)
        time.sleep(3.000)
        print("Arduino is ready to go!")

    def pulse(self):
        self.send(self.PULSE_MSG)
        time.sleep(0.100)

    def close(self):
        self.ser.close()

    def test_loop(self):
        while True:
            try:
                # self.init()
                self.pulse()
                time.sleep(1)
                self.pulse()
                time.sleep(1)
                self.pulse()
                time.sleep(1)
            except KeyboardInterrupt:
                self.close()
                continue


if __name__ == '__main__':
    a = Arduino()
    a.test_loop()
