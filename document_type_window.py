import subprocess
from PySide import QtGui, QtCore
import psutil
import os
import file_get_props
import time
import random
import sys
import requests
import server_tools

ms = 0
s = 0
m = 0

class DocumentWindow(QtGui.QWidget):
    def __init__(self, player_name):
        QtGui.QWidget.__init__(self)
        self.player_name = player_name
        self.mistakes = 0
        
        self.resize(639, 501)
        icon = QtGui.QIcon()
        icon.addFile('res/logos/pwc_logo_16x16.png', QtCore.QSize(16,16))
        icon.addFile('res/logos/pwc_logo_24x24.png', QtCore.QSize(24,24))
        icon.addFile('res/logos/pwc_logo_32x32.png', QtCore.QSize(32,32))
        icon.addFile('res/logos/pwc_logo_48x48.png', QtCore.QSize(48,48))
        icon.addFile('res/logos/pwc_logo_256x256.png', QtCore.QSize(256,256))
        self.setWindowIcon(icon)
        self.setWindowTitle('BeatTheBot')

        self.label_logo = QtGui.QLabel(self)
        self.label_logo.move(50, 30)
        self.label_logo.setText("")
        self.label_logo.setPixmap(QtGui.QPixmap("res/logos/pwc_logo_bw_100x76.png"))
        self.label_logo.show()

        
        self.text_label = QtGui.QLabel(self) 
        self.text_label.setText("Select document")
        self.text_label.setGeometry(QtCore.QRect(120, 170, 435, 72))
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setWeight(75)
        self.text_label.setFont(font)
        self.text_label.show()

        self.submit_btn = QtGui.QPushButton('Submit', self)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.submit_btn.setFont(font)
        self.submit_btn.move(447,350)
        self.submit_btn.clicked.connect(self.handleSubmit)

        self.btn_cv = QtGui.QRadioButton("CV", self)
        self.btn_cv.toggled.connect(lambda:self.btnstate(self.btn_cv))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.btn_cv.setFont(font)
        self.btn_cv.move(120, 250)

        self.btn_invoice = QtGui.QRadioButton("Invoice", self)
        self.btn_invoice.toggled.connect(lambda:self.btnstate(self.btn_invoice))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.btn_invoice.setFont(font)
        self.btn_invoice.move(230, 250)

        self.btn_group = QtGui.QButtonGroup()
        self.btn_group.addButton(self.btn_cv)
        self.btn_group.addButton(self.btn_invoice)

        self.lcd = QtGui.QLCDNumber(self)
        self.lcd.setGeometry(QtCore.QRect(120, 400, 435, 72))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.lcd.setFont(font)

        try:
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.stopwatch_show_time)
        except (KeyboardInterrupt, SystemExit):
            print "Keyboard interrupt, quitting threads."
            sys.exit()
            pass

        doc_dir = os.path.dirname(os.path.realpath(__file__)) + "\\documents\\output\\"
        doc_files = os.listdir(doc_dir)
        self.filenames = []
        for doc_file in doc_files:
            # Don't include word rubbish files created by taskkill / gitignore / zip files
            if ('$' not in doc_file) and ('.gitignore' not in doc_file) and ('.zip' not in doc_file) and ('.docx' not in doc_file):
                self.filenames.append(doc_dir+doc_file)
        random.shuffle(self.filenames)
        # self.filenames = self.filenames[:5]

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

        # Verify if choice is correct: CVs have even sum digits, invoices have odd
        fname, file_extension = os.path.splitext(os.path.basename(self.filenames[self.current_file_index]))
        if (submitted_doc_type == 'CV') and (sum_digits(int(fname)) % 2 == 0):
            print "The choice is correct"
            # TODO: Light up green leds in tree
            pass
        elif (submitted_doc_type == "Invoice") and (sum_digits(int(fname)) % 2 != 0):
            print "The choice is correct"
            # TODO: Light up green leds in tree
            pass
        else:
            print "The choice is NOT correct"
            # TODO: Light up red leds in tree
            self.mistakes += 1

        # close active subprocess: word, acrobat, photo viewer
        os.system("taskkill /f /im winword.exe /im AcroRd32.exe /im acrobat.exe /im dllhost.exe")
        # increment file index
        self.current_file_index += 1
        self.hide()
        self.display_docs()

    def btnstate(self,b):
        pass

    def launch_doc(self, filename):
        # print "filepath = "+filename
        command = ['cmd', '/c', 'start', '/max', filename]
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
            final_time = "{0}:{1}:{2}".format("%02d"%(m,),"%02d"%(s,),"%02d"%(ms,))
            print "you did it in " + final_time + " and had " + str(self.mistakes) + " mistakes"
            # self.post_json(self.player_name, final_time, self.mistakes)
            server_tools.post_game_end_json(self.player_name, final_time, self.mistakes)
            server_tools.open_results_page()
            self.close()
            return

        server_tools.post_player_progress_json(self.player_name, self.current_file_index, len(self.filenames))
        self.current_file = self.filenames[self.current_file_index]
        # print "current filename  = "+ self.current_file
        self.launch_doc(self.current_file)
        
        # Launch the window to get the document type selected by the player
        time.sleep(5)

        self.show()
        self.activateWindow()
        if self.current_file_index == 0:
            self.stopwatch_start_timer()

    def post_json(self, player_name, final_time, mistakes):
        r = requests.post('http://localhost:5000/foo', json={"username": player_name, "time":final_time,"mistakes":mistakes})

def exit_handler():
    os.system("taskkill /f /im winword.exe /im AcroRd32.exe /im acrobat.exe /im dllhost.exe")
import qdarkstyle
import atexit
import settings

def sum_digits(n):
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s

if __name__ == '__main__':
    settings.init()
    # GUI app will get the name of the player
    player_name_app = QtGui.QApplication(sys.argv)
    player_name_window = DocumentWindow('Horia')
    player_name_app.setStyleSheet(qdarkstyle.load_stylesheet_pyside())
    player_name_window.show()
    player_name_app.exec_()
    atexit.register(exit_handler)
    sys.exit()
