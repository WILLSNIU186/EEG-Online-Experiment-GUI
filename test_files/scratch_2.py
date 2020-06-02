
from package.entity.edata.utils import Utils
import pdb
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt, iirnotch, lfilter
import pandas as pd


def butter_lowpass(data, cutoff, fs, order=5):
    '''
    Returns low passed data between the frequency specified in the input.
    Args:
        data (numpy.ndarray): array of samples. samples * channels
        cutoff (float): cut off frequency(Hz)
        fs (float): sampling frequency(Hz)
        order(int): filter order
    Returns:
        (numpy.ndarray): filtered data

    '''
    data_out = []
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    for i in range(data.shape[1]):
        filtered_data = lfilter(b, a, data[:, i])
        data_out.append(filtered_data)
    data_out = np.asarray(data_out)
    data_out = np.transpose(data_out)
    return data_out


def butter_highpass(data, cutoff, fs, order=5):
    '''
    Returns high passed data between the frequency specified in the input.
    Args:
        data (numpy.ndarray): array of samples. samples * channels
        cutoff (float): cut off frequency(Hz)
        fs (float): sampling frequency(Hz)
        order(int): filter order
    Returns:
        (numpy.ndarray): filtered data

    '''
    data_out = []
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    for i in range(data.shape[1]):
        filtered_data = lfilter(b, a, data[:, i])
        data_out.append(filtered_data)
    data_out = np.asarray(data_out)
    data_out = np.transpose(data_out)
    return data_out

def butter_notch(data, low_cut, high_cut, fs, order=2):
    '''
    Returns bandstop passed data between the frequency specified in the input.
    Args:
        data (numpy.ndarray): array of samples. samples * channels
        low_cut (float): low cut off frequency(Hz)
        high_cut (float): high cut off frequency(Hz)
        fs (float): sampling frequency(Hz)
        order(int): filter order
    Returns:
        (numpy.ndarray): filtered data

    '''
    data_out = []
    nyq = 0.5 * fs
    low = low_cut / nyq
    high = high_cut / nyq
    b, a = butter(order, [low, high], btype='bandstop', analog=False)
    for i in range(data.shape[1]):
        filtered_data = lfilter(b, a, data[:, i])
        data_out.append(filtered_data)
    data_out = np.asarray(data_out)
    data_out = np.transpose(data_out)
    return data_out

def lap(data_pre_lap):
    lap_filter = [-1 / 8] * 8
    lap_filter.insert(0, 1)
    lap_filter = np.asarray(lap_filter)
    data_lap_filtered = np.matmul(data_pre_lap, np.transpose(lap_filter))
    return data_lap_filtered


def preprocess(dataIn, fs):
    '''
    Input: dataIn samples*channels
    '''
    # # low pass
    # low_passed_MRCP = butter_lowpass(dataIn, 3, fs, 5)
    # # high pass
    # high_passed_MRCP = butter_highpass(low_passed_MRCP, 0.05, fs, 5)

    data_chan_selected = dataIn[:, 0:9]

    data_CAR = data_chan_selected - np.transpose(
        np.tile(np.mean(data_chan_selected, 1), (9, 1)))  # common average reference

    plt.figure()
    for i in range(9):

        str_label = "{}".format(i)
        if i == 0:
            linewidth = 4
        else:
            linewidth = 1
        plt.plot(x, data_CAR[:, i], label=str_label, linewidth=linewidth)
    plt.title("CAR filtered data")
    plt.legend()

    data_centered = data_CAR - np.tile(np.mean(data_CAR, 0), (len(data_CAR), 1))  # centering

    plt.figure()
    for i in range(9):

        str_label = "{}".format(i)
        if i == 0:
            linewidth = 4
        else:
            linewidth = 1
        plt.plot(x, data_CAR[:, i], label=str_label, linewidth=linewidth)
    plt.title("centered data")
    plt.legend()


    dataOut = lap(data_centered)

    return dataOut


df = pd.read_csv("records\\Subject_Jiansheng_Niu_exp_1_20200318\\mrcp_template.csv", header = None)
mrcp_temp = df.values

pdb.set_trace()
x = np.linspace(-2, 4, 7200)
for i in range(mrcp_temp.shape[0]):
    plt.plot(x, mrcp_temp[i, :])
plt.plot(x, np.mean(mrcp_temp, 0), linewidth = 4)
plt.show()






second_mrcp = raw_mrcp[31:47, :]

x = np.linspace(-2, 4, 7201)
plt.figure()
for i in range(9):
    str_label = "{}".format(i)
    plt.plot(x, second_mrcp[i, :], label = str_label)
plt.title("input data 2nd")
plt.legend()



low_passed_MRCP = butter_lowpass(np.transpose(second_mrcp), 3, 1200, 5)
high_passed_MRCP = butter_highpass(np.transpose(low_passed_MRCP), 0.05, 1200, 5)

plt.figure()
for i in range(9):
    str_label = "{}".format(i)
    if i == 4:
        linewidth = 4
    else:
        linewidth = 1
    plt.plot(x, high_passed_MRCP[i, :], label = str_label, linewidth = linewidth)
plt.title("input bandpassed")
plt.legend()



data_out = preprocess(np.transpose(high_passed_MRCP), 1200)



plt.figure()
plt.plot(x, data_out, label = "python")

plt.title("mrcp template")
plt.legend()
plt.show()

pdb.set_trace()

