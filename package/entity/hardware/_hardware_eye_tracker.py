import socket
import csv
import numpy as np
import time

class HardwareAdditionalMethods:
    def record(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = '10.32.140.57'
        s.connect((addr, 9015))
        csvfile = open('file_test4.csv', 'w', newline='')
        # csvfile = open('file_test4.csv', 'w')
        writer = csv.writer(csvfile)
        stack = np.zeros(5)

        self.is_on = True
        counter = 0


        while self.is_on:
        # for i in range(10):
            # while self.is_recording_running:

            msg = s.recv(1024)
            # msg_d = msg.decode("utf-8")
            a = msg.decode("utf-8").split('\t', 3)
            # print(a)
            stack[0] = int(a[0])
            stack[1] = "{0:.2f}".format(float(a[2]))
            stack[2] = "{0:.2f}".format(float(a[3].split('\r\n', 1)[0]))
            t = time.time()
            stack[3] = float("{:.4f}".format(t - int(t / 10000) * 10000))

            writer.writerow(stack)

            time.sleep(0.016)
            counter += 1
            # rec_time: Recording time [s]
            if counter > 130*60:
                csvfile.close()
                self.is_on = False
                print("done")