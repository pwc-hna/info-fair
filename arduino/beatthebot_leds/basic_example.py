import serial
import time

#The following line is for serial over GPIO
port = 'COM6' # note I'm using Mac OS-X


ard = serial.Serial(port,9600,timeout=5)
time.sleep(5) # wait for Arduino

i = 0

while (i < 1):
    # Serial write section

    ard.flush()
    mStr = 'FTTFTFTT\n'
    print ("Python value sent: "+mStr)
    ard.write(mStr)
    while(ard.in_waiting == 0):
        pass
    time.sleep(0.1) # I shortened this to match the new value in your Arduino code

    # Serial read section
    msg = ard.read(ard.inWaiting()) # read all characters in buffer
    print ("Message from arduino: ")
    print (msg)
    i = i + 1
else:
    print "Exiting"
exit()
