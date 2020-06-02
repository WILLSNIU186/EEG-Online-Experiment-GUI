import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtGui import QPainter
from PyQt5 import QtGui, QtCore, QtMultimedia
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from pycnbi import logger
from random import randrange, randint
import pdb
from ..entity.edata.variables import Variables
from ..entity.edata.utils import Utils
import os
from scipy.signal import butter, lfilter, lfiltic, buttord
import math

DEBUG_TRIGGER = False  # TODO: parameterize
NUM_X_CHANNELS = 16  # TODO: parameterize


class Presenter:
    # Main control
    def Update_SV_image(self):
        print("SV time {}".format(self.SV_time))
        print("\nevent list\n", self.event_timestamp_list)
        if self.SV_time % self.cycle_time == 0:
            print("idle")
            logger.info('\nidle LSL clock: {}'.format(self.router.get_LSL_clock() + self.router.get_lsl_offset()))
            if self.task_counter < self.new_task_table.shape[0]:
                self.event_timestamp_list.append(
                    [self.event_table_dictionary[self.new_task_table[self.task_counter][0]],
                     self.router.get_LSL_clock() + self.router.get_lsl_offset()])

            print("\nTASK COUNTER: ", self.task_counter)
            if self.task_counter > 0:
                self.update_MRCP_plot()
                # update interval time
                if self.ui.checkBox_randomize_interval_time.isChecked():
                    self.idle_time = randint(0,6)
                    self.focus_time = self.idle_time + randint(0,2)
                    self.prepare_time = self.focus_time + randint(0,1)
                    self.two_time = self.prepare_time + randint(0,1)
                    self.one_time = self.two_time + int(self.ui.oneTimeLineEdit.text())
                    self.task_time = self.one_time + int(self.ui.taskTimeLineEdit.text())
                    self.relax_time = self.task_time + 2
                    self.cycle_time = self.relax_time

            self.update_SV_task()
            self.task_counter += 1
            # Idle
            self.SV_window.LBimage.setPixmap(QtGui.QPixmap("%s/package/views/icon/idle.png" % os.getcwd()))
        elif self.SV_time % self.cycle_time == self.idle_time:
            print("focus")
            # logger.info('\nfocus LSL clock: %s' % self.router.get_LSL_clock() + self.router.get_lsl_offset())
            self.event_timestamp_list.append(
                [self.event_table_dictionary['Focus'], self.router.get_LSL_clock() + self.router.get_lsl_offset()])
            # Focus
            self.SV_window.LBimage.setPixmap(QtGui.QPixmap("%s/package/views/icon/focus.png" % os.getcwd()))
        elif self.SV_time % self.cycle_time == self.focus_time:
            print("prepare")
            # logger.info('\nprepare LSL clock: %s' % self.router.get_LSL_clock() + self.router.get_lsl_offset())
            self.event_timestamp_list.append(
                [self.event_table_dictionary['Prepare'], self.router.get_LSL_clock() + self.router.get_lsl_offset()])
            # Prepare
            self.SV_window.LBimage.setPixmap(QtGui.QPixmap("%s/package/views/icon/prepare.png" % os.getcwd()))
        elif self.SV_time % self.cycle_time == self.prepare_time:
            print("two")
            # Two
            # logger.info('\ntwo LSL clock: %s' % self.router.get_LSL_clock() + self.router.get_lsl_offset())
            self.event_timestamp_list.append(
                [self.event_table_dictionary['Two'], self.router.get_LSL_clock() + self.router.get_lsl_offset()])
            self.SV_window.LBimage.setPixmap(QtGui.QPixmap("%s/package/views/icon/two.png" % os.getcwd()))
        elif self.SV_time % self.cycle_time == self.two_time:
            print("one")
            # One
            # logger.info('\none LSL clock: %s' % self.router.get_LSL_clock() + self.router.get_lsl_offset())
            self.event_timestamp_list.append(
                [self.event_table_dictionary['One'], self.router.get_LSL_clock() + self.router.get_lsl_offset()])
            self.SV_window.LBimage.setPixmap(QtGui.QPixmap("%s/package/views/icon/one.png" % os.getcwd()))
        elif self.SV_time % self.cycle_time == self.one_time:
            print("task")
            # Task
            # logger.info('\ntask LSL clock: %s' % self.router.get_LSL_clock() + self.router.get_lsl_offset())
            self.event_timestamp_list.append(
                [self.event_table_dictionary['Task'], self.router.get_LSL_clock() + self.router.get_lsl_offset()])
            self.SV_window.LBimage.setPixmap(QtGui.QPixmap("%s/package/views/icon/task.png" % os.getcwd()))
        elif self.SV_time % self.cycle_time == self.task_time:
            print("relax")
            # relax
            self.SV_window.LBimage.setPixmap(QtGui.QPixmap("%s/package/views/icon/idle.png" % os.getcwd()))
            self.SV_time = -2

        self.SV_time += 1

    def update_SV_task(self):
        # Update SV UI according to task list
        if self.task_counter < self.new_task_table.shape[0]:
            self.SV_window.label_task_content.setText(self.new_task_table[self.task_counter][1])
            self.SV_window.label_instruction_image.setPixmap(QtGui.QPixmap(self.new_task_table[self.task_counter][2]))
            self.play_task_sound(self.new_task_table[self.task_counter][3])
        else:
            self.stop_SV()

    def stop_SV(self):
        self.ui.statusBar.showMessage("Tasks finished")
        self.is_experiment_on = False
        self.ui.label_content_available_temp.setText(
            "{} - {}".format(self.temp_counter_list[0], self.temp_counter_list[-1]))
        self.ui.label_content_Disp_temp.setText(
            "{} - {}".format(self.temp_counter_list[0], self.temp_counter_list[-1]))
        self.ui.label_content_current_temp.setText(" ")
        self.event_file_path = Utils.write_data_to_csv(self.event_timestamp_list, 'event.csv')
        # self.save_event_file_to_csv()
        self.window.hide()

    def Time(self):
        if self.is_experiment_on:
            self.Update_SV_image()
        Variables.add_one_run_time_counter()
        time_show = Variables.get_run_time_counter()
        self.ui.lcdNumber_timer.display(time_show)

    def Reset(self):

        self.Runtimer.stop()
        Variables.set_run_time_counter(0)
        time = Variables.get_run_time_counter()
        self.ui.lcdNumber_timer.display(time)

        #
        #	Called by repaint()
        #

    # Subject Information

    # Experimental Protocol

    def get_task_name_table_content(self):
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
        self.ui.label_task_instruction_image.setPixmap(QtGui.QPixmap(self.task_image_path))

    def openFileNameDialog_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Image files (*.jpg *.png)", options=options)
        if fileName:
            print(fileName)
            self.task_image_path = fileName
        else:
            self.task_image_path = "{}/package/views/icon/blank.jpg".format(os.getcwd())
        self.show_task_instruction_image()

    def openFileNameDialog_sound(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Audio files (*.mp3 *.wav)", options=options)
        if fileName:
            print(fileName)
            self.task_sound_path = fileName
            self.play_task_sound(self.task_sound_path)
        else:
            self.task_sound_path = " "

    def openFileNameDialog_protocol(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "csv files (*.csv *.txt)", options=options)
        if fileName:
            self.protocol_path = fileName
            self.load_protocol()
        else:
            self.protocol_path = " "

    def load_protocol(self):
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
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "csv files (*.csv)", options=options)
        if fileName:
            print(fileName)
            Utils.save_protocol_to_csv(self.protocol, fileName)

    def play_task_sound(self, sound_path):
        logger.info("Played")
        QtMultimedia.QSound.play(sound_path)


    def init_task_name_table(self):
        self.ui.tableWidget_tasks.setColumnCount(4)
        self.ui.tableWidget_tasks.setHorizontalHeaderLabels(
            ["Task name", "Task description", "Task image", "Task sound"])


    def init_table_file_path(self):
        self.ui.tableWidget_file_path.setColumnCount(2)
        self.ui.tableWidget_file_path.setHorizontalHeaderLabels(["File name", "File path"])

    def update_table_file_path(self):
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

    # Event Management

    def get_event_number_table_content(self):
        self.event_number_list = []
        self.event_name_list = []
        for i in range(self.ui.tableWidget_task_event_number.rowCount()):
            self.event_name_list.append(self.ui.tableWidget_task_event_number.item(i, 0).text())
            self.event_number_list.append(int(self.ui.tableWidget_task_event_number.item(i, 1).text()))
        self.event_table_dictionary = dict(zip(self.event_name_list, self.event_number_list))
        # print("TTTTTTTTTTTTTTTTTTTTTTTTTTTT\n", self.event_table_dictionary)

    def init_task_event_number_table(self):
        self.ui.tableWidget_task_event_number.setColumnCount(2)
        self.ui.tableWidget_task_event_number.setHorizontalHeaderLabels(["Task name", "Event number"])

    # Oscilloscope
    def paintEvent(self, e):
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

        #
        #	Update stuff on the interface. Only graphical updates should be added here
        #

    def paintInterface(self, qp):
        # only works for 16 channel single channel rescale

            # print("I RUNNNNNNNNNNN")
            # print("single scale ", self.single_channel_scale)
            # print("scale ", self.scale)

            # for x in range(0, len(self.channels_to_show_idx)):
            #     if self.channels_to_show_idx[x] == self.channel_to_scale_row_index:
            #         print("single scale: ", self.single_channel_scale)
            #         print(type(self.data_plot))
            #         self.data_plot[:, self.channels_to_show_idx[x]] = self.data_plot[:, self.channels_to_show_idx[x]] * 1.1
            #         print(self.data_plot[:, self.channels_to_show_idx[x]])
            #
            #     self.curve_eeg[x].setData(x=self.x_ticks,
            #                               y=self.data_plot[:, self.channels_to_show_idx[x]] - x * self.scale)

        # Update EEG channels
        # print("paintInterface")
        # print("curve eeg : ", self.curve_eeg)
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

    #
    #	Do necessary stuff when scale has changed
    #
    def update_plot_scale(self, new_scale):

        if (new_scale < 1):
            new_scale = 1
        # commented out by dbdq.
        # else:
        #	new_scale = new_scale - new_scale%10

        self.scale = new_scale

        # Y Tick labels
        values = []
        for x in range(0, len(self.channels_to_show_idx)):
            values.append((-x  * self.scale,
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

    #
    #	Do necessary stuff when seconds to show have changed
    #
    def update_plot_seconds(self, new_seconds):

        # Do nothing unless...
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

        #
        #	Updates the title shown in the scope
        #

    def update_title_scope(self):
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
        #  Sharing variable to stop at the GUI level
        if not self.state.value:
            logger.info('Viewer stopped')
            sys.exit()

        try:
            # assert self.updating==False, 'thread destroyed?'
            # self.updating= True

            # self.handle_tobiid_input()	# Read TiDs.

            self.read_eeg()  # Read new chunk
            # print("shape of self eeg: ", self.eeg.shape)

            # print('self.te_list shape', len(self.ts_list))
            if len(self.ts_list) > 0:
                self.update_template_buffer()
                self.filter_signal()  # Filter acquired data
                self.update_ringbuffers()  # Update the plotting infor
                if (not self.stop_plot):
                    self.repaint()  # Call paint event
        except Exception as e:
            logger.exception('Exception. Dropping into a shell.')
            print(str(e))
            pdb.set_trace()
        finally:
            # self.updating= False
            # using singleShot instead
            # QtCore.QTimer.singleShot( 20, self.update_loop )
            pass

    def read_eeg(self):

        # if self.updating==True: print( '##### ERROR: thread destroyed ? ######' )
        # self.updating= True
        # print("TTTTTTTTTTTTTTTTTTTTT\nread eeg run \n")
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
            pdb.set_trace()

    def read_eeg_cnbiloop(self):
        # Reading in python is blocking, so it will wait until having the amount of data needed
        # Read timestamp. 1 value, type double
        timestamp = struct.unpack("<d", self.fin.read(8 * 1))
        # Read index. 1 value, type uint64
        index = struct.unpack("<Q", self.fin.read(8 * 1))
        # Read labels. self.config.labels, type double
        labels = struct.unpack("<" + str(self.config['labels']) + "I",
                               self.fin.read(4 * self.config['labels']))
        # Read eeg. self.config.samples*self.config.eeg_ch, type float
        beeg = struct.unpack("<" + str(
            self.config['samples'] * self.config['eeg_channels']) + "f",
                             self.fin.read(
                                 4 * self.config['samples'] * self.config['eeg_channels']))
        self.eeg = np.reshape(list(beeg),
                              (self.config['samples'], self.config['eeg_channels']))
        # Read exg. self.config.samples*self.config.exg_ch, type float
        bexg = struct.unpack("<" + str(
            self.config['samples'] * self.config['exg_channels']) + "f",
                             self.fin.read(
                                 4 * self.config['samples'] * self.config['exg_channels']))
        self.exg = np.reshape(list(bexg),
                              (self.config['samples'], self.config['exg_channels']))
        # Read tri. self.config.samples*self.config.tri_ch, type float
        self.tri = struct.unpack("<" + str(
            self.config['samples'] * self.config['tri_channels']) + "i",
                                 self.fin.read(
                                     4 * self.config['samples'] * self.config['tri_channels']))

        #
        #	Bandpas + CAR filtering
        #

    def filter_signal(self):

        if (self.apply_bandpass):
            for x in range(0, self.eeg.shape[1]):
                self.eeg[:, x], self.zi_bandpass_scope[:, x] = lfilter(self.b_bandpass_scope, self.a_bandpass_scope,
                                                        self.eeg[:, x], -1, self.zi_bandpass_scope[:, x])

        if (self.apply_notch):
            for x in range(0, self.eeg.shape[1]):
                self.eeg[:, x], self.zi_notch_scope[:, x] = lfilter(self.b_notch_scope, self.a_notch_scope,
                                                        self.eeg[:, x], -1, self.zi_notch_scope[:, x])

        if (self.apply_lowpass):
            for x in range(0, self.eeg.shape[1]):
                self.eeg[:, x], self.zi_lowpass_scope[:, x] = lfilter(self.b_lowpass_scope, self.a_lowpass_scope,
                                                        self.eeg[:, x], -1, self.zi_lowpass_scope[:, x])

        if (self.apply_highpass):
            for x in range(0, self.eeg.shape[1]):
                self.eeg[:, x], self.zi_highpass_scope[:, x] = lfilter(self.b_lowpass_scope, self.a_lowpass_scope,
                                                        self.eeg[:, x], -1, self.zi_lowpass_scope[:, x])
        # We only apply CAR if selected AND there are at least 2 channels. Otherwise it makes no sense
        if (self.apply_car) and (len(self.channels_to_show_idx) > 1):
            self.eeg = np.dot(self.matrix_car, np.transpose(self.eeg))
            self.eeg = np.transpose(self.eeg)

        #
        #	Update ringbuffers and events for plotting
        #

    def update_template_buffer(self):
        self.template_buffer = np.roll(self.template_buffer, -len(self.ts_list), 0)
        current_chunck = np.copy(self.eeg)

        low_pass_data_in = np.transpose(current_chunck)

        low_pass_data_out, self.initial_condition_list_lp = Utils.apply_filter(self.b_lp, self.a_lp, low_pass_data_in,
                                                                               self.initial_condition_list_lp)

        high_pass_data_in = low_pass_data_out

        high_pass_data_out, self.initial_condition_list_hp = Utils.apply_filter(self.b_hp, self.a_hp, high_pass_data_in,
                                                                                self.initial_condition_list_hp)

        self.template_buffer[-len(self.ts_list):, :] = np.transpose(high_pass_data_out)

    def read_template_buffer(self):
        pre_data_in = np.copy(self.template_buffer[- 6 * int(self.sr.sample_rate):, :])
        pre_data_in = np.copy(pre_data_in[:, 0:9])
        print('pre data in shape: ', pre_data_in.shape)
        return pre_data_in

    def update_ringbuffers(self):


        # update single channel scale
        # print("single channel scale: ", self.single_channel_scale)
        if self.ui.checkBox_single_channel_scale.isChecked() \
                and self.channel_to_scale_row_index != -1 \
                and self.channel_to_scale_column_index != -1 \
                and self.channel_to_scale_row_index in self.channels_to_show_idx:
            self.eeg[:, self.channel_to_scale_row_index] = self.eeg[:, self.channel_to_scale_row_index] * self.single_channel_scale

        # We have to remove those indexes that reached time = 0
        # leeq
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

        # =============================================================================
        #         subprocess.Popen(["cl_rpc", "closexdf"], close_fds=True)
        #         self.ui.pushButton_rec.setEnabled(True)
        #         self.ui.pushButton_stoprec.setEnabled(False)
        #         self.ui.statusBar.showMessage("Not recording")
        # =============================================================================

    # Online Experiment

    def set_MRCP_window_size(self, MRCP_window_size):
        self.MRCP_window_size = MRCP_window_size

    def update_MRCP_plot(self):
        self.set_MRCP_window_size(6)
        self.raw_trial_MRCP = self.read_template_buffer()
        self.processed_trial_MRCP = Utils.preprocess(self.raw_trial_MRCP)
        # save each MRCP and raw signals into total MRCP list
        self.total_trials_MRCP.append(self.processed_trial_MRCP)
        self.total_trials_raw_MRCP.append(np.transpose(self.raw_trial_MRCP).flatten())

        self.line_width = 4
        self.MRCP_plot(self.processed_trial_MRCP)
        self.temp_counter += 1
        self.temp_counter_list.append(self.temp_counter)
        self.ui.label_content_current_temp.setText(str(self.temp_counter))

    def MRCP_plot(self, about_to_plot_MRCP):
        # pdb.set_trace()
        size = len(about_to_plot_MRCP)
        print("\nMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM\nMRCP size: ", size)
        # print("processed_MRCP: {}".format(self.processed_trial_MRCP))
        # input()
        # x = list(range(0,size))
        x = [x / self.sr.sample_rate - 2 for x in list(range(0, size))]
        # x = list(range(size))
        # x = np.linspace(-2, 4, self.sr.sample_rate * 6)
        # pdb.set_trace()
        y = np.transpose(about_to_plot_MRCP)
        # plt.plot(x,y)
        # plt.show()
        R = randrange(255)
        G = randrange(255)
        B = randrange(255)
        # self.current_line_color = (R,G,B)
        self.ui.graphicsView.plot(x, y, pen=pg.mkPen(color=(R, G, B), width=1))
        # pdb.set_trace()
        # self.ui.graphicsView.plot(x,y,pen=QPen(QColor(R, G, B)))

    def plot_display_temp(self):
        # plot selcted MRCP
        self.ui.graphicsView.clear()
        print("display temp list", self.display_temp_list)
        for i in self.display_temp_list:
            self.MRCP_plot(self.total_trials_MRCP[int(i) - 1])

    def get_input_temp(self):
        self.selected_temp = self.ui.lineEdit_temp_selector.text()
        self.list_selected_temp = self.selected_temp.split()
        print("list_selected_temp", self.list_selected_temp)
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
        print("input temp list", self.input_temp_list)
