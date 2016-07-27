from PyQt5 import QtWidgets,QtGui,QtCore,Qt
import random

class VisualSearch(QtWidgets.QWidget):
    def __init__(self,parent = None):
        QtWidgets.QWidget.__init__(self)
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width()/2, screen.height()/2)
        self.move(screen.width()/2-self.width()/2,screen.height()/2-self.height()/2)
        
        #label
        self.lFix = QtWidgets.QLabel(self)
        self.lTarget = QtWidgets.QLabel(self)
        self.l1 = QtWidgets.QLabel(self)
        self.l2 = QtWidgets.QLabel(self)
        self.l3 = QtWidgets.QLabel(self)
        self.l4 = QtWidgets.QLabel(self)
        self.lGuider = QtWidgets.QLabel(self)
        
        self.label = [self.l1,self.l2,self.l3,self.l4]
        self.labelAll = self.label + [self.lFix,self.lTarget]
        self.number = list(range(9))
        self.alpha = ['A','B','C','D','E','F','G','H','I','J']
        self.character = ["上","木",'土','田','大','工','少','东','人','天']

        hbox = QtWidgets.QHBoxLayout()
        vbox = QtWidgets.QVBoxLayout()
        
        for l in self.label:
            #l.setStyleSheet("background-color:red")
            l.setFont(QtGui.QFont("Times",60))
            l.setAlignment(Qt.Qt.AlignCenter)
        #self.lTarget.setStyleSheet("background-color:red")
        self.lTarget.setFont(QtGui.QFont("Times",60))
        self.lTarget.setAlignment(Qt.Qt.AlignCenter)
        #self.lFix.setStyleSheet("background-color:red")
        self.lFix.setFont(QtGui.QFont("Times",60))
        self.lFix.setAlignment(Qt.Qt.AlignCenter)
        self.lFix.setText("+")
        self.lFix.hide()
        
        
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
        vbox.addWidget(self.lFix)
        vbox.addLayout(hbox)
        vbox.addStretch(2)
        
        self.setLayout(vbox)
        
        
        
        #计时器
        self.timerFix = QtCore.QTimer()
        self.timerFix.timeout.connect(self.tfUpdate)
        
        self.timerTarget = QtCore.QTimer()
        self.timerTarget.timeout.connect(self.ttUpdate)
        
        self.timerBlank = QtCore.QTimer()
        self.timerBlank.timeout.connect(self.tbUpdate)
        
        self.RT = QtCore.QElapsedTimer()
        
    def showEvent(self,event):
        while True:
            text, ok= QtWidgets.QInputDialog.getText(self, ("输入实验次数"), ("次数为6的整数倍"), QtWidgets.QLineEdit.Normal, "")
            if not ok: quit()
            try:
                self.Round = int(text)
                
                if (self.Round % 6 == 0) and (self.Round > 0) :
                    print ("right")
                    break
            except:        
                print("wrong")

        self.iRound = 0
        self.listRound = ['NY','NN','AY','AN','CY','CN']*int(self.Round/6)
        random.shuffle(self.listRound)
        self.bStart = False
        self.bResponse = False
        self.ResponseData = []
        self.rData = {}
        
        self.lGuider.setText("Visual Search\n \n请判断第二行是否有第一行的目标刺激\n如果有左手食指按F键，\n没有则右手食指按J键")
        self.lGuider.adjustSize()
        self.lGuider.setGeometry(0,0,600,300)
        self.lGuider.setAlignment(Qt.Qt.AlignCenter)
        self.lGuider.move((self.width()-self.lGuider.width())/2,(self.height()-self.lGuider.height())/2)
        self.lGuider.setFont(QtGui.QFont("宋体",20))
        self.lGuider.show()
   
    def keyPressEvent(self,event):
        if (event.key() == QtCore.Qt.Key_Enter) or (event.key() == QtCore.Qt.Key_Return):
            self.timerFix.start(1000)
            self.lGuider.hide()
        
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        
        if event.key() == QtCore.Qt.Key_F:
            if(self.bResponse):
                for l in self.labelAll:
                    l.hide()
                self.rData['RT'] = self.RT.elapsed()
                if(self.listRound[self.iRound] == 'AY' or self.listRound[self.iRound] == 'CY' or self.listRound[self.iRound] == 'NY'):
                    self.rData['isCorrect'] = 'R'
                else:
                    self.rData['isCorrect'] = 'W'
                
                self.timerBlank.stop()
                self.timerBlank.start(0)
                self.bResponse = False
        if event.key() == QtCore.Qt.Key_J:
            if(self.bResponse):
                for l in self.labelAll:
                    l.hide()
                self.rData['RT'] = self.RT.elapsed()
                if(self.listRound[self.iRound] == 'AY' or self.listRound[self.iRound] == 'CY' or self.listRound[self.iRound] == 'NY'):
                    self.rData['isCorrect'] = 'W'
                else:
                    self.rData['isCorrect'] = 'R'
                self.timerBlank.stop()
                self.timerBlank.start(0)
                self.bResponse = False
                
    
    
    def tfUpdate(self):
        self.lFix.show()
        self.timerTarget.start(1000)
        self.timerFix.stop()
    
    def ttUpdate(self):
        #self.lFix.hide()
        self.rData['No.'] = self.iRound +1
        print(self.rData['No.'])
        
        random.shuffle(self.number)
        random.shuffle(self.alpha)
        random.shuffle(self.character)
        
        random.shuffle(self.label)
        
        #print(self.number)
        #print(self.alpha)
        #print(self.character)
        
        
        if self.listRound[self.iRound] == 'NY':
            self.lTarget.setText(str(self.number[0]))
            self.label[0].setText(str(self.number[0]))
            self.rData['type'] = 'NY'
            print("NY")
            
        elif self.listRound[self.iRound] == 'NN':
            self.lTarget.setText(str(self.number[0]))
            i = random.randint(1,2)
            if i == 1:
                self.label[0].setText(str(self.character[0]))
            else:
                self.label[0].setText(str(self.alpha[0]))
            self.rData['type'] = 'NN'
            print("NN")
        elif self.listRound[self.iRound] == 'AY':
            self.lTarget.setText(str(self.alpha[0]))
            self.label[0].setText(str(self.alpha[0]))
            self.rData['type'] = 'AY'
            print("AY")
        elif self.listRound[self.iRound] == 'AN':
            self.lTarget.setText(str(self.alpha[0]))
            i = random.randint(1,2)
            if i == 1:
                self.label[0].setText(str(self.character[0]))
            else:
                self.label[0].setText(str(self.number[0]))
            self.rData['type'] = 'AN'
            print("AN")
        elif self.listRound[self.iRound] == 'CY':
            self.lTarget.setText(str(self.character[0]))
            self.label[0].setText(str(self.character[0]))
            self.rData['type'] = 'CY'
            print("CY")
        elif self.listRound[self.iRound] == 'CN':
            self.lTarget.setText(str(self.character[0]))
            i = random.randint(1,2)
            if i == 1:
                self.label[0].setText(str(self.alpha[0]))
            else:
                self.label[0].setText(str(self.number[0]))
            self.rData['type'] = 'CN'
            print("CN")
            
        content = self.number[1:] + self.alpha[1:] + self.character[1:]
        random.shuffle(content)
        #print(content)
        
        for l,c in zip(self.label[1:],content[1:]):
            l.setText(str(c))
        
        for l in self.labelAll:
            l.show()        
        
        if self.RT.isValid():
            self.RT.restart()
        else:
            self.RT.start()
        self.bResponse = True
        self.timerBlank.start(2000)
        self.timerTarget.stop()
        
    def tbUpdate(self):
        
        for l in self.labelAll:
            l.hide()
        self.iRound += 1 
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
            print(self.ResponseData)
            file = QtCore.QFile("VisualSearch.txt")
            if not file.open(QtCore.QIODevice.WriteOnly or QtCore.QIODevice.Text):
                print("error")
                return 0
            out = QtCore.QTextStream(file)
            out << "No." << "\t" << "isCorrect" << "\t" << "type" << "\t" << "RT" << "\r\n"
            for RT in self.ResponseData:
                out << RT['No.'] << "\t" << RT["isCorrect"]<< "\t" << RT["type"] << "\t" << RT["RT"] << "\r\n"
            self.lGuider.setText("结束实验，谢谢参与，请按ESC键退出")
            self.lGuider.setFont(QtGui.QFont("宋体",20))
            self.lGuider.setStyleSheet("color:black")
            self.lGuider.show()
        self.timerBlank.stop()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = VisualSearch()
    main.show()
    sys.exit(app.exec_())