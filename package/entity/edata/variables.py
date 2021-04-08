#!/usr/bin/env python
import numpy as np
import pdb
class Variables:
    """
    Variables class contains class methods to set and get variables needed in presenter
    and view
    """
    __current_environment = ""
    __run_time_counter = 0
    __file_path = ""
    __base_folder_path = ""
    __sub_folder_path = ""
    __amp_name = ""
    __amp_serial = ""
    __sample_rate = 1200
    __low_pass_data_out = np.array([])
    __low_pass_data_in = np.array([])
    __high_pass_data_out = np.array([])
    __high_pass_data_in = np.array([])
    __protocol_path = ""
    __run_counter = 0
    __raw_eeg_file_path = ""

    @classmethod
    def init_Variables_for_next_run(cls):
        cls.__current_environment = ""
        cls.__run_time_counter = 0
        cls.__file_path = ""
        cls.__sub_folder_path = ""
        cls.__sample_rate = 1200
        cls.__low_pass_data_out = np.array([])
        cls.__low_pass_data_in = np.array([])
        cls.__high_pass_data_out = np.array([])
        cls.__high_pass_data_in = np.array([])
        cls.__protocol_path = ""
        cls.__raw_eeg_file_path = ""
        cls.__raw_eeg_timestamp_file_path = ""

    @classmethod
    def set_current_environment(cls, new_environment):
        cls.__current_environment = new_environment

    @classmethod
    def get_current_environment(cls):
        return cls.__current_environment

    @classmethod
    def set_run_time_counter(cls, new_run_time_counter):
        cls.__run_time_counter = new_run_time_counter

    @classmethod
    def get_run_time_counter(cls):
        return cls.__run_time_counter

    @classmethod
    def add_one_run_time_counter(cls):
        cls.__run_time_counter = cls.__run_time_counter + 1

    @classmethod
    def get_file_path(cls):
        return cls.__file_path

    @classmethod
    def set_file_path(cls, file_path):
        cls.__file_path = file_path

    @classmethod
    def get_base_folder_path(cls):
        return cls.__base_folder_path

    @classmethod
    def set_base_folder_path(cls, base_folder_path):
        cls.__base_folder_path = base_folder_path

    @classmethod
    def get_sub_folder_path(cls):
        return cls.__sub_folder_path

    @classmethod
    def set_sub_folder_path(cls, sub_folder_path):
        cls.__sub_folder_path = sub_folder_path

    @classmethod
    def get_amp_name(cls):
        return cls.__amp_name

    @classmethod
    def set_amp_name(cls, amp_name):
        cls.__amp_name = amp_name

    @classmethod
    def get_amp_serial(cls):
        return cls.__amp_serial

    @classmethod
    def set_amp_serial(cls, amp_serial):
        cls.__amp_serial = amp_serial

    @classmethod
    def get_low_pass_data_in(cls):
        return cls.__low_pass_data_in

    @classmethod
    def set_low_pass_data_in(cls, low_pass_data_in):
        cls.__low_pass_data_in = low_pass_data_in

    @classmethod
    def get_low_pass_data_out(cls):
        return cls.__low_pass_data_out

    @classmethod
    def set_low_pass_data_out(cls, low_pass_data_out):
        cls.__low_pass_data_out = low_pass_data_out

    @classmethod
    def get_high_pass_data_in(cls):
        return cls.__high_pass_data_in

    @classmethod
    def set_high_pass_data_in(cls, high_pass_data_in):
        cls.__high_pass_data_in = high_pass_data_in

    @classmethod
    def get_high_pass_data_out(cls):
        # pdb.set_trace()
        return cls.__high_pass_data_out

    @classmethod
    def set_high_pass_data_out(cls, high_pass_data_out):
        cls.__high_pass_data_out = high_pass_data_out


    @classmethod
    def get_sample_rate(cls):
        # pdb.set_trace()
        return cls.__sample_rate

    @classmethod
    def set_sample_rate(cls, sample_rate):
        cls.__sample_rate = sample_rate

    @classmethod
    def set_protocol_path(cls, protocol_path):
        cls.__protocol_path = protocol_path

    @classmethod
    def get_protocol_path(cls):
        return cls.__protocol_path

    @classmethod
    def set_run_counter(cls, run_counter):
        cls.__run_counter = run_counter

    @classmethod
    def get_run_counter(cls):
        return cls.__run_counter

    @classmethod
    def add_run_counter(cls):
        cls.__run_counter += 1

    @classmethod
    def set_raw_eeg_file_path(cls, file_path):
        cls.__raw_eeg_file_path = file_path

    @classmethod
    def get_raw_eeg_file_path(cls):
        return cls.__raw_eeg_file_path

    @classmethod
    def set_raw_eeg_timestamp_file_path(cls, file_path):
        cls.__raw_eeg_timestamp_file_path = file_path

    @classmethod
    def get_raw_eeg_timestamp_file_path(cls):
        return cls.__raw_eeg_timestamp_file_path