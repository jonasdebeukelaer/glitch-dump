import sys
import time
import numpy as np

from PIL import Image
import imageio


# convert to black & white if it's not already
def monochrome(img):
    if len(img.shape) == 3:
        img = np.sum(img, axis=2).astype(np.float)
    else:
        img = img.astype(np.float)
    return img * 255. / np.max(img)


# wrap pixels around edges of the image
def wrap(max_position: int, position: int):
    if position > max_position:
        return position - max_position
    elif position < 0:
        return max_position + position
    else:
        return position


def display_percentage(msg: str, i: int, total: int):
    progress = i / (1. * total)
    bar_length = 20  # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(bar_length*progress))
    text = msg + "\r[{0}] {1}% {2}".format("="*block + " "*(bar_length-block), int(progress*100), status)
    sys.stdout.write(text)
    sys.stdout.flush()


def save_new_gif(gif_images, file_name: str):
    print("")
    print("renormalise and save...")
    file_name = "%s_%s" % (file_name, time.strftime("%y-%m-%d %H_%M_%S"))
    gif_images = [255. * image_array / image_array.max() for image_array in gif_images]

    imageio.mimsave(f"pic_archive/{file_name}.gif", gif_images, fps=24)


def save_new_file(image_array, file_name: str):
    print("")
    print("renormalise and save...")
    image_array = 255. * image_array / image_array.max()

    file_name = "%s_%s" % (file_name, time.strftime("%y-%m-%d, %H:%M:%S"))

    file = Image.fromarray(image_array.astype('uint8'))
    file.save(f"pic_archive/{file_name}.png")
