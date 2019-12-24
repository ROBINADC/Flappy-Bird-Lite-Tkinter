# -*- coding: utf-8 -*-

"""
Class - Background
run() - make the background moving
Created on 2019/12/22
"""

__author__ = "Yihang Wu"

from tkinter import Tk, Canvas

from utils import get_photo_image


class Background(Canvas):
    _background = []  # list for background id
    _stop = False  # indicate if the background is still rather than moving

    def __init__(self, tk_instance, width, height, fp, animation_speed=50):

        if not isinstance(tk_instance, Tk):
            raise TypeError('Argument "tk_instance" must be an instance of Tk')

        self._width = width
        self._height = height

        self.image_path = fp
        self.animation_speed = animation_speed

        # The construction function of Canvas
        Canvas.__init__(self, master=tk_instance, width=self._width, height=self._height)

        # Background image
        self._background_image = \
            get_photo_image(image_path=self.image_path, width=self._width, height=self._height, close_after=True)[0]

        # Create a default (static) background
        self._background_default = self.create_image(self._width // 2, self._height // 2, image=self._background_image)
        # Canvas.create_image(x, y, anchor, image)
        # default anchor is CENTER, which means the CENTER point of iamge would be placed at x, y (here, center)
        # return id of that image

        # Create dynamic background
        self._background.append(self.create_image(self._width // 2, self._height // 2, image=self._background_image))
        self._background.append(
            self.create_image(self._width + (self._width // 2), self._height // 2, image=self._background_image))

    def run(self):
        """
        Activate background animation
        """

        if not self._stop:
            self.move(self._background[0], -10, 0)
            self.move(self._background[1], -10, 0)
            # Canvas.move(PhotoImage, x, y) move PhotoImage x indent along x-axis and y indent along y-axis
            self.tag_lower(self._background[0])
            self.tag_lower(self._background[1])
            self.tag_lower(self._background_default)
            # self.tag_lower move the object to the lower level of canvas. 将图片移到最底下的图层 ??

            if self.bbox(self._background[0])[2] <= 0:
                # Delete the image that left beyond the vision
                self.delete(self._background[0])
                self._background.remove(self._background[0])

                width = self.bbox(self._background[0])[2] + self._width // 2
                self._background.append(self.create_image(width, self._height // 2, image=self._background_image))

            # execute this function every period of time
            self.after(self.animation_speed, self.run)

    def reset(self):
        """
        Reset the background
        """

        # delete all items in canvas
        self.delete("all")

        self._stop = False

        # Remove all items from list - self._background
        self._background.clear()

        # Redo create background
        self._background_default = self.create_image(self._width // 2, self._height // 2, image=self._background_image)

        self._background.append(self.create_image(self._width // 2, self._height // 2, image=self._background_image))
        self._background.append(
            self.create_image(self._width + (self._width // 2), self._height // 2, image=self._background_image))

    def stop(self):
        self._stop = True

    def get_background_id(self):
        """
        Return backgrounds' ID in order to ignore collision with them
        """
        return [self._background_default, *self._background]
