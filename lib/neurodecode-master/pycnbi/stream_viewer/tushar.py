# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 18:59:39 2020

@author: j33niu
"""
import os
import sys
import time
import datetime
import numpy as np
import multiprocessing as mp
import pycnbi.utils.add_lsl_events
import pycnbi.utils.q_common as qc
import pycnbi.utils.pycnbi_utils as pu
from pycnbi.utils.convert2fif import pcl2fif
from pycnbi.utils.cnbi_lsl import start_server
from pycnbi.gui.streams import redirect_stdout_to_queue
from pycnbi.stream_receiver.stream_receiver import StreamReceiver
from pycnbi import logger
from builtins import input
import threading


class RecordingFromHardWare():
    
    def __init__(self):
        self.start_recording= False
        self.new_data = []
        self.sr = StreamReceiver(buffer_size=0)
        self.record_dir = '%s/records' % os.getcwd()
        self.current_window = np.ndarray([])
        self.current_time_stamps = np.ndarray([])
        self.MRCP_window_size = 6
        print("I RUMNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
        
# =============================================================================
#     def runInfinitecording(self):
#         while self.start_recording:
#                self.sr.acquire()
#                if self.sr.get_buflen() > 20:
#                    duration = str(datetime.timedelta(seconds=int(self.sr.get_buflen())))
#                    #recordLogger.info('RECORDING %s' % duration)
#                    #next_sec += 1
#                buffers, times = self.sr.get_buffer()
#                signals = buffers
#                events = None
#             
#                 # channels = total channels from amp, including trigger channel
#                data = {'signals':signals, 'timestamps':times, 'events':events,
#                         'sample_rate':self.sr.get_sample_rate(), 'channels':self.sr.get_num_channels(),
#                         'ch_names':self.sr.get_channel_names(), 'lsl_time_offset':self.sr.lsl_time_offset}
#                print(data)
#                self.new_data.append(data)
# =============================================================================
      
    def startRecording(self):
        # do some stuff
        self.start_recording= True
        #download_thread = threading.Thread(target=self.runInfinitecording)
        recordLogger=logger
        thread = threading.Thread(target=self.record)
        thread.start()  
     
    def stopRecording(self):
        self.start_recording= False
        #Write into file
        #self.new_data = []        
               
    def isRecordingIsRunning(self):
        return  self.start_recording
    
    def set_MRCP_window_size(self, MRCP_window_size):
        self.MRCP_window_size = MRCP_window_size
    
    def record( self ):
        recordLogger = logger
        #redirect_stdout_to_queue(recordLogger, 'INFO')
    
        # set data file name
        timestamp = time.strftime('%Y%m%d-%H%M%S', time.localtime())
        pcl_file = "%s/%s-raw.pcl" % (self.record_dir, timestamp)
        eve_file = '%s/%s-eve.txt' % (self.record_dir, timestamp)
        recordLogger.info('>> Output file: %s' % (pcl_file))
    
        # test writability
        try:
            qc.make_dirs(self.record_dir)
            open(pcl_file, 'w').write('The data will written when the recording is finished.')
        except:
            raise RuntimeError('Problem writing to %s. Check permission.' % pcl_file)
    
        # start a server for sending out data pcl_file when software trigger is used
        outlet = start_server('StreamRecorderInfo', channel_format='string',\
            source_id=eve_file, stype='Markers')
    
        # connect to EEG stream server
        #sr = StreamReceiver(buffer_size=0, eeg_only=eeg_only)
    
        # start recording
        recordLogger.info('\n>> Recording started (PID %d).' % os.getpid())
        qc.print_c('\n>> Press Enter to stop recording', 'G')
        tm = qc.Timer(autoreset=True)
        next_sec = 1
        while  self.start_recording:
            self.sr.acquire()
            if self.sr.get_buflen() > next_sec:
                duration = str(datetime.timedelta(seconds=int(self.sr.get_buflen())))
                #recordLogger.info('RECORDING %s' % duration)
                next_sec += 1
                
            #current_buffer, current_times = self.sr.get_buffer()
            self.sr.set_window_size(self.MRCP_window_size)
            self.current_window, self.current_time_stamps = self.sr.get_window()
            #print("window shape: {} time stamps shape: {}".format(self.current_window.shape, self.current_time_stamps.shape))
            tm.sleep_atleast(0.001)
    
        # record stop
        recordLogger.info('>> Stop requested. Copying buffer')
        buffers, times = self.sr.get_buffer()
        signals = buffers
        events = None
    
        # channels = total channels from amp, including trigger channel
        data = {'signals':signals, 'timestamps':times, 'events':events,
                'sample_rate':self.sr.get_sample_rate(), 'channels':self.sr.get_num_channels(),
                'ch_names':self.sr.get_channel_names(), 'lsl_time_offset':self.sr.lsl_time_offset}
        print("data length : {}".format(data['signals'].shape))
        self.new_data = data['signals']
        recordLogger.info('Saving raw data ...')
        qc.save_obj(pcl_file, data)
        recordLogger.info('Saved to %s\n' % pcl_file)
    
        # automatically convert to fif and use event file if it exists (software trigger)
        if os.path.exists(eve_file):
            recordLogger.info('Found matching event file, adding events.')
        else:
            eve_file = None
        recordLogger.info('Converting raw file into fif.')
        pcl2fif(pcl_file, external_event=eve_file)

# =============================================================================
# a = RecordingFromHardWare()
# a.startRecording()
# 
# input()
# a.set_MRCP_window_size(2)
# input()
# a.stopRecording()
# =============================================================================
        
               