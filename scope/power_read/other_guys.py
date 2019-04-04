import time

import pyvisa


def get_serial(ser, t=1):
    time.sleep(t)
    nbytes = ser.inWaiting()
    if nbytes > 0:
        print(">> "+ '\n>> '.join(ser.read(nbytes).rstrip().split('\n')))

# port = sys.argv[1]
# print('Using port %s for Arduino' % port)
# ser = serial.Serial(port)

rm = pyvisa.ResourceManager()
print(rm.list_resources())

ii = rm.open_resource(rm.list_resources()[0])
ii.write('ACQUIRE:MODE SAMPLE')
ii.write('ACQ:STATE RUN')
ii.write('ACQUIRE:MODE AVERAGE')

ii.write('ACQUIRE:NUMAVG 16')

num_acqs = int(ii.query('ACQUIRE:NUMACQ?').split(' ')[1])

prev_acqs = num_acqs
orig_acqs = num_acqs
curr_acqs = 0

dirname = 'A:\\858\\'+'-'.join(time.strftime("%x").split('/'))+'-'+'-'.join(time.strftime("%X").split(':'))
ii.write('FILESystem:MKDir "'+dirname+'"')

num_traces = 4
n = 0

while n < num_traces:
    while not ii.query('TRIGGER:STATE?') != 'READY\n':
        print("Waiting for trigger...")
        continue

    print("Triggered!")
    prev_acqs = int(ii.query('ACQUIRE:NUMACQ?'))
    curr_acqs = int(ii.query('ACQUIRE:NUMACQ?'))

    while(curr_acqs == prev_acqs):
        curr_acqs = int(ii.query('ACQUIRE:NUMACQ?'))

    print(ii.write(f'SAVe:WAVEform CH1, "mycsv_{n}.csv"'))
    time.sleep(3)
    # get_serial(ser, 2)

# ser.close()
ii.close()
