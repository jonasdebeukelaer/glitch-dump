import numpy as np
import random
import tools
from tools import wrap


def affect_on_line_contrast(img, contrast=10, span=10, vertical=False, randomise=False, less_than=True):
    if vertical:
        img = np.swapaxes(img, 0, 1)
    new_img = np.asarray(img[:])
    y_max = img.shape[0]-1
    x_max = img.shape[1]-1
    print("")
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


def mixup(img):
    weight = 0.4
    cutoff = 100
    y_max = img.shape[0]
    x_max = img.shape[1]
    new_img = img
    for y in range(0, y_max):
        tools.display_percentage("running mixup... ", y, y_max)
        for x in range(0, x_max):
            if img[y, x, 2] < cutoff and img[y, x, 1] < cutoff:
                new_x = int(((x + img[y, x, 2]) * 2) % x_max)

                new_img[y, new_x][:] = ((1.0 - weight) * img[y, x][:] + weight * img[y, new_x][:])
                new_img[y, x][:] = (weight * img[y, x][:] + (1.0 - weight) * img[y, new_x][:])

    return new_img


def increase_contrast(img, factor=2):
    print("")
    new_img = (img - np.mean(img))**factor

    return new_img


def spread_primary_colours(img, mapping):
    print("")
    mapping_array = np.array(mapping, dtype='float32')
    for x in range(0, 3):
        mapping_array[x] = np.array(mapping_array[x]) * 1. / np.sum(mapping_array[x])

    for i, row in enumerate(img):
        tools.display_percentage("running spread_primary_colours... ", i, img.shape[0])

        for j, element in enumerate(row):
            img[i, j] = mapping_array.dot(img[i, j])

    return np.array(img) * 255. / np.sum(img)
