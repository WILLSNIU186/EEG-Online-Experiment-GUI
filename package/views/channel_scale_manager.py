import numpy as np
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
        for x in range(0, len(self.channels_to_show_idx)):
            self.curve_eeg[x].setData(x=self.x_ticks,
                                      y=self.data_plot[:, self.channels_to_show_idx[x]] - x * self.scale)

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
        if (new_seconds != self.seconds_to_show) and (new_seconds > 0) and (
                new_seconds < 100):
            self.ui.spinBox_time.setValue(new_seconds)
            self.main_plot_handler.setRange(xRange=[0, new_seconds])
            self.x_ticks = np.zeros(self.config['sf'] * new_seconds);
            for x in range(0, self.config['sf'] * new_seconds):
                self.x_ticks[x] = (x * 1) / float(self.config['sf'])

            if (new_seconds > self.seconds_to_show):
                padded_signal = np.zeros((self.config['sf'] * new_seconds,
                                          self.config['eeg_channels']))
                padded_signal[padded_signal.shape[0] - self.data_plot.shape[0]:, :] = self.data_plot
                for x in range(0, len(self.events_detected), 2):
                    self.events_detected[x] += padded_signal.shape[0] - \
                                               self.data_plot.shape[0]
                self.data_plot = padded_signal

            else:
                for x in range(0, len(self.events_detected), 2):
                    self.events_detected[x] -= self.data_plot.shape[0] - \
                                               self.config['sf'] * new_seconds
                self.data_plot = self.data_plot[self.data_plot.shape[0] - self.config['sf'] * new_seconds:, :]

            self.seconds_to_show = new_seconds
            self.trigger_help()

            # We force an immediate repaint to avoid "shakiness".
            if (not self.stop_plot):
                self.force_repaint = 1
                self.repaint()

    def update_ringbuffers(self):
        """
        Update selected channels scale
        """
        # update single channel scale
        # print("single channel scale: ", self.single_channel_scale)
        channel_to_scale = self.channel_to_scale_column_index * 16 + self.channel_to_scale_row_index
        if self.ui.checkBox_change_scale.isChecked():
            self.ui.statusBar.showMessage("Use UP and Down keys in keyboard to control scale")
            self.channels_to_scale = []
            self.sub_channel_names = self.read_sub_channel_names()
            for sub_channel_name in self.sub_channel_names:
                channel_to_scale = self.channel_labels.tolist().index(sub_channel_name)
                self.channels_to_scale.append(channel_to_scale)
            self.eeg[:, self.channels_to_scale] = self.eeg[:, self.channels_to_scale] * self.single_channel_scale

        # We have to remove those indexes that reached time = 0

        self.data_plot = np.roll(self.data_plot, -len(self.ts_list), 0)
        self.data_plot[-len(self.ts_list):, :] = self.eeg

        delete_indices_e = []
        delete_indices_c = []
        for x in range(0, len(self.events_detected), 2):
            xh = int(x / 2)
            self.events_detected[x] -= len(self.ts_list)  # leeq
            if (self.events_detected[x] < 0) and (not self.stop_plot):
                delete_indices_e.append(x)
                delete_indices_e.append(x + 1)
                delete_indices_c.append(xh)
                self.events_curves[xh].clear()
                self.main_plot_handler.removeItem(self.events_text[xh])

        self.events_detected = [i for j, i in enumerate(self.events_detected) if
                                j not in delete_indices_e]
        self.events_curves = [i for j, i in enumerate(self.events_curves) if
                              j not in delete_indices_c]
        self.events_text = [i for j, i in enumerate(self.events_text) if
                            j not in delete_indices_c]

        # Find LPT events and add them
        if (self.show_LPT_events) and (not self.stop_plot):
            for x in range(len(self.tri)):
                tri = int(self.tri[x])
                if tri != 0 and (tri > self.last_tri):
                    self.addEventPlot("LPT", tri)
                    logger.info('Trigger %d received' % tri)
                self.last_tri = tri
