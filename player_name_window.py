
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
 
        # The recipient control is an entry textbox
        self.player_name_edit = QtGui.QLineEdit(self)
        # Add some ghost text to indicate what sort of thing to enter
        self.player_name_edit.setPlaceholderText("Gandalf the grey")
        # Same width as the salutation
        self.player_name_edit.setMinimumWidth(285)
        # Same indent as salutation but 25 pixels lower
        self.player_name_edit.move(110, 30)

        self.submit_btn = QtGui.QPushButton('Submit', self)
        self.submit_btn.clicked.connect(self.handleNameButton)
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.player_name_label)
        self.layout.addWidget(self.player_name_edit)
        self.layout.addWidget(self.submit_btn)

    def handleNameButton(self):
        # store playername in a database
        print ('Got name ' + self.player_name_edit.text())
        self.player_name = self.player_name_edit.text()

        stopwatch = time.time()
        # Now we have a character name, iterate through the list of documents and open them for classification
        filename = 'cv_template.docx'
        open_doc_process = self.launch_doc(filename)
        
        # Launch the window to get the document type selected by the player
        time.sleep(5)
        document_type_window = DocumentWindow(filename)
        document_type_window.show()

        self.close()
        stopwatch = time.time() - stopwatch
        print ("You did it in ---%s seconds ---" % stopwatch)

    def launch_doc(self, filename):
        print "filepath = "+filename
        command = ['cmd', '/c', 'start', filename]
        return subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    def getPlayerName(self):
        return self.player_name