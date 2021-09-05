import numpy as np
import pdb
import matplotlib.pyplot as plt


import mne
from mne.time_frequency import tfr_morlet, psd_multitaper, psd_welch
from . import data_loader
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class Analyzer():
    consecutive_data_folder = r"{}\..\processed_data\consecutive_data".format(dir_path)
    epoched_data_folder = r"{}\..\processed_data\epoched_data".format(dir_path)
    aligned_epoched_data_folder = r"{}\..\processed_data\epoched_data\aligned_epochs".format(dir_path)
    temporal_SMR_different_bands_folder = r"..\results\temporal_SMR_different_bands"
    TFR_folder = r"..\results\TFR"
    report_folder = r"..\results\report"

    def __init__(self, exp_counter, low_freq=0.1, hi_freq=3, pick_channels=['Cz'], signal_tmin=-3,
                 signal_tmax=5, noise_tmin=3, noise_tmax=11, generate_report=False):
        self.exp_counter = exp_counter
        self.pick_channels = pick_channels
        self.data_loader = data_loader.DataLoader(exp_counter=self.exp_counter)
        self.data_loader.init_task_dependent_variables()
        self.data_loader.load_data()
        self.exp_name = self.data_loader.exp_name
        self.channel_dict = self.data_loader.channel_dict
        self.fs = self.data_loader.fs
        self.low_freq = low_freq
        self.hi_freq = hi_freq
        self.signal_tmin = signal_tmin
        self.signal_tmax = signal_tmax
        self.noise_tmin = noise_tmin
        self.noise_tmax = noise_tmax
        self.report = mne.Report(verbose=True)
        self.generate_report = generate_report

    def load_preprocessed_data(self, special_name, duration):
        file_path = '{}\{}_processed_BPF_{}Hz_{}Hz_{}.fif'.format(Analyzer.consecutive_data_folder, self.exp_name,
                                                               self.low_freq, self.hi_freq, special_name)

        self.preprocessed_data = mne.io.read_raw_fif(file_path, preload=True)
        # fig_all = self.preprocessed_data.plot(events=self.task_event_array,
        #                                       duration=self.preprocessed_data.n_times / self.fs)

        fig_all = self.preprocessed_data.plot(duration=duration)
        fig_all.subplots_adjust(top=0.9)
        fig_all.suptitle('{}_processed_BPF_{}Hz_{}Hz'.format(self.exp_name, self.low_freq, self.hi_freq))

        channel_picked_data = self.preprocessed_data.copy().pick_channels(self.pick_channels)
        # fig_picked = channel_picked_data.plot(events=self.task_event_array,
        #                                       duration=channel_picked_data.n_times / self.fs)
        fig_picked = channel_picked_data.plot(duration=duration)
        fig_picked.subplots_adjust(top=0.9)
        fig_picked.suptitle('{}_processed_BPF_{}Hz_{}Hz'.format(self.exp_name, self.low_freq, self.hi_freq))
        plt.show()

        if self.generate_report:
            self.report.add_figs_to_section(fig_all,
                                            captions='{}_processed_BPF_{}Hz_{}Hz'.format(self.exp_name, self.low_freq,
                                                                                         self.hi_freq),
                                            section='consecutive EEG')

        if self.generate_report:
            self.report.add_figs_to_section(fig_picked,
                                            captions='picked channel {}_processed_BPF_{}Hz_{}Hz'.format(self.exp_name,
                                                                                                        self.low_freq,
                                                                                                        self.hi_freq),
                                            section='consecutive EEG')
    def load_preprocessed_data_pipeline(self, special_name, duration):
        file_path = '{}\{}_processed_BPF_{}Hz_{}Hz_{}.fif'.format(Analyzer.consecutive_data_folder, self.exp_name,
                                                               self.low_freq, self.hi_freq, special_name)

        self.preprocessed_data = mne.io.read_raw_fif(file_path, preload=True)
        # fig_all = self.preprocessed_data.plot(events=self.task_event_array,
        #                                       duration=self.preprocessed_data.n_times / self.fs)


#     def create_event(self):
#         raw_eeg_path = self.data_loader.base_folder + "//raw_eeg.csv"
#         df = pd.read_csv(raw_eeg_path, header=None)
#         self.raw_data = df.values
#         event_path = self.data_loader.base_folder + "//event.csv"
#         event_df = pd.read_csv(event_path, header=None)
#         self.events = event_df.values
#         # self.events = self.events.astype(int)
#         self.origin_time = self.raw_data[0, 0]
#         self.onsets = self.events[:, 1] - self.origin_time
#         self.durations = np.zeros_like(self.onsets)
#         self.event_array = np.column_stack(((self.onsets * self.data_loader.fs).astype(int), np.zeros_like(self.onsets,
#                                                                                                            dtype=int),
#                                             self.events[:, 0].astype(int)))
#         self.task_events = self.events[np.where(self.events == 6)[0], :]

#         self.onsets = self.task_events[:, 1] - self.origin_time
#         self.durations = np.zeros_like(self.onsets)
#         self.task_event_array = np.column_stack(((self.onsets * self.data_loader.fs).astype(int),
#                                                  np.zeros_like(self.onsets, dtype=int),
#                                                  self.task_events[:, 0].astype(int)))
    def apply_referencing(self):
        preprocessed_avg_ref = self.preprocessed_data.set_eeg_reference(ref_channels='average', projection=True)
        for title, proj in zip(['Original', 'Average'], [False, True]):
            fig = preprocessed_avg_ref.plot(proj=proj, duration=preprocessed_avg_ref.n_times / self.fs)
            # make room for title
            fig.subplots_adjust(top=0.9)
            fig.suptitle('{} reference'.format(title), size='xx-large', weight='bold')
        plt.show()
        self.preprocessed_data = preprocessed_avg_ref
        if self.generate_report:
            self.report.add_figs_to_section(fig, captions='{} reference'.format(title), section='consecutive EEG')

    def load_epoches(self, caption):
        signal_epoch_file_path = '{}\{}_signal_epochs_{}s_{}s_{}Hz_{}Hz_{}.fif'.format(Analyzer.epoched_data_folder,
                                                                                   self.data_loader.exp_name,
                                                                                   self.signal_tmin,
                                                                                   self.signal_tmax, self.low_freq,
                                                                                   self.hi_freq, caption)
        self.epochs = mne.read_epochs(signal_epoch_file_path)
        return self.epochs
    
    def load_epoches_align(self, caption):
        signal_epoch_file_path = '{}\{}_signal_epochs_{}s_{}s_{}Hz_{}Hz_{}.fif'.format(Analyzer.aligned_epoched_data_folder,
                                                                                   self.data_loader.exp_name,
                                                                                   self.signal_tmin,
                                                                                   self.signal_tmax, self.low_freq,
                                                                                   self.hi_freq, caption)
        self.epochs = mne.read_epochs(signal_epoch_file_path)
        return self.epochs


#         self.signal_epochs_cued = self.signal_epochs[cue_type].copy()
#         fig_signal = self.signal_epochs_cued.plot()
#         fig_signal.subplots_adjust(top=0.9)
#         fig_signal.suptitle('{} signal epochs'.format(self.exp_name), size='xx-large', weight='bold')


    def epoch_data(self, tmin, tmax, baseline, cue_type, caption):
        event_dict = {v: k for k, v in self.data_loader.mapping.items()}
        events, event_id = mne.events_from_annotations(self.preprocessed_data, event_id=event_dict)
        # pdb.set_trace()
        self.epochs = mne.Epochs(self.preprocessed_data, events, tmin=tmin, tmax=tmax,
                                 event_id=event_id, preload=True, baseline=baseline, reject_by_annotation=True, event_repeated='error')
        epochs_cued = self.epochs[cue_type]
#         ch_counter = 0
#         for ch in self.pick_channels:
#             fig_image_map = epochs_cued.plot_image(picks=ch, show=False)
#             ch_counter += 3
#             if self.generate_report:
#                 self.report.add_figs_to_section(fig_image_map, captions='{} {} epochs'.format(self.exp_name, caption),
#                                                 section='epochs')
#         fig = epochs_cued.plot(show=False)
#         fig.subplots_adjust(top=0.9)
#         fig.suptitle('{} epochs'.format(caption), size='xx-large', weight='bold')
        
        return epochs_cued

    
    def epoch_data_align(self, tmin, tmax, baseline, cue_type, selected):
        event_dict = {v: k for k, v in self.data_loader.mapping.items()}
        events, event_id = mne.events_from_annotations(self.preprocessed_data, event_id=event_dict)
        self.epochs_align = mne.Epochs(self.preprocessed_data, events, tmin=tmin, tmax=tmax,
                                 event_id=event_id, preload=True, baseline=baseline, reject_by_annotation=False, event_repeated='error')
#         pdb.set_trace()
        epochs_cued = self.epochs_align[selected]
    
#         fig = epochs_cued.plot(show=False)
#         fig.subplots_adjust(top=0.9)
#         fig.suptitle('{} epochs'.format(caption), size='xx-large', weight='bold')
        
        return epochs_cued
    
    def epoch_data_auto(self, tmin, tmax, baseline, caption, plot=False):
        event_dict = {v: k for k, v in self.data_loader.mapping.items()}
        events, event_id = mne.events_from_annotations(self.preprocessed_data, event_id=event_dict)

        self.epochs = mne.Epochs(self.preprocessed_data, events, tmin=tmin, tmax=tmax,
                                 event_id=event_id, preload=True, baseline=baseline, reject_by_annotation=True,
                                 event_repeated='drop')

        epochs_cued = mne.concatenate_epochs([self.epochs['EMG_WE_l'], self.epochs['EMG_WE_r'], \
                                              self.epochs['EMG_IE_l'], self.epochs['EMG_IE_r']])
#         pdb.set_trace()
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


    def epoch_data_self(self, tmin, tmax, baseline, cue_type, caption):
        event_dict = {v: k for k, v in self.data_loader.mapping.items()}
        events, event_id = mne.events_from_annotations(self.preprocessed_data, event_id=event_dict)
        # pdb.set_trace()
        self.epochs = mne.Epochs(self.preprocessed_data, events, tmin=tmin, tmax=tmax,
                                 event_id=event_id, preload=True, baseline=baseline, reject_by_annotation=True, event_repeated='drop')
        ch_counter = 0
        for ch in self.pick_channels:
            fig_image_map = self.epochs[cue_type].plot_image(picks=ch, show=False)
            ch_counter += 3
            if self.generate_report:
                self.report.add_figs_to_section(fig_image_map, captions='{} {} epochs'.format(self.exp_name, caption),
                                                section='epochs')
        fig = self.epochs[cue_type].plot(show=False)
        fig.subplots_adjust(top=0.9)
        fig.suptitle('{} epochs'.format(caption), size='xx-large', weight='bold')
        
        return self.epochs[cue_type]

    # def choose_epochs(self, epoch, cue_type, caption):
    #     epochs_cued = epoch[cue_type].copy()
    #     fig = epochs_cued.plot(show=False)
    #     fig.subplots_adjust(top=0.9)
    #     fig.suptitle('{} epochs'.format(caption), size='xx-large', weight='bold')
    #
    # def plot_epochs_image(self, epoch, cue_type, caption):
    #     epochs_cued = epoch[cue_type].copy()
    #     ch_counter = 0
    #     for ch in self.pick_channels:
    #         fig_image_map = epochs_cued.plot_image(picks=ch, show=False)
    #         ch_counter += 3
    #         if self.generate_report:
    #             self.report.add_figs_to_section(fig_image_map, captions='{} {} epochs'.format(self.exp_name, caption),
    #                                             section='epochs')

    def save_epoched_data(self, epoch, caption):
        epoch.save('{}\{}_signal_epochs_{}s_{}s_{}Hz_{}Hz_{}.fif'.format(Analyzer.epoched_data_folder,
                                                                                   self.data_loader.exp_name,
                                                                                   self.signal_tmin,
                                                                                   self.signal_tmax, self.low_freq,
                                                                                   self.hi_freq, caption), overwrite=True)

    def save_epoched_data_align(self, epoch, caption):
        epoch.save('{}\{}_signal_epochs_{}s_{}s_{}Hz_{}Hz_{}.fif'.format(Analyzer.aligned_epoched_data_folder,
                                                                         self.data_loader.exp_name,
                                                                         self.signal_tmin,
                                                                         self.signal_tmax, self.low_freq,
                                                                         self.hi_freq, caption), overwrite=True)

        
    def create_evoked_data(self, epoch_data, tmin, tmax, caption, line_color, vline):
        evoked_data = epoch_data.average()

        times = np.linspace(tmin, tmax, tmax - tmin + 1)
        fig = evoked_data.plot_joint(times=times, show=False)
        fig.subplots_adjust(top=0.9)
        fig.suptitle('{} {}'.format(self.exp_name, caption), size='xx-large', weight='bold')

        fig_topo = evoked_data.plot_topo(color=line_color, ylim=dict(eeg=[-10, 10]), show=False,
                                         title="{} {}".format(self.exp_name, caption), vline=vline)
        fig_topo.set_size_inches(10, 10)

        if self.generate_report:
            # self.report.add_figs_to_section(fig, captions='{} {}'.format(self.exp_name, caption), section='evoked')
            self.report.add_figs_to_section(fig_topo, captions='{} {} topo'.format(self.exp_name, caption), section='evoked')

        return evoked_data

    def lap(self, data_pre_lap):
        lap_filter = [-1 / 4] * 4
        lap_filter.insert(0, 1)  # center channel is channel 0
        lap_filter = np.asarray(lap_filter)
        temp = np.reshape(lap_filter, (1, 5))
        data_lap_filtered = np.dot(temp, data_pre_lap)
        return data_lap_filtered
    
    def lap_Cz(self, data_pre_lap):
        lap_filter = [-1 / 8] * 8
        lap_filter.insert(0, 1)  # center channel is channel 0
        lap_filter = np.asarray(lap_filter)
        temp = np.reshape(lap_filter, (1, 9))
        data_lap_filtered = np.dot(temp, data_pre_lap)
        return data_lap_filtered

    def apply_lap(self, evoked_data, caption, lap_type='large', tmin = -3, fs = 500):
        channel_names = evoked_data.ch_names
        if lap_type == 'large':
            large_lap_C3_chs = [channel_names.index('C3'), channel_names.index('T7'), channel_names.index('Cz'),
                                channel_names.index('F3'), channel_names.index('P3')]            
            large_lap_Cz_chs = [channel_names.index('Cz'), channel_names.index('C3'), channel_names.index('C4'),
                                channel_names.index('Fz'), channel_names.index('Pz')]
            large_lap_C4_chs = [channel_names.index('C4'), channel_names.index('Cz'), channel_names.index('T8'),
                                channel_names.index('F4'), channel_names.index('P4')]
            large_lap_FC1_chs = [channel_names.index('FC1'), channel_names.index('F3'), channel_names.index('Fz'),
                                channel_names.index('C3'), channel_names.index('Cz')]
            large_lap_FC2_chs = [channel_names.index('FC2'), channel_names.index('Cz'), channel_names.index('Fz'),
                                channel_names.index('F4'), channel_names.index('C4')]

            C3_large_lap_evoked = self.lap(evoked_data.copy().data[large_lap_C3_chs, :])
            Cz_large_lap_evoked = self.lap(evoked_data.copy().data[large_lap_Cz_chs, :])
            C4_large_lap_evoked = self.lap(evoked_data.copy().data[large_lap_C4_chs, :])
            FC1_large_lap_evoked = self.lap(evoked_data.copy().data[large_lap_FC1_chs, :])
            FC2_large_lap_evoked = self.lap(evoked_data.copy().data[large_lap_FC2_chs, :])
            large_lap_evoked = np.r_[C3_large_lap_evoked, Cz_large_lap_evoked, C4_large_lap_evoked, FC1_large_lap_evoked, FC2_large_lap_evoked]
            info = mne.create_info(ch_names=['C3', 'Cz', 'C4', 'FC1', 'FC2'], sfreq=fs, ch_types=['eeg', 'eeg', 'eeg', 'eeg', 'eeg'])
            info.set_montage('standard_1020')
            self.large_lap_evoked = mne.EvokedArray(large_lap_evoked, info=info, tmin=tmin,
                                                    nave=evoked_data.nave)
        elif lap_type =='mixed':
            large_lap_C3_chs = [channel_names.index('C3'), channel_names.index('T7'), channel_names.index('Cz'),
                                channel_names.index('F3'), channel_names.index('P3')] 
            large_lap_C1_chs = [channel_names.index('C1'), channel_names.index('C3'), channel_names.index('Cz'),
                                channel_names.index('FC1'), channel_names.index('CP1')] 
            large_lap_Cz_chs = [channel_names.index('Cz'), channel_names.index('C3'), channel_names.index('C4'),
                                channel_names.index('Fz'), channel_names.index('Pz')]
            large_lap_C2_chs = [channel_names.index('C2'), channel_names.index('C4'), channel_names.index('Cz'),
                                channel_names.index('FC2'), channel_names.index('CP2')] 
            large_lap_C4_chs = [channel_names.index('C4'), channel_names.index('Cz'), channel_names.index('T8'),
                                channel_names.index('F4'), channel_names.index('P4')]
            large_lap_FC1_chs = [channel_names.index('FC1'), channel_names.index('F3'), channel_names.index('Fz'),
                                channel_names.index('C3'), channel_names.index('Cz')]
            large_lap_FC2_chs = [channel_names.index('FC2'), channel_names.index('Cz'), channel_names.index('Fz'),
                                channel_names.index('F4'), channel_names.index('C4')]

            C3_large_lap_evoked = self.lap(evoked_data.copy().data[large_lap_C3_chs, :])
            C1_large_lap_evoked = self.lap(evoked_data.copy().data[large_lap_C1_chs, :])
            Cz_large_lap_evoked = self.lap(evoked_data.copy().data[large_lap_Cz_chs, :])
            C2_large_lap_evoked = self.lap(evoked_data.copy().data[large_lap_C2_chs, :])
            C4_large_lap_evoked = self.lap(evoked_data.copy().data[large_lap_C4_chs, :])
            FC1_large_lap_evoked = self.lap(evoked_data.copy().data[large_lap_FC1_chs, :])
            FC2_large_lap_evoked = self.lap(evoked_data.copy().data[large_lap_FC2_chs, :])
            large_lap_evoked = np.r_[C3_large_lap_evoked, C1_large_lap_evoked, Cz_large_lap_evoked, C2_large_lap_evoked, C4_large_lap_evoked, FC1_large_lap_evoked, FC2_large_lap_evoked]
            info = mne.create_info(ch_names=['C3', 'C1', 'Cz', 'C2', 'C4', 'FC1', 'FC2'], sfreq=fs, ch_types=['eeg', 'eeg', 'eeg','eeg', 'eeg', 'eeg', 'eeg'])
            info.set_montage('standard_1020')
            self.large_lap_evoked = mne.EvokedArray(large_lap_evoked, info=info, tmin=tmin,
                                                    nave=evoked_data.nave)
        elif lap_type =='large_Cz':
            channels = ['Cz', 'F3', 'F4', 'Fz', 'C3', 'C4', 'P3', 'P4', 'Pz']
            ch_idx = []
            for ch in channels:
                ch_idx.append(channel_names.index(ch))
            Cz_large_lap_evked = self.lap_Cz(evoked_data.copy().data[ch_idx, :])
            info = mne.create_info(ch_names=['Cz'], sfreq = fs, ch_types=['eeg'])
            self.large_lap_evoked = mne.EvokedArray(Cz_large_lap_evked, info=info, tmin = tmin,
                                                    nave=evoked_data.nave)
        
            
        return self.large_lap_evoked
#             fig = self.large_lap_evoked.plot_topo(show=False, title="C3 Cz C4 LAP {}".format(caption),
#                                                   ylim=dict(eeg=[-10, 10]))

#             if self.generate_report:
#                 self.report.add_figs_to_section(fig, captions='{} {} C3, Cz, C4 signal lap'.format(self.exp_name, caption),
#                                                 section='evoked')

    def plot_power_tfr(self, epoch, low_freq, high_freq, toi_min, toi_max, num_freq, task_name, mode, baseline=(0, 2)):
        # define frequencies of interest (log-spaced)
        # freqs = np.logspace(*np.log10([low_freq, high_freq]), num=num_freq)

        freqs = np.linspace(low_freq, high_freq, num=num_freq)
        n_cycles = [5] * len(freqs)  # different number of cycle per frequency

        power, itc = tfr_morlet(epoch, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                                return_itc=True, decim=3, n_jobs=1)
        power.plot_topo(baseline=baseline, mode=mode, title="{} ERD".format(task_name), show=False, vmin=-0.9, vmax=0.9)

        fig, axis = plt.subplots(1, 5, figsize=(1, 4))
        fig.subplots_adjust(top=0.9)
        fig.suptitle('{}'.format(self.exp_name), size='xx-large', weight='bold')
        # delta band
        power.plot_topomap(tmin=toi_min, tmax=toi_max, fmin=0, fmax=4, baseline=baseline, mode=mode, axes=axis[0],
                           title='delta', vmin=-0.5, vmax=0.5, colorbar=False, show=False)

        # theta band
        power.plot_topomap(tmin=toi_min, tmax=toi_max, fmin=4, fmax=8, baseline=baseline, mode=mode, axes=axis[1],
                           title='theta', vmin=-0.5, vmax=0.5, colorbar=False, show=False)

        # alpha band
        power.plot_topomap(tmin=toi_min, tmax=toi_max, fmin=8, fmax=12, baseline=baseline, mode=mode, axes=axis[2],
                           title='alpha', vmin=-0.5, vmax=0.5, colorbar=False, show=False)

        # beta band
        power.plot_topomap(tmin=toi_min, tmax=toi_max, fmin=12, fmax=30, baseline=baseline, mode=mode, axes=axis[3],
                           title='beta', vmin=-0.5, vmax=0.5, colorbar=False, show=False)
        # gamma band
        power.plot_topomap(tmin=toi_min, tmax=toi_max, fmin=30, fmax=45, baseline=baseline, mode=mode, axes=axis[4],
                           title='gamma', vmin=-0.5, vmax=0.5, colorbar=False, show=False)
        # plt.show()
        if self.generate_report:
            self.report.add_figs_to_section(fig, captions="{} ERD".format(task_name), section="bands ERD")
        return power

    def plot_power_band_temporal_ERD(self, epoch, low_freq, high_freq, toi_min, toi_max, num_freq, caption, task_name,
                                     mode, baseline=(0, 2)):
        # define frequencies of interest (log-spaced)
        freqs = np.linspace(low_freq, high_freq, num=num_freq)
        n_cycles = [5] * len(freqs)  # different number of cycle per frequency

        power, itc = tfr_morlet(epoch, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                                return_itc=True, decim=3, n_jobs=1)
        fig_tfr = power.plot_topo(baseline=baseline, mode=mode, title="{} {} ERD".format(task_name, caption),
                                  show=False,
                                  fig_facecolor='w', font_color='k', vmin=-0.5, vmax=0.5)
        fig_tfr.set_size_inches(10, 6)
        fig_tfr.savefig("{}\{}_tfr.png".format(Analyzer.TFR_folder, self.exp_name))

        counter_delta = 0
        counter_theta = 0
        counter_alpha = 0
        counter_beta = 0
        counter_gamma = 0

        fig_delta, axis_delta = plt.subplots(1, 6, figsize=(10, 6))
        fig_delta.suptitle('Delta {}'.format(self.exp_name), size='xx-large', weight='bold')
        fig_theta, axis_theta = plt.subplots(1, 6, figsize=(10, 6))
        fig_theta.suptitle('Theta {}'.format(self.exp_name), size='xx-large', weight='bold')
        fig_alpha, axis_alpha = plt.subplots(1, 6, figsize=(10, 6))
        fig_alpha.suptitle('Alpha {}'.format(self.exp_name), size='xx-large', weight='bold')
        fig_beta, axis_beta = plt.subplots(1, 6, figsize=(10, 6))
        fig_beta.suptitle('Beta {}'.format(self.exp_name), size='xx-large', weight='bold')
        fig_gamma, axis_gamma = plt.subplots(1, 6, figsize=(10, 6))
        fig_gamma.suptitle('Gamma {}'.format(self.exp_name), size='xx-large', weight='bold')
        while toi_max < 5:
            # delta band

            power.plot_topomap(tmin=toi_min, tmax=toi_max, fmin=0, fmax=4, baseline=baseline, mode=mode,
                               title='{}s~{}s'.format(toi_min, toi_max), vmin=-0.5,
                               vmax=0.5, colorbar=False, show=False, axes=axis_delta[counter_delta])
            counter_delta += 1

            # theta band

            power.plot_topomap(tmin=toi_min, tmax=toi_max, fmin=4, fmax=8, baseline=baseline, mode=mode,
                               title='{}s~{}s'.format(toi_min, toi_max), vmin=-0.5,
                               vmax=0.5, colorbar=False, show=False, axes=axis_theta[counter_theta])
            counter_theta += 1
            # alpha band

            power.plot_topomap(tmin=toi_min, tmax=toi_max, fmin=8, fmax=12, baseline=baseline, mode=mode,
                               title='{}s~{}s'.format(toi_min, toi_max), vmin=-0.5,
                               vmax=0.5, colorbar=False, show=False, axes=axis_alpha[counter_alpha])
            counter_alpha += 1

            # beta band

            power.plot_topomap(tmin=toi_min, tmax=toi_max, fmin=12, fmax=30, baseline=baseline, mode=mode,
                               title='{}s~{}s'.format(toi_min, toi_max), vmin=-0.5,
                               vmax=0.5, colorbar=False, show=False, axes=axis_beta[counter_beta])
            counter_beta += 1

            # gamma band

            power.plot_topomap(tmin=toi_min, tmax=toi_max, fmin=30, fmax=45, baseline=baseline, mode=mode,
                               title='{}s~{}s'.format(toi_min, toi_max), vmin=-0.5,
                               vmax=0.5, colorbar=False, show=False, axes=axis_gamma[counter_gamma])
            counter_gamma += 1

            toi_min += 1
            toi_max += 1
        # plt.show()

        if self.generate_report:
            self.report.add_figs_to_section(fig_tfr, captions="{} ERD".format(task_name), section='bands ERD')
            self.report.add_figs_to_section(fig_delta, captions='Delta {}'.format(self.exp_name), section="bands ERD")
            self.report.add_figs_to_section(fig_theta, captions='Theta {}'.format(self.exp_name), section="bands ERD")
            self.report.add_figs_to_section(fig_alpha, captions='Alpha {}'.format(self.exp_name), section="bands ERD")
            self.report.add_figs_to_section(fig_beta, captions='Beta {}'.format(self.exp_name), section="bands ERD")
            self.report.add_figs_to_section(fig_gamma, captions='Gamma {}'.format(self.exp_name), section="bands ERD")
        fig_delta.savefig("{}\{}_delta.png".format(Analyzer.temporal_SMR_different_bands_folder, self.exp_name))
        fig_theta.savefig("{}\{}_theta.png".format(Analyzer.temporal_SMR_different_bands_folder, self.exp_name))
        fig_alpha.savefig("{}\{}_alpha.png".format(Analyzer.temporal_SMR_different_bands_folder, self.exp_name))
        fig_beta.savefig("{}\{}_beta.png".format(Analyzer.temporal_SMR_different_bands_folder, self.exp_name))
        fig_gamma.savefig("{}\{}_gamma.png".format(Analyzer.temporal_SMR_different_bands_folder, self.exp_name))

    def plot_power_topomap(self, power, task_name, mode, baseline, toi_min=-3, toi_max=5, colorbar=False):
        counter_alpha = 0
        counter_beta = 0

        fig_alpha, axis_alpha = plt.subplots(1, int(toi_max-toi_min), figsize=(10, 6))
        fig_alpha.suptitle('Alpha {}'.format(task_name), size='xx-large', weight='bold')
        fig_beta, axis_beta = plt.subplots(1, int(toi_max-toi_min), figsize=(10, 6))
        fig_beta.suptitle('Beta {}'.format(task_name), size='xx-large', weight='bold')
        t_down = toi_min
        t_up = t_down + 1
        while t_up <= toi_max:
            # alpha band

            power.plot_topomap(tmin=t_down, tmax=t_up, fmin=8, fmax=12, baseline=baseline, mode=mode,
                               title='{}s~{}s'.format(t_down, t_up), vmin=-0.5,
                               vmax=0.5, colorbar=colorbar, show=False, axes=axis_alpha[counter_alpha])
            counter_alpha += 1

            # beta band

            power.plot_topomap(tmin=t_down, tmax=t_up, fmin=12, fmax=30, baseline=baseline, mode=mode,
                               title='{}s~{}s'.format(t_down, t_up), vmin=-0.5,
                               vmax=0.5, colorbar=colorbar, show=False, axes=axis_beta[counter_beta])
            counter_beta += 1

            t_down += 1
            t_up += 1
            
    def plot_psd_topomap(self, epochs, vmin, vmax, toi_min=-3, toi_max=5):
        t_down = toi_min
        t_up = t_down + 1
        while t_up <= toi_max:
            epochs.plot_psd_topomap(bands=[(8, 12, 'Alpha'), (12, 30, 'Beta')],ch_type='eeg', normalize=True, tmin=t_down, tmax=t_up,
                                    vmin=vmin, vmax=vmax);
            t_down += 1
            t_up += 1
            
            
    def save_report(self, mode, Ref):
        if mode == 'MRCP':
            if Ref is not None:
                self.report.save('{}\{}_MRCP_{}_{}_{}.html'.format(Analyzer.report_folder, self.exp_name, self.low_freq, self.hi_freq, Ref))
            else:
                self.report.save('{}\{}_MRCP_{}_{}.html'.format(Analyzer.report_folder, self.exp_name, self.low_freq, self.hi_freq))
        elif mode == 'SMR':
            if Ref is not None:
                self.report.save('{}\{}_SMR_{}_{}_{}.html'.format(Analyzer.report_folder, self.exp_name, Ref, self.low_freq, self.hi_freq))
            else:
                self.report.save('{}\{}_SMR_{}_{}.html'.format(Analyzer.report_folder, self.exp_name, self.low_freq, self.hi_freq))
