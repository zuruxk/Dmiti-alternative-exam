from rational_algebra.Rational import Rational
from rational_algebra.Natural import Natural
from rational_algebra.Integer import Integer

def TRANS_INT_Q(I:int):
    one_natural = Natural(0, [1])
    arr_numbers = [int(char) for char in str(I) if char.isdigit()]
    if I<0:
        return Rational(Integer(1,len(arr_numbers)-1, arr_numbers), one_natural)
    return Rational(Integer(0, len(arr_numbers) - 1, arr_numbers), one_natural)