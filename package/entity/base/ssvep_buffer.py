
import numpy as np
import joblib
import os
import mne
from PyQt5.QtWidgets import QMainWindow
from package.entity.base.buffer import Buffer
from package.views.layouts import online_test_layout
from package.entity.base.utils import SSVEPCCAAnalysis
import pdb


class SSVEPBuffer(Buffer):
    '''
    SSVEPBuffer is a child class of Buffer, it handles online processing and online testing.

    Parameter
    ----------
    window_stride: (second) Time interval between two windows
    window_size: (second) length of time window
    buffer_size: (second) length of buffer in StreamReceiver
    l_filter: None or object of Filter class
    filter_type: 'bpf' ---- band pass filter
                 'lpf' ---- low pass filter
                 'hpf' ---- high pass filter
                 'bsf; ---- band stop filter (notch filter)
    downsample: None or int, downsample rate
    model_path: None or file path containing .pkl file
    model_type: 'sklearn' or 'keras'. Further updating could be added for each configuration.
    model_name: name of classifier. E.g. cca, etc.

    '''
    def __init__(self, main_view, window_stride=0.1, window_size=2, buffer_size=10,
                 l_filter=None, filter_type=None, ica_path=None, downsample=None, model_path=None,
                 model_type=None, model_name='cca', stimulus_type='ssvep', channels_list=['O1', 'O2', 'Oz'],
                 target_frequencies=None):
        super().__init__(window_stride, window_size, buffer_size, l_filter, filter_type)    
        self.main_view = main_view
        self.downsample = downsample
        self.ica_model = None
        self.stimulus_type = stimulus_type
        self.model_type = model_type
        self.model_name = model_name
        self.target_frequencies = target_frequencies
        self.cca_pipeline = 0
        self.predicted_class = None
        self.required_channels = channels_list
        self.channel_indexes = []
        print(self.eeg_ch_names)
        for ch_name in self.required_channels:
            if ch_name in self.eeg_ch_names:
                self.channel_indexes.append(self.eeg_ch_names.index(ch_name))
                
        print('self.channel_indexes: ', self.channel_indexes)
    
        if downsample:
            self.sf = downsample
            self.n_sample = int(self.window_size * self.sf)
            self.window = np.zeros((self.n_ch, self.n_sample))
            self.eeg_window = np.zeros((self.n_eeg_ch, self.n_sample))

        if ica_path is not None:
            if os.path.exists(ica_path):
                self.ica_model = mne.preprocessing.read_ica(ica_path)
                
        if self.model_name=='cca':
            self.cca_pipeline = 1
        else:
            raise NotImplementedError('Reqeusted method not implemented')

        self.mne_info = mne.create_info(ch_names=self.eeg_ch_names, sfreq=self.sf, ch_types='eeg')
        self.mne_info.set_montage('standard_1020')
    
    def loop(self):
        '''
        Get called every window_stride seconds.
        It reads chunks of data using stream_receiver and process them.
        Processing steps include filter, downsample, ica, prediction.

        '''
        data, self.ts_list = self.sr.acquire('buffer using', blocking=True)
        if len(self.ts_list) > 0:
            data = data[:, self.sr.get_channels()].T / self.sr.multiplier
            # pdb.set_trace()
            self.window = np.roll(self.window, -len(self.ts_list), 1)
            if self.filter:
                filtered_data, _ = self.filter.apply_filter(data)
                self.window[:, -len(self.ts_list):] = filtered_data
            else:
                self.window[:, -len(self.ts_list):] = data
            
            self.eeg_window = self.window[self.eeg_ch_idx, :]

            eeg_window_3d = np.expand_dims(self.eeg_window, axis=0)
            window_epoch = mne.EpochsArray(eeg_window_3d, info=self.mne_info)
            # pdb.set_trace()
            if self.downsample:
                window_epoch = window_epoch.resample(self.downsample)
            if self.ica_model:
                window_epoch = self.ica_model.apply(window_epoch)
                # pdb.set_trace()
            
            # predict_window = window_epoch.get_data().copy()
            self.eeg_window = window_epoch.get_data()[0, :, :]
            if len(self.channel_indexes)==len(self.required_channels):
                self.detection_window = self.eeg_window[self.channel_indexes, :]
            else:
                raise NotImplementedError('Requested channels not in the channel list')
            
            if self.cca_pipeline:
                cca_analysis_object = SSVEPCCAAnalysis(fs=self.sf, data_len=self.window_size, 
                                                       target_freqs=self.target_frequencies, 
                                                       num_harmonics=2)
                corr_coeff = cca_analysis_object.apply_cca(self.detection_window.T)
                print('cca output: ', corr_coeff) 
                self.predicted_class = np.argmax(corr_coeff, axis=-1)
                print('predicted_class: ', self.predicted_class) 
            
            self.window[self.eeg_ch_idx, :] = self.eeg_window

    def update_window_stride(self, new_stride):
        '''
        Update window stride on the fly
        :param new_stride: int
        '''
        self.stop_timer()
        self.start_timer()
        self.window_stride = new_stride