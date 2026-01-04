import re
from rational_algebra.Polynomial import Polynomial
from rational_algebra.Rational import Rational
from rational_algebra.Integer import Integer
from rational_algebra.Natural import Natural
from complex_algebra.Complex import Complex
from complex_algebra.ComplexPolynomial import ComplexPolynomial
from rational_algebra.TRANS.TRANS_INT_Q import TRANS_INT_Q
from rational_algebra.TRANS.TRANS_STR_P import TRANS_STR_P
from rational_algebra.TRANS.TRANS_Q_P import TRANS_Q_P
from rational_algebra.TRANS.TRANS_INT_N import TRANS_INT_N
from rational_algebra.TRANS.TRANS_INT_Z import TRANS_INT_Z


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def to_rpn(expression: str):
    expression = expression.replace(' ', '')

    # Обрабатываем специальные операторы
    expression = expression.replace('//', '§')  # временная замена для целочисленного деления

    # Например: (...)x → (...)*x
    expression = re.sub(r'(?<=\))(?=x)', '*', expression)
    # Также: число сразу перед x (например 3x) → 3*x
    expression = re.sub(r'(?<=\d)(?=x)', '*', expression)

    # Разбиваем на токены (включая знаки)
    token_pattern = r'(x\^\d+|x|\d+\.\d+|\d+|[+\-*/§%^()])'  # добавлен § и %
    tokens = re.findall(token_pattern, expression)

    # === Обработка унарных минусов ===
    processed = []
    for i, tok in enumerate(tokens):
        if tok == '-':
            # Унарный минус — если стоит в начале или после оператора или открывающей скобки
            if i == 0 or tokens[i - 1] in {'+', '-', '*', '/', '§', '%', '^', '('}:
                if i + 1 < len(tokens):
                    nxt = tokens[i + 1]
                    combined = '-' + nxt
                    processed.append(combined)
                    tokens[i + 1] = ''  # помечаем, что этот токен уже использован
                continue
        if tok != '':
            processed.append(tok)

    # === Алгоритм сортировочной станции ===
    output = []
    stack = []

    precedence = {'^': 4, '*': 3, '/': 3, '§': 3, '%': 3, '+': 2, '-': 2}  # добавлены § и %
    right_assoc = {'^'}

    for token in processed:
        if re.fullmatch(r'-?\d+(\.\d+)?', token) or re.fullmatch(r'-?x(\^\d+)?', token):
            output.append(token)
        elif token in precedence:
            while stack and stack[-1] in precedence:
                top = stack[-1]
                if (token not in right_assoc and precedence[token] <= precedence[top]) or \
                        (token in right_assoc and precedence[token] < precedence[top]):
                    output.append(stack.pop())
                else:
                    break
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # убрать '('

    while stack:
        output.append(stack.pop())

    # Заменяем временный символ § обратно на //
    result = []
    for token in output:
        if token == '§':
            result.append('//')
        else:
            result.append(token)

    return result


def eval_rpn_p(tokens):
    stack = []

    for t in tokens:
        if t in ['+', '-', '*', '/', '%']:
            b = stack.pop()
            a = stack.pop()
            if t == '+':
                if type(a) == int:
                    a = TRANS_INT_Q(a)
                if type(b) == int:
                    b = TRANS_INT_Q(b)
                if type(a) == type(b) and type(a) != str:
                    stack.append(a + b)
                else:
                    if type(a) == Rational:
                        a = TRANS_Q_P(a)
                    if type(b) == Rational:
                        b = TRANS_Q_P(b)
                    stack.append(a + b)
            elif t == '%':
                if type(a) == int or type(b) == int:
                    raise TypeError
                if type(a) == Rational or type(b) == Rational:
                    raise TypeError
                stack.append(a % b)
            elif t == '-':
                if type(a) == int:
                    a = TRANS_INT_Q(a)
                if type(b) == int:
                    b = TRANS_INT_Q(b)
                if type(a) == type(b) and type(a) != str:
                    stack.append(a - b)
                else:
                    if type(a) == Rational:
                        a = TRANS_Q_P(a)
                    if type(b) == Rational:
                        b = TRANS_Q_P(b)
                    stack.append(a - b)
            elif t == '*':
                if type(a) == int:
                    a = TRANS_INT_Q(a)
                if type(b) == int:
                    b = TRANS_INT_Q(b)
                if type(a) == type(b) and type(a) != str:
                    stack.append(a * b)
                else:
                    if type(a) == Rational:
                        a = TRANS_Q_P(a)
                    if type(b) == Rational:
                        b = TRANS_Q_P(b)
                    stack.append(a * b)
            elif t == '/':
                if type(a) == int:
                    a = TRANS_INT_Q(a)
                if type(b) == int:
                    b = TRANS_INT_Q(b)
                if type(a) == type(b) and type(a) != str:
                    if type(a) == Polynomial:
                        stack.append(a // b)
                    else:
                        stack.append(a / b)

                else:
                    if type(a) == Rational:
                        a = TRANS_Q_P(a)
                    if type(b) == Rational:
                        b = TRANS_Q_P(b)
                    stack.append(a // b)
            elif t == '^':
                stack.append(a ** b)
        else:
            if is_number(t):
                stack.append(TRANS_INT_Q(int(t)))
            elif 'x' in t:
                stack.append(TRANS_STR_P(t))
            else:
                raise SyntaxError
    return stack[-1]


def eval_rpn_n(tokens):
    stack = []

    for t in tokens:
        if t in ['+', '-', '*', '/', '//', '%']:
            b = stack.pop()
            a = stack.pop()
            if t == '+':
                stack.append(a + b)
            elif t == '-':
                stack.append(a - b)
            elif t == '*':
                stack.append(a * b)
            elif t == '//':
                stack.append(a // b)
            elif t == '%':
                stack.append((a % b))
        else:
            stack.append(TRANS_INT_N(int(t)))

    return stack[-1]

def eval_rpn_z(tokens):
    stack = []

    for t in tokens:
        if t in ['+', '-', '*', '/', '//', '%']:
            b = stack.pop()
            a = stack.pop()
            if t == '+':
                stack.append(a + b)
            elif t == '-':
                stack.append(a - b)
            elif t == '*':
                stack.append(a * b)
            elif t == '//':
                stack.append(a // b)
            elif t == '%':
                stack.append((a % b))
        else:
            stack.append(TRANS_INT_Z(int(t)))

    return stack[-1]

def eval_rpn_q(tokens):
    stack = []

    for t in tokens:
        if t in ['+', '-', '*', '/', '//', '%']:
            b = stack.pop()
            a = stack.pop()
            if t == '+':
                stack.append(a + b)
            elif t == '-':
                stack.append(a - b)
            elif t == '*':
                stack.append(a * b)
            elif t == '/':
                stack.append(a / b)
        else:
            stack.append(TRANS_INT_Q(int(t)))

    return stack[-1]

def to_rpn_complex(expression: str):
    """Преобразует выражение с комплексными числами в RPN"""
    expression = expression.replace(' ', '')

    # Заменяем 'i' на '(0+1i)'
    expression = re.sub(r'(?<!\d)(?<!\.)(?<!\))i', '(0+1i)', expression)
    expression = re.sub(r'(\d+)i', r'\1*(0+1i)', expression)
    
    # Заменяем '-i' на '-(0+1i)'
    expression = expression.replace('-i', '-(0+1i)')

    token_pattern = r'(\(0[+-]1i\)|\d+\.\d+|\d+|[+\-*/^()])'
    tokens = re.findall(token_pattern, expression)

    processed = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok == '-':
            if i == 0 or tokens[i - 1] in {'+', '-', '*', '/', '^', '('}:
                # Объединяем с следующим токеном
                if i + 1 < len(tokens):
                    nxt = tokens[i + 1]
                    if nxt not in ['+', '-', '*', '/', '^', ')']:
                        combined = '-' + nxt
                        processed.append(combined)
                        i += 1
                    else:
                        processed.append(tok)
                else:
                    processed.append(tok)
            else:
                processed.append(tok)
        elif tok != '':
            processed.append(tok)
        i += 1

    output = []
    stack = []
    
    precedence = {'^': 4, '*': 3, '/': 3, '+': 2, '-': 2}
    right_assoc = {'^'}
    
    for token in processed:
        if re.fullmatch(r'-?\d+(\.\d+)?', token) or token in ['(0+1i)', '(0-1i)']:
            output.append(token)
        elif token in precedence:
            while stack and stack[-1] in precedence:
                top = stack[-1]
                if (token not in right_assoc and precedence[token] <= precedence[top]) or \
                        (token in right_assoc and precedence[token] < precedence[top]):
                    output.append(stack.pop())
                else:
                    break
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
    
    while stack:
        output.append(stack.pop())
    
    # Преобразуем обратно в удобный формат
    result = []
    for token in output:
        if token == '(0+1i)':
            result.append('1i')
        elif token == '(0-1i)':
            result.append('-1i')
        elif token.startswith('(') and token.endswith(')'):
            # Это уже комплексное число в скобках
            result.append(token)
        else:
            result.append(token)
    
    return result

def parse_complex_token(token):
    """Парсит токен в комплексное число"""
    
    if token == '1i':
        real = Rational(Integer(0, 0, [0]), Natural(0, [1]))
        imag = Rational(Integer(0, 0, [1]), Natural(0, [1]))
        return Complex(real, imag)
    elif token == '-1i':
        real = Rational(Integer(0, 0, [0]), Natural(0, [1]))
        imag = Rational(Integer(1, 0, [1]), Natural(0, [1]))
        return Complex(real, imag)
    else:
        try:
            num = int(token)
            num_int = Integer(0 if num >= 0 else 1,
                             len(str(abs(num))) - 1,
                             [int(d) for d in str(abs(num))])
            real = Rational(num_int, Natural(0, [1]))
            imag = Rational(Integer(0, 0, [0]), Natural(0, [1]))
            return Complex(real, imag)
        except:
            raise ValueError(f"Не удалось распознать токен как число: {token}")

def eval_rpn_complex(tokens):
    """Вычисляет RPN для комплексных выражений"""
    stack = []
    
    for t in tokens:
        if t in ['+', '-', '*', '/', '^']:
            if len(stack) < 2:
                raise ValueError(f"Недостаточно операндов для операции {t}")
            b = stack.pop()
            a = stack.pop()
            
            if t == '+':
                result = a + b
            elif t == '-':
                result = a - b
            elif t == '*':
                result = a * b
            elif t == '/':
                result = a / b
            elif t == '^':
                if isinstance(b, Complex):
                    if b.imaginary.numerator.A == [0]:
                        try:
                            numer_str = ''.join(map(str, b.real.numerator.A))
                            denom_str = ''.join(map(str, b.real.denominator.A))
                            
                            numerator = int(numer_str) if numer_str else 0
                            denominator = int(denom_str) if denom_str else 1
                            
                            if b.real.numerator.s == 1:
                                numerator = -numerator
                            
                            power_value = numerator // denominator
                            
                            if power_value < 0:
                                raise ValueError("Степень должна быть натуральным числом")

                            from rational_algebra.Natural import Natural
                            power_str = str(power_value)
                            power_digits = [int(d) for d in power_str]
                            n_natural = Natural(len(power_digits)-1, power_digits)
                            
                            result = a.POW_CN_C(n_natural)
                        except Exception as e:
                            raise ValueError(f"Ошибка возведения в степень: {e}")
                    else:
                        raise ValueError("Степень должна быть действительным числом")
                else:
                    raise ValueError("Степень должна быть комплексным числом")
            
            stack.append(result)
        else:
            # Парсим число
            try:
                stack.append(parse_complex_token(t))
            except Exception as e:
                raise
    
    return stack[-1] if stack else None

def parse_complex_polynomial_token(token):
    """Парсит токен для комплексного полинома"""
    if token == 'i':
        return Complex(Rational(Integer(0, 0, [1]), Natural(0, [1])), 
                       Rational(Integer(0, 0, [0]), Natural(0, [1])))
    elif token.startswith('-i'):
        return Complex(Rational(Integer(0, 0, [1]), Natural(0, [1])), 
                       Rational(Integer(1, 0, [1]), Natural(0, [1])))
    elif 'i' in token:
        parts = token.split('i')
        real = int(parts[0]) if parts[0] else 0
        return Complex(TRANS_INT_Q(real), 
                       Rational(Integer(0, 0, [1]), Natural(0, [1])))
    else:
        num = int(token)
        return Complex(TRANS_INT_Q(num), 
                       Rational(Integer(0, 0, [0]), Natural(0, [1])))

def eval_rpn_complex_poly(tokens):
    """Вычисляет RPN для комплексных полиномов - УПРОЩЕННАЯ ВЕРСИЯ"""
    stack = []
    
    for t in tokens:
        
        if t in ['+', '-', '*', '/', '%']:
            if len(stack) < 2:
                raise ValueError(f"Недостаточно операндов для операции {t}")
            b = stack.pop()
            a = stack.pop()
            
            if t == '+':
                result = a + b
            elif t == '-':
                result = a - b
            elif t == '*':
                result = a * b
            elif t == '/':
                result = a // b
            elif t == '%':
                result = a % b
            
            stack.append(result)
            
        else:
            # Парсим токен
            if t.startswith('(0+') and t.endswith('i)'):
                sign = t[3]
                imag_str = t[4:-2]
                imag = int(imag_str) if imag_str else 1
                if sign == '-':
                    imag = -imag
                
                real = TRANS_INT_Q(0)
                imag_rational = TRANS_INT_Q(imag)
                coeff = Complex(real, imag_rational)
                coeffs = [coeff]
                poly = ComplexPolynomial(0, coeffs)
                stack.append(poly)
                
            elif 'x' in t:
                if '^' in t:
                    parts = t.split('^')
                    coeff_part = parts[0].replace('x', '')
                    degree = int(parts[1])

                    if not coeff_part or coeff_part == '+':
                        coeff_val = 1
                    elif coeff_part == '-':
                        coeff_val = -1
                    else:
                        coeff_val = int(coeff_part)

                    coeff = Complex(TRANS_INT_Q(coeff_val), TRANS_INT_Q(0))

                    zero = Complex(TRANS_INT_Q(0), TRANS_INT_Q(0))
                    coeffs = [coeff] + [zero] * degree
                    poly = ComplexPolynomial(degree, coeffs)
                    
                else:
                    coeff_part = t.replace('x', '')
                    
                    if not coeff_part or coeff_part == '+':
                        coeff_val = 1
                    elif coeff_part == '-':
                        coeff_val = -1
                    else:
                        coeff_val = int(coeff_part)

                    coeff = Complex(TRANS_INT_Q(coeff_val), TRANS_INT_Q(0))

                    zero = Complex(TRANS_INT_Q(0), TRANS_INT_Q(0))
                    coeffs = [coeff, zero]
                    poly = ComplexPolynomial(1, coeffs)
                
                stack.append(poly)
                
            else:
                num = int(t)
                coeff = Complex(TRANS_INT_Q(num), TRANS_INT_Q(0))
                coeffs = [coeff]
                poly = ComplexPolynomial(0, coeffs)
                stack.append(poly)
    
    if len(stack) != 1:
        raise ValueError(f"В стеке осталось {len(stack)} элементов, ожидался 1")
    
    return stack[0]

def parse_complex_str(s):
    """Парсит строку вида 'a+bi', '(a+bi)', '-5i' в Complex"""
    s = s.strip()

    if s.startswith('(') and s.endswith(')'):
        s = s[1:-1]
    
    if s == 'i':
        return Complex(Rational(Integer(0, 0, [0]), Natural(0, [1])), 
                       Rational(Integer(0, 0, [1]), Natural(0, [1])))
    elif s == '-i':
        return Complex(Rational(Integer(0, 0, [0]), Natural(0, [1])), 
                       Rational(Integer(1, 0, [1]), Natural(0, [1])))

    if 'i' in s:
        parts = s.replace('+', ' +').replace('-', ' -').split()
        
        real_part = 0
        imag_part = 0
        
        for part in parts:
            if part == '':
                continue
                
            if 'i' in part:
                # Мнимая часть
                imag_str = part.replace('i', '').strip()
                if imag_str == '' or imag_str == '+':
                    imag_part = 1
                elif imag_str == '-':
                    imag_part = -1
                else:
                    imag_part = int(imag_str)
            else:
                real_part = int(part)

        real_rational = TRANS_INT_Q(real_part)

        imag_sign = 0 if imag_part >= 0 else 1
        imag_abs = abs(imag_part)
        imag_digits = [int(d) for d in str(imag_abs)]
        imag_int = Integer(imag_sign, len(imag_digits)-1, imag_digits)
        imag_rational = Rational(imag_int, Natural(0, [1]))
        
        return Complex(real_rational, imag_rational)
    else:
        num = int(s)
        return Complex(TRANS_INT_Q(num), 
                       Rational(Integer(0, 0, [0]), Natural(0, [1])))
    
def to_rpn_complex_poly(expression: str):
    """Преобразует выражение с комплексными полиномами в RPN - УПРОЩЕННАЯ ВЕРСИЯ"""
    expression = expression.replace(' ', '')

    expression = re.sub(r'(?<!\d)i(?!\d)', '(0+1i)', expression)

    expression = re.sub(r'(\d+)i', r'\1*(0+1i)', expression)

    expression = re.sub(r'-i', '-(0+1i)', expression)

    expression = re.sub(r'(?<=\d)(?=x)', '*', expression)

    expression = re.sub(r'(?<=\))(?=x)', '*', expression)

    token_pattern = r'(\(0[+-]\d+i\)|x\^\d+|x|\d+\.\d+|\d+|[+\-*/^()])'
    tokens = re.findall(token_pattern, expression)

    processed = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok == '-':
            if i == 0 or tokens[i - 1] in {'+', '-', '*', '/', '^', '('}:
                if i + 1 < len(tokens):
                    nxt = tokens[i + 1]
                    if nxt not in ['+', '-', '*', '/', '^', ')']:
                        combined = '-' + nxt
                        processed.append(combined)
                        i += 1
                    else:
                        processed.append(tok)
                else:
                    processed.append(tok)
            else:
                processed.append(tok)
        elif tok != '':
            processed.append(tok)
        i += 1

    output = []
    stack = []

    precedence = {'^': 4, '*': 3, '/': 3, '+': 2, '-': 2}
    right_assoc = {'^'}

    for token in processed:
        if re.fullmatch(r'-?\d+(\.\d+)?', token) or re.fullmatch(r'-?x(\^\d+)?', token) or \
           re.fullmatch(r'\(0[+-]\d+i\)', token):
            output.append(token)
        elif token in precedence:
            while stack and stack[-1] in precedence:
                top = stack[-1]
                if (token not in right_assoc and precedence[token] <= precedence[top]) or \
                   (token in right_assoc and precedence[token] < precedence[top]):
                    output.append(stack.pop())
                else:
                    break
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()

    while stack:
        output.append(stack.pop())

    return output