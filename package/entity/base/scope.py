import numpy as np
from pycnbi import logger
import pyqtgraph as pg

import numpy as np
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore

NUM_X_CHANNELS = 16
class Scope(QMainWindow):
    '''
    Scope class create a virtual oscilloscope using pyqt.
    This could be instantiated every time you need an oscilloscope.
    Please refer to package/views/main_GUI/online_testing/online_test.py for usage example.

    Parameter
    ---------
    buffer: buffer object
    '''
    def __init__(self, buffer):
        super(Scope, self).__init__()
        self.buffer = buffer

        ################################################################################################################
        # Initialize scope window
        ################################################################################################################
        self.win = pg.GraphicsWindow()
        self.win.hide()
        self.main_plot_handler = self.win.addPlot()
        self.win.resize(1280, 800)

        self.seconds_to_show = buffer.window_size
        self.scale = 100

        self.channels_to_show_idx = list(range(0, buffer.n_ch))
        # Set range and ticks
        values = []
        for x in range(0, len(self.channels_to_show_idx)):
            values.append((-x * self.scale, buffer.ch_labels[self.channels_to_show_idx[x]]))
        values_axis = []
        values_axis.append(values)
        values_axis.append([])
        self.main_plot_handler.getAxis('left').setTicks(values_axis)
        self.main_plot_handler.setRange(xRange=[0, self.seconds_to_show],
                                        yRange=[+1.5 * self.scale,
                                                -0.5 * self.scale - self.scale * buffer.n_ch])
        self.main_plot_handler.disableAutoRange()
        self.main_plot_handler.showGrid(y=True)
        self.main_plot_handler.setLabel(axis='left',
                                        text='Scale (uV): ' + str(self.scale))
        self.main_plot_handler.setLabel(axis='bottom', text='Time (s)')

        self.x_ticks = np.zeros(buffer.sf * self.seconds_to_show)
        for x in range(0, buffer.sf * self.seconds_to_show):
            self.x_ticks[x] = (x * 1) / float(buffer.sf)

        # Plotting colors. If channels > 16, colors will roll back to the beginning
        self.colors = np.array(
            [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0],
             [0, 255, 255], [255, 0, 255], [128, 100, 100], [0, 128, 0],
             [0, 128, 128], [128, 128, 0], [255, 128, 128], [128, 0, 128],
             [128, 255, 0], [255, 128, 0], [0, 255, 128], [128, 0, 255]])
        self.curve_eeg = []
        for x in range(0, len(self.channels_to_show_idx)):
            self.curve_eeg.append(self.main_plot_handler.plot(x=self.x_ticks,
                                                              y=buffer.window[self.channels_to_show_idx[x],:].T * buffer.sr.multiplier,
                                                              pen=pg.mkColor(
                                                                  self.colors[
                                                                  self.channels_to_show_idx[x] % NUM_X_CHANNELS, :])))

        # Stop plot functionality
        self.stop_plot = 0

        # Force repaint even when we shouldn't repaint.
        self.force_repaint = 1
        self.init_timer()


    def init_timer(self):
        """
        Initialize main timer used for refreshing oscilloscope window. This refreshes every 20ms.
        """
        QtCore.QCoreApplication.processEvents()
        QtCore.QCoreApplication.flush()
        self.timer = QtCore.QTimer(self)
        self.timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer.timeout.connect(self.loop)

    def start_timer(self, cycle):
        '''
        :param cycle: update cycle milisecond
        '''
        self.timer.start(cycle)

    def show_win(self):
        self.win.show()


    def loop(self):
        try:
            if not self.stop_plot:
                for x in range(0, len(self.channels_to_show_idx)):
                    self.curve_eeg[x].setData(x=self.x_ticks,
                                              y=self.buffer.sr.multiplier * self.buffer.window[self.channels_to_show_idx[x], :].T - x * self.scale)

        except Exception as e:
                logger.exception('Exception. Dropping into a shell.')
                print(str(e))
        finally:
            pass
