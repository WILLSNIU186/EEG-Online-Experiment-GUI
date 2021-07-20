import os
import datetime
import os
import time
from threading import Thread

import numpy as np
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from pycnbi import logger
from twisted.internet import reactor

from ..entity.edata.utils import Utils
from ..entity.edata.variables import Variables

DEBUG_TRIGGER = False  # TODO: parameterize
NUM_X_CHANNELS = 16  # TODO: parameterize


class ViewController:
    """
    ViewController contains the event listeners for each widget.
    """

    # def onClicked_button_Main_switch(self, pressed):
    #     """
    #     Event listener for main switch down the experimenter GUI
    #     """
    #     if pressed:
    #         self.ui.statusBar.showMessage("System is On")
    #         self.ui.tab_experimental_protocol.setEnabled(True)
    #         self.ui.tab_subjec_information.setEnabled(True)
    #         self.ui.tab_event_and_file_management.setEnabled(True)
    #         self.ui.tab_Oscilloscope.setEnabled(True)
    #         self.ui.tab_experiment_type.setEnabled(True)
    #     else:
    #         self.ui.statusBar.showMessage("System is Off")
    #         self.ui.tab_experimental_protocol.setEnabled(False)
    #         self.ui.tab_subjec_information.setEnabled(False)
    #         self.ui.tab_event_and_file_management.setEnabled(False)
    #         self.ui.tab_Oscilloscope.setEnabled(False)
    #         self.ui.tab_experiment_type.setEnabled(False)

    # def onClicked_button_scope_switch(self, pressed):
    #
    #     if pressed:
    #         self.ui.statusBar.showMessage("show oscilloscope")
    #         self.win.show()
    #     else:
    #         self.ui.statusBar.showMessage("oscilloscope closed")
    #         self.win.hide()

    # def onClicked_button_train(self):
    #     pass
    #
    # def onClicked_button_test(self):
    #     pass
    #
    # def onClicked_button_rec(self, pressed):
    #     """
    #     Start the recording when recording button been clicked
    #     """
    #     if pressed:
    #         print(1)
    #         self.ui.statusBar.showMessage("Recording started")
    #         logger.info("rec clicked")
    #         Variables.add_run_counter()
    #
    #         path = "{}\Run{}".format(Variables.get_base_folder_path(), Variables.get_run_counter())
    #         Variables.set_sub_folder_path(path)
    #         try:
    #             os.makedirs(Variables.get_sub_folder_path())
    #         except OSError:
    #             print("Creation of the directory %s failed" % Variables.get_sub_folder_path())
    #
    #         eeg_file = "%s\\raw_eeg.csv" % (Variables.get_sub_folder_path())
    #         Variables.set_raw_eeg_file_path(eeg_file)
    #         eeg_timestamp_file = "%s/raw_eeg_timestamp.csv" % (Variables.get_sub_folder_path())
    #         Variables.set_raw_eeg_timestamp_file_path(eeg_timestamp_file)
    #
    #         self.router.set_raw_eeg_file_path()
    #         print(Variables.get_raw_eeg_file_path())
    #
    #         self.ui.label_run_number.setText(str(Variables.get_run_counter()))
    #         print("\nsubfolder created Run {}".format(Variables.get_run_counter()))
    #
    #         self.init_table_file_path()
    #         self.update_table_file_path()
    #
    #         self.router.start_recording()
    #         # Variables.set_run_time_counter(0)
    #         # time_show = Variables.get_run_time_counter()
    #         self.time_show = 0
    #         self.ui.lcdNumber_timer.display(self.time_show)
    #
    #         self.Runtimer.start(1)
    #         self.t = Thread(target=reactor.run, args=(False,))
    #         self.t.start()
    #
    #         timestamp = time.strftime('%Y%m%d-%H%M%S', time.localtime())
    #         print("\nlocal time stamp: ", timestamp)
    #     else:
    #         print(0)
    #         self.ui.statusBar.showMessage("Recording stopped")
    #         logger.info("stop rec clicked")
    #         print("get raw eeg file path", Variables.get_raw_eeg_file_path())
    #         #
    #         # self.t.join()
    #         reactor.stop()
    #         self.Runtimer.stop()
    #
    #         self.router.stop_recording()
    #         Utils.write_data_to_csv(self.os_time_list, "os_time_list.csv")
    #         Utils.write_data_to_csv(self.os_time_list1, "os_time_list1.csv")
    #         Utils.write_dict_to_csv(self.create_channel_dict(), "channels.csv")
    #         Utils.write_dict_to_csv(self.bad_epoch_dict, "bad_epochs.csv")
    #         self.event_file_path = Utils.write_data_to_csv(self.event_timestamp_list, 'event.csv')
    #         print(self.event_file_path)
    #         # if self.total_trials_raw_MRCP != [] and self.total_trials_MRCP != []:
    #         #     no_trials = len(self.total_trials_raw_MRCP)
    #         #     no_channels = 9
    #         #     # raw_MRCP = np.reshape(np.asarray(self.total_trials_raw_MRCP), (no_trials * no_channels, -1))
    #         #     # self.raw_mrcp_file_path = Utils.write_data_to_csv(raw_MRCP, "raw_mrcp.csv")
    #         #     # self.mrcp_template_file_path = Utils.write_data_to_csv(self.total_trials_MRCP, "mrcp_template.csv")
    #
    #         self.update_table_file_path()
    #         Variables.init_Variables_for_next_run()
    #         self.init_panel_GUI_stop_recording()
    #         self.init_SV_GUI()
    #
    #         self.ui.tab_event_and_file_management.setEnabled(True)
    #         self.ui.tab_experimental_protocol.setEnabled(True)
    #         self.ui.tab_experiment_type.setEnabled(True)
    #         self.ui.groupBox_task_manager.setEnabled(True)
    #         self.ui.tableWidget_tasks.setRowCount(0)
    #         self.ui.tableWidget_task_event_number.setRowCount(0)
    #         self.ui.graphicsView.clear()

    # def onClicked_button_stop_SV(self):
    #     self.stop_SV()
    # def create_channel_dict(self):
    #     """
    #     Read current channel names from LSL and return a dictionary.
    #     :return: channel name dictionary
    #     """
    #     keys = list(range(len(self.channel_labels.tolist())))
    #     channel_dict = dict(zip(keys, self.channel_labels.tolist()))
    #     return channel_dict

    # def onClicked_button_start_SV(self):
    #     """
    #     Event listener for task button
    #     """
    #     self.ui.statusBar.showMessage("Tasks started")
    #     self.SV_time = 0
    #     self.is_experiment_on = True
    #     self.window.show()


    # def onClicked_button_save_subject_information(self):
    #     """
    #     Event listener for 'save' button on subject information tab. The subject information typed in GUI
    #     will be saved to subject.txt
    #     """
    #     self.first_name = self.ui.lineEdit_first_name.text()
    #     self.last_name = self.ui.lineEdit_last_name.text()
    #     self.gender = self.ui.lineEdit_gender.text()
    #     self.age = self.ui.lineEdit_age.text()
    #     self.email = self.ui.lineEdit_email.text()
    #     self.telephone = self.ui.lineEdit_telephone.text()
    #     self.address = self.ui.lineEdit_address.text()
    #     self.additional_comment = self.ui.plainTextEdit_additional_comments.toPlainText()
    #     self.ui.tab_subjec_information.setEnabled(False)
    #
    #     base_path = self.choose_base_folder()
    #     path = r"{}\{}".format(base_path,
    #                            self.first_name + "_" + self.last_name + datetime.datetime.today().strftime('%Y-%m-%d'))
    #     Variables.set_base_folder_path(path)
    #     try:
    #         os.makedirs(Variables.get_base_folder_path())
    #     except OSError:
    #         print("Creation of the directory %s failed" % Variables.get_base_folder_path())
    #     self.subject_file_path = "{}\subject.txt".format(Variables.get_base_folder_path())
    #     f = open(self.subject_file_path, "w+")
    #     f.writelines("first name: {}\n".format(self.first_name))
    #     f.writelines("last name: {}\n".format(self.last_name))
    #     f.writelines("age: {}\n".format(self.age))
    #     f.writelines("gender: {}\n".format(self.gender))
    #     f.writelines("email: {}\n".format(self.email))
    #     f.writelines("telephone: {}\n".format(self.telephone))
    #     f.writelines("address: {}\n".format(self.address))
    #     f.writelines("additional comments: {}\n".format(self.additional_comment))
    #     f.close()
    #     self.ui.statusBar.showMessage(
    #         "Subject information is saved to {}".format("{}\subject.txt".format(Variables.get_base_folder_path())))

    # def onClicked_toolButton_choose_sound_task(self):
    #     """
    #     Event listener for three dot button next to choose sound for task in Experiment Protocal tab
    #     """
    #     self.openFileNameDialog_sound()

    # def onClicked_button_define_task_add(self):
    #     """
    #     Event listener for Add button in Task manager in Experimental Protocal tab
    #     """
    #     # Add task name and description in table
    #     exp_task_name = self.ui.lineEdit_define_task.text()
    #     task_descriptor = self.ui.lineEdit_subject_view_description.text()
    #
    #     if len(exp_task_name) > 0:
    #         row_position = self.ui.tableWidget_tasks.rowCount()
    #         self.ui.tableWidget_tasks.insertRow(row_position)
    #         self.ui.tableWidget_tasks.setItem(row_position, 0, QTableWidgetItem(exp_task_name))
    #         self.ui.tableWidget_tasks.setItem(row_position, 1, QTableWidgetItem(task_descriptor))
    #         self.ui.tableWidget_tasks.setItem(row_position, 2, QTableWidgetItem(self.task_image_path))
    #         self.ui.tableWidget_tasks.setItem(row_position, 3, QTableWidgetItem(self.task_sound_path))

    # def onClicked_toolButton_choose_image_task(self):
    #     """
    #     Event listener for three dot button next to choose image for task in Experiment Protocal tab
    #     """
    #     self.openFileNameDialog_image()


    # def onClicked_button_define_task_done(self):
    #     """
    #     Event listener for Done button in Task manager in Experimental protocol tab.
    #     By clicking Done button, no more new tasks could be added.
    #     """
    #     self.task_table, _ = self.get_task_name_table_content()
    #     self.new_task_table = np.copy(self.task_table)  # initialize new_task_table
    #     self.ui.groupBox_sequence_manager.setEnabled(True)
    #     self.ui.groupBox_task_manager.setEnabled(False)
    #     # print("task name list:\n",self.new_task_list)
    #     # print("task description list:\n",self.task_descriptor_list)
    #     # print("task image paths list:\n",self.task_image_path_list)

    # def onClicked_button_create_sequence(self):
    #     """
    #     Event listener for create sequence button in Experimental Protocol tab.
    #     The listed tasks will be iterated 'group number' times in the Task table
    #     """
    #     group_number = self.ui.lineEdit_group_number.text()
    #     for i in range(int(group_number) - 1):
    #         self.new_task_table = np.r_[self.new_task_table, self.task_table]
    #     self.ui.tableWidget_tasks.setRowCount(self.new_task_table.shape[0])
    #     for i in range(self.new_task_table.shape[0]):
    #         self.ui.tableWidget_tasks.setItem(i, 0, QTableWidgetItem(self.new_task_table[i][0]))
    #         self.ui.tableWidget_tasks.setItem(i, 1, QTableWidgetItem(self.new_task_table[i][1]))
    #         self.ui.tableWidget_tasks.setItem(i, 2, QTableWidgetItem(self.new_task_table[i][2]))
    #         self.ui.tableWidget_tasks.setItem(i, 3, QTableWidgetItem(self.new_task_table[i][3]))

    # def onClicked_button_randomize(self):
    #     """
    #     Event listener for Randomize button in Experimental protocol
    #     Randomize the order of tasks in Task table
    #     """
    #     np.random.shuffle(self.new_task_table)
    #     self.ui.tableWidget_tasks.setRowCount(self.new_task_table.shape[0])
    #     for i in range(self.new_task_table.shape[0]):
    #         self.ui.tableWidget_tasks.setItem(i, 0, QTableWidgetItem(self.new_task_table[i][0]))
    #         self.ui.tableWidget_tasks.setItem(i, 1, QTableWidgetItem(self.new_task_table[i][1]))
    #         self.ui.tableWidget_tasks.setItem(i, 2, QTableWidgetItem(self.new_task_table[i][2]))
    #         self.ui.tableWidget_tasks.setItem(i, 3, QTableWidgetItem(self.new_task_table[i][3]))

    # def onClicked_toolButton_load_protocol(self):
    #     """
    #     Event listener for load exp. protocol button
    #     Open folder to choose existing experimental protocol files
    #     """
    #     self.openFileNameDialog_protocol()

    # def onClicked_experimental_protocol_finish(self):
    #     """
    #     Event listener for Finish button in experimental protocol tab.
    #     Disable all inputs in this tab and save Task table into variable to be used for generating tasks.
    #     """
    #     self.ui.tab_experimental_protocol.setEnabled(False)
    #     self.new_task_list = self.new_task_table[:,0].tolist()
    #     self.unique_task_list = np.unique(self.new_task_list)
    #     self.event_list = self.unique_task_list.tolist() + ['Idle', 'Focus', 'Prepare', 'Two', 'One', 'Task']
    #     self.ui.tableWidget_task_event_number.setRowCount(len(self.event_list))
    #     for i in range(len(self.event_list)):
    #         self.ui.tableWidget_task_event_number.setItem(i, 0, QTableWidgetItem(self.event_list[i]))
    #     self.idle_time = int(self.ui.idleTimeLineEdit.text())
    #     self.focus_time = self.idle_time + int(self.ui.focusTimeLineEdit.text())
    #     self.prepare_time = self.focus_time + int(self.ui.prepareTimeLineEdit.text())
    #     self.two_time = self.prepare_time + int(self.ui.twoTimeLineEdit.text())
    #     self.one_time = self.two_time + int(self.ui.oneTimeLineEdit.text())
    #     self.task_time = self.one_time + int(self.ui.taskTimeLineEdit.text())
    #     self.relax_time = self.task_time + 2
    #     self.cycle_time = self.relax_time
    #     # write to class epoch counter table
    #     self.ui.tableWidget_class_epoch_counter.setRowCount(len(self.unique_task_list))
    #     for i in range(len(self.unique_task_list)):
    #         self.ui.tableWidget_class_epoch_counter.setItem(i, 0, QTableWidgetItem(self.unique_task_list[i]))
    #     # write to bad epoch table
    #     self.ui.tableWidget_bad_epoch.setRowCount(len(self.unique_task_list))
    #     for i in range(len(self.unique_task_list)):
    #         self.ui.tableWidget_bad_epoch.setItem(i, 0, QTableWidgetItem(self.unique_task_list[i]))
    #     # create bad epoch dict
    #     self.bad_epoch_dict = {k: [] for k in self.unique_task_list}

    # def onClicked_button_save_protocol(self):
    #     """
    #     Event listener for Save current protocol button in Experimental protocol tab.
    #     Save task table to a csv file.
    #     """
    #     _, self.protocol = self.get_task_name_table_content()
    #     self.saveFileNameDialog_protocol()
    #     # Utils.save_protocol_to_csv(protocol, "exp. protocol.csv")
    #     self.ui.statusBar.showMessage("protocol saved to {}".format(Variables.get_protocol_path()))

    # def onClicked_button_save_event_number(self):
    #     """
    #     Event listener for save button in Event and File Management tab.
    #     Save task name and event number to Run1/event.csv
    #     """
    #     event_dict = self.get_event_number_table_content()
    #     Utils.write_event_number_to_csv(event_dict)

    # def onActivated_checkbox_bandpass(self):
    #     """
    #     Event listener for check box in front of Bandpass filter in Oscilloscope tab.
    #     Check to bandpass filter displayed signal.
    #     """
    #     self.apply_bandpass = False
    #     self.ui.pushButton_bp.setEnabled(self.ui.checkBox_bandpass.isChecked())
    #     self.ui.doubleSpinBox_hp.setEnabled(self.ui.checkBox_bandpass.isChecked())
    #     self.ui.doubleSpinBox_lp.setEnabled(self.ui.checkBox_bandpass.isChecked())
    #     self.update_title_scope()
    #
    # def onActivated_checkbox_notch(self):
    #     """
    #     Event listener for check box in front of notch filter in Oscilloscope tab.
    #     Check to notch filter displayed signal.
    #     """
    #     self.apply_notch = False
    #     self.ui.pushButton_apply_notch.setEnabled(self.ui.checkBox_notch.isChecked())
    #     self.ui.doubleSpinBox_lc_notch.setEnabled(self.ui.checkBox_notch.isChecked())
    #     self.ui.doubleSpinBox_hc_notch.setEnabled(self.ui.checkBox_notch.isChecked())

    # def onActivated_checkbox_lowpass(self):
    #     self.apply_lowpass = False
    #     self.ui.pushButton_apply_lowpass.setEnabled(self.ui.checkBox_low_pass.isChecked())
    #     self.ui.doubleSpinBox_lc_lowpass.setEnabled(self.ui.checkBox_low_pass.isChecked())
    #
    # def onActivated_checkbox_highpass(self):
    #     self.apply_highpass = False
    #     self.ui.pushButton_apply_highpass.setEnabled(self.ui.checkBox_highpass.isChecked())
    #     self.ui.doubleSpinBox_lc_highpass.setEnabled(self.ui.checkBox_highpass.isChecked())

    # def onActivated_checkbox_car(self):
    #     """
    #     Event listener for check box in front of CAR filter in Oscilloscope tab.
    #     Apply Common Average Reference filter to displayed data if checked.
    #     """
    #     self.apply_car = self.ui.checkBox_car.isChecked()
    #     self.update_title_scope()

    # def onValueChanged_spinbox_time(self):
    #     """
    #     Event listener for spinbox of time in Scale Manager of Oscilloscope tab
    #     """
    #     self.update_plot_seconds(self.ui.spinBox_time.value())

    # def onActivated_combobox_scale(self):
    #     """
    #     Event listener for scale of data in Scale Manager of Oscilloscope tab
    #     """
    #     self.update_plot_scale(self.scales_range[self.ui.comboBox_scale.currentIndex()])

    # def onClicked_button_bp(self):
    #     """
    #     Event listener for Apply BP button in Filter Manager in Oscilloscope tab
    #     Apply BPF to displaying data
    #     """
    #     if self.ui.checkBox_change_filter.isChecked():
    #         if (self.ui.doubleSpinBox_lp.value() > self.ui.doubleSpinBox_hp.value()):
    #             self.apply_bandpass = True
    #             self.b_bandpass_scope_refilter, self.a_bandpass_scope_refilter, self.zi_bandpass_scope_refilter = \
    #                 Utils.butter_bandpass_scope(
    #                 self.ui.doubleSpinBox_hp.value(),
    #                 self.ui.doubleSpinBox_lp.value(),
    #                 self.config['sf'],
    #                 self.config['eeg_channels'])
    #     else:
    #         if (self.ui.doubleSpinBox_lp.value() > self.ui.doubleSpinBox_hp.value()):
    #             self.apply_bandpass = True
    #             self.b_bandpass_scope, self.a_bandpass_scope, self.zi_bandpass_scope = Utils.butter_bandpass_scope(
    #                 self.ui.doubleSpinBox_hp.value(),
    #                 self.ui.doubleSpinBox_lp.value(),
    #                 self.config['sf'],
    #                 self.config['eeg_channels'])
    #         self.update_title_scope()

    # def onClicked_button_notch(self):
    #     """
    #     Event listener for Apply Notch in Filter Manager in Oscilloscope tab
    #     Apply notch filter to displaying data
    #     """
    #     if self.ui.checkBox_change_filter.isChecked():
    #         if (self.ui.doubleSpinBox_hc_notch.value() > self.ui.doubleSpinBox_lc_notch.value()):
    #             self.apply_notch = True
    #             self.b_notch_scope_refilter, self.a_notch_scope_refilter, self.zi_notch_scope_refilter = \
    #                 Utils.butter_notch_scope(
    #                 self.ui.doubleSpinBox_hc_notch.value(),
    #                 self.ui.doubleSpinBox_lc_notch.value(),
    #                 self.config['sf'],
    #                 self.config['eeg_channels'])
    #     else:
    #         if (self.ui.doubleSpinBox_hc_notch.value() > self.ui.doubleSpinBox_lc_notch.value()):
    #             self.apply_notch = True
    #             self.b_notch_scope, self.a_notch_scope, self.zi_notch_scope = Utils.butter_notch_scope(
    #                 self.ui.doubleSpinBox_hc_notch.value(),
    #                 self.ui.doubleSpinBox_lc_notch.value(),
    #                 self.config['sf'],
    #                 self.config['eeg_channels'])


    # def onDoubleClicked_channel_table(self):
    #     for idx in self.ui.table_channels.selectionModel().selectedIndexes():
    #         self.selected_channel_row_index = idx.row()
    #         self.selected_channel_column_index = idx.column()
    #         print("ch index: {}, {}".format(self.selected_channel_row_index, self.selected_channel_column_index))

    # def onClicked_button_update_channel_name(self):
    #     """
    #     Update channel name by double clicking channel name in channel manager and click update channel name
    #     to update them in Oscilloscope
    #     """
    #
    #     # self.channel_labels[self.selected_channel_column_index * 16 + self.selected_channel_row_index] = \
    #     #     self.ui.table_channels.item(self.selected_channel_row_index, self.selected_channel_column_index).text()
    #     idx = 0
    #     new_channel_labels = []
    #     for y in range(0, 4):
    #         for x in range(0, NUM_X_CHANNELS):
    #             if (idx < self.config['eeg_channels']):
    #                 new_channel_labels.append(self.ui.table_channels.item(x, y).text())
    #                 idx += 1
    #     self.channel_labels = np.asarray(new_channel_labels)
    #     print("channel labels: {}".format(self.channel_labels))

    # def onSelectionChanged_table(self):
    #     """
    #     Update highlighted channels in Channel Manager when different channels are selected
    #     """
    #     # Remove current plot
    #     for x in range(0, len(self.channels_to_show_idx)):
    #         self.main_plot_handler.removeItem(self.curve_eeg[x])
    #
    #     # Which channels should I plot?
    #     self.channels_to_show_idx = []
    #     self.channels_to_hide_idx = []
    #     idx = 0
    #     for y in range(0, 4):
    #         for x in range(0, NUM_X_CHANNELS):
    #             if (idx < self.config['eeg_channels']):
    #                 if (QTableWidgetItem.isSelected(  # Qt5
    #                         self.ui.table_channels.item(x, y))):
    #                     self.channels_to_show_idx.append(idx)
    #                 else:
    #                     self.channels_to_hide_idx.append(idx)
    #                 idx += 1
    #
    #     # Add new plots
    #     self.curve_eeg = []
    #     for x in range(0, len(self.channels_to_show_idx)):
    #         self.curve_eeg.append(self.main_plot_handler.plot(x=self.x_ticks,
    #                                                           y=self.data_plot[:, self.channels_to_show_idx[x]],
    #                                                           pen=self.colors[
    #                                                               self.channels_to_show_idx[x] % NUM_X_CHANNELS, :]))
    #         self.curve_eeg[-1].setDownsampling(ds=self.subsampling_value,
    #                                            auto=False, method="mean")
    #
    #     # Update CAR so it's computed based only on the shown channels
    #     if (len(self.channels_to_show_idx) > 1):
    #         self.matrix_car = np.zeros(
    #             (self.config['eeg_channels'], self.config['eeg_channels']),
    #             dtype=float)
    #         self.matrix_car[:, :] = -1 / float(len(self.channels_to_show_idx))
    #         np.fill_diagonal(self.matrix_car,
    #                          1 - (1 / float(len(self.channels_to_show_idx))))
    #         for x in range(0, len(self.channels_to_hide_idx)):
    #             self.matrix_car[self.channels_to_hide_idx[x], :] = 0
    #             self.matrix_car[:, self.channels_to_hide_idx[x]] = 0
    #
    #     # Refresh the plot
    #     self.update_plot_scale(self.scale)

        #

    # def keyPressEvent(self, event):
    #     """
    #     Event listeners for different key button pressed
    #     Example: When there is a channel name been typed in channel names box in Sub channel manager in
    #              Oscilloscope, and change scale is checked, pressing up and down button will increase
    #              and decrease that channels' scale respectively
    #     """
    #     key = event.key()
    #     # if (key == QtCore.Qt.Key_Escape):
    #     #     self.closeEvent(None)
    #     if (key == QtCore.Qt.Key_H):
    #         self.show_help = not self.show_help
    #         self.trigger_help()
    #     if (key == QtCore.Qt.Key_Up):
    #         # Python's log(x, 10) has a rounding bug. Use log10(x) instead.
    #         # new_scale = self.scale + max(1, 10 ** int(math.log10(self.scale)))
    #         # self.update_plot_scale(new_scale)
    #         self.single_channel_scale *= 2
    #     if (key == QtCore.Qt.Key_Space):
    #         self.stop_plot = not self.stop_plot
    #     if (key == QtCore.Qt.Key_Down):
    #         if self.single_channel_scale >= 0:
    #             self.single_channel_scale /= 2
    #         else:
    #             self.single_channel_scale = 1
    #
    #     if (key == QtCore.Qt.Key_Left):
    #         self.update_plot_seconds(self.seconds_to_show - 1)
    #     if (key == QtCore.Qt.Key_Right):
    #         self.update_plot_seconds(self.seconds_to_show + 1)
    #     if (key == QtCore.Qt.Key_C):
    #         self.ui.checkBox_car.setChecked(not self.ui.checkBox_car.isChecked())
    #     if (key == QtCore.Qt.Key_B):
    #         self.ui.checkBox_bandpass.setChecked(
    #             not self.ui.checkBox_bandpass.isChecked())
    #         if self.ui.checkBox_bandpass.isChecked():
    #             self.ui.pushButton_bp.click()
    #     if ((key >= QtCore.Qt.Key_0) and (key <= QtCore.Qt.Key_9)):
    #         if (self.show_Key_events) and (not self.stop_plot):
    #             self.addEventPlot("KEY", 990 + key - QtCore.Qt.Key_0)

    #
    # def onClicked_button_temp_view(self):
    #     """
    #     Event listener for View button in Online Experiment tab.
    #     View selected trials
    #     """
    #     try:
    #         self.get_input_temp()
    #         self.display_temp_list = self.input_temp_list
    #         self.ui.label_content_Disp_temp.setText("{}".format(self.display_temp_list))
    #         self.plot_display_temp()
    #     except Exception as e:
    #         logger.exception('Exception. Dropping into a shell.')
    #         print(str(e))
    #     finally:
    #         pass
    #
    # def onClicked_button_temp_remove(self):
    #     """
    #     Event listener for Remove button in Onlin Experiment tab.
    #     Remove selected trials
    #     """
    #     try:
    #         self.get_input_temp()
    #         for element in self.input_temp_list:
    #             del self.total_trials_MRCP[element - 1]
    #         # self.display_temp_list = [x for x in self.total_MRCP_inds if x not in self.input_temp_list]
    #         self.display_temp_list = list(range(1, len(self.total_trials_MRCP) + 1))
    #         self.ui.label_content_Disp_temp.setText("{}".format(self.display_temp_list))
    #         self.ui.label_content_available_temp.setText("{}".format(self.display_temp_list))
    #         self.plot_display_temp()
    #     except Exception as e:
    #         logger.exception('Exception. Dropping into a shell.')
    #         print(str(e))
    #     finally:
    #         pass
    #
    # def onClicked_button_temp_clear(self):
    #     """
    #     Event listener for Clear button in Online Experiment tab
    #     Clear MRCP plot
    #     """
    #     self.ui.graphicsView.clear()
    #
    # def onClicked_button_temp_mean(self):
    #     """
    #     Event listener for Mean button in Online Experiment tab
    #     Calculate mean of all templates
    #     """
    #     try:
    #         self.mean_MRCP = np.mean(self.total_trials_MRCP, 0)
    #         self.ui.graphicsView.clear()
    #         self.MRCP_plot(self.mean_MRCP)
    #     except Exception as e:
    #         logger.exception('Exception. Dropping into a shell.')
    #         print(str(e))
    #     finally:
    #         pass

    # def onClicked_button_bad_epoch(self):
    #     """
    #     Event listener for bad epoch button in Online Experimente tab
    #     Record bad epochs during the experiment, the bad epoch number will be saved to Run1/bad_epochs.csv
    #     :return:
    #     """
    #     current_task = self.new_task_list[self.task_counter]
    #     row_number = self.unique_task_list.tolist().index(current_task)
    #     epoch_number = self.find_epoch_number()
    #     self.bad_epoch_dict[current_task].append(epoch_number+1)
    #     self.ui.tableWidget_bad_epoch.setItem(row_number, 1, QTableWidgetItem(str(self.bad_epoch_dict[current_task])))
    #     # self.ui.tableWidget_class_epoch_counter.viewport().update()
