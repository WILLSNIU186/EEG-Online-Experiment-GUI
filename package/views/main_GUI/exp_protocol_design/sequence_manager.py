import numpy as np
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem

class SequenceManager():

    def onClicked_button_create_sequence(self):
        """
        Event listener for create sequence button in Experimental Protocol tab.
        The listed tasks will be iterated 'group number' times in the Task table
        """
        group_number = int(self.ui.lineEdit_group_number.text())
        self.protocol.create_sequence(group_number)

        self.ui.tableWidget_tasks.setRowCount(len(self.protocol.trial_list))
        for i in range(len(self.protocol.trial_list)):
            self.ui.tableWidget_tasks.setItem(i, 0, QTableWidgetItem(self.protocol.trial_list[i].name))
            self.ui.tableWidget_tasks.setItem(i, 1, QTableWidgetItem(str(self.protocol.trial_list[i].event_number)))
            self.ui.tableWidget_tasks.setItem(i, 2, QTableWidgetItem(self.protocol.trial_list[i].desc_name))
            self.ui.tableWidget_tasks.setItem(i, 3, QTableWidgetItem(self.protocol.trial_list[i].image))
            self.ui.tableWidget_tasks.setItem(i, 4, QTableWidgetItem(self.protocol.trial_list[i].sound))

    def onClicked_button_randomize(self):
        """
        Event listener for Randomize button in Experimental protocol
        Randomize the order of tasks in Task table
        """

        self.protocol.randomize_order()
        self.ui.tableWidget_tasks.setRowCount(len(self.protocol.trial_list))
        for i in range(len(self.protocol.trial_list)):
            self.ui.tableWidget_tasks.setItem(i, 0, QTableWidgetItem(self.protocol.trial_list[i].name))
            self.ui.tableWidget_tasks.setItem(i, 1, QTableWidgetItem(str(self.protocol.trial_list[i].event_number)))
            self.ui.tableWidget_tasks.setItem(i, 2, QTableWidgetItem(self.protocol.trial_list[i].desc_name))
            self.ui.tableWidget_tasks.setItem(i, 3, QTableWidgetItem(self.protocol.trial_list[i].image))
            self.ui.tableWidget_tasks.setItem(i, 4, QTableWidgetItem(self.protocol.trial_list[i].sound))