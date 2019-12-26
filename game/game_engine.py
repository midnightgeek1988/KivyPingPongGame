#@AlirezaKarimi
#alireza.karimi.67@gmail.com
from kivy.clock import Clock


class Engine(object):
    def __init__(self):
        self.event = None

    def start(self, call_back):
        self.event = Clock.schedule_interval(call_back, 1.0 / 60.0)

    def stop(self):
        Clock.unschedule(self.event)
