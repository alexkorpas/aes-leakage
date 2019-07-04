from arduino.arduino import Arduino

if __name__ == '__main__':
    # Set up the arduino and run the aquisition loop. For usage ins
    a = Arduino()
    a.run_acquisition_loop()
