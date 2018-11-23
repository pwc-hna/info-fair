
from PySide import QtGui
import subprocess
from document_type_window import DocumentWindow
import time
import os

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
        self.player_name_edit.setPlaceholderText("Gandalf the grey")
        # Same width as the salutation
        self.player_name_edit.setMinimumWidth(285)
        # Same indent as salutation but 25 pixels lower
        self.player_name_edit.move(110, 30)

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.player_name_label)
        self.layout.addWidget(self.player_name_edit)
        self.layout.addWidget(self.submit_btn)

    def handleNameButton(self):
        # store playername in a database
        print ('Got name ' + self.player_name_edit.text())
        self.player_name = self.player_name_edit.text()

        document_type_window = DocumentWindow(self.player_name)
        self.close()

    def getPlayerName(self):
        return self.player_name