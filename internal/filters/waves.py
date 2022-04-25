import random
import numpy as np
from math import sin, pi
from internal.tools import wrap, display_percentage


def rand_wavify_lin(img: np.array) -> np.array:
    r_thickness = int(2 + random.random() * 3)
    r_line_count = int(20 + random.random() * 150)
    r_overlap = int(random.random() * 4 + 3)
    r_type = "vertical" if (random.random() > 0.5) else "horizontal"

    return wavify(img, r_line_count, r_thickness, r_overlap, r_type)


def rand_wavify_circle(img: np.array) -> np.array:
    scale = img.shape[0]

    r_thickness = int(15 + random.random() * 0.1 * scale)
    r_line_count = int(20 + random.random() * 0.1 * scale)
    r_overlap = int(random.random() * 4 + 20)

    return wavify_circle(img, r_line_count, r_thickness, r_overlap)


def wavify_constant_wave(
    img, line_count, thickness=1, overlap=0, constant_wave_count=10
) -> np.array:
    return wavify_do(
        img,
        line_count,
        thickness,
        overlap,
        constant_wave=True,
        constant_wave_count=constant_wave_count,
    )


def wavify(img, line_count, thickness=1, overlap=0, type="vertical") -> np.array:
    if type == "vertical":
        img = np.swapaxes(img, 0, 1)
        img = wavify_do(img, line_count, thickness, overlap)
        img = np.swapaxes(img, 0, 1)
    elif type == "horizontal":
        img = wavify_do(img, line_count, thickness, overlap, constant_wave=False)
    elif type == "circle":
        img = wavify_circle(img, line_count, thickness, overlap)

    return img


def wavify_do(
    img, line_count, thickness=1, overlap=0, constant_wave=False, constant_wave_count=0
) -> np.array:
    args = locals()
    del args["img"]
    print("args: ", args)

    sparseness = int(1.0 * img.shape[0] / line_count)

    if len(img.shape) == 2:
        return wavify_monochrome(
            img, sparseness, thickness, overlap, 0, constant_wave, constant_wave_count
        )
    else:
        img0 = wavify_monochrome(
            img[:, :, 0],
            sparseness,
            thickness,
            overlap,
            0,
            constant_wave,
            constant_wave_count,
        )
        img1 = wavify_monochrome(
            img[:, :, 1],
            sparseness,
            thickness,
            overlap,
            0,
            constant_wave,
            constant_wave_count,
        )
        img2 = wavify_monochrome(
            img[:, :, 2],
            sparseness,
            thickness,
            overlap,
            0,
            constant_wave,
            constant_wave_count,
        )
        img = np.dstack([img0, img1, img2])
        return img


def wavify_monochrome(
    img, sparseness, thickness, overlap, offset, constant_wave, constant_wave_count
) -> np.array:
    print("")
    img = img.astype(np.float)

    h_line_shape = img.shape[1]
    blank_h_line = np.zeros(h_line_shape)

    line_img = np.array(
        [sparsify(x, sparseness, i, blank_h_line, offset) for i, x in enumerate(img)]
    )

    wavy_img = np.zeros(line_img.shape)
    line_img = line_img * 1.0 / np.max(line_img)

    max_index = [wavy_img.shape[0] - 1, wavy_img.shape[1] - 1]

    for i, row in enumerate(line_img):
        display_percentage("running wavify... ", i, img.shape[0])
        if (i - offset) % sparseness != 0:
            continue

        for j, element in enumerate(row):
            if not constant_wave:
                new_y_index = wrap(
                    max_index[0], (i + verticalise(sparseness, element, overlap))
                )
            else:
                wavelength = int(1.0 * max_index[1] / constant_wave_count)
                new_y_index = wrap(
                    max_index[0],
                    (i + sin_verticalise(sparseness, element, overlap, j, wavelength)),
                )

            for x in range(0, thickness):
                wavy_img[wrap(max_index[0], new_y_index + x), j] = 255

    return wavy_img


def sparsify(x, sparseness, index, blank_h_line, offset) -> int:
    if (index - offset) % sparseness == 0:
        return x
    else:
        return blank_h_line


def verticalise(sparseness, brightness, overlap) -> int:
    if (brightness - 0.5) * sparseness * (1 + overlap) == "NaN":
        print(sparseness)
        print(brightness)
        print(overlap)
    return -int((brightness - 0.5) * sparseness * (1 + overlap))


def sin_verticalise(sparseness, brightness, overlap, j, wavelength) -> int:
    vanilla_sine_wave = sin(2.0 * pi * j / wavelength)
    return -int((brightness - 0.5) * sparseness * (1 + overlap) * vanilla_sine_wave)


def wavify_circle(
    img: np.array, line_count: int, thickness: int, overlap: int
) -> np.array:
    args = locals()
    del args["img"]
    print("args: ", args)

    new_img = np.zeros(img.shape)
    if img.shape[2] == 4:
        new_img[:, :, 3] = img[:, :, 3]

    x_bar = int(img.shape[0] / 2)
    y_bar = int(img.shape[1] / 2)
    sparseness = int((x_bar + y_bar) / line_count)

    pixel_thickness = thickness * sparseness / 100

    if sparseness < 1:
        raise ValueError(
            "ratio of img res to line_count is too low, resulting sparseness = 0"
        )

    for x, row in enumerate(img):
        display_percentage("running wavify_circle... ", x, img.shape[0])
        for y, px in enumerate(row):
            if on_concentric_circle(x, y, x_bar, y_bar, sparseness, pixel_thickness):
                split_colours = True

                if split_colours:
                    new_x, new_y = new_coords(
                        x, y, x_bar, y_bar, px[0], sparseness, overlap
                    )
                    new_img[new_x, new_y, 0] = px[0]
                    new_x, new_y = new_coords(
                        x, y, x_bar, y_bar, px[1], sparseness, overlap
                    )
                    new_img[new_x, new_y, 1] = px[1]
                    new_x, new_y = new_coords(
                        x, y, x_bar, y_bar, px[2], sparseness, overlap
                    )
                    new_img[new_x, new_y, 2] = px[2]
                else:
                    px_bar = np.average(px)
                    new_x, new_y = new_coords(
                        x, y, x_bar, y_bar, px_bar, sparseness, overlap
                    )
                    new_img[new_x, new_y, 0] = px[0]
                    new_img[new_x, new_y, 1] = px[1]
                    new_img[new_x, new_y, 2] = px[2]

    return new_img


def on_concentric_circle(
    x: int, y: int, x_bar: int, y_bar: int, sparseness: int, thickness: int
) -> bool:
    n = np.sqrt((x - x_bar) ** 2 + (y - y_bar) ** 2)
    lim = int(thickness / 2 + 0.5)

    return int(n) % sparseness in range(-lim, lim)


# provide new x and y coordinates, given the value of the pixel
def new_coords(
    x: int, y: int, x_bar: int, y_bar: int, value: int, sparseness: int, overlap: int
) -> (int, int):
    if x == x_bar and y == y_bar:
        return x, y

    # if overlap:
    #     dist = value * 0.1 # figure out
    # else:
    dist = (value - 128) / 256 * sparseness * (1 + overlap)

    x_c = x - x_bar
    y_c = y - y_bar

    abs_denom = abs(x_c) + abs(y_c)

    dx = (x_c / abs_denom) * dist
    dy = (y_c / abs_denom) * dist

    return wrap(x_bar * 2, int(x + dx)), wrap(y_bar * 2, int(y + dy))
