import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import settings
import requests
from main import start_game
from time import sleep
import thread

def is_player_live():
    url = settings.serverAddress + "/live"
    try:
        resp = requests.get(url)
        data = resp.json()
        print data
        if data['live_player'] is not None:
            return True
    except KeyError as e:
        return False
    return False

def poll_live_player():
    while not is_player_live():
        sleep(0.2)

def start_robot():
    print "Starting robot!"
    pass

def start_new_game(wtfarg):
    start_game()


if __name__ == '__main__':
    # First iteration
    settings.init()
    try:
        thread.start_new_thread(start_new_game,("wtfarg",))
    except Exception as e:
        print "Error: unable to start thread " + str(e)
    poll_live_player()
    start_robot()
