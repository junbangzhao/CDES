from PyQt5 import QtWidgets,QtGui,QtCore,Qt

class VisualSearch(QtWidgets.QWidget):
    def __init__(self,parent = None):
        QtWidgets.QWidget.__init__(self)
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width()/2, screen.height()/2)
        self.move(screen.width()/2-self.width()/2,screen.height()/2-self.height()/2)
        
        self.lFix = QtWidgets.QLabel(self)
        self.lTarget = QtWidgets.QLabel(self)
        self.l1 = QtWidgets.QLabel(self)
        self.l2 = QtWidgets.QLabel(self)
        self.l3 = QtWidgets.QLabel(self)
        self.l4 = QtWidgets.QLabel(self)
        
        label = [self.l1,self.l2,self.l3,self.l4,self.lTarget]
        display = ['A','1','上','B','X']
        
        for (l,d) in zip(label,display):
            l.setStyleSheet("background-color:red")
            l.setText(d)
            l.setFont(QtGui.QFont("Times",70))
            l.setAlignment(Qt.Qt.AlignCenter)
        hbox = QtWidgets.QHBoxLayout()
        vbox = QtWidgets.QVBoxLayout()
        
        hbox.addStretch(2)
        hbox.addWidget(self.l1)
        hbox.addStretch(1)
        hbox.addWidget(self.l2)
        hbox.addStretch(1)
        hbox.addWidget(self.l3)
        hbox.addStretch(1)
        hbox.addWidget(self.l4)
        hbox.addStretch(2)
        
        vbox.addStretch(2)
        vbox.addWidget(self.lTarget)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(2)
        
        self.setLayout(vbox)
        
        
        
        
        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = VisualSearch()
    main.show()
    sys.exit(app.exec_())