#@AlirezaKarimi
#alireza.karimi.67@gmail.com
from kivy.uix.gridlayout import GridLayout


class WinAlarm(GridLayout):
    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super(WinAlarm, self).__init__(**kwargs)

    def on_answer(self, *args):
        pass
