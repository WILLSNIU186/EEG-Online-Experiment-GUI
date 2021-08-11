import sys
import time
from pycnbi import logger
from package.entity.edata.utils import Utils
from scipy.signal import lfilter
import numpy as np
DEBUG_TRIGGER = False
import pdb


class GUITimer():

    def update_loop(self):
        """
        Update three parts by real time data: template_buffer, filter displayed signal, ringbuffer.
        This function connects with main timer defined in MainView and is called every 20ms.
        """

        os_time = time.time()
        self.os_time_list1.append(os_time)
        #  Sharing variable to stop at the GUI level
        if not self.state.value:
            logger.info('Viewer stopped')
            sys.exit()

        try:
            self.read_eeg()  # Read new chunk
            self.ui.widget_mrcp_extractor.clear()
            # print('chunk ', self.eeg.shape)

            if len(self.ts_list) > 0:
                self.update_template_buffer()
                self.filter_signal()  # Filter acquired data
                self.update_ringbuffers()  # Update the plotting infor
                # self.MRCP_plot(self.read_template_buffer()[:, 12])
                # self.MRCP_plot(self.mrcp_buffer.window[20, :].T)

                if (not self.stop_plot):
                    self.repaint()  # Call paint event
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



    def read_eeg(self):
        """
        Get real time data from LSL
        """
        try:
            # data, self.ts_list= self.sr.inlets[0].pull_chunk(max_samples=self.config['sf']) # [frames][channels]
            data, self.ts_list = self.sr.acquire("scope using", blocking=False)

            # print("TTTTTTTTTTTTTTTTTTTTT\ndata = ", data)
            # TODO: check and change to these two lines
            # self.sr.acquire("scope using",blocking=False)
            # data, self.ts_list = self.sr.get_window()
            # print(data.shape)
            if len(self.ts_list) == 0:
                # self.eeg= None
                # self.tri= None
                return

            n = self.config['eeg_channels']
            # print('eeg channels: ', n)
            '''
            x= np.array( data )
            trg_ch= self.config['tri_channels']
            if trg_ch is not None:
                self.tri= np.reshape( x[:,trg_ch], (-1,1) ) # samples x 1
            self.eeg= np.reshape( x[:,self.sr.eeg_channels], (-1,n) ) # samples x channels
            '''
            trg_ch = self.config['tri_channels']
            if trg_ch is not None:
                self.tri = np.reshape(data[:, trg_ch], (-1, 1))  # samples x 1
            self.eeg = np.reshape(data[:, self.sr.get_channels()],
                                  (-1, n))  # samples x channels
            # print("TTTTTTTTTTTTTTTTTTTTT\ndata = ", self.eeg)
            if DEBUG_TRIGGER:
                # show trigger value
                try:
                    trg_value = max(self.tri)
                    if trg_value > 0:
                        logger.info('Received trigger %s' % trg_value)
                except:
                    logger.exception('Error! self.tri = %s' % self.tri)

                    # Read exg. self.config.samples*self.config.exg_ch, type float
                    # bexg = np.random.rand( 1, self.config['samples'] * self.config['exg_channels'] )
                    # self.exg = np.reshape(list(bexg), (self.config['samples'],self.config['exg_channels']))
        except WindowsError:
            # print('**** Access violation in read_eeg():\n%s\n%s'% (sys.exc_info()[0], sys.exc_info()[1]))
            pass
        except:
            logger.exception()
            # pdb.set_trace()



    def update_ringbuffers(self):
        """
        Update selected channels scale
        """
        # logger.info('called')
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
        self.data_plot_sub = self.data_plot[0:len(self.data_plot):self.subsampling_ratio]
        # pdb.set_trace()

        # print('data_plot ', self.data_plot.shape)
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
