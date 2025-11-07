import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.lang import Builder
import random
import os
import sys

kivy.require('2.1.0')

# --- KV Layout ---
KV = '''
<Player>:
    source: 'assets/player.png'
    size_hint: None, None
    size: 80, 80

<Obstacle>:
    source: 'assets/enemy.png'
    size_hint: None, None
    size: 80, 80

<RunnerGame>:
    player: runner_player
    
    canvas.before:
        Color:
            rgb: 0.3, 0.6, 1
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgb: 0.2, 0.2, 0.2
        Rectangle:
            size: self.width, 100
            pos: self.x, self.y

    Player:
        id: runner_player
        pos: self.parent.center_x - 40 if self.parent else 0, 100

    Label:
        font_size: 24
        text: 'Score: ' + str(root.score)
        pos_hint: {"x": 0.02, "top": 0.98}
        size_hint: None, None
        height: 30
        width: 150

    Label:
        id: game_over_label
        font_size: 48
        text: 'Game Over' if root.game_over else ''
        color: 1, 0, 0, 1
        center_x: root.center_x
        center_y: root.center_y
'''

# --- Player ---
class Player(Image):
    velocity_x = NumericProperty(0)
    gravity = NumericProperty(-2000)
    jump_velocity = NumericProperty(800)
    is_jumping = NumericProperty(0)

    def move(self, dt):
        lane_width = self.parent.width / 3
        self.x += self.velocity_x * dt

        # Clamp to screen lanes
        if self.center_x < lane_width / 2:
            self.center_x = lane_width / 2
        elif self.center_x > self.parent.width - lane_width / 2:
            self.center_x = self.parent.width - lane_width / 2

        # Jumping logic
        if self.is_jumping == 1:
            self.y += self.jump_velocity * dt
            self.jump_velocity += self.gravity * dt

            ground_y = self.parent.y + 100
            if self.y <= ground_y:
                self.y = ground_y
                self.is_jumping = 0
                self.jump_velocity = 800

    def jump(self):
        if self.is_jumping == 0:
            self.is_jumping = 1

    def change_lane(self, direction):
        lane_width = self.parent.width / 3
        target_x = self.center_x + direction * lane_width
        self.center_x = target_x


# --- Obstacle ---
class Obstacle(Image):
    scroll_speed = NumericProperty(300)

    def move(self, dt):
        self.x -= self.scroll_speed * dt
        if self.right < 0:
            if self.parent:
                self.parent.remove_widget(self)


# --- Main Game Logic ---
class RunnerGame(Widget):
    player = ObjectProperty(None)
    score = NumericProperty(0)
    game_over = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(RunnerGame, self).__init__(**kwargs)
        self.obstacles = []
        self.passed_obstacles = []

        # Load sounds safely
        self.bg_music = SoundLoader.load('assets/bg_music.mp3') if os.path.exists('assets/bg_music.mp3') else None
        self.over_sound = SoundLoader.load('assets/over.mp3') if os.path.exists('assets/over.mp3') else None

        if self.bg_music:
            self.bg_music.loop = True
            self.bg_music.play()

        self.bind(on_touch_down=self.on_mobile_touch)

        Clock.schedule_interval(self.update, 1 / 60)
        Clock.schedule_interval(self.spawn_obstacle, 2.5)

    def update(self, dt):
        if self.game_over:
            return

        self.player.move(dt)

        for obstacle in list(self.obstacles):
            obstacle.move(dt)

            if self.player.collide_widget(obstacle):
                self.game_end()
                return

            if obstacle.right < self.player.x and obstacle not in self.passed_obstacles:
                self.score += 1
                self.passed_obstacles.append(obstacle)

    def spawn_obstacle(self, dt):
        if self.game_over:
            return

        lane_width = self.width / 3
        lane = random.choice([0, 1, 2])
        x_pos = self.width + 100
        y_pos = self.y + 100

        obstacle = Obstacle()
        obstacle.center_x = x_pos
        obstacle.y = y_pos
        obstacle.center_x = lane_width * (lane + 0.5)

        self.add_widget(obstacle)
        self.obstacles.append(obstacle)

    def game_end(self):
        self.game_over = True
        if self.bg_music:
            self.bg_music.stop()
        if self.over_sound:
            self.over_sound.play()

    def on_mobile_touch(self, touch):
        if self.game_over:
            # Restart game by reloading
            App.get_running_app().stop()
            os.execl(sys.executable, sys.executable, *sys.argv)

        if touch.is_double_tap:
            self.player.jump()
        elif touch.pos[0] < self.width / 2:
            self.player.change_lane(-1)
        else:
            self.player.change_lane(1)


# --- App ---
class SubwayRunnerApp(App):
    def build(self):
        Builder.load_string(KV)
        return RunnerGame()


if __name__ == '__main__':
    SubwayRunnerApp().run()
