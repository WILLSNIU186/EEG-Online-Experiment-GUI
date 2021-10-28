from psychopy import visual, event, core
import pdb
import numpy as np
import pandas as pd
import time
from datetime import timezone
import datetime
import multiprocessing as mp
from pycnbi.stream_receiver.stream_receiver import StreamReceiver
from package.entity.edata.variables import Variables

stimulus_type_dict = {'SSVEP_Flicker': 'ssvep',
                      'SSMVEP_Checkerboard': 'ssmvep',
                      'AO_Gait': 'ao_gait'}

screen_size = [1700, 900]

ao_images_folder_path = 'D:\Aravind\dev\code\ssvep_stimulus_gen\subset_compressed_contrast_modified'


checkerboard_size = (1.25*128, 1.25*128)
screen_refresh_rate = 60

rcycles = 14
M = 12
D = 10
L = 18
stimulus_size = 64

xylim = 2 * np.pi * rcycles
x1, y1 = np.meshgrid(np.linspace(-xylim, xylim, stimulus_size), np.linspace(-xylim, xylim, stimulus_size))
angle_xy = np.arctan2(x1, y1)
temp_circle = (x1**2 + y1**2)
radius_values = np.sqrt(temp_circle)
circle1 = (temp_circle <= xylim**2)*1
circle2 = (temp_circle >= 80)*1
mask = circle1 * circle2
first_term = (np.pi*radius_values/D)
second_term = np.cos(angle_xy*M)


def get_frame_movement_phase(frame_number, stimulus_frequency, screen_refresh_rate):
    movement_phase = ((np.pi/2)+(np.pi/2)*np.sin((2*np.pi*frame_number*(stimulus_frequency/(2*screen_refresh_rate)))-(np.pi/2)))
    checks = np.sign(np.cos(first_term+movement_phase*(L/D))*second_term) * mask
    
    return checks

def generate_radial_stimulus_list(win, positions_list, stimulus_size):
    stimulus_list = []
    for stim_position in positions_list:
        wedge = visual.GratingStim(win, size=checkerboard_size[0], pos=stim_position, units='pix')  
        stimulus_list.append(wedge)
        
    return stimulus_list


# def generate_radial_stimulus_list(win, positions_list, stimulus_size, radial_cycles=5, angular_cycles=12):
#     stimulus_list = []
#     stimulus_mask_list = []
#     for stim_position in positions_list:
#         wedge = visual.RadialStim(win, tex='sqrXsqr', color=-1, size=stimulus_size[0], pos=stim_position, units='pix',
#                                   visibleWedge=[0, 360], radialCycles=5, angularCycles=12, interpolate=False,
#                                   autoLog=False)
#         stimulus_list.append(wedge)
#         circle_target = visual.Circle(win, fillColor=[0.5, 0.5, 0.5], size=10, pos=stim_position, units='pix')
#         stimulus_mask_list.append(circle_target)

#     return stimulus_list, stimulus_mask_list




def get_ao_stimuli_paths(ao_images_folder_path):
    ao_stimuli_image_paths = []
    for image_idx in range(1, 17):
        ao_stimuli_image_paths.append(f'{ao_images_folder_path}/{image_idx}.jpg')
    
    return ao_stimuli_image_paths

def get_utc_time():
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    
    return utc_timestamp

# def get_frame_movement_phase(frame_number, stimulus_frequency, screen_refresh_rate):
#     movement_phase = ((np.pi / 2) + (np.pi / 2) * np.sin(
#         (2 * np.pi * frame_number * (stimulus_frequency / (2 * screen_refresh_rate))) - (np.pi / 2))) / np.pi * 0.5
#     return movement_phase

def get_frame_intensity(frame_number, stimulus_frequency, screen_refresh_rate):
    stimulus_intensity = np.sin(2 * np.pi * frame_number * (stimulus_frequency / (screen_refresh_rate)))
    return stimulus_intensity


def generate_flickering_stimulus_list(win, positions_list, stimulus_size, radial_cycles=5, angular_cycles=12):
    stimulus_list = []
    for stim_position in positions_list:
        circle_target = visual.Circle(win, fillColor=[1.0, 1.0, 1.0], size=stimulus_size[0], pos=stim_position,
                                      units='pix')
        stimulus_list.append(circle_target)

    return stimulus_list

#check event.py in base folder
def save_timestamps_dataframe(event_times_df, base_folder_path, stimulus_type):
    utc_timestamp = get_utc_time()
    savefile_path = f'{base_folder_path}\{stimulus_type}_timestamps_event_id_{int(utc_timestamp)}.csv'
    event_times_df.to_csv(savefile_path, index=False)
    
def run_ssvep_protocol(stim_type='ssvep', serial=None, name=None, base_folder_path=None, stimulus_sequence=None,
                       positions_list=None, screen_refresh_rate=60, frequencies_list=None, 
                       stimulus_size=(128, 128), cue_period=2, stimulation_period=6,
                       break_period=4):
    event_times_df = pd.DataFrame({'event_name': [], 'timestamp': [], 'utc_time': [], 'lsl_time': []})
    sr = StreamReceiver(window_size=1, buffer_size=10,
                        amp_serial=serial, amp_name=name)
    data, times = sr.acquire("from ssvep", blocking=False)
    win = visual.Window(screen_size, color=(0.0, 0.0, 0.0))
    if stim_type == 'ssvep':
        stimulus_list = generate_flickering_stimulus_list(win, positions_list, stimulus_size)
        stimulus_mask_list = None
    elif stim_type == 'ssmvep':
        # stimulus_list, stimulus_mask_list = generate_radial_stimulus_list(win, positions_list, stimulus_size)
        stimulus_list = generate_radial_stimulus_list(win, positions_list, stimulus_size)

    for sequence_idx, stimulus_id in enumerate(stimulus_sequence):
        data, times = sr.acquire("from ssvep", blocking=False)    
        event_times_df = event_times_df.append({'event_name': 'cue_start', 'timestamp': sr.timestamps[-1][-1], 'utc_time': get_utc_time(), 'lsl_time': sr.get_lsl_clock()}, ignore_index=True)
        message = visual.TextStim(win, text='1', height=0.1, color=(0, 1, 0))
        message.setAutoDraw(True)
        message.pos = (
            positions_list[stimulus_id - 1][0] / screen_size[0] * 2,
            positions_list[stimulus_id - 1][1] / screen_size[1] * 2)
        win.flip()
        time.sleep(cue_period)
        message.setAutoDraw(False)
        data, times = sr.acquire("from ssvep", blocking=False)    
        event_times_df = event_times_df.append({'event_name': f'stim_{stimulus_id}', 'timestamp': sr.timestamps[-1][-1], 'utc_time': get_utc_time(), 'lsl_time': sr.get_lsl_clock()}, ignore_index=True)
        for frame_number in range(1, int(stimulation_period * screen_refresh_rate)):
            if not event.getKeys():
                for stimulus_idx, stimulus in enumerate(stimulus_list):
                    if stim_type == 'ssvep':
                        stimulus.opacity = get_frame_intensity(frame_number, frequencies_list[stimulus_idx],
                                                               screen_refresh_rate)
                        stimulus.draw()
                    elif stim_type == 'ssmvep':
                        # stimulus.radialPhase = get_frame_movement_phase(frame_number,
                        #                                                 frequencies_list[stimulus_idx],
                        #                                                 screen_refresh_rate)
                        
                        for stimulus_idx, stimulus in enumerate(stimulus_list):
                            stimulus.tex = get_frame_movement_phase(frame_number,
                                                                frequencies_list[stimulus_idx],
                                                                screen_refresh_rate)
                        for stimulus_idx, stimulus in enumerate(stimulus_list):
                            stimulus.draw()
                        # stimulus_mask_list[stimulus_idx].draw()
                win.flip()
            else:
                win.close()
                save_timestamps_dataframe(event_times_df, base_folder_path, stim_type)
                core.quit()
        win.flip()
        data, times = sr.acquire("from ssvep", blocking=False)    
        event_times_df = event_times_df.append({'event_name': 'break_start', 'timestamp': sr.timestamps[-1][-1], 'utc_time': get_utc_time(), 'lsl_time': sr.get_lsl_clock()}, ignore_index=True)
        time.sleep(break_period)
        data, times = sr.acquire("from ssvep", blocking=False)    
        event_times_df = event_times_df.append({'event_name': 'break_end', 'timestamp': sr.timestamps[-1][-1], 'utc_time': get_utc_time(), 'lsl_time': sr.get_lsl_clock()}, ignore_index=True)
    save_timestamps_dataframe(event_times_df, base_folder_path, stim_type)


def run_ao_gait_protocol(stimulus_type='ao_gait', serial=None, name=None, base_folder_path=None, stimulus_sequence=None,
                         positions_list=None, screen_refresh_rate=60, frequencies_list=None, 
                         stimulus_size=(128, 128), cue_period=2, stimulation_period=6,
                         break_period=4, ao_stimuli_image_paths=None):
    #TODO: Refactor the code
    print('Cue: ', cue_period, 'Stim: ', stimulation_period, 'Break: ', break_period)
    event_times_df = pd.DataFrame({'event_name': [], 'timestamp': [], 'utc_time': [], 'lsl_time': []})
    sr = StreamReceiver(window_size=1, buffer_size=10,
                        amp_serial=serial, amp_name=name)
    data, times = sr.acquire("from ssvep", blocking=False)
    win = visual.Window(screen_size, color=(-1.0, -1.0, -1.0))
    for sequence_idx, stimulus_id in enumerate(stimulus_sequence):
        data, times = sr.acquire("from ssvep", blocking=False)    
        event_times_df = event_times_df.append({'event_name': 'cue_start', 'timestamp': sr.timestamps[-1][-1], 'utc_time': get_utc_time(), 'lsl_time': sr.get_lsl_clock()}, ignore_index=True)
        message = visual.TextStim(win, text=f'{stimulus_id}', height=0.1, color=(0, 1, 0))
        message.setAutoDraw(True)
        message.pos = (positions_list[stimulus_id-1][0], positions_list[stimulus_id-1][1])
        win.flip()
        time.sleep(cue_period)
        message.setAutoDraw(False)
        data, times = sr.acquire("from ssvep", blocking=False)    
        event_times_df = event_times_df.append({'event_name': f'stim_{stimulus_id}', 'timestamp': sr.timestamps[-1][-1], 'utc_time': get_utc_time(), 'lsl_time': sr.get_lsl_clock()}, ignore_index=True)
        stimulus_current_elapsed_time_1 = time.time()
        stimulus_current_elapsed_time_2 = time.time()
        img_idx_1 = 0
        img_idx_2 = 0
        stimulation_start = time.time()
        while (time.time() - stimulation_start) < stimulation_period:
            if not event.getKeys():
                ao_stimulus_1 = visual.ImageStim(win, image=ao_stimuli_image_paths[img_idx_1], size=stimulus_size, pos=positions_list[0])
                ao_stimulus_1.draw()
                ao_stimulus_2 = visual.ImageStim(win, image=ao_stimuli_image_paths[img_idx_2], size=stimulus_size, pos=positions_list[1])
                ao_stimulus_2.draw()
                if (time.time() - stimulus_current_elapsed_time_1) >= (frequencies_list[0]/screen_refresh_rate):
                    img_idx_1 += 1
                    img_idx_1 = img_idx_1 % len(ao_stimuli_image_paths)
                    ao_stimulus_1 = visual.ImageStim(win, image=ao_stimuli_image_paths[img_idx_1], size=stimulus_size, pos=positions_list[0])
                    ao_stimulus_1.draw()
                    stimulus_current_elapsed_time_1 = time.time()
                # print(time.time() - stimulus_current_elapsed_time_2)
                if (time.time() - stimulus_current_elapsed_time_2) >= (frequencies_list[1]/screen_refresh_rate):
                    img_idx_2 += 1
                    img_idx_2 = img_idx_2 % len(ao_stimuli_image_paths)
                    ao_stimulus_2 = visual.ImageStim(win, image=ao_stimuli_image_paths[img_idx_2], size=stimulus_size, pos=positions_list[1])
                    ao_stimulus_2.draw()
                    stimulus_current_elapsed_time_2 = time.time()
                win.flip()
            else:
                win.close()
                save_timestamps_dataframe(event_times_df, base_folder_path, stimulus_type)
                core.quit()
        win.flip()
        data, times = sr.acquire("from ssvep", blocking=False)    
        event_times_df = event_times_df.append({'event_name': 'break_start', 'timestamp': sr.timestamps[-1][-1], 'utc_time': get_utc_time(), 'lsl_time': sr.get_lsl_clock()}, ignore_index=True)
        time.sleep(break_period)
        data, times = sr.acquire("from ssvep", blocking=False)    
        event_times_df = event_times_df.append({'event_name': 'break_end', 'timestamp': sr.timestamps[-1][-1], 'utc_time': get_utc_time(), 'lsl_time': sr.get_lsl_clock()}, ignore_index=True)
    save_timestamps_dataframe(event_times_df, base_folder_path, stimulus_type)
        
    
class SSVEPExpProtocol():
    
    def input_stimulus_type(self):
        self.stimulus_type = stimulus_type_dict[self.ui.SSVEPStimulusTypeDropDownSelection.currentText()]
        
    def input_number_of_trials(self):
        self.number_of_trials = int(self.ui.lineEdit_InputSSVEPNumberOfTrials.text())
    
    def input_stimulus_size(self):
        split_text = self.ui.lineEdit_InputSSVEPStimulusSize.text().split(',')
        self.stimulus_size = (float(split_text[0][1:]), float(split_text[1][0:-1]))
        
    def input_ssvep_stim_frequencies(self):
        self.stimulus_frequency_string = self.ui.lineEdit_InputSSVEPStimulusFrequencies.text()
        stimulus_frequency_string = self.stimulus_frequency_string
        self.stimulus_frequency_list = list(map(float, stimulus_frequency_string.split(',')))
        number_of_stimuli = len(self.stimulus_frequency_list)
        self.stimulus_sequence = np.tile(np.arange(1, number_of_stimuli+1), self.number_of_trials)
        np.random.shuffle(self.stimulus_sequence)
        
    def input_ssvep_stim_positions(self):
        self.stimulus_positions_string = self.ui.lineEdit_InputSSVEPStimulusPositions.text()
        stimulus_positions_string = self.stimulus_positions_string
        self.stimulus_positions_list = []
        for x_y_string in stimulus_positions_string.split(';'):
            x_coordinate = float(x_y_string.split(',')[0][1:])
            y_coordinate = float(x_y_string.split(',')[1][0:-1])
            self.stimulus_positions_list.append((x_coordinate, y_coordinate))

    def input_protocol_parameters(self):
        self.cue_period = float(self.ui.lineEdit_InputSSVEPCuePeriod.text())
        self.stimulation_period = float(self.ui.lineEdit_InputSSVEPStimulationPeriod.text())
        self.break_period = float(self.ui.lineEdit_InputSSVEPBreakPeriod.text())

    def on_clicked_push_button_ssvep_task(self):
        self.input_stimulus_type()
        self.input_number_of_trials()
        self.input_stimulus_size()
        self.input_ssvep_stim_frequencies()
        self.input_ssvep_stim_positions()
        self.input_protocol_parameters()
        print('Cue: ', self.cue_period, 'Stim: ', self.stimulation_period, 'Break: ', self.break_period)
        self.screen_refresh_rate = 60 #TODO infer from the pyqt or psychopy
        if self.stimulus_type=='ao_gait':
            print('Cue: ', self.cue_period, 'Stim: ', self.stimulation_period, 'Break: ', self.break_period)
            self.ao_stimuli_image_paths = get_ao_stimuli_paths(ao_images_folder_path)
            proc = mp.Process(target=run_ao_gait_protocol, args=[self.stimulus_type, Variables.get_amp_serial(), Variables.get_amp_name(),
                                                                 Variables.get_base_folder_path(), self.stimulus_sequence,
                                                                 self.stimulus_positions_list, self.screen_refresh_rate, self.stimulus_frequency_list,
                                                                 self.stimulus_size, self.cue_period, self.stimulation_period, self.break_period,
                                                                 self.ao_stimuli_image_paths])
            proc.start()
        else:
            proc = mp.Process(target=run_ssvep_protocol, args=[self.stimulus_type, Variables.get_amp_serial(), Variables.get_amp_name(),
                                                               Variables.get_base_folder_path(), self.stimulus_sequence,
                                                               self.stimulus_positions_list, self.screen_refresh_rate, self.stimulus_frequency_list,
                                                               self.stimulus_size, self.cue_period, self.stimulation_period, self.break_period])
            proc.start()
        


if __name__ == '__main__':
    ssvep = SSVEPExpProtocol()
    ssvep.run_ssvep_protocol()