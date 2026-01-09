from rational_algebra.Rational import Rational
from rational_algebra.Integer import Integer
from rational_algebra.Natural import Natural
from rational_algebra.TRANS.TRANS_N_Z import TRANS_N_Z

class Complex:
    def __init__(self, real: Rational, imaginary: Rational):
        # Действительная часть числа
        self.real = real
        # Мнимая часть числа
        self.imaginary = imaginary

    def RE_C_Q(self)->Rational:
        """
        Получить действительную часть числа
        Возвращает Rational
        """
        return self.real

    def IM_C_Q(self)->Rational:
        """
        Получить мнимую часть числа
        Возвращает Rational
        """
        return self.imaginary

    def IS_RE_C_B(self)->bool:
        """
        Определяет является ли число действительным
        (мнимая часть числа равна 0)
        Возвращает True, если число действительное, иначе False
        """
        # Проверяем, равен ли числитель мнимой части нулю
        return self.imaginary.numerator.A == [0]
    
    def IS_IM_C_B(self)->bool:
        """
        Определяет является ли число чисто мнимым
        (действителья часть числа равна 0)
        Возвращает True, если число действительное, иначе False
        """
        # Проверяем, равен ли числитель действительной части нулю
        return self.real.numerator.A == [0]
    
    def NZERO_C_B(self)->bool:
        """
        Определяет является ли число нулем
        (действительная и мнимая части числа равны 0)
        Возвращает True, если число действительное, иначе False
        """
        # Проверяем, что действительная и мнимая части не равны нулю одновременно
        return not(self.IS_RE_C_B() and self.IS_IM_C_B())
    
    def __add__(self, other):
        """
        Сложение комплексных чисел
        Возвращает новое комплексное число
        """
        # Попарно скаладываем действительные и мнимые части
        # Формируем результат
        return Complex(self.real + other.real,
                       self.imaginary + other.imaginary)
    
    def __sub__(self, other):
        """
        Разность комплексных чисел
        Возвращает новое коплексное число
        """
        # Попарно находим разность действительных и мнимых частей
        # Формируем результат 
        return Complex(self.real - other.real,
                       self.imaginary - other.imaginary)
    
    def __mul__(self, other):
        """
        Умножение комплексных чисел
        (a + bi) * (c + di) = (ac - bd) + (ad + bc)i
        Возвращает новое комплексное число
        """
        # Находим действительную и мнимую часть в соответствии с формулой
        # Формируем результат
        return Complex(self.real * other.real - self.imaginary * other.imaginary,
                       self.real * other.imaginary + self.imaginary * other.real)

    def __truediv__(self, other):
        """
        Деление комплексных чисел
        (a + bi) / (c + di) = ((a*c + b*d)/(c^2 + d^2)) + ((b*c - a*d)/(c^2 + d^2))i
        Возвращает новое комплексное число
        """
        # Проверяем, что делитель не равен нулю
        if not other.NZERO_C_B():
            raise ZeroDivisionError("Деление на нулевое комплексное число")
        
        # Знаменатель обеих частей: (c^2 + d^2)
        denom = other.real * other.real + other.imaginary * other.imaginary

        # Действительная часть результата: ((a*c + b*d)/(c^2 + d^2))
        re = (self.real * other.real + self.imaginary * other.imaginary) / denom

        # Мнимая часть результата: ((b*c - a*d)/(c^2 + d^2))
        im = (self.imaginary * other.real - self.real * other.imaginary) / denom

        # Формируем результат
        return Complex(re, im)
    
    def CONJ_C_Z(self)->Integer:
        """
        Получение сопряженного комплексного числа
        Возвращает новое комплексное число
        """
        # Меняем знак мнимой части на противоположный
        new_imaginary_numerator = self.imaginary.numerator.MUL_ZM_Z()
        new_imaginary = Rational(new_imaginary_numerator, self.imaginary.denominator)

        # Формируем результат
        return Complex(self.real, new_imaginary)
    
    def ABS_C_Q(self)->Rational:
        """
        Вычисление квадрата модуля комплексного числа
        |a + bi| = sqrt(a^2 + b^2)
        Возвращает Rаtional
        """
        return self.real * self.real + self.imaginary * self.imaginary

    def INV_C_С(self):
        """
        Получение обратного комплексного числа (1/z)
        1/(a + bi) = (a - bi) / |a + bi|^2
        Возвращает новое комплексное число
        """
        # Проверяем, что число не равно нулю
        if not self.NZERO_C_B():
            raise ZeroDivisionError("Деление на нулевое комплексное число")

        # Находим сопряженное
        conjugate = self.CONJ_C_Z()

        # Находим квадрат модуля числа
        module_squared = self.ABS_C_Q()

        # Находим разность сопряженного и квадрата модуля
        # Формируем результат
        return conjugate / Complex(module_squared, Rational(Integer(0, 0, [0]), Natural(0, [1])))
    
    def TAN_ARG_C_Q(self)->Rational:
        """
        Вычисление тангенса аргумента комплексного числа
        tan(fi) = b/a, a - действительная часть, b - мнимая
        Возвращает Rational, если определено, иначе None
        Для особых случаев возвращает строку-идентификатор
        """
        # Проверяем, является ли число нулевм
        if not self.NZERO_C_B():
            # Аргумент нулевого комплексного числа не определен
            return 'UNDEFINED'
        
        # Проверяем, лежит ли число на действительной оси
        if self.IS_RE_C_B():
            # tan(0) = 0, tan(pi) = 0
            return Rational(Integer(0, 0, [0]), Natural(0, [1]))
        
        # Проверяем, лежит ли число на мнимой оси
        if self.IS_IM_C_B():
            # Положительная ось
            if self.imaginary.numerator.s == 0:
                return 'POS_INF'
            # Отрицательная ось
            else:
                return 'NEG_INF'
            
        return self.imaginary / self.real
    
    def QUARTER_C_D(self)->int:
        """
        Определение четверти комплексной плоскости
        Возвращает, число соответствующее четверти:
        -1 - начало координат (0, 0)
        0 - лежит на оси
        1 - I четверть
        2 - II четверть
        3 - III четверть
        4 - IV четверть
        """
        # Проверяем, является ли число нулевым
        if not self.NZERO_C_B():
            return -1
        
        # Проверяем, лежит ли число на оси
        if self.IS_RE_C_B() or self.IS_IM_C_B():
            return 0
        
        # Действительная и мнимая части положительные
        if self.real.numerator.s == 0 and self.imaginary.numerator.s == 0:
            # I четверть
            return 1
        
        # Действительная часть отрицательная и мнимая часть положительная
        if self.real.numerator.s != 0 and self.imaginary.numerator.s == 0:
            # II четверть
            return 2
        
        # Действительная и мнимая части отрицательные
        if self.real.numerator.s != 0 and self.imaginary.numerator.s != 0:
            # III четверть
            return 3
        
        # Действительная часть положительная и мнимая часть отрицательная
        if self.real.numerator.s == 0 and self.imaginary.numerator.s != 0:
            # IV четверть
            return 4
        
    def AXIS_C_D(self)->int:
        """
        Определение оси комплексного числа
        Возвращает, число соответствующее оси:
        -1 - начало координат (0, 0)
        0 - не лежит на оси
        1 - действительная положительная ось
        2 - мнимая положительная ось
        3 - действительная отрицательная ось
        4 - мнимая отрицательная ось
        """
        # Проверяем, является ли число нулевым
        if not self.NZERO_C_B():
            return -1
        
        # Проверяем, лежит ли число на оси
        if not (self.IS_RE_C_B() or self.IS_IM_C_B()):
            return 0
        
        # Мнимая часть равна 0
        if self.IS_RE_C_B():
            # Положительная действительная ось
            if self.real.numerator.s == 0:
                return 1
            # Отрицательная действительная ось
            else:
                return 3
        # Действительная часть равна 0
        else:
            # Положительная мнимая ось
            if self.imaginary.numerator.s == 0:
                return 2
            # Отрицательная мнимая ось
            else:
                return 4
    
    def EQ_C_B(self, other)->bool:
        """
        Проверка равенства двух комплексных чисел
        Возвращает True, если числа равны, иначе false 
        """
        return (self.real.numerator.A == other.real.numerator.A and 
                self.real.numerator.s == other.real.numerator.s and
                self.real.denominator.A == other.real.denominator.A and
                self.imaginary.numerator.A == other.imaginary.numerator.A and
                self.imaginary.numerator.s == other.imaginary.numerator.s and
                self.imaginary.denominator.A == other.imaginary.denominator.A)
    
    def POW_CN_C(self, n: Natural):
        """
        Возведение комплексного числа в натуральную степень n
        """
        result = Complex(Rational(Integer(0, 0, [1]), Natural(0, [1])),
                         Rational(Integer(0, 0, [0]), Natural(0, [1])))
        base = self
        while n.NZER_N_B():
            if (n % Natural(0, [2])).A == [1]:
                result = result * base
            base = base * base
            n = n // Natural(0, [2])

        return result
    
    def show_alg(self)->str:
        """
        Отображение комплексного числа
        в алгебраической форме
        """
        re = self.real.show()
        im = self.imaginary.show()

        if self.imaginary.numerator.A == [0]:
            return re
        elif self.imaginary.numerator.A == [0]:
            return im + 'i'
        else:
            if self.imaginary.numerator.s == 0:
                return '(' + re + '+' + im + 'i' + ')'
            else:
                return '(' + re + im + 'i' + ')'
    
    def show_exp(self)->str:
        """
        Отображение комплексного числа
        в показательной форме
        """
        if not self.NZERO_C_B():
            return '0'
        
        r = self.ABS_C_Q()
        tan_fi = self.TAN_ARG_C_Q()

        if isinstance(tan_fi, str):
            if tan_fi == 'POS_INF': return f'{r.show()}·e^(i·π/2)'
            if tan_fi == 'NEG_INF': return f'{r.show()}·e^(-i·π/2)'
            if tan_fi == 'ZERO':
                if self.real.numerator.s == 0: return f'{r.show()}·e^(i·0)'
                else: return f'{r.show()}·e^(i·π)'
        
        return f'√{r.show()}·e^(i·arctan({tan_fi.show()}))'