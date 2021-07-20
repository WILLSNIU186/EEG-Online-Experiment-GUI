
import sys
import time
import numpy as np
from pycnbi import logger

DEBUG_TRIGGER = False
class ScopeSwitch():
    def onClicked_button_scope_switch(self, pressed):

        if pressed:
            self.ui.statusBar.showMessage("show oscilloscope")
            self.win.show()
        else:
            self.ui.statusBar.showMessage("oscilloscope closed")
            self.win.hide()

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
            if len(self.ts_list) > 0:
                self.update_template_buffer()
                self.filter_signal()  # Filter acquired data
                self.update_ringbuffers()  # Update the plotting infor
                if (not self.stop_plot):
                    self.repaint()  # Call paint event
        except Exception as e:
            logger.exception('Exception. Dropping into a shell.')
            print(str(e))
        finally:
            pass

    def read_eeg(self):
        """
        Get real time data from LSL
        """
        try:
            # data, self.ts_list= self.sr.inlets[0].pull_chunk(max_samples=self.config['sf']) # [frames][channels]
            data, self.ts_list = self.sr.acquire("scope using", blocking=False)

            # print("TTTTTTTTTTTTTTTTTTTTT\ndata = ", data)
            # TODO: check and change to these two lines
            # self.sr.acquire(blocking=False, decim=DECIM)
            # data, self.ts_list = self.sr.get_window()

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
            self.eeg = np.reshape(data[:, self.sr.eeg_channels],
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