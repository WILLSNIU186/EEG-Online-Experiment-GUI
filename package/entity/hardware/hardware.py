#!/usr/bin/env python

from . import _hardware
import numpy as np
import threading
from ..edata.variables import Variables
from pycnbi.stream_receiver.stream_receiver import StreamReceiver
from pycnbi import logger


class Hardware(_hardware.HardwareAdditionalMethods):

    def __init__(self):
        logger.info('TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT')
        self.is_recording_running = False
        self.recorded_data = np.array([])
        self.current_window = np.ndarray([])
        self.current_time_stamps = np.ndarray([])
        self.MRCP_window_size = 6
        self.finished_recording = False
        self.lsl_time_list = []
        self.server_time_list = []
        self.offset_time_list = []
        self.eeg_file_path = ''



    def connect_with_hardware(self):
        pass

    def is_recording_running(self):
        return self.is_recording_running

    def start_recording_data(self):
        self.is_recording_running = True
        self.streamReceiver = StreamReceiver(buffer_size=0,
                                             amp_serial=Variables.get_amp_serial(), amp_name=Variables.get_amp_name())
        self.thread = threading.Thread(target=self.record)
        self.thread.start()


    def stop_recording_data(self):
        self.is_recording_running = False

        # print("is thread alive? ", self.thread.is_alive())
        # print("is thread alive? ", self.thread.is_alive())


    def cancel_recording_data(self):
        self.is_recording_running = False
        self.recorded_data = np.array([])

    def get_current_window(self):
        return self.current_window

    def get_LSL_clock(self):
        return self.streamReceiver.get_lsl_clock()

    def get_lsl_offset(self):
        return self.streamReceiver.get_lsl_offset()

    def get_server_clock(self):
        return self.streamReceiver.get_server_clock()

    def set_eeg_file_path(self):
        self.eeg_file_path = Variables.get_raw_eeg_file_path()