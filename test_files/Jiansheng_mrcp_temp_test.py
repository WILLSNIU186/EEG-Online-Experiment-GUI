import pdb
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt, iirnotch, lfilter, lfiltic
import pandas as pd
from multiprocessing import Process, Queue, JoinableQueue, Manager
import scipy.io
from package.entity.edata.utils import Utils
from package.entity.edata.variables import Variables
import threading

DataPath = "D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface" \
           "\StepGUI_Classifier_Online\data\Jiansheng_mrcp_temp_test1_0311_1\\run1\\"

RawData = scipy.io.loadmat(DataPath + "raw_data.mat")
# TemplateBuffer = scipy.io.loadmat(DataPath + "TemplateBuffer.mat")
# TrialTimer = scipy.io.loadmat(DataPath + "TrialTimer.mat")

def write_template_buffer(template_buffer, eeg):
    template_buffer = np.roll(template_buffer, -120, 0)
    current_chunck = np.copy(eeg)

    template_buffer[-120:, :] = current_chunck
    return template_buffer


def read_template_buffer(template_buffer):
    pre_data_in = np.copy(template_buffer[- 4 * SampleRate:, :])
    pre_data_in = np.copy(pre_data_in[:, 0:9])

    return pre_data_in


#
# df = pd.read_csv("records/Subject_Pilot_mrcp_temp_test2_20200316\\raw_eeg.csv")
# # df = pd.read_csv("records/Subject_Pilot_mrcp_temp_test2_20200316\\raw_mrcp.csv")
# header = df.columns.values.astype(float)
# header = np.reshape(header, (len(header), 1))
# raw_data = np.r_[np.transpose(header), df.values]
# raw_data = df.values
#
# raw_data = raw_data[:, 2:]
# # raw_data = np.transpose(raw_data)
# print(raw_data.shape)

if __name__ == '__main__':
    SampleRate = 1200
    nChannels = 13
    ScaleINT2Volt = 2** -31
    TrialNum = 15
    BufferLength = 4
    #
    raw_data = RawData['raw_data']
    # template_buffer = TemplateBuffer['TemplateBuffer']
    # trial_timer = TrialTimer['TrialTimer']
    x = np.linspace(-2.5, 1.5, 4800)

    y = np.linspace(0, BufferLength * SampleRate - 40 , 120).astype(int)
    template_buffer = np.zeros((4 * SampleRate, 13), dtype = float)

    stop_sample = 319208
    start_sample = stop_sample - BufferLength * SampleRate
    new_data = np.copy(raw_data[:,  start_sample:stop_sample])
    # pdb.set_trace()
    new_data = np.transpose(new_data)
    new_data = new_data * 10**-9
    b_lp, a_lp = Utils.butter_lowpass(3, 1200, 2)
    initial_data = new_data[0:120, :]
    # initial_condition = lfiltic(b_lp, a_lp, initial_data)
    initial_condition = None
    pdb.set_trace()

    for i in y:
        print(i)
        # data = Array('d', new_data[i: i + 120, :])

        # #process try
        # manager = Manager()
        # shared_list = manager.list(new_data[i: i + 120, :])
        # # pdb.set_trace()
        # p1 = Process(target=Utils.butter_lowpass, args=(shared_list,))
        # p1.start()
        # p1.join()
        # # pdb.set_trace()
        #
        #
        # p2 = Process(target=Utils.butter_highpass, args=(shared_list,))
        # p2.start()
        # p2.join()
        # # pdb.set_trace()
        # # pdb.set_trace()

        #thread try
        # Variables.set_low_pass_data_in(data_in_low_pass)
        # t1 =threading.Thread(target=Utils.butter_lowpass)
        # # t1.daemon = True
        # t1.start()
        # t1.join()
        # low_pass_data_out = Variables.get_low_pass_data_out()
        # Variables.set_high_pass_data_in(low_pass_data_out)
        # t2 = threading.Thread(target=Utils.butter_highpass)
        # # p2.daemon = True
        # t2.start()
        # t2.join()
        # high_pass_data_out = Variables.get_high_pass_data_out()
        #thread try end

        # pdb.set_trace()

        low_pass_data_in = new_data[i: i+120, :]
        data_out , initial_condition = lfilter(b_lp, a_lp, low_pass_data_in, axis = -1, zi = initial_condition)
        pdb.set_trace()
        high_passed_data = Utils.butter_highpass(data= new_data[i: i + 120, :])
        print('high passed data shape: ', high_passed_data.shape)
        # pdb.set_trace()
        # high_pass_data_out =  np.asarray(shared_list)
        template_buffer = write_template_buffer(template_buffer, high_passed_data)
        MRCP_temp = Utils.preprocess(template_buffer, SampleRate)
        plt.figure()
        plt.plot(x, MRCP_temp, 'b', label = 'calculated template')
        plt.show()
    # for i in range(20):
    #     BufferLength = BufferLength + 4
    #     # stop_sample = int(SampleRate * (trial_timer[TrialNum, 3] - 2.5))
    #     stop_sample = 319208
    #     start_sample = stop_sample - BufferLength * SampleRate
    #
    #     new_data = np.copy(raw_data[:, start_sample:stop_sample])
    #     # pdb.set_trace()
    #     # new_data = new_data.astype(float) * ScaleINT2Volt
    #     # for c in range(13):
    #     #     #     plt.plot(x, new_data[c,:])
    #     #     # pdb.set_trace()
    #     new_data = np.transpose(new_data)
    #
    #     low_passed_data = Utils.butter_lowpass(new_data, 3, SampleRate, 2)
    #     high_passed_data = Utils.butter_highpass(low_passed_data, 0.05, SampleRate, 2)
    #
    #     # for c in range(9):
    #     #     label = '{}'.format(c)
    #     #     plt.plot(x, high_passed_data[:, c], label = label)
    #     # plt.legend()
    #     # plt.show()
    #     # pdb.set_trace()
    #     pre_data_in = np.copy(high_passed_data[-4800:,:])
    #     print('pre data in shape: ', pre_data_in.shape)
    #     MRCP_temp = Utils.preprocess(pre_data_in, SampleRate)
    #     print('MRCP temp shape', MRCP_temp.shape)
    #
    #     plt.figure()
    #     # plt.plot(x, template_buffer[TrialNum, :], 'r', label='Template')
    #     plt.plot(x, MRCP_temp, 'b', label = 'calculated template')
    #     plt.legend()
    plt.show()

