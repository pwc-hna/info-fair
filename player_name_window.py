
from PySide import QtGui
import subprocess
from document_type_window import DocumentWindow
import time
import os
import server_tools

class PlayerNameWindow(QtGui.QWidget):
    player_name = None 
    def __init__(self):
        QtGui.QWidget.__init__(self)

        # The label for the recipient control
        self.player_name_label = QtGui.QLabel('Enter your Nickname:', self)
        # 5 pixel indent, 25 pixels lower than last pair of widgets
        self.player_name_label.move(5, 30)
 
        self.submit_btn = QtGui.QPushButton('Submit', self)
        self.submit_btn.clicked.connect(self.handleNameButton)

        # The recipient control is an entry textbox
        self.player_name_edit = QtGui.QLineEdit(self)
        self.player_name_edit.returnPressed.connect(self.submit_btn.click)

        # Add some ghost text to indicate what sort of thing to enter
        self.default_player_name = "Gandalf the Grey"
        self.player_name_edit.setPlaceholderText(self.default_player_name)
        # Same width as the salutation
        self.player_name_edit.setMinimumWidth(285)
        # Same indent as salutation but 25 pixels lower
        self.player_name_edit.move(110, 30)

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.player_name_label)
        self.layout.addWidget(self.player_name_edit)
        self.layout.addWidget(self.submit_btn)

    def handleNameButton(self):
        self.player_name = self.player_name_edit.text()
        if self.player_name == None:
            self.player_name = self.default_player_name
        # server_tools.post_player_progress_json(self.player_name, '0','2')
        document_type_window = DocumentWindow(self.player_name)
        self.close()

    def getPlayerName(self):
        return self.player_name