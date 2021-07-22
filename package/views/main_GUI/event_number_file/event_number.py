from package.entity.edata.utils import Utils


class EventNumber():

    def onClicked_button_save_event_number(self):
        """
        Event listener for save button in Event and File Management tab.
        Save task name and event number to Run1/event.csv
        """
        event_dict = self.get_event_number_table_content()
        Utils.write_event_number_to_csv(event_dict)

    def get_event_number_table_content(self):
        """
        Get task name and event number from event number table.
        """
        self.event_number_list = []
        self.event_name_list = []
        for i in range(self.ui.tableWidget_task_event_number.rowCount()):
            self.event_name_list.append(self.ui.tableWidget_task_event_number.item(i, 0).text())
            self.event_number_list.append(int(self.ui.tableWidget_task_event_number.item(i, 1).text()))
        self.event_table_dictionary = dict(zip(self.event_name_list, self.event_number_list))
        return self.event_table_dictionary
        # print("TTTTTTTTTTTTTTTTTTTTTTTTTTTT\n", self.event_table_dictionary)


    def init_task_event_number_table(self):
        """
        Initialize the header of event number table.
        """
        self.ui.tableWidget_task_event_number.setColumnCount(2)
        self.ui.tableWidget_task_event_number.setHorizontalHeaderLabels(["Task name", "Event number"])