import struct
import time
from datetime import datetime
from os import mkdir
from statistics import stdev

from pyvisa import Resource

from arduino.arduino import Arduino
from power_read import visa_tools
from power_read.visa_tools import file_open_append, num_folders

CH_1 = "CH1"
CH_2 = "CH2"
CH_MATH = "MATH"
DEFAULT_CHANNELS = [CH_2]

PULSE_DURATION = 100  # ms.
DEFAULT_DATA_ROOT = "../data/output/"


def read_unit_data(raw_data):
    raw_data = raw_data.split(b"42500", 1)[1]

    raw_data = raw_data[:-len(b'\r\n')]

    return struct.unpack(('B' * len(raw_data)), raw_data)


class Scope:
    PREFERRED_USB = "USB0::0x0699::0x0369::C103083::INSTR"
    MAX_SAMPLE_SIZE = 2500
    ARDUINO_TIMEOUT = 10

    def __init__(self, data_root=DEFAULT_DATA_ROOT, record_channels=None):
        self.sample_size = self.MAX_SAMPLE_SIZE
        date = str(datetime.fromtimestamp(time.time())).split(' ')[0]
        self.data_dir = f"{data_root}{date}_{num_folders(data_root)}"

        self.trace_files = {}
        if record_channels is None:
            self.record_channels = DEFAULT_CHANNELS
        else:
            self.record_channels = record_channels

        if len(self.record_channels) <= 0:
            print("Record channels not specified, not saving traces!")

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

    def get_traces(self, num_traces):
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
            curr_acquisitions = self.get_num_acquisitions()

            print(f"Capturing trace_100 ({i+1}/{num_traces}), acq = {curr_acquisitions}.")
            self.write_trace()

        self.close_files()

    def get_resource(self) -> Resource:
        return visa_tools.get_resource(self.PREFERRED_USB)

    def read_channel(self, channel=CH_MATH):
        return read_unit_data(self.read_raw(channel))

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

    def print_values(self):
        chm = self.read_channel(CH_MATH)

        print(len(chm))

        values = chm

        for entries in values:
            print([int(e) for e in entries])

        ch1 = self.read_channel()

        print()
        print(f"Length of trace: {len(ch1)}.")
        print(f"StDev of trace: {stdev(ch1)}.")

    def write_trace(self):
        for channel in self.trace_files:
            trace = read_unit_data(self.read_raw(channel))
            self.trace_files[channel].write(str(trace) + '\n')

    def get_num_acquisitions(self):
        raw_acq = self.scope.query('ACQUIRE:NUMACQ?').split(' ')

        if len(raw_acq) > 1:
            res = int(self.scope.query('ACQUIRE:NUMACQ?').split(' ')[1])
        else:
            res = int(self.scope.query('ACQUIRE:NUMACQ?').split(' ')[0])

        return res

    def open_files(self, num_traces):
        if self.data_dir is not None:
            mkdir(self.data_dir)

            self.trace_files = {}
            for channel in self.record_channels:
                channel_low = channel.lower()
                self.trace_files[channel] = file_open_append(self.data_dir, f"trace_{channel_low}_{num_traces}")

    def close_files(self):
        for channel in self.trace_files:
            self.trace_files[channel].close()

        self.trace_files = {}

    def close(self):
        self.scope.close()


if __name__ == '__main__':
    scope = Scope()
    scope.get_traces(10)
