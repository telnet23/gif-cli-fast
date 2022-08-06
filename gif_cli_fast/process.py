from io import BytesIO
from PIL import GifImagePlugin, Image, ImageSequence

import py256color


def _ascii(r, g, b):
    # These are the characters and weights used in jp2a by default
    # https://manpages.ubuntu.com/manpages/bionic/man1/jp2a.1.html
    CHARS = "   ...',;:clodxkO0KXNWM"
    return CHARS[round((0.2989 * r + 0.5866 * g + 0.1145 * b) / 255 * (len(CHARS) - 1))]


def _256color(r, g, b):
    return "\x1B[48;5;{:d}m ".format(py256color.from_rgb(r, g, b))


def _truecolor(r, g, b):
    return f"\x1B[48;2;{r:d};{g:d};{b:d}m "


_PROCESSORS = {
    "ascii": _ascii,
    "256color": _256color,
    "truecolor": _truecolor,
}


def process(content, size, mode):
    GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS
    image = Image.open(BytesIO(content))

    imsize = image.size[0] * 2, image.size[1]
    scale = min(size[0] / imsize[0], size[1] / imsize[1], 1)
    imsize = int(scale * imsize[0]), int(scale * imsize[1])

    processor = _PROCESSORS[mode]

    home = "" if mode == "ascii" else "\x1B[H"
    end = "\n" if mode == "ascii" else "\x1B[0m\n"

    return [
        [
            "".join(
                (
                    home,
                    "".join(
                        "".join(
                            (processor(*color), end if index % -imsize[0] == -1 else "")
                        )
                        for index, color in enumerate(frame.resize(imsize).getdata())
                    ),
                )
            ),
            frame.info["duration"] / 1000,
        ]
        for frame in ImageSequence.Iterator(image)
    ]
