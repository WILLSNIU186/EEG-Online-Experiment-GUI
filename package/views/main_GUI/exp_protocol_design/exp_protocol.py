
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
import numpy as np
from package.entity.edata.utils import Utils
from package.entity.edata.variables import Variables


class ExpProtocol():
    """
    save and load experimental protocols and finish whole exp design
    """
    def onClicked_button_save_protocol(self):
        """
        Event listener for Save current protocol button in Experimental protocol tab.
        Save task table to a csv file.
        """
        _, self.protocol = self.get_task_name_table_content()
        self.saveFileNameDialog_protocol()
        # Utils.save_protocol_to_csv(protocol, "exp. protocol.csv")
        self.ui.statusBar.showMessage("protocol saved to {}".format(Variables.get_protocol_path()))

    def onClicked_toolButton_load_protocol(self):
        """
        Event listener for load exp. protocol button
        Open folder to choose existing experimental protocol files
        """
        self.openFileNameDialog_protocol()

    def onClicked_experimental_protocol_finish(self):
        """
        Event listener for Finish button in experimental protocol tab.
        Disable all inputs in this tab and save Task table into variable to be used for generating tasks.
        """
        self.ui.tab_experimental_protocol.setEnabled(False)
        self.new_task_list = self.new_task_table[:,0].tolist()
        self.unique_task_list = np.unique(self.new_task_list)
        self.event_list = self.unique_task_list.tolist() + ['Idle', 'Focus', 'Prepare', 'Two', 'One', 'Task']
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
        # write to class epoch counter table
        self.ui.tableWidget_class_epoch_counter.setRowCount(len(self.unique_task_list))
        for i in range(len(self.unique_task_list)):
            self.ui.tableWidget_class_epoch_counter.setItem(i, 0, QTableWidgetItem(self.unique_task_list[i]))
        # write to bad epoch table
        self.ui.tableWidget_bad_epoch.setRowCount(len(self.unique_task_list))
        for i in range(len(self.unique_task_list)):
            self.ui.tableWidget_bad_epoch.setItem(i, 0, QTableWidgetItem(self.unique_task_list[i]))
        # create bad epoch dict
        self.bad_epoch_dict = {k: [] for k in self.unique_task_list}




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