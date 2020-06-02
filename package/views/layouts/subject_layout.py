# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'package\views\layouts\subjectview.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class SubjectLayout(object):
    def setupUi(self, SV):
        SV.setObjectName("SV")
        SV.resize(722, 759)
        SV.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(SV)
        self.centralwidget.setObjectName("centralwidget")
        self.LBimage = QtWidgets.QLabel(self.centralwidget)
        self.LBimage.setGeometry(QtCore.QRect(10, 230, 701, 501))
        self.LBimage.setText("")
        self.LBimage.setPixmap(QtGui.QPixmap("package\\views\\layouts\\../../../../Desktop/neurodecode-master/pycnbi/stream_viewer/icon/idle.png"))
        self.LBimage.setScaledContents(True)
        self.LBimage.setObjectName("LBimage")
        self.label_task = QtWidgets.QLabel(self.centralwidget)
        self.label_task.setGeometry(QtCore.QRect(30, 20, 91, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(22)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_task.setFont(font)
        self.label_task.setObjectName("label_task")
        self.label_task_content = QtWidgets.QLabel(self.centralwidget)
        self.label_task_content.setGeometry(QtCore.QRect(120, 30, 281, 151))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_task_content.setFont(font)
        self.label_task_content.setText("")
        self.label_task_content.setWordWrap(True)
        self.label_task_content.setObjectName("label_task_content")
        self.label_instruction_image = QtWidgets.QLabel(self.centralwidget)
        self.label_instruction_image.setGeometry(QtCore.QRect(440, 30, 231, 191))
        self.label_instruction_image.setText("")
        self.label_instruction_image.setPixmap(QtGui.QPixmap("package\\views\\layouts\\../icon/blank.jpg"))
        self.label_instruction_image.setScaledContents(True)
        self.label_instruction_image.setObjectName("label_instruction_image")
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
