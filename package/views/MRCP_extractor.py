from pycnbi import logger
import numpy as np
from ..entity.edata.utils import Utils
from random import randrange
import pyqtgraph as pg

class MRCPExtractor():

    def onClicked_button_temp_view(self):
        """
        Event listener for View button in Online Experiment tab.
        View selected trials
        """
        try:
            self.get_input_temp()
            self.display_temp_list = self.input_temp_list
            self.ui.label_content_Disp_temp.setText("{}".format(self.display_temp_list))
            self.plot_display_temp()
        except Exception as e:
            logger.exception('Exception. Dropping into a shell.')
            print(str(e))
        finally:
            pass

    def onClicked_button_temp_remove(self):
        """
        Event listener for Remove button in Onlin Experiment tab.
        Remove selected trials
        """
        try:
            self.get_input_temp()
            for element in self.input_temp_list:
                del self.total_trials_MRCP[element - 1]
            # self.display_temp_list = [x for x in self.total_MRCP_inds if x not in self.input_temp_list]
            self.display_temp_list = list(range(1, len(self.total_trials_MRCP) + 1))
            self.ui.label_content_Disp_temp.setText("{}".format(self.display_temp_list))
            self.ui.label_content_available_temp.setText("{}".format(self.display_temp_list))
            self.plot_display_temp()
        except Exception as e:
            logger.exception('Exception. Dropping into a shell.')
            print(str(e))
        finally:
            pass

    def onClicked_button_temp_clear(self):
        """
        Event listener for Clear button in Online Experiment tab
        Clear MRCP plot
        """
        self.ui.graphicsView.clear()

    def onClicked_button_temp_mean(self):
        """
        Event listener for Mean button in Online Experiment tab
        Calculate mean of all templates
        """
        try:
            self.mean_MRCP = np.mean(self.total_trials_MRCP, 0)
            self.ui.graphicsView.clear()
            self.MRCP_plot(self.mean_MRCP)
        except Exception as e:
            logger.exception('Exception. Dropping into a shell.')
            print(str(e))
        finally:
            pass



    def update_template_buffer(self):
        """
        Update buffer for drawing online MRCP template. Low pass filter followed by high pass filter are
        applied to the buffer.
        """
        self.template_buffer = np.roll(self.template_buffer, -len(self.ts_list), 0)
        current_chunck = np.copy(self.eeg)

        low_pass_data_in = np.transpose(current_chunck)

        low_pass_data_out, self.initial_condition_list_lp = Utils.apply_filter(self.b_lp, self.a_lp, low_pass_data_in,
                                                                               self.initial_condition_list_lp)

        high_pass_data_in = low_pass_data_out

        high_pass_data_out, self.initial_condition_list_hp = Utils.apply_filter(self.b_hp, self.a_hp, high_pass_data_in,
                                                                                self.initial_condition_list_hp)

        # print('\nhigh pass data out size: ', high_pass_data_out.shape)
        self.template_buffer[-len(self.ts_list):, :] = np.transpose(high_pass_data_out)


    def read_template_buffer(self):
        """
        Get bandpassed real time template buffer
        """
        pre_data_in = np.copy(self.template_buffer[- 5 * int(self.sr.sample_rate):, :])
        pre_data_in = np.copy(pre_data_in)
        print('pre data in shape: ', pre_data_in.shape)
        return pre_data_in

    def set_MRCP_window_size(self, MRCP_window_size):
        """
        Set the time length of MRCP template displayed in Online Experiment tab
        """
        self.MRCP_window_size = MRCP_window_size


    def update_MRCP_plot(self):
        """
        Update the signal in MRCP template window
        """
        try:
            self.set_MRCP_window_size(5)
            self.raw_trial_MRCP = self.read_template_buffer()
            ch_list = self.channel_labels.tolist()
            lap_ch_list = [ch_list.index(self.ui.lineEdit_lap_central.text()),
                           ch_list.index(self.ui.lineEdit_lap_1.text()),
                           ch_list.index(self.ui.lineEdit_lap_2.text()),
                           ch_list.index(self.ui.lineEdit_lap_3.text()),
                           ch_list.index(self.ui.lineEdit_lap_4.text())]
            self.processed_trial_MRCP = Utils.preprocess(self.raw_trial_MRCP, lap_ch_list)
            # save each MRCP and raw signals into total MRCP list
            self.total_trials_MRCP.append(self.processed_trial_MRCP)
            self.total_trials_raw_MRCP.append(np.transpose(self.raw_trial_MRCP).flatten())

            self.line_width = 4
            self.MRCP_plot(self.processed_trial_MRCP)
            self.temp_counter += 1
            self.temp_counter_list.append(self.temp_counter)
            self.ui.label_content_current_temp.setText(str(self.temp_counter))
        except:
            logger.info('MRCP extractor went wrong')
            self.ui.statusBar.showMessage("are lap channels exist?")
        finally:
            pass


    def MRCP_plot(self, about_to_plot_MRCP):
        """
        Plot MRCP template
        :param about_to_plot_MRCP: template buffer extracted from real-time data stream
        :return:
        """
        size = len(about_to_plot_MRCP)
        x = [x / self.sr.sample_rate - 2 for x in list(range(0, size))]
        y = np.transpose(about_to_plot_MRCP)
        R = randrange(255)
        G = randrange(255)
        B = randrange(255)
        self.ui.graphicsView.plot(x, y, pen=pg.mkPen(color=(R, G, B), width=1))



    def plot_display_temp(self):
        """
        Plot certain MRCP templates selected by the text box below the MRCP plot window.
        """
        self.ui.graphicsView.clear()
        # print("display temp list", self.display_temp_list)
        for i in self.display_temp_list:
            self.MRCP_plot(self.total_trials_MRCP[int(i) - 1])


    def get_input_temp(self):
        """
        Choose tpyed templates from the text box below the MRCP plot window.
        """
        self.selected_temp = self.ui.lineEdit_temp_selector.text()
        self.list_selected_temp = self.selected_temp.split()
        # print("list_selected_temp", self.list_selected_temp)
        if len(self.list_selected_temp) == 1:
            self.input_temp_list = [int(x) for x in self.list_selected_temp]
            # self.ui.label_content_Disp_temp.setText("{}".format(self.input_temp_list[0]))

        elif len(self.list_selected_temp) > 1:
            if self.list_selected_temp[1] == "-":
                start_index = int(self.list_selected_temp[0])
                stop_index = int(self.list_selected_temp[-1]) + 1
                self.input_temp_list = list(range(start_index, stop_index))
            else:
                self.input_temp_list = [int(x) for x in self.list_selected_temp]
