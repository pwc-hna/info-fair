import serial           # import the module
import time

ComPort = serial.Serial('\\.\COM6') # open COM24
ComPort.baudrate = 9600 # set Baud rate to 9600
ComPort.bytesize = 8    # Number of data bits = 8
ComPort.parity   = 'N'  # No parity
ComPort.stopbits = 1    # Number of Stop bits = 1
# Write character 'A' to serial port
#data = bytearray(b'Arne Horia\n')
stringh = 'TFNNNNNN\n'
data = bytearray(stringh)
time.sleep(5)
#ComPort.close()
#ComPort.open()
ComPort.flush()
while True:
	No = ComPort.write(data)
	#No = ComPort.writeline('arne horia \n')
	time.sleep(1)
	data2 = ComPort.readline()        # Wait and read data
	print(data2)                      # print the received data
	# ComPort.close()         # Close the Com port