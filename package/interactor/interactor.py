
from ..entity.hardware import hardware, hardware_eye_tracker


DEBUG_TRIGGER = False  # TODO: parameterize
NUM_X_CHANNELS = 16  # TODO: parameterize


class Interactor:

    def __init__(self):
        self.__hardware = hardware.Hardware()
        self.__eye_tracker_hardware = hardware_eye_tracker.HardwareEyeTracker()

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

    def get_server_clock(self):
        return self.__hardware.get_server_clock()

    def set_raw_eeg_file_path(self):
        self.__hardware.set_eeg_file_path()

    def start_eye_tracker_recording(self):
        self.__eye_tracker_hardware.start_recording()

    def stop_eye_tracker_recording(self):
        self.__eye_tracker_hardware.stop_recording()