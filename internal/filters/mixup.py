from internal import tools
import numpy as np
import random


def rand_mixup(img) -> np.array:
    r_weight = random.random()
    r_cutoff = 40 + random.random() * 200
    return mixup(img, r_weight, r_cutoff)


def mixup(img: np.array, weight: float, cutoff: int) -> np.array:
    y_max = img.shape[0]
    x_max = img.shape[1]
    new_img = img
    for y in range(0, y_max):
        tools.display_percentage("running mixup... ", y, y_max)
        for x in range(0, x_max):
            if img[y, x, 2] < cutoff and img[y, x, 1] < cutoff:
                new_x = int(((x + img[y, x, 2]) * 2) % x_max)

                new_img[y, new_x][:] = (1.0 - weight) * img[y, x][:] + weight * img[
                    y, new_x
                ][:]
                new_img[y, x][:] = (
                    weight * img[y, x][:] + (1.0 - weight) * img[y, new_x][:]
                )

    return new_img
