import numpy as np
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
import os
from threading import Thread
from PyQt5.QtGui import QPixmap
from playsound import playsound
from pycnbi import logger
from package.entity.base.trial import Trial
import pdb

class TaskManager():
    def onClicked_toolButton_choose_image_task(self):
        """
        Event listener for three dot button next to choose image for task in Experiment Protocal tab
        """
        self.openFileNameDialog_image_task()

    def onClicked_toolButton_choose_sound_task(self):
        """
        Event listener for three dot button next to choose sound for task in Experiment Protocal tab
        """
        self.openFileNameDialog_sound_task()

    def onClicked_button_define_task_add(self):
        """
        Event listener for Add button in Task manager in Experimental Protocal tab
        """
        # Add task name and description in table
        self.trial = Trial(name = self.ui.lineEdit_define_task.text(),
                           desc_name = self.ui.lineEdit_subject_view_description.text(),
                           event_number=int(self.ui.lineEdit_task_event_number.text()),
                           cue_list = self.cue_list,
                           image = self.trial_image,
                           sound = self.trial_sound)

        # exp_task_name = self.ui.lineEdit_define_task.text()
        # task_descriptor = self.ui.lineEdit_subject_view_description.text()

        if len(self.trial.name) > 0:
            row_position = self.ui.tableWidget_tasks.rowCount()
            self.ui.tableWidget_tasks.insertRow(row_position)
            self.ui.tableWidget_tasks.setItem(row_position, 0, QTableWidgetItem(self.trial.name))
            self.ui.tableWidget_tasks.setItem(row_position, 1, QTableWidgetItem(str(self.trial.event_number)))
            self.ui.tableWidget_tasks.setItem(row_position, 2, QTableWidgetItem(self.trial.desc_name))
            self.ui.tableWidget_tasks.setItem(row_position, 3, QTableWidgetItem(self.trial.image))
            self.ui.tableWidget_tasks.setItem(row_position, 4, QTableWidgetItem(self.trial.sound))
            self.protocol.add_task(self.trial)

    def onClicked_button_define_task_done(self):
        """
        Event listener for Done button in Task manager in Experimental protocol tab.
        By clicking Done button, no more new tasks could be added.
        """
        self.protocol.finish_adding_task()
        self.ui.groupBox_sequence_manager.setEnabled(True)
        self.ui.groupBox_task_manager.setEnabled(False)
        self.ui.pushButton_save_protocol.setEnabled(True)

        # print("task name list:\n",self.new_task_list)
        # print("task description list:\n",self.task_descriptor_list)
        # print("task image paths list:\n",self.task_image_path_list)


    def openFileNameDialog_image_task(self):
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
            self.trial_image = fileName
            self.show_task_instruction_image()
        else:
            self.trial_image = None

    def openFileNameDialog_sound_task(self):
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
            self.trial_sound = fileName
            # self.play_task_sound(self.task_sound_path)
            Thread(target=self.play_sound, args=(self.trial_sound,)).start()
        else:
            self.trial_sound = None


    def init_task_name_table(self):
        """
        Initialize task table header.
        """
        self.ui.tableWidget_tasks.setColumnCount(5)
        self.ui.tableWidget_tasks.setHorizontalHeaderLabels(
            ["Task name", "event number", "Task description", "Task image", "Task sound"])



    def show_task_instruction_image(self):
        """
        Show task instruction image in subject view window
        """
        self.ui.label_task_instruction_image.setPixmap(QPixmap(self.trial_image))

    def play_sound(self, sound_path):
        """
        play sound for from sound path
        :param sound_path: .wav sound file directory path
        """
        try:
            # logger.info("Played, sound path: {}".format(sound_path))
            playsound(sound_path)
        except:
            logger.info("sound path: {} not found".format(sound_path))
            self.ui.statusBar.showMessage("sound path not found")