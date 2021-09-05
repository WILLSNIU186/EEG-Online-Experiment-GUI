from package.entity.base.buffer import Buffer
import numpy as np
from pycnbi.stream_receiver.stream_receiver import StreamReceiver


class SSVEPBuffer(Buffer):
    def __init__(self, window_stride=0.1, window_size=1, buffer_size=10, filter=None, filter_type=None,
                 serial_number=None, amp_name=None):
        super().__init__(self)

        self.serial_number = serial_number
        self.amp_name = amp_name
        self.sr = StreamReceiver(window_size=self.window_size,
                                 buffer_size=self.buffer_size,
                                 amp_serial=self.serial_number,
                                 amp_name=self.amp_name)

        self.window_stride = window_stride
        self.window_size = window_size
        self.buffer_size = buffer_size
        if filter:
            self.filter = filter
            if filter_type == 'bpf':
                self.filter.build_butter_band_pass()
            elif filter_type == 'lpf':
                self.filter.build_butter_low_pass()
            elif filter_type == 'hpf':
                self.filter.build_butter_high_pass()
            elif filter_type == 'bsf':
                self.filter.build_butter_notch()

    # overriding method
    def loop(self):
        data, self.ts_list = self.sr.acquire("buffer using", blocking=True)
        self.window = np.roll(self.window, -len(self.ts_list), 1)

