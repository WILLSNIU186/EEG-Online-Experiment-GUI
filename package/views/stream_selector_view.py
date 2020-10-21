from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow
from package.views.layouts import stream_slector_layout1
import pycnbi.utils.pycnbi_utils as pu
from package.entity.edata import variables


class StreamSelectorView():
    def __init__(self):
        self.stream_selector_window = QMainWindow()
        self.selector_window = stream_slector_layout1.Ui_MainWindow()
        self.selector_window.setupUi(self.stream_selector_window)
        self.init_GUI()
        self.confirm_clicked = True
        self.amp_list, self.streamInfos = pu.list_lsl_streams(window=self)
        while self.confirm_clicked:
            QCoreApplication.processEvents()

        # self.stream_selector_window.show()

    def init_GUI(self):
        self.selector_window.pushButton_confirm.clicked.connect(self.onClicked_pushButton_confirm)

    def onClicked_pushButton_confirm(self):
        self.confirm_clicked = False
        index = int(self.selector_window.lineEdit_stream_selected.text())
        amp_name, amp_serial = pu.search_lsl(amp_list=self.amp_list, streamInfos=self.streamInfos, index=index)
        variables.Variables.set_amp_name(amp_name)
        variables.Variables.set_amp_serial(amp_serial)
        self.stream_selector_window.hide()
