import argparse
import json
import shutil
import sys

from pathlib import Path

from appicongen.imaging import AVAILABLE_RESIZE_MODES, DEFAULT_RESIZE_MODE, find_mean_color, generate_icon, open_image
from appicongen.size import ICON_SIZES

if sys.version_info < (3, 9):
    print('Python version >= 3.9 is required!')
    exit(1)

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
    parser.add_argument('-r', '--resize-mode', default=DEFAULT_RESIZE_MODE, choices=AVAILABLE_RESIZE_MODES, help='Resize mode (only relevant for non-quadratic icons).')
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
    size_files = {size.filename: (size.scaled_width, size.scaled_height) for template in templates for size in ICON_SIZES[template]}

    if not templates:
        print('==> No templates specified, thus not generating any icons (use --all to generate all)')
    
    # Generate scaled icons
    
    print('==> Generating scaled icons...')
    with open_image(input_path) as input_img:
        bg_color = find_mean_color(input_img)
        for filename, (scaled_width, scaled_height) in size_files.items():
            generate_icon(
                input_img=input_img,
                output_path=output_path / filename,
                width=scaled_width,
                height=scaled_height,
                resize_mode=args.resize_mode,
                bg_color=bg_color,
                bigsurify=args.bigsurify
            )
    
    # Generate manifest

    print('==> Generating manifest')
    manifest = {
        'images': [{k: v for k, v in {
            'size': size.size_str,
            'expected-size': str(size.scaled_size),
            'filename': size.filename,
            'idiom': size.idiom,
            'scale': size.scale_str,
            'role': size.role,
            'subtype': size.subtype,
        }.items() if v} for template in templates for size in ICON_SIZES[template]]
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
