
class MainSwitch():
    def onClicked_button_Main_switch(self, pressed):
        """
        Event listener for main switch down the experimenter GUI
        """
        if pressed:
            self.ui.statusBar.showMessage("System is On")
            self.ui.tab_experimental_protocol.setEnabled(True)
            self.ui.tab_subjec_information.setEnabled(True)
            self.ui.tab_event_and_file_management.setEnabled(True)
            self.ui.tab_Oscilloscope.setEnabled(True)
            self.ui.tab_experiment_type.setEnabled(True)
        else:
            self.ui.statusBar.showMessage("System is Off")
            self.ui.tab_experimental_protocol.setEnabled(False)
            self.ui.tab_subjec_information.setEnabled(False)
            self.ui.tab_event_and_file_management.setEnabled(False)
            self.ui.tab_Oscilloscope.setEnabled(False)
            self.ui.tab_experiment_type.setEnabled(False)