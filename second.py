import serial
ser = serial.Serial('/dev/ttyUSB0', 9600)
while True:
    ser.reset_input_buffer()
    print(ser.readline().decode())