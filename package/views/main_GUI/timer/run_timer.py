import time

class RunTimer():

    def Time(self):
        """
        Call update subject view window image if task button clicked and display timer on experimenter
        GUI.
        """
        os_time = time.time()
        self.os_time_list.append(os_time)
        if self.is_experiment_on:
            self.Update_SV_image()
        # Variables.add_one_run_time_counter()
        # time_show = Variables.get_run_time_counter()
        self.time_show += 1
        self.ui.lcdNumber_timer.display(self.time_show)