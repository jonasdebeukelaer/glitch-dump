import math
import numpy as np

from internal.filters.cutoff import mid_pass
from internal.filters import line_contrast, lines


def gaussian_blur(img, sigma=5):
    print("Running Gaussian blur...")
    f_img_red = np.fft.rfft2(img[:, :, 0], axes=(0, 1))
    f_img_blue = np.fft.rfft2(img[:, :, 1], axes=(0, 1))
    f_img_green = np.fft.rfft2(img[:, :, 2], axes=(0, 1))

    g_shape = img.shape
    mu_x = int((g_shape[0]) / 2)
    mu_y = int((g_shape[1]) / 2)

    gaussian = [
        [
            (1.0 / (2 * math.pi * sigma ** 2))
            * math.exp((-1.0) * ((i - mu_y) ** 2 + (j - mu_x) ** 2) / (2 * sigma ** 2))
            for i in range(g_shape[1])
        ]
        for j in range(g_shape[0])
    ]
    gaussian = np.array(gaussian)
    f_gaussian = np.fft.rfft2(gaussian, axes=(0, 1))

    blurred_img = np.zeros(img.shape)
    blurred_img[:, :, 0] = np.fft.irfft2(f_img_red * f_gaussian)
    blurred_img[:, :, 1] = np.fft.irfft2(f_img_blue * f_gaussian)
    blurred_img[:, :, 2] = np.fft.irfft2(f_img_green * f_gaussian)
    blurred_img = np.fft.fftshift(blurred_img, axes=(0, 1))

    gaussian3 = np.zeros(img.shape)
    gaussian3[:, :, 0] = gaussian
    gaussian3[:, :, 1] = gaussian
    gaussian3[:, :, 2] = gaussian

    blurred_img = 255.0 * blurred_img / blurred_img.max(initial=0)
    return blurred_img


def selective_blur(img, splits=2, cutoff=127, sigma=5):
    print("Running Selective blur...")
    interval = int(1.0 * 255 / splits)

    truth1 = mid_pass(img, 0, cutoff - 1)
    truth2 = mid_pass(img, cutoff, 256)
    img1 = np.array(img)
    img2 = np.array(img)
    img1[not truth1] = 0

    img1 = lines.linify(
        img1, separate_colours=False, line_factor=2, lean=1, allow_line_merging=False
    )
    img1 = line_contrast.affectOnLineContrast(
        img1,
        contrast=50,
        span=5,
        vertical=True,
        randomise=False,
        ifContrastLessThan=True,
    )
    img1 = gaussian_blur(img1, sigma=sigma)

    final_img = np.array(img1)
    final_img[not truth1] = img2[not truth1]

    return final_img
