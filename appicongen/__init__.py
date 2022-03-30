import argparse

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional, Union

@dataclass
class IconSize:
    size: Union[int, Fraction]
    scale: int
    subtype: Optional[str] = None
    role: Optional[str] = None

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

