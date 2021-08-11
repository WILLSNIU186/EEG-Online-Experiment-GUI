from twisted.internet import task
from twisted.internet import reactor
from threading import Thread
from pycnbi.stream_receiver.stream_receiver import StreamReceiver
from package.entity.edata.variables import Variables
from package.entity.edata.utils import Utils
from package.entity.base.filter import Filter
import numpy as np
import pdb


class Buffer:
    '''
    Buffer is a base class, which creates a StreamReceiver object to read real-time data and return a certain length
    data window. A timer function controls the updating frequency. Once the timer starts, loop function
    will be called every 'window_stride' seconds.

    Attribute
    ---------
    timer: calls loop function every 'window_stride' seconds
    sr: object of StreamReceiver
    n_ch: number of channels
    n_eeg_ch: number of EEG channels
    n_sample: number of time samples
    window: n_ch * n_sample, time window


    Parameter
    ---------
    window_stride: (second) Time interval between two windows
    window_size: (second) length of time window
    buffer_size: (second) length of buffer in StreamReceiver
    filer: object of Filter class
    filter_type: 'bpf' ---- band pass filter
                 'lpf' ---- low pass filter
                 'hpf' ---- high pass filter
                 'bsf; ---- band stop filter (notch filter)

    '''
    def __init__(self, window_stride=0.1, window_size=1, buffer_size=10, filter=None, filter_type=None):
        self.timer = task.LoopingCall(self.loop)
        self.window_stride = window_stride
        self.window_size = window_size
        self.buffer_size = buffer_size
        self.sr = StreamReceiver(window_size=self.window_size,
                                 buffer_size=self.buffer_size,
                                 amp_serial=Variables.get_amp_serial(),
                                 amp_name=Variables.get_amp_name())
        self.ch_names = self.sr.ch_list
        self.ch_types = self.sr.channel_type
        self.n_ch = int(self.sr.get_num_channels())
        self.eeg_ch_idx = self.sr.get_eeg_channels()
        self.eeg_ch_names = self.sr.get_eeg_channel_names()

        self.n_eeg_ch = int(len(self.eeg_ch_idx))
        self.n_sample = int(self.window_size * self.sr.sample_rate)
        self.window = np.zeros((self.n_ch, self.n_sample))
        self.eeg_window = np.zeros((self.n_eeg_ch, self.n_sample))
        self.filter = filter
        if filter:
            if filter_type == 'bpf':
                self.filter.build_butter_band_pass()
            elif filter_type == 'lpf':
                self.filter.build_butter_low_pass()
            elif filter_type == 'hpf':
                self.filter.build_butter_high_pass()
            elif filter_type == 'bsf':
                self.filter.build_butter_notch()

        print('Buffer window', self.window.shape)

    def start_timer(self):
        '''
        start timer in a different thread and call loop() from now on every 'window_stride' seconds.
        '''
        self.timer.start(self.window_stride)
        t = Thread(target=reactor.run, args=(False,))
        t.start()

    def stop_timer(self):
        '''
        stop timer and stop calling loop()
        '''
        reactor.stop()
        self.timer.stop()


    def loop(self):
        '''
        Do processing when each loop() is called. This acts as a place holder function waiting for child classes to
        specify what should be done.
        '''
        pass



if __name__ == '__main__':
    buffer = Buffer()
    buffer.start_timer()
