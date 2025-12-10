from rational_algebra.Polynomial import Polynomial
from .TRANS_INT_Q import TRANS_INT_Q


def TRANS_STR_P(s: str):
    # Определяем знак
    power = 1
    if s[0] == '-':
        positive = False
        q = TRANS_INT_Q(-1)
        s = s[1:]
    else:
        positive = True
        q = TRANS_INT_Q(1)
        s = s[1:]
    q_arr = [q]
    # Обрабатываем степень
    if '^' in s:
        # Формат x^n
        power = int(s.split('^')[1])
        for i in range(power):
            q_arr.append(TRANS_INT_Q(0))

    else:
        q_arr.append(TRANS_INT_Q(0))
        power = 1

    return Polynomial(power, q_arr)