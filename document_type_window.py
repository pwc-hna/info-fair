
from PySide import QtGui

class DocumentWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        layout = QtGui.QHBoxLayout()
        self.b1 = QtGui.QRadioButton("Button1")
        self.b1.setChecked(True)
        self.b1.toggled.connect(lambda:self.btnstate(self.b1))
        layout.addWidget(self.b1)
            
        self.b2 = QtGui.QRadioButton("Button2")
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))

        layout.addWidget(self.b2)
        self.setLayout(layout)
        self.setWindowTitle("RadioButton demo")
            
    def btnstate(self,b):
        
        if b.text() == "Button1":
            if b.isChecked() == True:
                print b.text()+" is selected"
            else:
                print b.text()+" is deselected"
                    
        if b.text() == "Button2":
            if b.isChecked() == True:
                print b.text()+" is selected"
            else:
                print b.text()+" is deselected"
