from package.entity.base.buffer import Buffer
import numpy as np
import joblib
import mne
import os
from PyQt5.QtWidgets import QMainWindow
from package.views.layouts import online_test_layout
import tensorflow as tf
from tensorflow import keras
import pdb


class MRCPBuffer(Buffer):
    def __init__(self,main_view, window_stride=0.1, window_size=2, buffer_size=10,
                 filter=None, filter_type=None, ica_path=None, downsample=None, model_path=None,
                 model_type=None, model_name=None):
        super().__init__(window_stride, window_size, buffer_size, filter, filter_type)

        self.main_view = main_view
        self.downsample = downsample
        if downsample:
            self.sf = downsample
            self.n_sample = int(self.window_size * self.sf)
            self.window = np.zeros((self.n_ch, self.n_sample))
            self.eeg_window = np.zeros((self.n_eeg_ch, self.n_sample))

        if os.path.exists(ica_path):
            self.ica_model = mne.preprocessing.read_ica(ica_path)
        else:
            self.ica_model = None

        self.model_type = model_type
        self.model_name = model_name
        if os.path.exists(model_path):
            if model_type == 'sklearn':
                self.model = joblib.load(model_path)
            elif model_type == 'keras':
                self.model = tf.keras.models.load_model(model_path)
        else:
            self.model = None

        self.mne_info = mne.create_info(ch_names=self.eeg_ch_names, sfreq=self.sf, ch_types='eeg')
        self.mne_info.set_montage('standard_1020')

        self.mrcp_test_win = QMainWindow()
        self.mrcp_online_test_window = online_test_layout.Ui_MainWindow()
        self.mrcp_online_test_window.setupUi(self.mrcp_test_win)


    def loop(self):
        data, self.ts_list = self.sr.acquire("buffer using", blocking=True)
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
            if self.model:
                predict_window = window_epoch.get_data().copy()
                if self.model_type == 'sklearn':
                    pred = int(self.model.predict(predict_window))
                elif self.model_type == 'keras' and self.model_name == 'EEGNET':
                    predict_window *= 1000
                    predict_window = predict_window.reshape(1, self.n_eeg_ch, self.n_sample, 1)
                    pred = int(self.model.predict(predict_window).argmax(axis=-1))

                if pred == 1:
                    self.mrcp_online_test_window.label.setText('DETECTED')
                    self.main_view.addEventPlot('D_{}'.format(self.model_name), 'D_{}'.format(self.model_name))
                else:
                    self.mrcp_online_test_window.label.setText('')
                print(pred)
            # pdb.set_trace()

            self.eeg_window = window_epoch.get_data()[0, :, :]
            self.window[self.eeg_ch_idx, :] = self.eeg_window

    def update_window_stride(self, new_stride):
        self.stop_timer()
        self.start_timer()
        self.window_stride = new_stride


