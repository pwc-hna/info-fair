import serial
import time
import gevent
import sys

#The following line is for serial over GPIO
port = 'COM6' # note I'm using Mac OS-X


ard = serial.Serial(port,9600,timeout=10)
gevent.sleep(2) # wait for Arduino


def arduino_send_message(message):
    try:
        # ard.flush()
        print ("Python value sent: "+message)
        ard.write(message)
        while(ard.in_waiting == 0):
            pass
        gevent.sleep(0.1) # I shortened this to match the new value in your Arduino code

        # Serial read section
        msg = ard.read(ard.inWaiting()) # read all characters in buffer
        print ("Message from arduino: ")
        print (str(msg))
        # gevent.sleep(2)
        return str(msg)
    except IOError:
        return ""

# messages = ['FNNNNNNN\n','TNNNNNNN\n','TFNNNNNN\n','TFFNNNNN\n','TFFTNNNN\n','TFFTFNNN\n','TFFTFTNN\n', 'TFFTFTTT\n']
messages = ['TFFTFTTT\n']
# Serial write section
for message in messages:
    rcv_msg = ""
    if ( message not in rcv_msg):
        rcv_msg = arduino_send_message(message)
        # if ( message not in rcv_msg):
        #     rcv_msg = arduino_send_message(message)

if __name__ == '__main__':
    print ("arg = " + sys.argv[1])
    arduino_send_message(sys.argv[1]+"\n")