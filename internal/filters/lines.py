import numpy as np
import random
from internal.tools import display_percentage
from internal.tools import wrap


def rand_linify(img: np.array) -> np.array:
    r_line_factor = int(random.random() * 16 + 0.5)
    r_lean = int(random.random()**2 * 4) * (-1)**(int(random.random()*2))
    r_separate_colours = random.random() > 0.7
    r_allow_line_merging = random.random() > 0.8
    r_left = random.random() > 0.7
    r_straight = random.random() > 0.8

    return linify(img, r_separate_colours, r_line_factor, r_lean, r_allow_line_merging, r_left, r_straight)


def linify(img, separate_colours=False, line_factor=4, lean=0, allow_line_merging=False, left_only=False, straight_only=False):
    if line_factor == 0:
        line_factor = 1

    args = locals()
    del args["img"]
    print("args: ", args)

    new_img = np.zeros(img.shape)

    colour_map = {0: "red", 1: "blue", 2: "green", 3: "???"}

    number_of_lines = int(1.0 * img.shape[1] / line_factor) - 1

    gradient_array = np.zeros((img.shape[0], img.shape[1] - 1, img.shape[2]))
    img_temp = img[:, 1:, :]
    gradient_array = img[:, :-1, :] - img_temp

    img_width = img.shape[1]-2

    for colour in range(0, 2):
        offset = colour if separate_colours else (line_factor / 2)

        previous_positions = np.zeros((img.shape[0]))
        previous_positions = [x * line_factor + 1 for x in range(0, number_of_lines)]
        new_img[0, 2::line_factor, :] = img[0, 2::line_factor, :]
        for i in range(1, img.shape[0]):
            # lean = -lean
            display_percentage("running linify for colour %s... " % colour_map[colour], i, img.shape[0])
            for j in range(0, number_of_lines):
                direction = 0
                if left_only:
                    if gradient_array[i, wrap(img_width-1, previous_positions[j]), colour] - gradient_array[i, wrap(img_width-1, previous_positions[j]-1), colour] > lean:
                        direction = 1
                else:
                    if straight_only:
                        gradient_direction = gradient_array[i, wrap(img_width-1, previous_positions[j]), colour] - int(gradient_array[i, wrap(img_width-1, previous_positions[j]-1), colour])
                        if gradient_direction > lean:
                            direction = 1
                        elif gradient_direction < lean:
                            direction = -1
                    else:

                        direction = int(gradient_array[i, wrap(img_width-1, previous_positions[j]), colour] - int(gradient_array[i, wrap(img_width-1, previous_positions[j]-1), colour])/500)

                if separate_colours:
                    new_img[i, wrap(img_width, previous_positions[j]+direction), colour] = img[i, wrap(img_width, previous_positions[j]+direction), colour]
                else:
                    if straight_only:
                        new_img[i, wrap(img_width, previous_positions[j]+direction), 0] = img[i, wrap(img_width, previous_positions[j]+direction), 0]
                        new_img[i, wrap(img_width, previous_positions[j]+direction), 1] = img[i, wrap(img_width, previous_positions[j]+direction), 1]
                        new_img[i, wrap(img_width, previous_positions[j]+direction), 2] = img[i, wrap(img_width, previous_positions[j]+direction), 2]
                    else:
                        new_img[i, previous_positions[j]:wrap(img_width, previous_positions[j]+direction), 0] = img[i, wrap(img_width, previous_positions[j]+direction), 0]
                        new_img[i, previous_positions[j]:wrap(img_width, previous_positions[j]+direction), 1] = img[i, wrap(img_width, previous_positions[j]+direction), 1]
                        new_img[i, previous_positions[j]:wrap(img_width, previous_positions[j]+direction), 2] = img[i, wrap(img_width, previous_positions[j]+direction), 2]

                if allow_line_merging or previous_positions[wrap(number_of_lines - 1, j + 1)] > previous_positions[j]:
                    previous_positions[j] += direction
                    previous_positions[j] = wrap(img_width, previous_positions[j])

    return new_img
