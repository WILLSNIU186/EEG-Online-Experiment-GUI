#!/usr/bin/env python

from . import _hardware
import numpy as np
import threading
from ..edata.variables import Variables
from pycnbi.stream_receiver.stream_receiver import StreamReceiver
from pycnbi import logger


class Hardware(_hardware.HardwareAdditionalMethods):
    """
    Hardware class controls recording data in a different thread
    """
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
        """
        Check if record start or stop button pressed
        """
        return self.is_recording_running

    def start_recording_data(self):
        """
        Start recording data, set the flag to Ture and create a new thread
        """
        self.is_recording_running = True
        self.streamReceiver = StreamReceiver(buffer_size=0,
                                             amp_serial=Variables.get_amp_serial(), amp_name=Variables.get_amp_name())
        self.thread = threading.Thread(target=self.record)
        self.thread.start()


    def stop_recording_data(self):
        """
        Stop recording by setting the flag to False
        """
        self.is_recording_running = False


    def cancel_recording_data(self):
        """
        Interrupt recording and delete current buffer
        """
        self.is_recording_running = False
        self.recorded_data = np.array([])

    def get_current_window(self):
        """
        Get one window data
        :return: window data
        """
        return self.current_window

    def get_LSL_clock(self):
        """
        Get timestamps of LSL
        :return: current LSL timestamps
        """
        return self.streamReceiver.get_lsl_clock()

    def get_lsl_offset(self):
        """
        Get offset calculated by LSL, which is the delay of transmission
        :return: LSL offset
        """
        return self.streamReceiver.get_lsl_offset()

    def get_server_clock(self):
        """
        Get timestamps from instrument
        :return: timestamps of instrument
        """
        return self.streamReceiver.get_server_clock()

    def set_eeg_file_path(self):
        """
        Set recording directory by reading path from Variable class
        """
        self.eeg_file_path = Variables.get_raw_eeg_file_path()