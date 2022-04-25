import numpy as np
import random

from internal.tools import display_percentage


def rand_misalign(img: np.array) -> np.array:
    r_segments = int(random.random() * 16 + 5)
    r_horizontal = random.random() > 0.3
    r_max_shift_percent = 20 + 80 * random.random()

    return misalign(
        img,
        segments=r_segments,
        horizontal=r_horizontal,
        max_shift_percent=r_max_shift_percent,
    )


def misalign(
    img, segments: int = 11, horizontal: bool = True, max_shift_percent: int = 20
):
    args = locals()
    del args["img"]
    print("args: ", args)

    if not horizontal:
        np.swapaxes(img, 0, 1)

    remainder = img.shape[0] % segments

    new_img = img[: (img.shape[0] - remainder), :, :]

    img_segments = np.split(new_img, segments, axis=0)
    last_segment = img[(img.shape[0] - remainder) :, :, :]

    img_segments.append(last_segment)
    max_shift = max_shift_percent * img.shape[0] / 100

    for i, seg in enumerate(img_segments):
        display_percentage("running misalign... ", i, segments)
        shift = int(max_shift * random.random() * 2 - max_shift)
        img_segments[i] = np.roll(seg, shift)

    collected_segments = np.concatenate(img_segments, axis=0)

    return collected_segments if horizontal else np.swapaxes(collected_segments, 1, 0)
