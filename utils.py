# -*- coding: utf-8 -*-

"""
Utilities
Created on 2019/12/22 
"""

import time
from datetime import timedelta

import PIL.Image
from PIL.ImageTk import PhotoImage

__author__ = "Yihang Wu"


def get_photo_image(image=None, image_path=None, width=None, height=None, close_after=False):
    """
    Get (PhotoImage, image_resized, image)
    """

    if not image:
        if not image_path:
            return

        image = PIL.Image.open(image_path)

    if not width:
        width = image.width
    if not height:
        height = image.height

    # Resize the image
    image_resized = image.resize([width, height])

    # Create a PhotoImage object
    photo_image = PhotoImage(image_resized)

    # If close_after
    if close_after:
        image_resized.close()
        image_resized = None

        image.close()
        image = None

    return photo_image, image_resized, image


class Timer:

    def __init__(self):
        self._start_time = None
        self._last_time = None
        self._pause_time = None
        self._resume_time = None
        self._stop_time = None

        self._accumulated_time = 0

        self._started = False
        self._paused = False
        self._deprecated = False

    def start(self):
        if self._deprecated:
            # raise TypeError("Timer has been deprecated, use clear() to reuse it.")
            self.clear()

        if self._started:
            raise TypeError("Cannot call start() twice")

        self._started = True
        self._start_time = time.time()
        self._last_time = time.time()

    def pause(self):
        if self._deprecated:
            raise TypeError("Timer has been deprecated, use clear() to reuse it.")

        if self._paused:
            raise TypeError("Cannot pause twice without calling resume()")

        if not self._started:
            raise TypeError("Cannot pause without starting")

        self._paused = True
        self._pause_time = time.time()
        self._accumulated_time += self._pause_time - self._last_time

    def resume(self):
        if self._deprecated:
            raise TypeError("Timer has been deprecated, use clear() to reuse it.")

        if not self._paused:
            raise TypeError("Cannot resume without pausing")

        if not self._started:
            raise TypeError("Cannot resume without starting")

        self._paused = False
        self._resume_time = time.time()
        self._last_time = self._resume_time

    def stop(self):
        if self._deprecated:
            raise TypeError("Timer has been deprecated, use clear() to reuse it.")

        if not self._started:
            raise TypeError("Cannot stop without starting")

        self._deprecated = True

        if self._paused:
            self._stop_time = self._pause_time
        else:
            self._stop_time = time.time()
            self._accumulated_time += self._stop_time - self._last_time

    def _gettime(self):
        if not self._started:
            raise TypeError("Cannot get time without starting")

        if self._deprecated or self._paused:
            return self._accumulated_time
        else:
            return self._accumulated_time + time.time() - self._last_time

    def __str__(self):
        return str(timedelta(seconds=int(self._gettime())))

    def clear(self):
        self._start_time = None
        self._last_time = None
        self._pause_time = None
        self._resume_time = None
        self._stop_time = None

        self._accumulated_time = 0

        self._started = False
        self._paused = False
        self._deprecated = False


if __name__ == "__main__":
    _timer = Timer()

    _timer.start()
    time.sleep(2)
    _timer.pause()
    print(str(_timer))  # 2
    _timer.resume()
    time.sleep(4)
    print(str(_timer))  # 6
    time.sleep(6)
    _timer.stop()  # 12
    print(str(_timer))
    _timer.resume()  # raise TypeError
