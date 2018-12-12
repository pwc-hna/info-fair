# settings.py


def init():
    global serverAddress
    serverHostname = 'http://13.69.20.181'
    serverPort = '80'
    serverAddress = serverHostname + ':' + serverPort
    global playerName 
    playerName = None
    global game_status 
    game_status = "FNNNNNNN"
    global serial_port
    serial_port = 'COM6'
