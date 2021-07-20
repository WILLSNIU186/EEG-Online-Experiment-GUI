import numpy as np
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem

class SequenceManager():

    def onClicked_button_create_sequence(self):
        """
        Event listener for create sequence button in Experimental Protocol tab.
        The listed tasks will be iterated 'group number' times in the Task table
        """
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
        """
        Event listener for Randomize button in Experimental protocol
        Randomize the order of tasks in Task table
        """
        np.random.shuffle(self.new_task_table)
        self.ui.tableWidget_tasks.setRowCount(self.new_task_table.shape[0])
        for i in range(self.new_task_table.shape[0]):
            self.ui.tableWidget_tasks.setItem(i, 0, QTableWidgetItem(self.new_task_table[i][0]))
            self.ui.tableWidget_tasks.setItem(i, 1, QTableWidgetItem(self.new_task_table[i][1]))
            self.ui.tableWidget_tasks.setItem(i, 2, QTableWidgetItem(self.new_task_table[i][2]))
            self.ui.tableWidget_tasks.setItem(i, 3, QTableWidgetItem(self.new_task_table[i][3]))