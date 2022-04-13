import argparse
import json
import shutil
import sys

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from PIL import Image, ImageDraw
from typing import Optional, Union

if sys.version_info < (3, 9):
    print('Python version >= 3.9 is required!')
    exit(1)

@dataclass
class IconSize:
    idiom: str
    size: Union[int, Fraction]
    scale: int
    subtype: Optional[str] = None
    role: Optional[str] = None

    def scaled_size(self) -> int:
        return int(self.size * self.scale)
    
    def filename(self) -> str:
        return f'{self.scaled_size()}.png'

    def size_str(self) -> str:
        size = self.size
        if isinstance(size, Fraction):
            size = float(size)
        return f'{size}x{size}'
    
    def scale_str(self) -> str:
        return f'{self.scale}x'

    def __str__(self) -> str:
        return f'{self.size_str()} ({self.scale}x)'

ICON_SIZES = {
    'ios': [
        IconSize(idiom='iphone', size=20, scale=2),
        IconSize(idiom='iphone', size=20, scale=3),
        IconSize(idiom='iphone', size=29, scale=2),
        IconSize(idiom='iphone', size=29, scale=3),
        IconSize(idiom='iphone', size=40, scale=2),
        IconSize(idiom='iphone', size=40, scale=3),
        IconSize(idiom='iphone', size=60, scale=2),
        IconSize(idiom='iphone', size=60, scale=3),
        IconSize(idiom='ipad', size=20, scale=1),
        IconSize(idiom='ipad', size=20, scale=2),
        IconSize(idiom='ipad', size=29, scale=1),
        IconSize(idiom='ipad', size=29, scale=2),
        IconSize(idiom='ipad', size=40, scale=1),
        IconSize(idiom='ipad', size=40, scale=2),
        IconSize(idiom='ipad', size=76, scale=2),
        IconSize(idiom='ipad', size=Fraction('83.5'), scale=2),
        IconSize(idiom='ios-marketing', size=1024, scale=1),
    ],
    'macos': [
        IconSize(idiom='mac', size=16, scale=1),
        IconSize(idiom='mac', size=16, scale=2),
        IconSize(idiom='mac', size=32, scale=1),
        IconSize(idiom='mac', size=32, scale=2),
        IconSize(idiom='mac', size=128, scale=1),
        IconSize(idiom='mac', size=128, scale=2),
        IconSize(idiom='mac', size=256, scale=1),
        IconSize(idiom='mac', size=256, scale=2),
        IconSize(idiom='mac', size=512, scale=1),
        IconSize(idiom='mac', size=512, scale=2),
    ],
    'watchos': [
        IconSize(idiom='watch', size=24, scale=2, role='notificationCenter', subtype='38mm'),
        IconSize(idiom='watch', size=Fraction('27.5'), scale=2, role='notificationCenter', subtype='42mm'),
        IconSize(idiom='watch', size=29, scale=2, role='companionSettings'),
        IconSize(idiom='watch', size=29, scale=3, role='companionSettings'),
        IconSize(idiom='watch', size=33, scale=2, role='notificationCenter', subtype='45mm'),
        IconSize(idiom='watch', size=40, scale=2, role='appLauncher', subtype='38mm'),
        IconSize(idiom='watch', size=44, scale=2, role='appLauncher', subtype='40mm'),
        IconSize(idiom='watch', size=46, scale=2, role='appLauncher', subtype='41mm'),
        IconSize(idiom='watch', size=50, scale=2, role='appLauncher', subtype='44mm'),
        IconSize(idiom='watch', size=51, scale=2, role='appLauncher', subtype='45mm'),
        IconSize(idiom='watch', size=86, scale=2, role='quickLook', subtype='38mm'),
        IconSize(idiom='watch', size=98, scale=2, role='quickLook', subtype='42mm'),
        IconSize(idiom='watch', size=108, scale=2, role='quickLook', subtype='44mm'),
        IconSize(idiom='watch', size=117, scale=2, role='quickLook', subtype='45mm'),
        IconSize(idiom='watch-marketing', size=1024, scale=1),
    ]
}

def generate_icon(input_img: Image, output_path: Path, size: int, bigsurify: bool=False):
    if bigsurify:
        rect_size = int(size * 0.8)
        rect_offset = (size - rect_size) // 2
        corner_radius = int(size * 0.175)

        # Paste a scaled and rounded-corner version of the image
        with Image.new('L', (rect_size, rect_size)) as mask:
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, rect_size, rect_size), fill=255, radius=corner_radius)
            with input_img.copy() as base_img:
                base_img.thumbnail((rect_size, rect_size), Image.LANCZOS)
                with Image.new(base_img.mode, (size, size)) as img:
                    img.paste(base_img, (rect_offset, rect_offset), mask)
                    img.save(output_path)
    else:
        # Just scale the image
        with input_img.copy() as img:
            img.thumbnail((size, size), Image.LANCZOS)
            img.save(output_path)

def confirm(prompt: str):
    answer = input(f'{prompt} [y/n] ')
    if answer.lower() != 'y':
        print('Exiting')
        exit(0)

def main():
    # Parse CLI arguments

    parser = argparse.ArgumentParser(description='Tool for generating macOS/iOS app icons')

    for template in ICON_SIZES.keys():
        parser.add_argument(f'--{template}', action='store_true', help=f'Generate icons for the {template} template')

    parser.add_argument('-a', '--all', action='store_true', help='Generate icons for all idioms')
    parser.add_argument('-o', '--output', default='./AppIcon.appiconset', help='Path to the output appiconset bundle.')
    parser.add_argument('-m', '--manifest-name', default='Contents.json', help='Name of the manifest (should generally not be changed).')
    parser.add_argument('-b', '--bigsurify', action='store_true', help='Cut out a rounded-rectangle shape in the style of a macOS Big Sur icon (useful in conjunction with --macos).')
    parser.add_argument('input', help='Path to the input image (a 1024x1024 PNG image is recommended)')

    args = parser.parse_args()
    arg_dict = vars(args)

    # Prepare paths

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    print(f'==> (Re)creating {output_path} if needed...')
    if output_path.exists():
        if not output_path.is_relative_to(Path.cwd()):
            confirm(f'The output path is outside your current working dir and will be deleted, are you sure?')
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True)

    # Resolve templates and (distinct) icon sizes

    templates = {template for template in ICON_SIZES.keys() if args.all or arg_dict[template.replace('-', '_')]}
    size_files = {size.filename(): size.scaled_size() for template in templates for size in ICON_SIZES[template]}

    if not templates:
        print('==> No templates specified, thus not generating any icons (use --all to generate all)')
    
    # Generate scaled icons
    
    print('==> Generating scaled icons...')
    with Image.open(input_path) as input_img:
        for filename, scaled_size in size_files.items():
            generate_icon(input_img, output_path / filename, scaled_size, args.bigsurify)
    
    # Generate manifest

    print('==> Generating manifest')
    manifest = {
        'images': [{
            'size': size.size_str(),
            'expected-size': str(size.scaled_size()),
            'filename': size.filename(),
            'idiom': size.idiom,
            'scale': size.scale_str(),
        } for template in templates for size in ICON_SIZES[template]]
    }
    with open(output_path / args.manifest_name, 'w') as f:
        f.write(json.dumps(manifest, indent=2))
    
    # Print summary

    print('==> Summary')
    for template in templates:
        sizes = ICON_SIZES[template]
        print(f'Generated {len(sizes)} {template} icon(s):')
        for size in sizes:
            print(f'  {str(size)}')
