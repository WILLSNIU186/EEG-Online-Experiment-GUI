import struct
import sys
from pycnbi import logger
from ..entity.hardware import hardware
from ..router import router
import pdb
import numpy as np
from scipy.signal import butter, lfilter, lfiltic, buttord

DEBUG_TRIGGER = False  # TODO: parameterize
NUM_X_CHANNELS = 16  # TODO: parameterize


class Interactor:

    def __init__(self):
        self.__hardware = hardware.Hardware()

    def start_recording(self):
        self.__hardware.start_recording_data()

    def stop_recording(self):
        self.__hardware.stop_recording_data()

    def get_current_window(self):
        return self.__hardware.get_current_window()

    def get_LSL_clock(self):
        return self.__hardware.get_LSL_clock()

    def get_lsl_offset(self):
        return self.__hardware.get_lsl_offset()