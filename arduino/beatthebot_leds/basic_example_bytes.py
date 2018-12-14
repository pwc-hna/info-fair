import serial
import time
import struct

#The following line is for serial over GPIO
port = 'COM6' # note I'm using Mac OS-X


ard = serial.Serial(port,115200,timeout=5)
time.sleep(5) # wait for Arduino

i = 0

messages=["FNNNNNNN","TNNNNNNN", "TTNNNNNN", "TTTNNNNN", "TTTTNNNN", "TTTTTNNN", "TTTTTTNN","TTTTTTTN", "TTTTTTTF"]
sampleMessage="TTFFFTFN"
def convert_str_to_byte(message):
    byte_arr = []
    # message = message.replace('N','1')
    # message = message.replace('T','2')
    # message = message.replace('F','3')
    print "message = "+message
    for c in message:
        if c == 'N':
            byte_arr.append(1)
        if c == 'T':
            byte_arr.append(2)
        if c == 'F':
            byte_arr.append(3)
        
    byte_arr.append(0)
    return byte_arr


while (i < len(messages)):
    # Serial write section

    # ard.flush()

    # mArr = [2,3,2,1,1,1,1,1,0]
    mArr = convert_str_to_byte(messages[i])
    numelements = len(mArr)
    print ("Python value sent: "+str(struct.pack('b'*numelements,*mArr)))
    ard.write(struct.pack('b'*numelements,*mArr))
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
