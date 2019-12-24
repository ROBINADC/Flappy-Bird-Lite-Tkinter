# -*- coding: utf-8 -*-

"""
Main application of Flappy bird
refer: https://github.com/geekcomputers/Python/tree/master/Flappy%20Bird%20-%20created%20with%20tkinter
Created on 2019/12/22
"""

__author__ = "Yihang Wu"

import os
import time
import datetime

from tkinter import Tk, Button

from settings import Settings
from background import Background
from bird import Bird
from tubes import Tubes
from utils import get_photo_image


class App(Tk, Settings):
    _background_animation_speed = 720  # A scaled speed for background animation
    _bird_descend_speed = 38.4  # A scaled speed for bird descending
    _bestscore = 0
    _score = 0
    _buttons = []
    _playing = False
    _time = '%H:%M:%S'

    def __init__(self):

        Tk.__init__(self)
        self.set_options()

        # Component
        self._background = None
        self._bird = None
        self._tubes = None

        # Window Size
        if self.window_width and self.window_height:
            self._width = self.window_width
            self._height = self.window_height
        else:
            self._width = self.winfo_screenwidth()
            self._height = self.winfo_screenheight()

        # Window Configuration
        self.title(self.window_name)
        self.geometry(f'{self._width}x{self._height}')
        self.resizable(*self.window_resizable)
        self.attributes('-fullscreen', self.window_fullscreen)
        self['bg'] = 'black'  # Background color

        # Check the integrity of game resources
        for img_fp in self.images_fp:
            if not os.path.exists(img_fp):
                raise FileNotFoundError(f'Cannot find resource:\n{img_fp}')

        # Create a PhotoImage object for start button
        self._start_button_image = get_photo_image(
            image_path=self.start_button_fp,
            width=int(self._width * self.button_scaled_width),
            height=int(self._height * self.button_scaled_height),
            close_after=True
        )[0]

        # Create a PhotoImage object for exit button
        self._exit_button_image = get_photo_image(
            image_path=self.exit_button_fp,
            width=int(self._width * self.button_scaled_width),
            height=int(self._height * self.button_scaled_height),
            close_after=True
        )[0]

        # Create a PhotoImage object for title
        self._title_image = get_photo_image(
            image_path=self.title_fp,
            width=int(self._width * self.title_scaled_width),
            height=int(self._height * self.title_scaled_height),
            close_after=True
        )[0]

        # Create a PhotoImage object for scoreboard
        self._scoreboard_image = get_photo_image(
            image_path=self.scoreboard_fp,
            width=int(self._width * self.scoreboard_scaled_width),
            height=int(self._height * self.scoreboard_scaled_height),
            close_after=True
        )[0]

        # Set background animation speed according to window width
        # 不知道数值是怎么得出来的
        self._background_animation_speed = int(self._background_animation_speed / (self._width / 100))

        # Set bird descend speed according to window height
        self._bird_descend_speed = int(self._bird_descend_speed / (self._height / 100))

    def initialize(self):
        """
        Method to initialize all the components and start the game
        """

        # Load best score
        self.load_score()

        self._background = Background(
            self, self._width, self._height, fp=self.background_fp, animation_speed=self._background_animation_speed
        )

        self._background.focus_force()  # ?

        self._background.bind(self.window_fullscreen_event, self.change_fullscreen_option)
        self._background.bind(self.window_start_event, self.start)
        self._background.bind(self.window_exit_event, self.close)

        # 用self.close注册"WM_DELETE_WINDOW"协议
        # 当用户使用窗口管理器显式关闭窗口时,调用self.close函数,先记录分数,再退出
        self.protocol("WM_DELETE_WINDOW", self.close)

        self._background.pack()  # ?

        self.create_title_image()

        self.create_menu_buttons()

        self._bird = Bird(
            self._background, self.gameover, self.bird_fp, self._width, self._height,
            descend_speed=self._bird_descend_speed, event=self.bird_event
        )



    def create_title_image(self):
        self._background.create_image(self._width // 2, self._height * self.title_scaled_pos_y,
                                      image=self._title_image)

    def create_menu_buttons(self):
        """
        Create menu buttons including START and EXIT
        """

        width = int(self._width * self.button_scaled_width)

        # Create a Button object for start_button
        start_button = Button(
            master=self,  # 按钮的父容器
            image=self._start_button_image,
            command=self.start,  # 按钮被点击时,执行该方法
            bd=0,  # 按钮边框大小,默认为2
            cursor=self.button_cursor,  # 鼠标放上去时的变化
            bg=self.button_bg,  # 按钮背景色
            activebackground=self.button_activebackground  # 当鼠标放上去时，按钮的背景色
        )

        # Place the start_button in background (Canvas)
        self._buttons.append(self._background.create_window((self._width // 2) - width // 1.5,
                                                            int(self._height * self.button_scaled_pos_y),
                                                            window=start_button))

        # Create a Button object for exit_button
        exit_button = Button(
            master=self,
            image=self._exit_button_image,
            command=self.close,
            bd=0,
            cursor=self.button_cursor,
            bg=self.button_bg,
            activebackground=self.button_activebackground
        )

        # Place the exit_button in background (Canvas)
        self._buttons.append(self._background.create_window((self._width // 2) + width // 1.5,
                                                            int(self._height * self.button_scaled_pos_y),
                                                            window=exit_button))

    def delete_menu_buttons(self):
        """
        Delete all menu buttons
        """

        for button in self._buttons:
            self._background.delete(button)

        self._buttons.clear()

    def create_scoreboard(self):
        """
        Create Scoreboard image in background
        """

        x = self._width // 2
        y = int(self._height * self.scoreboard_scaled_pos_y)

        scoreboard_w = int(self._width * self.scoreboard_scaled_width)
        scoreboard_h = int(self._height * self.scoreboard_scaled_height)

        # Location of last game score
        score_x = x - scoreboard_w * 0.3
        score_y = y + scoreboard_h * 0.05

        # Location of best score
        bestscore_x = x + scoreboard_w * 0.175
        bestscore_y = y + scoreboard_h * 0.05

        # Location of time
        time_x = x
        time_y = y + scoreboard_h * 0.25

        # Scoreboard font
        font = (self.scoreboard_font, int(0.02 * self._width + 0.5))

        # Create image for scoreboard in background
        self._background.create_image(x, y, image=self._scoreboard_image)

        self._background.create_text(
            score_x, score_y, text=f"Score: {self._score}", fill=self.scoreboard_fill, font=font
        )

        self._background.create_text(
            bestscore_x, bestscore_y, text=f"Best Score: {self._bestscore}", fill=self.scoreboard_fill, font=font
        )

        self._background.create_text(
            time_x, time_y, text=f"Time: {self._time}", fill=self.scoreboard_fill, font=font
        )

    def start(self, event=None):
        """
        Start the game
        Argument event should be kept
        """

        # Run this method only if _playing=False
        if self._playing:
            return

        self._playing = True

        # Reinitialize score and time
        self._score = 0
        self._time = time.time()

        # Remove menu buttons
        self.delete_menu_buttons()

        # Reset background
        self._background.reset()

        if self.background_animation:
            self._background.run()

        self._bird = Bird(
            self._background, self.gameover, self.bird_fp, self._width, self._height,
            descend_speed=self._bird_descend_speed, event=self.bird_event
        )

        self._tubes = Tubes(
            self._background, self._bird, self._width, self._height, score_function=self.increase_score,
            tube_body_fp=self.tube_fp[0], tube_mouth_fp=self.tube_fp[1],
            animation_speed=self._background_animation_speed
        )

        self._bird.start()
        self._tubes.start()

    def close(self, event=None):
        """
        Exit the Game
        Argument event should be kept
        """

        # Save socre
        self.save_score()

        try:
            self._background.stop()
            self._bird.kill()
            self._tubes.stop()
        finally:
            quit()

    def change_fullscreen_option(self, event=None):
        self.window_fullscreen = not self.window_fullscreen
        self.attributes("-fullscreen", self.window_fullscreen)

    def increase_score(self):
        """
        Add one score, and update best score if needed
        """

        self._score += 1

        if self._score > self._bestscore:
            self._bestscore = self._score

    def load_score(self):

        try:
            with open(self.bestscore_fp) as fin:
                self._bestscore = int(fin.read(), 16)
        except IOError:
            with open(self.bestscore_fp, 'w') as fout:
                fout.write(hex(self._bestscore))

    def save_score(self):
        with open(self.bestscore_fp, 'w') as fout:
            fout.write(hex(self._bestscore))

    def gameover(self):

        self._time = int(time.time() - float(self._time))
        self._time = str(
            datetime.timedelta(seconds=self._time))  # A kind of formating, use str to get the formatted time

        self._background.stop()
        self._tubes.stop()

        # Set _playing=False
        # 否则,按下Enter的时候,self.start()不会被运行,背景不被重置,依旧会动,并且会叠加
        self._playing = False

        self.create_menu_buttons()
        self.create_title_image()
        self.create_scoreboard()


if __name__ == '__main__':
    try:
        app = App()
        app.initialize()
        app.mainloop()

    except FileNotFoundError as e:
        print(e)
