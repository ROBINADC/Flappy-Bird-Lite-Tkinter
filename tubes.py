# -*- coding: utf-8 -*-

"""
This is used to 
refer:
Created on 2019/12/22 
"""

import random
from threading import Thread

from background import Background
import PIL.Image
from PIL.ImageTk import PhotoImage

__author__ = "Yihang Wu"


class Tubes(Thread):
    """
    Class for tubes
    """

    _distance = 0
    _move = 10
    _past_tubes = []

    def __init__(self):
        pass