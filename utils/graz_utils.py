import numpy as np
import pdb
import matplotlib.pyplot as plt
import mne
from mne.channels import make_dig_montage
from mne.preprocessing import ICA
import pandas as pd

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class GrazUtils():
    consecutive_data_folder = r'{}\..\Develop\Graz_dataset\processed_data\consecutive'.format(dir_path)
    mov_onset_folder = r'{}\..\Develop\Graz_dataset\mov_onset'.format(dir_path)


    def __init__(self, sub, run):
        self.sub = sub
        self.run = run
        self.sub_channels = ['F3', 'F1', 'Fz', 'F2', 'F4', 'FC5', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'FC6', 'C5', 'C3',\
                             'C1', 'Cz', 'C2', 'C4', 'C6', 'CP5', 'CP3', 'CP1', 'CPz', 'CP2', 'CP4', 'CP6', 'P3', 'P1',\
                             'Pz', 'P2', 'P4']
        self.eeg_channels =['F3', 'F1', 'Fz', 'F2', 'F4', 'FFC5h', 'FFC3h', 'FFC1h', 'FFC2h', 'FFC4h', 'FFC6h',\
                            'FC5', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'FC6', 'FTT7h', 'FCC5h', 'FCC3h', 'FCC1h',\
                            'FCC2h', 'FCC4h', 'FCC6h', 'FTT8h', 'C5', 'C3', 'C1', 'Cz', 'C2', 'C4', 'C6', 'TTP7h',\
                            'CCP5h', 'CCP3h', 'CCP1h', 'CCP2h', 'CCP4h', 'CCP6h', 'TTP8h', 'CP5', 'CP3', 'CP1',\
                            'CPz', 'CP2', 'CP4', 'CP6', 'CPP5h', 'CPP3h', 'CPP1h', 'CPP2h', 'CPP4h', 'CPP6h', 'P3',\
                            'P1', 'Pz', 'P2', 'P4', 'PPO1h', 'PPO2h']
        self.eog_channels = ['eog-r', 'eog-m', 'eog-l']
        self.stim_channels = ['ShoulderAdductio',
                             'ShoulderFlexionE',
                             'ShoulderRotation',
                             'thumb_near',
                             'thumb_far',
                             'thumb_index',
                             'index_near',
                             'index_far',
                             'index_middle',
                             'middle_near',
                             'middle_far',
                             'middle_ring',
                             'ring_near',
                             'ring_far',
                             'ring_little',
                             'litte_near',
                             'litte_far',
                             'thumb_palm',
                             'wrist_bend',
                             'roll',
                             'pitch',
                             'gesture',
                             'handPosX',
                             'handPosY',
                             'handPosZ',
                             'elbowPosX',
                             'elbowPosY',
                             'elbowPosZ',
                             'Elbow',
                             'ProSupination',
                             'Wrist',
                             'GripPressure']
        self.channel_types = ['eeg']*61 + ['eog']*3 + ['emg']*32

        self.fs = 512
        self.low = 0.05
        self.hi = 5
        self.bad_channels = {1: [],
                             2: [],
                             3: ['FCz', 'C1', 'C2', 'CCP5h'],
                             4: ['FC3', 'CPP1h'],
                             5: [],
                             6: [],
                             7: [],
                             8: [],
                             9: [],
                             10: [],
                             11: [],
                             12: [],
                             13: [],
                             14: [],
                             15: []}

        self.EMG_onset_offset_list = [[-1.2, -1.1, -0.75, -0.8, -0.8, -0.8],
                                 [-1.2, -0.8, -0.8, -1, -0.8, -0.8],
                                 [-1.2, -1.2, -0.75, -0.75, -0.7, -0.7],
                                 [-1, -1, -0.75, -0.75, -0.7, -0.7],
                                 [-1.2, -1.2, -0.8, -0.7, -0.8, -0.7],
                                 [-1.2, -1.2, -0.8, -0.8, -0.8, -0.75],
                                 [-1.2, -1.2, -0.8, -0.6, -0.75, -0.75],
                                 [-1.2, -1, -0.8, -0.8, -0.8, -0.8],
                                 [-0.85, -0.85, -0.8, -0.8, -0.5, -0.5],
                                 [-1, -0.8, -0.75, -0.5, -0.75, -0.5],
                                 [-1, -0.9, -0.8, -0.8, -0.8, -0.8],
                                 [-1, -1, -0.8, -0.8, -0.8, -0.8],
                                 [-1.2, -1.2, -0.8, -0.8, -0.68, -0.7],
                                 [-1, -1, -0.8, -0.8, -0.8, -0.8],
                                 [-1, -1, -0.8, -0.9, -0.8, -0.8]]



    def load_run(self, file_path, exclude=[]):
        self.raw = mne.io.read_raw_gdf(input_fname=file_path, eog=self.eog_channels, \
                                       exclude=exclude, preload=True)
        info = mne.create_info(sfreq = self.fs, ch_names = self.eeg_channels + self.eog_channels + self.stim_channels, \
                               ch_types= self.channel_types)
        fname = r'D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\offline_processing\Develop\Graz_dataset\eeg_positions\data\Nz-T10-Iz-T9\standard_1005_3D.tsv'

        labels = np.loadtxt(fname, skiprows=1, usecols=0, dtype='U6')
        coords = np.loadtxt(fname, skiprows=1, usecols=(1, 2, 3))
        ch_pos = {label: coord for label, coord in zip(labels, coords)}

        montage = make_dig_montage(ch_pos=ch_pos,
                                   nasion=ch_pos['Nz'],
                                   lpa=ch_pos['T9'],
                                   rpa=ch_pos['T10'])

        info.set_montage(montage)
        info['meas_date'] = self.raw.info['meas_date']
        self.raw.info = info

    def rescale(self):
        nan_free_raw = np.nan_to_num(self.raw.get_data())
        self.rescaled_raw = mne.io.RawArray(nan_free_raw/ 10**6, self.raw.info)
        self.rescaled_raw.set_annotations(self.raw.annotations)
        self.raw = self.rescaled_raw.copy()

    def check_channels(self):
        self.raw.info['bads'] = self.bad_channels[self.sub]
        self.raw.interpolate_bads(reset_bads=True)

    def remove_nan_from_array(self, array):
        return array[~np.isnan(array)]

    def add_mov_onset(self):
        file = r"{}\EMG_onsets_sub_{}_run_{}.csv".format(GrazUtils.mov_onset_folder, self.sub, self.run)
        dt = pd.read_csv(file, index_col=0, header=None)
        task_name_list = ['EF', 'EX', 'Sup', 'Pro', 'HC', 'HO']
        EMG_onsets_dict = dict.fromkeys(task_name_list)
        offset = 0.9
        EMG_onsets_dict['EF'] = self.remove_nan_from_array(dt.values[0, :]) + self.EMG_onset_offset_list[self.sub-1][0] +offset
        EMG_onsets_dict['EX'] = self.remove_nan_from_array(dt.values[1, :])+ self.EMG_onset_offset_list[self.sub-1][1]+offset
        EMG_onsets_dict['Sup'] = self.remove_nan_from_array(dt.values[2, :])+ self.EMG_onset_offset_list[self.sub-1][2]+offset
        EMG_onsets_dict['Pro'] = self.remove_nan_from_array(dt.values[3, :])+ self.EMG_onset_offset_list[self.sub-1][3]+offset
        EMG_onsets_dict['HC'] = self.remove_nan_from_array(dt.values[4, :])+ self.EMG_onset_offset_list[self.sub-1][4]+offset
        EMG_onsets_dict['HO'] = self.remove_nan_from_array(dt.values[5, :])+ self.EMG_onset_offset_list[self.sub-1][5]+offset

        onsets_for_annotation = np.concatenate((self.raw.annotations.onset,
                                                EMG_onsets_dict['EF'],
                                                EMG_onsets_dict['EX'],
                                                EMG_onsets_dict['Sup'],
                                                EMG_onsets_dict['Pro'],
                                                EMG_onsets_dict['HC'],
                                                EMG_onsets_dict['HO']))

        

        durations_for_annotation = np.zeros_like(onsets_for_annotation)
        descriptions_for_annotation = np.concatenate((self.raw.annotations.description,
                                                      np.array(['EMG_EF'] * len(EMG_onsets_dict['EF'])),
                                                      np.array(['EMG_EX'] * len(EMG_onsets_dict['EX'])),
                                                      np.array(['EMG_Sup'] * len(EMG_onsets_dict['Sup'])),
                                                      np.array(['EMG_Pro'] * len(EMG_onsets_dict['Pro'])),
                                                      np.array(['EMG_HC'] * len(EMG_onsets_dict['HC'])),
                                                      np.array(['EMG_HO'] * len(EMG_onsets_dict['HO']))))



        annot_from_events = mne.Annotations(onset=onsets_for_annotation,
                                            duration=durations_for_annotation,
                                            description=descriptions_for_annotation)
        self.raw.set_annotations(annot_from_events)

    def add_mov_end_onset(self):
        file = r"{}\EMG_end_onsets_sub_{}_run_{}.csv".format(GrazUtils.mov_onset_folder, self.sub, self.run)
        dt = pd.read_csv(file, index_col=0, header=None)
        task_name_list = ['EF', 'EX', 'Sup', 'Pro', 'HC', 'HO']
        EMG_onsets_dict = dict.fromkeys(task_name_list)
        offset = 0.9
        EMG_onsets_dict['EF'] = self.remove_nan_from_array(dt.values[0, :]) + self.EMG_onset_offset_list[self.sub - 1][
            0] + offset
        EMG_onsets_dict['EX'] = self.remove_nan_from_array(dt.values[1, :]) + self.EMG_onset_offset_list[self.sub - 1][
            1] + offset
        EMG_onsets_dict['Sup'] = self.remove_nan_from_array(dt.values[2, :]) + self.EMG_onset_offset_list[self.sub - 1][
            2] + offset
        EMG_onsets_dict['Pro'] = self.remove_nan_from_array(dt.values[3, :]) + self.EMG_onset_offset_list[self.sub - 1][
            3] + offset
        EMG_onsets_dict['HC'] = self.remove_nan_from_array(dt.values[4, :]) + self.EMG_onset_offset_list[self.sub - 1][
            4] + offset
        EMG_onsets_dict['HO'] = self.remove_nan_from_array(dt.values[5, :]) + self.EMG_onset_offset_list[self.sub - 1][
            5] + offset

        onsets_for_annotation = np.concatenate((self.raw.annotations.onset,
                                                EMG_onsets_dict['EF'],
                                                EMG_onsets_dict['EX'],
                                                EMG_onsets_dict['Sup'],
                                                EMG_onsets_dict['Pro'],
                                                EMG_onsets_dict['HC'],
                                                EMG_onsets_dict['HO']))

        durations_for_annotation = np.zeros_like(onsets_for_annotation)
        descriptions_for_annotation = np.concatenate((self.raw.annotations.description,
                                                      np.array(['EMG_EF_end'] * len(EMG_onsets_dict['EF'])),
                                                      np.array(['EMG_EX_end'] * len(EMG_onsets_dict['EX'])),
                                                      np.array(['EMG_Sup_end'] * len(EMG_onsets_dict['Sup'])),
                                                      np.array(['EMG_Pro_end'] * len(EMG_onsets_dict['Pro'])),
                                                      np.array(['EMG_HC_end'] * len(EMG_onsets_dict['HC'])),
                                                      np.array(['EMG_HO_end'] * len(EMG_onsets_dict['HO']))))

        annot_from_events = mne.Annotations(onset=onsets_for_annotation,
                                            duration=durations_for_annotation,
                                            description=descriptions_for_annotation)
        self.raw.set_annotations(annot_from_events)

    def apply_filter(self, hi, low, order, write_to_raw=False, distortion = 15, duration=100, plot=False):
        self.low = low
        self.hi = hi
        iir_params = dict(order=order, ftype='butter')
        self.filtered_raw_array = self.raw.copy().filter(l_freq=low, h_freq=hi,  method='iir',\
                                                         picks=['eeg'], iir_params=iir_params)

        distortion_events = [15, self.filtered_raw_array.n_times - 15*self.fs]
        onsets = np.asarray(distortion_events) / self.fs
        durations = [distortion] * len(distortion_events)
        descriptions = ['bad_distortion'] * len(distortion_events)


        onsets_for_annotation = np.concatenate((self.filtered_raw_array.annotations.onset, onsets))
        durations_for_annotation = np.concatenate((np.zeros_like(self.filtered_raw_array.annotations.onset),\
                                                   durations))
        descriptions_for_annotation = np.concatenate((self.filtered_raw_array.annotations.description, descriptions))
        distortion_annot = mne.Annotations(onsets_for_annotation, durations_for_annotation, \
                                           descriptions_for_annotation, \
                                           orig_time=self.filtered_raw_array.info['meas_date'])


        self.filtered_raw_array.set_annotations(distortion_annot)
        if plot:
            fig = self.filtered_raw_array.plot(duration=duration)
            # fig.canvas.key_press_event('a')
            fig.subplots_adjust(top=0.9)
            fig.suptitle('sub{} run{} {}-{}Hz BPF'.format(self.sub, self.run, self.low, self.hi), \
                         size='xx-large', weight='bold')

            print("select bad span of signal..., press c to continue")
        if write_to_raw:
            self.raw = self.filtered_raw_array.copy()

    def apply_ICA(self, plot_IC=False, plot_pre_post=False, plot_overlay=True):
        ica = ICA(n_components=len(self.eeg_channels), random_state=97)
        ica.fit(self.raw)
        if plot_IC:
            ica.plot_sources(self.raw, stop=self.raw.n_times / self.fs)
            ica.plot_components(picks="all", inst=self.raw)
        ica.exclude = []
        # find which ICs match the EOG pattern
        eog_indices_l, _ = ica.find_bads_eog(self.raw, ch_name='eog-l')
        eog_indices_r, _ = ica.find_bads_eog(self.raw, ch_name='eog-r')
        eog_indices_m, _ = ica.find_bads_eog(self.raw, ch_name='eog-m')
        print('eog_indices_l', eog_indices_l)
        print('eog_indices_r', eog_indices_r)
        print('eog_indices_m', eog_indices_m)

        eog_indices = eog_indices_l + eog_indices_r + eog_indices_m
        eog_indices = np.unique(np.asarray(eog_indices)).tolist()
        
        ica.exclude = eog_indices
        # ica.exclude = [18]
        print('ica exclude ', ica.exclude)

        before_ICA = self.raw.copy()
        if plot_pre_post:
            fig_before_ICA = before_ICA.plot(duration=200)
            fig_before_ICA.subplots_adjust(top=0.9)
            fig_before_ICA.suptitle('sub{} run{} before ICA'.format(self.sub, self.run), size='xx-large', weight='bold')

        ica.apply(self.raw)

        if plot_pre_post:
            fig_after_ICA = self.raw.plot(duration=200)
            fig_after_ICA.subplots_adjust(top=0.9)
            fig_after_ICA.suptitle('sub{} run{} after ICA'.format(self.sub, self.run), size='xx-large', weight='bold')

        if  plot_overlay:
            ica.plot_overlay(before_ICA, exclude=ica.exclude, picks='eeg', start=0.0,
                                  stop=self.raw.n_times / self.fs)


    def save_consecutive_data(self, special_name='origin_ref'):
        self.raw.save('{}\sub{}_run{}_processed_BPF_{}Hz_{}Hz_{}.fif'.format(GrazUtils.consecutive_data_folder,
                                                                                self.sub, self.run, self.low,
                                                                                self.hi, special_name), overwrite=True)





