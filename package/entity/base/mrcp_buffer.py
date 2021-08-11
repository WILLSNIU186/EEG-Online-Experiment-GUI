from package.entity.base.buffer import Buffer
import numpy as np
import joblib
import pdb


class MRCPBuffer(Buffer):
    def __init__(self,window_stride=0.1, window_size=2, buffer_size=10, filter=None, filter_type=None):
        super().__init__(self)

        self.window_stride = window_stride
        self.window_size = window_size
        self.n_sample = int(self.window_size * self.sr.sample_rate)
        self.window = np.zeros((self.n_ch, self.n_sample))
        self.buffer_size = buffer_size
        self.filter = filter
        if self.filter:
            if filter_type == 'bpf':
                self.filter.build_butter_band_pass()
            elif filter_type == 'lpf':
                self.filter.build_butter_low_pass()
            elif filter_type == 'hpf':
                self.filter.build_butter_high_pass()
            elif filter_type == 'bsf':
                self.filter.build_butter_notch()
        self.model = joblib.load(r'package\entity\base\svm.pkl')

    # overriding method
    def loop(self):
        data, self.ts_list = self.sr.acquire("buffer using", blocking=True)
        self.window = np.roll(self.window, -len(self.ts_list), 1)
        if self.filter:
            filtered_data, _ = self.filter.apply_filter(data.T)
            self.window[:, -len(self.ts_list):] = filtered_data
        else:
            self.window[:, -len(self.ts_list):] = data.T
        self.eeg_window = self.window[self.eeg_ch_idx, :]
        predict_window = np.expand_dims(self.eeg_window , axis=0)
        pred = int(self.model.predict(predict_window))
        if pred == 1:
            print('Detected')
        # print(self.window.shape)