
import subprocess

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from package.views.layouts import record_replay
import pycnbi.stream_player.stream_player as sp
import threading

class RecordReplaySelector():
    """

    RecordReplay chooses whether to record new data from device or replay recorded .fif data

    """

    def __init__(self):
        self.replay_record_window = QMainWindow()
        self.mode_window = record_replay.Ui_MainWindow()
        self.mode_window.setupUi(self.replay_record_window)
        self.init_GUI()
        self.replay_record_window.show()
        self.button_clicked = False
        while not self.button_clicked:
            QCoreApplication.processEvents()

    def init_GUI(self):
        """
        Initialize replay record GUI
        """
        self.mode_window.pushButton_record.clicked.connect(self.onClicked_pushButton_record)
        self.mode_window.pushButton_replay.clicked.connect(self.onClicked_pushButton_replay)

    def onClicked_pushButton_record(self):
        """
        Event listener for record button.
        """
        QCoreApplication.processEvents()
        self.button_clicked = True
        self.replay_record_window.hide()

    def onClicked_pushButton_replay(self):
        """Event listener for replay button"""
        self.openFileNameDialog()

    def openFileNameDialog(self):
        """
        Open folder to choose processed .fif file.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, "find your .fif file",
                                                  r"sample_data/",
                                                  "fif files (*.fif)", options=options)
        if fileName:
            self.path = fileName
            self.run_stream_player()
            self.replay_record_window.hide()
            self.button_clicked = True

        else:
            self.path = " "

    def run_stream_player(self):
        """Run stream player with selected .fif file"""

        server_name = 'StreamPlayer'
        chunk_size = 8  # chunk streaming frequency in Hz
        print(self.path)
        command = ["python", "lib\\neurodecode-master\pycnbi\stream_player\stream_player.py", self.path]

        p = subprocess.Popen(command)
        # subprocess.Popen('python C:\\Users\WILLS\PycharmProjects\\uw_eboinics_experimental_interface\lib\\neurodecode-master\pycnbi\stream_player\stream_player.py self.path')
        # self.thread = threading.Thread(target=sp.stream_player(server_name, fif_file, chunk_size))
        # self.thread.start()

        # sp.stream_player(server_name, fif_file, chunk_size)
