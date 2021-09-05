import os
import time
from threading import Thread
from pycnbi import logger
from twisted.internet import reactor
import csv
from package.entity.edata.utils import Utils
from package.entity.edata.variables import Variables

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


            self.router.set_raw_eeg_file_path()
            print(Variables.get_raw_eeg_file_path())

            self.ui.label_run_number.setText(str(Variables.get_run_counter()))
            print("\nsubfolder created Run {}".format(Variables.get_run_counter()))

            self.router.start_recording()
            # Variables.set_run_time_counter(0)
            # time_show = Variables.get_run_time_counter()
            self.time_show = 0
            self.ui.lcdNumber_timer.display(self.time_show)

            self.Runtimer.start(1)
            self.t = Thread(target=reactor.run, args=(False,))
            self.t.start()


            self.event_obj.create_file()
            self.bad_epoch.create_file()

            logger.info(self.event_file_path)

            timestamp = time.strftime('%Y%m%d-%H%M%S', time.localtime())
            print("\nlocal time stamp: ", timestamp)
        else:
            print(0)
            self.ui.statusBar.showMessage("Recording stopped")
            logger.info("stop rec clicked")
            print("get raw eeg file path", Variables.get_raw_eeg_file_path())

            reactor.stop()
            self.Runtimer.stop()

            self.router.stop_recording()

            Utils.write_dict_to_csv(self.create_channel_dict(), "channels.csv")

            Variables.init_Variables_for_next_run()
            self.init_panel_GUI_stop_recording()
            self.init_SV_GUI()

            self.ui.tab_experimental_protocol.setEnabled(True)
            self.ui.tab_experiment_type.setEnabled(True)
            self.ui.groupBox_task_manager.setEnabled(True)
            self.ui.tableWidget_tasks.setRowCount(0)
            self.ui.widget_mrcp_extractor.clear()


    def create_channel_dict(self):
        """
        Read current channel names from LSL and return a dictionary.
        :return: channel name dictionary
        """
        keys = list(range(len(self.channel_labels.tolist())))
        channel_dict = dict(zip(keys, self.channel_labels.tolist()))
        return channel_dict