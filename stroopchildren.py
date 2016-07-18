from PyQt5 import QtWidgets, QtCore, QtGui, Qt
import random


class StroopChildren(QtWidgets.QWidget):
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
  
        self.labelLeft = QtWidgets.QLabel(self)
        self.labelLeft.setAlignment(Qt.Qt.AlignCenter)
        
        self.labelLeft.setFont(QtGui.QFont("Times",40))
        self.labelLeft.setGeometry(0,0,100,100)
        self.labelLeft.move((self.width()-self.labelLeft.width())/2-100,(self.height()-self.labelLeft.height())/2)
        #print(self.labelLeft.fontMetrics().height())
        self.labelLeft.setText("2")
        #self.labelLeft.hide()
        #self.labelLeft.setStyleSheet("background-color:red")
        
        
        self.labelRight = QtWidgets.QLabel(self)
        self.labelRight.setAlignment(Qt.Qt.AlignCenter)
        self.labelRight.setFont(QtGui.QFont("Times",100))
        self.labelRight.setText("9")
        self.labelRight.setGeometry(0,0,100,100)
        self.labelRight.move((self.width()-self.labelRight.width())/2+100,(self.height()-self.labelRight.height())/2)
        #self.labelRight.setStyleSheet("background-color:red")
        #self.labelRight.hide()
        
        self.labelFix = QtWidgets.QLabel(self)
        self.labelFix.setAlignment(Qt.Qt.AlignCenter)
        self.labelFix.setFont(QtGui.QFont("Times",40))
        self.labelFix.setText("+")
        self.labelFix.setGeometry(0,0,100,100)
        self.labelFix.move((self.width()-self.labelFix.width())/2,(self.height() -self.labelFix.height())/2)

        
        #self.setCursor(Qt.Qt.BlankCursor)
        self.bResponse = False
        self.RT = QtCore.QElapsedTimer()

    def setRound(self,Round):
        self.Round = Round
        
    def showEvent(self,event):
        while True:
            text, ok= QtWidgets.QInputDialog.getText(self, ("实验次数"), ("次数为6的整数倍"), QtWidgets.QLineEdit.Normal, "")
            if not ok:
                quit()
            try:
                self.Round = int(text)
                
                if self.Round % 6 == 0:
                    print ("right")
                    break
            except:        
                print("wrong")
                pass
        
        self.iRound = 0
        self.bStart = False
        self.listRound = ['LS','LD','LN','SS','SD','SN']*int(self.Round/4)
        random.shuffle(self.listRound)
        self.ResponseData = []
        self.rData = {}
        
        '''
        self.labelLeft.setText("Stroop效应\n\n 如果左边的数字大用左手食指按F键，\n右边的数字大用右手食指按J键")
        self.labelLeft.setFont(QtGui.QFont("宋体",40))
        self.labelLeft.show()
        #print("Show")
        #print(self.bStart)
        print(self.listRound)
        '''
        
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            print(self.ResponseData)
            self.close()
        if event.key() == QtCore.Qt.Key_Return:
            if not self.bStart :
                self.labelLeft.hide()
                self.labelRight.hide()
                self.labelFix.hide()
                self.timer_fix.start(1000)
                self.bStart = True
            else:
                print("Already Start")
            
        if event.key() == QtCore.Qt.Key_F:
            if(self.bResponse):
                self.labelLeft.hide()
                self.rData['RT'] = self.RT.elapsed()
                if(self.listRound[self.iRound] == 'RR' or 'GR'):
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
                self.labelLeft.hide()
                self.rData['RT'] = self.RT.elapsed()
                if(self.listRound[self.iRound] == 'RG' or 'GG'):
                    self.rData['isCorrect'] = 'R'
                else:
                    self.rData['isCorrect'] = 'W'
                
                self.timer_blank.stop()
                self.timer_blank.start(0)
                self.bResponse = False
            else:
                print("Wrong Response")
                
    def tfUpdate(self):
        self.labelFix.show()
        self.timer_fix.stop()
        self.timer_target.start(1000)
        
    def ttUpdate(self):
        #print('iRound = %d'%self.iRound)
        #print(self.listRound[self.iRound])
        self.labelFix.hide()
        self.rData['No.'] = self.iRound + 1
        if self.listRound[self.iRound] == 'LS':
            self.labelLeft.setText("1")
            self.labelLeft.setFont(QtGui.QFont("Times",40))
            self.labelRight.setText("9")
            self.labelRight.setFont(QtGui.QFont("Times",80))
            self.rData['type'] = 'LS'
            print('LS')
        elif self.listRound[self.iRound] == 'LD':
            self.labelLeft.setText("1")
            self.labelLeft.setFont(QtGui.QFont("Times",80))
            self.labelRight.setText("9")
            self.labelRight.setFont(QtGui.QFont("Times",40))
            self.rData['type'] = 'LD'
            print('LD')
        elif self.listRound[self.iRound] == 'LN':
            self.labelLeft.setText("1")
            self.labelLeft.setFont(QtGui.QFont("Times",40))
            self.labelRight.setText("9")
            self.labelRight.setFont(QtGui.QFont("Times",40))
            self.rData['type'] = 'LN'
            print('GR')
        elif self.listRound[self.iRound] == 'SS':
            self.labelLeft.setText("1")
            self.labelLeft.setFont(QtGui.QFont("Times",40))
            self.labelRight.setText("2")
            self.labelRight.setFont(QtGui.QFont("Times",80))
            self.rData['type'] = 'SS'
            print('SS')
        elif self.listRound[self.iRound] == 'SD':
            self.labelLeft.setText("1")
            self.labelLeft.setFont(QtGui.QFont("Times",80))
            self.labelRight.setText("2")
            self.labelRight.setFont(QtGui.QFont("Times",40))
            self.rData['type'] = 'SD'
            print('SD')
        elif self.listRound[self.iRound] == 'SN':
            self.labelLeft.setText("1")
            self.labelLeft.setFont(QtGui.QFont("Times",40))
            self.labelRight.setText("2")
            self.labelRight.setFont(QtGui.QFont("Times",40))
            self.rData['type'] = 'SN'
            print('SN')
        self.labelLeft.show()
        self.labelRight.show()
        
        if self.RT.isValid():
            self.RT.restart()
        else:
            self.RT.start()
        
        self.bResponse = True
        
        self.timer_target.stop()
        self.timer_blank.start(1500)
        #print ("target")

    def tbUpdate(self):
        self.labelLeft.hide()
        self.labelRight.hide()
        if self.bResponse:
            self.rData['RT'] = 0
            self.rData['isCorrect'] = 'M'
        self.ResponseData.append(self.rData)
        print(self.rData)
        self.iRound = self.iRound + 1
        self.rData = {}
        self.bResponse = False
        if self.iRound < self.Round:
            self.timer_fix.start(1000) 
        else:
            file = QtCore.QFile("StroopChildrenResut.txt")
            if not file.open(QtCore.QIODevice.WriteOnly or QtCore.QIODevice.Text):
                print("error")
                return 0
            out = QtCore.QTextStream(file)
            out << "No." << "\t" << "isCorrect" << "\t" << "type" << "\t" << "RT" << "\r\n"
            for RT in self.ResponseData:
                out << RT['No.'] << "\t" << RT["isCorrect"]<< "\t" << RT["type"] << "\t" << RT["RT"] << "\r\n"
            self.labelLeft.setText("结束实验，谢谢参与，请按ESC键退出")
            self.labelLeft.setFont(QtGui.QFont("宋体",20))
            self.labelLeft.setStyleSheet("color:black")
            self.labelLeft.show()
        #print("blank")
        
        
        self.timer_blank.stop()

        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = StroopChildren()
    main.show()
    sys.exit(app.exec_())
