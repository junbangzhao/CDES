from PyQt5 import QtWidgets,QtGui,QtCore,Qt
import random

class AttentionNetwork(QtWidgets.QWidget):
    def __init__(self,parent = None):
        QtWidgets.QWidget.__init__(self)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width()/2, screen.height()/2)
        self.move(screen.width()/2-self.width()/2,screen.height()/2-self.height()/2)
        
        #label
        self.labelFix = QtWidgets.QLabel(self)
        self.labelCueU = QtWidgets.QLabel(self)
        self.labelCueD = QtWidgets.QLabel(self)
        self.labelCueC = QtWidgets.QLabel(self)
        self.labelT1 = QtWidgets.QLabel(self)
        self.labelT2 = QtWidgets.QLabel(self)
        self.labelT3 = QtWidgets.QLabel(self)
        self.labelT4 = QtWidgets.QLabel(self)
        self.labelT5 = QtWidgets.QLabel(self)
        
        self.labelGuide = QtWidgets.QLabel(self)
            
        
        
        self.labelTarget = [self.labelT1,self.labelT2,self.labelT3,self.labelT4,self.labelT5]
        self.labelSide = [self.labelT1,self.labelT2,self.labelT4,self.labelT5]
        self.labelCue = [self.labelCueU,self.labelCueD]
        self.PosH = list(range(-2,3,1))
        self.PosV = [-1,1]
        
        #QTimer
        self.timerFix = QtCore.QTimer()
        self.timerFix.timeout.connect(self.tfUpdate)
        
        self.timerCue = QtCore.QTimer()
        self.timerCue.timeout.connect(self.tcUpdate)
        
        self.timerTarget = QtCore.QTimer()
        self.timerTarget.timeout.connect(self.ttUpdate)
        
        self.timerBlank = QtCore.QTimer()
        self.timerBlank.timeout.connect(self.tbUpdate)
        
        self.FixOrder = 0
        self.CuePos = 0
        
        self.RT = QtCore.QElapsedTimer()
        

        
    def showEvent(self,event):
        while True:
            text, ok= QtWidgets.QInputDialog.getText(self, ("实验次数"), ("次数为24的整数倍"), QtWidgets.QLineEdit.Normal, "")
            if not ok:
                quit()
            try:
                self.Round = int(text)
                
                if (self.Round % 24 == 0) and (self.Round > 0):
                    print ("right")
                    break
            except:        
                print("wrong")
        
        
        self.labelGuide.setText("注意网络实验\n\n 如果中间箭头朝左用左手食指按F键，\n如果中间箭头朝右右手食指按J键，\n按Enter键开始")
        self.labelGuide.setFont(QtGui.QFont("宋体",20))
        self.labelGuide.setGeometry(0,0,500,200)
        self.labelGuide.move((self.width() - self.labelGuide.width())/2,(self.height() - self.labelGuide.height())/2)
        self.labelGuide.setAlignment(Qt.Qt.AlignCenter)
        self.labelGuide.show()
        
        
        self.labelFix.setText("+")
        self.labelFix.setAlignment(Qt.Qt.AlignCenter)
        #self.labelFix.setStyleSheet("background-color:red")
        self.labelFix.setFont(QtGui.QFont("Times",40))
        self.labelFix.setGeometry(0,0,80,80)
        self.labelFix.move((self.width()-self.labelFix.width())/2,(self.height()-self.labelFix.height())/2)
        
        self.labelCueC.setText("*")
        self.labelCueC.setAlignment(Qt.Qt.AlignCenter)
        #self.labelCueC.setStyleSheet("background-color:red")
        self.labelCueC.setFont(QtGui.QFont("Times",40))
        self.labelCueC.setGeometry(0,0,80,80)
        self.labelCueC.move((self.width()-self.labelCueC.width())/2,(self.height()-self.labelCueC.height())/2)
        
        for l,p in zip(self.labelCue,self.PosV):
            l.setText("*")
            l.setAlignment(Qt.Qt.AlignCenter)
            #l.setStyleSheet("background-color:red")
            l.setFont(QtGui.QFont("Times",40))
            l.setGeometry(0,0,80,80)
            l.move((self.width()-self.labelFix.width())/2,(self.height()-self.labelFix.height())/2+100*p)
            l.hide()
        
        for l,p in zip(self.labelTarget,self.PosH):
            l.setText(str(p))
            l.setAlignment(Qt.Qt.AlignCenter)
            #l.("background-color:red")
            l.setFont(QtGui.QFont("Times",40))
            l.setGeometry(0,0,80,80)
            l.move((self.width()-l.width())/2 + 100*p,(self.height()-l.height())/2 - 100)
            l.hide()
            
        self.labelFix.hide()
        self.labelCueC.hide()
        self.iRound = 0
        
        self.Order = []
        D = {}

        for l in ['NoCue','CentralCue','DoubleCue','SpatialCue']:
            for m in ['Con','Incon','Neutral']:
                for n in ['Left','Right']:
                    D['cue'] = l
                    D['type'] = m
                    D['dir'] = n
                    self.Order.append(D)
                    D = {}
        random.shuffle(self.Order)
            
            
        self.ResponseData = []
        self.rData = {}
        
        self.bResponse = False
        self.bStart = False
        
        
    def keyPressEvent(self,event):
        if (event.key() == QtCore.Qt.Key_Enter) or (event.key() == QtCore.Qt.Key_Return):
            if not self.bStart :
                self.labelGuide.hide()
                self.timerFix.start(1000)
                self.bStart = True
            else:
                print("Already Start")
        
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
            
        if event.key() == QtCore.Qt.Key_F:
            if self.bResponse:
                self.rData['RT'] = self.RT.elapsed()
                if self.Order[self.iRound]['dir'] == "Left":
                    self.rData['isCorrect'] ='R'
                else:
                    self.rData['isCorrect'] = 'W'
                self.timerBlank.stop()
                self.timerBlank.start(0)
                self.bResponse = False
            else:
                print("Wrong Response")
                
        if event.key() == QtCore.Qt.Key_J:
            if self.bResponse:
                self.rData['RT'] = self.RT.elapsed()
                if self.Order[self.iRound]['dir'] == "Left":
                    self.rData['isCorrect'] = 'W'
                else:
                    self.rData['isCorrect'] =    'R'
                
                self.timerBlank.stop()
                self.timerBlank.start(0)
                self.bResponse = False
            else:
                print("Wrong Response")
    
    def tfUpdate(self):
        self.labelFix.show()
        if self.FixOrder == 0:
            t = random.randint(400,1600)
            self.timerCue.start(t)
        else:
            self.labelCueU.hide()
            self.labelCueD.hide()
            self.labelCueC.hide()
            self.timerTarget.start(450)
            self.FixOrder = 0
            
        self.timerFix.stop()
    
    def ttUpdate(self):        
        if self.CuePos == 0:
            for l,p in zip(self.labelTarget,self.PosH):
                l.move((self.width()-l.width())/2 + 100*p,(self.height()-l.height())/2 - 100)
        else:
            for l,p in zip(self.labelTarget,self.PosH):
                l.move((self.width()-l.width())/2 + 100*p,(self.height()-l.height())/2 + 100)
        
        if self.Order[self.iRound]['dir'] == 'Left':
            print("Left")
            if self.Order[self.iRound]['type'] == 'Con':
                for l,p in zip(self.labelTarget,self.PosH):
                    l.setText('<-')
                    l.show()
                self.rData['type'] = "Congruent"
                print("Congruent")
            elif self.Order[self.iRound]['type'] == 'Incon':
                for l,p in zip(self.labelTarget,self.PosH):
                    l.setText('->')
                    l.show()
                self.labelT3.setText('<-')
                print("Incogruent")
                self.rData['type'] = 'Incongruent'
            elif self.Order[self.iRound]['type'] == 'Neutral':
                self.labelT3.setText('<-')
                self.labelT3.show()
                self.rData['type'] = 'Neutral'
                print("Neutral")
            else: print("Wrong type")

        elif self.Order[self.iRound]['dir'] == 'Right':
            print("Right")
            if self.Order[self.iRound]['type'] == 'Con':
                for l,p in zip(self.labelTarget,self.PosH):
                    l.setText('->')
                    l.show()
                print("Congruent")
                self.rData['type'] = "Congruent"
            elif self.Order[self.iRound]['type'] == 'Incon':
                for l,p in zip(self.labelTarget,self.PosH):
                    l.setText('<-')
                    l.show()
                print("Incongruent")
                self.rData['type'] = "Incongruent"
                self.labelT3.setText('->')
            elif self.Order[self.iRound]['type'] == 'Neutral':
                self.labelT3.setText('->')
                self.labelT3.show()
                print("Neutral")
                self.rData['type'] = "Neutral"
            else: print("Wrong type")
            
        else: print("Wrong Direction")
        
        if self.RT.isValid():
            self.RT.restart()
        else:
            self.RT.start()
        self.bResponse = True
        self.timerBlank.start(1700)
        self.timerTarget.stop()

    def tbUpdate(self):
        for l in self.labelTarget:
            l.hide()
        self.iRound += 1       
        self.labelFix.hide()
        if self.bResponse:
            self.rData['RT'] = 0
            self.rData['isCorrect'] = 'M'
        self.ResponseData.append(self.rData)
        print(self.rData)
        self.rData = {}
        self.bResponse = False
        
        if self.iRound < self.Round:
            self.timerFix.start(1000)
        else:
            file = QtCore.QFile("AttentionNetwork.txt")
            if not file.open(QtCore.QIODevice.WriteOnly or QtCore.QIODevice.Text):
                print("error")
                return 0
            out = QtCore.QTextStream(file)
            out << "No." << "\t" << "isCorrect" << "\t" << "type" << "\t" << "Cue" << '\t' << "RT" << "\r\n"
            for RT in self.ResponseData:
                out << RT['No.'] << "\t" << RT["isCorrect"]<< "\t" << RT["type"] << "\t"  << RT['cue'] << '\t' << RT["RT"] << "\r\n"
            self.labelGuide.setText("结束实验，谢谢参与，\n请按ESC键退出")
            self.labelGuide.setFont(QtGui.QFont("宋体",20))            
            self.labelGuide.setStyleSheet("color:black")
            self.labelGuide.show()
        self.timerBlank.stop()

    def tcUpdate(self):
        print("-----------------------")
        print(self.iRound + 1)
        self.rData['No.'] = self.iRound + 1
        self.CuePos = random.randint(0,1)
        if self.Order[self.iRound]["cue"] == "NoCue":
            print("NoCue")
            self.rData['cue'] = 'NoCue'
        elif self.Order[self.iRound]["cue"] == "CentralCue":
            self.labelFix.hide()
            self.labelCueC.show()
            print("CentralCue")
            self.rData['cue'] = 'Central' 
        elif self.Order[self.iRound]["cue"] == "DoubleCue":
            for l in self.labelCue:
                l.show()
            print("DoubleCue")
            self.rData['cue'] = 'DoubleCue'
        elif self.Order[self.iRound]["cue"] == "SpatialCue":

            if self.CuePos == 0:
                self.labelCueU.show()
            else:
                self.labelCueD.show()
            print("SpatialCue")
            self.rData['cue'] = "SpatialCue"
        if self.CuePos == 0:
            print("CueUP")
        else: print("CueDown")
        self.timerFix.start(150)
        self.FixOrder = 1
        self.timerCue.stop()
    
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = AttentionNetwork()
    main.show()
    sys.exit(app.exec_())