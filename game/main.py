#@AlirezaKarimi
#alireza.karimi.67@gmail.com
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

from game_engine import Engine
from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector

from win_popup import WinAlarm

sm = ScreenManager()


class SettingsScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game = PongGame()
        self.game.serve_ball()
        self.add_widget(self.game)

    def start_game(self):
        self.game.start_game()


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    game_engine = Engine()

    def open_main(self):
        self.game_engine.stop()
        self.player1.score = 0
        self.player2.score = 0
        self.serve_ball()
        sm.current = 'MainScreen'

    def start_game(self):
        self.game_engine.start(self.update)

    def stop_game(self):
        self.game_engine.stop()

    def restart_game(self):
        self.player1.score = 0
        self.player2.score = 0
        self.serve_ball()
        self.start_game()

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))

        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

        if self.player1.score == 1:
            self.stop_game()
            content = WinAlarm()
            content.bind(on_answer=self.alarm_answer)
            self.popup = Popup(title="Player 1 Win the game", content=content, size_hint=(None, None), size=(300, 200),
                               auto_dismiss=False)
            self.popup.open()
        elif self.player2.score == 1:
            self.stop_game()
            content = WinAlarm()
            content.bind(on_answer=self.alarm_answer)
            self.popup = Popup(title="Player 2 Win the game", content=content, size_hint=(None, None), size=(300, 200),
                               auto_dismiss=False)
            self.popup.open()

    def on_touch_move(self, touch):
        if touch.x < self.width /3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

    def alarm_answer(self, instance, play_again):
        if play_again == "yes":
            self.popup.dismiss()
            self.restart_game()
        elif play_again == "no":
            self.popup.dismiss()
            sm.current = 'MainScreen'


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            speed_up = 1.1
            offset = 0.02 * Vector(0, ball.center_y - self.center_y)
            ball.velocity = speed_up * (offset - ball.velocity)


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongApp(App):
    def build(self):
        sm.add_widget(MainScreen(name='MainScreen'))
        sm.add_widget(GameScreen(name='GameScreen'))
        sm.add_widget(SettingsScreen(name='SettingScreen'))
        sm.current = 'MainScreen'
        return sm


if __name__ == '__main__':
    PongApp().run()
