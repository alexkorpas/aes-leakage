import time
import serial


class Arduino:
    SERIAL_RATE = 9600
    ARDUINO_PORT = "COM14"
    INIT_MSG = b"r"
    PULSE_MSG = b"e"

    def __init__(self, port=ARDUINO_PORT):
        self.ser = serial.Serial(port, self.SERIAL_RATE)

    def send(self, msg):
        self.ser.write(msg)

    def init(self):
        print("Resetting Arduino.")
        self.send(self.INIT_MSG)
        time.sleep(1.000)
        print("Arduino is ready to go!")

    def pulse(self):
        self.send(self.PULSE_MSG)

    def send_msg(self, msg='deadbeefdeadbeef'):
        self.send(bytes(f'{msg}\n', 'utf-8'))
        time.sleep(1)

    def close(self):
        self.ser.close()

    def test_loop(self):
        while True:
            try:
                # self.init()
                self.send_msg()
                # self.pulse()
                # time.sleep(1)
                # self.pulse()
                # time.sleep(1)
            except KeyboardInterrupt:
                self.close()
                continue


if __name__ == '__main__':
    a = Arduino()
    a.test_loop()
