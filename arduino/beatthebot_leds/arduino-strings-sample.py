import serial
import time
import gevent
global game_status
game_status = "FNNNNNNN"
ser = None
try:
    ser = serial.Serial('COM6', 9600)
    print("before sleep")
    #gevent.sleep(10)
    print("after sleep")
except Exception as e:
    print (str(e))

def arduino_send_message(message):
    global game_status
    print("arduino send message = "+message)

    try:
        print("write array: "+message)
        ser.write(bytearray(message+"\n"))
        time.sleep(1)
        recv = ser.readline()
        print(recv)
    except Exception as e:
        print(str(e))

def arduino_send_player_submit_name_game_message():
    global game_status
    message = "TNNNNNNN"
    game_status = message
    arduino_send_message(message)

def arduino_send_start_game_message():
    global game_status
    arduino_send_message(game_status)

def arduino_send_end_game_message():
    global game_status
    messageList = list(game_status)
    messageList[0] = 'F'
    message = ''.join(messageList)
    game_status = message
    arduino_send_message(message)

def arduino_send_progress_message(isGameStarted, current_doc_index, isCorrect):
    global game_status
    messageList = list(game_status)
    messageList[0] = 'T' if isGameStarted else 'F'
    messageList[current_doc_index + 1] = 'T' if isCorrect else 'F'
    message = ''.join(messageList)
    game_status = message
    arduino_send_message(message)


if __name__ == '__main__':
    print("initial status = "+game_status)
    arduino_send_start_game_message()
    time.sleep(2)
    arduino_send_progress_message(True,4,False)
    time.sleep(2)
    arduino_send_progress_message(True,5,True)
    time.sleep(2)
    arduino_send_progress_message(True,0,False)
    time.sleep(2)
    arduino_send_progress_message(True,1,True)
    time.sleep(2)
    arduino_send_progress_message(True,2,True)
    time.sleep(2)
    arduino_send_progress_message(True,3,False)
    time.sleep(2)
    arduino_send_progress_message(True,6,False)
    time.sleep(2)
    arduino_send_end_game_message()
