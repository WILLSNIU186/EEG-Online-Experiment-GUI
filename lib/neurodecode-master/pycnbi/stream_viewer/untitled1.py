import sys
from PyQt5 import QtGui, QtCore,QtWidgets
 
s = 0
m = 0
h = 0
 
class Main(QtWidgets.QMainWindow):
 
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.initUI()
 
    def initUI(self):
 
        centralwidget = QtWidgets.QWidget(self)
 
        self.lcd = QtWidgets.QLCDNumber(self)
 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Time)
        
        self.secondtimer = QtCore.QTimer(self)
        self.secondtimer.timeout.connect(self.secondTime)
 
        self.start = QtWidgets.QPushButton("Start",self)
        self.start.clicked.connect(self.Start)
 
        self.stop = QtWidgets.QPushButton("Stop",self)
        self.stop.clicked.connect(lambda: self.timer.stop())
 
        self.reset = QtWidgets.QPushButton("Reset",self)
        self.reset.clicked.connect(self.Reset)
 
        grid = QtWidgets.QGridLayout()
         
        grid.addWidget(self.start,1,0)
        grid.addWidget(self.stop,1,1)
        grid.addWidget(self.reset,1,2)
        grid.addWidget(self.lcd,2,0,1,3)
 
        centralwidget.setLayout(grid)
 
        self.setCentralWidget(centralwidget)
 
#---------Window settings --------------------------------
         
        self.setGeometry(300,300,280,170)
 
    def Reset(self):
        global s,m,h
 
        self.timer.stop()
 
        s = 0
        m = 0
        h = 0
 
        time = "{0}:{1}:{2}".format(h,m,s)
 
        self.lcd.setDigitCount(len(time))
        self.lcd.display(time)
 
    def Start(self):
        global s,m,h
         
        self.timer.start(1000)
        self.secondtimer.start(500)
     
    def Time(self):
        global s,m,h
 
        if s < 59:
            s += 1
        else:
            if m < 59:
                s = 0
                m += 1
            elif m == 59 and h < 24:
                h += 1
                m = 0
                s = 0
            else:
                self.timer.stop()
 
        time = "{0}:{1}:{2}".format(h,m,s)
 
        self.lcd.setDigitCount(len(time))
        self.lcd.display(time)
    
    def secondTime(self):
        print("second timer fired")
def main():
    app = QtWidgets.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()