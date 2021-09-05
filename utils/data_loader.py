
import numpy as np
import pdb
import pandas as pd

from scipy import io

import mne


class DataLoader():
    total_exp_number = 43
    
    record_folder = r"D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\offline_processing"
    
    def __init__(self, exp_counter):
        self.exp_counter = exp_counter
        self.trial_removel_list = []

        self.mapping = {100: 'exe', 200: "rest", 300: "img", 400: "eye fixed", 500: "watching cue", 10: "left",
                        20: "right", 1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}


    def init_task_dependent_variables(self):
        # set up task-dependent variables
        if self.exp_counter < 12:  # right hand movement
            self.fs = 1200
            self.n_trial = 25
            self.channel_dict = {'C5': 0, 'FC3': 1, 'CP3': 2, 'C3': 3, 'C1': 4, 'FCz': 5, 'Cz': 6, 'CPz': 7, 'C2': 8}
            self.channel_names = ['C5', 'FC3', 'CP3', 'C3', 'C1', 'FCz', 'Cz', 'CPz', 'C2']
            self.channel_type = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg","eeg"]
            self.channel_position_dict = {'C5': 6, 'FC3': 2, 'CP3': 12, 'C3': 7, 'C1': 8, 'FCz': 4, 'Cz': 9, 'CPz': 14,
                                     'C2': 10}
            self.lap_C3_ch = [self.channel_dict['C3'], self.channel_dict['FC3'], self.channel_dict['C5'], self.channel_dict['CP3'],
                         self.channel_dict['C1']]
            self.lap_Cz_ch = [self.channel_dict['Cz'], self.channel_dict['FCz'], self.channel_dict['C1'], self.channel_dict['CPz'],
                         self.channel_dict['C2']]
            self.channel_ind = np.arange(2, 11)
            self.n_channel = 9
            self.single_trial_ylim = [-60, 60]
            self.average_trial_ylim = [-30, 30]
        elif 12 <= self.exp_counter < 24 or 42 <= self.exp_counter <= 53:  # left hand movement
            self.fs = 1200
            self.n_trial = 35
            self.channel_dict = {'FC4': 0, 'C4': 1, 'C6': 2, 'CP4': 3, 'C1': 4, 'FCz': 5, 'Cz': 6, 'CPz': 7, 'C2': 8}
            self.channel_names = list(self.channel_dict.keys())
            self.channel_position_dict = {'FC4': 4, 'C4': 9, 'C6': 10, 'CP4': 14, 'C1': 6, 'FCz': 2, 'Cz': 7, 'CPz': 12,
                                     'C2': 8}
            self.channel_type = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg","eeg"]
            self.lap_C4_ch = [self.channel_dict['C4'], self.channel_dict['FC4'], self.channel_dict['C2'], self.channel_dict['CP4'],
                         self.channel_dict['C6']]
            self.lap_Cz_ch = [self.channel_dict['Cz'], self.channel_dict['FCz'], self.channel_dict['C1'], self.channel_dict['CPz'],
                         self.channel_dict['C2']]
            self.lap_C2_ch = [self.channel_dict['C2'], self.channel_dict['C4'], self.channel_dict['Cz']]
            self.channel_ind = np.arange(2, 11)
            self.n_channel = 9
            self.single_trial_ylim = [-50, 50]
            self.average_trial_ylim = [-20, 20]
        elif 24 <= self.exp_counter < 36:  # RIGHT hand movement round 2
            self.fs = 1200
            self.n_trial = 19
            self.channel_dict = {'FC4': 0, 'C4': 1, 'C6': 2, 'CP4': 3, 'C1': 4, 'FCz': 5, 'Cz': 6, 'CPz': 7, 'C2': 8,
                            'C3': 9, 'CP3': 10, 'FC3': 11, 'C5': 12}
            self.channel_type = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg","eeg", "eeg","eeg", "eeg","eeg"]
            self.channel_position_dict = {'FC4': 6, 'C4': 13, 'C6': 14, 'CP4': 20, 'C1': 10, 'FCz': 4, 'Cz': 11, 'CPz': 18,
                                     'C2': 12, 'C3': 9, 'CP3': 16, 'FC3': 2, 'C5': 8}
            self.channel_names = list(self.channel_dict.keys())
            self.lap_C4_ch = [self.channel_dict['C4'], self.channel_dict['FC4'], self.channel_dict['C2'], self.channel_dict['CP4'],
                         self.channel_dict['C6']]
            self.lap_Cz_ch = [self.channel_dict['Cz'], self.channel_dict['FCz'], self.channel_dict['C1'], self.channel_dict['CPz'],
                         self.channel_dict['C2']]
            self.lap_C3_ch = [self.channel_dict['C3'], self.channel_dict['FC3'], self.channel_dict['C5'], self.channel_dict['CP3'],
                         self.channel_dict['C1']]
            self.channel_ind = np.arange(2, 15)
            self.n_channel = 13
            self.exe_event_number = 100
            self.img_event_number = 300
            self.rest_event_number = 200
            self.single_trial_ylim = [-50, 50]
            self.average_trial_ylim = [-20, 20]
        elif 36 <= self.exp_counter < 42:
            self.fs = 1200
            self.n_trial = 20
            self.channel_dict = {'Fp1': 0, 'AF3': 1, 'Fp2': 2, 'AF4': 3, 'C1': 4, 'FCz': 5, 'Cz': 6, 'CPz': 7, 'C2': 8,
                            'C3': 9, 'CP3': 10, 'FC3': 11, 'C5': 12}
            self.channel_type = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg","eeg", "eeg","eeg", "eeg","eeg"]
            self.channel_names = list(self.channel_dict.keys())
            self.channel_position_dict = {'C5': 6, 'FC3': 2, 'CP3': 12, 'C3': 7, 'C1': 8, 'FCz': 4, 'Cz': 9, 'CPz': 14,
                                     'C2': 10}
            self.lap_Cz_ch = [self.channel_dict['Cz'], self.channel_dict['FCz'], self.channel_dict['C1'], self.channel_dict['CPz'],
                         self.channel_dict['C2']]
            self.lap_C3_ch = [self.channel_dict['C3'], self.channel_dict['FC3'], self.channel_dict['C5'], self.channel_dict['CP3'],
                         self.channel_dict['C1']]
            self.channel_ind = np.arange(2, 15)
            self.n_channel = 13
            self.exe_event_number = 100.
            self.rest_event_number = 200.
            self.eye_fixed_event_number = 400.
            self.watching_cue_event_number = 500.
            self.task_event_number = 6.
            self.single_trial_ylim = [-50, 50]
            self.average_trial_ylim = [-20, 20]
        elif 55 <= self.exp_counter <100:

            self.fs = 1200
            if self.exp_counter == 57:
                self.fs = 256
            self.channel_dict = {'Fp1': 1, 'Fp2': 2, 'F3': 11, 'Fz': 9, 'F4': 6, 'T7': 3, 'C3': 8, 'Cz': 7, 'C4': 4,
                                 'T8': 5, 'P3': 12, 'Pz': 10, 'P4': 13}
            self.channel_type = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg",
                                 "eeg"]
            self.channel_names = list(self.channel_dict.keys())
            self.channel_ind = list(self.channel_dict.values())
            self.channel_ind = [x + 1 for x in self.channel_ind]
            self.n_channel = len(self.channel_names)

        elif 100 <= self.exp_counter <= 113:
            self.fs = 500
            self.channel_dict = {'Fp1': 17,  'Fp2': 13, 'F3': 16, 'Fz': 14, 'F4': 12, 'C3': 15, 'Cz': 3, 'C4': 11,
                                 'Pz': 4,  'P3': 5, 'P4': 2}

            self.channel_type = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg","eeg", "eeg","eeg"]
            self.channel_names = list(self.channel_dict.keys())
            # self.lap_Cz_ch = [self.channel_dict['Cz'], self.channel_dict['FCz'], self.channel_dict['C1'], self.channel_dict['CPz'],
            #              self.channel_dict['C2']]
            # self.lap_C3_ch = [self.channel_dict['C3'], self.channel_dict['FC3'], self.channel_dict['C5'], self.channel_dict['CP3'],
            #              self.channel_dict['C1']]
            self.channel_ind = list(self.channel_dict.values())
            self.channel_ind = [x+1 for x in self.channel_ind]
            self.n_channel = 11
            self.exe_event_number = 100.
            self.rest_event_number = 200.
            self.eye_fixed_event_number = 400.
            self.watching_cue_event_number = 500.
            self.task_event_number = 6.
            self.single_trial_ylim = [-50, 50]
            self.average_trial_ylim = [-20, 20]
        elif 114 <= self.exp_counter<126:#NE
            self.fs = 500
            self.channel_dict = {'Fp1': 17,  'Fp2': 13, 'F3': 16, 'Fz': 14, 'F4': 12, 'FC1': 19, 'FC2': 10, 'C1': 1,
                                 'C2': 6, 'C3': 15, 'Cz': 3, 'C4': 11, 'T7': 9, 'T8': 18, 'Pz': 4,  'P3': 5, 'P4': 2}

            self.channel_type = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg",
                                 "eeg", "eeg", "eeg", "eeg", "eeg"]
            self.channel_names = list(self.channel_dict.keys())
            self.channel_ind = list(self.channel_dict.values())
            self.channel_ind = [x+1 for x in self.channel_ind]
            self.n_channel = 17
            
        elif 126 <= self.exp_counter < 132:#NE
            self.fs = 500
            self.channel_dict = {'Fp1': 17, 'Fp2': 13, 'F3': 16, 'Fz': 14, 'F4': 12, 'C3': 15, 'Cz': 3, 'C4': 11,
                                 'T7': 18, 'T8': 9, 'Pz': 4, 'P3': 5, 'P4': 2}

            self.channel_type = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg",
                                 "eeg"]
            self.channel_names = list(self.channel_dict.keys())
            self.channel_ind = list(self.channel_dict.values())
            self.channel_ind = [x + 1 for x in self.channel_ind]
            self.n_channel = 13
            
        elif 132 <= self.exp_counter < 142:
            self.fs = 500
            self.channel_dict = {'P7': 1,
                                 'P4': 2,
                                 'Cz': 3,
                                 'Pz': 4,
                                 'P3': 5,
                                 'P8': 6,
                                 'O1': 7,
                                 'O2': 8,
                                 'T8': 9,
                                 'F8': 10,
                                 'C4': 11,
                                 'F4': 12,
                                 'Fp2': 13,
                                 'Fz': 14,
                                 'C3': 15,
                                 'F3': 16,
                                 'Fp1': 17,
                                 'T7': 18,
                                 'F7': 19,
                                 'Fpz': 20,
                                 'C2': 21,
                                 'FC6': 22,
                                 'FC2': 23,
                                 'AF4': 24,
                                 'CP6': 25,
                                 'CP2': 26,
                                 'CP1': 27,
                                 'CP5': 28,
                                 'FC1': 29,
                                 'FC5': 30,
                                 'AF3': 31,
                                 'C1': 32}
            self.channel_type = 'eeg'
            self.channel_names = list(self.channel_dict.keys())
            self.channel_ind = list(self.channel_dict.values())
            self.channel_ind = [x + 1 for x in self.channel_ind]
            self.n_channel = 32
        elif 142 <= self.exp_counter < 145:
            self.fs = 500
            self.channel_dict = {'P7': 1,
                                 'P4': 2,
                                 'Cz': 3,
                                 'Pz': 4,
                                 'P3': 5,
                                 'P8': 6,
                                 'EMG_SL': 7,
                                 'O2': 8,
                                 'T8': 9,
                                 'F8': 10,
                                 'C4': 11,
                                 'F4': 12,
                                 'Fp2': 13,
                                 'Fz': 14,
                                 'C3': 15,
                                 'F3': 16,
                                 'Fp1': 17,
                                 'T7': 18,
                                 'F7': 19,
                                 'EMG_WL':20,
                                 'EMG_SR': 21,
                                 'FC6': 22,
                                 'FC2': 23,
                                 'C2': 24,
                                 'CP6': 25,
                                 'CP2': 26,
                                 'CP1': 27,
                                 'CP5': 28,
                                 'FC1': 29,
                                 'FC5': 30,
                                 'C1': 31,
                                 'EMG_WR': 32}
                                 
            self.channel_type = ['eeg','eeg','eeg','eeg','eeg','eeg','emg','eeg','eeg',
                                 'eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg',
                                 'eeg','emg','emg','eeg','eeg','eeg','eeg','eeg','eeg',
                                 'eeg','eeg','eeg','eeg','emg']
                                 
            self.channel_names = list(self.channel_dict.keys())
            self.channel_ind = list(self.channel_dict.values())
            self.channel_ind = [x + 1 for x in self.channel_ind]
            self.n_channel = 32
            
        elif 145 <= self.exp_counter < 200 or 300 <= self.exp_counter <=301:
            self.fs = 500
            self.channel_dict = {'P7': 1,
                                 'P4': 2,
                                 'Cz': 3,
                                 'Pz': 4,
                                 'P3': 5,
                                 'P8': 6,
                                 'EMG_WE_right': 7,
                                 'EMG_IE_right': 8,
                                 'T8': 9,
                                 'F8': 10,
                                 'C4': 11,
                                 'F4': 12,
                                 'Fp2': 13,
                                 'Fz': 14,
                                 'C3': 15,
                                 'F3': 16,
                                 'Fp1': 17,
                                 'T7': 18,
                                 'F7': 19,

                                 'EMG_IE_left': 21,
                                 'FC6': 22,
                                 'FC2': 23,
                                 'C2': 24,
                                 'CP6': 25,
                                 'CP2': 26,
                                 'CP1': 27,
                                 'CP5': 28,
                                 'FC1': 29,
                                 'FC5': 30,
                                 'C1': 31,
                                 'EMG_WE_left': 32}
                                 
            self.channel_type = ['eeg','eeg','eeg','eeg','eeg','eeg','emg','emg','eeg',
                                 'eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg',
                                 'eeg','emg','eeg','eeg','eeg','eeg','eeg','eeg',
                                 'eeg','eeg','eeg','eeg','emg']
                                 
            self.channel_names = list(self.channel_dict.keys())
            self.channel_ind = list(self.channel_dict.values())
            self.channel_ind = [x + 1 for x in self.channel_ind]
            self.n_channel = len(self.channel_ind)
            
        elif 302 <= self.exp_counter < 306:
            self.fs = 500
            self.channel_dict = {'P7': 1,
                                 'P4': 2,
                                 'Cz': 3,
                                 'Pz': 4,
                                 'P3': 5,
                                 'P8': 6,
                                 'EMG_WE_right': 7,
                                 'EMG_IE_right': 8,
                                 'T8': 9,
                                 'F8': 10,
                                 'C4': 11,
                                 'F4': 12,
                                 'Fp2': 13,
                                 'Fz': 14,
                                 'C3': 15,
                                 'F3': 16,
                                 'Fp1': 17,
                                 'T7': 18,
                                 'F7': 19,

                                 'EMG_IE_left': 21,
                                 'FC6': 22,
                                 'FC2': 23,
                                 'C2': 24,
                                 'CP6': 25,
                                 'CP2': 26,
                                 'CP1': 27,
                                 'CP5': 28,
                                 'FC1': 29,
                                 'FC5': 30,
                                 'C1': 31,
                                 'EMG_WE_left': 20}
                                 
            self.channel_type = ['eeg','eeg','eeg','eeg','eeg','eeg','emg','emg','eeg',
                                 'eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg',
                                 'eeg','emg','eeg','eeg','eeg','eeg','eeg','eeg',
                                 'eeg','eeg','eeg','eeg','emg']
                                 
            self.channel_names = list(self.channel_dict.keys())
            self.channel_ind = list(self.channel_dict.values())
            self.channel_ind = [x + 1 for x in self.channel_ind]
            self.n_channel = len(self.channel_ind)
            
            
            
        elif self.exp_counter == 306:
            self.fs = 500
            self.channel_dict = {'P7': 1,
                                 'P4': 2,
                                 'Cz': 3,
                                 'Pz': 4,
                                 'P3': 5,
                                 'P8': 6,
                                 'EMG_WE_right': 7,
                                 'EMG_IE_right': 8,
                                 'T8': 9,
                                 'F8': 10,
                                 'C4': 11,
                                 'F4': 12,
                                 'Fp2': 13,
                                 'Fz': 14,
                                 'C3': 15,
                                 'F3': 16,
                                 'Fp1': 17,
                                 'T7': 18,
                                 'F7': 19,

                                 'EMG_IE_left': 21,
                                 'FC6': 32,
                                 'FC2': 23,
                                 'C2': 24,
                                 'CP6': 25,
                                 'CP2': 26,
                                 'CP1': 27,
                                 'CP5': 28,
                                 'FC1': 29,
                                 'FC5': 30,
                                 'C1': 31,
                                 'EMG_WE_left': 20}
                                 
            self.channel_type = ['eeg','eeg','eeg','eeg','eeg','eeg','emg','emg','eeg',
                                 'eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg',
                                 'eeg','emg','eeg','eeg','eeg','eeg','eeg','eeg',
                                 'eeg','eeg','eeg','eeg','emg']
                                 
            self.channel_names = list(self.channel_dict.keys())
            self.channel_ind = list(self.channel_dict.values())
            self.channel_ind = [x + 1 for x in self.channel_ind]
            self.n_channel = len(self.channel_ind)
            
            
        elif 307 <= self.exp_counter < 350:
            self.fs = 500
            self.channel_dict = {'P7': 1,
                                 'P4': 2,
                                 'Cz': 3,
                                 'Pz': 4,
                                 'P3': 5,
                                 'P8': 6,
                                 'EMG_WE_right': 7,
                                 'EMG_IE_right': 8,
                                 'T8': 9,
                                 'F8': 10,
                                 'C4': 11,
                                 'F4': 12,
                                 'Fp2': 13,
                                 'Fz': 14,
                                 'C3': 15,
                                 'F3': 16,
                                 'Fp1': 17,
                                 'T7': 18,
                                 'F7': 19,

                                 'EMG_IE_left': 21,
                                 'FC6': 22,
                                 'FC2': 23,
                                 'C2': 24,
                                 'CP6': 25,
                                 'CP2': 26,
                                 'CP1': 27,
                                 'CP5': 28,
                                 'FC1': 29,
                                 'FC5': 30,
                                 'C1': 31,
                                 'EMG_WE_left': 20}
                                 
            self.channel_type = ['eeg','eeg','eeg','eeg','eeg','eeg','emg','emg','eeg',
                                 'eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg',
                                 'eeg','emg','eeg','eeg','eeg','eeg','eeg','eeg',
                                 'eeg','eeg','eeg','eeg','emg']
                                 
            self.channel_names = list(self.channel_dict.keys())
            self.channel_ind = list(self.channel_dict.values())
            self.channel_ind = [x + 1 for x in self.channel_ind]
            self.n_channel = len(self.channel_ind)
            
            
        elif 200 < self.exp_counter < 205:
            self.fs = 500
            self.channel_dict = {'Fp1': 1, 'Fp2': 32, 'F3': 3, 'Fz': 2, 'F4': 30, 'C3': 8, 'Cz': 24, 'C4': 25,
                                 'T7': 9, 'T8': 26, 'Pz': 13, 'P3': 14, 'P4': 19}
            # self.channel_dict = {'Fp1': 1, 'Fz': 2, 'F3': 3, 'F7': 4, 'F9': 5, 'FC5': 6, 'FC1': 7, 'C3': 8, 'T7': 9,
            #                      'TP9':10, 'CP5': 11, 'CP1':12, 'Pz':13, 'P3':14, 'P7':15, 'O1':16, 'Oz':17, 'O2':18,
            #                      'P4':19, 'P8':20, 'CP10': 21, 'CP6': 22, 'CP2': 23, 'Cz': 24, 'C4': 25, 'T8': 26,
            #                      'F10': 27, 'FC6': 28, 'FC2': 29, 'F4': 30, 'F8': 31, 'Fp2':32}

            self.channel_type = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg",
                                 "eeg"]

            # self.channel_type = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg",
            #                      "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg",
            #                      "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg"]
            self.channel_names = list(self.channel_dict.keys())
            self.channel_ind = list(self.channel_dict.values())
            self.channel_ind = [x + 1 for x in self.channel_ind]
            self.n_channel = len(self.channel_names)
        elif 205 <= self.exp_counter <= 207:
            self.mapping = {10: "EE_l", 20: "EE_r", 30: "R_l", 40: "R_r", 50: "WE_l", 60: "WE_r", 90: "AD",
                            1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
            self.fs = 500
            # self.channel_dict = {'Fp1': 1, 'Fp2': 32, 'F3': 3, 'Fz': 2, 'F4': 30, 'C3': 8, 'Cz': 24, 'C4': 25,
            #                      'T7': 9, 'T8': 26, 'Pz': 13, 'P3': 14, 'P4': 19}
            self.channel_dict = {'Fp1': 1, 'Fz': 2, 'F3': 3, 'F7': 4, 'FT9': 5, 'FC5': 6, 'FC1': 7, 'C3': 8, 'T7': 9,
                                 'TP9':10, 'CP5': 11, 'CP1':12, 'Pz':13, 'P3':14, 'P7':15, 'O1':16, 'Oz':17, 'O2':18,
                                 'P4':19, 'P8':20, 'TP10': 21, 'CP6': 22, 'CP2': 23, 'Cz': 24, 'C4': 25, 'T8': 26,
                                 'FT10': 27, 'FC6': 28, 'FC2': 29, 'F4': 30, 'F8': 31, 'Fp2':32}

            self.channel_type = 'eeg'

            # self.channel_type = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg",
            #                      "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg",
            #                      "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg"]
            self.channel_names = list(self.channel_dict.keys())
            self.channel_ind = list(self.channel_dict.values())
            self.channel_ind = [x + 1 for x in self.channel_ind]
            self.n_channel = len(self.channel_names)

        elif self.exp_counter >= 2000:
            self.fs = 500
            self.channel_dict = {'EMG': 33}
            # self.channel_dict = {'Fp1': 1, 'Fz': 2, 'F3': 3, 'F7': 4, 'FT9': 5, 'FC5': 6, 'FC1': 7, 'C3': 8, 'T7': 9,
            #                      'TP9':10, 'CP5': 11, 'CP1':12, 'Pz':13, 'P3':14, 'P7':15, 'O1':16, 'Oz':17, 'O2':18,
            #                      'P4':19, 'P8':20, 'TP10': 21, 'CP6': 22, 'CP2': 23, 'Cz': 24, 'C4': 25, 'T8': 26,
            #                      'FT10': 27, 'FC6': 28, 'FC2': 29, 'F4': 30, 'F8': 31, 'Fp2':32, 'EMG':33}

            self.channel_type = 'emg'

            # self.channel_type = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg",
            #                      "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg",
            #                      "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "emg"]
            self.channel_names = list(self.channel_dict.keys())
            self.channel_ind = list(self.channel_dict.values())
            self.channel_ind = [x + 1 for x in self.channel_ind]
            self.n_channel = len(self.channel_names)



    def load_data(self):

        if self.exp_counter == 0:
            self.exp_name = "right wrist extension exe"
            self.base_folder = DataLoader.record_folder + r"\\records/Pilot_right_wrist_extension_1_2020-04-27/Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_wrist_extension_exe_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 1:
            self.exp_name = "right wrist extension img"
            self.base_folder = DataLoader.record_folder + r"\\records/Pilot_right_wrist_extension_1_2020-04-27/Run2"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_wrist_extension_img_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 2:
            self.exp_name = "right wrist flexion exe"
            self.base_folder = DataLoader.record_folder + r"\\records/Pilot_right_wrist_flexion_1_2020-04-27/Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_wrist_flexion_exe_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 3:
            self.exp_name = "right wrist flexion img"
            self.base_folder = DataLoader.record_folder + r"\\records/Pilot_right_wrist_flexion_1_2020-04-27/Run2"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_wrist_flexion_img_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 4:
            self.exp_name = "right fisting exe"
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_right_fisting_1_2020-04-27/Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_fisting_exe_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 5:
            self.exp_name = "right fisting img"
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_right_fisting_1_2020-04-27/Run2"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_fisting_img_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 6:
            self.exp_name = "right index extension exe"
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_right_index_extension_1_2020-04-27/Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_index_extension_exe_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 7:
            self.exp_name = "right index extension img"
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_right_index_extension_1_2020-04-27/Run2"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_index_extension_img_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 8:
            self.exp_name = "right center out reaching with object exe"
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_right_reaching_with_object_1_2020-04-27/Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_reaching_with_object_exe_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 9:
            self.exp_name = "right center out reaching with object img"
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_right_reaching_with_object_1_2020-04-27/Run2"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_reaching_with_object_img_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 10:
            self.exp_name = "right reaching without object exe"
            # trial_removel_list = [0, 2, 3, 5, 11, 13, 14, 17, 18, 19, 21, 22, 23]
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_right_reaching_without_object_1_2020-04-27/Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_reaching_without_object_exe_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 11:
            self.exp_name = "right reaching without object img"
            self.n_trial = 16
            # trial_removel_list = [2, 5, 10, 12, 15]
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_right_reaching_without_object_img_2020-04-27/Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_reaching_without_object_img_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 12:
            self.exp_name = "left wrist extension exe"
            # trial_removel_list = [0, 3, 8, 10, 17, 21, 23, 25, 27, 30, 34]
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_left_wrist_extension_1_2020-04-30/Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/left_wrist_extension_exe_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 13:
            self.exp_name = "left wrist extension img"
            # trial_removel_list = [0, 5, 6, 12, 10, 16, 17, 19, 20, 21, 23, 30, 31]
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_left_wrist_extension_1_2020-04-30/Run2"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/left_wrist_extension_img_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 14:
            self.exp_name = "left wrist flexion exe"
            # trial_removel_list = [16, 18, 9, 23, 27, 33]
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_left_wrist_flexion_1_2020-04-30/Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/left_wrist_flexion_exe_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 15:
            self.exp_name = "left wrist flexion img"
            # trial_removel_list = [0, 6, 8, 14, 17, 18, 16, 24, 25, 26, 32]
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_left_wrist_flexion_1_2020-04-30/Run2"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/left_wrist_flexion_img_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 16:
            self.exp_name = "left fisting exe"
            # trial_removel_list = [0, 9, 25, 31, 33]
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_left_fisting_1_2020-04-30/Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/left_fisting_exe_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 17:
            self.exp_name = "left fisting img"
            # trial_removel_list = [4, 5, 6, 8, 18, 20]
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_left_fisting_1_2020-04-30/Run2"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/left_fisting_img_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])

        elif self.exp_counter == 18:
            self.exp_name = "left index extension exe"
            # trial_removel_list = [1, 2, 3, 12, 21, 28, 32]
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_left_index_extension_1_2020-04-30/Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/left_index_extension_exe_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 19:
            self.exp_name = "left index extension img"
            # trial_removel_list = [2, 5, 17, 24]
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_left_index_extension_1_2020-04-30/Run2"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/left_index_extension_img_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])

        elif self.exp_counter == 20:
            self.exp_name = "left center out reaching with object exe"
            # trial_removel_list = [2, 5, 8, 9, 14, 24, 34]
            trial_removel_list = [2]
            self.EB_removed_eeg = io.loadmat(
                '..\\records\pilot_left_reaching_with_object_1_2020-04-30\Run1\left_reaching_with_object_EB_removed_data.mat')
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_left_reaching_with_object_1_2020-04-30/Run1"
        elif self.exp_counter == 21:
            self.exp_name = "left center out reaching with object img"
            # trial_removel_list = [7, 18, 21, 29, 30, 31]
            # trial_removel_list = [0]
            self.EB_removed_eeg = io.loadmat(
                '..\\records\pilot_left_reaching_with_object_1_2020-04-30\Run2\left_reaching_with_object_EB_removed_data.mat')
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_left_reaching_with_object_1_2020-04-30/Run2"
        elif self.exp_counter == 22:
            self.exp_name = "left reaching without object exe"
            # trial_removel_list = [10, 28, 30, 33, 34]
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_left_reaching_without_object_1_2020-04-30/Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/left_reaching_without_object_exe_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 23:
            self.exp_name = "left reaching without object img"
            # trial_removel_list = [10, 17, 28, 30, 32, 33, 34]
            self.base_folder = DataLoader.record_folder + r"\\records/pilot_left_reaching_without_object_1_2020-04-30/Run2"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/left_reaching_without_object_img_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 24:
            self.exp_name = "right reaching with object exe round 2"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_right_reaching_with_object_2_2020-05-22\Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_reaching_with_object_exe_round2_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 25:
            self.exp_name = "right reaching with object img round 2"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_right_reaching_with_object_2_2020-05-22\Run2"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_reaching_with_object_img_round2_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 26:
            self.exp_name = "right reaching without object exe round 2"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_right_reaching_without_object_2_2020-05-22\Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_reaching_without_object_exe_round2_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 27:
            self.exp_name = "right reaching without object img round 2"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_right_reaching_without_object_2_2020-05-22\Run2"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_reaching_without_object_img_round2_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 28:
            self.exp_name = "right wrist extension exe round 2"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_right_wrist_extension_2_2020-05-22\Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_wrist_extension_exe_round2_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 29:
            self.exp_name = "right wrist extension img round 2"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_right_wrist_extension_2_2020-05-22\Run2"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_wrist_extension_img_round2_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 30:
            self.exp_name = "right wrist flexion exe round 2"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_right_wrist_flexion_2_2020-05-22\Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_wrist_flexion_exe_round2_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 31:
            self.exp_name = "right wrist flexion img round 2"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_right_wrist_flexion_2_2020-05-22\Run2"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_wrist_flexion_img_round2_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 32:
            self.exp_name = "right fisting exe round 2"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_right_fsting_2_2020-05-22\Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_fisting_exe_round2_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 33:
            self.exp_name = "right fisting img round 2"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_right_fsting_2_2020-05-22\Run2"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_fisting_img_round2_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 34:
            self.exp_name = "right index extension exe round 2"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_right_index_extension_2_2020-05-22\Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_index_extension_exe_round2_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 35:
            self.exp_name = "right index extension img round 2"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_right_index_extension_2_2020-05-22\Run2"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_index_extension_img_round2_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 36:
            self.event = self.eye_fixed_event_number
            self.exp_name = "eye fixed"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_eye_fixed_2020-05-25\Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/eye_fixed_EB_removed_data.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 37:
            self.event = self.watching_cue_event_number
            self.exp_name = "watching cues"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_watching_cue_2020-05-25\Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/watching_cue.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 38:
            self.event = self.exe_event_number
            self.exp_name = "Index extension followed by rest"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_10_IEexe_10_rest_2020-05-25\Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/index_extension_followed_by_rest.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 39:
            self.event = self.exe_event_number
            self.exp_name = "Index extension with rest randomized"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_index_extension_rest_random_2020-05-25\Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/index_extension_rest_randomize.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 40:
            self.exp_name = "right index extension random interval"
            self.event = self.task_event_number
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_index_extension_random_interval_new_2020-05-28\Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/index_extension_random_interval.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 41:
            self.exp_name = "right index extension rest + task"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_right_index_extension_10_rest_10_exe_2020-05-28\Run1"
            self.EB_removed_eeg = io.loadmat(self.base_folder + "/right_index_extension_rest_task.mat")
            self.EB_removed_data = np.transpose(self.EB_removed_eeg['ans'])
        elif self.exp_counter == 42:
            self.exp_name = "Ailin left reaching with object exe"
            self.base_folder = DataLoader.record_folder + r"\records\Ailin_reaching_with_object_1_2020-05-07\Run1"
        elif self.exp_counter == 43:
            self.exp_name = "Ailin left reaching with object img"
            self.base_folder = "\Ailin_reaching_with_object_1_2020-05-07\Run2"
        elif self.exp_counter == 44:
            self.exp_name = "Ailin left reaching without object exe"
            self.base_folder = DataLoader.record_folder + r"\records\Ailin_reaching_without_object_1_2020-05-07\Run1"
        elif self.exp_counter == 45:
            self.exp_name = "Ailin left reaching without object img"
            self.base_folder = DataLoader.record_folder + r"\records\Ailin_reaching_without_object_1_2020-05-07\Run2"
        elif self.exp_counter == 46:
            self.exp_name = "Ailin left wrist flexion exe"
            self.base_folder = DataLoader.record_folder + r"\records\Ailin_left_wrist_flexion_1_2020-05-06\Run1"
        elif self.exp_counter == 47:
            self.exp_name = "Ailin left wrist flexion img"
            self.base_folder = DataLoader.record_folder + r"\records\Ailin_left_wrist_flexion_1_2020-05-06\Run2"
        elif self.exp_counter == 48:
            self.exp_name = "Ailin left wrist extension exe"
            self.base_folder = DataLoader.record_folder + r"\records\Ailin_left_wrist_extension_1_2020-05-06\Run1"
        elif self.exp_counter == 49:
            self.exp_name = "Ailin left wrist extension img"
            self.base_folder = DataLoader.record_folder + r"\records\Ailin_left_wrist_extension_1_2020-05-06\Run2"
        elif self.exp_counter == 50:
            self.exp_name = "Ailin left index extension exe"
            self.base_folder = DataLoader.record_folder + r"\records\Ailin_index_extension_1_2020-05-07\Run1"
        elif self.exp_counter == 51:
            self.exp_name = "Ailin left index extension img"
            self.base_folder = DataLoader.record_folder + r"\records\Ailin_index_extension_1_2020-05-07\Run2"
        elif self.exp_counter == 52:
            self.exp_name = "Ailin left fisting exe"
            self.base_folder = DataLoader.record_folder + r"\records\Ailin_left_fisting_1_2020-05-06\Run1"
        elif self.exp_counter == 53:
            self.exp_name = "Ailin left fisting img"
            self.base_folder = DataLoader.record_folder + r"\records\Ailin_left_fisting_1_2020-05-06\Run2"
        elif self.exp_counter == 100:
            self.exp_name = " Jiansheng_NE_10rest+10FXexe"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_NE_10rest+10FXexe_2020-06-22\Run1"
        elif self.exp_counter ==101:
            self.exp_name = " NE pure rest"
            self.base_folder = DataLoader.record_folder + r"\\records\Jianshen_NE_pure_rest_2020-06-22\Run1"
        elif self.exp_counter == 102:
            self.exp_name = "NE pure rest 2"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_NE_pure_rest_2_2020-06-22\Run1"
        elif self.exp_counter == 103:
            self.exp_name = "NE random right IE exe"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_NE_random_right_IE_3_2020-06-22\Run1"
        elif self.exp_counter == 104:
            self.exp_name = " NE rest + right WE exe"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_NE_rest+right_WE_2020-06-22\Run1"
        elif self.exp_counter == 105:
            self.exp_name = " NE rest + right WE img"
            self.base_folder = DataLoader.record_folder + r"\\records\Jiansheng_NE_right_WE_img_2020-06-22\Run1"
        elif self.exp_counter == 106:
            self.exp_name = "NE record test"
            self.base_folder = r"C:\uw_ebionics_mrcp_online_interface_python\\records\NE_record_test_2_2020-06-23\Run1"
        elif self.exp_counter == 107:
            self.exp_name = "NE_noise_test"
            self.base_folder = DataLoader.record_folder + r"\\records\NE_noise_test1_2020-06-25\Run1"
        elif self.exp_counter == 108:
            self.exp_name = "NE_left_reaching_without_object"
            self.base_folder = DataLoader.record_folder + r"\\records\NE_left_CRO_2020-06-25\Run1"
        elif self.exp_counter == 109:
            self.exp_name = "NE_AD"
            self.base_folder = DataLoader.record_folder + r"\\records\NE_AD_exe_2020-06-25\Run1"
        elif self.exp_counter == 110:
            self.exp_name = "NE_rest"
            self.base_folder = DataLoader.record_folder + r"\records\NE_rest_test_2020-06-30\Run1"
        elif self.exp_counter == 111:
            self.exp_name = "NE_right_IE_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_IE_right_2020-06-30\Run1"
        elif self.exp_counter == 112:
            self.exp_name = "NE_right_IE_img"
            self.base_folder = DataLoader.record_folder + r"\records\NE_IE_right_2020-06-30\Run2"
        elif self.exp_counter == 113:
            self.exp_name = "NE_left_IE_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_JN_left_IE_exe_2020-06-30\Run1"
        elif self.exp_counter == 114:
            self.exp_name = "NE_Ailin_IE_right_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Ailin_IE_right_exe_2020-07-02\Run1"
        elif self.exp_counter == 115:
            self.exp_name = "NE_Ailin_IE_left_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Ailin_left_IE_2_exe_2020-07-02\Run1"
        elif self.exp_counter == 116:
            self.exp_name = "NE_Ailin_WE_right_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Ailin_right_WE_exe_2020-07-02\Run1"
        elif self.exp_counter == 117:
            self.exp_name = "NE_Ailin_WE_left_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Ailin_left_WE_exe_2020-07-02\Run1"
        elif self.exp_counter == 118:
            self.exp_name = "NE_Ailin_RwoO_right_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Ailin_right_RwoO_exe_2020-07-02\Run1"
        elif self.exp_counter == 119:
            self.exp_name = "NE_Ailin_RwoO_left_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Ailin_left_RwoO_exe_2020-07-02\Run1"
        elif self.exp_counter == 120:
            self.exp_name = "NE_Ailin_AD_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Ailin_right_AD_exe_2020-07-02\Run1"
        elif self.exp_counter == 121:
            self.exp_name = "NE_Jiansheng_IE_LR_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Jiansheng_IE_new_LR_exe_2020-07-09\Run1"
        elif self.exp_counter == 122:
            self.exp_name = "NE_Jiansheng_WE_LR1_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Jiansheng_WE_LR_exe_2020-07-09\Run1"
        elif self.exp_counter == 123:
            self.exp_name = "NE_Jiansheng_WE_LR2_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Jianhseng_WE_new_LR_exe_2020-07-09\Run1"
        elif self.exp_counter == 124:
            self.exp_name = "NE_Jiansheng_RwoO_LR1_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Jiansheng_RwoO_LR_exe_2020-07-09\Run1"
        elif self.exp_counter == 125:
            self.exp_name = "NE_Jiansheng_RwoO_LR2_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Jiansheng_RwoO_LR2_exe_2020-07-09\Run1"
        elif self.exp_counter == 126:
            self.exp_name = "NE_Ailin_IE_LR1_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Ailin_IE_LR_1_2020-07-19\Run1"
        elif self.exp_counter == 127:
            self.exp_name = "NE_Ailin_EF_LR1_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Ailin_EF_LR_1_2020-07-19\Run1"
        elif self.exp_counter == 128:
            self.exp_name = "NE_Ailin_RwoO_LR1_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Ailin_EF_LR_1_2020-07-19\Run1"
        elif self.exp_counter == 129:
            self.exp_name = "NE_Ailin_rest"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Ailin_rest_2020-09-08\Run1"
        elif self.exp_counter == 130:
            self.exp_name = "NE_Ailin_RwoO_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Ailin_RwoO_exe_2020-09-08\Run1"
        elif self.exp_counter == 131:
            self.exp_name = "NE_Ailin_WE_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Ailin_WE_exe_2020-09-08\Run1"
            
        elif self.exp_counter == 200:
            self.exp_name = "BP_Jiansheng_WE_LR_exe"
            self.base_folder = DataLoader.record_folder + r"\records\BP_Jiansheng_WE_LR_exe_2020-08-12\Run1"
        elif self.exp_counter == 201:
            self.exp_name = "BP_Jiansheng_RwoO_LR_exe"
            self.base_folder = DataLoader.record_folder + r"\records\BP_Jiansheng_RwoO_LR_2020-08-12\Run1"
        elif self.exp_counter == 2000:
            self.exp_name = "BP_EMG_test1"
            self.base_folder = DataLoader.record_folder + r"\records\BP_EMG_2020-08-13\Run1"
        elif self.exp_counter == 2001:
            self.exp_name = "BP_EMG_test2"
            self.base_folder = DataLoader.record_folder + r"\records\full_test1_2020-09-17\Run1"
        elif self.exp_counter == 2002:
            self.exp_name = "BP_EMG_test3"
            self.base_folder = DataLoader.record_folder + r"\records\EMG_test3_2020-09-17\Run1"
        elif self.exp_counter == 202:
            self.exp_name = "BP_Ailin_rest"
            self.base_folder = DataLoader.record_folder + r"\records\BP_Ailin_rest2_2020-08-27\Run1"
        elif self.exp_counter == 203:
            self.exp_name = "BP_Ailin_reaching_LR_exe"
            self.base_folder = DataLoader.record_folder + r"\records\BP_ailin_reaching_LR_exe_2020-08-27\Run1"
        elif self.exp_counter == 204:
            self.exp_name = "BP_Ailin_WE_LR_exe"
            self.base_folder = DataLoader.record_folder + r"\records\BP_Ailin_WE_lr_exe_2_2020-08-27\Run1"
        elif self.exp_counter == 55:
            self.exp_name = "gtec_Ailin_RwoO_LR_exe"
            self.base_folder = DataLoader.record_folder + r"\records\gTEC_aILIN_rWOo_lr_2020-09-01\Run1"
        elif self.exp_counter == 56:
            self.exp_name = "gtec_Ailin_WE_LR_exe"
            self.base_folder = DataLoader.record_folder + r"\records\gtec_Ailin_WE_LR_exe_2020-09-01\Run1"
        elif self.exp_counter == 57:
            self.exp_name = "gtec_Ailin_RwoO_LR_exe2"
            self.base_folder = DataLoader.record_folder + r"\records\GTEC_aILIN_RwoO_LR_exe_2020-09-01\Run1"
        elif self.exp_counter == 205:
            self.exp_name = "BP_Ning_upper_limb"
            self.base_folder = DataLoader.record_folder + r"\records\Ning_2020-09-11\Run1"
        elif self.exp_counter == 206:
            self.exp_name = "BP_Ning_AD"
            self.base_folder = DataLoader.record_folder + r"\records\Ning_AD_2020-09-11\Run1"
        elif self.exp_counter == 207:
            self.exp_name = "BP_saline_environment"
            self.base_folder = DataLoader.record_folder + r"\records\BP_saline_environment_2020-09-14\Run1"
        elif self.exp_counter == 132:
            self.exp_name = "NE_Jiansheng_rest"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Jiansheng_rest_2020-09-23\Run1"
            self.mapping = {10: "rest", 1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 133:
            self.exp_name = "NE_Jiansheng_Reaching_EE_WE_exe_LR"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Jiansheng_Reaching_EE_WE_exe_LR_2020-09-23\Run1"
            self.mapping = {10: "EE_l", 20: "EE_r", 30: "R_l", 40: "R_r", 50: "WE_l", 60: "WE_r", 90: "AD",
                            1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 134:
            self.exp_name = "NE_Jiansheng_AD"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Jiansheng_AD_exe_2020-09-23\Run1"
            self.mapping = {50: "AD", 1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 135:
            self.exp_name = "NE_Ning_rest"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Ning_rest_1_2020-10-02\Run1"
            self.mapping = {100: "rest", 1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 136:
            self.exp_name = "NE_Ning_rest2"
            self.base_folder = DataLoader.record_folder + r"\records\NE_ning_rest2_2020-10-02\Run1"
        elif self.exp_counter == 137:
            self.exp_name = "NE_Ning_WE_WF_exe"
            self.base_folder = DataLoader.record_folder + r"\records\NE_ning_WE_WF_2020-10-02\Run1"
            self.mapping = {10: "WE_r", 20: "WE_l", 30: "WF_l", 40: "WF_r", 1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
#             self.mapping = {1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 138:
            self.exp_name = "NE_Jiansheng_EMG_random_class"
            self.base_folder = DataLoader.record_folder + r"\records\NE_test_EMG_Random_class_2020-10-04\Run1"
            self.mapping = {110: "move", 120: "still", 1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 139:
            self.exp_name = "NE_Jiansheng_EMG_sync"
            self.base_folder = DataLoader.record_folder + r"\records\NE_Jiansheng_SYNC_test_2020-10-04\Run1"
            self.mapping = {110: "move", 120: "still", 1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 140:
            self.exp_name = "NE_timer_test15"
            self.base_folder = DataLoader.record_folder + r"\records\NE_timer_test15_2020-10-06\Run1"
            self.mapping = {10: "left", 30: "right", 1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 141:
            self.exp_name = "NE_timer_EMG_test"
            self.base_folder = DataLoader.record_folder + r"\records\NE_new_timer_EMG_test_2020-10-06\Run1"
            self.mapping = {90: "exe", 1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 142:
            self.exp_name = "NE_BO_rest"
            self.base_folder = DataLoader.record_folder + r"\records\Bo_rest_2020-10-10\Run1"
            self.mapping = {100: "rest", 1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
            
        elif self.exp_counter == 143:
            self.exp_name = "NE_BO_3LR"
            self.base_folder = DataLoader.record_folder + r"\records\NE_BO_3LR_2020-10-10\Run1"
            self.mapping = {10: "EE_l", 20: "EE_r", 30: "R_l", 40: "R_r", 50: "WE_l", 60: "WE_r", 1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
            
        elif self.exp_counter == 144:
            self.exp_name = "stop test"
            self.base_folder = DataLoader.record_folder + r"\records\IEWELR_test1_2020-10-16\Run1"
            self.mapping = {10: "EE_l", 20: "EE_r", 30: "R_l", 40: "R_r", 50: "WE_l", 60: "WE_r", 1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 145:
            self.exp_name = "IEWE EMG"
            self.base_folder = DataLoader.record_folder + r"\records\EMG_test_2020-10-16\Run1"
            self.mapping = {10: "IE_l", 20: "IE_r", 30: "WE_l", 40: "WE_r", 1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 146:
            self.exp_name = "Narsimha WEIE LR"
            self.base_folder = DataLoader.record_folder + r"\records\Narsimha_WEIE_LR_formal_2020-10-17\Run1"
            self.mapping = {10: "IE_l", 20: "IE_r", 30: "WE_l", 40: "WE_r", 100: "EMG_WE_l",
                            200: "EMG_WE_r", 300: "EMG_IE_l", 400: "EMG_IE_r",
                            1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 147:
            self.exp_name = "test WEIE LR"
            self.base_folder = DataLoader.record_folder + r"\records\test1_2020-11-13\Run1"
            self.mapping = {10: "IE_l", 20: "IE_r", 30: "WE_l", 40: "WE_r", 100: "EMG_WE_l",
                            200: "EMG_WE_r", 300: "EMG_IE_l", 400: "EMG_IE_r",
                            1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 148:
            self.exp_name = "Rebecca WEIE LR"
            self.base_folder = DataLoader.record_folder + r"\records\Rebecca4_2020-11-14\Run1"
            self.mapping = {10: "IE_l", 20: "IE_r", 30: "WE_l", 40: "WE_r", 100: "EMG_WE_l",
                            200: "EMG_WE_r", 300: "EMG_IE_l", 400: "EMG_IE_r",
                            1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 149:
            self.exp_name = "Stevie practice WEIE LR"
            self.base_folder = r"C:\Users\WILLS\Desktop\MRCP experiment\records\stevie_practice_2020-11-25\Run1"
            self.mapping = {10: "IE_l", 20: "IE_r", 30: "WE_l", 40: "WE_r", 100: "EMG_WE_l",
                            200: "EMG_WE_r", 300: "EMG_IE_l", 400: "EMG_IE_r",
                            1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 300:
            self.exp_name = "Ailin WEIE LR"
            self.base_folder = DataLoader.record_folder + r"\records\Ailin_2021-01-03\Run1"
            self.mapping = {10: "IE_l", 20: "IE_r", 30: "WE_l", 40: "WE_r", 100: "EMG_WE_l",
                            200: "EMG_WE_r", 300: "EMG_IE_l", 400: "EMG_IE_r",
                            1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 301:
            self.exp_name = "Jiansheng WEIE LR"
            self.base_folder = DataLoader.record_folder + r"\records\Jiansheng_2021-01-06\Run1"
            self.mapping = {10: "IE_l", 20: "IE_r", 30: "WE_l", 40: "WE_r", 100: "EMG_WE_l",
                            200: "EMG_WE_r", 300: "EMG_IE_l", 400: "EMG_IE_r",
                            1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 399:
            self.exp_name = "test6"
            self.base_folder = DataLoader.record_folder + r"\records\test6_2021-03-15\Run1"
            self.mapping = {10: "IE_l", 20: "IE_r", 30: "WE_l", 40: "WE_r", 100: "EMG_WE_l",
                            200: "EMG_WE_r", 300: "EMG_IE_l", 400: "EMG_IE_r",
                            1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 302:
            self.exp_name = "Nargess WEIE LR"
            self.base_folder = DataLoader.record_folder + r"\records\Nargess_2021-03-16\Run1"
            self.mapping = {10: "IE_l", 20: "IE_r", 30: "WE_l", 40: "WE_r", 100: "EMG_WE_l",
                            200: "EMG_WE_r", 300: "EMG_IE_l", 400: "EMG_IE_r",
                            1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 303:
            self.exp_name = "Francis WEIE LR"
            self.base_folder = DataLoader.record_folder + r"\records\Francis_2021-03-17\Run1"
            self.mapping = {10: "IE_l", 20: "IE_r", 30: "WE_l", 40: "WE_r", 100: "EMG_WE_l",
                            200: "EMG_WE_r", 300: "EMG_IE_l", 400: "EMG_IE_r",
                            1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 304:
            self.exp_name = "Ash WEIE LR"
            self.base_folder = DataLoader.record_folder + r"\records\Ash_real_2021-03-18\Run1"
            self.mapping = {10: "IE_l", 20: "IE_r", 30: "WE_l", 40: "WE_r", 100: "EMG_WE_l",
                            200: "EMG_WE_r", 300: "EMG_IE_l", 400: "EMG_IE_r",
                            1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 305:
            self.exp_name = "Tushar WEIE LR"
            self.base_folder = DataLoader.record_folder + r"\records\Tushar_2021-03-18\Run1"
            self.mapping = {10: "IE_l", 20: "IE_r", 30: "WE_l", 40: "WE_r", 100: "EMG_WE_l",
                            200: "EMG_WE_r", 300: "EMG_IE_l", 400: "EMG_IE_r",
                            1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 306:
            self.exp_name = "Stevie WEIE LR"
            self.base_folder = DataLoader.record_folder + r"\records\Stevie_new_2021-03-25\Run1"
            self.mapping = {10: "IE_l", 20: "IE_r", 30: "WE_l", 40: "WE_r", 100: "EMG_WE_l",
                            200: "EMG_WE_r", 300: "EMG_IE_l", 400: "EMG_IE_r",
                            1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
        elif self.exp_counter == 307:
            self.exp_name = "Aravind WEIE LR"
            self.base_folder = DataLoader.record_folder + r"\records\Aravind_2021-03-30\Run1"
            self.mapping = {10: "IE_l", 20: "IE_r", 30: "WE_l", 40: "WE_r", 100: "EMG_WE_l",
                            200: "EMG_WE_r", 300: "EMG_IE_l", 400: "EMG_IE_r",
                            1: "Idle", 2: 'focus', 3: 'prepare', 4: 'two', 5: 'one', 6: 'task'}
            
    def create_raw_object(self):
        # read raw data from csv file
        raw_eeg_path = self.base_folder + "//raw_eeg.csv"
        df = pd.read_csv(raw_eeg_path, header=None)
        self.raw_data = df.values
        # self.raw_emg = self.raw_data[:, 15]
        self.raw_eeg = self.raw_data[:, self.channel_ind]



        info = mne.create_info(sfreq = self.fs, ch_names = self.channel_names, ch_types=self.channel_type)
        info.set_montage('standard_1020')

        self.raw_array = mne.io.RawArray(np.transpose(self.raw_eeg/10**6), info)# convert uV to V


    def create_event(self):
        event_path = self.base_folder + "//event.csv"
        event_df = pd.read_csv(event_path, header=None)
        self.events = event_df.values
        self.origin_time = self.raw_data[0, 0]
        self.onsets = self.events[:, 1] - self.origin_time
        self.durations = np.zeros_like(self.onsets)
        self.event_array = np.column_stack(((self.onsets * self.fs).astype(int), np.zeros_like(self.onsets, dtype = int), self.events[:, 0].astype(int)))
        self.descriptions = [self.mapping[event_id] for event_id in self.event_array[:, 2]]
        self.annot_from_events = mne.Annotations(onset=self.onsets, duration=self.durations, description=self.descriptions)
        self.raw_array.set_annotations(self.annot_from_events)
        
    def remove_nan_from_array(self, array):
        return array[~np.isnan(array)]
    
    def add_EMG_event(self):
        file = r"{}\{}".format(self.base_folder, 'EMG_onsets.csv')
        dt = pd.read_csv(file, index_col=0, header=None)
        task_name_list = ['WE_l', 'WE_r', 'IE_l', 'IE_r']
        EMG_onsets_dict = dict.fromkeys(task_name_list)
        EMG_onsets_dict['WE_l'] = self.remove_nan_from_array(dt.values[0, :])
        EMG_onsets_dict['WE_r'] = self.remove_nan_from_array(dt.values[1, :])
        EMG_onsets_dict['IE_l'] = self.remove_nan_from_array(dt.values[2, :])
        EMG_onsets_dict['IE_r'] = self.remove_nan_from_array(dt.values[3, :])
        onsets_for_annotation = np.concatenate((self.raw_array.annotations.onset,
                                                EMG_onsets_dict['WE_l'],
                                                EMG_onsets_dict['WE_r'],
                                                EMG_onsets_dict['IE_l'],
                                                EMG_onsets_dict['IE_r']))
        durations_for_annotation = np.zeros_like(onsets_for_annotation)
        descriptions_for_annotation = np.concatenate((self.raw_array.annotations.description,
                                                      np.array(['EMG_WE_l'] * len(EMG_onsets_dict['WE_l'])),
                                                      np.array(['EMG_WE_r'] * len(EMG_onsets_dict['WE_r'])),
                                                      np.array(['EMG_IE_l'] * len(EMG_onsets_dict['IE_l'])),
                                                      np.array(['EMG_IE_r'] * len(EMG_onsets_dict['IE_r']))))
        annot_from_events = mne.Annotations(onset=onsets_for_annotation,
                                            duration=durations_for_annotation,
                                            description=descriptions_for_annotation)
        self.raw_array.set_annotations(annot_from_events)
    
    

