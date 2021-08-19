from PyQt5 import QtCore
import numpy as np
import pyqtgraph as pg
from PyQt5.QtGui import QPainter
from pycnbi import logger
import pdb
from package.entity.edata.variables import Variables
from package.entity.edata.utils import Utils
import pylsl

class EventPlot():

    def keyPressEvent(self, event):
        """
        Event listeners for different key button pressed
        Example: When there is a channel name been typed in channel names box in Sub channel manager in
                 Oscilloscope, and change scale is checked, pressing up and down button will increase
                 and decrease that channels' scale respectively
        """
        key = event.key()
        # if (key == QtCore.Qt.Key_Escape):
        #     self.closeEvent(None)
        if (key == QtCore.Qt.Key_H):
            self.show_help = not self.show_help
            self.trigger_help()
        if (key == QtCore.Qt.Key_Up):
            # Python's log(x, 10) has a rounding bug. Use log10(x) instead.
            # new_scale = self.scale + max(1, 10 ** int(math.log10(self.scale)))
            # self.update_plot_scale(new_scale)
            self.single_channel_scale *= 2
        if (key == QtCore.Qt.Key_Space):
            self.stop_plot = not self.stop_plot
        if (key == QtCore.Qt.Key_Down):
            if self.single_channel_scale >= 0:
                self.single_channel_scale /= 2
            else:
                self.single_channel_scale = 1

        if (key == QtCore.Qt.Key_Left):
            self.update_plot_seconds(self.seconds_to_show - 1)
        if (key == QtCore.Qt.Key_Right):
            self.update_plot_seconds(self.seconds_to_show + 1)
        if (key == QtCore.Qt.Key_C):
            self.ui.checkBox_car.setChecked(not self.ui.checkBox_car.isChecked())
        if (key == QtCore.Qt.Key_B):
            self.ui.checkBox_bandpass.setChecked(
                not self.ui.checkBox_bandpass.isChecked())
            if self.ui.checkBox_bandpass.isChecked():
                self.ui.pushButton_bp.click()
        if ((key >= QtCore.Qt.Key_0) and (key <= QtCore.Qt.Key_9)):
            if (self.show_Key_events) and (not self.stop_plot):
                self.addEventPlot("KEY", 990 + key - QtCore.Qt.Key_0)

    def addEventPlot(self, event_name, event_id):
        """
        Add marker during recording. Note: marker not supported in current version
        """
        if (event_name == "TID"):
            color = pg.mkColor(0, 0, 255)
        elif (event_name == "KEY"):
            color = pg.mkColor(255, 0, 0)
        elif (event_name == "LPT"):
            color = pg.mkColor(0, 255, 0)
        elif (event_name == 'D'):
            color = pg.mkColor(255, 0, 0)
        else:
            color = pg.mkColor(255, 255, 255)

        self.events_detected.append(self.data_plot.shape[0] - 1)
        self.events_detected.append(event_id)
        self.events_curves.append(self.main_plot_handler.plot(pen=color,
                                                              x=np.array([self.x_ticks[-1], self.x_ticks[-1]]),
                                                              y=np.array(
                                                                  [+1.5 * self.scale,
                                                                   -1.5 * self.scale * self.config['eeg_channels']])))
        # text = pg.TextItem(event_name + "(" + str(self.events_detected[-1]) + ")", anchor=(1.1,0), fill=(0,0,0), color=color)
        text = pg.TextItem(str(self.events_detected[-1]), anchor=(1.1, 0),
                           fill=(0, 0, 0), color=color)
        text.setPos(self.x_ticks[-1], self.scale)
        self.events_text.append(text)
        self.main_plot_handler.addItem(self.events_text[-1])

    def add_stream_player_event(self):
        time_diff = pylsl.local_clock() - Variables.get_stream_player_starting_time()
        event_onset = self.raw.annotations.onset[self.event_counter]
        print(abs(time_diff - event_onset))
        _, self.event_counter = Utils.find_nearest(self.raw.annotations.onset, time_diff)

        if abs(time_diff - event_onset) < 0.03 and self.prev_event_counter != self.event_counter:
            self.addEventPlot(self.raw.annotations.description[self.event_counter], self.raw.annotations.description[self.event_counter])
            self.prev_event_counter = self.event_counter




    def paintEvent(self, e):
        """
        Paint the oscilloscope
        """
        # logger.info('paintEvent')
        # Distinguish between paint events from timer and event QT widget resizing, clicking etc (sender is None)
        # We should only paint when the timer triggered the event.
        # Just in case, there's a flag to force a repaint even when we shouldn't repaint
        sender = self.sender()
        # pdb.set_trace()
        if 'force_repaint' not in self.__dict__.keys():
            logger.warning('force_repaint is not set! Is it a Qt bug?')
            self.force_repaint = 0
        if (sender is None) and (not self.force_repaint):
            pass
        else:
            self.force_repaint = 0
            qp = QPainter()
            qp.begin(self)
            # Update the interface
            self.paintInterface(qp)
            qp.end()
