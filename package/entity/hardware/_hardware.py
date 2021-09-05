#!/ustreamReceiver/bin/env python
import datetime
import os
import time

import numpy as np
import pycnbi.utils.q_common as qc
from pycnbi import logger
import csv
import pdb

from ..edata.variables import Variables


class HardwareAdditionalMethods:
    """
    HardwareAdditionalMethods controls heavy recording function in a separate thread
    """
    def record(self):
        """
        Continue recording data until the record stop button is pressed, the recorded data
        are firstly saved in a buffer which will be saved to a csv file during recording every 60s.
        """
        eeg_file = self.eeg_file_path
        logger.info(eeg_file)
        csvfile = open(eeg_file, 'w', newline='')
        writer = csv.writer(csvfile, delimiter=',')
        # start recording
        logger.info('\n>> Recording started (PID %d).' % os.getpid())
        tm = qc.Timer(autoreset=True)
        next_sec = 1
        counter = 0
        while self.is_recording_running:

            self.streamReceiver.acquire("recorder using")
            # print(self.streamReceiver.data_size)

            if self.streamReceiver.get_buflen() > next_sec:
                duration = str(datetime.timedelta(seconds=counter))
                logger.info('RECORDING %s' % duration)
                counter += 1
                next_sec += 1

            if self.streamReceiver.get_buflen() > 60:
                logger.info('writing to file ...')
                buffers, times = self.streamReceiver.get_buffer()
                new_lines = np.c_[times, buffers]
                writer.writerows(new_lines)
                self.streamReceiver.flush_buffer()
                next_sec = 1

            # self.streamReceiver.set_window_size(self.MRCP_window_size)
            # self.current_window, self.current_time_stamps = self.streamReceiver.get_window()
            tm.sleep_atleast(0.001)


        buffers, times = self.streamReceiver.get_buffer()
        new_lines = np.c_[times, buffers]
        writer.writerows(new_lines)
        csvfile.close()


    def write_recorded_data_to_csv(self, data):
        """
        Write buffer to Run1/raw_eeg.csv
        """
        eeg_file = self.eeg_file_path
        logger.info(eeg_file)
        raw_data_with_time_stamps = np.c_[data['timestamps'], data['signals']]
        with open(eeg_file, 'w') as f:
            np.savetxt(eeg_file, raw_data_with_time_stamps, delimiter=',', fmt='%.5f', header = '')

        logger.info('Saved to %s\n' % eeg_file)

    def write_timestamps_to_csv(self):
        """
        Write timestamps to Run1/event.csv
        """
        eeg_timestamp_file = Variables.get_raw_eeg_timestamp_file_path()
        logger.info(eeg_timestamp_file)
        # pdb.set_trace()
        time_stamps = np.c_[self.lsl_time_list, self.server_time_list, self.offset_time_list]
        with open(eeg_timestamp_file, 'w') as f:
            np.savetxt(eeg_timestamp_file, time_stamps, delimiter=',', fmt='%.5f', header = '')


