
from PySide import QtGui, QtUiTools, QtCore
import subprocess
from document_type_window import DocumentWindow
import time
import os
import server_tools

class PlayerNameWindow(QtGui.QWidget):
    player_name = None 
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(639, 501)
        icon = QtGui.QIcon()
        icon.addFile('res/logos/pwc_logo_16x16.png', QtCore.QSize(16,16))
        icon.addFile('res/logos/pwc_logo_24x24.png', QtCore.QSize(24,24))
        icon.addFile('res/logos/pwc_logo_32x32.png', QtCore.QSize(32,32))
        icon.addFile('res/logos/pwc_logo_48x48.png', QtCore.QSize(48,48))
        icon.addFile('res/logos/pwc_logo_256x256.png', QtCore.QSize(256,256))
        self.setWindowIcon(icon)
        self.setWindowTitle('BeatTheBot')

        self.label_enter_name = QtGui.QLabel('Enter your name:', self)
        self.label_enter_name.setGeometry(QtCore.QRect(120, 170, 435, 72))
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setWeight(75)
        font.setBold(True)
        self.label_enter_name.setFont(font)

        self.submit_btn = QtGui.QPushButton('Submit', self)
        self.submit_btn.clicked.connect(self.handleNameButton)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.submit_btn.setFont(font)
        self.submit_btn.move(447,350)

        self.edit_player_name = QtGui.QLineEdit(self)
        self.edit_player_name.returnPressed.connect(self.submit_btn.click)
        self.edit_player_name.setGeometry(QtCore.QRect(120, 250, 435, 72))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.edit_player_name.setFont(font)

         # Add some ghost text to indicate what sort of thing to enter
        self.edit_default_player_name = "Gandalf the Grey"
        self.edit_player_name.setPlaceholderText(self.edit_default_player_name)
        # Same width as the salutation
        self.edit_player_name.setMinimumWidth(300)

        self.label_logo = QtGui.QLabel(self)
        self.label_logo.move(50, 30)
        self.label_logo.setText("")
        self.label_logo.setPixmap(QtGui.QPixmap("res/logos/pwc_logo_bw_100x76.png"))
        self.label_logo.show()

    def handleNameButton(self):
        self.player_name = self.edit_player_name.text()
        if self.player_name == None:
            self.player_name = self.edit_default_player_name
        document_type_window = DocumentWindow(self.player_name)
        self.close()

    def getPlayerName(self):
        return self.player_name