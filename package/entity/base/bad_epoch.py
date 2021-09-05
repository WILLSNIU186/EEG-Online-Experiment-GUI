from package.entity.edata.variables import Variables
from package.entity.edata.utils import Utils

class BadEpoch():
    '''
    BadEpoch records trial numbers of noise-contaminated trials identified by experimenter during experiment.

    Attribute
    ----------
    bad_epoch_dict: a dictionary holds task names as key and their corresponding bad trial number as list
    '''
    def __init__(self):
        self.bad_epoch_dict = {}

    def add_events(self, task_list):
        '''
        add event as keys for bad_epoch_dict and initialize it with an empty list
        :param task_list: a list of trial objects.
        '''
        for i in range(len(task_list)):
            self.bad_epoch_dict[task_list[i].name] = []

    def create_file(self):
        '''
        create a bad_epoch file in the beginning
        '''
        self.file_path = r"{}/{}".format(Variables.get_sub_folder_path(), 'bad_epochs.csv')
        f = open(self.file_path, 'x')
        f.close()

    def add_bad_epoch(self, task_name, trial_number):
        '''
        add one bad epoch at a time, append to specific key of bad_epoch_dict and write to file
        :param task_name: protocol.task_list[id].name
        :param trial_number: current trial of a certain task
        '''
        self.bad_epoch_dict[task_name].append(trial_number + 1)
        Utils.write_dict_to_csv(self.bad_epoch_dict, "bad_epochs.csv")

