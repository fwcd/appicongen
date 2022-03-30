import argparse

from dataclasses import dataclass

@dataclass
class IconSize:
    size: int
    scale: int

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
    'ios-marketing': [
        IconSize(size=1024, scale=1),
    ],
}

def main():
    parser = argparse.ArgumentParser(description='Tool for generating macOS/iOS app icons')

    for idiom in ICON_SIZES.keys():
        parser.add_argument(f'--{idiom}', action='store_true', help=f'Generate icons for the {idiom} idiom')

    args = parser.parse_args()
    arg_dict = vars(args)
    idioms = sorted(idiom.replace('_', '-') for idiom, enabled in arg_dict.items() if enabled)
    
    if not idioms:
        print('Defaulting to all idioms...')
        idioms = sorted(ICON_SIZES.keys())
    
    for idiom in idioms:
        print(f'==> Generating icons for the {idiom} idiom...')
        print(ICON_SIZES[idiom.replace('_', '-')])

