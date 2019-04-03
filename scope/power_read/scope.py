import struct
import time
from datetime import datetime
from os import mkdir
from statistics import stdev

from pyvisa import Resource
from tqdm import tqdm

from arduino.arduino import Arduino
from power_read import visa_tools
from power_read.visa_tools import file_open_append, num_folders

CH_MATH = "MATH"
PULSE_DURATION = 100  # ms.
DEFAULT_DATA_ROOT = "../data/"


class Scope:
    PREFERRED_USB = "USB0::0x0699::0x0369::C103071::INSTR"
    MAX_SAMPLE_SIZE = 2500
    ARDUINO_TIMEOUT = 10

    def __init__(self, data_root=DEFAULT_DATA_ROOT):
        self.sample_size = self.MAX_SAMPLE_SIZE
        date = str(datetime.fromtimestamp(time.time())).split(' ')[0]
        self.data_dir = f"{data_root}{date}_{num_folders(data_root)}"
        self.file_raw = self.file_trace = None

        if self.data_dir is None:
            print("Data dir not specified, not saving traces!")

        self.scope: Resource = self.get_resource()
        self.scope.write(f':DATA:RECORDLENGTH {self.sample_size}')
        self.scope.write(f':DATA:STOP {self.sample_size}')

        self.scope.write(f':DATA:STOP {self.sample_size}')

        self.scope.write('ACQUIRE:MODE SAMPLE')
        self.scope.write('ACQ:STATE RUN')

        print("Scope set up.")

        self.arduino = self.get_arduino()

    @staticmethod
    def get_arduino():
        return Arduino()

    def get_traces(self, num_traces=1):
        self.arduino.init()

        self.open_files(num_traces)
        for i in range(num_traces):
            self.arduino.pulse()
            timeout_start = time.time()

            print("Sending pulse, waiting for trigger...")
            while not self.trigger_active():
                if (time.time() - timeout_start) > self.ARDUINO_TIMEOUT:
                    print("Timeout! Terminating...")
                    return
                continue

            print("Triggered!")
            prev_acquisitions = self.get_num_acquisitions()
            curr_acquisitions = self.get_num_acquisitions()

            while curr_acquisitions == prev_acquisitions:
                curr_acquisitions = self.get_num_acquisitions()

            print(f"Capturing trace_100 ({i+1}/{num_traces}), acq = {curr_acquisitions}.")
            self.write_trace(True)

        self.close_files()

    def get_resource(self) -> Resource:
        return visa_tools.get_resource(self.PREFERRED_USB)

    def read_channel(self, channel=CH_MATH):
        return self.read_unit_data(channel, self.read_raw(channel))

    def trigger_active(self):
        return self.scope.query('TRIGGER:STATE?') != 'READY\n'

    def read_raw(self, channel):
        self.scope.write(f":DATa:SOUrce {channel}")
        self.scope.write("CURV?")
        raw_read = self.scope.read_raw()
        return raw_read

    def read_setting(self, channel, prop):
        # noinspection PyUnresolvedReferences
        raw_value = self.scope.query(f":{channel}:{prop}?").rstrip()
        return raw_value

    def read_unit_data(self, channel, raw_data):
        raw_data = raw_data.split(b"42500", 1)[1]
        raw_data = raw_data[:-len(b'\r\n')]

        return struct.unpack(('B' * len(raw_data)), raw_data)

    def print_values(self):
        chm = self.read_channel(CH_MATH)

        print(len(chm))

        values = chm

        for entries in values:
            print([int(e) for e in entries])

        ch1 = self.read_channel()

        print()
        print(f"Length of trace_100: {len(ch1)}.")
        print(f"StDev of trace_100: {stdev(ch1)}.")

    def write_trace(self, write_raw=False):
        raw = self.read_raw(CH_MATH)
        trace = self.read_unit_data(CH_MATH, raw)

        if self.data_dir:
            self.file_trace.write(str(trace) + '\n')

            if write_raw:
                self.file_raw.write(str(raw) + '\n')

    def get_num_acquisitions(self):
        return int(self.scope.query('ACQUIRE:NUMACQ?').split(' ')[1])

    def open_files(self, num_traces):
        if self.data_dir is not None:
            mkdir(self.data_dir)

            self.file_raw = file_open_append(self.data_dir, f"raw_{num_traces}")
            self.file_trace = file_open_append(self.data_dir, f"trace_{num_traces}")

    def close_files(self):
        if self.data_dir is not None:
            self.file_raw.close()
            self.file_trace.close()


if __name__ == '__main__':
    scope = Scope()
    scope.get_traces()
