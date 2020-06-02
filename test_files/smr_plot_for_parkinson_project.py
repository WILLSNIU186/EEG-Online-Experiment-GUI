import pandas as pd
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, lfilter
from scipy import io

import mne
from mne.time_frequency import tfr_morlet, psd_multitaper, psd_welch

signal_data_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\Parkinson project\OneDrive-2020-03-30\codes\SMR_tutorial\\results\-3s_to_5s\data_-3s_to_5s\\"
file_name = ["freezer_time_locked_all_BPF_1_50Hzwithout_ICA.mat",
             "healthy_time_locked_all_BPF_1_50Hzwithout_ICA.mat",
             "non_freezer_time_locked_all_BPF_1_50Hzwithout_ICA.mat"]
group_name_title = ["freezer", "healthy", "non freezer"]
result_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\Parkinson project\OneDrive-2020-03-30\\results\\new_brain_map_various_band"
channel_names = [ 'AF3', 'AF4', 'F3', 'Fz', 'F4', 'FC1', 'FC2', 'C3', 'Cz', 'C4', 'CP1', 'CP2', 'P3', 'Pz', 'P4']
ch_types = "eeg"
fs = 250


def lap(data_pre_lap):
    lap_filter = [-1 / 4] * 4
    lap_filter.insert(0, 1)  # center channel is channel 0
    lap_filter = np.asarray(lap_filter)
    data_lap_filtered = np.matmul(data_pre_lap, np.transpose(lap_filter))
    return data_lap_filtered

counter = 0
for group_name in file_name:

    full_path = signal_data_folder + group_name
    data = io.loadmat(full_path)
    epoched_data = data['time_locked_all']
    epoched_data = epoched_data[2:17, :, :]
    n_trials = epoched_data.shape[2]
    nptns_signal = epoched_data.shape[1]
    epoched_data = np.transpose(epoched_data, (1,0,2))
    lap_Cz_ch = [channel_names.index('Cz'), channel_names.index('FC1'), channel_names.index('FC2'),
                  channel_names.index('CP1'), channel_names.index('CP2')]
    lap_FC1_ch = [channel_names.index('FC1'), channel_names.index('F3'), channel_names.index('Fz'),
                  channel_names.index('C3'), channel_names.index('Cz')]
    lap_FC2_ch = [channel_names.index('FC2'), channel_names.index('Fz'), channel_names.index('F4'),
                  channel_names.index('C4'), channel_names.index('Cz')]
    lap_CP1_ch = [channel_names.index('CP1'), channel_names.index('C3'), channel_names.index('Cz'),
                  channel_names.index('P3'), channel_names.index('Pz')]
    lap_CP2_ch = [channel_names.index('CP2'), channel_names.index('Cz'), channel_names.index('C4'),
                  channel_names.index('Pz'), channel_names.index('P4')]

    signal_lap_Cz_data_epochs = np.zeros((nptns_signal, n_trials), dtype=float)
    signal_lap_FC1_data_epochs = np.zeros((nptns_signal, n_trials), dtype=float)
    signal_lap_FC2_data_epochs = np.zeros((nptns_signal, n_trials), dtype=float)
    signal_lap_CP1_data_epochs = np.zeros((nptns_signal, n_trials), dtype=float)
    signal_lap_CP2_data_epochs = np.zeros((nptns_signal, n_trials), dtype=float)

    for i in range(n_trials):
        signal_lap_Cz_data_epochs[:, i] = lap(epoched_data[:, lap_Cz_ch, i])
        signal_lap_FC1_data_epochs[:, i] = lap(epoched_data[:, lap_FC1_ch, i])
        signal_lap_FC2_data_epochs[:, i] = lap(epoched_data[:, lap_FC2_ch, i])
        signal_lap_CP1_data_epochs[:, i] = lap(epoched_data[:, lap_CP1_ch, i])
        signal_lap_CP2_data_epochs[:, i] = lap(epoched_data[:, lap_CP2_ch, i])

    new_lap_data = np.dstack((signal_lap_Cz_data_epochs, signal_lap_CP1_data_epochs, signal_lap_CP2_data_epochs,
                             signal_lap_FC1_data_epochs, signal_lap_FC2_data_epochs))






    new_epoched_data = np.transpose(new_lap_data, (1, 2, 0))
    # new_epoched_data = np.transpose(epoched_data, (2, 0, 1))
    montage = 'standard_1005'
    lap_channel_names = ['Cz', 'FC1', 'FC2', 'CP1', 'CP2']

    info = mne.create_info(ch_names=lap_channel_names, sfreq=fs, ch_types = ch_types)
    # info = mne.create_info(ch_names=channel_names, sfreq=fs, ch_types=ch_types)
    info.set_montage(montage)

    new_epoched_data_average_over_trial = new_epoched_data - np.mean(new_epoched_data, 0)

    epochs = mne.EpochsArray(new_epoched_data_average_over_trial, info=info)

    t = 1
    while t < 7:
        fig = epochs.plot_psd_topomap(tmin = t, tmax = t+1, normalize=True,  show = False, cmap = 'coolwarm')
        fig.suptitle("{} {}s to {}s ".format(group_name_title[counter], t-3, t-2))
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        t += 1
    plt.show()

    # figure_name = "{}".format(group_name_title[counter])
    # fig.savefig("{}\{}".format(result_folder, figure_name))
    counter += 1
    # # define frequencies of interest (log-spaced)
    # freqs = np.linspace(1, 50, num=20)
    # # n_cycles = np.logspace(*np.log10([4, 10]), num = 20)
    # n_cycles = freqs / 2.  # different number of cycle per frequency
    # power, itc = tfr_morlet(epochs, freqs=freqs, n_cycles=n_cycles, use_fft=True,
    #                         return_itc=True, decim=3, n_jobs=1)
    # # pdb.set_trace()
    # power.plot_topo(tmin=0.5, tmax=5.5, baseline=(4.5, 5), mode='percent', title='Average power')
    # itc.plot_topo(title='Inter-Trial coherence', vmin=0., vmax=1., cmap='Reds')
    # pdb.set_trace()
plt.show()