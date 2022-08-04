from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

def open_image(path: Path) -> Image.Image:
    return Image.open(path)

def generate_icon(input_img: Image.Image, output_path: Path, width: int, height: int, bigsurify: bool=False):
    if bigsurify:
        assert width == height, "Bigsurify is currently only supported for quadratic icons!"
        size = width
        rect_size = int(size * 0.8)
        rect_offset = (size - rect_size) // 2
        corner_radius = int(size * 0.175)

        # Paste a scaled and rounded-corner version of the image
        with Image.new('L', (rect_size, rect_size)) as mask:
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, rect_size, rect_size), fill=255, radius=corner_radius)
            with input_img.copy() as base_img:
                base_img.thumbnail((rect_size, rect_size), Image.LANCZOS)
                with Image.new(base_img.mode, (size, size)) as img: # pyright: ignore[reportGeneralTypeIssues]
                    img.paste(base_img, (rect_offset, rect_offset), mask)
                    img.save(output_path)
    else:
        # Just crop and scale the image
        with input_img.copy() as img:
            with ImageOps.fit(img, (width, height), Image.LANCZOS) as thumb_img:
                thumb_img.save(output_path)
