import sys
from PyQt5 import QtGui, QtCore, QtWidgets
 
class Main(QtWidgets.QMainWindow):
 
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.initUI()
 
    def initUI(self):
 
        self.timer = QtCore.QTimer(self)
 
        self.lcd = QtWidgets.QLCDNumber(self)
        self.lcd.setDigitCount(8)
 
        self.time = QtWidgets.QTimeEdit(self)
        self.timer.timeout.connect(self.Time)
 
        self.set = QtWidgets.QPushButton("Set",self)
        self.set.clicked.connect(self.Set)
 
        self.stop = QtWidgets.QPushButton("Stop",self)
        self.stop.clicked.connect(lambda: self.timer.stop())
 
        grid = QtWidgets.QGridLayout(self)
 
        grid.addWidget(self.lcd,3,0)
        grid.addWidget(self.time,0,0)
        grid.addWidget(self.set,1,0)
        grid.addWidget(self.stop,2,0)
 
        centralwidget = QtWidgets.QWidget()
 
        self.setCentralWidget(centralwidget)
 
        centralwidget.setLayout(grid)
 
#---------Window settings --------------------------------
         
        self.setGeometry(300,300,280,170)
 
    def Set(self):
        global t,h,m,s
         
        t = self.time.time()
        self.lcd.display(t.toString())
 
        self.timer.start(1000)
 
        h = t.hour()
        m = t.minute()
        s = t.second()
 
    def Time(self):
        global t,h,m,s
 
        if s > 0:
            s -=1
        else:
            if m > 0:
                m -= 1
                s = 59
            elif m == 0 and h > 0:
                h -= 1
                m = 59
                s = 59
            else:
                self.timer.stop()
                stop = QtWidgets.QMessageBox.warning(self,"Time is up","Time is up")
 
        time = ("{0}:{1}:{2}".format(h,m,s))
 
        self.lcd.setDigitCount(len(time))
        self.lcd.display(time)
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
