import numpy as np
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
import os
from threading import Thread
from PyQt5.QtGui import QPixmap
from package.entity.base.cue import Cue
import pdb
from playsound import playsound
from pycnbi import logger

class CueManager():
    def onClicked_toolButton_choose_image_cue(self):
        """
        Event listener for three dot button next to choose image for task in Experiment Protocal tab
        """
        self.openFileNameDialog_image_cue()

    def onClicked_toolButton_choose_sound_cue(self):
        """
        Event listener for three dot button next to choose sound for task in Experiment Protocal tab
        """
        self.openFileNameDialog_sound_cue()

    def onClicked_button_define_cue_add(self):
        self.cue = Cue(name = self.ui.lineEdit_define_cue.text(),
                       event_number = int(self.ui.lineEdit_cue_event_number.text()),
                       image = self.cue_image,
                       sound = self.cue_sound)
        duration_text = self.ui.lineEdit_cue_duration.text()
        duration_tuple = tuple(map(int, duration_text.split(' - ')))
        if len(duration_tuple) == 1:
            self.cue.set_duration(duration_tuple[0])
        else:
            self.cue.set_duration(duration_tuple)
        if len(self.cue.name) > 0:
            row_position = self.ui.tableWidget_cue.rowCount()
            self.ui.tableWidget_cue.insertRow(row_position)
            self.ui.tableWidget_cue.setItem(row_position, 0, QTableWidgetItem(self.cue.name))
            self.ui.tableWidget_cue.setItem(row_position, 1, QTableWidgetItem(str(self.cue.event_number)))
            self.ui.tableWidget_cue.setItem(row_position, 2, QTableWidgetItem(str(self.cue.duration)))
            self.ui.tableWidget_cue.setItem(row_position, 3, QTableWidgetItem(self.cue.image))
            self.ui.tableWidget_cue.setItem(row_position, 4, QTableWidgetItem(self.cue.sound))
            self.cue_list.append(self.cue)

    def onClicked_button_define_cue_done(self):
        self.ui.groupBox_cue_manager.setEnabled(False)
        self.ui.groupBox_task_manager.setEnabled(True)


    def init_cue_name_table(self):
        """
        Initialize cue table header.
        """
        self.ui.tableWidget_cue.setColumnCount(5)
        self.ui.tableWidget_cue.setHorizontalHeaderLabels(
            ["Cue name", "event number", "Duration (s)", "image", "sound"])


    def openFileNameDialog_image_cue(self):
        """
        Open file folder to choose task instruction image.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()",
                                                  r"package\views\icon",
                                                  "Image files (*.jpg *.png)", options=options)
        if fileName:
            print(fileName)
            self.cue_image = fileName
            self.show_task_instruction_image_cue()
        else:
            self.cue_image = None


    def show_task_instruction_image_cue(self):
        """
        Show task instruction image in subject view window
        """
        self.ui.label_task_instruction_image_cue.setPixmap(QPixmap(self.cue_image))

    def openFileNameDialog_sound_cue(self):
        """
        Open file folder to choose sound file for task instruction.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()",
                                                  r"package\views\sounds",
                                                  "Audio files (*.mp3 *.wav)", options=options)
        if fileName:
            print(fileName)
            self.cue_sound = fileName
            # self.play_task_sound(self.task_sound_path)
            Thread(target=self.play_sound, args=(self.cue_sound,)).start()
        else:
            self.cue_sound = None