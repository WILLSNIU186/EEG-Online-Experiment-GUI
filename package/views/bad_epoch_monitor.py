from PyQt5.QtWidgets import QTableWidgetItem
import numpy as np

class BadEpochMonitor():
    def onClicked_button_bad_epoch(self):
        """
        Event listener for bad epoch button in Online Experimente tab
        Record bad epochs during the experiment, the bad epoch number will be saved to Run1/bad_epochs.csv
        :return:
        """
        current_task = self.new_task_list[self.task_counter]
        row_number = self.unique_task_list.tolist().index(current_task)
        epoch_number = self.find_epoch_number()
        self.bad_epoch_dict[current_task].append(epoch_number+1)
        self.ui.tableWidget_bad_epoch.setItem(row_number, 1, QTableWidgetItem(str(self.bad_epoch_dict[current_task])))
        # self.ui.tableWidget_class_epoch_counter.viewport().update()

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
