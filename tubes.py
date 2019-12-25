# -*- coding: utf-8 -*-

"""
Tubes class
Created on 2019/12/22 
"""

__author__ = "Yihang Wu"

import random
from threading import Thread

from background import Background
from bird import Bird
from utils import get_photo_image


class Tubes(Thread):
    """
    Class for tubes
    """

    _distance = 0
    _move = 10  # move steps
    _past_tubes = []

    def __init__(self, background, bird, screen_width, screen_height, score_function,
                 tube_body_fp, tube_mouth_fp, animation_speed):

        # Arguments Checking
        if not isinstance(background, Background):
            raise TypeError("Argument background must be an instance of Background.")

        if not isinstance(bird, Bird):
            raise TypeError("Argument bird must be an instance of Bird")

        if not callable(score_function):
            raise TypeError("Argument score_function must be a callable object")

        Thread.__init__(self)

        # Instance parameters
        self._background = background
        self._bird_w = bird.width
        self._bird_h = bird.height

        self._width = screen_width
        self._height = screen_height

        self._score_method = score_function
        self._animation_speed = animation_speed

        self._image_w = int(0.1 * self._width)
        self._image_h = int(0.05 * self._height)

        # Create a list for tube body
        self._tube_body_images = []

        self.tube_mouth_image = get_photo_image(
            image_path=tube_mouth_fp, width=self._image_w, height=self._image_h, close_after=True
        )[0]

        # Get the tube body image, which is not a PhotoImage
        self.tube_body_image = get_photo_image(
            image_path=tube_body_fp, width=self._image_w, height=self._image_h
        )[1]

        # Minimum distance between two tubes
        self._min_distance = int(self._image_w * 4.5)

        self._stop = False
        self._tubes = []

    def create_tubes_pair(self):
        """
        Create a pair of tubes in the same x position
        """

        self._tube_body_images.append([])

        # Tube --- Top
        # A list for body of top tubes
        top_tube = []

        x = self._width + self._image_w

        # Position y of the mouth of top tube
        y = random.randint(self._image_h // 2, self._height - self._image_h - (self._bird_h * 2))

        # Mouth of top tubes
        top_tube.append(self._background.create_image(x, y, image=self.tube_mouth_image))

        # Create a new images in _tube_images[-1] representing the body of top tube
        # whose height is the distance between ceiling and the center of the mouth of top tubes
        self._tube_body_images[-1].append(get_photo_image(image=self.tube_body_image, width=self._image_w, height=y)[0])

        # Position y of the body of top tube
        y_body = (y - self._image_h) // 2  # Do some math

        # Body of top tube
        top_tube.append(self._background.create_image(x, y_body, image=self._tube_body_images[-1][0]))

        # ------------------------------------------------------
        # ------------------------------------------------------

        # Tube --- Bottom
        bottom_tube = []

        # Position y of the mouth of bottom tube
        y += self._bird_h * 2 + self._image_h

        # Mouth of bottom tube
        bottom_tube.append(self._background.create_image(x, y, image=self.tube_mouth_image))

        # Create a new images in _tube_images[-1] representing the body of bottom tube
        self._tube_body_images[-1].append(
            get_photo_image(image=self.tube_body_image, width=self._image_w, height=self._height - y)[0])

        # Position y of body of bottom tube
        y_body = (self._height + y + self._image_h) // 2  # Just do some math

        # Body of buttom tube
        bottom_tube.append(self._background.create_image(x, y_body, image=self._tube_body_images[-1][1]))

        # Append this pair of tubes to self._tubes
        self._tubes.append([top_tube, bottom_tube])

        # Set the distance to 0
        self._distance = 0

    def move(self):
        """
        Move tubes
        """

        # Record whether this pair of tubes have been passed and increased score
        scored = False

        for tubes in self._tubes:
            for tube in tubes:

                # If this pair of tubes haven't scored, check if we should score it
                if not scored:

                    # Coordinate x2 of the mouth of top tube
                    t_x2 = self._background.bbox(tube[0])[2]

                    # Coordinate x1 of the bird
                    b_x1 = (self._width - self._bird_w) / 2

                    # If the bird will pass the tubes at this move...
                    if b_x1 - self._move < t_x2 <= b_x1:

                        if tube[0] not in self._past_tubes:
                            self._score_method()
                            self._past_tubes.append(tube[0])
                            scored = True

                for part in tube:
                    self._background.move(part, -self._move, 0)

    def run(self) -> None:
        if self._stop:
            return

        # Eliminate the tubes that are out from left side
        # check if x2 of the left-most top tube's mouth is smaller than 0
        if len(self._tubes) > 0 and self._background.bbox(self._tubes[0][0][0])[2] <= 0:
            # print(self._tubes) -> shape = [n, 2, 2]
            # [
            #   [[60, 61], [62, 63]],
            #   [[64, 65], [66, 67]],
            #   [[69, 70], [71, 72]]
            # ]

            # print(self._tube_images) -> shape = [n, 2]

            for tube in self._tubes[0]:
                for part in tube:
                    self._background.delete(part)

            self._tube_body_images.remove(self._tube_body_images[0])  #

            self._tubes.remove(self._tubes[0])

            self._past_tubes.remove(self._past_tubes[0])

        # Whether to create a pair of tubes or not
        if self._distance >= self._min_distance:
            self.create_tubes_pair()
        else:
            self._distance += self._move

        self.move()
        self._background.after(self._animation_speed, self.run)

    def stop(self):
        self._stop = True

    def resume(self):
        self._stop = False
        self.run()
