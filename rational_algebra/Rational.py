from rational_algebra.Natural import Natural
from rational_algebra.Integer import Integer
#from TRANS.TRANS_N_Z import TRANS_N_Z

def TRANS_N_Z(N):
    """
    Сделала: Имховик Наталья
    Преобразование натурального в целое
    Возвращает целое
    """
    # Формируем положительное целое с полями натурального
    return Integer(0, N.len, N.A[:])


class Rational:
    def __init__(self, numerator, denominator):
        self.numerator = numerator  # Integer числитель
        self.denominator = denominator  # Natural знаменатель

    def RED_Q_Q(self):
        """
        Выполнил: Сурин Максим
        Сокращение дроби
        """
        # Если числитель равен нулю, возвращаем 0/1
        if self.numerator.A == [0]:
            return Rational(Integer(0, 0, [0]), Natural(0, [1]))

        # Получаем абсолютное значение числителя как натуральное число
        abs_numerator = self.numerator.ABS_Z_Z()
        numerator_natural = Natural(abs_numerator.len, abs_numerator.A)

        # Вычисляем НОД числителя и знаменателя
        gcf = numerator_natural.GCF_NN_N(self.denominator)

        # Создаем новый числитель и знаменатель
        new_numerator = self.numerator
        new_denominator = self.denominator

        # Если НОД не равен 1, сокращаем
        if gcf.A != [1]:
            # Делим числитель и знаменатель на НОД
            # Для числителя: преобразуем НОД в целое число и используем целочисленное деление
            new_numerator_abs = numerator_natural // gcf
            new_numerator = Integer(self.numerator.s, new_numerator_abs.len, new_numerator_abs.A)

            # Делим знаменатель на НОД
            new_denominator = self.denominator // gcf

        return Rational(new_numerator, new_denominator)

    def INT_Q_B(self) -> bool:
        """
        Сделал: Захаренко Александр
        Проверка сокращенного дробного на целое,
        если рациональное число является целым,
        то «да», иначе «нет»
        """
        # Сокращаем дробь и проверяем, равен ли знаменатель 1
        reduced = self.RED_Q_Q()
        return reduced.denominator.A == [1]

    def __add__(self, other):
        """
        Сделала: Имховик Наталья
        Выполняет сложение дробей
        Возвращает дробь
        """
        # Находим НОК знаменателей
        lcm = self.denominator.LCM_NN_N(other.denominator)

        # Находим дополнительные множители используя целочисленное деление
        multiplierA = lcm // self.denominator
        multiplierB = lcm // other.denominator

        # Преобразуем натуральные множители в целые числа
        multiplierA_int = Integer(0, multiplierA.len, multiplierA.A)
        multiplierB_int = Integer(0, multiplierB.len, multiplierB.A)

        # Умножаем числители на дополнительные множители и складываем
        new_numerator = (self.numerator * multiplierA_int) + (other.numerator * multiplierB_int)

        # Создаем результирующую дробь
        return Rational(new_numerator, lcm).RED_Q_Q()

    def __sub__(self, other):
        """
        Сделала: Имховик Наталья
        Находит разность дробей
        Возвращает дробь
        """
        # Находим НОК знаменателей
        lcm = self.denominator.LCM_NN_N(other.denominator)

        # Находим дополнительные множители используя целочисленное деление
        multiplierA = lcm // self.denominator
        multiplierB = lcm // other.denominator

        # Преобразуем натуральные множители в целые числа
        multiplierA_int = Integer(0, multiplierA.len, multiplierA.A)
        multiplierB_int = Integer(0, multiplierB.len, multiplierB.A)

        # Умножаем числители на дополнительные множители и вычитаем
        new_numerator = (self.numerator * multiplierA_int) - (other.numerator * multiplierB_int)

        # Создаем результирующую дробь
        return Rational(new_numerator, lcm).RED_Q_Q()

    def __mul__(self, other):
        """
        Сделал: Чумаков Никита Ярославович
        Умножение двух рациональных чисел.
        Результат — новый Rational.
        """
        new_numerator = self.numerator * other.numerator
        new_denominator = self.denominator * other.denominator

        # Формируем новую дробь
        result = Rational(new_numerator, new_denominator)

        return result.RED_Q_Q()

    def __truediv__(self, other):
        """
        Сделал: Чумаков Никита Ярославович
        Деление рациональных чисел q1 / q2.
        Делитель q2 ≠ 0.
        Возвращает новый Rational.
        """
        # Проверим, что делитель не равен нулю
        if other.numerator.A == [0]:
            raise ZeroDivisionError("Деление на ноль в рациональных числах")

        # По формуле: (a/b) ÷ (c/d) = (a*d) / (b*c)
        # Преобразуем знаменатель other в целое число
        other_denominator_int = TRANS_N_Z(other.denominator)

        # Получаем абсолютное значение числителя other
        other_numerator_abs = other.numerator.ABS_Z_Z()

        # Умножаем
        new_numerator = self.numerator * other_denominator_int
        new_denominator = self.denominator * Natural(other_numerator_abs.len, other_numerator_abs.A)

        # Учитываем знак
        if other.numerator.s == 1:  # Если other отрицательный, меняем знак
            new_numerator = new_numerator.MUL_ZM_Z()

        # Формируем новое рациональное число
        result = Rational(new_numerator, new_denominator)

        return result.RED_Q_Q()
    
    def EQ_Q_B(self, other):
        """Проверка равенства двух рациональных чисел"""
        # Приводим к общему знаменателю и сравниваем числители
        num1 = self.numerator.MUL_ZZ_Z(other.denominator)
        num2 = other.numerator.MUL_ZZ_Z(self.denominator)
        return num1.A == num2.A and num1.s == num2.s
    
    def ROOT_QN_Q(self, n: Natural=2, iterations=5):
        """
        Вычисление приближенного корня n-ой степени через метод Ньютона
        x{n+1} = ((n-1)x{n} + a / x{n}^(n-1)) / n, a = self
        Возвращает Rational - приближение root(self)
        """
        # # Сохраняем n как int
        # n_int = int(''.join(map(str, n.A)))

        # Проверяем, равна ли степень корня единице
        if n.A == [1]:
            return self
        
        # Для отрицательных чисел:
        if self.numerator.s == 1:
            # Если корень четный
            if (n % Natural(0, [2])).A == [0]:
                raise ValueError(f"Корень четной степени из отрицательного числа")
            # Нечетный корень
            else:
                abs_self = self.ABS_Q_Q()
                abs_root = abs_self.ROOT_QN_Q(n, iterations)
                # Для нечетного корня: корень из (-a) = -(корень из a)
                return Rational(abs_root.numerator.MUL_ZM_Z(), abs_root.denominator)
        
        # Для положительных чисел
        # Проверяем, равно ли число нулю
        if self.numerator.A == [0]:
            # Корень из (0) = 0
            return Rational(Integer(0, 0, [0]), Natural(0, [1]))
        
        # Выбираем начальное приближение
        # Если self > 1 -> x0 = self/2
        # self > 1, когда числитель числа больше его знаменателя
        if Natural(self.numerator.len, self.numerator.A).COM_NN_D(self.denominator) == 1:
            x = self / Rational(Integer(0, 0, [2]), Natural(0, [1]))
        # Если self < 1 -> x0 = 1
        else:
            x = Rational(Integer(0, 0, [1]), Natural(0, [1]))
        
        # метод Ньютона
        for i in range(iterations):
            # Проверяем, что x не равен нулю
            if x.numerator.A == [0]:
                # Начинаем с единицы
                x = Rational(Integer(0, 0, [1]), Natural(0, [1]))
                continue

            # Находим x^(n-1)
            x_pow = Rational(Integer(0, 0, [1]), Natural(0, [1]))
            n_int = int(''.join(map(str, n.A)))
            for _ in range(n_int - 1):
                x_pow = x_pow * x
            
            # x{n+1} = ((n-1)x{n} + a / x{n}^(n-1)) / n
            numerator = (x * Rational(TRANS_N_Z(n - Natural(0, [1])), Natural(0, [1]))) + (self / x_pow)
            x = numerator / Rational(TRANS_N_Z(n), Natural(0, [1]))

        return x.RED_Q_Q()
    
    def ABS_Q_Q(self):
        """
        Нахождение абсолютного значения числа
        Возвращает новый Rational
        """
        abs_numerator = self.numerator.ABS_Z_Z() if self.numerator.s == 1 else self.numerator
        return Rational(abs_numerator, self.denominator)
    
    def TRUNCAT_Q_Q(self, max_digits=20):
        """
        Усечение Rational до max_digits цифр
        """
        # Если уже достаточно мал
        if len(''.join(map(str, self.numerator.A))) <= max_digits and \
           len(''.join(map(str, self.denominator.A))) <= max_digits:
            return self
        
        # Упрощаем: берем первые max_digits цифр
        num_str = ''.join(map(str, self.numerator.A))
        den_str = ''.join(map(str, self.denominator.A))
        
        # Ограничиваем длину
        if len(num_str) > max_digits:
            num_str = num_str[:max_digits]
        if len(den_str) > max_digits:
            den_str = den_str[:max_digits]
        
        # Создаем новые числа
        new_numerator = Integer(self.numerator.s, len(num_str)-1, [int(d) for d in num_str])
        new_denominator = Natural(len(den_str)-1, [int(d) for d in den_str])
        
        return Rational(new_numerator, new_denominator).RED_Q_Q()

    def show(self):
        s=''
        if self.numerator.A[0] == 0:
            return '0'
        if self.numerator.s == 1:
            s='-'
        if self.denominator.len == 0 and self.denominator.A[0] == 1:
            temp = list(map(str, self.numerator.A))
            temp = "".join(temp)
            s = s+temp
            return s
        temp = list(map(str, self.numerator.A))
        s = s + '('
        temp = "".join(temp)
        s = s + temp
        temp = list(map(str, self.denominator.A))
        s = s+'/'
        temp = "".join(temp)
        s = s+temp
        s = s + ')'
        return s
