# -*- coding: utf-8 -*-

"""
Bird class
Created on 2019/12/22 
"""

__author__ = "Yihang Wu"

from threading import Thread

from .background import Background
from .utils import get_photo_image


class Bird(Thread):
    """
    Class for a Bird
    """

    _tag = "Bird"
    _alive = None  # denote the bird is alive
    _going_up = False  # denote whether the bird is going up
    _going_down = 0  # accumulate the going down value, the bird would move down by "_going_down" per descend_speed
    _times_skipped = 0  # accumulate a value, which would record the times that the bird climbs
    _stop = True  # indicate whether the method run() is stopped, that means whether bird is automatically descending

    scaled_max_descend = 0.0038  # A scaled value of maximum descend length (per time unit)
    # 在每一个descend_speed(ms)里,鸟最多下降多少距离(/屏幕宽度),数值越大,鸟的最大下降速度越大

    scaled_max_climb = 0.0911  # A scaled value of maximum climb length

    # 当鸟执行一次跳跃动作时,它会上升多少距离(/屏幕宽度),e.g.数值为0.5,每次跳跃都会跳半屏的距离

    def __init__(self, background, gameover_function, fp, screen_width, screen_height,
                 descend_speed, climb_speed=3, jump_event="<Up>", jump_event_2='<space>', immortal=False):

        # Type Check
        if not isinstance(background, Background):
            raise TypeError("Argument background must be an instance of Background.")
        if not callable(gameover_function):
            raise TypeError("Argument gameover_function must be callable")

        self._canvas = background
        self.gameover_method = gameover_function
        self.image_path = fp
        self._width = screen_width
        self._height = screen_height
        self._descend_speed = descend_speed
        self._climb_speed = climb_speed
        self._immortal = immortal

        # Set decends and climbs according to window width
        self.max_descend = int(self.scaled_max_descend * self._height + 0.5)
        self.max_climb = int(self.scaled_max_climb * self._height + 0.5)

        # Call the contruct function of Thread
        Thread.__init__(self)

        # Set the size (width, height) of the bird according to window size
        self.width = (self._width // 100) * 6
        self.height = (self._height // 100) * 11

        # Create the bird in background
        self._canvas.bird_image = get_photo_image(image_path=self.image_path, width=self.width, height=self.height,
                                                  close_after=True)[0]
        self._bird_id = self._canvas.create_image(self._width // 2, self._height // 2,
                                                  image=self._canvas.bird_image, tag=self._tag)

        # Define a event that raise the bird
        self._canvas.focus_force()  # ?
        self._canvas.bind(jump_event, self.jumps)
        self._canvas.bind(jump_event_2, self.jumps)

        # Set _alive to be True
        self._alive = True

    def check_collision(self):
        """
        Check if the bird is out of window or hitting something
        """

        # Get the position of bird [x1, y1, x2, y2]
        position = list(self._canvas.bbox(self._tag))

        # If the bird gets out of the window, it dies
        if position[1] <= -20 or position[3] >= self._height + 20:
            self._alive = False

        # Set a error value to each coordinate, in case it dies too precisely
        position[0] += int(0.33 * self.width)
        position[1] += int(0.25 * self.height)
        position[2] -= int(0.26 * self.width)
        position[3] -= int(0.13 * self.height)

        # Set some irrelevant collision object
        ignored_collisions = []
        ignored_collisions.extend(self._canvas.get_background_id())
        ignored_collisions.append(self._bird_id)

        # Check if collide
        possible_collisions = list(self._canvas.find_overlapping(*position))
        for item in ignored_collisions:
            try:
                possible_collisions.remove(item)
            except ValueError:
                continue
        if len(possible_collisions) > 0:
            self._alive = False

        return not self._alive

    def jumps(self, event=None):
        """
        Bird jumps
        This method will be called when the certain key (<Up>) is pressed
        """

        # Immortal Option
        if not self._immortal:
            self.check_collision()

        # If the bird died, return
        if not self._alive or self._stop:
            self._going_up = False
            return

        # Set signal
        self._going_up = True
        self._going_down = 0

        # Move up the bird until exceed the limit
        if self._times_skipped < self.max_climb:

            self._canvas.move(self._tag, 0, -1)
            self._times_skipped += 1

            # Execute this function again
            self._canvas.after(self._climb_speed, self.jumps)  # A kind of sensitivity
        else:
            self._going_up = False
            self._times_skipped = 0

    def start(self) -> None:
        self._stop = False
        super().start()

    def run(self) -> None:
        """
        Method to descend the bird
        """

        if not self._stop:

            # Immortal Option
            if self._immortal:
                position = list(self._canvas.bbox(self._tag))
                if position[3] >= self._height + 20:
                    self._canvas.after(self._descend_speed, self.run)
                    return
            else:
                self.check_collision()

            if self._going_down < self.max_descend:
                self._going_down += 0.05

            if self._alive:
                if not self._going_up:
                    self._canvas.move(self._tag, 0, self._going_down)

                # Execute this funciton again
                self._canvas.after(self._descend_speed, self.run)
            else:
                self._stop = True
                self.gameover_method()

    def kill(self):
        """
        Kill the bird
        """

        self._alive = False

    def alive(self) -> bool:
        return self._alive

    def tag(self):
        return self._tag

    def stop(self):
        self._stop = True

    def resume(self):
        self._stop = False
        self.run()
