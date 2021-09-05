
from package.entity.edata.utils import Utils
import pdb
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
        # pdb.set_trace()
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
                # pdb.set_trace()
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


    def read_sub_channel_names(self):
        """
        Read channel names typed in Sub Channel Manager in Oscilloscope tab and apply filter or scaler later
        """
        str_sub_channel = self.ui.lineEdit_subchannel_names.text()
        sub_channel_names = str_sub_channel.split()
        return sub_channel_names