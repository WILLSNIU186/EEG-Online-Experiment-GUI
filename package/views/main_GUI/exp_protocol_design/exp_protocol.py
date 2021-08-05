
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
import numpy as np
from package.entity.edata.utils import Utils
from package.entity.edata.variables import Variables
from package.entity.base.protocol import Protocol


class ExpProtocol():
    """
    save and load experimental protocols and finish whole exp design
    """
    def onClicked_button_save_protocol(self):
        """
        Event listener for Save current protocol button in Experimental protocol tab.
        Save task table to a csv file.
        """
        protocol_path = self.saveFileNameDialog_protocol()
        self.protocol.save_protocol(protocol_path)
        Variables.set_protocol_path(protocol_path)
        self.ui.statusBar.showMessage("protocol saved to {}".format(Variables.get_protocol_path()))

    def onClicked_toolButton_load_protocol(self):
        """
        Event listener for load exp. protocol button
        Open folder to choose existing experimental protocol files
        """
        protocol_path = self.openFileNameDialog_protocol()
        self.protocol = Protocol.load_protocol(protocol_path)

        self.write_protocol_to_task_table()
        self.write_protocol_to_cue_table()

    def onClicked_experimental_protocol_finish(self):
        """
        Event listener for Finish button in experimental protocol tab.
        Disable all inputs in this tab and save Task table into variable to be used for generating tasks.
        """
        self.ui.tab_experimental_protocol.setEnabled(False)
        # self.new_task_list = self.new_task_table[:,0].tolist()
        # self.unique_task_list = np.unique(self.new_task_list)
        # self.event_list = self.unique_task_list.tolist() + ['Idle', 'Focus', 'Prepare', 'Two', 'One', 'Task']

        # total_event_num = len(self.protocol.task_list) + len(self.protocol.task_list[0].cue_list)
        #
        # self.ui.tableWidget_task_event_number.setRowCount(total_event_num)
        # for x in range(len(self.protocol.task_list)):
        #     self.ui.tableWidget_task_event_number.setItem(x, 0, QTableWidgetItem(self.protocol.task_list[x].name))
        # for y in np.arange(x+1, x + 1 + len(self.protocol.task_list[0].cue_list)):
        #     self.ui.tableWidget_task_event_number.setItem(y, 0, QTableWidgetItem(self.protocol.task_list[0].cue_list[y-x-1].name))

        self.protocol.set_break_trial_number(int(self.ui.lineEdit_break_trial_number.text()))
        self.write_task_to_epoch_table()
        #
        #
        # self.idle_time = int(self.ui.idleTimeLineEdit.text())
        # self.focus_time = self.idle_time + int(self.ui.focusTimeLineEdit.text())
        # self.prepare_time = self.focus_time + int(self.ui.prepareTimeLineEdit.text())
        # self.two_time = self.prepare_time + int(self.ui.twoTimeLineEdit.text())
        # self.one_time = self.two_time + int(self.ui.oneTimeLineEdit.text())
        # self.task_time = self.one_time + int(self.ui.taskTimeLineEdit.text())
        # self.relax_time = self.task_time + 2
        # self.cycle_time = self.relax_time

        # # write to class epoch counter table
        # self.ui.tableWidget_class_epoch_counter.setRowCount(len(self.protocol.task_list))
        # for i in range(len(self.protocol.task_list)):
        #     self.ui.tableWidget_class_epoch_counter.setItem(i, 0, QTableWidgetItem(self.task_list[i].name))
        # # write to bad epoch table
        # self.ui.tableWidget_bad_epoch.setRowCount(len(self.protocol.task_list))
        # for i in range(len(self.protocol.task_list)):
        #     self.ui.tableWidget_bad_epoch.setItem(i, 0, QTableWidgetItem(self.task_list[i].name))
        # create bad epoch dict





    def openFileNameDialog_protocol(self):
        """
        Open foldre to choose saved experimental protocal.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()",
                                                  r"experimental_protocols",
                                                  "csv files (*.pickle)", options=options)
        if fileName:
            print(fileName)
            return fileName
            # self.protocol_path = fileName
            # self.load_protocol()
        # else:
        #     self.protocol_path = " "

    def write_protocol_to_task_table(self):
        """
        write existing experimental protocal to task table
        """
        if len(self.protocol.trial_list) > 0:
            self.ui.tableWidget_tasks.setRowCount(len(self.protocol.trial_list))
            for row in range(len(self.protocol.trial_list)):
                for col in range(5):
                    self.ui.tableWidget_tasks.setItem(row, 0, QTableWidgetItem(self.protocol.trial_list[row].name))
                    self.ui.tableWidget_tasks.setItem(row, 1, QTableWidgetItem(str(self.protocol.trial_list[row].event_number)))
                    self.ui.tableWidget_tasks.setItem(row, 2, QTableWidgetItem(self.protocol.trial_list[row].desc_name))
                    self.ui.tableWidget_tasks.setItem(row, 3, QTableWidgetItem(self.protocol.trial_list[row].image))
                    self.ui.tableWidget_tasks.setItem(row, 4, QTableWidgetItem(self.protocol.trial_list[row].sound))
            self.ui.groupBox_sequence_manager.setEnabled(True)
            self.ui.groupBox_task_manager.setEnabled(True)

    def write_protocol_to_cue_table(self):
        """
        write existing experimental protocal to cue table
        TODO: Don't assume every trial has same cues
        """
        if len(self.protocol.trial_list[0].cue_list) >0:
            self.ui.tableWidget_cue.setRowCount(len(self.protocol.trial_list[0].cue_list))
            for row in range(len(self.protocol.trial_list[0].cue_list)):
                for col in range(5):
                    self.ui.tableWidget_cue.setItem(row, 0, QTableWidgetItem(self.protocol.trial_list[0].cue_list[row].name))
                    self.ui.tableWidget_cue.setItem(row, 1, QTableWidgetItem(str(self.protocol.trial_list[0].cue_list[row].event_number)))
                    self.ui.tableWidget_cue.setItem(row, 2, QTableWidgetItem(str(self.protocol.trial_list[0].cue_list[row].duration)))
                    self.ui.tableWidget_cue.setItem(row, 3, QTableWidgetItem(self.protocol.trial_list[0].cue_list[row].image))
                    self.ui.tableWidget_cue.setItem(row, 4, QTableWidgetItem(self.protocol.trial_list[0].cue_list[row].sound))




    def saveFileNameDialog_protocol(self):
        """
        Save current tasks listed in the task table to an experimental protocal file.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()",
                                                  r"experimental_protocols",
                                                  "csv files (*.pickle)", options=options)
        if fileName:
            print(fileName)
            return fileName

    # def get_task_name_table_content(self):
    #     """
    #     Get task name, task description, image path and sound path from task name table in experimenter GUI
    #     :return: lists of table content
    #     """
    #     self.task_list = []
    #     self.task_descriptor_list = []
    #     self.task_image_path_list = []
    #     self.task_sound_path_list = []
    #     task_table = np.ndarray([])
    #     task_table_list = []
    #     for i in range(self.ui.tableWidget_tasks.rowCount()):
    #         self.task_list.append(self.ui.tableWidget_tasks.item(i, 0).text())
    #         self.task_descriptor_list.append(self.ui.tableWidget_tasks.item(i, 1).text())
    #         self.task_image_path_list.append(self.ui.tableWidget_tasks.item(i, 2).text())
    #         self.task_sound_path_list.append(self.ui.tableWidget_tasks.item(i, 3).text())
    #     task_table_list.append(self.task_list)
    #     task_table_list.append(self.task_descriptor_list)
    #     task_table_list.append(self.task_image_path_list)
    #     task_table_list.append(self.task_sound_path_list)
    #     task_table = np.c_[np.asarray(self.task_list),
    #                        np.asarray(self.task_descriptor_list),
    #                        np.asarray(self.task_image_path_list),
    #                        np.asarray(self.task_sound_path_list)]
    #     print("tasks list:\n", task_table)
    #     task_table_list = np.transpose(np.asarray(task_table_list))
    #     return task_table, task_table_list