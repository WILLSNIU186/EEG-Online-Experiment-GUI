
import matplotlib.pyplot as plt

from os import path
import numpy as np

import mne

from . import data_loader
import pickle


class Preprocessing():
    consecutive_data_folder = "..\..\processed_data\consecutive_data"
    epoched_data_folder = "..\..\processed_data\epoched_data"

    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.fs = self.data_loader.fs
        self.filtered_raw_array = self.data_loader.raw_array.copy()
        if path.exists("ica_exclude_dict.p"):
            self.ICA_exclude_dict = self.load_dict_from_file('ica_exclude_dict.p')
        else:
            self.init_ICA_exclude_dict()

    def visualize_raw(self):
        fig = self.data_loader.raw_array.copy().plot(duration=100)
        fig.subplots_adjust(top=0.9)
        fig.suptitle(self.data_loader.exp_name)
        print("select bad span of signal..., press c to continue")
        plt.show()

    def apply_filter(self, hi, low, order, duration=100):
        self.hi = hi
        self.low = low
        iir_params = dict(order=order, ftype='butter')
        self.filtered_raw_array = self.data_loader.raw_array.copy().filter(l_freq=low, h_freq=hi,  method='iir',
                                                                           picks=['eeg'], iir_params=iir_params)
        # fig = self.filtered_raw_array.plot(duration=self.filtered_raw_array.n_times / self.fs)
        fig = self.filtered_raw_array.plot(duration=duration)
        fig.canvas.key_press_event('a')
        fig.subplots_adjust(top=0.9)
        fig.suptitle(self.data_loader.exp_name)
        print("select bad span of signal..., press c to continue")

    def apply_notch_filter(self, notch_freq, order, duration):
        iir_params = dict(order=order, ftype='butter')
        self.filtered_raw_array = self.filtered_raw_array.notch_filter(freqs=notch_freq, method='iir', picks=['eeg'], \
                                                                     iir_params=iir_params)

        fig = self.filtered_raw_array.plot(duration=duration)
        fig.canvas.key_press_event('a')
        fig.subplots_adjust(top=0.9)
        fig.suptitle(self.data_loader.exp_name)
        print("select bad span of signal..., press c to continue")



    def interpolate_bad_chs(self, duration=100):
        self.filtered_raw_array.interpolate_bads()
        fig = self.filtered_raw_array.plot(duration=duration)
        fig.suptitle('{} interpolated'.format(self.data_loader.exp_name))
        
    def apply_referencing(self, reference_channel, duration, change_raw=False):
        fig = self.filtered_raw_array.plot(duration=duration)
        fig.subplots_adjust(top=0.9)
        fig.suptitle('raw', size='xx-large', weight='bold')

        raw_new_ref = self.filtered_raw_array.copy().set_eeg_reference(ref_channels=reference_channel)
        fig = raw_new_ref.plot(duration=duration)
        fig.subplots_adjust(top=0.9)
        fig.suptitle('referenced using {}'.format(reference_channel), size='xx-large', weight='bold')

        if change_raw:
            self.filtered_raw_array.set_eeg_reference(ref_channels=reference_channel)

    def apply_ICA(self):
        self.ica = mne.preprocessing.ICA(n_components=len(mne.pick_types(self.filtered_raw_array.info, eeg=True, emg=False)) -
                                                      len(self.filtered_raw_array.info['bads']), random_state=97)
        self.ica.fit(self.filtered_raw_array, reject_by_annotation=True)
        self.ica.plot_sources(self.filtered_raw_array, stop=self.filtered_raw_array.n_times / self.fs)
        self.ica.plot_components(picks="all", inst=self.filtered_raw_array)
        self.save_excluded_ICs()

    def save_excluded_ICs(self):
        self.ICA_exclude_dict[self.data_loader.exp_counter] = self.ica.exclude
        self.save_dict_to_file('ica_exclude_dict.p', self.ICA_exclude_dict)

    def init_ICA_exclude_dict(self):
        key_list = list(range(data_loader.DataLoader.total_exp_number))
        self.ICA_exclude_dict = dict([(key, []) for key in key_list])

    def save_dict_to_file(self, file_name, dictionary):
        with open(file_name, 'wb') as fp:
            pickle.dump(dictionary, fp, protocol=pickle.HIGHEST_PROTOCOL)

    def load_dict_from_file(self, file_name):
        with open(file_name, 'rb') as fp:
            dictionary = pickle.load(fp)
        return dictionary

    def plot_exclude_ICA(self):
        filtered_before_ICA = self.filtered_raw_array.copy()
        # fig_before_ICA = filtered_before_ICA.plot(duration=filtered_before_ICA.n_times / self.fs)
        fig_before_ICA = filtered_before_ICA.plot(duration=200)

        fig_before_ICA.subplots_adjust(top=0.9)
        fig_before_ICA.suptitle('before ICA', size='xx-large', weight='bold')

        self.ica.apply(self.filtered_raw_array)
        # fig_after_ICA = self.filtered_raw_array.plot(duration=self.filtered_raw_array.n_times / self.fs)
        fig_after_ICA = self.filtered_raw_array.plot(duration=200)

        fig_after_ICA.subplots_adjust(top=0.9)
        fig_after_ICA.suptitle('after ICA', size='xx-large', weight='bold')
        self.ica.plot_overlay(filtered_before_ICA, exclude=self.ica.exclude, picks='eeg', start=0.0,
                              stop=self.filtered_raw_array.n_times / self.fs)

    def apply_ICA_auto(self, plot_IC=False, plot_pre_post=False, plot_overlay=True):
        ica = mne.preprocessing.ICA(n_components=len(mne.pick_types(self.filtered_raw_array.info, eeg=True, emg=False)),\
                                    random_state=97)
        ica.fit(self.filtered_raw_array)
        if plot_IC:
            ica.plot_sources(self.filtered_raw_array, stop=self.filtered_raw_array.n_times / self.fs)
            ica.plot_components(picks="all", inst=self.filtered_raw_array)
        ica.exclude = []
        # find which ICs match the EOG pattern
        eog_indices_l, _ = ica.find_bads_eog(self.filtered_raw_array, ch_name='Fp1')
        eog_indices_r, _ = ica.find_bads_eog(self.filtered_raw_array, ch_name='Fp2')
        print('eog_indices_l', eog_indices_l)
        print('eog_indices_r', eog_indices_r)

        eog_indices = eog_indices_l + eog_indices_r
        eog_indices = np.unique(np.asarray(eog_indices)).tolist()

        ica.exclude = eog_indices
        # ica.exclude = [18]
        print('ica exclude ', ica.exclude)

        before_ICA = self.filtered_raw_array.copy()
        if plot_pre_post:
            fig_before_ICA = before_ICA.plot(duration=200)
            fig_before_ICA.subplots_adjust(top=0.9)
            fig_before_ICA.suptitle('{} before ICA'.format(self.data_loader.exp_name), size='xx-large', weight='bold')

        ica.apply(self.filtered_raw_array)

        if plot_pre_post:
            fig_after_ICA = self.filtered_raw_array.plot(duration=200)
            fig_after_ICA.subplots_adjust(top=0.9)
            fig_after_ICA.suptitle('{} after ICA'.format(self.data_loader.exp_name), size='xx-large', weight='bold')

        if plot_overlay:
            ica.plot_overlay(before_ICA, exclude=ica.exclude, picks='eeg', start=0.0,
                             stop=self.filtered_raw_array.n_times / self.fs)

    def save_consecutive_data(self, special_name):
        self.filtered_raw_array.save('{}\{}_processed_BPF_{}Hz_{}Hz_{}.fif'.format(Preprocessing.consecutive_data_folder,
                                                                                self.data_loader.exp_name, self.low,
                                                                                self.hi, special_name), overwrite=True)
