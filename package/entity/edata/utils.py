#!/usr/bin/env python

import numpy as np
import pandas as pd
from numpy import mean, sqrt, square
from scipy.signal import butter, lfilter, lfilter_zi

from .variables import Variables


class Utils:
    """Class used to perform common multipurpose scientific calculations."""

    #
    #	Calculation of bandpass coefficients.
    #	Order is computed automatically.
    #	Note that if filter is unstable this function crashes (TODO handle problems)
    #
    @staticmethod
    def butter_bandpass_scope(highcut, lowcut, fs, num_ch):
        low = lowcut / (0.5 * fs)
        high = highcut / (0.5 * fs)
        b, a = butter(2, [high, low], btype='band')
        zi = np.zeros([a.shape[0] - 1, num_ch])
        return b, a, zi

    @staticmethod
    def butter_notch_scope(highcut, lowcut, fs, num_ch):
        low = lowcut / (0.5 * fs)
        high = highcut / (0.5 * fs)
        b, a = butter(2, [low, high], btype='bandstop')
        zi = np.zeros([a.shape[0] - 1, num_ch])
        return b, a, zi

    @staticmethod
    def butter_lowpass_scope(lowcut, fs, num_ch):
        low = lowcut / (0.5 * fs)
        b, a = butter(2, low, btype='low')
        zi = np.zeros([a.shape[0] - 1, num_ch])
        return b, a, zi

    @staticmethod
    def butter_highpass_scope(highcut, fs, num_ch):
        high = highcut / (0.5 * fs)
        b, a = butter(2, high, btype='high')
        zi = np.zeros([a.shape[0] - 1, num_ch])
        return b, a, zi


    @staticmethod
    def fft(data, resolution, start_freq, end_freq, sample_rate):
        """
        Returns fft data between the frequency ranges specified in the input.
        Args:
            data (numpy.ndarray): array of samples.
            resolution (float): increment in x-axis for frequencies
            start_freq (float): lower cutoff frequency (Hz).
            end_freq (float): Higher cutoff frequency (Hz).
            sample_rate (float): sampling rate (Hz).
        Returns:
            (numpy.ndarray): numpy array of frequency magnitudes
        """
        NFFT1 = round(sample_rate / resolution)
        fft_index_start = int(round(start_freq / resolution))
        fft_index_end = int(round(end_freq / resolution))
        temp_FFT = np.fft.fft(data, NFFT1) / (data.shape[0])
        magnitude_spectrum = 2 * np.abs(temp_FFT[fft_index_start:fft_index_end])
        # fft_axis = np.arange(magnitude_spectrum.shape[0]) * resolution
        return magnitude_spectrum

    @staticmethod
    def rms(data):
        """
        Returns RMS value of data.
        Args:
            data (numpy.ndarray): array of samples.
        Returns:
            (float): RMS value
        """
        return sqrt(mean(square(data)))

    @staticmethod
    def power(data):
        """
        Returns Power of data.
        Args:
            data (numpy.ndarray): array of samples.
        Returns:
            (float): Power value
        """
        return mean(square(data))

    @staticmethod
    def lap(data_pre_lap):
        # lap_filter = [-1 / 8] * 8
        lap_filter = [-1 / 4] * 4
        lap_filter.insert(0, 1)
        lap_filter = np.asarray(lap_filter)
        data_lap_filtered = np.matmul(data_pre_lap, np.transpose(lap_filter))
        return data_lap_filtered

    @staticmethod
    def butter_lowpass(cutoff = 3, fs = 1200, order = 2):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    @staticmethod
    def butter_highpass(cutoff = 0.05, fs = 1200, order = 2):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return b, a

    @staticmethod
    def butter_notch(low_cut, high_cut, fs, order=2):
        data_out = []
        nyq = 0.5 * fs
        low = low_cut / nyq
        high = high_cut / nyq
        b, a = butter(order, [low, high], btype='bandstop', analog=False)
        return b, a

    @staticmethod
    def construct_initial_condition_list(b, a, n_chan):
        '''
        data_in: chan * sample
        '''
        initial_condition_list = []
        for chan in range(n_chan):
            initial_condition = lfilter_zi(b, a)
            initial_condition_list.append(initial_condition)
        initial_condition_list = np.asarray(initial_condition_list)
        return initial_condition_list

    @staticmethod
    def apply_filter(b, a, data_in, initial_condition_list):
        '''
        data_in: chan * sample
        '''
        data_out, initial_condition_list = lfilter(b, a, data_in, axis=-1, zi=initial_condition_list)
        return data_out, initial_condition_list


    @staticmethod
    def preprocess(dataIn, ch_list):
        '''
        dataIn: sample * chan
        '''
        # data_chan_selected = dataIn[:, 0:9]
        data_chan_selected = dataIn[:, ch_list]
        # data_CAR = data_chan_selected - np.transpose(
        #     np.tile(np.mean(data_chan_selected, 1), (9, 1)))  # common average reference
        data_CAR = data_chan_selected - np.transpose(
            np.tile(np.mean(data_chan_selected, 1), (5, 1)))  # common average reference
        data_centered = data_CAR - np.tile(np.mean(data_CAR, 0), (len(data_CAR), 1))  # centering
        dataOut = Utils.lap(data_centered)

        return dataOut

    @staticmethod
    def write_data_to_csv(data, file_name):
        file = "{}/{}".format(Variables.get_sub_folder_path(), file_name)
        with open(file, 'w') as f:
            np.savetxt(file, data, delimiter=',', fmt='%.5f')
        return file

    @staticmethod
    def write_dict_to_csv(dict, file_name):
        file = "{}/{}".format(Variables.get_sub_folder_path(), file_name)
        print(file)
        pd.DataFrame.from_dict(data=dict, orient='index').to_csv(file, header=False)

    @staticmethod
    def write_event_number_to_csv(dict):
        file = "{}/event_annotation.csv".format(Variables.get_base_folder_path())
        print(file)
        pd.DataFrame.from_dict(data=dict, orient='index').to_csv(file, header=False)


    @staticmethod
    def save_protocol_to_csv(data, file):
        Variables.set_protocol_path(file)
        with open(file, 'w') as f:
            np.savetxt(file, data, delimiter=',', fmt='%.200s', header = "task_name, task_description, image_path, sound_path")

    @staticmethod
    def read_protocol_csv(file_name):
        df = pd.read_csv(file_name)
        task_table = df.values

        return task_table

