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

        
        self.setCursor(Qt.Qt.BlankCursor)
        self.bResponse = False
        self.RT = QtCore.QElapsedTimer()
        self.ResponseType = ""

    def setRound(self,Round):
        self.Round = Round
        
    def showEvent(self,event):
        while True:
            text, ok= QtWidgets.QInputDialog.getText(self, ("实验次数"), ("次数为6的整数倍"), QtWidgets.QLineEdit.Normal, "")
            if not ok:
                quit()
            try:
                self.Round = int(text)
                
                if (self.Round % 6 == 0) and (self.Round > 0):
                    print ("right")
                    break
            except:        
                print("wrong")
                pass
        
        self.iRound = 0
        self.bStart = False
        self.listRound = ['LS','LD','LN','SS','SD','SN']*int(self.Round/6)
        random.shuffle(self.listRound)
        self.ResponseData = []
        self.rData = {}
        self.labelLeft.hide()
        self.labelRight.hide()
        self.labelFix.hide()
        self.labelGuide = QtWidgets.QLabel(self)

        self.labelGuide.setText("数字Stroop效应\n\n 如果左边的数字大用左手食指按F键，\n右边的数字大用右手食指按J键，\n按Enter键开始")
        self.labelGuide.setFont(QtGui.QFont("宋体",20))
        self.labelGuide.setGeometry(0,0,500,200)
        self.labelGuide.move((self.width() - self.labelGuide.width())/2,(self.height() - self.labelGuide.height())/2)
        self.labelGuide.setAlignment(Qt.Qt.AlignCenter)
        self.labelGuide.show()
        #print("Show")
        #print(self.bStart)

        
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            print(self.ResponseData)
            self.bStart = False
            self.close()
        if (event.key() == QtCore.Qt.Key_Return) or (event.key() == QtCore.Qt.Key_Enter):
            if not self.bStart :
                self.labelGuide.hide()
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
                self.labelRight.hide()
                self.rData['RT'] = self.RT.elapsed()
                if self.ResponseType == 'F':
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
                if self.ResponseType == 'J':
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
            num = random.randint(1,4)
            if num == 1:
                self.labelLeft.setText("1")
                self.labelRight.setText("9")
            elif num == 2:
                self.labelLeft.setText("2")
                self.labelRight.setText("8")
            elif num == 3:
                self.labelLeft.setText("9")
                self.labelRight.setText("1")
            elif num == 4:
                self.labelLeft.setText("8")
                self.labelRight.setText("2")
            
            if int(self.labelLeft.text()) > int(self.labelRight.text()):
                self.labelLeft.setFont(QtGui.QFont("Times",80))
                self.labelRight.setFont(QtGui.QFont("Times",40))
                self.ResponseType = 'F'
            else:
                self.labelLeft.setFont(QtGui.QFont("Times",40))
                self.labelRight.setFont(QtGui.QFont("Times",80))
                self.ResponseType = 'J'
            self.rData['type'] = 'LS'
            print('LS')
        elif self.listRound[self.iRound] == 'LD':
            num = random.randint(1,4)
            if num == 1:
                self.labelLeft.setText("1")
                self.labelRight.setText("9")
            elif num == 2:
                self.labelLeft.setText("2")
                self.labelRight.setText("8")
            elif num == 3:
                self.labelLeft.setText("9")
                self.labelRight.setText("1")
            elif num == 4:
                self.labelLeft.setText("8")
                self.labelRight.setText("2")
            
            if int(self.labelLeft.text()) < int(self.labelRight.text()):
                self.labelLeft.setFont(QtGui.QFont("Times",80))
                self.labelRight.setFont(QtGui.QFont("Times",40))
                self.ResponseType = 'J'
            else:
                self.labelLeft.setFont(QtGui.QFont("Times",40))
                self.labelRight.setFont(QtGui.QFont("Times",80))
                self.ResponseType = 'F'
            self.rData['type'] = 'LD'
            print('LD')
        elif self.listRound[self.iRound] == 'LN':
            num = random.randint(1,4)
            if num == 1:
                self.labelLeft.setText("1")
                self.labelRight.setText("9")
            elif num == 2:
                self.labelLeft.setText("2")
                self.labelRight.setText("8")
            elif num == 3:
                self.labelLeft.setText("9")
                self.labelRight.setText("1")
            elif num == 4:
                self.labelLeft.setText("8")
                self.labelRight.setText("2")
            size = random.randint(1,2)
            
            if int(self.labelLeft.text()) < int(self.labelRight.text()):
                self.ResponseType = 'J'
            else:
                self.ResponseType = 'F'
            if size == 1:
                self.labelLeft.setFont(QtGui.QFont("Times",40))
                self.labelRight.setFont(QtGui.QFont("Times",40))
            else:
                self.labelLeft.setFont(QtGui.QFont("Times",80))
                self.labelRight.setFont(QtGui.QFont("Times",80))
            self.rData['type'] = 'LN'
            print('LN')
            
        elif self.listRound[self.iRound] == 'SS':
            num = random.randint(1,4)
            if num == 1:
                self.labelLeft.setText("1")
                self.labelRight.setText("2")
            elif num == 2:
                self.labelLeft.setText("8")
                self.labelRight.setText("9")
            elif num == 3:
                self.labelLeft.setText("2")
                self.labelRight.setText("1")
            elif num == 4:
                self.labelLeft.setText("9")
                self.labelRight.setText("8")
            
            if int(self.labelLeft.text()) > int(self.labelRight.text()):
                self.labelLeft.setFont(QtGui.QFont("Times",80))
                self.labelRight.setFont(QtGui.QFont("Times",40))
                self.ResponseType = 'F'
            else:
                self.labelLeft.setFont(QtGui.QFont("Times",40))
                self.labelRight.setFont(QtGui.QFont("Times",80))
                self.ResponseType = 'J'
            self.rData['type'] = 'SS'
            print('SS')
        elif self.listRound[self.iRound] == 'SD':
            num = random.randint(1,4)
            if num == 1:
                self.labelLeft.setText("1")
                self.labelRight.setText("2")
            elif num == 2:
                self.labelLeft.setText("8")
                self.labelRight.setText("9")
            elif num == 3:
                self.labelLeft.setText("2")
                self.labelRight.setText("1")
            elif num == 4:
                self.labelLeft.setText("9")
                self.labelRight.setText("8")
            
            if int(self.labelLeft.text()) < int(self.labelRight.text()):
                self.labelLeft.setFont(QtGui.QFont("Times",80))
                self.labelRight.setFont(QtGui.QFont("Times",40))
                self.ResponseType = 'J'
            else:
                self.labelLeft.setFont(QtGui.QFont("Times",40))
                self.labelRight.setFont(QtGui.QFont("Times",80))
                self.ResponseType = 'F'
            self.rData['type'] = 'SD'
            print('SD')
        elif self.listRound[self.iRound] == 'SN':
            num = random.randint(1,4)
            if num == 1:
                self.labelLeft.setText("1")
                self.labelRight.setText("2")
            elif num == 2:
                self.labelLeft.setText("8")
                self.labelRight.setText("9")
            elif num == 3:
                self.labelLeft.setText("2")
                self.labelRight.setText("1")
            elif num == 4:
                self.labelLeft.setText("9")
                self.labelRight.setText("8")
            
            if int(self.labelLeft.text()) < int(self.labelRight.text()):
                self.ResponseType = 'J'
            else:
                self.ResponseType = 'F'
                
            size = random.randint(1,2)
            if size == 1:
                self.labelLeft.setFont(QtGui.QFont("Times",40))
                self.labelRight.setFont(QtGui.QFont("Times",40))
            else:
                self.labelLeft.setFont(QtGui.QFont("Times",80))
                self.labelRight.setFont(QtGui.QFont("Times",80))
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
            self.labelFix.setText("结束实验，谢谢参与，\n请按ESC键退出")
            self.labelFix.setFont(QtGui.QFont("宋体",20))
            self.labelFix.adjustSize()
            
            self.labelFix.setStyleSheet("color:black")
            self.labelFix.show()
        #print("blank")
        
        
        self.timer_blank.stop()

        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = StroopChildren()
    main.show()
    sys.exit(app.exec_())
