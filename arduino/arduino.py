import time

# Install pyserial.
import serial


class Arduino:
    PC_PORT = "COM14"
    BIT_RATE = 9600

    def __init__(self, port):
        self.serial = serial.Serial(port, Arduino.BIT_RATE)

        ready = False
        time_start = time.time()
        while not ready:
            if self.serial.in_waiting > 0:
                self.serial.readline()
                break

            if time.time() - time_start >= 5:
                raise Exception('Arduino connection timeout after 5 seconds...')

    def write(self, msg):
        self.serial.write(bytearray('[' + msg + ']', 'utf-8'))

    def read(self):
        return self.serial.readline()


if __name__ == "__main__":
    a = Arduino(Arduino.PC_PORT)
    a.write("foo")
    print(a.read())
