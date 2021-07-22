from PyQt5.QtWidgets import QTableWidgetItem
from package.entity.edata.variables import Variables

class FilePathManager():
    def init_table_file_path(self):
        """
        Initialize file path table in Event and File Management tab
        """
        self.ui.tableWidget_file_path.setColumnCount(2)
        self.ui.tableWidget_file_path.setHorizontalHeaderLabels(["File name", "File path"])


    def update_table_file_path(self):
        """
        Update content in File Path table.
        """
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
