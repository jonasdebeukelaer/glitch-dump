import numpy as np
from internal import tools


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
