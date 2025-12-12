from rational_algebra.Rational import Rational
from rational_algebra.Integer import Integer
from rational_algebra.Natural import Natural

class Complex:
    def __init__(self, real: Rational, imaginary: Rational):
        # Действительная часть числа
        self.real = real
        # Мнимая часть числа
        self.imaginary = imaginary

    def RE_C_Q(self):
        """
        Получить действительную часть числа
        Возвращает Rational
        """
        return self.real

    def IM_C_Q(self):
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
        if not other.NZERO():
            raise ZeroDivisionError("Деление на нулевое комплексное число")
        
        # Знаменатель обеих частей: (c^2 + d^2)
        denom = other.real * other.real + other.imaginary * other.imaginary

        # Действительная часть результата: ((a*c + b*d)/(c^2 + d^2))
        re = (self.real * other.real + self.imaginary * other.imaginary) / denom

        # Мнимая часть результата: ((b*c - a*d)/(c^2 + d^2))
        im = (self.imaginary * other.real - self.real * other.imaginary) / denom

        # Формируем результат
        return Complex(re, im)
    
    def CONJ_C_Z(self):
        """
        Получение сопряженного комплексного числа
        Возвращает новое комплексное число
        """
        # Меняем знак мнимой части на противоположный
        new_imaginary_numerator = self.imaginary.numerator.MUL_ZM_Z()
        new_imaginary = Rational(new_imaginary_numerator, self.imaginary.denominator)

        # Формируем результат
        return Complex(self.real, new_imaginary)
    
    def ABS_C_Q(self):
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
    
