# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'subjectview1.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class SubjectLayout(object):
    def setupUi(self, SV):
        SV.setObjectName("SV")
        SV.resize(722, 586)
        SV.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(SV)
        self.centralwidget.setObjectName("centralwidget")
        self.label_task = QtWidgets.QLabel(self.centralwidget)
        self.label_task.setGeometry(QtCore.QRect(20, 110, 91, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(22)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_task.setFont(font)
        self.label_task.setObjectName("label_task")
        self.label_task_content = QtWidgets.QLabel(self.centralwidget)
        self.label_task_content.setGeometry(QtCore.QRect(20, 220, 701, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_task_content.setFont(font)
        self.label_task_content.setText("")
        self.label_task_content.setAlignment(QtCore.Qt.AlignCenter)
        self.label_task_content.setWordWrap(True)
        self.label_task_content.setObjectName("label_task_content")
        self.label_instruction_image = QtWidgets.QLabel(self.centralwidget)
        self.label_instruction_image.setGeometry(QtCore.QRect(260, 10, 231, 191))
        self.label_instruction_image.setText("")
        self.label_instruction_image.setPixmap(QtGui.QPixmap("../icon/blank.jpg"))
        self.label_instruction_image.setScaledContents(True)
        self.label_instruction_image.setObjectName("label_instruction_image")
        self.label_current_trial = QtWidgets.QLabel(self.centralwidget)
        self.label_current_trial.setGeometry(QtCore.QRect(566, 70, 51, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(22)
        self.label_current_trial.setFont(font)
        self.label_current_trial.setText("")
        self.label_current_trial.setObjectName("label_current_trial")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(630, 70, 16, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(22)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_total_trial = QtWidgets.QLabel(self.centralwidget)
        self.label_total_trial.setGeometry(QtCore.QRect(650, 70, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(22)
        self.label_total_trial.setFont(font)
        self.label_total_trial.setText("")
        self.label_total_trial.setObjectName("label_total_trial")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 300, 701, 211))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(72)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(570, 32, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        SV.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SV)
        self.statusbar.setObjectName("statusbar")
        SV.setStatusBar(self.statusbar)

        self.retranslateUi(SV)
        QtCore.QMetaObject.connectSlotsByName(SV)

    def retranslateUi(self, SV):
        _translate = QtCore.QCoreApplication.translate
        SV.setWindowTitle(_translate("SV", "Subject View"))
        self.label_task.setText(_translate("SV", "Task:"))
        self.label_2.setText(_translate("SV", "/"))
        self.label_3.setText(_translate("SV", "Trial number"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SV = QtWidgets.QMainWindow()
    ui = Ui_SV()
    ui.setupUi(SV)
    SV.show()
    sys.exit(app.exec_())
