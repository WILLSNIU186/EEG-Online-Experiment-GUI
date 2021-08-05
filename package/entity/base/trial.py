class Trial():
    '''
    One trial includes multiple cues, it also has a property of task type

    Parameters
    ----------
    name: trial name (e.g. WE_L)
    desc_name: descriptive trial name show for subject (e.g. left wrist extension)
    image: illustration image path
    video: illustration video path
    sound: illustration sound path

    Attributes
    ----------
    cue_list: cues contained in this trial
    duration: duration of whole trial
    '''

    def __init__(self, name=None, desc_name=None, event_number = None, cue_list=None, image=None, video=None, sound=None):
        self.cue_list = cue_list
        self.name = name
        self.desc_name = desc_name
        self.image = image
        self.video = video
        self.sound = sound
        self.event_number = event_number
        self.duration = 0

    def concatenate_cues(self, cues):
        '''
        create a trial by concatenating different cues
        :param cues: list of Cue objects
        '''
        self.cue_list = cues

    def add_cues(self, cues):
        '''
        add one or multiple cues to the current trial
        :param cues: Cue or list of Cue objects
        '''
        self.cue_list.extend(cues)

    def get_duration(self):
        '''
        Add cue duration together to get trial duration
        '''
        for cue in self.cue_list:
            self.duration += cue.duration

    def set_event_number(self, event_number):
        '''
        set event number for each cue
        :param event_number: int
        '''
        self.event_number = event_number


