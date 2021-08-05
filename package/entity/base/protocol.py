import numpy as np
from package.entity.edata.utils import Utils
import pickle

class Protocol():
    '''
    Protocol contains all trials in a specific order.

    Attributes
    ----------
    task_list: a 2d list with shape of #_task * 5, it contains all different tasks
    trial_list: this is a 2d list with shape of #_trial * 5. Five columns consists of
                trial name, event number, trial descriptive name, image path and sound path
    '''
    def __init__(self):
        self.task_list = []
        self.trial_list = []
        self.break_trial_number = 30

    def add_task(self, trial):
        '''
        Add one trial to the trial list
        :param trial: object of Trial
        '''
        self.task_list.append(trial)

    def delete_task(self, delete_id):
        '''
        Delete one trial from existing trial list
        :param delete_id: id of the trial to delete
        '''
        self.task_list.pop(delete_id)

    def finish_adding_task(self):
        '''
        copy task_list to trial_list
        '''
        self.trial_list = self.task_list.copy()

    def randomize_order(self):
        '''
        Randomize the order of the trial list
        '''
        np.random.shuffle(self.trial_list)

    def create_sequence(self, times):
        '''
        Create repetitive groups of trial sequence
        :param times: # of repetition
        '''
        for i in range(int(times) - 1):
            self.trial_list.extend(self.task_list)

    def save_protocol(self, file):
        '''
        Save current object to pickle
        :param file: protocol file name (.pickle)
        '''
        with open(file, 'wb') as f:
            pickle.dump(self, f)
        # with open(file, 'w') as f:
        #     np.savetxt(file, self.trial_list, delimiter=',', fmt='%.200s',
        #                header="task_name, task_description, image_path, sound_path")

    @classmethod
    def load_protocol(self, file):
        '''
        load saved protocol from pickle file
        :param file: protocol file path
        '''
        with open(file, 'rb') as f:
            protocol = pickle.load(f)
        return protocol

    def set_break_trial_number(self, num):
        '''
        set number of trials before a break
        :param num: number of trials before a break
        '''
        self.break_trial_number = num
