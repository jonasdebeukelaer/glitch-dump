import os
import argparse

import numpy as np
from PIL import Image

from internal import tools
from internal.filters import (
    contrast,
    cutoff,
    fourier,
    line_contrast,
    lines,
    mixup,
    spread,
    waves,
    misalign,
)


class Glitcher:
    def __init__(self, source_file_path: str, iterations: int, effects: list):
        _, self.filename = os.path.split(source_file_path)
        self.img = Image.open(source_file_path)
        self.image_array = np.array(self.img)
        self.iterations = iterations
        self.effects = effects

    rand_effect_map = {
        "fourier": fourier.rand_blur_2d,
        "line_contrast": line_contrast.rand_affect_on_line_contrast,
        "lines": lines.rand_linify,
        "mixup": mixup.rand_mixup,
        "spread": spread.rand_spread_colours,
        "waves_linear": waves.rand_wavify_lin,
        "waves_circle": waves.rand_wavify_circle,
        "misalign": misalign.rand_misalign,
    }

    # needs fixing
    def gif_to_gif(self):
        img = self.img
        i = 0
        my_palette = img.getpalette()
        gif_images = []
        try:
            while i + 1:
                img.putpalette(my_palette)
                new_im = Image.new("RGBA", img.size)
                new_im.paste(img)
                image_array = np.array(new_im)
                image_array = image_array[:, :, :-1]
                image_array = self.apply_effects(image_array)
                gif_images.append(image_array)
                i += 1
                img.seek(img.tell() + 1)

        except EOFError:
            pass  # end of sequence
        tools.save_new_gif(gif_images, self.filename)

    def img_to_gif(self, range_max):
        img_list = []
        for i in range(0, range_max):
            print("\n")
            print("creating img {}".format(i))

            new_image_array = self.apply_effects(self.image_array)
            img_list.append((new_image_array + 0.5).astype(np.uint8))

        tools.save_new_gif(img_list, self.filename)

    def img_to_img(self):
        image_array = np.array(self.image_array)

        # remove any alpha channels, so image doesn't just come out transparent when saved again, since we apply effects
        # on all channels in the same way
        # TODO: figure out best way to deal with alpha channel
        if len(image_array.shape) == 4:
            image_array = image_array[:, :, 0:-1]

        for i in range(0, self.iterations):
            print("\n-----------------------")
            print("creating img {}".format(i))
            new_img = self.apply_effects(image_array)
            tools.save_new_file(new_img, self.filename + "_" + str(i))

    def apply_effects(self, img: np.array) -> np.array:
        image_array = np.array(img)

        for effect in self.effects:
            print("")
            if effect not in self.rand_effect_map:
                print(f"\nWARNING: effect {effect} not found, skipping")
                continue

            image_array = self.rand_effect_map[effect](image_array)

        return image_array


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Glitch some images, using randomised parameters!"
    )
    parser.add_argument("filepath", type=str, default=None, help="source image path")
    parser.add_argument(
        "-m",
        "--media",
        type=str,
        default="img",
        help="media to output. can be [img, img_gif, gif]",
    )
    parser.add_argument(
        "-gf",
        "--gif_frames",
        type=int,
        default=10,
        help="count of gif frames to generate",
    )
    parser.add_argument(
        "-e",
        "--effects",
        nargs="+",
        type=str,
        help=f"effects to apply. available options: [{list(Glitcher.rand_effect_map.keys())}]",
    )
    parser.add_argument(
        "-i", "--iterations", type=int, default=1, help="number of outputs to create"
    )
    args = parser.parse_args()

    g = Glitcher(args.filepath, args.iterations, args.effects)

    if args.media == "img":
        g.img_to_img()
    elif args.media == "img_gif":
        g.img_to_gif(args.gif_frames)
    elif args.media == "gif":
        g.gif_to_gif()
    else:
        raise ValueError("unrecognised media type")
