import argparse
import json

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from PIL import Image
from typing import Optional, Union

@dataclass
class IconSize:
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
    'iphone': [
        IconSize(size=20, scale=2),
        IconSize(size=20, scale=3),
        IconSize(size=29, scale=1),
        IconSize(size=29, scale=2),
        IconSize(size=29, scale=3),
        IconSize(size=40, scale=2),
        IconSize(size=40, scale=3),
        IconSize(size=57, scale=1),
        IconSize(size=57, scale=2),
        IconSize(size=60, scale=1),
        IconSize(size=60, scale=2),
    ],
    'ipad': [
        IconSize(size=20, scale=1),
        IconSize(size=20, scale=2),
        IconSize(size=29, scale=1),
        IconSize(size=29, scale=2),
        IconSize(size=40, scale=1),
        IconSize(size=40, scale=2),
        IconSize(size=50, scale=1),
        IconSize(size=50, scale=2),
        IconSize(size=72, scale=1),
        IconSize(size=72, scale=2),
        IconSize(size=76, scale=1),
        IconSize(size=76, scale=2),
        IconSize(size=Fraction('83.5'), scale=2),
    ],
    'ios-marketing': [
        IconSize(size=1024, scale=1),
    ],
    'mac': [
        IconSize(size=16, scale=1),
        IconSize(size=16, scale=2),
        IconSize(size=32, scale=1),
        IconSize(size=32, scale=2),
        IconSize(size=128, scale=1),
        IconSize(size=256, scale=1),
        IconSize(size=256, scale=2),
        IconSize(size=512, scale=1),
        IconSize(size=512, scale=2),
    ],
    'watch': [
        IconSize(size=24, scale=2, subtype='38mm', role='notificationCenter'),
        IconSize(size=Fraction('27.5'), scale=2, subtype='42mm', role='notificationCenter'),
        IconSize(size=29, scale=2, role='companionSettings'),
        IconSize(size=29, scale=3, role='companionSettings'),
        IconSize(size=40, scale=2, subtype='38mm', role='appLauncher'),
        IconSize(size=44, scale=2, subtype='40mm', role='appLauncher'),
        IconSize(size=50, scale=2, subtype='44mm', role='appLauncher'),
        IconSize(size=86, scale=2, subtype='38mm', role='quickLook'),
        IconSize(size=98, scale=2, subtype='42mm', role='quickLook'),
        IconSize(size=108, scale=2, subtype='44mm', role='quickLook'),
    ],
    'watch-marketing': [
        IconSize(size=1024, scale=1),
    ]
}

def generate_icon(input_img: Image, output_path: Path, size: int):
    with input_img.copy() as img:
        img.thumbnail((size, size), Image.LANCZOS)
        img.save(output_path)

def main():
    # Parse CLI arguments

    parser = argparse.ArgumentParser(description='Tool for generating macOS/iOS app icons')

    for idiom in ICON_SIZES.keys():
        parser.add_argument(f'--{idiom}', action='store_true', help=f'Generate icons for the {idiom} idiom')

    parser.add_argument('-a', '--all', action='store_true', help='Generate icons for all idioms')
    parser.add_argument('-o', '--output', default='./AppIcon.appiconset', help='Path to the output appiconset bundle.')
    parser.add_argument('-m', '--manifest-name', default='Contents.json', help='Name of the manifest (should generally not be changed).')
    parser.add_argument('input', help='Path to the input image (a 1024x1024 PNG image is recommended)')

    args = parser.parse_args()
    arg_dict = vars(args)

    # Prepare paths

    input_path = Path(args.input)
    output_path = Path(args.output)

    print(f'==> Creating {output_path} if needed...')
    output_path.mkdir(parents=True, exist_ok=True)

    # Read and aggregate idioms and (distinct) icon sizes

    idioms = {idiom for idiom in ICON_SIZES.keys() if args.all or arg_dict[idiom.replace('-', '_')]}
    size_files = {size.filename(): size.scaled_size() for idiom in idioms for size in ICON_SIZES[idiom]}

    if not idioms:
        print('==> No idioms specified, thus not generating any icons (use --all to generate all)')
    
    # Generate scaled icons
    
    print('==> Generating scaled icons...')
    with Image.open(input_path) as input_img:
        for filename, scaled_size in size_files.items():
            generate_icon(input_img, output_path / filename, scaled_size)
    
    # Generate manifest

    print('==> Generating manifest')
    manifest = {
        'images': [{
            'size': size.size_str(),
            'expected-size': str(size.scaled_size()),
            'filename': size.filename(),
            'idiom': idiom,
            'scale': size.scale_str(),
        } for idiom in idioms for size in ICON_SIZES[idiom]]
    }
    with open(output_path / args.manifest_name, 'w') as f:
        f.write(json.dumps(manifest, indent=2))
    
    # Print summary

    print('==> Summary')
    for idiom in idioms:
        sizes = ICON_SIZES[idiom]
        print(f'Generated {len(sizes)} {idiom} icon(s):')
        for size in sizes:
            print(f'  {str(size)}')
