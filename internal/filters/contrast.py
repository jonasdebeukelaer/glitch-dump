import numpy as np


def increase_contrast(img, factor=2):
    new_img = (img - np.mean(img))**factor

    return new_img
