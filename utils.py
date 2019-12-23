# -*- coding: utf-8 -*-

"""
This is used to 
refer:
Created on 2019/12/22 
"""

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
