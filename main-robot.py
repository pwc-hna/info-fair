import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import settings
import requests
from main import start_game
from time import sleep
import thread
import gevent
from subprocess import Popen, PIPE
import server_tools

robot_names = []
def is_player_live():
    url = settings.serverAddress + "/live"
    try:
        resp = requests.get(url)
        data = resp.json()
        for live_player in data:
            if 'mRobot' not in live_player['username']:
                robotName = 'mRobot'+live_player['username']+'*'+live_player['creation_date']
                if robotName not in robot_names:
                    robot_names.append(robotName)
                    return [True, robotName]
    except KeyError:
        pass
    except IOError:
        pass
    return [False, None]

def poll_live_player():
    playerIsLive = False
    playerName = ''
    while not playerIsLive: 
        [playerIsLive, playerName] = is_player_live()
        gevent.sleep(0.2)
    return playerName

def start_robot(playerName):
    print "Starting robot!"
    proc = Popen(["C:\\Users\\naidinh\\AppData\\Local\\UiPath\\app-18.4.0\\UiRobot.exe","/file" ,"C:\\Work\\python-info-fair-wrapper\\robot\\robotProcess\\Main.xaml", "-input", "{'player_name':'"+playerName+"'}"], shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    proc.wait()
    output, err = proc.communicate()
    rc = proc.returncode

def start_new_game():
    proc = Popen(["C:\Python27\python.exe", "C:\\Work\\python-info-fair-wrapper\\main.py"], shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return proc


if __name__ == '__main__':
    settings.init()
    while True:
        try:
            main_game_proc = start_new_game()
        except Exception as e:
            print "Error: unable to start thread " + str(e)
        robotName = poll_live_player()
        print ("Start robot with player name = "+robotName)
        try:
            start_robot(robotName)
            main_game_proc.wait()
            output, err = main_game_proc.communicate()
        except KeyboardInterrupt as e:
            exit(-1)
