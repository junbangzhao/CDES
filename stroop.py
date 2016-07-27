from PyQt5 import QtWidgets, QtCore, QtGui, Qt
import random

class Stroop(QtWidgets.QWidget):  
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self)
        #self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width()/2, screen.height()/2)
        self.move(screen.width()/2-self.width()/2,screen.height()/2-self.height()/2)
        #---------------------------------------------
        #时间控件初始化
        self.timer_fix = QtCore.QTimer()
        self.timer_fix.timeout.connect(self.tfUpdate)
        
        self.timer_target = QtCore.QTimer()
        self.timer_target.timeout.connect(self.ttUpdate)
        
        self.timer_blank = QtCore.QTimer()
        self.timer_blank.timeout.connect(self.tbUpdate)
        #----------------------------------------------
  
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(Qt.Qt.AlignCenter)
        self.label.hide()
        #-----------------------------------------------
        #布局
        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch(0)
        vbox.addWidget(self.label)
        vbox.addStretch(0)
        
        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(0)
        hbox.addLayout(vbox)
        hbox.addStretch(0)
        
        self.setLayout(hbox)
        #-----------------------------------------------
        
        self.setCursor(Qt.Qt.BlankCursor)
        self.bResponse = False
        self.RT = QtCore.QElapsedTimer()

    def setRound(self,Round):
        self.Round = Round
        
    def showEvent(self,event):
        #self.Round = 4
        while True:
            text, ok= QtWidgets.QInputDialog.getText(self, ("实验次数"), ("次数为4的整数倍"), QtWidgets.QLineEdit.Normal, "")
            if not ok: quit()
            try:
                self.Round = int(text)
                
                if self.Round % 4 == 0 and self.Round > 0:
                    print ("right")
                    break
            except:        
                print("wrong")
                pass
        
        self.iRound = 0
        self.bStart = False
        self.listRound = ['RR','RG','GR','GG']*int(self.Round/4)
        random.shuffle(self.listRound)
        self.ResponseData = []
        self.rData = {}
        
        self.label.setText("Stroop效应\n \n请看到红颜色的字左手食指按F键，\n绿颜色的字右手食指按J键")
        self.label.setFont(QtGui.QFont("宋体",40))
        self.label.show()
        #print("Show")
        #print(self.bStart)
        print(self.listRound)
        
        
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            print(self.ResponseData)
            self.close()
        if event.key() == QtCore.Qt.Key_Return:
            if not self.bStart :
                self.label.hide()
                self.timer_fix.start(1000)
                self.bStart = True
            else:
                print("Already Start")
            
        if event.key() == QtCore.Qt.Key_F:
            if(self.bResponse):
                self.label.hide()
                self.rData['RT'] = self.RT.elapsed()
                if(self.listRound[self.iRound] == 'RR' or self.listRound[self.iRound] == 'RG'):
                    self.rData['isCorrect'] = 'R'
                else:
                    self.rData['isCorrect'] = 'W'
                
                self.timer_blank.stop()
                self.timer_blank.start(0)
                self.bResponse = False
            else:
                print ("Wrong Response")
        
        if event.key() == QtCore.Qt.Key_J:
            if (self.bResponse):
                self.label.hide()
                self.rData['RT'] = self.RT.elapsed()
                if(self.listRound[self.iRound] == 'GR' or self.listRound[self.iRound] == 'GG'):
                    self.rData['isCorrect'] = 'R'
                else:
                    self.rData['isCorrect'] = 'W'
                
                self.timer_blank.stop()
                self.timer_blank.start(0)
                self.bResponse = False
            else:
                print("Wrong Response")
                
    def tfUpdate(self):
        self.label.setText("+")
        self.label.setStyleSheet("color:black")
        self.label.setFont(QtGui.QFont("Times",60))
        self.label.show()
        self.timer_fix.stop()
        self.timer_target.start(1000)
        #print ("fixation")
        
    def ttUpdate(self):
        print('iRound = %d'%self.iRound)
        print(self.listRound[self.iRound])
        self.rData['No.'] = self.iRound + 1
        if self.listRound[self.iRound] == 'RR':
            self.label.setStyleSheet("color:red")
            self.label.setText("红")
            self.rData['type'] = 'S'
            print('RR')
        elif self.listRound[self.iRound] == 'RG':
            self.label.setStyleSheet("color:red")
            self.label.setText("绿")
            self.rData['type'] = 'D'
            print('RG')
        elif self.listRound[self.iRound] == 'GR':
            self.label.setStyleSheet("color:green")
            self.label.setText("红")
            self.rData['type'] = 'D'
            print('GR')
        elif self.listRound[self.iRound] == 'GG':
            self.label.setStyleSheet("color:green")
            self.label.setText("绿")
            self.rData['type'] = 'S'
            print('GG')
        self.label.setFont(QtGui.QFont("宋体", 100))
        self.label.show()
        
        if self.RT.isValid():
            self.RT.restart()
        else:
            self.RT.start()
        
        self.bResponse = True
        
        self.timer_target.stop()
        self.timer_blank.start(1000)
        #print ("target")

    def tbUpdate(self):
        self.label.hide()
        if self.bResponse:
            self.rData['RT'] = 0
            self.rData['isCorrect'] = 'M'
        self.ResponseData.append(self.rData)
        print(self.rData)
        self.iRound = self.iRound + 1
        self.rData = {}
        self.bResponse = False
        if self.iRound < self.Round:
            self.timer_fix.start(1500) 
        else:
            file = QtCore.QFile("StroopResut.txt")
            if not file.open(QtCore.QIODevice.WriteOnly or QtCore.QIODevice.Text):
                print("error")
                return 0
            out = QtCore.QTextStream(file)
            out << "No." << "\t" << "isCorrect" << "\t" << "type" << "\t" << "RT" << "\r\n"
            for RT in self.ResponseData:
                out << RT['No.'] << "\t" << RT["isCorrect"]<< "\t" << RT["type"] << "\t" << RT["RT"] << "\r\n"
            self.label.setText("结束实验，谢谢参与，请按ESC键退出")
            self.label.setFont(QtGui.QFont("宋体",20))
            self.label.setStyleSheet("color:black")
            self.label.show()
        #print("blank")
        
        
        self.timer_blank.stop()

        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = Stroop()
    main.show()
    sys.exit(app.exec_())
