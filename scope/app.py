from arduino.arduino import Arduino

if __name__ == '__main__':
    # Set up the arduino and run the acquisition loop.
    #   Usage instructions can be found in '.\readme.md'.

    # Please insert the serial port to which your arduino is connected.
    serial_port = "COM14"

    a = Arduino(serial_port)
    a.run_acquisition_loop()
