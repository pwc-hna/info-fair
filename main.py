import sys
import os
import time
import subprocess
from PySide import QtGui
import qdarkstyle
from player_name_window import PlayerNameWindow
from document_type_window import DocumentWindow
    
def launch_doc():
    filename = 'cv_template.docx'
    print "filepath = "+filename
    command = ['cmd', '/c', 'start', filename]
    return subprocess.Popen(command)

if __name__ == '__main__':
    # GUI app will get the name of the player
    player_name_app = QtGui.QApplication(sys.argv)
    player_name_window = PlayerNameWindow()
    player_name_app.setStyleSheet(qdarkstyle.load_stylesheet_pyside())
    player_name_window.show()
    player_name_app.exec_()
    sys.exit()

