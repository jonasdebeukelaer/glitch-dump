import numpy as np
import random
from PIL import Image
import argparse

import tools
import filter1
import filterFourier
import filterLines
import filterBlur
import filterCutoff
import filterWave


class Glitcher:

    def __init__(self, filename: str):
        self.filename = filename
        self.img = Image.open(f"source/{filename}")
        self.image_array = np.array(self.img)

    def gif_glitch(self):
        img = self.img
        i = 0
        my_palette = img.getpalette()
        gif_images = []
        try:
            while i+1:
                img.putpalette(my_palette)
                new_im = Image.new("RGBA", img.size)
                new_im.paste(img)
                image_array = np.array(new_im)
                image_array = image_array[:, :, :-1]
                # image_array = filter1.increaseContrast(image_array, factor=1.8)
                image_array = filterLines.linify(image_array, separate_colours=False, line_factor=4, lean=1, allow_line_merging=True)
                image_array = filter1.affect_on_line_contrast(image_array, contrast=150, span=8, vertical=True, randomise=True, less_than=False)
                gif_images.append(image_array)
                i += 1
                img.seek(img.tell() + 1)

        except EOFError:
            pass  # end of sequence
        tools.save_new_gif(gif_images, self.filename)

    def img_to_gif_glitch(self, range_max):
        img_list = []
        for i in range(0, range_max):
            print("")
            print("creating img {}".format(i))

            v_cutoff = int(255 - abs(255 - ((1.0*i/range_max)*510)))
            v_sigma = max(0.01, 10 - abs(10 - (1.0*20*i/range_max)))

            print("params: v_cutoff %i, v_sigma %i" % (v_cutoff, v_sigma))

            new_image_array = filterBlur.selective_blur(self.image_array, splits=2, cutoff=v_cutoff, sigma=v_sigma)
            img_list.append((new_image_array+0.5).astype(int))

        tools.save_new_gif(img_list, self.filename)

    # gif_glitch("source/%s.gif" % (file_name))
    # img_to_gif_glitch(image_array, 60)

    def img_to_img(self):
        image_array = np.array(self.image_array)

        # remove any alpha channels, so image doesn't just come out transparent when saved again, since we apply effects
        # on all channels in the same way
        # TODO: figure out best way to deal with alpha channel
        if len(image_array.shape) == 4:
            image_array = image_array[:, :, 0:-1]

        colour_mapping = [[186,   0,   0],
                         [240, 227, 227],
                         [37,  163, 70]]
        for i in range(0, 40):
            print("creating img {}".format(i))
            image_array = np.array(self.image_array)

            r_contrast_factor = 1 + random.random() + 1
            r_line_factor = int(random.random() * 16 + 0.5)
            r_lean = int(random.random()**2 * 4) * (-1)**(int(random.random()*2))
            r_separate_colours = random.random() > 0.7
            r_allow_line_merging = random.random() > 0.8
            r_left = random.random() > 0.7
            r_straight = random.random() > 0.8

            r_contrast = int(random.random() * 200)
            r_span = int(random.random() * 5)
            r_vertical = random.random() > 0.3
            r_randomise = random.random() > 0.8
            r_if_contrast_less_than = random.random() > 0.7

            r_thickness = int(2 + random.random() * 3)
            r_line_count = int(20 + random.random() * 150)
            r_overlap = int(random.random() * 4 + 3)
            r_wave_vertical = random.random() > 0.5

            image_array = filter1.mixup(image_array)
            image_array = filterWave.wavify(image_array, line_count=r_line_count, thickness=r_thickness,
                                            overlap=r_overlap, vertical=r_wave_vertical)
            image_array = filterFourier.blur_2d(image_array, gaussian_accent=200, process="antialiase")
            image_array = filterLines.linify(image_array, r_separate_colours, r_line_factor, r_lean,
                                             r_allow_line_merging, r_left, r_straight)
            # image_array = filterWave.wavify(image_array, lineCount=r_lineCount, thickness=r_thickness,
            #                                 overlap=r_overlap, vertical=r_waveVertical)
            # image_array = filter1.spreadPrimaryColours(image_array, colour_mapping)

            # image_array = filterFourier.blur2D(image_array, gaussianAccent=600, process="antialiase")

            tools.save_new_file(image_array, self.filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Glitch some pics!')
    parser.add_argument('filename', type=str, default=None, help='source image filename')
    args = parser.parse_args()

    g = Glitcher(args.filename)
    g.img_to_img()

# img_to_gif_glitch(image_array, 50)
