from package.entity.edata.utils import Utils
from package.entity.edata.variables import Variables
class Event():
    '''
    Event class controls recording event number with timestamps.

    Attribute
    ---------
    event_timestamp_list: N by 2 list, first column is event number, second column is timestamp
    event_file_path: csv file to save event file
    '''
    def __init__(self):
        self.event_timestamp_list = []
        self.event_file_path = ""

    def add_event(self, event_number, timestamp):
        '''
        add one event with its timestamp to the event_timestamp_list and write this row into event file
        :param event_number: a number associated with each cue and task
        :param timestamp: LSL timestamp or any other universal timestamps which could match with raw_eeg.csv
        '''
        self.event_timestamp_list.append([event_number, timestamp])
        event_row = [event_number, timestamp]
        Utils.write_data_during_recording(self.event_file_path, event_row)

    def create_file(self):
        '''
        create an event file in the beginning
        '''
        self.event_file_path = r"{}/{}".format(Variables.get_sub_folder_path(), 'event.csv')
        f = open(self.event_file_path, 'x')
        f.close()
