# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 18:30:12 2020

@author: j33niu
"""
import  numpy as np
from scipy import signal
from tushar import RecordingFromHardWare

class GetMRCPTemplate():
    
    def __init__(self,dataIn ,fs):
        self.dataIn = dataIn
        self.fs = fs
        self.dataOut = []
        self.channel_list = []
    
    def lap (self, data_pre_lap):
        lap_filter = [-1/8]*8
        lap_filter.insert(0 , 1)
        lap_filter = np.asarray(lap_filter)
        data_lap_filtered = np.matmul(data_pre_lap , np.transpose(lap_filter))
        return data_lap_filtered
        
        
    def band_pass_butter (self,data_pre_filter, high_order = 4, low_order = 2, high_freq = 30, low_freq = 0.05,factor = 1):
        b, a = signal.butter(high_order, high_freq*2/self.fs, 'high')
        bb, aa = signal.butter(low_order, low_freq*2/self.fs, 'low')
        data_high_passed = signal.filtfilt(b, a, np.transpose(data_pre_filter))
        data_low_passed = signal.filtfilt(bb, aa, data_high_passed)
        
        newfs = self.fs / factor
        if newfs < low_freq * 2 * 1.2:
            print("risk of aliasing")
            print("New Nyquist reate: {} Hz".format(newfs/2))
            print("Anti-aliasing filter cutoff freq. : {} Hz".format(low_freq))
        data_filtered = np.transpose(data_low_passed[: , 0::factor])
        return data_filtered 
        
    def preprocess(self):
        data_chan_selected = self.dataIn[:,0:9]
        data_CAR = data_chan_selected - np.transpose(np.tile(np.mean(data_chan_selected,1),(9,1)))#common average reference
        data_centered = data_CAR -  np.tile(np.mean(data_CAR,0),(len(data_CAR),1))#centering
        data_filtered = self.band_pass_butter(data_centered, 4, 2, 30, 0.05,1)#BPF
        self.dataOut = self.lap(data_filtered)
        
        return self.dataOut
         
# =============================================================================
# a = RecordingFromHardWare()
# a.startRecording()
# print("space to stop")
# input( )
# 
# a.stopRecording()
# input()
# b = GetMRCPTemplate(a.new_data,512)
# MRCP = b.preprocess()        
# =============================================================================
        
    