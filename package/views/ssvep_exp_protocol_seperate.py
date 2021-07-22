from psychopy import visual, event, core
import numpy as np
import time

frequencies_list = [8.423, 9.374, 9.961, 10.84, 11.79, 13.4, 14.87]
positions_list = [(-64, 128), (64, 128), (-128, 0), (0, 0), (128, 0), (-64, -128), (64, -128)]
# stimulus_sequence = [1, 4, 3, 2, 5, 6, 7, 7, 1, 3, 4 ]

number_of_trials = 8
number_of_stimuli = len(frequencies_list)
stimulus_sequence = np.tile(np.arange(1, number_of_stimuli+1), number_of_trials)
np.random.shuffle(stimulus_sequence)

stimulation_period = 6
break_period = 4
cue_period = 2

stimulus_size = (128, 128)
screen_size = [1024, 512]
screen_refresh_rate = 60

def get_frame_movement_phase(frame_number, stimulus_frequency):
    movement_phase = ((np.pi / 2) + (np.pi / 2) * np.sin(
        (2 * np.pi * frame_number * (stimulus_frequency / (2 * screen_refresh_rate))) - (np.pi / 2))) / np.pi * 0.5
    return movement_phase


def get_frame_intensity(frame_number, stimulus_frequency):
    stimulus_intensity = np.sin(2 * np.pi * frame_number * (stimulus_frequency / (screen_refresh_rate)))
    return stimulus_intensity


def generate_radial_stimulus_list(win, positions_list, stimulus_size, radial_cycles=5, angular_cycles=12):
    stimulus_list = []
    stimulus_mask_list = []
    for stim_position in positions_list:
        wedge = visual.RadialStim(win, tex='sqrXsqr', color=-1, size=stimulus_size[0], pos=stim_position, units='pix',
                                  visibleWedge=[0, 360], radialCycles=5, angularCycles=12, interpolate=False,
                                  autoLog=False)
        stimulus_list.append(wedge)
        circle_target = visual.Circle(win, fillColor=[0.5, 0.5, 0.5], size=10, pos=stim_position, units='pix')
        stimulus_mask_list.append(circle_target)

    return stimulus_list, stimulus_mask_list


def generate_flickering_stimulus_list(win, positions_list, stimulus_size, radial_cycles=5, angular_cycles=12):
    stimulus_list = []
    for stim_position in positions_list:
        circle_target = visual.Circle(win, fillColor=[1.0, 1.0, 1.0], size=stimulus_size[0], pos=stim_position,
                                      units='pix')
        stimulus_list.append(circle_target)

    return stimulus_list


stim_type = 'ssmvep'

class SSVEPExpProtocol():
    def __init__(self):
        pass

    def onClicked_pushButton_ssvep_task(self):

        # Thread(target=self.play_task_sound, args=(self.new_task_table[self.task_counter][3],)).start()
        self.run_ssvep_protocol()
        # run_ssvep_protocol(win=win, stim_type='ssvep')


    def run_ssvep_protocol(self, stim_type='ssmvep', stimulus_sequence=stimulus_sequence,
                           positions_list=positions_list, screen_refresh_rate=screen_refresh_rate,
                           frequencies_list=frequencies_list):
        # self.hide()
        win = visual.Window(screen_size, color=(-1.0, -1.0, -1.0))
        if stim_type == 'ssvep':
            stimulus_list = generate_flickering_stimulus_list(win, positions_list, stimulus_size)
            stimulus_mask_list = None
        elif stim_type == 'ssmvep':
            stimulus_list, stimulus_mask_list = generate_radial_stimulus_list(win, positions_list, stimulus_size)

        for sequence_idx, stimulus_id in enumerate(stimulus_sequence):
            message = visual.TextStim(win, text='1', height=0.1, color=(0, 1, 0))
            message.setAutoDraw(True)
            message.pos = (
                positions_list[stimulus_id - 1][0] / screen_size[0] * 2,
                positions_list[stimulus_id - 1][1] / screen_size[1] * 2)
            win.flip()
            time.sleep(cue_period)
            message.setAutoDraw(False)
            for frame_number in range(1, int(stimulation_period * screen_refresh_rate)):
                if not event.getKeys():
                    for stimulus_idx, stimulus in enumerate(stimulus_list):
                        if stim_type == 'ssvep':
                            stimulus.opacity = get_frame_intensity(frame_number, frequencies_list[stimulus_idx])
                            stimulus.draw()
                        elif stim_type == 'ssmvep':
                            stimulus.radialPhase = get_frame_movement_phase(frame_number,
                                                                            frequencies_list[stimulus_idx])
                            stimulus.draw()
                            stimulus_mask_list[stimulus_idx].draw()
                    win.flip()
                else:
                    win.close()
                    core.quit()
            win.flip()
            time.sleep(break_period)


if __name__ == '__main__':
    ssvep = SSVEPExpProtocol()
    ssvep.run_ssvep_protocol()