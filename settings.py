# -*- coding: utf-8 -*-

"""
Settings class
Created on 2019/12/22
"""

__author__ = "Yihang Wu"

import os
import json


class Settings:
    """

    """

    # Configuration for window
    window_name = "Flappy Bird Lite"
    window_resizable = (False, False)
    window_fullscreen = True
    window_width = None
    window_height = None

    # Configuration for Animation
    background_animation = True

    # Configuration for buttons
    button_scaled_width = 0.22
    button_scaled_height = 0.17
    button_scaled_pos_y = 0.85
    button_bg = "black"
    button_fg = "white"
    button_activebackground = "black"
    button_cursor = "hand2"
    # button_font = ("Impact", 40)

    # Configuration for scoreboard
    scoreboard_scaled_width = 0.40
    scoreboard_scaled_height = 0.40
    scoreboard_scaled_pos_y = 0.50

    # Configuration for scoreboard font
    scoreboard_font = "Impact"
    scoreboard_fill = "White"

    # Configuration for title image
    title_scaled_width = 0.35
    title_scaled_height = 0.15
    title_scaled_pos_y = 0.20


    # Event
    bird_event = '<Up>'
    bird_2_event = '<space>'
    window_fullscreen_event = '<F11>'
    window_start_event = '<Return>'
    window_exit_event = '<Escape>'
    window_pause_event = '<p>'
    window_pause_2_event = '<P>'

    # File Path
    bestscore_fp = 'data/bsc.txt'
    settings_fp = 'data/settings.json'

    background_fp = 'images/background.png'
    bird_fp = 'images/bird.png'
    start_button_fp = 'images/start_button.png'
    exit_button_fp = 'images/exit_button.png'
    tube_fp = ['images/tube_body.png', 'images/tube_mouth.png']
    title_fp = 'images/title.png'
    scoreboard_fp = 'images/scoreboard.png'

    images_fp = [background_fp, bird_fp, start_button_fp, exit_button_fp, tube_fp[0], tube_fp[1], title_fp,
                 scoreboard_fp]

    def set_options(self):
        """
        Get settings from existed json file or create one from default settings
        """

        attributes = ["window_fullscreen", "window_width", "window_height"]

        # from existed file
        try:
            with open(self.settings_fp, 'r') as fin:
                data = json.loads(fin.read())

            for attr in data:
                if attr in attributes or 'event' in attr:
                    setattr(Settings, attr, data[attr])

        # create new one
        except:
            if not os.path.exists(os.path.split(self.settings_fp)[0]):
                os.makedirs(os.path.split(self.settings_fp)[0])

            data = dict()

            for attr in Settings.__dict__:
                if attr in attributes or 'event' in attr:
                    data[attr] = Settings.__dict__[attr]

            with open(self.settings_fp, 'w') as fout:
                fout.write(json.dumps(data, indent=2))


if __name__ == '__main__':
    Settings().set_options()
