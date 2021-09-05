import random

class Cue():
    '''
    Base class for Cue. Cue is the most fundamental element of experiment,
    a trial is established by concatenating multiple cues.

    Parameter
    ----------
    name: str name of cue (e.g. 'IDLE')
    duration: int or tuple, duration of cue
    image: illustration image path
    video: illustration video path
    sound: illustration sound path

    '''
    def __init__(self, name=None, duration=None, event_number=None, image=None, video=None, sound=None):
        self.name = name
        self.image = image
        self.video = video
        self.sound = sound
        self.event_number = event_number
        self.duration = duration

    def set_event_number(self, event_number):
        '''
        set event number for each cue
        :param event_number: int
        '''
        self.event_number = event_number

    def set_duration(self, duration):
        if isinstance(duration, int):
            self.duration = duration
        elif isinstance(duration, tuple):
            self.randomize_duration(duration[0], duration[1])

    def randomize_duration(self, lower_limit, higher_limit):
        '''
        set a tuple for duration of a cue
        :param lower_limit: lower bound of the duration
        :param higher_limit: higher bound of the duration

        '''
        self.duration = random.randint(lower_limit, higher_limit)





