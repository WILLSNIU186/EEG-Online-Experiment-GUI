from PyQt5.QtWidgets import QTableWidgetItem
import numpy as np

class BadEpochMonitor():
    def onClicked_button_bad_epoch(self):
        """
        Event listener for bad epoch button in Online Experimente tab
        Record bad epochs during the experiment, the bad epoch number will be saved to Run1/bad_epochs.csv
        :return:
        """
        # current_task = self.new_task_list[self.task_counter]
        # row_number = self.unique_task_list.tolist().index(current_task)
        # epoch_number = self.find_epoch_number()
        # self.bad_epoch_dict[self.protocol.trial_list[self.trial_counter].name].append(self.trial_counter+1)
        # self.ui.tableWidget_bad_epoch.setItem(row_number, 1, QTableWidgetItem(str(self.bad_epoch_dict[current_task])))

        self.bad_epoch.add_bad_epoch(self.protocol.trial_list[self.trial_counter].name, self.trial_counter)
        for row_number in range(len(self.protocol.task_list)):
            if self.protocol.trial_list[self.trial_counter].name == \
               self.ui.tableWidget_bad_epoch.item(row_number, 0).text():

                self.ui.tableWidget_bad_epoch.setItem(row_number, 1, \
                                                      QTableWidgetItem(str(self.bad_epoch.bad_epoch_dict[self.protocol.trial_list[self.trial_counter].name])))
                self.ui.tableWidget_bad_epoch.viewport().update()
                self.ui.tableWidget_bad_epoch.selectRow(row_number)


        # self.ui.tableWidget_class_epoch_counter.viewport().update()

    # def find_epoch_number(self):
    #     """
    #     Get the current epoch number in its own class to show it in task monitor in Online Experiment tab
    #     :return the index of this epoch in its own class
    #
    #     """
    #     current_task = self.trial_counter + 1
    #     return current_task


    def set_epoch_number(self):
        """
        Display current task epoch number in its own task in task monitor in Online Experiment tab
        """
        # current_task = self.new_task_list[self.task_counter]
        # row_number = self.unique_task_list.tolist().index(current_task)
        # epoch_number = self.find_epoch_number()
        # epoch_number = self.trial_counter

        for row_number in range(len(self.protocol.task_list)):
            if self.protocol.trial_list[self.trial_counter].name == \
               self.ui.tableWidget_class_epoch_counter.item(row_number, 0).text():

                self.ui.tableWidget_class_epoch_counter.setItem(row_number, 1, \
                                                                QTableWidgetItem(str(self.trial_counter + 1)))
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

    def write_task_to_epoch_table(self):
        # write to class epoch counter table
        self.ui.tableWidget_class_epoch_counter.setRowCount(len(self.protocol.task_list))
        for i in range(len(self.protocol.task_list)):
            self.ui.tableWidget_class_epoch_counter.setItem(i, 0, QTableWidgetItem(self.protocol.task_list[i].name))
        # write to bad epoch table
        self.ui.tableWidget_bad_epoch.setRowCount(len(self.protocol.task_list))
        for i in range(len(self.protocol.task_list)):
            self.ui.tableWidget_bad_epoch.setItem(i, 0, QTableWidgetItem(self.protocol.task_list[i].name))

        # initialize bad_epoch dict with current task names
        self.bad_epoch.add_events(self.protocol.task_list)

        # for i in range(len(self.protocol.task_list)):
            # self.bad_epoch_dict[self.protocol.task_list[i].name] = []