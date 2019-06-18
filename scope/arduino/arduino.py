import os
import random
import string
import time

import pyperclip as pyperclip
import serial


class Arduino:
    SERIAL_RATE = 9600
    ARDUINO_PORT = "COM5"
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

    def send_on_file_change(self, folder="../traces", traces=100):
        for _ in range(traces):
            # Get files for file watcher
            before = get_files(folder)

            # Get the random plaintext message
            plaintext = ''.join(random.choice(string.ascii_lowercase) for _ in range(16))
            print(f"Sending plaintext '{plaintext}' to arduino...")
            self.send_msg(plaintext)

            print(f"Waiting for oscilloscope...")
            # Copy the unnamed file to the clipboard for the mouse macro.
            # Randomness is added to not disturb the mouse macro in the process.
            pyperclip.copy("unnamed_" + ''.join(random.choice(string.ascii_lowercase) for _ in range(8)))

            # Check for file changes
            found_file = False
            while not found_file:
                # Check 2 times per second.
                time.sleep(.5)
                after = get_files(folder)

                # For every new or changed filename
                for f in [f for f in after if f not in before]:
                    print(f"Found new file '{f}', assuming it is for '{plaintext}'.")

                    # In case the oscilloscope is still writing data (takes a long time...)
                    exception = True
                    while exception:
                        try:
                            os.rename(f"{folder}/{f}", f"{folder}/{plaintext}.csv")
                            exception = False
                        except PermissionError:
                            time.sleep(.1)

                    found_file = True


def get_files(folder):
    return dict([(f, None) for f in os.listdir(folder)])


if __name__ == '__main__':
    a = Arduino()
    # a.test_loop()
    a.send_on_file_change()
