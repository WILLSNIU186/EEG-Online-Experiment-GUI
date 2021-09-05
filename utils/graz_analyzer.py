import numpy as np
import pdb
import matplotlib.pyplot as plt
import mne
from .graz_utils import GrazUtils
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


class GrazAnalyzer():
    epoched_data_folder = r'{}\..\Develop\Graz_dataset\processed_data\epoched'.format(dir_path)

    sub_channels = ['F3', 'F1', 'Fz', 'F2', 'F4', 'FC5', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'FC6', 'C5', 'C3', \
                    'C1', 'Cz', 'C2', 'C4', 'C6', 'CP5', 'CP3', 'CP1', 'CPz', 'CP2', 'CP4', 'CP6', 'P3', 'P1', \
                    'Pz', 'P2', 'P4']
    # sub_channels = ['F3', 'F1', 'Fz', 'F2', 'F4', 'FFC5h', 'FFC3h', 'FFC1h', 'FFC2h', 'FFC4h', 'FFC6h', \
    #  'FC5', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'FC6', 'FTT7h', 'FCC5h', 'FCC3h', 'FCC1h', \
    #  'FCC2h', 'FCC4h', 'FCC6h', 'FTT8h', 'C5', 'C3', 'C1', 'Cz', 'C2', 'C4', 'C6', 'TTP7h', \
    #  'CCP5h', 'CCP3h', 'CCP1h', 'CCP2h', 'CCP4h', 'CCP6h', 'TTP8h', 'CP5', 'CP3', 'CP1', \
    #  'CPz', 'CP2', 'CP4', 'CP6', 'CPP5h', 'CPP3h', 'CPP1h', 'CPP2h', 'CPP4h', 'CPP6h', 'P3', \
    #  'P1', 'Pz', 'P2', 'P4', 'PPO1h', 'PPO2h']
    mapping = {'EF': 1536, 'EX': 1537, 'Sup': 1538, 'Pro': 1539, \
               'HC': 1540, 'HO': 1541, 'Rest': 1542}

    def __init__(self, sub, run, low_freq=0.1, hi_freq=3, pick_channels=['Cz'], signal_tmin=-3,\
                 signal_tmax=5, noise_tmin=3, noise_tmax=11, load_epochs_caption='whole',\
                 load_preprocessed_data_caption='origin_ref'):
        self.sub = sub
        self.run = run
        self.low_freq = low_freq
        self.hi_freq = hi_freq
        self.pick_channels = pick_channels
        self.signal_tmin = signal_tmin
        self.signal_tmax = signal_tmax
        self.noise_tmin = noise_tmin
        self.noise_tmax = noise_tmax
        self.load_epochs_caption = load_epochs_caption
        self.load_preprocessed_data_caption = load_preprocessed_data_caption

    def load_preprocessed_data(self, duration, plot=True):
        special_name = self.load_preprocessed_data_caption
        file_path = '{}\sub{}_run{}_processed_BPF_{}Hz_{}Hz_{}.fif'.format(GrazUtils.consecutive_data_folder,
                                                                           self.sub, self.run, self.low_freq,
                                                                           self.hi_freq, special_name)

        self.preprocessed_data = mne.io.read_raw_fif(file_path, preload=True)

        if plot:
            fig_all = self.preprocessed_data.plot(duration=duration)
            fig_all.subplots_adjust(top=0.9)
            fig_all.suptitle('sub{}_run{}_processed_BPF_{}Hz_{}Hz'.format(self.sub, self.run, \
                                                                          self.low_freq, self.hi_freq))

            channel_picked_data = self.preprocessed_data.copy().pick_channels(self.pick_channels)
            # fig_picked = channel_picked_data.plot(events=self.task_event_array,
            #                                       duration=channel_picked_data.n_times / self.fs)
            fig_picked = channel_picked_data.plot(duration=duration)
            fig_picked.subplots_adjust(top=0.9)
            fig_picked.suptitle('sub{}_run{}_processed_BPF_{}Hz_{}Hz'.format(self.sub, self.run, \
                                                                             self.low_freq, self.hi_freq))
            plt.show()

    def epoch_data_manual(self, tmin, tmax, baseline, cue, caption, plot=False):
        events_from_annot, event_dict = mne.events_from_annotations(self.preprocessed_data)

        self.epochs = mne.Epochs(self.preprocessed_data, events_from_annot, tmin=tmin, tmax=tmax,
                                 event_id=event_dict, preload=True, baseline=baseline, reject_by_annotation=True,
                                 event_repeated='drop')
        cue_type = str(GrazAnalyzer.mapping[cue])
        epochs_cat = mne.concatenate_epochs([self.epochs['1536'], self.epochs['1537'], self.epochs['1538'],
                                            self.epochs['1539'], self.epochs['1540'], self.epochs['1541'],
                                            self.epochs['1542']])
        epochs_cued = epochs_cat

        if plot:
            # ch_counter = 0
            # for ch in self.pick_channels:
            #     epochs_cued.plot_image(picks=ch, show=False)
            #     ch_counter += 3

            fig = epochs_cued.plot(show=False)
            fig.subplots_adjust(top=0.9)
            fig.suptitle('{} epochs'.format(caption), size='xx-large', weight='bold')

        return epochs_cued


    def epoch_data_auto(self, tmin, tmax, baseline, caption, plot=False):
        events_from_annot, event_dict = mne.events_from_annotations(self.preprocessed_data)

        self.epochs = mne.Epochs(self.preprocessed_data, events_from_annot, tmin=tmin, tmax=tmax,
                                 event_id=event_dict, preload=True, baseline=baseline, reject_by_annotation=True,
                                 event_repeated='drop')


        epochs_cued = mne.concatenate_epochs([self.epochs['1536'], self.epochs['1537'], self.epochs['1538'], \
                                              self.epochs['1539'], self.epochs['1540'], self.epochs['1541'],
                                              self.epochs['1542']])

        if plot:
            self.epochs.plot_drop_log()
            ch_counter = 0
            for ch in self.pick_channels:
                epochs_cued.plot_image(picks=ch, show=False)
                ch_counter += 3

            fig = epochs_cued.plot(show=False)
            fig.subplots_adjust(top=0.9)
            fig.suptitle('{} epochs'.format(caption), size='xx-large', weight='bold')

        return epochs_cued

    def epoch_data_mov_onset_auto(self, tmin, tmax, baseline, caption, plot=False):
        events_from_annot, event_dict = mne.events_from_annotations(self.preprocessed_data)

        self.epochs = mne.Epochs(self.preprocessed_data, events_from_annot, tmin=tmin, tmax=tmax,
                                 event_id=event_dict, preload=True, baseline=baseline, reject_by_annotation=True,
                                 event_repeated='drop')
        # event_list = ['EMG_EF', 'EMG_EX', 'EMG_Sup', 'EMG_Pro', 'EMG_HC', 'EMG_HO']
        # exist_event_list = []
        #
        # for event in event_list:
        #     if event in self.epochs.event_id.keys():
        #         exist_event_list.append(event)
        #     else:
        #         print('{} is not in this run'.format(event))
        #
        # epochs_cued = self.epochs['1542']
        # for exist_event in exist_event_list:
        #     epochs_cued = mne.concatenate_epochs([epochs_cued, self.epochs[exist_event]])
        epochs_cued = mne.concatenate_epochs([self.epochs['EMG_EF'], self.epochs['EMG_EX'], self.epochs['EMG_Sup'], \
                                              self.epochs['EMG_Pro'], self.epochs['EMG_HC'], self.epochs['EMG_HO'],
                                              self.epochs['EMG_EF_end'], self.epochs['EMG_EX_end'], self.epochs['EMG_Sup_end'], \
                                              self.epochs['EMG_Pro_end'], self.epochs['EMG_HC_end'], self.epochs['EMG_HO_end'],
                                              self.epochs['1542']])

        if plot:
            self.epochs.plot_drop_log()
            ch_counter = 0
            for ch in self.pick_channels:
                epochs_cued.plot_image(picks=ch, show=False)
                ch_counter += 3

            fig = epochs_cued.plot(show=False)
            fig.subplots_adjust(top=0.9)
            fig.suptitle('{} epochs'.format(caption), size='xx-large', weight='bold')

        return epochs_cued


    def save_epoched_data(self, epoch, caption, overwrite=True):
        epoch.save('{}\sub{}_run{}_epochs_{}s_{}s_{}Hz_{}Hz_{}.fif'.format(GrazAnalyzer.epoched_data_folder,
                                                                       self.sub, self.run,
                                                                       self.signal_tmin,
                                                                       self.signal_tmax, self.low_freq,
                                                                       self.hi_freq, caption),
                   overwrite=overwrite)


    def load_epochs(self):
        caption = self.load_epochs_caption
        signal_epoch_file_path = '{}\sub{}_run{}_epochs_{}s_{}s_{}Hz_{}Hz_{}.fif'.format(GrazAnalyzer.epoched_data_folder,
                                                                       self.sub, self.run,
                                                                       self.signal_tmin,
                                                                       self.signal_tmax, self.low_freq,
                                                                       self.hi_freq, caption)
        epochs = mne.read_epochs(signal_epoch_file_path)
        return epochs