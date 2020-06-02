import pdb
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt, iirnotch, lfilter
from scipy.fftpack import fft
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
        filtered_data = filtfilt(b, a, data[:, i])
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



def apply_notch_filter(data, fs, power_freq = 60):
    Q = 30.0  # Quality factor
    w0 = power_freq / (fs / 2)  # Normalized Frequency
    b, a = iirnotch(w0, Q)
    data_out = filtfilt(b, a, data)
    return data_out


raw_data = scipy.io.loadmat('D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\StepGUI_Classifier_Online\\temp_test_data\\raw_data.mat')
raw_data_first_temp = scipy.io.loadmat('D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\StepGUI_Classifier_Online\\temp_test_data\\raw_data_first_temp.mat')
data_in_first_temp = scipy.io.loadmat('D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\StepGUI_Classifier_Online\\temp_test_data\\data_in_first_temp.mat')
MRCP_temp_first = scipy.io.loadmat('D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\StepGUI_Classifier_Online\\temp_test_data\\MRCP_temp_first.mat')
MRCP_temps = scipy.io.loadmat('D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\StepGUI_Classifier_Online\\data\\\Jiansheng_mrcp_temp_test1_0311_1\\run1\TemplateBuffer.mat')


raw_data = raw_data['new_data']
raw_data_second_temp = raw_data[:, 9014:13814]
MRCP_temps = MRCP_temps['TemplateBuffer']
MRCP_temp_second = MRCP_temps[0,:]

raw_data_first_temp = raw_data_first_temp['raw_data_first_temp']
data_in_first_temp = data_in_first_temp['data_in_first_temp']
MRCP_temp_first = MRCP_temp_first['MRCP_temp_first']

x = np.linspace(-2.5, 1.5, 4800)
plt.figure()
for i in range(9):

    str_label = "{}".format(i)
    if i == 0:
        linewidth = 4
    else:
        linewidth = 1
    plt.plot(x, raw_data_second_temp[i, :], label = str_label, linewidth = linewidth)
plt.title("input data")
plt.legend()

low_passed_MRCP = butter_lowpass(np.transpose(raw_data_second_temp), 3, 1200, 5)
# high pass
high_passed_MRCP = butter_highpass(np.transpose(low_passed_MRCP), 0.05, 1200, 5)

plt.figure()
for i in range(9):
    str_label = "{}".format(i)
    if i == 0:
        linewidth = 4
    else:
        linewidth = 1
    plt.plot(x, high_passed_MRCP[i, :], label = str_label, linewidth = linewidth)
plt.title("input data bandpassed")
plt.legend()

data_out = preprocess(np.transpose(high_passed_MRCP), 1200)


plt.figure()
plt.plot(x, data_out, label = "python")
plt.plot(x, np.transpose(MRCP_temp_second), label = "matlab")
plt.plot(x, np.transpose(MRCP_temp_first), label = "matlab_new")
plt.title("mrcp template matlab")
plt.legend()
plt.show()





plt.figure()
for i in range(13):
    str_label = "{}".format(i)
    plt.plot(x, TempDataIn_array[i, :], label = str_label)
plt.plot(x, TempDataIn_array[0, :])
plt.title("input data matlab 1st")
plt.legend()


first_mrcp_dada_in = TempDataIn_array[0:13, :]
first_mrcp_temp = TempBuffer_array[0, :]

data_out = preprocess(np.transpose(first_mrcp_dada_in), 1200)

plt.figure()
plt.plot(x, data_out)
plt.title("python dataout")
plt.show()



# plt.figure()
# for i in range(13,26,1):
#     plt.plot(x, TempDataIn_array[i, :])
# # plt.plot(x, TempDataIn_array[13, :])
# plt.title("input data matlab 2nd")






df = pd.read_csv("records\Subject_jiansheng_mrcp_temp_test1\\raw_mrcp.csv")
data_in = df.values
pdb.set_trace()



#low pass
low_passed_MRCP = butter_lowpass(data_pre, 3, 1200, 5)
#high pass
high_passed_MRCP = butter_highpass(low_passed_MRCP, 0.05, 1200, 5)
# bandstop
bandstoped_MRCP = butter_notch(high_passed_MRCP, 55, 65, 1200, 2)
processed_trial_MRCP = preprocess(bandstoped_MRCP, 1200)

x1 = np.linspace(-2, 4, 7201)
plt.figure()
plt.plot(x1, data_pre[:, 4], label = "original")
plt.plot(x1, low_passed_MRCP[:, 4], label = "low passed")
plt.plot(x1, high_passed_MRCP[:, 4], label = "high passed")
plt.plot(x1, bandstoped_MRCP[:, 4], label = "bandstop passed")
plt.plot(x1, processed_trial_MRCP, label = "MRCP template")
plt.title("mrcp template python")
plt.legend()
plt.show()








plt.figure()
x1 = np.linspace(50, 56, 7200)
for i in range(data_pre.shape[0]):
    plt.plot(x1, data_pre[i,:])
plt.title("input data python")

#test low pass multi channel
data_low_passed = butter_lowpass(np.transpose(data_pre), 120, 1200, 5)
pdb.set_trace()
plt.figure()
x1 = np.linspace(50, 56, 7200)
data_toplot = np.transpose(data_low_passed)
for i in range(data_toplot.shape[0]):
    plt.plot(x1, data_toplot[i,:])
plt.title("input data low passed python")
plt.show()

# Number of sample points
N = 7200
# sample spacing
T = 1.0 / 1200.0
x = np.linspace(0.0, N*T, N)
y = np.transpose(data_pre[0, :])
yf = fft(y)
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
plt.figure()
plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
plt.title("fft of data pre")


y_notch = apply_notch_filter(y, 1200, 60)
yf_notch = fft(y_notch)
plt.figure()
plt.plot(xf, 2.0/N * np.abs(yf_notch[0:N//2]))
plt.title("fft of data pre notch filterd")


#low pass filter
plt.figure()
plt.plot(x, data_pre[0, :], label="original data")
data_low_passed = butter_lowpass(np.transpose(data_pre[0, :]), 120, 1200, 5)
plt.plot(x, data_low_passed, label="low passed data")
data_high_passed = butter_highpass(data_low_passed, 3, 1200, 5)
plt.plot(x, data_high_passed, label="high passed data")
data_notched = butter_notch(data_high_passed, 55, 65, 1200, 2)
plt.plot(x, data_notched, label="notch passed data")
plt.legend()
plt.title("filtering")









data_pre_notch_filtered = apply_notch_filter(data_pre, 1200, 60)

plt.figure()
x1 = np.linspace(50, 56, 7200)
for i in range(data_pre_notch_filtered.shape[0]):
    plt.plot(x1, data_pre_notch_filtered[i,:])
plt.title("input data notch filtered python")



dataout = preprocess(data_pre, 1200)

plt.figure()
plt.plot(x1, dataout)
plt.title("mrcp template python")







plt.show()



# pdb.set_trace()
