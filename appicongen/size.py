from dataclasses import dataclass
from fractions import Fraction
from typing import Optional, Union

from appicongen.utils import to_decimal

@dataclass
class IconSize:
    idiom: str
    size: Union[int, Fraction]
    scale: int
    aspect_ratio: Union[int, Fraction] = 1
    platform: Optional[str] = None
    subtype: Optional[str] = None
    role: Optional[str] = None

    @property
    def scaled_size(self) -> int:
        return int(self.size * self.scale)

    @property
    def scaled_width(self) -> int:
        return int(self.width * self.scale)

    @property
    def scaled_height(self) -> int:
        return int(self.height * self.scale)

    @property
    def width(self) -> Union[int, Fraction]:
        return self.size * self.aspect_ratio

    @property
    def height(self) -> Union[int, Fraction]:
        return self.size

    @property
    def size_str(self) -> str:
        width = to_decimal(self.width)
        height = to_decimal(self.height)
        return f'{width}x{height}'

    @property
    def scale_str(self) -> str:
        return f'{self.scale}x'

    @property
    def bigsurifiable(self) -> bool:
        return self.idiom == 'mac'

    def filename(self, bigsurify: bool=False) -> str:
        suffix = 'b' if bigsurify and self.bigsurifiable else ''
        return f'{self.scaled_width}x{self.scaled_height}{suffix}.png'

    def __str__(self) -> str:
        return f'{self.size_str} ({self.scale}x)'

ICON_SIZES = {
    'ios': [
        IconSize(idiom='universal', platform='ios', size=1024, scale=1),
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
    'tvos': [
        IconSize(idiom='tv', size=240, aspect_ratio=Fraction(10, 6), scale=1),
        IconSize(idiom='tv', size=240, aspect_ratio=Fraction(10, 6), scale=2),
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
        IconSize(idiom='watch', size=54, scale=2, role='appLauncher', subtype='49mm'),
        IconSize(idiom='watch', size=86, scale=2, role='quickLook', subtype='38mm'),
        IconSize(idiom='watch', size=98, scale=2, role='quickLook', subtype='42mm'),
        IconSize(idiom='watch', size=108, scale=2, role='quickLook', subtype='44mm'),
        IconSize(idiom='watch', size=117, scale=2, role='quickLook', subtype='45mm'),
        IconSize(idiom='watch', size=129, scale=2, role='quickLook', subtype='49mm'),
        IconSize(idiom='watch-marketing', size=1024, scale=1),
    ]
}
