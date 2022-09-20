import numpy as np
import subprocess

from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
from tempfile import NamedTemporaryFile
from typing import Optional

RESAMPLER = Image.LANCZOS
RESIZE_MODES = {
    'fit': lambda img, size, bg: ImageOps.fit(img, size=size, method=RESAMPLER),
    'pad': lambda img, size, bg: ImageOps.pad(img, size=size, color=bg, method=RESAMPLER),
}

AVAILABLE_RESIZE_MODES = sorted(RESIZE_MODES.keys())
DEFAULT_RESIZE_MODE = 'fit'

def open_image(path: Path) -> Image.Image:
    if path.name.endswith('.svg'):
        with NamedTemporaryFile(prefix='appicon-', suffix='.png') as f:
            subprocess.run([
                'inkscape',
                '--export-type', 'png',
                '--export-filename', f.name,
                # TODO: Render different widths directly from svg
                '--export-width', '1024',
                str(path),
            ], check=True)
            img = Image.open(f.name)
            img.load() # Load it now since the tempfile will be deleted
            return img
    else:
        return Image.open(path)

def find_mean_color(img: Image.Image) -> tuple:
    arr = np.asarray(img)
    arr = arr.reshape((-1, arr.shape[-1]))
    mean = np.mean(arr, axis=0).astype(int)
    return tuple(mean)

def generate_icon(
    input_img: Image.Image,
    output_path: Path,
    width: int,
    height: int,
    resize_mode: str=DEFAULT_RESIZE_MODE,
    bg_color: Optional[tuple]=None,
    bigsurify: bool=False
):
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
                base_img.thumbnail((rect_size, rect_size), resample=RESAMPLER)
                with Image.new(base_img.mode, (size, size)) as img: # pyright: ignore[reportGeneralTypeIssues]
                    img.paste(base_img, (rect_offset, rect_offset), mask)
                    img.save(output_path)
    else:
        # Just crop and scale the image
        with input_img.copy() as img:
            with RESIZE_MODES[resize_mode](img, (width, height), bg_color) as thumb_img:
                thumb_img.save(output_path)
