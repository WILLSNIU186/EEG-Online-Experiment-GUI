from scipy.signal import lfilter
import numpy as np
from package.entity.edata.utils import Utils

class ChannelFilter():
    def onActivated_checkbox_car(self):
        """
        Event listener for check box in front of CAR filter in Oscilloscope tab.
        Apply Common Average Reference filter to displayed data if checked.
        """
        self.apply_car = self.ui.checkBox_car.isChecked()
        self.update_title_scope()

    def onActivated_checkbox_bandpass(self):
        """
        Event listener for check box in front of Bandpass filter in Oscilloscope tab.
        Check to bandpass filter displayed signal.
        """
        self.apply_bandpass = False
        self.ui.pushButton_bp.setEnabled(self.ui.checkBox_bandpass.isChecked())
        self.ui.doubleSpinBox_hp.setEnabled(self.ui.checkBox_bandpass.isChecked())
        self.ui.doubleSpinBox_lp.setEnabled(self.ui.checkBox_bandpass.isChecked())
        self.update_title_scope()

    def onActivated_checkbox_notch(self):
        """
        Event listener for check box in front of notch filter in Oscilloscope tab.
        Check to notch filter displayed signal.
        """
        self.apply_notch = False
        self.ui.pushButton_apply_notch.setEnabled(self.ui.checkBox_notch.isChecked())
        self.ui.doubleSpinBox_lc_notch.setEnabled(self.ui.checkBox_notch.isChecked())
        self.ui.doubleSpinBox_hc_notch.setEnabled(self.ui.checkBox_notch.isChecked())

    def onClicked_button_bp(self):
        """
        Event listener for Apply BP button in Filter Manager in Oscilloscope tab
        Apply BPF to displaying data
        """
        if self.ui.checkBox_change_filter.isChecked():
            if (self.ui.doubleSpinBox_lp.value() > self.ui.doubleSpinBox_hp.value()):
                self.apply_bandpass = True
                self.b_bandpass_scope_refilter, self.a_bandpass_scope_refilter, self.zi_bandpass_scope_refilter = \
                    Utils.butter_bandpass_scope(
                    self.ui.doubleSpinBox_hp.value(),
                    self.ui.doubleSpinBox_lp.value(),
                    self.config['sf'],
                    self.config['eeg_channels'])
        else:
            if (self.ui.doubleSpinBox_lp.value() > self.ui.doubleSpinBox_hp.value()):
                self.apply_bandpass = True
                self.b_bandpass_scope, self.a_bandpass_scope, self.zi_bandpass_scope = Utils.butter_bandpass_scope(
                    self.ui.doubleSpinBox_hp.value(),
                    self.ui.doubleSpinBox_lp.value(),
                    self.config['sf'],
                    self.config['eeg_channels'])
            self.update_title_scope()

    def onClicked_button_notch(self):
        """
        Event listener for Apply Notch in Filter Manager in Oscilloscope tab
        Apply notch filter to displaying data
        """
        if self.ui.checkBox_change_filter.isChecked():
            if (self.ui.doubleSpinBox_hc_notch.value() > self.ui.doubleSpinBox_lc_notch.value()):
                self.apply_notch = True
                self.b_notch_scope_refilter, self.a_notch_scope_refilter, self.zi_notch_scope_refilter = \
                    Utils.butter_notch_scope(
                    self.ui.doubleSpinBox_hc_notch.value(),
                    self.ui.doubleSpinBox_lc_notch.value(),
                    self.config['sf'],
                    self.config['eeg_channels'])
        else:
            if (self.ui.doubleSpinBox_hc_notch.value() > self.ui.doubleSpinBox_lc_notch.value()):
                self.apply_notch = True
                self.b_notch_scope, self.a_notch_scope, self.zi_notch_scope = Utils.butter_notch_scope(
                    self.ui.doubleSpinBox_hc_notch.value(),
                    self.ui.doubleSpinBox_lc_notch.value(),
                    self.config['sf'],
                    self.config['eeg_channels'])


    def update_title_scope(self):
        """
        Updates the title shown in the scope
        """
        if (hasattr(self, 'main_plot_handler')):
            self.main_plot_handler.setTitle(
                title='TLK: ' + self.bool_parser[self.show_TID_events] +
                      self.bool_parser[self.show_LPT_events] + self.bool_parser[
                          self.show_Key_events] + ', CAR: ' + self.bool_parser[
                          self.apply_car] + ', BP: ' + self.bool_parser[
                          self.apply_bandpass] + ' [' + str(
                    self.ui.doubleSpinBox_hp.value()) + '-' + str(
                    self.ui.doubleSpinBox_lp.value()) + '] Hz')


    def filter_signal(self):
        """
        Apply BPF and notch filters to displayed signal
        """

        self.channels_to_filter = list(range(len(self.channel_labels)))

        if self.ui.checkBox_change_filter.isChecked():
            self.channels_to_refilter = []
            self.sub_channel_names = self.read_sub_channel_names()
            for sub_channel_name in self.sub_channel_names:
                channel_to_refilter = self.channel_labels.tolist().index(sub_channel_name)
                self.channels_to_refilter.append(channel_to_refilter)
                self.channels_to_filter.remove(channel_to_refilter)

            if (self.apply_bandpass):
                for x in self.channels_to_refilter:
                    self.eeg[:, x], self.zi_bandpass_scope_refilter[:, x] = lfilter(self.b_bandpass_scope_refilter,
                                                                                    self.a_bandpass_scope_refilter,
                                                                                    self.eeg[:, x], -1,
                                                                                    self.zi_bandpass_scope_refilter[:,
                                                                                    x])

            if (self.apply_notch):
                for x in self.channels_to_refilter:
                    self.eeg[:, x], self.zi_notch_scope_refilter[:, x] = lfilter(self.b_notch_scope_refilter,
                                                                                 self.a_notch_scope_refilter,
                                                                                 self.eeg[:, x], -1,
                                                                                 self.zi_notch_scope_refilter[:, x])

        if (self.apply_bandpass):
            for x in self.channels_to_filter:
                self.eeg[:, x], self.zi_bandpass_scope[:, x] = lfilter(self.b_bandpass_scope, self.a_bandpass_scope,
                                                                       self.eeg[:, x], -1, self.zi_bandpass_scope[:, x])

        if (self.apply_notch):
            for x in self.channels_to_filter:
                self.eeg[:, x], self.zi_notch_scope[:, x] = lfilter(self.b_notch_scope, self.a_notch_scope,
                                                                    self.eeg[:, x], -1, self.zi_notch_scope[:, x])

        # We only apply CAR if selected AND there are at least 2 channels. Otherwise it makes no sense
        if (self.apply_car) and (len(self.channels_to_show_idx) > 1):
            self.eeg = np.dot(self.matrix_car, np.transpose(self.eeg))
            self.eeg = np.transpose(self.eeg)


    def read_sub_channel_names(self):
        """
        Read channel names typed in Sub Channel Manager in Oscilloscope tab and apply filter or scaler later
        """
        str_sub_channel = self.ui.lineEdit_subchannel_names.text()
        sub_channel_names = str_sub_channel.split()
        return sub_channel_names