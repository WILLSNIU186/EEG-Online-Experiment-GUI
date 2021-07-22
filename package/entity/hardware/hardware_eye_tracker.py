from threading import Thread
from . import _hardware_eye_tracker

class HardwareEyeTracker(_hardware_eye_tracker.HardwareAdditionalMethods):
    def __init__(self):
        # self.record_final = record_thread.record_threading()
        self.is_on = False

    def stop_recording(self):
        self.is_on = False

    def start_recording(self):
        self.is_on = True
        self.thread = Thread(target=self.record)
        self.thread.start()
        self.thread.join()
