import numpy as np
import random
from internal import tools
from internal.tools import wrap


def rand_affect_on_line_contrast(img: np.array) -> np.array:
    r_contrast = int(random.random() * 50)
    r_span = int(random.random() * 20)
    r_vertical = random.random() > 0.3
    r_randomise = random.random() > 0.8
    r_if_contrast_less_than = random.random() > 0.7

    return affect_on_line_contrast(img, r_contrast, r_span, r_vertical, r_randomise, r_if_contrast_less_than)


def affect_on_line_contrast(img, contrast=10, span=10, vertical=False, randomise=False, less_than=True):
    if vertical:
        img = np.swapaxes(img, 0, 1)
    new_img = np.asarray(img[:])
    y_max = img.shape[0]-1
    x_max = img.shape[1]-1

    for y in range(0, y_max):
        tools.display_percentage("running outlines... ", y, y_max)
        for x in range(span, x_max-span):
            max_val = 0
            min_val = 255
            avg = 0
            for i in range(x-span, x+span):
                if max(img[y, i, 0:2]) > max_val:
                    max_val = max(img[y, i, 0:2])
                elif min(img[y, i, 0:2]) < min_val:
                    min_val = min(img[y, i, 0:2])
                avg += img[y, i, 0]

            avg /= (span * 2 + 1)

            if less_than == ((max_val - min_val) < contrast):
                if randomise:
                    rand_y = int(y - (span / 2) + random.random() * span)
                    new_red = get_rand_colour_from_y_span(img, rand_y, x, y_max, 0)
                    new_green = get_rand_colour_from_y_span(img, rand_y, x, y_max, 1)
                    new_blue = get_rand_colour_from_y_span(img, rand_y, x, y_max, 2)
                else:
                    new_red = int(1. * (int(img[wrap(y_max, y), wrap(x_max, x-1), 0]) + int(img[wrap(y_max, y), wrap(x_max-1, x-2), 0]) + int(img[wrap(y_max, y), wrap(x_max, x+1), 0]) + int(img[wrap(y_max, y), wrap(x_max, x+2), 0])) / 4)
                    new_green = int(1. * (int(img[wrap(y_max, y), wrap(x_max, x-1), 1]) + int(img[wrap(y_max, y), wrap(x_max-1, x-2), 1]) + int(img[wrap(y_max, y), wrap(x_max, x+1), 1]) + int(img[wrap(y_max, y), wrap(x_max, x+2), 1])) / 4)
                    new_blue = int(1. * (int(img[wrap(y_max, y), wrap(x_max, x-1), 2]) + int(img[wrap(y_max, y), wrap(x_max-1, x-2), 2]) + int(img[wrap(y_max, y), wrap(x_max, x+1), 2]) + int(img[wrap(y_max, y), wrap(x_max, x+2), 2])) / 4)

                if new_red > 10 or new_green > 10 or new_blue > 10:
                    if img.shape[2] == 4:
                        new_img[y][max(x-span, 0):min(x+span, x_max)][:] = [new_red, new_green, new_blue, 255]
                    else:
                        new_img[y][max(x-span, 0):min(x+span, x_max)][:] = [new_red, new_green, new_blue]

    if vertical:
        new_img = np.swapaxes(new_img, 0, 1)

    return new_img


def get_rand_colour_from_y_span(img, rand_y, x, y_max, colour_number):
    return int(img[min(rand_y, y_max-1), x, colour_number])


