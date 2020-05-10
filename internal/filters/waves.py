import numpy as np
from math import sin, pi
from internal.tools import wrap, display_percentage


def wavify_constant_wave(img, line_count, thickness=1, overlap=0, constant_wave_count=10):
    return wavify_do(img, line_count, thickness, overlap, constant_wave=True, constant_wave_count=constant_wave_count)


def wavify(img, line_count, thickness=1, overlap=0, vertical=False):
    if vertical:
        img = np.swapaxes(img, 0, 1)
    img = wavify_do(img, line_count, thickness, overlap, constant_wave=False)
    return np.swapaxes(img, 0, 1)


def wavify_do(img, line_count, thickness=1, overlap=0, constant_wave=False, constant_wave_count=0):
    print("")
    args = locals()
    del args["img"]
    print("args: ", args)

    sparseness = int(1.0 * img.shape[0] / line_count)

    if len(img.shape) == 2:
        return wavify_monochrome(img, sparseness, thickness, overlap, 0, constant_wave, constant_wave_count)
    else:
        img0 = wavify_monochrome(img[:, :, 0], sparseness, thickness, overlap, 0, constant_wave, constant_wave_count)
        img1 = wavify_monochrome(img[:, :, 1], sparseness, thickness, overlap, 0, constant_wave, constant_wave_count)
        img2 = wavify_monochrome(img[:, :, 2], sparseness, thickness, overlap, 0, constant_wave, constant_wave_count)
        img = np.dstack([img0, img1, img2])
        return img


def wavify_monochrome(img, sparseness, thickness, overlap, offset, constant_wave, constant_wave_count):
    print("")
    img = img.astype(np.float)

    h_line_shape = img.shape[1]
    blank_h_line = np.zeros(h_line_shape)

    line_img = np.array([sparsify(x, sparseness, i, blank_h_line, offset) for i, x in enumerate(img)])

    wavy_img = np.zeros(line_img.shape)
    line_img = line_img * 1. / np.max(line_img)

    max_index = [wavy_img.shape[0]-1, wavy_img.shape[1]-1]

    for i, row in enumerate(line_img):
        display_percentage("running wavify... ", i, img.shape[0])
        if (i - offset) % sparseness != 0:
            continue

        for j, element in enumerate(row):
            if not constant_wave:
                new_y_index = wrap(max_index[0], (i + verticalise(sparseness, element, overlap)))
            else:
                wavelength = int(1. * max_index[1] / constant_wave_count)
                new_y_index = wrap(max_index[0], (i + sin_verticalise(sparseness, element, overlap, j, wavelength)))

            for x in range(0, thickness):
                wavy_img[wrap(max_index[0], new_y_index + x), j] = 255

    return wavy_img


def sparsify(x, sparseness, index, blank_h_line, offset):
    if (index - offset) % sparseness == 0:
        return x
    else:
        return blank_h_line


def verticalise(sparseness, brightness, overlap):
    if (brightness-0.5) * sparseness * (1+overlap) == 'NaN':
        print(sparseness)
        print(brightness)
        print(overlap)
    return -int((brightness-0.5) * sparseness * (1+overlap))


def sin_verticalise(sparseness, brightness, overlap, j, wavelength):
    vanilla_sine_wave = sin(2. * pi * j / wavelength)
    return -int((brightness-0.5) * sparseness * (1+overlap)) * vanilla_sine_wave
