import subprocess
from PySide import QtGui, QtCore
import psutil
import os
import file_get_props
import time
import random
import sys

ms = 0
s = 0
m = 0

class DocumentWindow(QtGui.QWidget):
    def __init__(self, player_name):
        QtGui.QWidget.__init__(self)
        self.player_name = player_name
        self.mistakes = 0

        layout = QtGui.QGridLayout()
        
        text_label = QtGui.QLabel() 
        text_label.setText(str(self.player_name) + ", Which category is appropriate for the document in background?")
        layout.addWidget(text_label,1,0)
        
        self.submit_btn = QtGui.QPushButton('Submit', self)
        self.submit_btn.clicked.connect(self.handleSubmit)
        layout.addWidget(self.submit_btn,3,0)


        self.btn_cv = QtGui.QRadioButton("CV")
        self.btn_cv.toggled.connect(lambda:self.btnstate(self.btn_cv))
        layout.addWidget(self.btn_cv,2,0)
            
        self.btn_invoice = QtGui.QRadioButton("Invoice")
        self.btn_invoice.toggled.connect(lambda:self.btnstate(self.btn_invoice))
        layout.addWidget(self.btn_invoice,2,1)
        self.btn_group = QtGui.QButtonGroup()
        self.btn_group.addButton(self.btn_cv)
        self.btn_group.addButton(self.btn_invoice)       


        self.lcd = QtGui.QLCDNumber(self)
        layout.addWidget(self.lcd,4,0,1,3)

        try:
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.stopwatch_show_time)
        except (KeyboardInterrupt, SystemExit):
            print "Keyboard interrupt, quitting threads."
            sys.exit()
            pass



        self.setLayout(layout)
        self.setWindowTitle("?")

        self.filenames = ['word_cv_template.docx','word_invoice.docx']
        random.shuffle(self.filenames)

        self.current_file_index = 0
        self.display_docs()

    def handleSubmit(self):
        submitted_doc_type = None
        if self.btn_cv.isChecked():
            # print self.btn_cv.text() + "is selected"
            submitted_doc_type = self.btn_cv.text()
        elif self.btn_invoice.isChecked():
            # print self.btn_invoice.text() + " is selected"
            submitted_doc_type = self.btn_invoice.text()
        else:
            print "Nothing is selected"
            return
        self.btn_group.setExclusive(False)
        self.btn_cv.setChecked(False)
        self.btn_invoice.setChecked(False)
        self.btn_group.setExclusive(True)

        # Verify if choice is correct
        if (submitted_doc_type == file_get_props.get_comments(self.current_file)):
            # print "The choice is correct"
            pass
        else:
            # print "The choice is NOT correct"
            self.mistakes += 1
            
        # close active subprocess
        os.system("taskkill /im winword.exe")
        # increment file index
        self.current_file_index += 1
        self.hide()
        self.display_docs()

    def btnstate(self,b):
        pass

    def launch_doc(self, filename):
        # print "filepath = "+filename
        command = ['cmd', '/c', 'start', filename]
        return subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    def stopwatch_show_time(self):
        global ms,s,m
        if ms < 99:
            ms += 1
        elif s < 59:
            ms = 0
            s += 1
        elif s == 59 and m < 60:
            ms = 0
            s = 0
            m += 1
        else:
            self.timer.stop()

        time = "{0}:{1}:{2}".format("%02d"%(m,),"%02d"%(s,),"%02d"%(ms,))

        self.lcd.setDigitCount(len(time))
        self.lcd.display(time)

    def stopwatch_start_timer(self):
        global ms,s,m
        self.timer.start(10)

    def display_docs(self):
        global ms,s,m
        # print "filenames = "+str(self.filenames)

        if self.current_file_index >= len(self.filenames):
            # print "Last file, stop timer" 
            self.timer.stop()
            # TODO: send name + time + accuracy to server
            print "you did it in " + "{0}:{1}:{2}".format("%02d"%(m,),"%02d"%(s,),"%02d"%(ms,)) + " and had " + str(self.mistakes) + " mistakes"
            self.close()
            return

        self.current_file = self.filenames[self.current_file_index]
        # print "current filename  = "+ self.current_file
        self.launch_doc(self.current_file)
        
        # Launch the window to get the document type selected by the player
        time.sleep(5)

        self.show()
        self.activateWindow()
        if self.current_file_index == 0:
            self.stopwatch_start_timer()
        