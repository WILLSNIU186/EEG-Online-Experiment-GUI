
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
import numpy as np
from package.entity.edata.utils import Utils
from package.entity.edata.variables import Variables
from package.entity.base.protocol import Protocol
import pdb


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
        self.protocol.set_break_trial_number(int(self.ui.lineEdit_break_trial_number.text()))
        self.write_task_to_epoch_table()
        event_annotation_dict = {}
        for task in self.protocol.task_list:
            event_annotation_dict[task.name] = task.event_number
            for cue in task.cue_list:
                event_annotation_dict[cue.name] = cue.event_number
        Utils.write_event_number_to_csv(event_annotation_dict)



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
