import socket
import numpy as np
from PyQt5 import QtWidgets

class EyeTracker():
    def onClicked_pushButton_open_eye_tracker_ui(self):
        self.eye_tracker_dialog.show()


    def update_rec_time(self, rec_time):
        return rec_time


    def loaddata(self):
        self.table_col = 0
        self.tableWidget.setItem(self.table_row, self.table_col, QtWidgets.QTableWidgetItem(str(self.gaze_x)))
        self.tableWidget.setItem(self.table_row, self.table_col+1, QtWidgets.QTableWidgetItem(str(self.gaze_y)))

        print(self.gaze_x, self.gaze_y)
        print(self.table_row, self.table_col)


    def update_cal1(self):
        self.collect_data()
        # self.points[0,0], self.points[0,1] = self.gaze_x, self.gaze_y
        self.table_row =  0
        self.loaddata()

    def update_cal2(self):
        self.collect_data()
        self.table_row = 1
        self.loaddata()

    def update_cal3(self):
        self.collect_data()
        self.table_row = 2
        self.loaddata()

    def update_cal4(self):
        self.collect_data()
        self.table_row = 3
        self.loaddata()

    def update_cal5(self):
        self.collect_data()
        self.table_row = 4
        self.loaddata()

    def update_cal6(self):
        self.collect_data()
        self.table_row = 5
        self.loaddata()

    def update_cal7(self):
        self.collect_data()
        self.table_row = 6
        self.loaddata()

    def update_cal8(self):
        self.collect_data()
        self.table_row = 7
        self.loaddata()

    def update_cal9(self):
        self.collect_data()
        self.table_row = 8
        self.loaddata()



    def collect_data(self):
        # Create a TCP/IP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = '10.32.140.57'
        s.connect((addr, 9015))
        # streaming data ~ 1024 'buffer size' [bytes]
        msg = s.recv(1024)
        # msg_d = msg.decode("utf-8")
        # print(msg.decode("utf-8"))

        a = msg.decode("utf-8").split('\t', 3)
        a[3] = a[3].split('\r\n', 1)[0]

        chunk = np.zeros((60, 3))
        stack = np.zeros(3)

        i = 0
        while (i < 60):
            msg = s.recv(1024)
            # msg_d = msg.decode("utf-8")
            a = msg.decode("utf-8").split('\t', 3)
            stack[0] = int(a[0])
            stack[1] = "{0:.2f}".format(float(a[2]))
            stack[2] = "{0:.2f}".format(float(a[3].split('\r\n', 1)[0]))

            chunk[i] = stack

            i += 1

        chunk = np.array(chunk)
        # print(chunk[0,0])
        chunk[:, 0] = chunk[:, 0] - chunk[0, 0]

        ## average - outliner elimination
        gaze_x = chunk[:, 1]
        gaze_y = chunk[:, 2]

        avg_x = np.mean(gaze_x)
        avg_y = np.mean(gaze_y)
        std_x = np.std(gaze_x)
        std_y = np.std(gaze_y)

        print(avg_x, avg_y, std_x, std_y)

        self.gaze_x = avg_x
        self.gaze_y = avg_y

        # blin = avg_x-std_x avg_x+std_x

        blin_x = np.array(np.where(np.logical_and(gaze_x >= avg_x - std_x, gaze_x <= avg_x + std_x)))
        blin_y = np.array(np.where(np.logical_and(gaze_y >= avg_y - std_y, gaze_y <= avg_y + std_y)))
        sel_x = gaze_x[blin_x[0, :]]
        sel_y = gaze_y[blin_y[0, :]]

    def recording_stop(self):
        # self.record_stop = 0
        self.router.stop_eye_tracker_recording()

    def recording_data(self, pressed):
        self.rec_time = self.update_rec_time(self.eye_tracker_window.LineEdit_rec.text())
        # print(self.rec_time)

        if pressed:
            self.router.start_eye_tracker_recording()
            # self.record_start.thread_record(self.rec_time)

        elif pressed == False:
            self.router.stop_eye_tracker_recording()
            # self.record_start.thread_record(self.rec_time)



    def update_current_gaze_loc(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = '10.32.140.57'
        s.connect((addr, 9015))
        # streaming data ~ 1024 'buffer size' [bytes]
        msg = s.recv(1024)
        # msg_d = msg.decode("utf-8")
        # print(msg.decode("utf-8"))

        a = msg.decode("utf-8").split('\t', 3)
        a[3] = a[3].split('\r\n', 1)[0]

        # chunk = np.zeros((60, 3))
        stack = np.zeros(3)

        i = 0
        while True:
            msg = s.recv(1024)
            # msg_d = msg.decode("utf-8")
            a = msg.decode("utf-8").split('\t', 3)
            stack[0] = int(a[0])
            stack[1] = "{0:.2f}".format(float(a[2]))
            stack[2] = "{0:.2f}".format(float(a[3].split('\r\n', 1)[0]))

            # chunk[i] = stack

            i += 1





