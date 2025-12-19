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
            
    def NORM_C_C(self):
        """
        Нормализация комплексного числа
        z' = z / |z|
        Возвращает нормализованное комплексное число
        """
        # Находим модуль числа
        mod = self.ABS_C_Q().ROOT_QN_Q(Natural(0, [2]))
        mod = Complex(mod, Rational(Integer(0, 0, [0]), Natural(0, [1])))

        # Возвращаем исходное число денное на его норму
        return self / mod
            
    def ROTATE_CQ_C(self, angle_tan: Rational):
        """
        Поворот на угол, заданный тангенсом
        z' = z * (cos(fi) + i*sin(fi)), tan(fi) = angle_tan
        cos(fi) = 1 / sqrt(1 + tan^2(fi))
        sin(fi) = tan(fi) / sqrt(1 + tan^2(fi))
        z' = z * (1 + t*i) / |1 + i·t|, t = tan(fi)
        Возвращает новое комплексное число
        """
        # Создаем вектор направления (1 + tan(fi)*i)
        rotation_vector = Complex(Rational(Integer(0, 0, [1]), Natural(0, [1])), angle_tan)

        # Нормализуем вектор поворота
        rotation_norm = rotation_vector.NORM_C_C()

        # Поворачиваем исходный вектор: z' = z * rotation_norm
        return self * rotation_norm
    
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
    
    def COS_C_R(self)->Rational:
        """
        Вычисление косинуса аргумента комплексного числа
        для (a + bi):
        cos(fi) = a / r, r = |a + bi|
        Возвращает Rational
        """
        # Находим модуль числа
        r = self.ABS_C_Q().ROOT_QN_Q(Natural(0, [2]))

        # Находим cos(fi) = a / r
        return self.real / r
    
    def SIN_C_Q(self)->Rational:
        """
        Вычисление синуса аргумента комплексного числа
        для (a + bi):
        sin(fi) = b / r, r = |a + bi|
        Возвращает Rational
        """
        # Находим модуль числа
        r = self.ABS_C_Q().ROOT_QN_Q(Natural(0, [2]))

        # Находим sin(fi) = b / r
        return self.imaginary / r
    
    def POW_CN_C(self, n: Natural):
        """
        Возведение комплексного числа в натуральную степень n по формуле Муавра
        z^n = (r(cos(fi) + i sin(fi)))^n = r^n (cos(n*fi) + i sin(n*fi))
        Возвращает новое комплексное число
        """
        # Проверяем, равно ли число нулю
        if not self.NZERO_C_B():
            # Проверяем, равна ли степень n
            if n.A != [0]:
                # 0^n = 0
                return Complex(self.real, self.imaginary)
            else:
                # 0^0 не определено
                raise ValueError("0^0 не определено")
        
        # Проверяем, равна ли степень n нулю
        if n.A == [0]:
            # z^0 = 1
            return Complex(Rational(Integer(0, 0, [1]), Natural(0, [1])),
                           Rational(Integer(0, 0, [0]), Natural(0, [1])))
        
        # Сохраняем n как int
        n_int = int(''.join(map(str, n.A)))

        # Нормируем исходный вектор,
        # z_norm = cos(fi) + i*sin(fi)
        z_norm = self.NORM_C_C()

        # Возводим нормированное в степень,
        # (cos(fi) + i*sin(fi))^n = cos(n*fi) + i*sin(n*fi)
        result_norm = Complex(Rational(Integer(0, 0, [1]), Natural(0, [1])), Rational(Integer(0, 0, [0]), Natural(0, [1])))
        for _ in range(n_int):
            result_norm = result_norm * z_norm
        
        # Возводим аргумент в степень
        r = self.ABS_C_Q().ROOT_QN_Q(Natural(0, [2]))
        r_power = Rational(Integer(0, 0, [1]), Natural(0, [1]))
        for _ in range(n_int):
            r_power = r_power * r

        # Сохраняем в алгебраической форме
        return Complex(r_power * result_norm.real, r_power * result_norm.imaginary)
    
    def ROOT_CN_C(self, n: Natural, iterations=3):
        """
        Нахождения главного корня n-ой степени из комплексного числа
        Через метод Ньютона: w{k+1} = ((n-1)*w{k} + z / (w{k}^(n-1))) / n, z = self
        Возвращает комплексное число
        """
        # Проверяем, равно ли число нулю
        if not self.NZERO_C_B():
            return Complex(self.real, self.imaginary)
        
        # Проверяем, равна ли степень корня единице
        if n.A == [1]:
            return Complex(self.real, self.imaginary)
        
        n_int = int(''.join(map(str, n.A)))
        
        # Для положительных действительных
        if self.IS_RE_C_B() and self.real.numerator.s == 0:
            # z = a (положительное)
            re_root = self.real.ROOT_QN_Q(n, iterations)
            return Complex(re_root, Rational(Integer(0, 0, [0]), Natural(0, [1])))
        
        # Для отрицательных действительных и нечетного n
        elif self.IS_RE_C_B() and self.real.numerator.s == 1 and n_int % 2 == 1:
            # z = -a, n нечетное
            abs_self = self.real.ABS_Z_Z()
            abs_rational = Rational(abs_self, self.denominator)
            re_root = abs_rational.ROOT_QN_Q(n, iterations)
            # Меняем знак
            neg_numer = re_root.numerator.MUL_ZM_Z()
            return Complex(Rational(neg_numer, re_root.denominator),
                           Rational(Integer(0, 0, [0]), Natural(0, [1])))
        
        # Выбираем начальное приближение
        # Берем приближение модуля
        r = self.ABS_C_Q().ROOT_QN_Q(Natural(0, [2]), iterations=2)
        
        # Находим r^(1/n)
        r_root_n = r.ROOT_QN_Q(n, iterations=2)
        
        # Нормируем число
        z_norm = Complex(
            self.real / r,
            self.imaginary / r
        )
        
        # Начальное приближение
        w = Complex(
            r_root_n * z_norm.real,
            r_root_n * z_norm.imaginary
        )
        
        # Метод Ньютона

        n_minus_1 = n_int - 1

        # Создаем Integer для n_minus_1
        n_minus_1_digits = [int(d) for d in str(n_minus_1)]
        n_minus_1_integer = Integer(0, len(n_minus_1_digits)-1, n_minus_1_digits)
        n_minus_1_rat = Rational(n_minus_1_integer, Natural(0, [1]))
        
        # Создаем Integer для n
        n_digits = [int(d) for d in str(n_int)]
        n_integer = Integer(0, len(n_digits)-1, n_digits)
        n_rat = Rational(n_integer, Natural(0, [1]))
        
        for _ in range(min(iterations, 3)):
            if not w.NZERO_C_B():
                w = Complex(
                    Rational(Integer(0, 0, [1]), Natural(0, [1])),
                    Rational(Integer(0, 0, [0]), Natural(0, [1]))
                )
                continue
            
            # Быстрое возведение w^(n-1)
            w_pow = w
            power = 1
            
            while power * 2 <= n_minus_1:
                w_pow = w_pow * w_pow
                power *= 2
            
            while power < n_minus_1:
                w_pow = w_pow * w
                power += 1
            
            # Находим z / w^(n-1)
            z_div_w_pow = self / w_pow
            
            # Находим (n-1)*w
            n_minus_1_w = Complex(
                w.real * n_minus_1_rat,
                w.imaginary * n_minus_1_rat
            )
            
            # w{k+1} = ((n-1)*w{k} + z/w{k}^(n-1)) / n
            numerator = n_minus_1_w + z_div_w_pow
            w_new = Complex(
                numerator.real / n_rat,
                numerator.imaginary / n_rat
            )
            
            w = w_new
        
        return w.TRUNCAT_C_C()

    def TRUNCAT_C_C(self, max_digits=10):
        """
        Усечение обеих компонент комплексного числа
        """
        return Complex(
            self.real.TRUNCAT_Q_Q(max_digits),
            self.imaginary.TRUNCAT_Q_Q(max_digits)
        )
    
    def TO_POLAR_C_Z(self):
        """
        Полярное представление комплексного числа
        Возвращает (r^2, tan(fi), четверть)
        """
        # Проверяем, равно ли число нулю
        if not self.NZERO_C_B():
            return(Rational(Integer(0, 0, [0]), Natural(0, [1])),
                   Rational(Integer(0, 0, [0]), Natural(0, [1])),
                   -1)
        
        # Находим квадрат модуля числа
        r_sq = self.ABS_C_Q()

        # Находим тангенс аргумента числа
        tan_fi = self.TAN_ARG_C_Q()

        # Определяем четверть, в которой лежит число
        quadrant = self.QUARTER_C_D()

        return (r_sq, tan_fi, quadrant)

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