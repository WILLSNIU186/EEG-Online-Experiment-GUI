import numpy as np
import pandas as pd
import mne
import pdb

class DataLoader():
    def __init__(self, record_folder, fs, experiment_type=None):
        self.record_folder = record_folder
        self.fs = fs
        self.experiment_type = experiment_type


    def get_channels(self):
        channel_path = self.record_folder + "//Run1" + "//channels.csv"
        df = pd.read_csv(channel_path, header=None)
        channel_array = df.values
        self.channel_names = channel_array[:, -1].tolist()
        self.channel_ind = channel_array[:, 0]
        self.channel_ind = [x + 2 for x in self.channel_ind]
        self.n_channel = len(self.channel_ind)

    def get_event_mapping(self):
        event_path = self.record_folder + "//event_annotation.csv"
        df = pd.read_csv(event_path, header=None)
        event_mapping = df.values
        self.mapping = {}
        for value, key in event_mapping:
            self.mapping[key] = value

    def get_channel_types(self):
        if self.experiment_type == 'MRCP':
            self.channel_type = ['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'emg', 'emg', 'eeg',
                                 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg',
                                 'eeg', 'eeg', 'emg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg',
                                 'eeg', 'eeg', 'eeg', 'eeg', 'emg']
        else:
            self.channel_type = 'eeg'

    def create_raw_object(self):
        # read raw data from csv file
        raw_eeg_path = self.record_folder + "//Run1" + "//raw_eeg.csv"
        df = pd.read_csv(raw_eeg_path, header=None)
        self.raw_data = df.values
        self.raw_eeg = self.raw_data[:, self.channel_ind]
        info = mne.create_info(sfreq = self.fs, ch_names = self.channel_names, ch_types=self.channel_type)
        info.set_montage('standard_1020')
        self.raw_array = mne.io.RawArray(np.transpose(self.raw_eeg/10**6), info)# convert uV to V

    def create_event(self):
        event_path = self.record_folder + "//Run1" + "//event.csv"
        event_df = pd.read_csv(event_path, header=None)
        self.events = event_df.values
        self.origin_time = self.raw_data[0, 0]
        self.onsets = self.events[:, 1] - self.origin_time
        self.durations = np.zeros_like(self.onsets)
        self.event_array = np.column_stack(((self.onsets * self.fs).astype(int), np.zeros_like(self.onsets, dtype = int), self.events[:, 0].astype(int)))
        self.descriptions = [self.mapping[event_id] for event_id in self.event_array[:, 2]]
        self.annot_from_events = mne.Annotations(onset=self.onsets, duration=self.durations, description=self.descriptions)
        self.raw_array.set_annotations(self.annot_from_events)

    def get_raw_object(self):
        return self.raw_array
        

    
if __name__ == '__main__':
    record_folder = r"D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\offline_processing\records\Narsimha_WEIE_LR_formal_2020-10-17"
    data_loader = DataLoader(record_folder=record_folder, fs=500, experiment_type='MRCP')
    data_loader.get_channels()
    data_loader.get_event_mapping()
    data_loader.get_channel_types()
    data_loader.create_raw_object()
    data_loader.create_event()
