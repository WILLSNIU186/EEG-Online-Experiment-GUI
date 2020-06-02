# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\neurodecode-master\pycnbi\stream_viewer\subjectview.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SV(object):
    def setupUi(self, SV):
        SV.setObjectName("SV")
        SV.resize(737, 480)
        self.centralwidget = QtWidgets.QWidget(SV)
        self.centralwidget.setObjectName("centralwidget")
        self.LBimage = QtWidgets.QLabel(self.centralwidget)
        self.LBimage.setGeometry(QtCore.QRect(90, 10, 561, 431))
        self.LBimage.setText("")
        self.LBimage.setPixmap(QtGui.QPixmap("icon/idle.png"))
        self.LBimage.setObjectName("LBimage")
        SV.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SV)
        self.statusbar.setObjectName("statusbar")
        SV.setStatusBar(self.statusbar)

        self.retranslateUi(SV)
        QtCore.QMetaObject.connectSlotsByName(SV)

    def retranslateUi(self, SV):
        _translate = QtCore.QCoreApplication.translate
        SV.setWindowTitle(_translate("SV", "Subject View"))

#if __name__ == "__main__":
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    SV = QtWidgets.QMainWindow()
#    ui = Ui_SV()
#    ui.setupUi(SV)
#    SV.show()
#    sys.exit(app.exec_())

