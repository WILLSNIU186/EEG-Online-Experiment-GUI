from ..interactor import interactor, interactor_mrcp_template


class Router:
    def __init__(self):
        self.__interactor=interactor.Interactor()


    def start_recording(self):
        self.__interactor.start_recording()

    def stop_recording(self):
        self.__interactor.stop_recording()

    def get_current_window(self):
        return self.__interactor.get_current_window()

    def get_LSL_clock(self):
        return self.__interactor.get_LSL_clock()

    def get_lsl_offset(self):
        return self.__interactor.get_lsl_offset()