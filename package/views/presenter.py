import os
import pdb
import sys
import time
from random import randrange, randint
from threading import Thread

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from playsound import playsound
from pycnbi import logger
from scipy.signal import lfilter

from ..entity.edata.utils import Utils
from ..entity.edata.variables import Variables

DEBUG_TRIGGER = False  # TODO: parameterize
NUM_X_CHANNELS = 16  # TODO: parameterize


class Presenter:
    """
    Presenter manages the real-time data and present them to GUI like oscilloscope.
    This class is a part of MainView class, it is separated from MainView for functionality encapsulation.
    """

    def Update_SV_image(self):
        """ Update subject view GUI visual cues inlcuding Idle, focus, prepare, two, one, task"""
        if self.SV_time % self.cycle_time == 0:
            # print("idle")
            # logger.info('\nidle server clock: {}'.format(self.router.get_server_clock()))
            if self.task_counter < self.new_task_table.shape[0]:
                self.event_timestamp_list.append(
                    [self.event_table_dictionary['Idle'], self.router.get_server_clock()])

            self.SV_window.label_current_trial.setText(str(self.task_counter + 1))
            self.SV_window.label_total_trial.setText(str(self.new_task_table.shape[0]))
            self.set_epoch_number()

            # print("\nTASK COUNTER: ", self.task_counter)
            if self.task_counter > 0:
                # self.update_MRCP_plot()
                # update interval time
                if self.ui.checkBox_randomize_interval_time.isChecked():
                    self.idle_time = randint(1, 6)
                    self.focus_time = self.idle_time + int(self.ui.focusTimeLineEdit.text())
                    self.prepare_time = self.focus_time + int(self.ui.prepareTimeLineEdit.text())
                    self.two_time = self.prepare_time + int(self.ui.twoTimeLineEdit.text())
                    self.one_time = self.two_time + int(self.ui.oneTimeLineEdit.text())
                    self.task_time = self.one_time + int(self.ui.taskTimeLineEdit.text())
                    self.relax_time = self.task_time + 2
                    self.cycle_time = self.relax_time

            self.update_SV_task()
            # self.task_counter += 1

            # Idle
            # self.SV_window.LBimage.setPixmap(QtGui.QPixmap("%s/package/views/icon/idle.png" % os.getcwd()))
            self.SV_window.label.setStyleSheet("color: green;")
            self.SV_window.label.setText("IDLE")

        elif self.SV_time % self.cycle_time == self.idle_time:
            # print("focus")
            # logger.info('\nfocus server clock: %s' % self.router.get_server_clock())
            self.event_timestamp_list.append(
                [self.event_table_dictionary['Focus'], self.router.get_server_clock()])
            # Focus
            # self.SV_window.LBimage.setPixmap(QtGui.QPixmap("%s/package/views/icon/focus.png" % os.getcwd()))
            self.SV_window.label.setStyleSheet("color: blue;")
            self.SV_window.label.setText("FOCUS")
        elif self.SV_time % self.cycle_time == self.focus_time:
            # print("prepare")
            # logger.info('\nprepare server clock: %s' % self.router.get_server_clock())
            self.event_timestamp_list.append(
                [self.event_table_dictionary['Prepare'], self.router.get_server_clock()])
            # Prepare
            # self.SV_window.LBimage.setPixmap(QtGui.QPixmap("%s/package/views/icon/prepare.png" % os.getcwd()))
            self.SV_window.label.setStyleSheet("color: black;")
            self.SV_window.label.setText("PREPARE")
        elif self.SV_time % self.cycle_time == self.prepare_time:
            # print("two")
            # Two
            # logger.info('\ntwo server clock: %s' % self.router.get_server_clock())
            self.event_timestamp_list.append(
                [self.event_table_dictionary['Two'], self.router.get_server_clock()])
            # self.SV_window.LBimage.setPixmap(QtGui.QPixmap("%s/package/views/icon/two.png" % os.getcwd()))
            self.SV_window.label.setText("TWO")
        elif self.SV_time % self.cycle_time == self.two_time:
            # print("one")
            # One
            # logger.info('\none server clock: %s' % self.router.get_server_clock())
            self.event_timestamp_list.append(
                [self.event_table_dictionary['One'], self.router.get_server_clock()])
            # self.SV_window.LBimage.setPixmap(QtGui.QPixmap("%s/package/views/icon/one.png" % os.getcwd()))
            self.SV_window.label.setText("ONE")
        elif self.SV_time % self.cycle_time == self.one_time:
            # print("task")
            # Task
            # logger.info('\ntask server clock: %s' % self.router.get_server_clock())
            # self.event_timestamp_list.append(
            #     [self.event_table_dictionary[self.new_task_table[self.task_counter - 1][0]],
            #      self.router.get_server_clock()])
            self.event_timestamp_list.append(
                [self.event_table_dictionary[self.new_task_table[self.task_counter][0]],
                 self.router.get_server_clock()])
            # self.SV_window.LBimage.setPixmap(QtGui.QPixmap("%s/package/views/icon/task.png" % os.getcwd()))
            self.SV_window.label.setStyleSheet("color: red;")
            self.SV_window.label.setText("TASK")
        elif self.SV_time % self.cycle_time == self.task_time:
            # print("relax")
            # relax
            # self.SV_window.LBimage.setPixmap(QtGui.QPixmap("%s/package/views/icon/idle.png" % os.getcwd()))
            self.SV_window.label.setStyleSheet("color: green;")
            self.SV_window.label.setText("IDLE")
            self.SV_time = -2



        elif self.SV_time % self.cycle_time == self.task_time + 1:
            self.update_MRCP_plot()
            # add task counter and check for break
            # if self.task_counter < self.new_task_table.shape[0]:
            self.task_counter += 1
            self.break_trial_number = int(self.ui.lineEdit_break_trial_number.text())
            if self.task_counter % self.break_trial_number == 0 and self.task_counter != 0:
                # self.window.hide()
                self.is_experiment_on = False
            if self.task_counter >= self.new_task_table.shape[0]:
                logger.info('SV stopped')
                self.stop_SV()

        self.SV_time += 1

    def update_SV_task(self):
        """ Update task instruction image, task description and task sound on subject view GUI"""
        # Update SV UI according to task list
        if self.task_counter < self.new_task_table.shape[0]:
            self.SV_window.label_task_content.setText(self.new_task_table[self.task_counter][1])
            self.SV_window.label_instruction_image.setPixmap(QtGui.QPixmap(self.new_task_table[self.task_counter][2]))
            # self.play_task_sound(self.new_task_table[self.task_counter][3])
            Thread(target=self.play_task_sound, args=(self.new_task_table[self.task_counter][3],)).start()
        else:
            self.stop_SV()

    def stop_SV(self):
        """ Stop subject view window updating when tasks finished"""
        self.is_experiment_on = False
        # self.window.hide()
        self.ui.statusBar.showMessage("Tasks finished")
        try:
            self.ui.label_content_available_temp.setText(
                "{} - {}".format(self.temp_counter_list[0], self.temp_counter_list[-1]))
            self.ui.label_content_Disp_temp.setText(
                "{} - {}".format(self.temp_counter_list[0], self.temp_counter_list[-1]))
            self.ui.label_content_current_temp.setText(" ")
        except:
            logger.info('MRCP template display went wrong, but this does not affect data saving, please be patient ...')

    def Time(self):
        """
        Call update subject view window image if task button clicked and display timer on experimenter
        GUI.
        """
        os_time = time.time()
        self.os_time_list.append(os_time)
        if self.is_experiment_on:
            self.Update_SV_image()
        # Variables.add_one_run_time_counter()
        # time_show = Variables.get_run_time_counter()
        self.time_show += 1
        self.ui.lcdNumber_timer.display(self.time_show)

    def get_task_name_table_content(self):
        """
        Get task name, task description, image path and sound path from task name table in experimenter GUI
        :return: lists of table content
        """
        self.task_list = []
        self.task_descriptor_list = []
        self.task_image_path_list = []
        self.task_sound_path_list = []
        task_table = np.ndarray([])
        task_table_list = []
        for i in range(self.ui.tableWidget_tasks.rowCount()):
            self.task_list.append(self.ui.tableWidget_tasks.item(i, 0).text())
            self.task_descriptor_list.append(self.ui.tableWidget_tasks.item(i, 1).text())
            self.task_image_path_list.append(self.ui.tableWidget_tasks.item(i, 2).text())
            self.task_sound_path_list.append(self.ui.tableWidget_tasks.item(i, 3).text())
        task_table_list.append(self.task_list)
        task_table_list.append(self.task_descriptor_list)
        task_table_list.append(self.task_image_path_list)
        task_table_list.append(self.task_sound_path_list)
        task_table = np.c_[np.asarray(self.task_list),
                           np.asarray(self.task_descriptor_list),
                           np.asarray(self.task_image_path_list),
                           np.asarray(self.task_sound_path_list)]
        print("tasks list:\n", task_table)
        task_table_list = np.transpose(np.asarray(task_table_list))
        return task_table, task_table_list

    def show_task_instruction_image(self):
        """
        Show task instruction image in subject view window
        """
        self.ui.label_task_instruction_image.setPixmap(QtGui.QPixmap(self.task_image_path))

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

    def openFileNameDialog_protocol(self):
        """
        Open foldre to choose saved experimental protocal.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()",
                                                  r"experimental_protocols",
                                                  "csv files (*.csv *.txt)", options=options)
        if fileName:
            self.protocol_path = fileName
            self.load_protocol()
        else:
            self.protocol_path = " "

    def load_protocol(self):
        """
        Load existing experimental protocal.
        """
        loaded_task_table = Utils.read_protocol_csv(self.protocol_path)
        self.ui.tableWidget_tasks.setRowCount(loaded_task_table.shape[0])
        for i in range(loaded_task_table.shape[0]):
            for n in range(loaded_task_table.shape[1]):
                print(type(loaded_task_table[i][n]))
                if type(loaded_task_table[i][n]) == float:
                    loaded_task_table[i][n] = ''
            self.ui.tableWidget_tasks.setItem(i, 0, QTableWidgetItem(loaded_task_table[i][0]))
            self.ui.tableWidget_tasks.setItem(i, 1, QTableWidgetItem(loaded_task_table[i][1]))
            self.ui.tableWidget_tasks.setItem(i, 2, QTableWidgetItem(loaded_task_table[i][2]))
            self.ui.tableWidget_tasks.setItem(i, 3, QTableWidgetItem(loaded_task_table[i][3]))
        self.task_table, _ = self.get_task_name_table_content()
        self.new_task_table = np.copy(self.task_table)  # initialize new_task_table
        self.ui.groupBox_sequence_manager.setEnabled(True)
        self.ui.groupBox_task_manager.setEnabled(True)

    def saveFileNameDialog_protocol(self):
        """
        Save current tasks listed in the task table to an experimental protocal file.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()",
                                                  r"experimental_protocols",
                                                  "csv files (*.csv)", options=options)
        if fileName:
            print(fileName)
            Utils.save_protocol_to_csv(self.protocol, fileName)

    def choose_base_folder(self):
        """
        Choose directory to save recording files.
        :returns: directory path
        """
        dir_name = QFileDialog.getExistingDirectory(self, "",
                                                    r"D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\records",
                                                    QFileDialog.ShowDirsOnly)
        if dir_name:
            print(dir_name)
        return dir_name

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
        # QtMultimedia.QSound.play(sound_path)

    def init_task_name_table(self):
        """
        Initialize task table heade.
        """
        self.ui.tableWidget_tasks.setColumnCount(4)
        self.ui.tableWidget_tasks.setHorizontalHeaderLabels(
            ["Task name", "Task description", "Task image", "Task sound"])

    def init_table_file_path(self):
        """
        Initialize file path table in Event and File Management tab
        """
        self.ui.tableWidget_file_path.setColumnCount(2)
        self.ui.tableWidget_file_path.setHorizontalHeaderLabels(["File name", "File path"])


    def update_table_file_path(self):
        """
        Update content in File Path table.
        """
        self.ui.tableWidget_file_path.setRowCount(5)
        self.ui.tableWidget_file_path.setItem(0, 0, QTableWidgetItem("subject.txt"))
        self.ui.tableWidget_file_path.setItem(0, 1, QTableWidgetItem(self.subject_file_path))
        self.ui.tableWidget_file_path.setItem(1, 0, QTableWidgetItem("event.csv"))
        self.ui.tableWidget_file_path.setItem(1, 1, QTableWidgetItem(self.event_file_path))
        self.ui.tableWidget_file_path.setItem(2, 0, QTableWidgetItem("mrcp_template.csv"))
        self.ui.tableWidget_file_path.setItem(2, 1, QTableWidgetItem(self.mrcp_template_file_path))
        self.ui.tableWidget_file_path.setItem(3, 0, QTableWidgetItem("raw_eeg.csv"))
        self.ui.tableWidget_file_path.setItem(3, 1, QTableWidgetItem(Variables.get_raw_eeg_file_path()))
        self.ui.tableWidget_file_path.setItem(4, 0, QTableWidgetItem("raw_mrcp.csv"))
        self.ui.tableWidget_file_path.setItem(4, 1, QTableWidgetItem(self.raw_mrcp_file_path))


    def get_event_number_table_content(self):
        """
        Get task name and event number from event number table.
        """
        self.event_number_list = []
        self.event_name_list = []
        for i in range(self.ui.tableWidget_task_event_number.rowCount()):
            self.event_name_list.append(self.ui.tableWidget_task_event_number.item(i, 0).text())
            self.event_number_list.append(int(self.ui.tableWidget_task_event_number.item(i, 1).text()))
        self.event_table_dictionary = dict(zip(self.event_name_list, self.event_number_list))
        return self.event_table_dictionary
        # print("TTTTTTTTTTTTTTTTTTTTTTTTTTTT\n", self.event_table_dictionary)


    def init_task_event_number_table(self):
        """
        Initialize the header of event number table.
        """
        self.ui.tableWidget_task_event_number.setColumnCount(2)
        self.ui.tableWidget_task_event_number.setHorizontalHeaderLabels(["Task name", "Event number"])


    def paintEvent(self, e):
        """
        Paint the oscilloscope
        """
        # Distinguish between paint events from timer and event QT widget resizing, clicking etc (sender is None)
        # We should only paint when the timer triggered the event.
        # Just in case, there's a flag to force a repaint even when we shouldn't repaint
        sender = self.sender()
        if 'force_repaint' not in self.__dict__.keys():
            logger.warning('force_repaint is not set! Is it a Qt bug?')
            self.force_repaint = 0
        if (sender is None) and (not self.force_repaint):
            pass
        else:
            self.force_repaint = 0
            qp = QPainter()
            qp.begin(self)
            # Update the interface
            self.paintInterface(qp)
            qp.end()


    def find_epoch_number(self):
        """
        Get the current epoch number in its own class to show it in task monitor in Online Experiment tab
        :return the index of this epoch in its own class

        """
        current_task = self.new_task_list[self.task_counter]
        return np.where(np.asarray(self.new_task_list) == current_task)[0].tolist().index(self.task_counter)


    def set_epoch_number(self):
        """
        Display current task epoch number in its own task in task monitor in Online Experiment tab
        """
        current_task = self.new_task_list[self.task_counter]
        row_number = self.unique_task_list.tolist().index(current_task)
        epoch_number = self.find_epoch_number()
        self.ui.tableWidget_class_epoch_counter.setItem(row_number, 1, QTableWidgetItem(str(epoch_number + 1)))
        self.ui.tableWidget_class_epoch_counter.viewport().update()
        self.ui.tableWidget_class_epoch_counter.selectRow(row_number)


    def init_class_epoch_counter_table(self):
        """
        Initialize table header for Task Monitor table
        """
        self.ui.tableWidget_class_epoch_counter.setColumnCount(2)
        self.ui.tableWidget_class_epoch_counter.setHorizontalHeaderLabels(["Task name", "current no."])


    def init_class_bad_epoch_table(self):
        """
        Initialize table header for bad epochs recording table in task monitor
        """
        self.ui.tableWidget_bad_epoch.setColumnCount(2)
        self.ui.tableWidget_bad_epoch.setHorizontalHeaderLabels(["Task name", "bad epochs"])


    def paintInterface(self, qp):
        """
        Update stuff on the interface. Only graphical updates should be added here
        """
        for x in range(0, len(self.channels_to_show_idx)):
            self.curve_eeg[x].setData(x=self.x_ticks,
                                      y=self.data_plot[:, self.channels_to_show_idx[x]] - x * self.scale)

        # Update events
        for x in range(0, len(self.events_detected), 2):
            xh = int(x / 2)
            self.events_curves[xh].setData(x=np.array(
                [self.x_ticks[self.events_detected[x]],
                 self.x_ticks[self.events_detected[x]]]), y=np.array(
                [+1.5 * self.scale,
                 -0.5 * self.scale - self.scale * self.config[
                     'eeg_channels']]))
            self.events_text[xh].setPos(self.x_ticks[self.events_detected[x]],
                                        self.scale)


    def update_plot_scale(self, new_scale):
        """
        Update channel scales when changed
        :param: new_scale: new scale of data (mv)
        """
        if (new_scale < 1):
            new_scale = 1
        # commented out by dbdq.
        # else:
        #	new_scale = new_scale - new_scale%10

        self.scale = new_scale

        # Y Tick labels
        values = []
        for x in range(0, len(self.channels_to_show_idx)):
            values.append((-x * self.scale,
                           self.channel_labels[self.channels_to_show_idx[x]]))

        values_axis = []
        values_axis.append(values)
        values_axis.append([])
        # print("value: ", values)
        # print("value axis ", values_axis)

        self.main_plot_handler.getAxis('left').setTicks(values_axis)

        self.main_plot_handler.setRange(
            yRange=[+self.scale, -self.scale * len(self.channels_to_show_idx)])

        # print(self.scale)
        # print(-self.scale * len(self.channels_to_show_idx))

        self.main_plot_handler.setLabel(axis='left',
                                        text='Scale (uV): ' + str(self.scale))
        self.trigger_help()

        # We force an immediate repaint to avoid "shakiness".
        if (not self.stop_plot):
            self.force_repaint = 1
            self.repaint()


    def update_plot_seconds(self, new_seconds):
        """
        Update the time length displayed in oscilloscope
        :param new_seconds: time length to display (s)
        """
        if (new_seconds != self.seconds_to_show) and (new_seconds > 0) and (
                new_seconds < 100):
            self.ui.spinBox_time.setValue(new_seconds)
            self.main_plot_handler.setRange(xRange=[0, new_seconds])
            self.x_ticks = np.zeros(self.config['sf'] * new_seconds);
            for x in range(0, self.config['sf'] * new_seconds):
                self.x_ticks[x] = (x * 1) / float(self.config['sf'])

            if (new_seconds > self.seconds_to_show):
                padded_signal = np.zeros((self.config['sf'] * new_seconds,
                                          self.config['eeg_channels']))
                padded_signal[padded_signal.shape[0] - self.data_plot.shape[0]:,
                :] = self.data_plot
                for x in range(0, len(self.events_detected), 2):
                    self.events_detected[x] += padded_signal.shape[0] - \
                                               self.data_plot.shape[0]
                self.data_plot = padded_signal

            else:
                for x in range(0, len(self.events_detected), 2):
                    self.events_detected[x] -= self.data_plot.shape[0] - \
                                               self.config['sf'] * new_seconds
                self.data_plot = self.data_plot[
                                 self.data_plot.shape[0] - self.config['sf'] * new_seconds:, :]

            self.seconds_to_show = new_seconds
            self.trigger_help()

            # We force an immediate repaint to avoid "shakiness".
            if (not self.stop_plot):
                self.force_repaint = 1
                self.repaint()

        #
        # 	Add an event to the scope
        #


    def addEventPlot(self, event_name, event_id):
        """
        Add marker during recording. Note: marker not supported in current version
        """
        if (event_name == "TID"):
            color = pg.mkColor(0, 0, 255)
        elif (event_name == "KEY"):
            color = pg.mkColor(255, 0, 0)
        elif (event_name == "LPT"):
            color = pg.mkColor(0, 255, 0)
        else:
            color = pg.mkColor(255, 255, 255)

        self.events_detected.append(self.data_plot.shape[0] - 1)
        self.events_detected.append(event_id)
        self.events_curves.append(self.main_plot_handler.plot(pen=color,
                                                              x=np.array([self.x_ticks[-1], self.x_ticks[-1]]),
                                                              y=np.array(
                                                                  [+1.5 * self.scale,
                                                                   -1.5 * self.scale * self.config['eeg_channels']])))
        # text = pg.TextItem(event_name + "(" + str(self.events_detected[-1]) + ")", anchor=(1.1,0), fill=(0,0,0), color=color)
        text = pg.TextItem(str(self.events_detected[-1]), anchor=(1.1, 0),
                           fill=(0, 0, 0), color=color)
        text.setPos(self.x_ticks[-1], self.scale)
        self.events_text.append(text)
        self.main_plot_handler.addItem(self.events_text[-1])



    def update_title_scope(self):
        """
        Updates the title shown in the scope
        """
        if (hasattr(self, 'main_plot_handler')):
            self.main_plot_handler.setTitle(
                title='TLK: ' + self.bool_parser[self.show_TID_events] +
                      self.bool_parser[self.show_LPT_events] + self.bool_parser[
                          self.show_Key_events] + ', CAR: ' + self.bool_parser[
                          self.apply_car] + ', BP: ' + self.bool_parser[
                          self.apply_bandpass] + ' [' + str(
                    self.ui.doubleSpinBox_hp.value()) + '-' + str(
                    self.ui.doubleSpinBox_lp.value()) + '] Hz')
            # ', BP: ' + self.bool_parser[self.apply_bandpass] + (' [' + str(self.doubleSpinBox_hp.value()) + '-' + str(self.doubleSpinBox_lp.value()) + '] Hz' if self.apply_bandpass else ''))


    def update_loop(self):
        """
        Update three parts by real time data: template_buffer, filter displayed signal, ringbuffer.
        This function connects with main timer defined in MainView and is called every 20ms.
        """

        os_time = time.time()
        self.os_time_list1.append(os_time)
        #  Sharing variable to stop at the GUI level
        if not self.state.value:
            logger.info('Viewer stopped')
            sys.exit()

        try:
            self.read_eeg()  # Read new chunk
            if len(self.ts_list) > 0:
                self.update_template_buffer()
                self.filter_signal()  # Filter acquired data
                self.update_ringbuffers()  # Update the plotting infor
                if (not self.stop_plot):
                    self.repaint()  # Call paint event
        except Exception as e:
            logger.exception('Exception. Dropping into a shell.')
            print(str(e))
        finally:
            pass


    def read_eeg(self):
        """
        Get real time data from LSL
        """
        try:
            # data, self.ts_list= self.sr.inlets[0].pull_chunk(max_samples=self.config['sf']) # [frames][channels]
            data, self.ts_list = self.sr.acquire("scope using", blocking=False)

            # print("TTTTTTTTTTTTTTTTTTTTT\ndata = ", data)
            # TODO: check and change to these two lines
            # self.sr.acquire(blocking=False, decim=DECIM)
            # data, self.ts_list = self.sr.get_window()

            if len(self.ts_list) == 0:
                # self.eeg= None
                # self.tri= None
                return

            n = self.config['eeg_channels']
            # print('eeg channels: ', n)
            '''
            x= np.array( data )
            trg_ch= self.config['tri_channels']
            if trg_ch is not None:
                self.tri= np.reshape( x[:,trg_ch], (-1,1) ) # samples x 1
            self.eeg= np.reshape( x[:,self.sr.eeg_channels], (-1,n) ) # samples x channels
            '''
            trg_ch = self.config['tri_channels']
            if trg_ch is not None:
                self.tri = np.reshape(data[:, trg_ch], (-1, 1))  # samples x 1
            self.eeg = np.reshape(data[:, self.sr.eeg_channels],
                                  (-1, n))  # samples x channels
            # print("TTTTTTTTTTTTTTTTTTTTT\ndata = ", self.eeg)
            if DEBUG_TRIGGER:
                # show trigger value
                try:
                    trg_value = max(self.tri)
                    if trg_value > 0:
                        logger.info('Received trigger %s' % trg_value)
                except:
                    logger.exception('Error! self.tri = %s' % self.tri)

                    # Read exg. self.config.samples*self.config.exg_ch, type float
                    # bexg = np.random.rand( 1, self.config['samples'] * self.config['exg_channels'] )
                    # self.exg = np.reshape(list(bexg), (self.config['samples'],self.config['exg_channels']))
        except WindowsError:
            # print('**** Access violation in read_eeg():\n%s\n%s'% (sys.exc_info()[0], sys.exc_info()[1]))
            pass
        except:
            logger.exception()
            # pdb.set_trace()


    def filter_signal(self):
        """
        Apply BPF and notch filters to displayed signal
        """

        self.channels_to_filter = list(range(len(self.channel_labels)))

        if self.ui.checkBox_change_filter.isChecked():
            self.channels_to_refilter = []
            self.sub_channel_names = self.read_sub_channel_names()
            for sub_channel_name in self.sub_channel_names:
                channel_to_refilter = self.channel_labels.tolist().index(sub_channel_name)
                self.channels_to_refilter.append(channel_to_refilter)
                self.channels_to_filter.remove(channel_to_refilter)

            if (self.apply_bandpass):
                for x in self.channels_to_refilter:
                    self.eeg[:, x], self.zi_bandpass_scope_refilter[:, x] = lfilter(self.b_bandpass_scope_refilter,
                                                                                    self.a_bandpass_scope_refilter,
                                                                                    self.eeg[:, x], -1,
                                                                                    self.zi_bandpass_scope_refilter[:,
                                                                                    x])

            if (self.apply_notch):
                for x in self.channels_to_refilter:
                    self.eeg[:, x], self.zi_notch_scope_refilter[:, x] = lfilter(self.b_notch_scope_refilter,
                                                                                 self.a_notch_scope_refilter,
                                                                                 self.eeg[:, x], -1,
                                                                                 self.zi_notch_scope_refilter[:, x])

        if (self.apply_bandpass):
            for x in self.channels_to_filter:
                self.eeg[:, x], self.zi_bandpass_scope[:, x] = lfilter(self.b_bandpass_scope, self.a_bandpass_scope,
                                                                       self.eeg[:, x], -1, self.zi_bandpass_scope[:, x])

        if (self.apply_notch):
            for x in self.channels_to_filter:
                self.eeg[:, x], self.zi_notch_scope[:, x] = lfilter(self.b_notch_scope, self.a_notch_scope,
                                                                    self.eeg[:, x], -1, self.zi_notch_scope[:, x])

        # We only apply CAR if selected AND there are at least 2 channels. Otherwise it makes no sense
        if (self.apply_car) and (len(self.channels_to_show_idx) > 1):
            self.eeg = np.dot(self.matrix_car, np.transpose(self.eeg))
            self.eeg = np.transpose(self.eeg)


    def update_template_buffer(self):
        """
        Update buffer for drawing online MRCP template. Low pass filter followed by high pass filter are
        applied to the buffer.
        """
        self.template_buffer = np.roll(self.template_buffer, -len(self.ts_list), 0)
        current_chunck = np.copy(self.eeg)

        low_pass_data_in = np.transpose(current_chunck)

        low_pass_data_out, self.initial_condition_list_lp = Utils.apply_filter(self.b_lp, self.a_lp, low_pass_data_in,
                                                                               self.initial_condition_list_lp)

        high_pass_data_in = low_pass_data_out

        high_pass_data_out, self.initial_condition_list_hp = Utils.apply_filter(self.b_hp, self.a_hp, high_pass_data_in,
                                                                                self.initial_condition_list_hp)

        # print('\nhigh pass data out size: ', high_pass_data_out.shape)
        self.template_buffer[-len(self.ts_list):, :] = np.transpose(high_pass_data_out)


    def read_template_buffer(self):
        """
        Get bandpassed real time template buffer
        """
        pre_data_in = np.copy(self.template_buffer[- 5 * int(self.sr.sample_rate):, :])
        pre_data_in = np.copy(pre_data_in)
        print('pre data in shape: ', pre_data_in.shape)
        return pre_data_in


    def read_sub_channel_names(self):
        """
        Read channel names typed in Sub Channel Manager in Oscilloscope tab and apply filter or scaler later
        """
        str_sub_channel = self.ui.lineEdit_subchannel_names.text()
        sub_channel_names = str_sub_channel.split()
        return sub_channel_names


    def update_ringbuffers(self):
        """
        Update selected channels scale
        """
        # update single channel scale
        # print("single channel scale: ", self.single_channel_scale)
        channel_to_scale = self.channel_to_scale_column_index * 16 + self.channel_to_scale_row_index
        if self.ui.checkBox_change_scale.isChecked():
            self.ui.statusBar.showMessage("Use UP and Down keys in keyboard to control scale")
            self.channels_to_scale = []
            self.sub_channel_names = self.read_sub_channel_names()
            for sub_channel_name in self.sub_channel_names:
                channel_to_scale = self.channel_labels.tolist().index(sub_channel_name)
                self.channels_to_scale.append(channel_to_scale)
            self.eeg[:, self.channels_to_scale] = self.eeg[:, self.channels_to_scale] * self.single_channel_scale

        # We have to remove those indexes that reached time = 0

        self.data_plot = np.roll(self.data_plot, -len(self.ts_list), 0)
        self.data_plot[-len(self.ts_list):, :] = self.eeg

        delete_indices_e = []
        delete_indices_c = []
        for x in range(0, len(self.events_detected), 2):
            xh = int(x / 2)
            self.events_detected[x] -= len(self.ts_list)  # leeq
            if (self.events_detected[x] < 0) and (not self.stop_plot):
                delete_indices_e.append(x)
                delete_indices_e.append(x + 1)
                delete_indices_c.append(xh)
                self.events_curves[xh].clear()
                self.main_plot_handler.removeItem(self.events_text[xh])

        self.events_detected = [i for j, i in enumerate(self.events_detected) if
                                j not in delete_indices_e]
        self.events_curves = [i for j, i in enumerate(self.events_curves) if
                              j not in delete_indices_c]
        self.events_text = [i for j, i in enumerate(self.events_text) if
                            j not in delete_indices_c]

        # Find LPT events and add them
        if (self.show_LPT_events) and (not self.stop_plot):
            for x in range(len(self.tri)):
                tri = int(self.tri[x])
                if tri != 0 and (tri > self.last_tri):
                    self.addEventPlot("LPT", tri)
                    logger.info('Trigger %d received' % tri)
                self.last_tri = tri

        # Online Experiment


    def set_MRCP_window_size(self, MRCP_window_size):
        """
        Set the time length of MRCP template displayed in Online Experiment tab
        """
        self.MRCP_window_size = MRCP_window_size


    def update_MRCP_plot(self):
        """
        Update the signal in MRCP template window
        """
        try:
            self.set_MRCP_window_size(5)
            self.raw_trial_MRCP = self.read_template_buffer()
            ch_list = self.channel_labels.tolist()
            lap_ch_list = [ch_list.index(self.ui.lineEdit_lap_central.text()),
                           ch_list.index(self.ui.lineEdit_lap_1.text()),
                           ch_list.index(self.ui.lineEdit_lap_2.text()),
                           ch_list.index(self.ui.lineEdit_lap_3.text()),
                           ch_list.index(self.ui.lineEdit_lap_4.text())]
            self.processed_trial_MRCP = Utils.preprocess(self.raw_trial_MRCP, lap_ch_list)
            # save each MRCP and raw signals into total MRCP list
            self.total_trials_MRCP.append(self.processed_trial_MRCP)
            self.total_trials_raw_MRCP.append(np.transpose(self.raw_trial_MRCP).flatten())

            self.line_width = 4
            self.MRCP_plot(self.processed_trial_MRCP)
            self.temp_counter += 1
            self.temp_counter_list.append(self.temp_counter)
            self.ui.label_content_current_temp.setText(str(self.temp_counter))
        except:
            logger.info('MRCP extractor went wrong')
            self.ui.statusBar.showMessage("are lap channels exist?")
        finally:
            pass


    def MRCP_plot(self, about_to_plot_MRCP):
        """
        Plot MRCP template
        :param about_to_plot_MRCP: template buffer extracted from real-time data stream
        :return:
        """
        size = len(about_to_plot_MRCP)
        x = [x / self.sr.sample_rate - 2 for x in list(range(0, size))]
        y = np.transpose(about_to_plot_MRCP)
        R = randrange(255)
        G = randrange(255)
        B = randrange(255)
        self.ui.graphicsView.plot(x, y, pen=pg.mkPen(color=(R, G, B), width=1))



    def plot_display_temp(self):
        """
        Plot certain MRCP templates selected by the text box below the MRCP plot window.
        """
        self.ui.graphicsView.clear()
        # print("display temp list", self.display_temp_list)
        for i in self.display_temp_list:
            self.MRCP_plot(self.total_trials_MRCP[int(i) - 1])


    def get_input_temp(self):
        """
        Choose tpyed templates from the text box below the MRCP plot window.
        """
        self.selected_temp = self.ui.lineEdit_temp_selector.text()
        self.list_selected_temp = self.selected_temp.split()
        # print("list_selected_temp", self.list_selected_temp)
        if len(self.list_selected_temp) == 1:
            self.input_temp_list = [int(x) for x in self.list_selected_temp]
            # self.ui.label_content_Disp_temp.setText("{}".format(self.input_temp_list[0]))

        elif len(self.list_selected_temp) > 1:
            if self.list_selected_temp[1] == "-":
                start_index = int(self.list_selected_temp[0])
                stop_index = int(self.list_selected_temp[-1]) + 1
                self.input_temp_list = list(range(start_index, stop_index))
            else:
                self.input_temp_list = [int(x) for x in self.list_selected_temp]
