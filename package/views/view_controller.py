import math
import os
import subprocess
import numpy as np
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem, QWidget, QHBoxLayout, \
    QApplication, QMainWindow
from PyQt5 import QtCore, QtGui
from ..entity.edata.utils import Utils
from pycnbi import logger
import pdb
from ..entity.edata.variables import Variables
import time
import datetime
import pandas as pd
from ..router import router

DEBUG_TRIGGER = False  # TODO: parameterize
NUM_X_CHANNELS = 16  # TODO: parameterize


class ViewController:

    # Main control buttons
    def onClicked_button_Main_switch(self, pressed):
        if pressed:
            self.ui.statusBar.showMessage("System is On")
            self.ui.tab_experimental_protocol.setEnabled(True)
            self.ui.tab_subjec_information.setEnabled(True)
            self.ui.tab_event_and_file_management.setEnabled(True)
            self.ui.tab_Oscilloscope.setEnabled(True)
            self.ui.tab_experiment_type.setEnabled(True)
        else:
            self.ui.statusBar.showMessage("System is Off")
            self.ui.tab_experimental_protocol.setEnabled(False)
            self.ui.tab_subjec_information.setEnabled(False)
            self.ui.tab_event_and_file_management.setEnabled(False)
            self.ui.tab_Oscilloscope.setEnabled(False)
            self.ui.tab_experiment_type.setEnabled(False)

    def onClicked_button_scope_switch(self, pressed):
        if pressed:
            self.ui.statusBar.showMessage("show oscilloscope")
            self.win.show()
        else:
            self.ui.statusBar.showMessage("oscilloscope closed")
            self.win.hide()

    def onClicked_button_train(self):
        pass

    def onClicked_button_test(self):
        pass

    def onClicked_button_rec(self, pressed):
        if pressed:
            print(1)
            self.ui.statusBar.showMessage("Recording started")
            logger.info("rec clicked")
            Variables.add_run_counter()

            path = "{}\Run{}".format(Variables.get_base_folder_path(), Variables.get_run_counter())
            Variables.set_sub_folder_path(path)
            try:
                os.makedirs(Variables.get_sub_folder_path())
            except OSError:
                print("Creation of the directory %s failed" % Variables.get_sub_folder_path())


            eeg_file = "%s\\raw_eeg.csv" % (Variables.get_sub_folder_path())
            Variables.set_raw_eeg_file_path(eeg_file)
            eeg_timestamp_file = "%s/raw_eeg_timestamp.csv" % (Variables.get_sub_folder_path())
            Variables.set_raw_eeg_timestamp_file_path(eeg_timestamp_file)

            self.router.set_raw_eeg_file_path()
            print(Variables.get_raw_eeg_file_path())

            self.ui.label_run_number.setText(str(Variables.get_run_counter()))
            print("\nsubfolder created Run {}".format(Variables.get_run_counter()))

            self.init_table_file_path()
            self.update_table_file_path()

            self.router.start_recording()
            Variables.set_run_time_counter(0)
            time_show = Variables.get_run_time_counter()
            self.ui.lcdNumber_timer.display(time_show)

            self.Runtimer.start(1000)

            timestamp = time.strftime('%Y%m%d-%H%M%S', time.localtime())
            print("\nlocal time stamp: ", timestamp)
        else:
            print(0)
            self.ui.statusBar.showMessage("Recording stopped")
            logger.info("stop rec clicked")
            print("get raw eeg file path", Variables.get_raw_eeg_file_path())
            self.Runtimer.stop()
            self.router.stop_recording()
            if self.total_trials_raw_MRCP != [] and self.total_trials_MRCP != []:
                no_trials = len(self.total_trials_raw_MRCP)
                no_channels = 9
                raw_MRCP = np.reshape(np.asarray(self.total_trials_raw_MRCP), (no_trials * no_channels, -1))
                self.raw_mrcp_file_path = Utils.write_data_to_csv(raw_MRCP, "raw_mrcp.csv")
                self.mrcp_template_file_path = Utils.write_data_to_csv(self.total_trials_MRCP, "mrcp_template.csv")

            self.update_table_file_path()
            Variables.init_Variables_for_next_run()
            self.init_panel_GUI_stop_recording()
            self.init_SV_GUI()

            self.ui.tab_event_and_file_management.setEnabled(True)
            self.ui.tab_experimental_protocol.setEnabled(True)
            self.ui.tab_experiment_type.setEnabled(True)
            self.ui.groupBox_task_manager.setEnabled(True)
            self.ui.tableWidget_tasks.setRowCount(0)
            self.ui.tableWidget_task_event_number.setRowCount(0)
            self.ui.graphicsView.clear()

    # def onClicked_button_stop_SV(self):
    #     self.stop_SV()

    def onClicked_button_start_SV(self):
        self.ui.statusBar.showMessage("Tasks started")
        self.SV_time = 0
        self.is_experiment_on = True
        self.window.show()

    def closeEvent(self, event):
        '''
        reply = QtGui.QMessageBox.question(self, "Quit", "Are you sure you want to quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        if (reply == QtGui.QMessageBox.Yes):
            if (self.pushButton_stoprec.isEnabled()):
                subprocess.Popen(["cl_rpc", "closexdf"], close_fds=True)
            self.fin.close()
            exit()
        '''
        # leeq
        if (self.ui.pushButton_stoprec.isEnabled()):
            subprocess.Popen(["cl_rpc", "closexdf"], close_fds=True)
        with self.state.get_lock():
            self.state.value = 0

        # ----------------------------------------------------------------------------------------------------
        # 		END OF EVENT HANDLERS
        # ----------------------------------------------------------------------------------------------------

    # Device

    # Subject Information button
    def onClicked_button_save_subject_information(self):

        self.first_name = self.ui.lineEdit_first_name.text()
        self.last_name = self.ui.lineEdit_last_name.text()
        self.gender = self.ui.lineEdit_gender.text()
        self.age = self.ui.lineEdit_age.text()
        self.email = self.ui.lineEdit_email.text()
        self.telephone = self.ui.lineEdit_telephone.text()
        self.address = self.ui.lineEdit_address.text()
        self.additional_comment = self.ui.plainTextEdit_additional_comments.toPlainText()
        self.ui.tab_subjec_information.setEnabled(False)

        base_path = self.choose_base_folder()
        path = r"{}\{}".format(base_path, self.first_name + "_" + self.last_name + datetime.datetime.today().strftime('%Y-%m-%d'))
        Variables.set_base_folder_path(path)
        try:
            os.makedirs(Variables.get_base_folder_path())
        except OSError:
            print("Creation of the directory %s failed" % Variables.get_base_folder_path())
        self.subject_file_path = "{}\subject.txt".format(Variables.get_base_folder_path())
        f = open(self.subject_file_path, "w+")
        f.writelines("first name: {}\n".format(self.first_name))
        f.writelines("last name: {}\n".format(self.last_name))
        f.writelines("age: {}\n".format(self.age))
        f.writelines("gender: {}\n".format(self.gender))
        f.writelines("email: {}\n".format(self.email))
        f.writelines("telephone: {}\n".format(self.telephone))
        f.writelines("address: {}\n".format(self.address))
        f.writelines("additional comments: {}\n".format(self.additional_comment))
        f.close()
        self.ui.statusBar.showMessage(
            "Subject information is saved to {}".format("{}\subject.txt".format(Variables.get_base_folder_path())))

    # Experimental protocol buttons
    def onClicked_toolButton_choose_sound_task(self):
        self.openFileNameDialog_sound()

    # Experimental protocol
    def onClicked_button_define_task_add(self):
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

    def onClicked_toolButton_choose_image_task(self):
        self.openFileNameDialog_image()

        # self.task_image_path_list.append(self.task_image_path)

    def onClicked_button_define_task_done(self):
        self.task_table, _ = self.get_task_name_table_content()
        self.new_task_table = np.copy(self.task_table)  # initialize new_task_table
        self.ui.groupBox_sequence_manager.setEnabled(True)
        self.ui.groupBox_task_manager.setEnabled(False)
        # print("task name list:\n",self.new_task_list)
        # print("task description list:\n",self.task_descriptor_list)
        # print("task image paths list:\n",self.task_image_path_list)

    def onClicked_button_create_sequence(self):
        group_number = self.ui.lineEdit_group_number.text()
        for i in range(int(group_number) - 1):
            self.new_task_table = np.r_[self.new_task_table, self.task_table]
        self.ui.tableWidget_tasks.setRowCount(self.new_task_table.shape[0])
        for i in range(self.new_task_table.shape[0]):
            self.ui.tableWidget_tasks.setItem(i, 0, QTableWidgetItem(self.new_task_table[i][0]))
            self.ui.tableWidget_tasks.setItem(i, 1, QTableWidgetItem(self.new_task_table[i][1]))
            self.ui.tableWidget_tasks.setItem(i, 2, QTableWidgetItem(self.new_task_table[i][2]))
            self.ui.tableWidget_tasks.setItem(i, 3, QTableWidgetItem(self.new_task_table[i][3]))

    def onClicked_button_randomize(self):
        np.random.shuffle(self.new_task_table)
        self.ui.tableWidget_tasks.setRowCount(self.new_task_table.shape[0])
        for i in range(self.new_task_table.shape[0]):
            self.ui.tableWidget_tasks.setItem(i, 0, QTableWidgetItem(self.new_task_table[i][0]))
            self.ui.tableWidget_tasks.setItem(i, 1, QTableWidgetItem(self.new_task_table[i][1]))
            self.ui.tableWidget_tasks.setItem(i, 2, QTableWidgetItem(self.new_task_table[i][2]))
            self.ui.tableWidget_tasks.setItem(i, 3, QTableWidgetItem(self.new_task_table[i][3]))



    def onClicked_toolButton_load_protocol(self):
        self.openFileNameDialog_protocol()


    def onClicked_experimental_protocol_finish(self):
        self.ui.tab_experimental_protocol.setEnabled(False)
        unique_task_list = np.unique(self.task_list)
        self.event_list = unique_task_list.tolist() + ['Idle', 'Focus', 'Prepare', 'Two', 'One', 'Task']
        self.ui.tableWidget_task_event_number.setRowCount(len(self.event_list))
        for i in range(len(self.event_list)):
            self.ui.tableWidget_task_event_number.setItem(i, 0, QTableWidgetItem(self.event_list[i]))
        self.idle_time = int(self.ui.idleTimeLineEdit.text())
        self.focus_time = self.idle_time + int(self.ui.focusTimeLineEdit.text())
        self.prepare_time = self.focus_time + int(self.ui.prepareTimeLineEdit.text())
        self.two_time = self.prepare_time + int(self.ui.twoTimeLineEdit.text())
        self.one_time = self.two_time + int(self.ui.oneTimeLineEdit.text())
        self.task_time = self.one_time + int(self.ui.taskTimeLineEdit.text())
        self.relax_time = self.task_time + 2
        self.cycle_time = self.relax_time

    def onClicked_button_save_protocol(self):
        _, self.protocol = self.get_task_name_table_content()
        self.saveFileNameDialog_protocol()
        # Utils.save_protocol_to_csv(protocol, "exp. protocol.csv")
        self.ui.statusBar.showMessage("protocol saved to {}".format(Variables.get_protocol_path()))

    # Event Management buttons

    def onClicked_button_save_event_number(self):
        event_dict = self.get_event_number_table_content()
        Utils.write_event_number_to_csv(event_dict)

    # Oscilloscope buttons
    def onActivated_checkbox_bandpass(self):
        self.apply_bandpass = False
        self.ui.pushButton_bp.setEnabled(self.ui.checkBox_bandpass.isChecked())
        self.ui.doubleSpinBox_hp.setEnabled(self.ui.checkBox_bandpass.isChecked())
        self.ui.doubleSpinBox_lp.setEnabled(self.ui.checkBox_bandpass.isChecked())
        self.update_title_scope()

    def onActivated_checkbox_notch(self):
        self.apply_notch = False
        self.ui.pushButton_apply_notch.setEnabled(self.ui.checkBox_notch.isChecked())
        self.ui.doubleSpinBox_lc_notch.setEnabled(self.ui.checkBox_notch.isChecked())
        self.ui.doubleSpinBox_hc_notch.setEnabled(self.ui.checkBox_notch.isChecked())

    def onActivated_checkbox_lowpass(self):
        self.apply_lowpass = False
        self.ui.pushButton_apply_lowpass.setEnabled(self.ui.checkBox_low_pass.isChecked())
        self.ui.doubleSpinBox_lc_lowpass.setEnabled(self.ui.checkBox_low_pass.isChecked())

    def onActivated_checkbox_highpass(self):
        self.apply_highpass = False
        self.ui.pushButton_apply_highpass.setEnabled(self.ui.checkBox_highpass.isChecked())
        self.ui.doubleSpinBox_lc_highpass.setEnabled(self.ui.checkBox_highpass.isChecked())

    def onActivated_checkbox_car(self):
        self.apply_car = self.ui.checkBox_car.isChecked()
        self.update_title_scope()


    def onValueChanged_spinbox_time(self):
        self.update_plot_seconds(self.ui.spinBox_time.value())

    def onActivated_combobox_scale(self):
        if self.ui.checkBox_single_channel_scale.isChecked():
            self.single_channel_scale = self.single_scales_range[self.ui.comboBox_scale.currentIndex()]

        else:
            # self.single_channel_scale = 0
            self.update_plot_scale(self.scales_range[self.ui.comboBox_scale.currentIndex()])

    def onClicked_button_bp(self):
        if (self.ui.doubleSpinBox_lp.value() > self.ui.doubleSpinBox_hp.value()):
            self.apply_bandpass = True
            self.b_bandpass_scope, self.a_bandpass_scope, self.zi_bandpass_scope = Utils.butter_bandpass_scope(self.ui.doubleSpinBox_hp.value(),
                                                            self.ui.doubleSpinBox_lp.value(),
                                                            self.config['sf'],
                                                            self.config['eeg_channels'])
        self.update_title_scope()

    def onClicked_button_notch(self):
        if (self.ui.doubleSpinBox_hc_notch.value() > self.ui.doubleSpinBox_lc_notch.value()):
            self.apply_notch = True
            self.b_notch_scope, self.a_notch_scope, self.zi_notch_scope = Utils.butter_notch_scope(
                                                            self.ui.doubleSpinBox_hc_notch.value(),
                                                            self.ui.doubleSpinBox_lc_notch.value(),
                                                            self.config['sf'],
                                                            self.config['eeg_channels'])

    def onClicked_button_lowpass(self):
        if (self.ui.doubleSpinBox_lc_lowpass.value() > 0.0):
            self.apply_lowpass = True
            self.b_lowpass_scope, self.a_lowpass_scope, self.zi_lowpass_scope = Utils.butter_lowpass_scope(
                                                            self.ui.doubleSpinBox_lc_lowpass.value(),
                                                            self.config['sf'],
                                                            self.config['eeg_channels'])


    def onClicked_button_highpass(self):
        if (self.ui.doubleSpinBox_lc_highpass.value() > 0.0):
            self.apply_highpass = True
            self.b_highpass_scope, self.a_highpass_scope, self.zi_highpass_scope = Utils.butter_highpass_scope(
                                                            self.ui.doubleSpinBox_lc_highpass.value(),
                                                            self.config['sf'],
                                                            self.config['eeg_channels'])

    def onDoubleClicked_channel_table(self):
        for idx in self.ui.table_channels.selectionModel().selectedIndexes():
            self.selected_channel_row_index = idx.row()
            self.selected_channel_column_index = idx.column()


    def onClicked_button_update_channel_name(self):
        self.channel_labels[self.selected_channel_row_index] = self.ui.table_channels.item(self.selected_channel_row_index, self.selected_channel_column_index).text()

    def onSelectionChanged_table(self):

        # Remove current plot
        print(self.channels_to_show_idx)
        for x in range(0, len(self.channels_to_show_idx)):
            self.main_plot_handler.removeItem(self.curve_eeg[x])

        # Which channels should I plot?
        self.channels_to_show_idx = []
        self.channels_to_hide_idx = []
        idx = 0
        for y in range(0, 4):
            for x in range(0, NUM_X_CHANNELS):
                if (idx < self.config['eeg_channels']):
                    # if (self.table_channels.isItemSelected( # Qt4 only
                    if (QTableWidgetItem.isSelected(  # Qt5
                            self.ui.table_channels.item(x, y))):
                        self.channels_to_show_idx.append(idx)
                    else:
                        self.channels_to_hide_idx.append(idx)
                    idx += 1

        # Add new plots
        self.curve_eeg = []
        for x in range(0, len(self.channels_to_show_idx)):
            self.curve_eeg.append(self.main_plot_handler.plot(x=self.x_ticks,
                                                              y=self.data_plot[:, self.channels_to_show_idx[x]],
                                                              pen=self.colors[
                                                                  self.channels_to_show_idx[x] % NUM_X_CHANNELS, :]))
            self.curve_eeg[-1].setDownsampling(ds=self.subsampling_value,
                                               auto=False, method="mean")

        # Update CAR so it's computed based only on the shown channels
        if (len(self.channels_to_show_idx) > 1):
            self.matrix_car = np.zeros(
                (self.config['eeg_channels'], self.config['eeg_channels']),
                dtype=float)
            self.matrix_car[:, :] = -1 / float(len(self.channels_to_show_idx))
            np.fill_diagonal(self.matrix_car,
                             1 - (1 / float(len(self.channels_to_show_idx))))
            for x in range(0, len(self.channels_to_hide_idx)):
                self.matrix_car[self.channels_to_hide_idx[x], :] = 0
                self.matrix_car[:, self.channels_to_hide_idx[x]] = 0

        # Refresh the plot
        self.update_plot_scale(self.scale)

        #

    def keyPressEvent(self, event):
        key = event.key()
        if (key == QtCore.Qt.Key_Escape):
            self.closeEvent(None)
        if (key == QtCore.Qt.Key_H):
            self.show_help = not self.show_help
            self.trigger_help()
        if (key == QtCore.Qt.Key_Up):
            # Python's log(x, 10) has a rounding bug. Use log10(x) instead.
            # new_scale = self.scale + max(1, 10 ** int(math.log10(self.scale)))
            # self.update_plot_scale(new_scale)
            self.single_channel_scale *= 2
        if (key == QtCore.Qt.Key_Space):
            self.stop_plot = not self.stop_plot
        if (key == QtCore.Qt.Key_Down):
            if self.single_channel_scale >= 0:
                self.single_channel_scale /= 2
            else:
                self.single_channel_scale = 1

        if (key == QtCore.Qt.Key_Left):
            self.update_plot_seconds(self.seconds_to_show - 1)
        if (key == QtCore.Qt.Key_Right):
            self.update_plot_seconds(self.seconds_to_show + 1)
        if (key == QtCore.Qt.Key_C):
            self.ui.checkBox_car.setChecked(not self.ui.checkBox_car.isChecked())
        if (key == QtCore.Qt.Key_B):
            self.ui.checkBox_bandpass.setChecked(
                not self.ui.checkBox_bandpass.isChecked())
            if self.ui.checkBox_bandpass.isChecked():
                self.ui.pushButton_bp.click()
        if ((key >= QtCore.Qt.Key_0) and (key <= QtCore.Qt.Key_9)):
            if (self.show_Key_events) and (not self.stop_plot):
                self.addEventPlot("KEY", 990 + key - QtCore.Qt.Key_0)
                # self.bci.id_msg_bus.SetEvent(990 + key - QtCore.Qt.Key_0)
                # self.bci.iDsock_bus.sendall(self.bci.id_serializer_bus.Serialize());
                # 666

    # Online Experiment
    # EEG
    # MRCP

    def onClicked_button_temp_view(self):
        self.get_input_temp()
        self.display_temp_list = self.input_temp_list
        self.ui.label_content_Disp_temp.setText("{}".format(self.display_temp_list))
        self.plot_display_temp()

    def onClicked_button_temp_remove(self):
        self.get_input_temp()
        for element in self.input_temp_list:
            del self.total_trials_MRCP[element - 1]
        # self.display_temp_list = [x for x in self.total_MRCP_inds if x not in self.input_temp_list]
        self.display_temp_list = list(range(1,len(self.total_trials_MRCP)+1))
        self.ui.label_content_Disp_temp.setText("{}".format(self.display_temp_list))
        self.ui.label_content_available_temp.setText("{}".format(self.display_temp_list))
        self.plot_display_temp()
        # pdb.set_trace()

    def onClicked_button_temp_clear(self):
        self.ui.graphicsView.clear()

    def onClicked_button_temp_mean(self):
        # calculate mean MRCP
        # NOT TESTED
        # dummy = np.asarray(self.total_trials_MRCP)
        # self.mean_MRCP = np.mean(dummy[self.display_temp_list], 0)
        self.mean_MRCP = np.mean(self.total_trials_MRCP, 0)
        self.ui.graphicsView.clear()
        self.MRCP_plot(self.mean_MRCP)

