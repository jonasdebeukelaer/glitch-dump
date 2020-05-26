import numpy as np
from internal import tools


def rand_spread_colours(img: np.array) -> np.array:
    rand_mapping = np.random.rand(3, 3) * 200 + 40
    return spread_primary_colours(img, rand_mapping)


def spread_primary_colours(img: np.array, mapping_array: np.array) -> np.array:
    for x in range(0, 3):
        mapping_array[x] = np.array(mapping_array[x]) * 1. / np.sum(mapping_array[x])

    for i, row in enumerate(img):
        tools.display_percentage("running spread_primary_colours... ", i, img.shape[0])

        for j, element in enumerate(row):
            img[i, j] = mapping_array.dot(img[i, j])

    return np.array(img) * 255. / np.max(img)
