from rational_algebra.Natural import Natural
from rational_algebra.Integer import Integer
from rational_algebra.Rational import Rational
from rational_algebra.TRANS.TRANS_N_Z import TRANS_N_Z
from .Complex import Complex

class ComplexPolynomial:
    def __init__(self, deg, C):
        """
        deg - int степень многочлена
        C - [] массив коэффициентов из Complex
        """
        self.deg = deg
        self.C = C
    
    def __add__(self, other):
        """
        Сложение многочленов с комплексными коэффициентами
        Возвращает новый комплексный многочлен
        """
        max_degree = max(self.deg, other.deg)

        # Создаем массив для коэффициентов результата
        result_coeffs = []

        for i in range(max_degree + 1):
            degree = max_degree - i

            # Находим соответствующие коэффициенты
            self_index = self.deg - degree if degree <= self.deg else -1
            other_index = other.deg - degree if degree <= other.deg else -1

            # Текущий коэффициент первого многочлена
            if self_index >= 0 and self_index <= self.deg:
                coeff1 = self.C[self_index]
            else:
                coeff1 = Complex(Rational(Integer(0, 0, [0]), Natural(0, [1])),
                                 Rational(Integer(0, 0, [0]), Natural(0, [1])))
            
            # Текущий коэффициент второго многочлена
            if other_index >= 0 and other_index <= other.deg:
                coeff2 = other.C[other_index]
            else:
                coeff2 = Complex(Rational(Integer(0, 0, [0]), Natural(0, [1])),
                                 Rational(Integer(0, 0, [0]), Natural(0, [1])))
            
            # Складываем комплексные коэффициенты
            sum_coeff = coeff1 + coeff2
            # Пропускаем ведущие нули
            if not(len(result_coeffs) == 0 and not sum_coeff.NZERO_C_B()):
                result_coeffs.append(sum_coeff)

        # Корректируем нулевой результат
        if len(result_coeffs) == 0:
            result_coeffs.append(0)

        # Находим степень результата
        result_degree = len(result_coeffs) - 1

        return ComplexPolynomial(result_degree, result_coeffs)
    
    def __sub__(self, other):
        """
        Разность многочленов с комплексными коэффициентами
        Возвращает новый комплексный многочлен
        """
        max_degree = max(self.deg, other.deg)
        result_coeffs = []

        for i in range(max_degree + 1):
            degree = max_degree - i

            self_index = self.deg - degree if degree <= self.deg else -1
            other_index = other.deg - degree if degree <= other.deg else -1

            # Текущий коэффициент первого многочлена
            if self_index >= 0:
                coeff1 = self.C[self_index]
            else:
                coeff1 = Complex(Rational(Integer(0, 0, [0]), Natural(0, [1])),
                                 Rational(Integer(0, 0, [0]), Natural(0, [1])))
                
            # Текущий коэффициент второго многочлена 
            if other_index >= 0:
                coeff2 = other.C[other_index]
            else:
                coeff2 = Complex(Rational(Integer(0, 0, [0]), Natural(0, [1])),
                                 Rational(Integer(0, 0, [0]), Natural(0, [1])))
            
            # Находим разность комплексных коэффициентов
            diff_coeff = coeff1 - coeff2
            # Пропускаем ведущие нули
            if not(len(result_coeffs) == 0 and not diff_coeff.NZERO_C_B()):
                result_coeffs.append(diff_coeff)
        
        # Корректируем нулевой результат
        if len(result_coeffs) == 0:
            result_coeffs.append(0)

        # Находим степень результата
        result_degree = len(result_coeffs) - 1

        return ComplexPolynomial(result_degree, result_coeffs)
        
    def MUL_PQ_P(self, q: Complex):
        """
        Умножение многочлена на комплексное число
        Возвращает новый комплексный многочлен
        """
        # Список для хранения новых коэффициентов
        new_C = []

        for coeff in self.C:
            # Проверяем, нулевой ли коэффициент
            if coeff.NZERO_C_B():
                # Умножаем коэффициент на число
                new_coeff = coeff * q
            else:
                # Сохраняем коэффициент без изменений
                new_coeff = coeff
            
            new_C.append(new_coeff)
        
        return ComplexPolynomial(self.deg, new_C)
    
    def MUL_Pxk_P(self, k: int):
        """
        Умножение многочлена на x^k
        Возвращает новый комплексный многочлен
        """
        # Степень нового многочлена
        new_deg = self.deg + k

        # Добавляем k нулевых комплексных чисел
        zero = Complex(Rational(Integer(0, 0, [0]), Natural(0, [1])),
                       Rational(Integer(0, 0, [0]), Natural(0, [1])))
        new_C = self.C + ([zero] * k)

        return ComplexPolynomial(new_deg, new_C)
    
    def __mul__(self, other):
        """
        Произведение многочленов с комплексными коэффициентами
        Возвращает новый комплексный многочлен
        """
        # Инициализируем нулевой многочлен
        zero = Complex(Rational(Integer(0, 0, [0]), Natural(0, [1])),
                       Rational(Integer(0, 0, [0]), Natural(0, [1])))
        
        product = ComplexPolynomial(0, [zero])

        # Определяем, какой многочлен имеет меньшую степень
        if self.deg <= other.deg:
            shorter, longer = self, other
        else:
            shorter, longer = other, self

        # Перемножаем каждый член меньшего многочлена с каждым членом большего
        for i in range(shorter.deg + 1):
            temp_poly = longer.MUL_PQ_P(shorter.C[i])
            if shorter.C[i].NZERO_C_B():
                temp_poly = temp_poly.MUL_Pxk_P(shorter.deg - i)
            product = product + temp_poly

        return product
    
    def LED_P_C(self)->Complex:
        """
        Возвращает старший коэффициент - Complex
        """
        if not self.C or self.deg < 0:
            return Complex(Rational(Integer(0, 0, [0]), Natural(0, [1])),
                           Rational(Integer(0, 0, [0]), Natural(0, [1])))
        
        return self.C[0]
    
    def DEG_P_N(self)->Natural:
        """
        Возвращает степень многочлена как Natural
        """
        deg_str = str(self.deg)
        A = [int(d) for d in deg_str]
        return Natural(len(A) - 1, A)
    
    def __floordiv__(self, other):
        """
        Частное от деления с остатком
        Возвращает комплексный многочлен
        """
        # Проверяем, что делитель не равен нулю
        if all(not coeff.NZERO_C_B() for coeff in other.C):
            raise ZeroDivisionError("Деление на нулевой многочлен")
        
        # Копируем делимое и делитель
        A = ComplexPolynomial(self.deg, self.C[:])
        B = ComplexPolynomial(other.deg, other.C[:])

        # Создаем нулевой многочлен для сохранения результата
        zero = Complex(Rational(Integer(0, 0, [0]), Natural(0, [1])),
                       Rational(Integer(0, 0, [0]), Natural(0, [1])))
        Q = ComplexPolynomial(0, [zero])

        # Основной цикл деления
        while True:
            degA = A.deg
            degB = B.deg

            # Если степень делимого меньше или делимое == 0
            if degA < degB or all(not coeff.NZERO_C_B() for coeff in A.C):
                break

            # Вычисляем разность степеней
            k = degA - degB

            # Выбираем старшие коэффициенты
            a_lead = A.C[0]
            b_lead = B.C[0]

            # Находим разность комплексных коэффициентов
            factor = a_lead / b_lead

            # Создаем одночлен factor * x^k
            term = ComplexPolynomial(0, [factor])
            term_shifted = term.MUL_Pxk_P(k)

            # Прибавляем одночлен к промежуточному частному
            Q = Q + term_shifted

            # Умножаем делитель на factor и x^k
            B_shifted = B.MUL_Pxk_P(k)
            B_scaled_coeffs = [c * factor for c in B_shifted.C]
            B_scaled = ComplexPolynomial(B_shifted.deg, B_scaled_coeffs)

            # Вычитаем
            A = A - B_scaled

            # # Удаляем ведущие нули
            # while len(A.C) > 1 and not A.C[0].NZERO_C_B():
            #     A.C.pop(0)
            #     A.deg -= 1

        # Удаляем ведущие нули в частном
        while len(Q.C) > 1 and not Q.C[0].NZERO_C_B():
            Q.C.pop(0)

        # Вычисляем степень результата 
        Q.deg = len(Q.C) - 1

        return Q

    def __mod__(self, other):
        """
        Остаток от деления многочленов
        Возвращает комплексный многочлен
        """
        # Находим частное от деления многочленов
        quotient = self // other

        # Находим произведение частного и делителя
        product = quotient * other

        # Вычитаем полученное значение из делимого
        return self - product
    
    def DER_P_P(self):
        """
        Производная многочлена
        Возвращает новый комплексный многочлен
        """
        # Проверяем, является ли многочлен константой
        if self.deg == 0:
            # Производная константы равна 0
            zero = Complex(Rational(Integer(0, 0, [0]), Natural(0, [1])),
                           Rational(Integer(0, 0, [0]), Natural(0, [1])))
            return ComplexPolynomial(0, [zero])
        
        coeffs = []
        for i in range(self.deg):
            # Для степени self.deg - i
            power = self.deg - i
            c = self.C[i]

            # Умножаем коэффициент на степень
            power_rational = Rational(Integer(0, len(str(power))-1, [int(d) for d in str(power)]), Natural(0, [1]))
            new_re = c.real * power_rational
            new_im = c.imaginary * power_rational
            coeffs.append(Complex(new_re, new_im))

        return ComplexPolynomial(self.deg - 1, coeffs)
    
    def EVAL_P_C(self, x: Complex)->Complex:
        """
        Вычисление значения многочлена в точке x по схеме Горнера
        Возвращает Complex
        """
        result = Complex(Rational(Integer(0, 0, [0]), Natural(0, [1])),
                         Rational(Integer(0, 0, [0]), Natural(0, [1])))
        
        for coeff in self.C:
            result = result * x
            result = result + coeff

        return result
    
    def show_alg(self)->str:
        """
        Отображение многочлена в алгебраической форме
        """
        if not self.C or self.deg < 0:
            return '0'
        
        result = ''
        for i in range(self.deg + 1):
            coeff = self.C[i]
            degree = self.deg - i

            if not coeff.NZERO_C_B():
                continue

            coeff_str = coeff.show_alg()
            if result:
                result += ' + '
            
            if degree == 0:
                result += coeff_str
            elif degree == 1:
                if coeff_str == '1':
                    result += 'x'
                elif coeff_str == '-1':
                    result += '-x'
                else:
                    result += f'{coeff_str}x'
            else:
                if coeff_str == '1':
                    result += f'x^{degree}'
                elif coeff_str == "-1":
                    result += f'-x^{degree}'
                else:
                    result += f'{coeff_str}x^{degree}'
        
        return result if result else '0'
    
    def show_exp(self):
        """
        Отображение многочлена в показательной форме коэффициентов
        """
        if not self.C or self.deg < 0:
            return '0'
        
        result = ''
        for i in range(self.deg + 1):
            coeff = self.C[i]
            degree = self.deg - i
            
            if not coeff.NZERO_C_B():
                continue
            
            coeff_str = coeff.show_exp()
            
            if result:
                result += ' + '
            
            if degree == 0:
                result += coeff_str
            elif degree == 1:
                result += f'{coeff_str}·x'
            else:
                result += f'{coeff_str}·x^{degree}'
        
        return result if result else '0'