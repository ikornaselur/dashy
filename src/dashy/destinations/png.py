from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

Resolution = Tuple[int, int]


def generate_png(
    text: List[str],
    *,
    font_name: str = "inconsolata.ttf",
    font_size: int = 32,
    resolution: Resolution = (600, 448),
    output: str = "out.png",
    margin: int = 0,
) -> None:
    image = Image.new("RGB", resolution, (255, 255, 255))
    font = ImageFont.truetype(font_name, font_size)

    ImageDraw.Draw(image).text((margin, margin), "\n".join(text), (0, 0, 0), font=font)

    image.save(output)
