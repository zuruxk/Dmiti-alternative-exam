import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rational_algebra.Rational import Rational
from rational_algebra.Integer import Integer
from rational_algebra.Natural import Natural
from complex_algebra.Complex import Complex
from rational_algebra.TRANS.TRANS_N_Z import TRANS_N_Z

class TestComplex(unittest.TestCase):
    
    def setUp(self):
        """Создаем тестовые комплексные числа"""
        self.nat_one = Natural(0, [1])
        self.nat_two = Natural(0, [2])

        self.int_zero = Integer(0, 0, [0])
        self.int_one = Integer(0, 0, [1])
        self.int_two = Integer(0, 0, [2])
        self.int_three = Integer(0, 0, [3])
        self.int_four = Integer(0, 0, [4])
        self.int_neg_one = Integer(1, 0, [1])
        self.int_neg_two = Integer(1, 0, [2])

        self.rat_zero = Rational(self.int_zero, self.nat_one)
        self.rat_one = Rational(self.int_one, self.nat_one)
        self.rat_two = Rational(self.int_two, self.nat_one)
        self.rat_three = Rational(self.int_three, self.nat_one)
        self.rat_four = Rational(self.int_four, self.nat_one)
        self.rat_neg_one = Rational(self.int_neg_one, self.nat_one)
        self.rat_half = Rational(self.int_one, Natural(0, [2]))
        self.rat_neg_half = Rational(self.int_neg_one, Natural(0, [2]))

        self.c_zero = Complex(self.rat_zero, self.rat_zero)           # 0 + 0i
        self.c_one = Complex(self.rat_one, self.rat_zero)             # 1 + 0i
        self.c_i = Complex(self.rat_zero, self.rat_one)               # 0 + 1i
        self.c_neg_i = Complex(self.rat_zero, self.rat_neg_one)       # 0 - 1i
        self.c_one_plus_i = Complex(self.rat_one, self.rat_one)       # 1 + i
        self.c_two_plus_three_i = Complex(self.rat_two, self.rat_three) # 2 + 3i
        self.c_one_minus_i = Complex(self.rat_one, self.rat_neg_one)  # 1 - i
        self.c_neg_one_plus_i = Complex(self.rat_neg_one, self.rat_one) # -1 + i
        self.c_neg_one_minus_i = Complex(self.rat_neg_one, self.rat_neg_one) # -1 - i
        self.c_real_two = Complex(self.rat_two, self.rat_zero)        # 2 + 0i
        self.c_imag_two = Complex(self.rat_zero, self.rat_two)        # 0 + 2i
        self.c_half_plus_half_i = Complex(self.rat_half, self.rat_half) # 0.5 + 0.5i
    
    def test_initialization(self):
        """Тест инициализации"""
        self.assertEqual(self.c_one.real, self.rat_one)
        self.assertEqual(self.c_one.imaginary, self.rat_zero)
        self.assertEqual(self.c_i.real, self.rat_zero)
        self.assertEqual(self.c_i.imaginary, self.rat_one)
    
    def test_RE_C_Q(self):
        """Тест получения действительной части"""
        self.assertEqual(self.c_one.RE_C_Q(), self.rat_one)
        self.assertEqual(self.c_i.RE_C_Q(), self.rat_zero)
        self.assertEqual(self.c_one_plus_i.RE_C_Q(), self.rat_one)
    
    def test_IM_C_Q(self):
        """Тест получения мнимой части"""
        self.assertEqual(self.c_one.IM_C_Q(), self.rat_zero)
        self.assertEqual(self.c_i.IM_C_Q(), self.rat_one)
        self.assertEqual(self.c_one_plus_i.IM_C_Q(), self.rat_one)
    
    def test_IS_RE_C_B(self):
        """Тест проверки на действительное число"""
        self.assertTrue(self.c_one.IS_RE_C_B())
        self.assertTrue(self.c_real_two.IS_RE_C_B())
        self.assertFalse(self.c_i.IS_RE_C_B())
        self.assertFalse(self.c_one_plus_i.IS_RE_C_B())
    
    def test_IS_IM_C_B(self):
        """Тест проверки на чисто мнимое число"""
        self.assertTrue(self.c_i.IS_IM_C_B())
        self.assertTrue(self.c_imag_two.IS_IM_C_B())
        self.assertFalse(self.c_one.IS_IM_C_B())
        self.assertFalse(self.c_one_plus_i.IS_IM_C_B())
    
    def test_NZERO_C_B(self):
        """Тест проверки на ноль"""
        self.assertFalse(self.c_zero.NZERO_C_B())
        self.assertTrue(self.c_one.NZERO_C_B())
        self.assertTrue(self.c_i.NZERO_C_B())
    
    def test_addition(self):
        """Тест сложения"""
        # (1 + 0i) + (0 + i) = (1 + i)
        result = self.c_one + self.c_i
        self.assertTrue(result.EQ_C_B(self.c_one_plus_i))
        
        # (1 + i) + (1 - i) = (2 + 0i)
        result = self.c_one_plus_i + self.c_one_minus_i
        self.assertTrue(result.EQ_C_B(self.c_real_two))
        
        # Коммутативность
        result1 = self.c_one_plus_i + self.c_neg_one_minus_i
        result2 = self.c_neg_one_minus_i + self.c_one_plus_i
        self.assertTrue(result1.EQ_C_B(result2))
    
    def test_subtraction(self):
        """Тест вычитания"""
        # (1 + i) - (1 + 0i) = (0 + i)
        result = self.c_one_plus_i - self.c_one
        self.assertTrue(result.EQ_C_B(self.c_i))
        
        # (1 + i) - (0 + i) = (1 + 0i)
        result = self.c_one_plus_i - self.c_i
        self.assertTrue(result.EQ_C_B(self.c_one))
        
        # (2 + 3i) - (1 + i) = (1 + 2i)
        c_one_plus_two_i = Complex(self.rat_one, self.rat_two)
        result = self.c_two_plus_three_i - self.c_one_plus_i
        self.assertTrue(result.EQ_C_B(c_one_plus_two_i))
    
    def test_multiplication(self):
        """Тест умножения"""
        # (1 + 0i) * (0 + i) = (0 + i)
        result = self.c_one * self.c_i
        self.assertTrue(result.EQ_C_B(self.c_i))
        
        # (1 + i) * (1 - i) = 2 + 0i
        result = self.c_one_plus_i * self.c_one_minus_i
        self.assertTrue(result.EQ_C_B(self.c_real_two))
        
        # i * i = -1
        result = self.c_i * self.c_i
        expected = Complex(self.rat_neg_one, self.rat_zero)
        self.assertTrue(result.EQ_C_B(expected))
    
    def test_division(self):
        """Тест деления"""
        # (1 + i) / (1 + i) = 1
        result = self.c_one_plus_i / self.c_one_plus_i
        self.assertTrue(result.EQ_C_B(self.c_one))
        
        # (2 + 0i) / (1 + i) = (1 - i)
        result = self.c_real_two / self.c_one_plus_i
        self.assertTrue(result.EQ_C_B(self.c_one_minus_i))
        
        # Проверка деления на ноль
        with self.assertRaises(ZeroDivisionError):
            result = self.c_one / self.c_zero
    
    def test_CONJ_C_Z(self):
        """Тест сопряжения"""
        # Сопряжение (1 + i) = (1 - i)
        result = self.c_one_plus_i.CONJ_C_Z()
        self.assertTrue(result.EQ_C_B(self.c_one_minus_i))
        
        # Сопряжение (0 + i) = (0 - i)
        result = self.c_i.CONJ_C_Z()
        self.assertTrue(result.EQ_C_B(self.c_neg_i))
        
        # Сопряжение действительного числа не меняет его
        result = self.c_one.CONJ_C_Z()
        self.assertTrue(result.EQ_C_B(self.c_one))
    
    def test_INV_C_C(self):
        """Тест обратного числа"""
        # 1/(1 + 0i) = 1
        result = self.c_one.INV_C_С()
        self.assertTrue(result.EQ_C_B(self.c_one))
        
        # 1/(0 + i) = -i
        result = self.c_i.INV_C_С()
        self.assertTrue(result.EQ_C_B(self.c_neg_i))
        
        # Проверка деления на ноль
        with self.assertRaises(ZeroDivisionError):
            result = self.c_zero.INV_C_С()
    
    def test_TAN_ARG_C_Q(self):
        """Тест тангенса аргумента"""
        # Для нуля - UNDEFINED
        result = self.c_zero.TAN_ARG_C_Q()
        self.assertEqual(result, 'UNDEFINED')
        
        # Для положительной мнимой оси - POS_INF
        result = self.c_i.TAN_ARG_C_Q()
        self.assertEqual(result, 'POS_INF')
        
        # Для отрицательной мнимой оси - NEG_INF
        result = self.c_neg_i.TAN_ARG_C_Q()
        self.assertEqual(result, 'NEG_INF')
    
    def test_QUARTER_C_D(self):
        """Тест определения четверти"""
        # Ноль
        self.assertEqual(self.c_zero.QUARTER_C_D(), -1)
        
        # Ось
        self.assertEqual(self.c_one.QUARTER_C_D(), 0)
        self.assertEqual(self.c_i.QUARTER_C_D(), 0)
        
        # I четверть
        self.assertEqual(self.c_one_plus_i.QUARTER_C_D(), 1)
        
        # II четверть
        self.assertEqual(self.c_neg_one_plus_i.QUARTER_C_D(), 2)
        
        # III четверть
        self.assertEqual(self.c_neg_one_minus_i.QUARTER_C_D(), 3)
        
        # IV четверть
        self.assertEqual(self.c_one_minus_i.QUARTER_C_D(), 4)
    
    def test_AXIS_C_D(self):
        """Тест определения оси"""
        # Ноль
        self.assertEqual(self.c_zero.AXIS_C_D(), -1)
        
        # Не на оси
        self.assertEqual(self.c_one_plus_i.AXIS_C_D(), 0)
        
        # Действительная положительная ось
        self.assertEqual(self.c_one.AXIS_C_D(), 1)
        
        # Мнимая положительная ось
        self.assertEqual(self.c_i.AXIS_C_D(), 2)
        
        # Действительная отрицательная ось
        c_neg_one = Complex(self.rat_neg_one, self.rat_zero)
        self.assertEqual(c_neg_one.AXIS_C_D(), 3)
        
        # Мнимая отрицательная ось
        self.assertEqual(self.c_neg_i.AXIS_C_D(), 4)
    
    def test_EQ_C_B(self):
        """Тест равенства"""
        self.assertTrue(self.c_one.EQ_C_B(self.c_one))
        self.assertTrue(self.c_zero.EQ_C_B(self.c_zero))
        self.assertFalse(self.c_one.EQ_C_B(self.c_i))
        self.assertFalse(self.c_one_plus_i.EQ_C_B(self.c_one_minus_i))

    def test_show_alg(self):
        """Тест строкового представления в алгебраической форме"""
        self.assertEqual(self.c_zero.show_alg(), '0')
        self.assertEqual(self.c_one.show_alg(), '1')
    
    def test_show_exp(self):
        """Тест строкового представления в показательной форме"""
        self.assertEqual(self.c_zero.show_exp(), '0')
        # Формат зависит от реализации, проверяем, что не возникает ошибок
        self.assertIsInstance(self.c_one.show_exp(), str)
        self.assertIsInstance(self.c_i.show_exp(), str)
        self.assertIsInstance(self.c_one_plus_i.show_exp(), str)


if __name__ == '__main__':
    unittest.main(verbosity=2)