from dataclasses import dataclass
from fractions import Fraction
from typing import Optional, Union

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
