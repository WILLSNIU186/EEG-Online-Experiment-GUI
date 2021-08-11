from package.entity.edata.utils import Utils
import numpy as np
import pdb

class Filter:
    """
    Filter class defines butterworth filters for bandpass, lowpass, highpass, notch conditions. This is a causal
    filter designed for real-time filtering and delay removal.

    Attribute:
    b, a: filter numerator and denominator coefficients
    initial_conditional_list: n_chan * order, initial conditions for the filter delays

    Parameter
    ---------
    low_cut: float, low cutoff frequency
    hi_cut: float, high cutoff frequency
    order: int, filter order
    sf: int, sampling frequency
    n_chan: channel number of input data
    """

    def __init__(self, low_cut, hi_cut, order, sf, n_chan):
        self.low_cut = low_cut
        self.hi_cut = hi_cut
        self.order = int(order)
        self.sf = int(sf)
        self.n_chan = int(n_chan)
        self.b = np.zeros((self.order + 1,), dtype=float)
        self.a = np.zeros((self.order + 1,), dtype=float)
        self.initial_condition_list = np.zeros((self.n_chan, self.order), dtype=float)

    def build_butter_band_pass(self):
        '''
        construct filter based on cutoff frequency and filter order
        '''
        self.b, self.a = Utils.butter_bandpass(self.low_cut, self.hi_cut, self.sf, self.order)
        self.initial_condition_list = Utils.construct_initial_condition_list(self.b, self.a, self.n_chan)

    def build_butter_low_pass(self):
        '''
        construct filter based on cutoff frequency and filter order
        '''
        self.b, self.a = Utils.butter_lowpass(self.low_cut, self.sf, self.order)
        self.initial_condition_list = Utils.construct_initial_condition_list(self.b, self.a, self.n_chan)

    def build_butter_high_pass(self):
        '''
        construct filter based on cutoff frequency and filter order
        '''
        self.b, self.a = Utils.butter_highpass(self.hi_cut, self.sf, self.order)
        self.initial_condition_list = Utils.construct_initial_condition_list(self.b, self.a, self.n_chan)

    def build_butter_notch(self):
        '''
        construct filter based on cutoff frequency and filter order
        '''
        self.b, self.a = Utils.butter_notch(self.low_cut, self.hi_cut, self.sf, self.order)
        self.initial_condition_list = Utils.construct_initial_condition_list(self.b, self.a, self.n_chan)

    def apply_filter(self, data_in):
        '''
        apply linear filter using scipy lfilter with initial conditions to remove filter delay during real-time
        recording
        :param data_in: n_chan * n_sample, prefiltered data
        :return: data_out: n_chan * n_sample, filtered data
                 initial_condition_list: n_chan * order, delay values
        '''
        data_out, self.initial_condition_list = Utils.apply_filter(self.b, self.a, data_in, self.initial_condition_list)
        return data_out, self.initial_condition_list


# if __name__ == '__main__':
#     filter = Filter(low_cut=0.05, hi_cut=3, order=2, sf=500, n_chan=32)