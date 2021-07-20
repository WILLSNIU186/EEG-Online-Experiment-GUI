import os
import time
from threading import Thread
from pycnbi import logger
from twisted.internet import reactor

from ..entity.edata.utils import Utils
from ..entity.edata.variables import Variables

class RecordSwitch():

    def onClicked_button_rec(self, pressed):
        """
        Start the recording when recording button been clicked
        """
        if pressed:
            print(1)
            self.ui.statusBar.showMessage("Recording started")
            logger.info("rec clicked")
            Variables.add_run_counter()

            path = "{}\Run{}".format(Variables.get_base_folder_path(), Variables.get_run_counter())
            Variables.set_sub_folder_path(path)
            try:
                os.makedirs(Variables.get_sub_folder_path())
            except OSError:
                print("Creation of the directory %s failed" % Variables.get_sub_folder_path())

            eeg_file = "%s\\raw_eeg.csv" % (Variables.get_sub_folder_path())
            Variables.set_raw_eeg_file_path(eeg_file)
            eeg_timestamp_file = "%s/raw_eeg_timestamp.csv" % (Variables.get_sub_folder_path())
            Variables.set_raw_eeg_timestamp_file_path(eeg_timestamp_file)

            self.router.set_raw_eeg_file_path()
            print(Variables.get_raw_eeg_file_path())

            self.ui.label_run_number.setText(str(Variables.get_run_counter()))
            print("\nsubfolder created Run {}".format(Variables.get_run_counter()))

            self.init_table_file_path()
            self.update_table_file_path()

            self.router.start_recording()
            # Variables.set_run_time_counter(0)
            # time_show = Variables.get_run_time_counter()
            self.time_show = 0
            self.ui.lcdNumber_timer.display(self.time_show)

            self.Runtimer.start(1)
            self.t = Thread(target=reactor.run, args=(False,))
            self.t.start()

            timestamp = time.strftime('%Y%m%d-%H%M%S', time.localtime())
            print("\nlocal time stamp: ", timestamp)
        else:
            print(0)
            self.ui.statusBar.showMessage("Recording stopped")
            logger.info("stop rec clicked")
            print("get raw eeg file path", Variables.get_raw_eeg_file_path())
            #
            # self.t.join()
            reactor.stop()
            self.Runtimer.stop()

            self.router.stop_recording()
            Utils.write_data_to_csv(self.os_time_list, "os_time_list.csv")
            Utils.write_data_to_csv(self.os_time_list1, "os_time_list1.csv")
            Utils.write_dict_to_csv(self.create_channel_dict(), "channels.csv")
            Utils.write_dict_to_csv(self.bad_epoch_dict, "bad_epochs.csv")
            self.event_file_path = Utils.write_data_to_csv(self.event_timestamp_list, 'event.csv')
            print(self.event_file_path)
            # if self.total_trials_raw_MRCP != [] and self.total_trials_MRCP != []:
            #     no_trials = len(self.total_trials_raw_MRCP)
            #     no_channels = 9
            #     # raw_MRCP = np.reshape(np.asarray(self.total_trials_raw_MRCP), (no_trials * no_channels, -1))
            #     # self.raw_mrcp_file_path = Utils.write_data_to_csv(raw_MRCP, "raw_mrcp.csv")
            #     # self.mrcp_template_file_path = Utils.write_data_to_csv(self.total_trials_MRCP, "mrcp_template.csv")

            self.update_table_file_path()
            Variables.init_Variables_for_next_run()
            self.init_panel_GUI_stop_recording()
            self.init_SV_GUI()

            self.ui.tab_event_and_file_management.setEnabled(True)
            self.ui.tab_experimental_protocol.setEnabled(True)
            self.ui.tab_experiment_type.setEnabled(True)
            self.ui.groupBox_task_manager.setEnabled(True)
            self.ui.tableWidget_tasks.setRowCount(0)
            self.ui.tableWidget_task_event_number.setRowCount(0)
            self.ui.graphicsView.clear()


    def create_channel_dict(self):
        """
        Read current channel names from LSL and return a dictionary.
        :return: channel name dictionary
        """
        keys = list(range(len(self.channel_labels.tolist())))
        channel_dict = dict(zip(keys, self.channel_labels.tolist()))
        return channel_dict