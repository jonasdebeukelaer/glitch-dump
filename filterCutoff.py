import numpy as np


def high_pass(img, cutoff):
    print("running highpass...")
    img = mid_pass(img, cutoff, 256)

    return img


def low_pass(img, cutoff):
    print("running lowPass...")
    img = mid_pass(img, 0, cutoff)

    return img


def mid_pass(img, cutoff_lower, cutoff_higher):
    print("running midPass...")

    mag_img = (np.amax(img, axis=2)).astype(int)

    cut = np.ones(mag_img.shape)
    cut[mag_img < cutoff_lower] = 0
    cut[mag_img > cutoff_higher] = 0

    return cut.astype(bool)
