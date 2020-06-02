import pdb
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt, iirnotch, lfilter, lfiltic, lfilter_zi
import pandas as pd
from multiprocessing import Process, Queue, JoinableQueue, Manager
import scipy.io
from package.entity.edata.utils import Utils
from package.entity.edata.variables import Variables
import threading

DataPath = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface" \
           "\StepGUI_Classifier_Online\data\Jiansheng_mrcp_temp_test1_0311_1\\run1\\"

RawData = scipy.io.loadmat(DataPath + "raw_data.mat")


df = pd.read_csv("records\\Subject_Jiansheng_mrcp_exp_4_20200318\\raw_eeg.csv", header = None)
raw_data = df.values
raw_data = raw_data[:, 2:]

tenth_sample = raw_data[154809:162009, :]


def write_template_buffer(template_buffer, eeg):
    template_buffer = np.roll(template_buffer, -120, 0)
    current_chunck = np.copy(eeg)

    template_buffer[-120:, :] = current_chunck
    return template_buffer


if __name__ == '__main__':
    SampleRate = 1200
    nChannels = 16
    ScaleINT2Volt = 2** -31
    TrialNum = 15
    BufferLength = 6
    #
    # raw_data = RawData['raw_data']
    # template_buffer = TemplateBuffer['TemplateBuffer']
    # trial_timer = TrialTimer['TrialTimer']
    x = np.linspace(-2, 4, 7200)
    y = np.linspace(0, BufferLength * SampleRate - 40 , 120).astype(int)
    template_buffer = np.zeros((6 * SampleRate, nChannels), dtype = float)

    # stop_sample = 319208
    # start_sample = stop_sample - BufferLength * SampleRate
    # new_data = np.copy(raw_data[:,  start_sample:stop_sample])
    # pdb.set_trace()
    new_data = tenth_sample
    new_data = new_data * 10**-9
    b_lp, a_lp = Utils.butter_lowpass(3, 1200, 2)
    b_hp, a_hp = Utils.butter_highpass(0.05, 1200, 2)
    initial_condition_list_lp = Utils.construct_initial_condition_list(b_lp, a_lp, nChannels)
    initial_condition_list_hp = Utils.construct_initial_condition_list(b_hp, a_hp, nChannels)
    for i in y:
        print(i)
        low_pass_data_in = np.transpose(new_data[i: i + 120, :])

        low_pass_data_out, initial_condition_list_lp = Utils.apply_filter(b_lp, a_lp, low_pass_data_in, initial_condition_list_lp)

        high_pass_data_in = low_pass_data_out

        high_pass_data_out, initial_condition_list_hp = Utils.apply_filter(b_hp, a_hp, high_pass_data_in, initial_condition_list_hp)

        template_buffer = write_template_buffer(template_buffer, np.transpose(high_pass_data_out))
        MRCP_temp = Utils.preprocess(template_buffer)
    plt.figure()
    plt.plot(x, MRCP_temp, 'b', label='calculated template')
    plt.show()