import os
import random
import string
import time

import pyperclip as pyperclip
import serial

import sys
sys.path.append("../")
from easy_scope.mouse_macro import start_macro


class Arduino:
    SERIAL_RATE = 9600
    ARDUINO_PORT = "COM14"
    INIT_MSG = b"r"
    PULSE_MSG = b"e"

    def __init__(self, port=ARDUINO_PORT, write_timeout_sec=10):
        print(f"Opening serial at port: '{port}'.")
        self.port = port
        self.ser = serial.Serial(port=port, baudrate=self.SERIAL_RATE, write_timeout=write_timeout_sec)
        print(f"Setting up arduino...")
        time.sleep(2.500)

    def reset_serial(self):
        print(f"Resetting serial...")
        self.ser.close()
        self.ser = serial.Serial(self.port, baudrate=self.SERIAL_RATE)
        time.sleep(2.500)

    def send(self, msg):
        self.ser.write(msg)

    def init(self):
        print("Resetting Arduino.")
        self.send(self.INIT_MSG)
        time.sleep(5.000)
        print("Arduino is ready to go!")

    def pulse(self):
        self.send(self.PULSE_MSG)

    def send_msg(self, msg, timeout_sec=10):
        try:
            self.send(f"{msg}\n".encode('utf-8'))
            time.sleep(1)
        except TimeoutError:
            print("Timeout for sending message!")
            self.reset_serial()
            print(f"Resending {msg}...")
            self.send_msg(msg, timeout_sec)

    def close(self):
        self.ser.close()

    def send_on_file_change(self, dir_name="../data/traces", num_traces=1000):
        print(f"Waiting for dummy file to be created in '{dir_name}'...")
        dummy_file = hold_for_file_changes(dir_name)
        for file in dummy_file:
            os.remove(f"{dir_name}/{file}")

        for i in range(num_traces):
            # Get the random plaintext message
            plaintext = ''.join(random.choice(string.ascii_lowercase) for _ in range(16))
            print(f"Sending plaintext '{plaintext}' to arduino ({i}/{num_traces})...")
            self.send_msg(plaintext, 10)

            # Copy the unnamed file to the clipboard for the mouse macro.
            # Randomness is added to not disturb the mouse macro in the process.
            pyperclip.copy("unnamed_" + ''.join(random.choice(string.ascii_lowercase) for _ in range(8)))

            start_macro()
            print(f"\tWaiting for oscilloscope...")
            try:
                changed_files = hold_for_file_changes(dir_name, 6000)
            except TimeoutError:
                print("Timeout for oscilloscope, stopping trace process loop.")
                break

            # For every new or changed filename
            for f in changed_files:
                print(f"\tFound new file '{f}', assuming it is for '{plaintext}'.")

                # In case the oscilloscope is still writing data
                exception = True
                while exception:
                    print("\tOscilloscope is still writing file, waiting...")

                    try:
                        os.rename(f"{dir_name}/{f}", f"{dir_name}/{plaintext}.csv")
                        exception = False
                    except PermissionError:
                        time.sleep(.5)
            
            
def get_files(folder):
    return dict([(f, None) for f in os.listdir(folder)])


def hold_for_file_changes(dir_name, timeout=0):
    before = get_files(dir_name)
    found_file = False
    changed_files = []
    time_start = time.time()

    while not found_file:
        # Check 2 times per second.
        time.sleep(.5)
        after = get_files(dir_name)

        changed_files = [f for f in after if f not in before]
        found_file = len(changed_files) > 0

        if 0 < timeout < time.time() - time_start:
            raise TimeoutError()

    return changed_files


if __name__ == '__main__':
    a = Arduino()
    # a.test_loop()
    a.send_on_file_change()
