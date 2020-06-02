#!/ustreamReceiver/bin/env python
import os
import time
import datetime
import pycnbi.utils.q_common as qc
from pycnbi.utils.convert2fif import pcl2fif
from pycnbi.utils.cnbi_lsl import start_server
from pycnbi import logger
import pdb
import numpy as np
from ..edata.variables import Variables

class HardwareAdditionalMethods:
    def record(self):
        # set data file name

        timestamp = time.strftime('%Y%m%d-%H%M%S', time.localtime())
        # start recording
        logger.info('\n>> Recording started (PID %d).' % os.getpid())
        tm = qc.Timer(autoreset=True)
        next_sec = 1
        while self.is_recording_running:

            self.streamReceiver.acquire("recorder using")

            if self.streamReceiver.get_buflen() > next_sec:
                print("\nbuffer length: ",self.streamReceiver.get_buflen())
                duration = str(datetime.timedelta(seconds=int(self.streamReceiver.get_buflen())))
                logger.info('RECORDING %s' % duration)
                logger.info('\nLSL clock: %s' %self.streamReceiver.get_lsl_clock())
                logger.info('Server timestamp = %s' % self.streamReceiver.get_server_clock())
                next_sec += 1

            self.streamReceiver.set_window_size(self.MRCP_window_size)
            self.current_window, self.current_time_stamps = self.streamReceiver.get_window()
            tm.sleep_atleast(0.001)


        buffers, times = self.streamReceiver.get_buffer()
        signals = buffers
        events = None

        data = {'signals': signals, 'timestamps': times, 'events': events,
                'sample_rate': self.streamReceiver.get_sample_rate(), 'channels': self.streamReceiver.get_num_channels(),
                'ch_names': self.streamReceiver.get_channel_names(), 'lsl_time_offset': self.streamReceiver.lsl_time_offset}
        logger.info('Saving raw data ...')
        self.write_recorded_data_to_csv(data)
        print("timestamp len before flush", len(self.streamReceiver.timestamps[0]))
        print("buffer len before flushing: ", len(self.streamReceiver.buffers[0]))
        self.streamReceiver.flush_buffer()
        print("timestamp len after flush", len(self.streamReceiver.timestamps[0]))
        print("buffer len after flushing: ", len(self.streamReceiver.buffers[0]))


    def write_recorded_data_to_csv(self, data):
        # eeg_file = "%s/raw_eeg.csv" % (Variables.get_sub_folder_path())
        eeg_file = Variables.get_raw_eeg_file_path()
        logger.info(eeg_file)
        raw_data_with_time_stamps = np.c_[data['timestamps'], data['signals']]
        with open(eeg_file, 'w') as f:
            np.savetxt(eeg_file, raw_data_with_time_stamps, delimiter=',', fmt='%.5f', header = '')

        logger.info('Saved to %s\n' % eeg_file)

