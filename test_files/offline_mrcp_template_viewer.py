import pandas as pd
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, lfilter
from scipy import io

import mne
from mne.time_frequency import tfr_morlet, psd_multitaper, psd_welch

def butter_bandpass_scope(highcut, lowcut, fs):
    low = lowcut / (0.5 * fs)
    high = highcut / (0.5 * fs)
    b, a = butter(2, [low, high], btype='band')# second order for MRCP, 4th order for SMR
    return b, a


def lap(data_pre_lap):
    lap_filter = [-1 / 4] * 4
    lap_filter.insert(0, 1)  # center channel is channel 0
    lap_filter = np.asarray(lap_filter)
    data_lap_filtered = np.matmul(data_pre_lap, np.transpose(lap_filter))
    return data_lap_filtered


def lap_2_ch(data_pre_lap):
    lap_filter = [-1 / 2] * 2
    lap_filter.insert(0, 1)  # center channel is channel 0
    lap_filter = np.asarray(lap_filter)
    data_lap_filtered = np.matmul(data_pre_lap, np.transpose(lap_filter))
    return data_lap_filtered

    # load datasets
    # for exp_counter in np.arange(11,24):
    print(exp_counter)

plot_switch = True
generate_bpf_data = False
# for exp_counter in [8,9,16,17,18,19,20,21]:
# for exp_counter in [0]:
for exp_counter in np.arange(24, 25):
    # initialize parameters
    trial_removel_list = []
    fs = 1200
    signal_start_time = -2
    signal_stop_time = 4
    noise_start_time = 4
    noise_stop_time = 10
    len_win_signal = signal_stop_time - signal_start_time
    nptns_signal = int(len_win_signal * fs)
    t_epoch_signal = np.arange(signal_start_time, signal_stop_time, 1 / fs)
    len_win_noise = noise_stop_time - noise_start_time
    nptns_noise = int(len_win_noise * fs)
    t_epoch_noise = np.arange(noise_start_time, noise_stop_time, 1 / fs)
    result_folder = 'D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\results\\new_results'
    BPF_data_folder = 'D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\BPF_data'
    # set up task-dependent variables
    if exp_counter < 12:  # right hand movement
        n_trial = 25
        channel_dict = {'C5': 0, 'FC3': 1, 'CP3': 2, 'C3': 3, 'C1': 4, 'FCz': 5, 'Cz': 6, 'CPz': 7, 'C2': 8}
        channel_names = ['C5', 'FC3', 'CP3', 'C3', 'C1', 'FCz', 'Cz', 'CPz', 'C2']
        ch_types = ['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg']
        channel_position_dict = {'C5': 6, 'FC3': 2, 'CP3': 12, 'C3': 7, 'C1': 8, 'FCz': 4, 'Cz': 9, 'CPz': 14, 'C2': 10}
        lap_C3_ch = [channel_dict['C3'], channel_dict['FC3'], channel_dict['C5'], channel_dict['CP3'],
                     channel_dict['C1']]
        lap_Cz_ch = [channel_dict['Cz'], channel_dict['FCz'], channel_dict['C1'], channel_dict['CPz'],
                     channel_dict['C2']]
        channel_ind = np.arange(2, 11)
        n_channel = 9
        single_trial_ylim = [-60, 60]
        average_trial_ylim = [-30, 30]
    elif 12 <= exp_counter < 24:  # left hand movement
        n_trial = 35
        channel_dict = {'FC4': 0, 'C4': 1, 'C6': 2, 'CP4': 3, 'C1': 4, 'FCz': 5, 'Cz': 6, 'CPz': 7, 'C2': 8}
        channel_position_dict = {'FC4': 4, 'C4': 9, 'C6': 10, 'CP4': 14, 'C1': 6, 'FCz': 2, 'Cz': 7, 'CPz': 12, 'C2': 8}
        lap_C4_ch = [channel_dict['C4'], channel_dict['FC4'], channel_dict['C2'], channel_dict['CP4'],
                     channel_dict['C6']]
        lap_Cz_ch = [channel_dict['Cz'], channel_dict['FCz'], channel_dict['C1'], channel_dict['CPz'],
                     channel_dict['C2']]
        lap_C2_ch = [channel_dict['C2'], channel_dict['C4'], channel_dict['Cz']]
        channel_ind = np.arange(2, 11)
        n_channel = 9
        single_trial_ylim = [-50, 50]
        average_trial_ylim = [-20, 20]
    elif 24 <= exp_counter <36:  # RIGHT hand movement round 2
        n_trial = 19
        channel_dict = {'FC4': 0, 'C4': 1, 'C6': 2, 'CP4': 3, 'C1': 4, 'FCz': 5, 'Cz': 6, 'CPz': 7, 'C2': 8, 'C3': 9, 'CP3': 10, 'FC3': 11, 'C5': 12}
        channel_position_dict = {'FC4': 6, 'C4': 13, 'C6': 14, 'CP4': 20, 'C1': 10, 'FCz': 4, 'Cz': 11, 'CPz': 18, 'C2': 12, 'C3': 9, 'CP3': 16, 'FC3': 2, 'C5': 8}
        channel_names = list(channel_dict.keys())
        lap_C4_ch = [channel_dict['C4'], channel_dict['FC4'], channel_dict['C2'], channel_dict['CP4'],
                     channel_dict['C6']]
        lap_Cz_ch = [channel_dict['Cz'], channel_dict['FCz'], channel_dict['C1'], channel_dict['CPz'],
                     channel_dict['C2']]
        lap_C3_ch = [channel_dict['C3'], channel_dict['FC3'], channel_dict['C5'], channel_dict['CP3'],
                     channel_dict['C1']]
        channel_ind = np.arange(2, 15)
        n_channel = 13
        exe_event_number = 100
        img_event_number = 300
        rest_event_number = 200
        single_trial_ylim = [-50, 50]
        average_trial_ylim = [-20, 20]
    elif 36 <= exp_counter <42:
        n_trial = 20
        channel_dict = {'FP1': 0, 'AF3': 1, 'FP2': 2, 'AF4': 3, 'C1': 4, 'FCz': 5, 'Cz': 6, 'CPz': 7, 'C2': 8, 'C3': 9, 'CP3': 10, 'FC3': 11, 'C5': 12}
        channel_names = list(channel_dict.keys())
        channel_position_dict = {'C5': 6, 'FC3': 2, 'CP3': 12, 'C3': 7, 'C1': 8, 'FCz': 4, 'Cz': 9, 'CPz': 14, 'C2': 10}
        lap_Cz_ch = [channel_dict['Cz'], channel_dict['FCz'], channel_dict['C1'], channel_dict['CPz'],
                     channel_dict['C2']]
        lap_C3_ch = [channel_dict['C3'], channel_dict['FC3'], channel_dict['C5'], channel_dict['CP3'],
                     channel_dict['C1']]
        channel_ind = np.arange(2, 15)
        n_channel = 13
        exe_event_number = 100.
        rest_event_number = 200.
        eye_fixed_event_number = 400.
        watching_cue_event_number = 500.
        task_event_number = 6.
        single_trial_ylim = [-50, 50]
        average_trial_ylim = [-20, 20]

    if exp_counter % 2 == 0:
        event = 100.
    else:
        event = 300.


    if exp_counter == 0:
        exp_name = "right wrist extension exe"
        # trial_removel_list = [2, 3, 11, 12, 17, 18, 19, 20, 22, 23, 24]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/Pilot_right_wrist_extension_1_2020-04-27/Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/right_wrist_extension_exe_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 1:
        exp_name = "right wrist extension img"
        # trial_removel_list = [2, 3, 4, 6, 7, 11, 14, 18, 19, 22, 24]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/Pilot_right_wrist_extension_1_2020-04-27/Run2"
        EB_removed_eeg = io.loadmat(base_folder + "/right_wrist_extension_img_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 2:
        exp_name = "right wrist flexion exe"
        # trial_removel_list = [2, 9, 14, 18, 19]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/Pilot_right_wrist_flexion_1_2020-04-27/Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/right_wrist_flexion_exe_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 3:
        exp_name = "right wrist flexion img"
        # trial_removel_list = [1, 6, 7, 12]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/Pilot_right_wrist_flexion_1_2020-04-27/Run2"
        EB_removed_eeg = io.loadmat(base_folder + "/right_wrist_flexion_img_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 4:
        exp_name = "right fisting exe"
        # trial_removel_list = [10, 12, 14, 23]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_right_fisting_1_2020-04-27/Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/right_fisting_exe_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 5:
        exp_name = "right fisting img"
        # trial_removel_list = [5, 6, 8, 12, 15, 23]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_right_fisting_1_2020-04-27/Run2"
        EB_removed_eeg = io.loadmat(base_folder + "/right_fisting_img_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 6:
        exp_name = "right index extension exe"
        # trial_removel_list = [0,5,9,11,19,20,21,22,24]
        # trial_removel_list = [1, 3, 5, 7, 9, 11, 19, 21]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_right_index_extension_1_2020-04-27/Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/right_index_extension_exe_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 7:
        exp_name = "right index extension img"
        # trial_removel_list = [1,4,9,10,14,17,21]
        # trial_removel_list = [0, 1, 9, 20, 21, 22, 23, 24]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_right_index_extension_1_2020-04-27/Run2"
        EB_removed_eeg = io.loadmat(base_folder + "/right_index_extension_img_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 8:
        exp_name = "right center out reaching with object exe"
        # trial_removel_list = [2, 4, 8, 10, 11, 16, 17, 19, 22, 23, 24]
        trial_removel_list = [6, 10, 11, 12, 14]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_right_reaching_with_object_1_2020-04-27/Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/right_reaching_with_object_exe_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 9:
        exp_name = "right center out reaching with object img"
        # trial_removel_list = [1, 2, 4, 5, 8, 11, 12, 15, 19, 20, 21, 22, 23, 24]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_right_reaching_with_object_1_2020-04-27/Run2"
        EB_removed_eeg = io.loadmat(base_folder + "/right_reaching_with_object_img_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 10:
        exp_name = "right reaching without object exe"
        # trial_removel_list = [0, 2, 3, 5, 11, 13, 14, 17, 18, 19, 21, 22, 23]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_right_reaching_without_object_1_2020-04-27/Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/right_reaching_without_object_exe_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 11:
        exp_name = "right reaching without object img"
        n_trial = 16
        # trial_removel_list = [2, 5, 10, 12, 15]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_right_reaching_without_object_img_2020-04-27/Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/right_reaching_without_object_img_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 12:
        exp_name = "left wrist extension exe"
        trial_removel_list = [0, 3, 8, 10, 17, 21, 23, 25, 27, 30, 34]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_left_wrist_extension_1_2020-04-30/Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/left_wrist_extension_exe_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 13:
        exp_name = "left wrist extension img"
        trial_removel_list = [0, 5, 6, 12, 10, 16, 17, 19, 20, 21, 23, 30, 31]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_left_wrist_extension_1_2020-04-30/Run2"
        EB_removed_eeg = io.loadmat(base_folder + "/left_wrist_extension_img_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 14:
        exp_name = "left wrist flexion exe"
        trial_removel_list = [16, 18, 9, 23, 27, 33]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_left_wrist_flexion_1_2020-04-30/Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/left_wrist_flexion_exe_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 15:
        exp_name = "left wrist flexion img"
        trial_removel_list = [0, 6, 8, 14, 17, 18, 16, 24, 25, 26, 32]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_left_wrist_flexion_1_2020-04-30/Run2"
        EB_removed_eeg = io.loadmat(base_folder + "/left_wrist_flexion_img_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 16:
        exp_name = "left fisting exe"
        # trial_removel_list = [0, 9, 25, 31, 33]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_left_fisting_1_2020-04-30/Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/left_fisting_exe_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 17:
        exp_name = "left fisting img"
        # trial_removel_list = [4, 5, 6, 8, 18, 20]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_left_fisting_1_2020-04-30/Run2"
        EB_removed_eeg = io.loadmat(base_folder + "/left_fisting_img_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])

    elif exp_counter == 18:
        exp_name = "left index extension exe"
        # trial_removel_list = [1, 2, 3, 12, 21, 28, 32]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_left_index_extension_1_2020-04-30/Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/left_index_extension_exe_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 19:
        exp_name = "left index extension img"
        # trial_removel_list = [2, 5, 17, 24]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_left_index_extension_1_2020-04-30/Run2"
        EB_removed_eeg = io.loadmat(base_folder + "/left_index_extension_img_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])

    elif exp_counter == 20:
        exp_name = "left center out reaching with object exe"
        # trial_removel_list = [2, 5, 8, 9, 14, 24, 34]
        trial_removel_list = [2]
        EB_removed_eeg = io.loadmat(
            'D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\pilot_left_reaching_with_object_1_2020-04-30\Run1\left_reaching_with_object_EB_removed_data.mat')
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_left_reaching_with_object_1_2020-04-30/Run1"
    elif exp_counter == 21:
        exp_name = "left center out reaching with object img"
        # trial_removel_list = [7, 18, 21, 29, 30, 31]
        trial_removel_list = [0]
        EB_removed_eeg = io.loadmat(
            'D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\pilot_left_reaching_with_object_1_2020-04-30\Run2\left_reaching_with_object_EB_removed_data.mat')
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_left_reaching_with_object_1_2020-04-30/Run2"
    elif exp_counter == 22:
        exp_name = "left reaching without object exe"
        # trial_removel_list = [10, 28, 30, 33, 34]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_left_reaching_without_object_1_2020-04-30/Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/left_reaching_without_object_exe_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 23:
        exp_name = "left reaching without object img"
        # trial_removel_list = [10, 17, 28, 30, 32, 33, 34]
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records/pilot_left_reaching_without_object_1_2020-04-30/Run2"
        EB_removed_eeg = io.loadmat(base_folder + "/left_reaching_without_object_img_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 24:
        exp_name = "right reaching with object exe round 2"
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_right_reaching_with_object_2_2020-05-22\Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/right_reaching_with_object_exe_round2_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 25:
        exp_name = "right reaching with object img round 2"
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_right_reaching_with_object_2_2020-05-22\Run2"
        EB_removed_eeg = io.loadmat(base_folder + "/right_reaching_with_object_img_round2_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 26:
        exp_name = "right reaching without object exe round 2"
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_right_reaching_without_object_2_2020-05-22\Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/right_reaching_without_object_exe_round2_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 27:
        exp_name = "right reaching without object img round 2"
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_right_reaching_without_object_2_2020-05-22\Run2"
        EB_removed_eeg = io.loadmat(base_folder + "/right_reaching_without_object_img_round2_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 28:
        exp_name = "right wrist extension exe round 2"
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_right_wrist_extension_2_2020-05-22\Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/right_wrist_extension_exe_round2_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 29:
        exp_name = "right wrist extension img round 2"
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_right_wrist_extension_2_2020-05-22\Run2"
        EB_removed_eeg = io.loadmat(base_folder + "/right_wrist_extension_img_round2_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 30:
        exp_name = "right wrist flexion exe round 2"
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_right_wrist_flexion_2_2020-05-22\Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/right_wrist_flexion_exe_round2_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 31:
        exp_name = "right wrist flexion img round 2"
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_right_wrist_flexion_2_2020-05-22\Run2"
        EB_removed_eeg = io.loadmat(base_folder + "/right_wrist_flexion_img_round2_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 32:
        exp_name = "right fisting exe round 2"
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_right_fsting_2_2020-05-22\Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/right_fisting_exe_round2_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 33:
        exp_name = "right fisting img round 2"
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_right_fsting_2_2020-05-22\Run2"
        EB_removed_eeg = io.loadmat(base_folder + "/right_fisting_img_round2_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 34:
        exp_name = "right index extension exe round 2"
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_right_index_extension_2_2020-05-22\Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/right_index_extension_exe_round2_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 35:
        exp_name = "right index extension img round 2"
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_right_index_extension_2_2020-05-22\Run2"
        EB_removed_eeg = io.loadmat(base_folder + "/right_index_extension_img_round2_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 36:
        event = eye_fixed_event_number
        exp_name = "eye fixed"
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_eye_fixed_2020-05-25\Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/eye_fixed_EB_removed_data.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 37:
        event = watching_cue_event_number
        exp_name = "watching cues"
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_watching_cue_2020-05-25\Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/watching_cue.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 38:
        event = exe_event_number
        exp_name = "Index extension followed by rest"
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_10_IEexe_10_rest_2020-05-25\Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/index_extension_followed_by_rest.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 39:
        event = exe_event_number
        exp_name = "Index extension with rest randomized"
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_index_extension_rest_random_2020-05-25\Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/index_extension_rest_randomize.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 40:
        exp_name = "right index extension random interval"
        event = task_event_number
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_index_extension_random_interval_new_2020-05-28\Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/index_extension_random_interval.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])
    elif exp_counter == 41:
        exp_name = "right index extension rest + task"
        event = exe_event_number
        base_folder = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\Jiansheng_right_index_extension_10_rest_10_exe_2020-05-28\Run1"
        EB_removed_eeg = io.loadmat(base_folder + "/right_index_extension_rest_task.mat")
        EB_removed_data = np.transpose(EB_removed_eeg['ans'])




    # Preprocessing
    # read raw data from csv file
    raw_eeg_path = base_folder + "//raw_eeg.csv"
    df = pd.read_csv(raw_eeg_path, header=None)
    raw_data = df.values
    raw_emg = raw_data[:, 15]
    raw_eeg = raw_data[:, channel_ind]
    # band pass signal between 0.05 and 3 Hz
    bp_b, bp_a = butter_bandpass_scope(3, 0.05, fs)

    bpf_eeg = filtfilt(bp_b, bp_a, raw_eeg, axis=0)
    pdb.set_trace()

    # save band passed signal in EB_data for ICA removal later
    if generate_bpf_data == True:
        bpf_file = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\\records\EB_data\\{}_BPF_0.05_3Hz.csv".format(
            exp_name)
        with open(bpf_file, 'w') as f:
            np.savetxt(bpf_file, bpf_eeg, delimiter=',', fmt='%.5f', header='')

    else:
        # use eeglab in MATLAB to remove eye blinks by running ICA...

        # load EB_removed eeg
        # CAR
        data_CAR = EB_removed_data - np.transpose(np.tile(np.mean(EB_removed_data, 1), (n_channel, 1)))  # common average reference
        data_centered = data_CAR - np.tile(np.mean(data_CAR, 0), (len(data_CAR), 1))  # centering

        # # CAR
        # data_CAR = bpf_eeg - np.transpose(np.tile(np.mean(bpf_eeg, 1), (n_channel, 1)))  # common average reference
        # # data_CAR = BPF_data
        # data_centered = data_CAR - np.tile(np.mean(data_CAR, 0), (len(data_CAR), 1))  # centering

        # Epoch
        event_path = base_folder + "//event.csv"
        event_df = pd.read_csv(event_path, header=None)
        events = event_df.values

        # extract epochs based on event time stamps

        movement_onset_actual_ind = np.where(events[:, 0] == event)
        movement_onset_actual_time_stamps = events[movement_onset_actual_ind][:, 1]
        signal_ind_list = []
        noise_ind_list = []
        for i in range(len(movement_onset_actual_time_stamps)):
            absolute_difference_function = lambda list_value: abs(list_value - movement_onset_actual_time_stamps[i])
            closest_value = min(raw_data[:, 0], key=absolute_difference_function)
            movement_onset_ind = np.where(raw_data[:, 0] == closest_value)
            # signal_start_value = movement_onset_ind[0][0] + 11 * fs + signal_start_time * fs
            signal_start_value = movement_onset_ind[0][0] + signal_start_time * fs
            signal_stop_value_ind = signal_start_value + nptns_signal
            # noise_start_value = movement_onset_ind[0][0] + 11 * fs + noise_start_time * fs
            noise_start_value = movement_onset_ind[0][0] + noise_start_time * fs
            noise_stop_value = noise_start_value + nptns_noise
            signal_ind_list.append([signal_start_value, signal_stop_value_ind])
            noise_ind_list.append([noise_start_value, noise_stop_value])
        n_trial = len(signal_ind_list)
        # Trial removal
        trial_list = list(range(n_trial))
        for remove_ind in trial_removel_list:
            trial_list.remove(remove_ind)
        movement_onset_timestamps = (np.asarray(signal_ind_list)[:, 0]) / fs - signal_start_time  # movement onset
        # timestamps list

        # initialize data array
        signal_raw_data_epochs = np.zeros((nptns_signal, n_channel, len(signal_ind_list)), dtype=float)
        signal_BPF_data_epochs = np.zeros((nptns_signal, n_channel, len(signal_ind_list)), dtype=float)
        signal_data_CAR_epochs = np.zeros((nptns_signal, n_channel, len(signal_ind_list)), dtype=float)
        signal_data_centered_epochs = np.zeros((nptns_signal, n_channel, len(signal_ind_list)), dtype=float)
        signal_EB_removed_data_epochs = np.zeros((nptns_signal, n_channel, len(signal_ind_list)), dtype=float)
        signal_lap_Cz_data_epochs_CAR = np.zeros((nptns_signal, len(signal_ind_list)), dtype=float)
        signal_lap_C3_data_epochs_CAR = np.zeros((nptns_signal, len(signal_ind_list)), dtype=float)
        signal_lap_C4_data_epochs_CAR = np.zeros((nptns_signal, len(signal_ind_list)), dtype=float)
        signal_lap_Cz_data_epochs = np.zeros((nptns_signal, len(signal_ind_list)), dtype=float)
        signal_lap_C3_data_epochs = np.zeros((nptns_signal, len(signal_ind_list)), dtype=float)
        signal_lap_C4_data_epochs = np.zeros((nptns_signal, len(signal_ind_list)), dtype=float)

        noise_raw_data_epochs = np.zeros((nptns_noise, n_channel, len(noise_ind_list)), dtype=float)
        noise_BPF_data_epochs = np.zeros((nptns_noise, n_channel, len(noise_ind_list)), dtype=float)
        noise_data_CAR_epochs = np.zeros((nptns_noise, n_channel, len(noise_ind_list)), dtype=float)
        noise_data_centered_epochs = np.zeros((nptns_noise, n_channel, len(noise_ind_list)), dtype=float)
        noise_EB_removed_data_epochs = np.zeros((nptns_noise, n_channel, len(noise_ind_list)), dtype=float)
        noise_lap_Cz_data_epochs_CAR = np.zeros((nptns_noise, len(noise_ind_list)), dtype=float)
        noise_lap_C3_data_epochs_CAR = np.zeros((nptns_noise, len(noise_ind_list)), dtype=float)
        noise_lap_C4_data_epochs_CAR = np.zeros((nptns_noise, len(noise_ind_list)), dtype=float)
        noise_lap_Cz_data_epochs = np.zeros((nptns_noise, len(noise_ind_list)), dtype=float)
        noise_lap_C3_data_epochs = np.zeros((nptns_noise, len(noise_ind_list)), dtype=float)
        noise_lap_C4_data_epochs = np.zeros((nptns_noise, len(noise_ind_list)), dtype=float)

        # Epoching signal

        for i in range(len(signal_ind_list)):
            # print(i)
            signal_raw_data_epochs[:, :, i] = raw_eeg[signal_ind_list[i][0]:signal_ind_list[i][1]]
            signal_BPF_data_epochs[:, :, i] = bpf_eeg[signal_ind_list[i][0]:signal_ind_list[i][1]]
            signal_EB_removed_data_epochs[:, :, i] = EB_removed_data[signal_ind_list[i][0]:signal_ind_list[i][1]]
            signal_data_CAR_epochs[:, :, i] = data_CAR[signal_ind_list[i][0]:signal_ind_list[i][1]]
            signal_data_centered_epochs[:, :, i] = data_centered[signal_ind_list[i][0]:signal_ind_list[i][1]]
            # lap filter
            if exp_counter < 12:
                signal_lap_C3_data_epochs_CAR[:, i] = lap(signal_data_centered_epochs[:, lap_C3_ch, i])
                signal_lap_Cz_data_epochs_CAR[:, i] = lap(signal_data_centered_epochs[:, lap_Cz_ch, i])
                signal_lap_C3_data_epochs[:, i] = lap(signal_EB_removed_data_epochs[:, lap_C3_ch, i])
                signal_lap_Cz_data_epochs[:, i] = lap(signal_EB_removed_data_epochs[:, lap_Cz_ch, i])
            elif exp_counter >= 12 and exp_counter < 24:
                signal_lap_C4_data_epochs_CAR[:, i] = lap(signal_data_centered_epochs[:, lap_C4_ch, i])
                signal_lap_Cz_data_epochs_CAR[:, i] = lap(signal_data_centered_epochs[:, lap_Cz_ch, i])
                signal_lap_C4_data_epochs[:, i] = lap(signal_EB_removed_data_epochs[:, lap_C4_ch, i])
                signal_lap_Cz_data_epochs[:, i] = lap(signal_EB_removed_data_epochs[:, lap_Cz_ch, i])
            elif 24 <= exp_counter < 36:
                signal_lap_C4_data_epochs_CAR[:, i] = lap(signal_data_centered_epochs[:, lap_C4_ch, i])
                signal_lap_Cz_data_epochs_CAR[:, i] = lap(signal_data_centered_epochs[:, lap_Cz_ch, i])
                signal_lap_C3_data_epochs_CAR[:, i] = lap(signal_data_centered_epochs[:, lap_C3_ch, i])
                signal_lap_C4_data_epochs[:, i] = lap(signal_EB_removed_data_epochs[:, lap_C4_ch, i])
                signal_lap_Cz_data_epochs[:, i] = lap(signal_EB_removed_data_epochs[:, lap_Cz_ch, i])
                signal_lap_C3_data_epochs[:, i] = lap(signal_EB_removed_data_epochs[:, lap_C3_ch, i])
            elif 36 <= exp_counter < 42:
                signal_lap_Cz_data_epochs_CAR[:, i] = lap(signal_data_centered_epochs[:, lap_Cz_ch, i])
                signal_lap_C3_data_epochs_CAR[:, i] = lap(signal_data_centered_epochs[:, lap_C3_ch, i])
                signal_lap_Cz_data_epochs[:, i] = lap(signal_EB_removed_data_epochs[:, lap_Cz_ch, i])
                signal_lap_C3_data_epochs[:, i] = lap(signal_EB_removed_data_epochs[:, lap_C3_ch, i])

        # Epoching noise
        for i in range(len(noise_ind_list)):
            # print(i)
            noise_raw_data_epochs[:, :, i] = raw_eeg[noise_ind_list[i][0]:noise_ind_list[i][1]]
            noise_BPF_data_epochs[:, :, i] = bpf_eeg[noise_ind_list[i][0]:noise_ind_list[i][1]]
            noise_EB_removed_data_epochs[:, :, i] = EB_removed_data[noise_ind_list[i][0]:noise_ind_list[i][1]]
            noise_data_CAR_epochs[:, :, i] = data_CAR[noise_ind_list[i][0]:noise_ind_list[i][1]]
            noise_data_centered_epochs[:, :, i] = data_centered[noise_ind_list[i][0]:noise_ind_list[i][1]]
            # lap filter
            if exp_counter < 12:
                noise_lap_C3_data_epochs_CAR[:, i] = lap(noise_data_centered_epochs[:, lap_C3_ch, i])
                noise_lap_Cz_data_epochs_CAR[:, i] = lap(noise_data_centered_epochs[:, lap_Cz_ch, i])
                noise_lap_C3_data_epochs[:, i] = lap(noise_EB_removed_data_epochs[:, lap_C3_ch, i])
                noise_lap_Cz_data_epochs[:, i] = lap(noise_EB_removed_data_epochs[:, lap_Cz_ch, i])
            elif exp_counter >= 12 and exp_counter < 24:
                noise_lap_C4_data_epochs_CAR[:, i] = lap(noise_data_centered_epochs[:, lap_C4_ch, i])
                noise_lap_Cz_data_epochs_CAR[:, i] = lap(noise_data_centered_epochs[:, lap_Cz_ch, i])
                noise_lap_C4_data_epochs[:, i] = lap(noise_EB_removed_data_epochs[:, lap_C4_ch, i])
                noise_lap_Cz_data_epochs[:, i] = lap(noise_EB_removed_data_epochs[:, lap_Cz_ch, i])
            elif 24 <=  exp_counter <36:
                noise_lap_C4_data_epochs_CAR[:, i] = lap(noise_data_centered_epochs[:, lap_C4_ch, i])
                noise_lap_Cz_data_epochs_CAR[:, i] = lap(noise_data_centered_epochs[:, lap_Cz_ch, i])
                noise_lap_C3_data_epochs_CAR[:, i] = lap(noise_data_centered_epochs[:, lap_C3_ch, i])
                noise_lap_C4_data_epochs[:, i] = lap(noise_EB_removed_data_epochs[:, lap_C4_ch, i])
                noise_lap_Cz_data_epochs[:, i] = lap(noise_EB_removed_data_epochs[:, lap_Cz_ch, i])
                noise_lap_C3_data_epochs[:, i] = lap(noise_EB_removed_data_epochs[:, lap_C3_ch, i])
            elif 36 <= exp_counter <42:
                noise_lap_C3_data_epochs_CAR[:, i] = lap(noise_data_centered_epochs[:, lap_C3_ch, i])
                noise_lap_Cz_data_epochs_CAR[:, i] = lap(noise_data_centered_epochs[:, lap_Cz_ch, i])
                noise_lap_C3_data_epochs[:, i] = lap(noise_EB_removed_data_epochs[:, lap_C3_ch, i])
                noise_lap_Cz_data_epochs[:, i] = lap(noise_EB_removed_data_epochs[:, lap_Cz_ch, i])

        # temp_data = signal_BPF_data_epochs
        #
        # new_epoched_data_no_lap = np.transpose(temp_data, (1, 0, 2))
        # bpf_data_file_name_no_lap = "{}/{}-3s_5s_1_50Hz_no_lap.mat".format(BPF_data_folder, exp_name)
        # io.savemat(bpf_data_file_name_no_lap, {'mydata':new_epoched_data_no_lap})
        #
        # if exp_counter <12:
        #     temp_data[:, channel_dict['Cz'], :] = signal_lap_Cz_data_epochs
        #     temp_data[:, channel_dict['C3'], :] = signal_lap_C3_data_epochs
        # else:
        #     temp_data[:, channel_dict['Cz'], :] = signal_lap_Cz_data_epochs
        #     temp_data[:, channel_dict['C4'], :] = signal_lap_C4_data_epochs
        # # pdb.set_trace()
        # new_epoched_data_lap = np.transpose(temp_data, (1, 0, 2))
        #
        # bpf_data_file_name_lap = "{}/{}-3s_5s_1_50Hz_lap.mat".format(BPF_data_folder, exp_name)
        # io.savemat(bpf_data_file_name_lap, {'mydata':new_epoched_data_lap})



        # pdb.set_trace()

        # montage = 'standard_1005'
        #
        # info = mne.create_info(ch_names=channel_names, sfreq=fs, ch_types = ch_types)
        # info.set_montage(montage)
        #
        # new_epoched_data_average_over_trial = new_epoched_data - np.mean(new_epoched_data, 0)
        #
        # epochs = mne.EpochsArray(new_epoched_data_average_over_trial, info=info)
        # epochs.plot_psd_topomap( normalize=True)
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

        if plot_switch:
            fig_CAR = plt.figure()
            ax = plt.subplot(2, 4, 1)
            for i in range(signal_BPF_data_epochs[:, channel_dict['Cz'], trial_list].shape[1]):
                ax.plot(t_epoch_signal, signal_BPF_data_epochs[:, channel_dict['Cz'], trial_list][:, i], label=str(i))
            ax.set_ylim(single_trial_ylim)
            ax.set_title("BPF Cz")

            ax1 = plt.subplot(2, 4, 5)
            ax1.plot(t_epoch_signal, np.mean(signal_BPF_data_epochs[:, channel_dict['Cz'], trial_list], 1), linewidth=3, c='r')
            ax1.set_ylim(average_trial_ylim)
            ax1.set_title("BPF Cz")

            ax2 = plt.subplot(2, 4, 2)
            for i in range(signal_EB_removed_data_epochs[:, channel_dict['Cz'], trial_list].shape[1]):
                ax2.plot(t_epoch_signal, signal_EB_removed_data_epochs[:, channel_dict['Cz'], trial_list][:, i], label=str(i))
            ax2.set_ylim(single_trial_ylim)
            ax2.set_title("BPF-ICA Cz")

            ax3 = plt.subplot(2, 4, 6)
            ax3.plot(t_epoch_signal, np.mean(signal_EB_removed_data_epochs[:, channel_dict['Cz'], trial_list], 1), linewidth=3,
                     c='r')
            ax3.set_ylim(average_trial_ylim)
            ax3.set_title("BPF-ICA Cz")

            ax4 = plt.subplot(2, 4, 3)
            for i in range(signal_data_centered_epochs[:, channel_dict['Cz'], trial_list].shape[1]):
                ax4.plot(t_epoch_signal, signal_data_centered_epochs[:, channel_dict['Cz'], trial_list][:, i], label=str(i))
            ax4.set_ylim(single_trial_ylim)
            ax4.set_title("BPF-CAR-centered Cz")

            ax5 = plt.subplot(2, 4, 7)
            ax5.plot(t_epoch_signal, np.mean(signal_data_centered_epochs[:, channel_dict['Cz'], trial_list], 1), linewidth=3,
                     c='r')
            ax5.set_ylim(average_trial_ylim)
            ax5.set_title("BPF-CAR-centered Cz")

            ax6 = plt.subplot(2, 4, 4)
            for i in range(signal_lap_Cz_data_epochs_CAR[:, trial_list].shape[1]):
                ax6.plot(t_epoch_signal, signal_lap_Cz_data_epochs_CAR[:, trial_list][:, i], label=str(i))
            ax6.set_ylim(single_trial_ylim)
            ax6.set_title("BPF-CAR-centered-LAP Cz")

            ax7 = plt.subplot(2, 4, 8)
            ax7.plot(t_epoch_signal, np.mean(signal_lap_Cz_data_epochs_CAR[:, trial_list], 1), linewidth=3, c='r')
            ax7.set_ylim(average_trial_ylim)
            ax7.set_title("BPF-CAR-centered-LAP Cz")

            fig_CAR.suptitle("{} signal ".format(exp_name))
            fig_CAR.tight_layout(rect=[0, 0.03, 1, 0.95])
            # # QT backend
            # manager = plt.get_current_fig_manager()
            # manager.window.showMaximized()
            fig_CAR.savefig("{}\{}_processing_steps.png".format(result_folder, exp_name))

            # plot consecutive signal
            fig_consecutive_signal = plt.figure()

            ax_consecutive_signal_1 = plt.subplot(3, 1, 1)
            t2 = np.arange(0, len(bpf_eeg) / fs, 1 / fs)
            # ax_consecutive_signal_1.plot(t2, lap_Cz_entire_before_ICA)
            # ax_consecutive_signal_1.plot(t2, bpf_eeg[:, channel_dict['Cz']], c='b', label="BPF")
            ax_consecutive_signal_1.plot(t2, EB_removed_data[:, channel_dict['Cz']], c='k', label="BPF-ICA")
            # ax_consecutive_signal_1.plot(t2, data_centered[:, channel_dict['Cz']], c='y', label="BPF-ICA-CAR")
            ax_consecutive_signal_1.set_title("Cz")
            xc_counter = 0
            # Cz_MRCP_list = [0, 4, 7, 11, 12, 13, 22, 24, 29, 32, 33, 34]
            for xc in movement_onset_timestamps:
                line_color = 'r'
                ax_consecutive_signal_1.axvline(x=xc, color=line_color, linestyle="--")
                xc_counter += 1

            t1 = np.arange(0, len(EB_removed_data) / fs, 1 / fs)

            if exp_counter < 12:
                ch_name = 'C3'
            elif 11 < exp_counter < 24:
                ch_name = 'C2'
            elif 24 <= exp_counter <36:
                ch_name = 'C3'
            elif 36 <= exp_counter <42:
                ch_name = 'C3'
            ax_consecutive_signal_2 = plt.subplot(3, 1, 2)
            # ax_consecutive_signal_2.plot(t1, bpf_eeg[:, channel_dict[ch_name]], c='b', label="BPF")
            ax_consecutive_signal_2.plot(t1, EB_removed_data[:, channel_dict[ch_name]], c='k', label="BPF-ICA")
            # ax_consecutive_signal_2.plot(t1, data_centered[:, channel_dict[ch_name]], c='y', label="BPF-ICA-CAR")

            ax_consecutive_signal_2.set_title(ch_name)
            ax_consecutive_signal_2.legend()
            xc_counter = 0
            # C2_MRCP_list = [2,5,9,10,14,15,16,17,18,22,24,25,26,27,28,29,34]

            for xc in movement_onset_timestamps:
                line_color = 'r'
                # if xc_counter in C2_MRCP_list:
                #     line_color = 'g'
                ax_consecutive_signal_2.axvline(x=xc, color=line_color, linestyle="--")
                xc_counter += 1

            t1 = np.arange(0, len(EB_removed_data) / fs, 1 / fs)

            ax_consecutive_signal_3 = plt.subplot(3, 1, 3)
            ax_consecutive_signal_3.plot(t1, EB_removed_data[:, channel_dict[ch_name]], c='b',
                                         label="{} BPF-ICA".format(ch_name))
            ax_consecutive_signal_3.plot(t1, EB_removed_data[:, channel_dict['Cz']], c='y', label="Cz BPF-ICA")
            # ax_consecutive_signal_3.plot(t1, data_centered[:, 1], c='k', label="C4 BPF-ICA-CAR")

            ax_consecutive_signal_3.set_title("{} vs Cz".format(ch_name))
            ax_consecutive_signal_3.legend()
            xc_counter = 0
            # C2_and_Cz_no_MRCP_list = [1,3,6,8,11,19,20,21,23,30,31]
            for xc in movement_onset_timestamps:
                line_color = 'r'
                # if xc_counter in C2_and_Cz_no_MRCP_list:
                #     line_color = 'r'
                ax_consecutive_signal_3.axvline(x=xc, color=line_color, linestyle="--")
                xc_counter += 1

            fig_consecutive_signal.suptitle("{}".format(exp_name))
            fig_consecutive_signal.tight_layout(rect=[0, 0.03, 1, 0.95])
            # # QT backend
            # manager = plt.get_current_fig_manager()
            # manager.window.showMaximized()
            fig_consecutive_signal.savefig("{}\{}_consecutive.png".format(result_folder, exp_name))

            fig_emg = plt.figure()
            plt.plot(t2, raw_emg)

            # plot raw eeg
            plt.figure()
            for i in range( n_channel):
                plt.plot(t2, raw_eeg[:, i] , label = channel_names[i])
            plt.legend()
            plt.title("{} raw data".format(exp_name))


            # plot BPF eeg
            plt.figure()
            for i in range( n_channel):
                plt.plot(t2, bpf_eeg[:, i] + 400 * i, label = channel_names[i])
            plt.legend()
            plt.title("{} BPF data".format(exp_name))

            # plot consecutive signal
            fig_consecutive_lap_signal = plt.figure()

            ax_consecutive_signal_1 = plt.subplot(3, 1, 1)
            t2 = np.arange(0, len(bpf_eeg) / fs, 1 / fs)
            lap_Cz = lap(EB_removed_data[:, lap_Cz_ch])
            ax_consecutive_signal_1.plot(t2, lap_Cz, c='k', label="BPF-ICA")

            ax_consecutive_signal_1.set_title("Cz")
            xc_counter = 0
            # Cz_MRCP_list = [0, 4, 7, 11, 12, 13, 22, 24, 29, 32, 33, 34]
            for xc in movement_onset_timestamps:
                line_color = 'r'
                ax_consecutive_signal_1.axvline(x=xc, color=line_color, linestyle="--")
                xc_counter += 1

            t1 = np.arange(0, len(EB_removed_data) / fs, 1 / fs)

            if exp_counter < 12:
                ch_name = 'C3'
            elif 11 < exp_counter < 24:
                ch_name = 'C2'
            elif 24 <= exp_counter < 36:
                ch_name = 'C3'
            elif 36 <= exp_counter < 42:
                ch_name = 'C3'
            ax_consecutive_signal_2 = plt.subplot(3, 1, 2)
            lap_C3 = lap(EB_removed_data[:, lap_C3_ch])
            ax_consecutive_signal_2.plot(t2, lap_C3, c='k', label="BPF-ICA")

            ax_consecutive_signal_2.set_title(ch_name)
            ax_consecutive_signal_2.legend()
            xc_counter = 0
            # C2_MRCP_list = [2,5,9,10,14,15,16,17,18,22,24,25,26,27,28,29,34]

            for xc in movement_onset_timestamps:
                line_color = 'r'
                # if xc_counter in C2_MRCP_list:
                #     line_color = 'g'
                ax_consecutive_signal_2.axvline(x=xc, color=line_color, linestyle="--")
                xc_counter += 1

            t1 = np.arange(0, len(EB_removed_data) / fs, 1 / fs)

            ax_consecutive_signal_3 = plt.subplot(3, 1, 3)
            ax_consecutive_signal_3.plot(t1, lap_Cz, c='b',
                                         label="{} BPF-ICA".format(ch_name))
            ax_consecutive_signal_3.plot(t1, lap_C3, c='y', label="Cz BPF-ICA")
            # ax_consecutive_signal_3.plot(t1, data_centered[:, 1], c='k', label="C4 BPF-ICA-CAR")

            ax_consecutive_signal_3.set_title("{} vs Cz".format(ch_name))
            ax_consecutive_signal_3.legend()
            xc_counter = 0
            # C2_and_Cz_no_MRCP_list = [1,3,6,8,11,19,20,21,23,30,31]
            for xc in movement_onset_timestamps:
                line_color = 'r'
                # if xc_counter in C2_and_Cz_no_MRCP_list:
                #     line_color = 'r'
                ax_consecutive_signal_3.axvline(x=xc, color=line_color, linestyle="--")
                xc_counter += 1

            fig_consecutive_lap_signal.suptitle("{} lap".format(exp_name))
            fig_consecutive_lap_signal.tight_layout(rect=[0, 0.03, 1, 0.95])






            # plot topographical-like channel signals
            fig_topo_signal = plt.figure()
            channel_dict = {'C5': 0, 'FC3': 1, 'CP3': 2, 'C3': 3, 'C1': 4, 'FCz': 5, 'Cz': 6, 'CPz': 7, 'C2': 8}
            for ch_idx in channel_dict:
                # print(ch_idx)
                ax = plt.subplot(3, 7, channel_position_dict[ch_idx])
                for i in range(signal_EB_removed_data_epochs[:, channel_dict[ch_idx], trial_list].shape[1]):
                    ax.plot(t_epoch_signal, signal_EB_removed_data_epochs[:, channel_dict[ch_idx], trial_list][:, i],
                            linewidth=0.2,
                            c='0.5')
                ax.plot(t_epoch_signal, np.mean(signal_EB_removed_data_epochs[:, channel_dict[ch_idx], trial_list], 1),
                        linewidth=2,
                        c='r', label='BPF-ICA_average')
                if ch_idx == 'Cz':
                    ax.plot(t_epoch_signal, np.mean(signal_lap_Cz_data_epochs[:, trial_list], 1), linewidth=2, c='k',
                            label='BPF-ICA-LAP_average')
                if ch_idx == 'C4':
                    ax.plot(t_epoch_signal, np.mean(signal_lap_C4_data_epochs[:, trial_list], 1), linewidth=2, c='k',
                            label='BPF-ICA-LAP_average')
                if ch_idx == 'C3':
                    ax.plot(t_epoch_signal, np.mean(signal_lap_C3_data_epochs[:, trial_list], 1), linewidth=2, c='k',
                            label='BPF-ICA-LAP_average')

                # ax.plot(t_epoch_signal, np.mean(signal_EB_removed_data_epochs[:, channel_dict[ch_idx], :], 1), c='k')
                ax.set_ylim(average_trial_ylim)

                ax.set_title(ch_idx)
                # ax.set_ylim(-5,5)

            fig_topo_signal.suptitle("SIGNAL {}".format(exp_name))
            fig_topo_signal.tight_layout(rect=[0, 0.03, 1, 0.95])
            # fig1.savefig("results/{} no lap average over trials.png".format(exp_name))
            fig_topo_signal.savefig("{}\{}_topo_signal.png".format(result_folder, exp_name))

            # plot topographical-like channel noises
            fig_topo_noise = plt.figure()
            for ch_idx in channel_dict:
                # print(ch_idx)
                ax = plt.subplot(3, 7, channel_position_dict[ch_idx])
                for i in range(noise_EB_removed_data_epochs[:, channel_dict[ch_idx], trial_list].shape[1]):
                    ax.plot(t_epoch_noise, noise_EB_removed_data_epochs[:, channel_dict[ch_idx], trial_list][:, i],
                            linewidth=0.2,
                            c='0.5')
                ax.plot(t_epoch_noise, np.mean(noise_EB_removed_data_epochs[:, channel_dict[ch_idx], trial_list], 1),
                        linewidth=2,
                        c='r',
                        label='BPF-ICA_average')
                if ch_idx == 'Cz':
                    ax.plot(t_epoch_noise, np.mean(noise_lap_Cz_data_epochs[:, trial_list], 1), linewidth=2, c='k',
                            label='BPF-ICA-LAP_average')
                if ch_idx == 'C4':
                    ax.plot(t_epoch_noise, np.mean(noise_lap_C4_data_epochs[:, trial_list], 1), linewidth=2, c='k',
                            label='BPF-ICA-LAP_average')
                if ch_idx == 'C3':
                    ax.plot(t_epoch_noise, np.mean(noise_lap_C3_data_epochs[:, trial_list], 1), linewidth=2, c='k',
                            label='BPF-ICA-LAP_average')

                # ax.plot(t_epoch_noise, np.mean(noise_EB_removed_data_epochs[:, channel_dict[ch_idx], :], 1), c='k')
                ax.set_ylim(average_trial_ylim)

                ax.set_title(ch_idx)
                # ax.set_ylim(-5,5)

            fig_topo_noise.suptitle("NOISE {}".format(exp_name))
            fig_topo_noise.tight_layout(rect=[0, 0.03, 1, 0.95])
            # # QT backend
            # manager = plt.get_current_fig_manager()
            # manager.window.showMaximized()
            fig_topo_noise.savefig("{}\{}_topo_noise.png".format(result_folder, exp_name))
            #
            # lap_Cz_data = signal_lap_Cz_data_epochs[:, trial_list]
            # # Plot single trial and mean mrcp
            #
            # fig = plt.figure()
            # ax = plt.subplot(2, 3, 1)
            # for i in range(lap_Cz_data.shape[1]):
            #     ax.plot(t_epoch_signal, lap_Cz_data[:, i], label=str(i))
            # # ax.set_ylim(-10, 10)
            # ax.set_title("single trials plot Cz")
            # # plt.legend()
            # # plt.savefig("single trials plot {}.png".format(exp_name))
            #
            # ax1 = plt.subplot(2, 3, 4)
            # ax1.plot(t_epoch_signal, np.mean(lap_Cz_data, 1), linewidth=3, c='r')
            # # ax1.set_ylim(-5, 5)
            # ax1.set_title("average trial plot Cz")
            # # plt.savefig("average trial plot {}.png".format(exp_name))
            #
            # if exp_counter < 12:
            #     lap_data = signal_lap_C3_data_epochs[:, trial_list]
            #     ch_name1 = 'C3'
            #     ch_index = 4
            #     ch_name = 'C1'
            # elif 12 <= exp_counter < 24:
            #     lap_data = signal_lap_C4_data_epochs[:, trial_list]
            #     ch_name1 = 'C4'
            #
            #     ch_index = 8
            #     ch_name = 'C2'
            #
            # ax2 = plt.subplot(2, 3, 3)
            # for i in range(lap_data.shape[1]):
            #     ax2.plot(t_epoch_signal, lap_data[:, i], label=str(i))
            # # ax2.set_ylim(-10, 10)
            # ax2.set_title("single trials plot {}".format(ch_name1))
            # # plt.legend()
            # # plt.savefig("single trials plot {}.png".format(exp_name))
            #
            # ax3 = plt.subplot(2, 3, 6)
            # ax3.plot(t_epoch_signal, np.mean(lap_data, 1), linewidth=3, c='r')
            # # ax3.set_ylim(-5, 5)
            # ax3.set_title("average trial plot {}".format(ch_name1))
            #
            # ax4 = plt.subplot(2, 3, 2)
            # for i in range(signal_data_centered_epochs[:, ch_index, :].shape[1]):
            #     ax4.plot(t_epoch_signal, signal_data_centered_epochs[:, ch_index, i])
            # # ax2.set_ylim(-10, 10)
            # ax4.set_title("single trials plot C2")
            # # plt.legend()
            # # plt.savefig("single trials plot {}.png".format(exp_name))
            #
            # ax5 = plt.subplot(2, 3, 5)
            # ax5.plot(t_epoch_signal, np.mean(signal_data_centered_epochs[:, ch_index, :], 1), linewidth=3, c='r')
            # # ax5.set_ylim(-5, 5)
            # ax5.set_title("average trial plot C2")
            #
            # # ax4 = plt.subplot(2, 3, 2)
            # # for i in trial_list:
            # #     ax4.plot(t_epoch_signal, signal_data_centered_epochs[:, ch_index, i])
            # # # ax4.set_ylim(-10, 10)
            # # ax4.set_title("single trials plot {}(no lap)".format(ch_name))
            # # # plt.legend()
            # # # plt.savefig("single trials plot {}.png".format(exp_name))
            # #
            # # ax5 = plt.subplot(2, 3, 5)
            # # ax5.plot(t_epoch_signal, np.mean(signal_data_centered_epochs[:, ch_index, trial_list], 1), linewidth=3, c='r')
            # # # ax5.set_ylim(-5, 5)
            # # ax5.set_title("average trial plot {}(no lap)".format(ch_name))
            #
            # fig.suptitle("{} lap ".format(exp_name))
            # fig.tight_layout(rect=[0, 0.03, 1, 0.95])
            # # fig.savefig("results/{} lap.png".format(exp_name))

            plt.show()
