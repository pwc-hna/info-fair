import json
import requests
import settings
import time
import os
import serial


def post_json_to_server(json, route):
    requests.post(settings.serverAddress + route, json=json)


def post_game_end_json(player_name, final_time, mistakes):
    post_json_to_server(json={"username": player_name,
                        "time": final_time, "mistakes": mistakes}, route='/finished')


def post_player_progress_json(player_name, current_doc, total_docs):
    post_json_to_server(json={"username": player_name, "current_doc": current_doc,
                        "total_docs": total_docs}, route='/progress')


def post_player_quit_game():
    if settings.playerName is not None:
        post_json_to_server(
            json={"username": settings.playerName}, route='/quit')


def open_results_page():
    os.startfile(settings.serverAddress)

def arduino_send_message(message):
    print("arduino send message = "+message)
    ser = None
    try:
        ser = serial.Serial('COM6', 9600)
    except Exception as e:
        print (str(e))

    try:
        ser.write(message)
    except Exception as e:
        print(str(e))

def arduino_send_player_submit_name_game_message():
    message = "TNNNNNNN"
    settings.game_status = message
    arduino_send_message(message)

def arduino_send_start_game_message():
    arduino_send_message(settings.game_status)

def arduino_send_end_game_message():
    messageList = list(settings.game_status)
    messageList[0] = 'F'
    message = ''.join(messageList)
    settings.game_status = message
    arduino_send_message(message)

def arduino_send_progress_message(isGameStarted, current_doc_index, isCorrect):
    messageList = list(settings.game_status)
    messageList[0] = 'T' if isGameStarted else 'F'
    messageList[current_doc_index + 1] = 'T' if isCorrect else 'F'
    message = ''.join(messageList)
    settings.game_status = message
    arduino_send_message(message)


if __name__ == '__main__':
    settings.init()
    print("initial status = "+settings.game_status)
    arduino_send_start_game_message()
    arduino_send_progress_message(True,0,False)
    arduino_send_progress_message(True,1,True)
    arduino_send_end_game_message()
