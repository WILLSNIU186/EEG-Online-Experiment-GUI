import numpy as np
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
import os
from threading import Thread
from PyQt5.QtGui import QPixmap
from playsound import playsound
from pycnbi import logger


class TaskManager():
    def onClicked_toolButton_choose_image_task(self):
        """
        Event listener for three dot button next to choose image for task in Experiment Protocal tab
        """
        self.openFileNameDialog_image()

    def onClicked_toolButton_choose_sound_task(self):
        """
        Event listener for three dot button next to choose sound for task in Experiment Protocal tab
        """
        self.openFileNameDialog_sound()

    def onClicked_button_define_task_add(self):
        """
        Event listener for Add button in Task manager in Experimental Protocal tab
        """
        # Add task name and description in table
        exp_task_name = self.ui.lineEdit_define_task.text()
        task_descriptor = self.ui.lineEdit_subject_view_description.text()

        if len(exp_task_name) > 0:
            row_position = self.ui.tableWidget_tasks.rowCount()
            self.ui.tableWidget_tasks.insertRow(row_position)
            self.ui.tableWidget_tasks.setItem(row_position, 0, QTableWidgetItem(exp_task_name))
            self.ui.tableWidget_tasks.setItem(row_position, 1, QTableWidgetItem(task_descriptor))
            self.ui.tableWidget_tasks.setItem(row_position, 2, QTableWidgetItem(self.task_image_path))
            self.ui.tableWidget_tasks.setItem(row_position, 3, QTableWidgetItem(self.task_sound_path))

    def onClicked_button_define_task_done(self):
        """
        Event listener for Done button in Task manager in Experimental protocol tab.
        By clicking Done button, no more new tasks could be added.
        """
        self.task_table, _ = self.get_task_name_table_content()
        self.new_task_table = np.copy(self.task_table)  # initialize new_task_table
        self.ui.groupBox_sequence_manager.setEnabled(True)
        self.ui.groupBox_task_manager.setEnabled(False)
        # print("task name list:\n",self.new_task_list)
        # print("task description list:\n",self.task_descriptor_list)
        # print("task image paths list:\n",self.task_image_path_list)


    def openFileNameDialog_image(self):
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
            self.task_image_path = fileName
        else:
            self.task_image_path = "{}/package/views/icon/blank.jpg".format(os.getcwd())
        self.show_task_instruction_image()

    def openFileNameDialog_sound(self):
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
            self.task_sound_path = fileName
            # self.play_task_sound(self.task_sound_path)
            Thread(target=self.play_task_sound, args=(self.task_sound_path,)).start()
        else:
            self.task_sound_path = " "


    def init_task_name_table(self):
        """
        Initialize task table heade.
        """
        self.ui.tableWidget_tasks.setColumnCount(4)
        self.ui.tableWidget_tasks.setHorizontalHeaderLabels(
            ["Task name", "Task description", "Task image", "Task sound"])



    def show_task_instruction_image(self):
        """
        Show task instruction image in subject view window
        """
        self.ui.label_task_instruction_image.setPixmap(QPixmap(self.task_image_path))

    def play_task_sound(self, sound_path):
        """
        play sound for task instruction
        :param sound_path: .wav sound file directory path
        """
        try:
            # logger.info("Played, sound path: {}".format(sound_path))
            playsound(sound_path)
        except:
            logger.info("sound path: {} not found".format(sound_path))
            self.ui.statusBar.showMessage("sound path not found")