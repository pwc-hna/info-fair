import subprocess
from PySide import QtGui
import psutil
import os
import file_get_props


class DocumentWindow(QtGui.QWidget):
    def __init__(self, filename):
        QtGui.QWidget.__init__(self)
        self.filename = filename
        layout = QtGui.QHBoxLayout()
        
        text_label = QtGui.QLabel() 
        text_label.setText("Which category is appropriate for the document in background?")
        layout.addWidget(text_label)
        
        self.submit_btn = QtGui.QPushButton('Submit', self)
        self.submit_btn.clicked.connect(self.handleSubmit)
        layout.addWidget(self.submit_btn)


        self.b1 = QtGui.QRadioButton("CV")
        self.b1.toggled.connect(lambda:self.btnstate(self.b1, self.submit_btn))
        layout.addWidget(self.b1)
            
        self.b2 = QtGui.QRadioButton("Invoice")
        self.b2.toggled.connect(lambda:self.btnstate(self.b2, self.submit_btn))
        layout.addWidget(self.b2)

        self.setLayout(layout)
        self.setWindowTitle("Test")
        self.activateWindow()

    def handleSubmit(self):
        submitted_doc_type = None
        if self.b1.isChecked():
            print self.b1.text() + "is selected"
            submitted_doc_type = self.b1.text()
            
        else:
            print self.b2.text() + "is selected"
            submitted_doc_type = self.b2.text()

        # Verify if choice is correct
        if (submitted_doc_type == file_get_props.get_comments(self.filename)):
            print "The choice is correct"
        else:
            print "The choice is NOT correct"
            
        # close active subprocess
        os.system("taskkill /im winword.exe")
        self.close()

    def btnstate(self,b,submit_btn):
        if b.text() == "CV":
            if b.isChecked() == True:
                print b.text()+" is selected"
            else:
                print b.text()+" is deselected"
        if b.text() == "Invoice":
            if b.isChecked() == True:
                print b.text()+" is selected"
            else:
                print b.text()+" is deselected"
