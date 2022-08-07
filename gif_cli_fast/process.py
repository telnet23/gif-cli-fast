from itertools import groupby
from io import BytesIO
from PIL import GifImagePlugin, Image, ImageSequence

import py256color


class _Ascii:
    @staticmethod
    def pre(color):
        red, green, blue = color
        # These are the characters and weights used in jp2a by default
        # https://manpages.ubuntu.com/manpages/bionic/man1/jp2a.1.html
        characters = "   ...',;:clodxkO0KXNWM"
        intensity = (0.2989 * red + 0.5866 * green + 0.1145 * blue) / 255
        return characters[round(intensity * (len(characters) - 1))]

    @staticmethod
    def post(key, length):
        return key * length

    reset = ""


class _256Color:
    @staticmethod
    def pre(color):
        return py256color.from_rgb(*color)

    @staticmethod
    def post(key, length):
        return f"\x1B[48;5;{key:d}m" + " " * length

    reset = "\x1B[m"


class _TrueColor:
    @staticmethod
    def pre(color):
        return color

    @staticmethod
    def post(key, length):
        red, green, blue = key
        return f"\x1B[48;2;{red:d};{green:d};{blue:d}m" + " " * length

    reset = "\x1B[m"


_PROCESSORS = {
    "ascii": _Ascii,
    "256color": _256Color,
    "truecolor": _TrueColor,
}


def process(content, size, mode):
    GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS
    image = Image.open(BytesIO(content))

    imsize = image.size[0] * 2, image.size[1]
    scale = min(size[0] / imsize[0], size[1] / imsize[1], 1)
    imsize = int(scale * imsize[0]), int(scale * imsize[1])

    processor = _PROCESSORS[mode]

    return [
        (
            "\n".join(
                "".join(
                    (
                        "".join(
                            processor.post(key, len(list(streak)))
                            for key, streak in groupby(
                                processor.pre(color) for color in row
                            )
                        ),
                        processor.reset,
                    )
                )
                for row in _matrix(frame.resize(imsize).getdata(), imsize[0])
            ),
            frame.info["duration"] / 1000,
        )
        for frame in ImageSequence.Iterator(image)
    ]


def _matrix(iterable, length):
    args = [iter(iterable)] * length
    return zip(*args)
