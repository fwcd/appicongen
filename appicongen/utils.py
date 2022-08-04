from decimal import Decimal
from fractions import Fraction
from typing import Union

def to_decimal(x: Union[int, Fraction]) -> Decimal:
    if isinstance(x, Fraction):
        return Decimal(x.numerator) / Decimal(x.denominator)
    else:
        return Decimal(x)
