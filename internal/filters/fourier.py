import random
from math import sqrt
from internal import tools
import numpy as np


def fourier_effect(img, steps):
    f_img = np.fft.rfft2(img, axes=(0, 1))
    new_f_img = f_img
    
    y_max = f_img.shape[0]
    x_max = f_img.shape[1]
    print("")
    for y in range(0, y_max):
        tools.display_percentage("running Fourier stuff... ", y, y_max)
        for x in range(0, x_max):
            new_f_img[y, x, 0] = f_img[y, x][0].real * sqrt(abs(x - (x_max/2))) + f_img[y, x][0].imag
            new_f_img[y, x, 1] = f_img[y, x][1].real * sqrt(abs(x - (x_max/2))) + f_img[y, x][1].imag
            new_f_img[y, x, 2] = f_img[y, x][2].real * sqrt(abs(x - (x_max/2))) + f_img[y, x][2].imag
            for index, step in enumerate(steps):
                if x % step == 0:
                    new_f_img[y][x][index] = 0

    new_img = np.real(np.fft.irfft2(new_f_img, axes=(0, 1)))
    return new_img


def rand_blur_2d(img: np.array) -> np.array:
    r_blur_accent = int(150 * random.random() + 50)
    return blur_2d(img, r_blur_accent, process="gaussian")


def blur_2d(img: np.array, gaussian_accent=0.4, process="gaussian") -> np.array:
    if len(img.shape) == 2: 
        return blur_2d_monochrome(img, gaussian_accent, process)
    else:
        img0 = blur_2d_monochrome(img[:, :, 0], gaussian_accent, process)
        img1 = blur_2d_monochrome(img[:, :, 1], gaussian_accent, process)
        img2 = blur_2d_monochrome(img[:, :, 2], gaussian_accent, process)
        new_img = np.dstack([img0, img1, img2])
        return new_img


def blur_2d_monochrome(img, gaussian_accent, process):
    print("")
    img = tools.monochrome(img)
    f_img = np.fft.rfft2(img, axes=(0, 1))

    kernel = create_kernel(img.shape, gaussian_accent, process)
    f_kernel = np.fft.rfft2(kernel, axes=(0, 1))

    new_f_img = (f_kernel * f_img)

    new_img = np.real(np.fft.irfft2(new_f_img, axes=(0, 1)))
    return np.fft.ifftshift(new_img)


def create_kernel(img_shape, gaussian_accent, process):
    x_ = int(img_shape[0]/2+1)
    y_ = int(img_shape[1]/2+1)
    kernel = np.zeros(img_shape)

    for xIndex, x in enumerate(kernel):
        tools.display_percentage("running %s blur... " % process, xIndex, img_shape[0])
        for yIndex, y in enumerate(x):

            kernel[xIndex, yIndex] = gaussian_2d(xIndex, yIndex, x_, y_, gaussian_accent)

    return kernel


def gaussian_2d(x, y, x_, y_, accent):
    square_x = (1.*(x-x_)/x_)**2
    square_y = (1.*(y-y_)/y_)**2
    return np.exp(-accent * (square_x + square_y)**0.5)
