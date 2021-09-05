import numpy as np
from pycnbi import logger
import pdb

class ChannelScaleManager():
    def onActivated_combobox_scale(self):
        """
        Event listener for scale of data in Scale Manager of Oscilloscope tab
        """
        self.update_plot_scale(self.scales_range[self.ui.comboBox_scale.currentIndex()])

    def onValueChanged_spinbox_time(self):
        """
        Event listener for spinbox of time in Scale Manager of Oscilloscope tab
        """
        self.update_plot_seconds(self.ui.spinBox_time.value())

    def onValueChanged_downsample_ratio(self):
        self.update_plot_sampling_rate(self.ui.spinBox_downsample_ratio.value())

    def update_plot_scale(self, new_scale):
        """
        Update channel scales when changed
        :param: new_scale: new scale of data (mv)
        """
        if (new_scale < 1):
            new_scale = 1
        # commented out by dbdq.
        # else:
        #	new_scale = new_scale - new_scale%10

        self.scale = new_scale

        # Y Tick labels
        values = []
        for x in range(0, len(self.channels_to_show_idx)):
            values.append((-x * self.scale,
                           self.channel_labels[self.channels_to_show_idx[x]]))

        values_axis = []
        values_axis.append(values)
        values_axis.append([])
        # print("value: ", values)
        # print("value axis ", values_axis)

        self.main_plot_handler.getAxis('left').setTicks(values_axis)

        self.main_plot_handler.setRange(
            yRange=[+self.scale, -self.scale * len(self.channels_to_show_idx)])

        # print(self.scale)
        # print(-self.scale * len(self.channels_to_show_idx))

        self.main_plot_handler.setLabel(axis='left',
                                        text='Scale (uV): ' + str(self.scale))
        self.trigger_help()

        # We force an immediate repaint to avoid "shakiness".
        if (not self.stop_plot):
            self.force_repaint = 1
            self.repaint()

    def paintInterface(self, qp):
        """
        Update stuff on the interface. Only graphical updates should be added here
        """

        # logger.info('paintinterface')
        for x in range(0, len(self.channels_to_show_idx)):

            self.curve_eeg[x].setData(x=self.x_ticks_sub,
                                      y=self.data_plot_sub[:, self.channels_to_show_idx[x]] - x * self.scale)
        # pdb.set_trace()
            # self.curve_eeg[-1].setDownsampling(ds=self.subsampling_value,
            #                                    auto=False, method="mean")
        # (self.data_plot_sub[:, self.channels_to_show_idx[x]] - x * self.scale).shape
        # Update events
        for x in range(0, len(self.events_detected), 2):
            xh = int(x / 2)
            self.events_curves[xh].setData(x=np.array(
                [self.x_ticks[self.events_detected[x]],
                 self.x_ticks[self.events_detected[x]]]), y=np.array(
                [+1.5 * self.scale,
                 -0.5 * self.scale - self.scale * self.config[
                     'eeg_channels']]))
            self.events_text[xh].setPos(self.x_ticks[self.events_detected[x]],
                                        self.scale)

    def update_plot_seconds(self, new_seconds):
        """
        Update the time length displayed in oscilloscope
        :param new_seconds: time length to display (s)
        """
        # logger.info('called')
        if (new_seconds != self.seconds_to_show) and (new_seconds > 0) and (
                new_seconds < 100):
            self.ui.spinBox_time.setValue(new_seconds)
            self.main_plot_handler.setRange(xRange=[0, new_seconds])
            self.x_ticks = np.zeros(self.config['sf'] * new_seconds);
            for x in range(0, self.config['sf'] * new_seconds):
                self.x_ticks[x] = (x * 1) / float(self.config['sf'])

            self.x_ticks_sub = np.zeros(self.subsampling_freq * new_seconds)
            for i, x in enumerate(np.arange(0, self.config['sf'] * new_seconds, self.subsampling_ratio)):
                self.x_ticks_sub[i] = (x * 1) / float(self.config['sf'])




            if (new_seconds > self.seconds_to_show):
                padded_signal = np.zeros((self.config['sf'] * new_seconds,
                                          self.config['eeg_channels']))
                padded_signal[padded_signal.shape[0] - self.data_plot.shape[0]:, :] = self.data_plot
                for x in range(0, len(self.events_detected), 2):
                    self.events_detected[x] += padded_signal.shape[0] - \
                                               self.data_plot.shape[0]
                self.data_plot = padded_signal
                self.data_plot_sub = self.data_plot[0 : len(self.data_plot) : self.subsampling_ratio]
            else:
                for x in range(0, len(self.events_detected), 2):
                    self.events_detected[x] -= self.data_plot.shape[0] - \
                                               self.config['sf'] * new_seconds
                self.data_plot = self.data_plot[self.data_plot.shape[0] - self.config['sf'] * new_seconds:, :]
                self.data_plot_sub = self.data_plot[0 : len(self.data_plot) : self.subsampling_ratio]
            self.seconds_to_show = new_seconds
            self.trigger_help()

            # We force an immediate repaint to avoid "shakiness".
            if (not self.stop_plot):
                self.force_repaint = 1
                self.repaint()

    def update_plot_sampling_rate(self, new_downsample_rate):
        """
        Update the downsampling rate for oscilloscope plotting
        :param new_downsample_rate: downsampling rate for oscilloscope
        """
        if self.subsampling_ratio != new_downsample_rate and new_downsample_rate > 0 \
                and new_downsample_rate < 100 and isinstance(new_downsample_rate, int) \
                and self.config['sf'] % new_downsample_rate == 0:

            self.subsampling_ratio = new_downsample_rate

            self.subsampling_freq = int(self.config['sf'] / self.subsampling_ratio)
            self.data_plot_sub = np.zeros((self.subsampling_freq * self.seconds_to_show, self.config['eeg_channels']))
            # pdb.set_trace()
            self.x_ticks_sub = np.zeros(self.subsampling_freq * self.seconds_to_show)
            for i, x in enumerate(np.arange(0, self.config['sf'] * self.seconds_to_show, self.subsampling_ratio)):
                self.x_ticks_sub[i] = (x * 1) / float(self.config['sf'])
        # logger.info('new sampling rate'+str(self.subsampling_freq))