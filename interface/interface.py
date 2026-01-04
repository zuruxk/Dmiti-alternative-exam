import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from parser import *
from rational_algebra.Polynomial import Polynomial
from complex_algebra.Complex import Complex
from rational_algebra.TRANS.TRANS_Q_P import TRANS_Q_P

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure




class CalculatorSelector:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Выбор калькулятора")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()


        window_width = int(screen_width * 0.3)
        window_height = int(screen_height * 0.5)

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.minsize(int(screen_width * 0.25), int(screen_height * 0.4))  # Минимальный размер
        self.window.resizable(True, True)

        self.create_widgets()

    def run(self):
        """Запускает приложение"""
        self.window.mainloop()

    def create_widgets(self):
        title_label = tk.Label(self.window, text="Выберите тип калькулятора",
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)

        # Кнопки для выбора типа калькулятора
        button_style = {'font': ('Arial', 14), 'height': 2, 'width': 20}

        natural_btn = tk.Button(self.window, text="Натуральные числа",
                                command=self.open_natural_calculator, **button_style)
        natural_btn.pack(pady=5)

        integer_btn = tk.Button(self.window, text="Целые числа",
                                command=self.open_integer_calculator, **button_style)
        integer_btn.pack(pady=5)

        rational_btn = tk.Button(self.window, text="Рациональные числа",
                                 command=self.open_rational_calculator, **button_style)
        rational_btn.pack(pady=5)

        polynomial_btn = tk.Button(self.window, text="Полиномы",
                                   command=self.open_polynomial_calculator, **button_style)
        polynomial_btn.pack(pady=5)

        complex_poly_btn = tk.Button(self.window, text="Комплексные полиномы",
                                     command=self.open_complex_polynomial_calculator, **button_style)
        complex_poly_btn.pack(pady=5)

        complex_btn = tk.Button(self.window, text="Комплексные числа",
                                command=self.open_complex_calculator, **button_style)
        complex_btn.pack(pady=5)

    def open_natural_calculator(self):
        geometry = self.window.geometry()
        self.window.destroy()
        calculator = Calculator("natural")
        calculator.window.geometry(geometry)
        calculator.run()

    def open_integer_calculator(self):
        geometry = self.window.geometry()
        self.window.destroy()
        calculator = Calculator("integer")
        calculator.window.geometry(geometry)
        calculator.run()

    def open_rational_calculator(self):
        geometry = self.window.geometry()
        self.window.destroy()
        calculator = Calculator("rational")
        calculator.window.geometry(geometry)
        calculator.run()

    def open_polynomial_calculator(self):
        geometry = self.window.geometry()
        self.window.destroy()
        calculator = Calculator("polynomial")
        calculator.window.geometry(geometry)
        calculator.run()

    def open_complex_polynomial_calculator(self):
        geometry = self.window.geometry()
        self.window.destroy()
        calculator = ComplexPolynomialCalculator("complex_polynomial")
        calculator.window.geometry(geometry)
        calculator.run()

    def open_complex_calculator(self):
        geometry = self.window.geometry()
        self.window.destroy()
        calculator = ComplexCalculator("complex")
        calculator.window.geometry(geometry)
        calculator.run()


class Calculator:
    def __init__(self, calc_type):
        self.calc_type = calc_type
        self.window = tk.Tk()

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()


        window_width = int(screen_width * 0.22)
        window_height = int(screen_height * 0.51)

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.minsize(window_width, window_height)
        self.window.resizable(True, True)


        titles = {
            "natural": "Калькулятор натуральных чисел",
            "integer": "Калькулятор целых чисел",
            "rational": "Калькулятор рациональных чисел",
            "polynomial": "Калькулятор полиномов"
        }
        self.window.title(titles.get(calc_type, "Калькулятор"))

        self.expression = ""

        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.window)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.columnconfigure(3, weight=1)
        main_frame.columnconfigure(4, weight=1)

        type_label = tk.Label(main_frame,
                              text=f"Тип: {self.get_calc_type_name()}",
                              font=('Arial', 10, 'bold'),
                              fg='blue')
        type_label.grid(row=0, column=0, columnspan=5, pady=(10, 5), sticky='ew')

        input_frame = tk.Frame(main_frame)
        input_frame.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky='ew')
        
        input_label = tk.Label(input_frame, text="Ввод:", font=('Arial', 10))
        input_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.display_input = tk.Entry(input_frame, font=('Arial', 14))
        self.display_input.pack(side=tk.LEFT, expand=True, fill='x')
        self.display_input.bind('<Return>', lambda e: self.show_result())
        self.display_input.bind('<Control-v>', lambda e: self.paste_from_clipboard())
        self.display_input.bind('<Control-c>', lambda e: self.copy_to_clipboard())

        output_frame = tk.Frame(main_frame)
        output_frame.grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky='ew')
        
        output_label = tk.Label(output_frame, text="Результат:", font=('Arial', 10))
        output_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.display_output = tk.Entry(output_frame, font=('Arial', 14), state='readonly',
                                      readonlybackground='white', fg='blue')
        self.display_output.pack(side=tk.LEFT, expand=True, fill='x')
        self.display_output.bind('<Control-c>', lambda e: self.copy_result_to_clipboard())

        copy_paste_frame = tk.Frame(main_frame)
        copy_paste_frame.grid(row=3, column=0, columnspan=5, pady=(0, 10), sticky='ew')
        
        copy_btn = tk.Button(copy_paste_frame, text="Копировать результат",
                            font=('Arial', 10), command=self.copy_result_to_clipboard,
                            bg='lightblue')
        copy_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        paste_btn = tk.Button(copy_paste_frame, text="Вставить в поле ввода",
                             font=('Arial', 10), command=self.paste_from_clipboard,
                             bg='lightgreen')
        paste_btn.pack(side=tk.LEFT)

        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=5, sticky='nsew', pady=10)

        main_frame.rowconfigure(4, weight=1)

        for i in range(5):
            button_frame.columnconfigure(i, weight=1)
        for i in range(5):
            button_frame.rowconfigure(i, weight=1)

        buttons = [
            '7', '8', '9', '/', 'i',
            '4', '5', '6', '*', '(',
            '1', '2', '3', '-', ')',
            '0', '.', '=', '+', 'C',
            'x²', 'xⁿ', '<—', '//', '^'
        ]

        row = 0
        col = 0

        for button in buttons:
            if button == '=':
                cmd = self.show_result
            elif button == 'C':
                cmd = self.clear
            elif button == '<—':
                cmd = self.backspace
            elif button in ['x²', 'x³', 'xⁿ']:
                cmd = lambda x=button: self.add_power(x)
            else:
                cmd = lambda x=button: self.add_to_expression(x)

            btn = tk.Button(
                button_frame,
                text=button,
                font=('Arial', 12),
                command=cmd
            )

            btn.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')

            col += 1
            if col > 4:
                col = 0
                row += 1

        bottom_frame = tk.Frame(main_frame)
        bottom_frame.grid(row=5, column=0, columnspan=5, sticky='ew', pady=10)

        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)

        back_btn = tk.Button(
            bottom_frame,
            text="Назад к выбору",
            font=('Arial', 12),
            command=self.back_to_selector,
            height=2,
            bg='lightgreen'
        )
        back_btn.grid(row=0, column=0, sticky='ew', padx=(0, 5))

        calc_btn = tk.Button(
            bottom_frame,
            text="Вычислить",
            font=('Arial', 12),
            command=self.show_result,
            height=2,
            bg='lightblue'
        )
        calc_btn.grid(row=0, column=1, sticky='ew', padx=(5, 0))

        self.update_display()

    def copy_result_to_clipboard(self):
        """Копирует результат в буфер обмена через Tk"""
        result = self.display_output.get()
        if result:
            try:
                # Очищаем буфер и добавляем результат
                self.window.clipboard_clear()
                self.window.clipboard_append(result)
                # Сохраняем для других приложений
                self.window.update()
                messagebox.showinfo("Успех", "Результат скопирован в буфер обмена")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось скопировать: {e}")
        else:
            messagebox.showwarning("Предупреждение", "Нет результата для копирования")

    def paste_from_clipboard(self):
        """Вставляет текст из буфера обмена в поле ввода"""
        try:
            # Получаем текст из буфера Tk
            clipboard_text = self.window.clipboard_get()
            if clipboard_text:
                current_text = self.display_input.get()
                self.display_input.delete(0, tk.END)
                self.display_input.insert(0, current_text + clipboard_text)
        except tk.TclError:
            # Если в буфере нет текстовых данных
            messagebox.showwarning("Предупреждение", "В буфере обмена нет текста")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось вставить: {e}")

    def get_calc_type_name(self):
        """Возвращает читаемое название типа калькулятора"""
        names = {
            "natural": "Натуральные числа",
            "integer": "Целые числа",
            "rational": "Рациональные числа",
            "polynomial": "Полиномы"
        }
        return names.get(self.calc_type, "Неизвестный тип")

    def add_to_expression(self, value):
        """Добавляет символ к выражению в поле ввода"""
        if self.calc_type in ["natural", "integer"] and len(value) == 1 and value[0] == '/':
            messagebox.showwarning("Ошибка", "В данном калькуляторе нельзя использовать операцию деления")
            return
        elif self.calc_type in ["rational", "polynomial"] and value[:2] == '//':
            messagebox.showwarning("Ошибка", "В данном калькуляторе нельзя использовать операцию целочисленного деления")
            return
        elif self.calc_type in ["rational"] and value[0] == '%':
            messagebox.showwarning("Ошибка", "В данном калькуляторе нельзя использовать операцию остатка от деления")
            return

        current_text = self.display_input.get()
        self.display_input.delete(0, tk.END)
        self.display_input.insert(0, current_text + str(value))

    def add_power(self, power_type):
        """Добавляет степень переменной в поле ввода"""
        if self.calc_type in ["natural","integer", "rational"]:
            messagebox.showwarning("Ошибка", "В данном калькуляторе нельзя использовать переменную 'x'")
            return
        
        current_text = self.display_input.get()
        if power_type == 'x²':
            self.display_input.insert(tk.END, 'x^2')
        elif power_type == 'x³':
            self.display_input.insert(tk.END, 'x^3')
        elif power_type == 'xⁿ':
            self.display_input.insert(tk.END, 'x^')

    def clear(self):
        """Очищает оба поля"""
        self.display_input.delete(0, tk.END)
        self.display_output.config(state='normal')
        self.display_output.delete(0, tk.END)
        self.display_output.config(state='readonly')

    def backspace(self):
        """Удаляет последний символ из поля ввода"""
        current_text = self.display_input.get()
        self.display_input.delete(0, tk.END)
        self.display_input.insert(0, current_text[:-1])

    def show_result(self):
        """Вычисляет результат и показывает его в поле вывода"""
        expression = self.display_input.get()
        if expression:
            try:
                # Вычисляем результат
                result = self.process_expression(expression)
                
                # Выводим результат в поле вывода
                self.display_output.config(state='normal')
                self.display_output.delete(0, tk.END)
                self.display_output.insert(0, str(result))
                self.display_output.config(state='readonly')
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка вычисления: {e}")
        else:
            messagebox.showwarning("Предупреждение", "Введите выражение")

    def update_display(self):
        pass

    def process_expression(self, expr):
        """Обрабатывает выражение в зависимости от типа калькулятора"""

        if self.calc_type == "natural":
            ans = eval_rpn_n(to_rpn(expr))
            return f"{ans.show()}"
        elif self.calc_type == "integer":
            ans = eval_rpn_z(to_rpn(expr))
            return f"{ans.show()}"
        elif self.calc_type == "rational":
            ans = eval_rpn_q(to_rpn(expr))
            return f"{ans.show()}"
        elif self.calc_type == "polynomial":
            ans = eval_rpn_p(to_rpn(expr))
            if type(ans) != Polynomial:
                ans = TRANS_Q_P(ans)
            return f"{ans.show()}"

        return 'answer'

    def back_to_selector(self):
        """Возврат к окну выбора калькулятора"""
        geometry = self.window.geometry()
        self.window.destroy()
        selector = CalculatorSelector()
        selector.window.geometry(geometry)
        selector.window.mainloop()

    def run(self):
        """Запускает приложение"""
        self.window.mainloop()

class ComplexCalculator(Calculator):
    def __init__(self, calc_type):
        self.calc_type = calc_type
        self.window = tk.Tk()
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = int(screen_width * 0.22)
        window_height = int(screen_height * 0.51)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.minsize(window_width, window_height)
        self.window.resizable(True, True)
        self.window.title("Калькулятор комплексных чисел")
        
        self.expression = ""
        self.current_result = None
        self.fig = None
        self.canvas = None
        
        # Создаем наш интерфейс с графиком
        self.create_widgets()
        
    def create_widgets(self):
        main_container = tk.Frame(self.window)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_container)
        left_frame.pack(side='left', fill='both', expand=True)

        right_frame = tk.Frame(main_container)
        right_frame.pack(side='right', fill='both', expand=True)
        
        self.create_calculator_widgets(left_frame)

        self.create_complex_plot(right_frame)

        self.window.update_idletasks()
    
    def create_tooltip(self, widget, text):
        """Создает всплывающую подсказку для кнопки"""
        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            label = tk.Label(self.tooltip, text=text, 
                            background="#ffffe0", relief="solid", borderwidth=1)
            label.pack()
    
        def leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def create_calculator_widgets(self, parent):
        """Создает интерфейс калькулятора в левой части"""
        left_main = tk.Frame(parent)
        left_main.pack(fill='both', expand=True)
        
        type_label = tk.Label(left_main,
                            text="Калькулятор комплексных чисел",
                            font=('Arial', 12, 'bold'),
                            fg='blue')
        type_label.pack(pady=(5, 10))

        input_frame = tk.Frame(left_main)
        input_frame.pack(pady=5, fill='x', padx=10)
        
        input_label = tk.Label(input_frame, text="Ввод:", font=('Arial', 10))
        input_label.pack(side='left', padx=(0, 5))
        
        self.display_input = tk.Entry(input_frame, font=('Arial', 14))
        self.display_input.pack(side='left', expand=True, fill='x')

        output_frame = tk.Frame(left_main)
        output_frame.pack(pady=5, fill='x', padx=10)
        
        output_label = tk.Label(output_frame, text="Результат:", font=('Arial', 10))
        output_label.pack(side='left', padx=(0, 5))
        
        self.display_output = tk.Entry(output_frame, font=('Arial', 14), state='readonly',
                                    readonlybackground='white', fg='blue')
        self.display_output.pack(side='left', expand=True, fill='x')

        copy_paste_frame = tk.Frame(left_main)
        copy_paste_frame.pack(pady=(0, 10), fill='x', padx=10)
        
        copy_btn = tk.Button(copy_paste_frame, text="Копировать результат",
                            font=('Arial', 10), command=self.copy_result_to_clipboard,
                            bg='lightblue')
        copy_btn.pack(side='left', padx=(0, 5))
        
        paste_btn = tk.Button(copy_paste_frame, text="Вставить в поле ввода",
                            font=('Arial', 10), command=self.paste_from_clipboard,
                            bg='lightgreen')
        paste_btn.pack(side='left')
        
        calc_frame = tk.Frame(left_main)
        calc_frame.pack(pady=10, padx=10)
        
        # Создаем стандартную клавиатуру калькулятора
        buttons = [
            '7', '8', '9', '/', 'i',
            '4', '5', '6', '*', '(',
            '1', '2', '3', '-', ')',
            '0', '.', '=', '+', 'C',
            '^', '²', '<—', '√', '||'
        ]
        
        row = 0
        col = 0
        
        for button in buttons:
            if button == '=':
                cmd = self.show_result
            elif button == 'C':
                cmd = self.clear
            elif button == '<—':
                cmd = self.backspace
            elif button == 'i':
                cmd = self.add_imaginary_unit
            elif button == '²':
                cmd = lambda: self.add_to_input('^2')
            elif button == '^':
                cmd = lambda: self.add_to_input('^')
            elif button == '√':
                cmd = self.calculate_root
            elif button == '||':
                cmd = lambda: self.complex_operation('Abs')  # Модуль
            else:
                cmd = lambda x=button: self.add_to_input(x)
            
            btn = tk.Button(
                calc_frame,
                text=button,
                font=('Arial', 12),
                command=cmd,
                width=4,
                height=2
            )
            
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
            
            col += 1
            if col > 4:
                col = 0
                row += 1
        
        special_frame = tk.Frame(left_main)
        special_frame.pack(pady=10, padx=10, fill='x')

        special_buttons_row1 = [
            ('Conj', 'Conj', 'Сопряженное'),
            ('Inv', '1/z', 'Обратное'),
            ('Re', 'Re', 'Действительная часть'),
            ('Im', 'Im', 'Мнимая часть'),
            ('Exp', 'Exp', 'Показательная форма')
        ]
        
        row1_frame = tk.Frame(special_frame)
        row1_frame.pack(fill='x')
        
        for command, text, tooltip in special_buttons_row1:
            btn = tk.Button(
                row1_frame,
                text=text,
                font=('Arial', 10),
                command=lambda cmd=command: self.complex_operation(cmd),
                width=8,
                height=2
            )
            btn.pack(side='left', padx=2, pady=2, expand=True, fill='x')
            self.create_tooltip(btn, tooltip)

        special_buttons_row2 = [
            ('Cos', 'cos θ', 'Косинус аргумента'),
            ('Sin', 'sin θ', 'Синус аргумента'),
            ('Tan', 'tan θ', 'Тангенс аргумента'),
            ('Norm', 'Norm', 'Нормализация'),
            ('Pow', 'z^n', 'Возведение в степень')
        ]
        
        row2_frame = tk.Frame(special_frame)
        row2_frame.pack(fill='x')
        
        for command, text, tooltip in special_buttons_row2:
            btn = tk.Button(
                row2_frame,
                text=text,
                font=('Arial', 10),
                command=lambda cmd=command: self.complex_operation(cmd),
                width=8,
                height=2
            )
            btn.pack(side='left', padx=2, pady=2, expand=True, fill='x')
            self.create_tooltip(btn, tooltip)
        
        nav_frame = tk.Frame(left_main)
        nav_frame.pack(pady=10, padx=10, fill='x')
        
        back_btn = tk.Button(
            nav_frame,
            text="Назад к выбору",
            font=('Arial', 12),
            command=self.back_to_selector,
            height=2,
            bg='lightgreen'
        )
        back_btn.pack(side='left', padx=(0, 5), expand=True, fill='x')
        
        calc_btn = tk.Button(
            nav_frame,
            text="Вычислить",
            font=('Arial', 12),
            command=self.show_result,
            height=2,
            bg='lightblue'
        )
        calc_btn.pack(side='left', expand=True, fill='x')

    def calculate_root(self):
        """Вычисляет корень n-ой степени"""
        if not self.current_result:
            messagebox.showwarning("Предупреждение", "Сначала введите комплексное число и нажмите '='")
            return
        
        try:
            n = simpledialog.askinteger("Извлечение корня", 
                                    "Введите степень корня n:",
                                    parent=self.window,
                                    minvalue=1)
            if n is not None:
                # from rational_algebra.Natural import Natural
                n_digits = [int(d) for d in str(n)]
                n_nat = Natural(len(n_digits)-1, n_digits)
                
                result = self.current_result.ROOT_CN_C(n_nat)
                text = f"{result.show_alg()}"

                self.display_output.config(state='normal')
                self.display_output.delete(0, tk.END)
                self.display_output.insert(0, text)
                self.display_output.config(state='readonly')
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка извлечения корня: {e}")

    def add_imaginary_unit(self):
        """Добавляет мнимую единицу в выражение"""  
        self.add_to_input('i')

    def create_complex_plot(self, parent):
        """Создает график комплексной плоскости - КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ"""
        try:
            plot_frame = tk.Frame(parent)
            plot_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            plot_label = tk.Label(plot_frame, text="Комплексная плоскость",
                                font=('Arial', 12, 'bold'))
            plot_label.pack()

            self.fig = Figure(figsize=(4, 4), dpi=80)
            self.ax = self.fig.add_subplot(111)  # ось тоже сохраняем в self
            
            # Настройка осей...
            self.ax.axhline(y=0, color='k', linewidth=0.5)
            self.ax.axvline(x=0, color='k', linewidth=0.5)
            self.ax.grid(True, alpha=0.3)
            self.ax.set_xlabel('Re (действительная часть)')
            self.ax.set_ylabel('Im (мнимая часть)')
            self.ax.set_title('Введите комплексное число')
            self.ax.set_xlim(-5, 5)
            self.ax.set_ylim(-5, 5)
            self.ax.set_aspect('equal', adjustable='box')

            self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            print(f"Ошибка создания графика: {e}")
            import traceback
            traceback.print_exc()
            self.fig = None
            self.canvas = None
            # Создаем заглушку
            error_label = tk.Label(parent, 
                                text="Ошибка создания графика",
                                fg='red')
            error_label.pack()

    def update_plot(self, real, imag):
        """Обновляет график с новым комплексным числом - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        try:
            if self.canvas is None:
                print("Canvas не инициализирован")
                return
            
            if self.fig is None:
                print("Фигура не инициализирована")
                return

            self.ax.clear()

            self.ax.axhline(y=0, color='k', linewidth=0.5)
            self.ax.axvline(x=0, color='k', linewidth=0.5)
            self.ax.grid(True, alpha=0.3)

            self.ax.quiver(0, 0, real, imag, 
                        angles='xy', scale_units='xy', scale=1,
                        color='red', width=0.005, headwidth=5)

            self.ax.plot(real, imag, 'ro', markersize=10)

            max_val = max(abs(real), abs(imag), 1) * 1.5
            self.ax.set_xlim(-max_val, max_val)
            self.ax.set_ylim(-max_val, max_val)

            self.ax.set_aspect('equal', adjustable='box')

            self.canvas.draw()
        
        except Exception as e:
            print(f"Ошибка обновления графика: {e}")
            import traceback
            traceback.print_exc()
    
    def complex_operation(self, operation):
        """Выполняет специальную операцию над комплексным числом"""
        if not self.current_result:
            messagebox.showwarning("Предупреждение", "Сначала введите комплексное число и нажмите '='")
            return
        
        try:
            if operation == 'Conj':
                result = self.current_result.CONJ_C_Z()
                text = f"{result.show_alg()}"
            elif operation == 'Inv':
                result = self.current_result.INV_C_С()
                text = f"{result.show_alg()}"
            elif operation == 'Re':
                result = self.current_result.RE_C_Q()
                text = f"{result.show()}"
            elif operation == 'Im':
                result = self.current_result.IM_C_Q()
                text = f"{result.show()}"
            elif operation == 'Abs':
                from rational_algebra.Natural import Natural
                result = self.current_result.ABS_C_Q().ROOT_QN_Q(Natural(0, [2]))
                text = f"{result.show()}"
            elif operation == 'Cos':
                result = self.current_result.COS_C_R()
                text = f"{result.show()}"
            elif operation == 'Sin':
                result = self.current_result.SIN_C_Q()
                text = f"{result.show()}"
            elif operation == 'Tan':
                result = self.current_result.TAN_ARG_C_Q()
                if isinstance(result, str):
                    text = f"{result}"
                else:
                    text = f"{result.show()}"
            elif operation == 'Norm':
                result = self.current_result.NORM_C_C()
                text = f"{result.show_alg()}"
            elif operation == 'Exp':
                res = self.current_result.show_exp()
                text = f"{res}"
            elif operation == 'Pow':
                power = simpledialog.askinteger("Возведение в степень", 
                                            "Введите натуральную степень n:",
                                            parent=self.window,
                                            minvalue=1)
                if power is not None:
                    from rational_algebra.Natural import Natural
                    power_digits = [int(d) for d in str(power)]
                    power_nat = Natural(len(power_digits)-1, power_digits)
                    result = self.current_result.POW_CN_C(power_nat)
                    text = f"{result.show_alg()}"
                else:
                    return
            else:
                text = f"Операция {operation} не реализована"
            
            # Обновляем поле вывода
            self.display_output.config(state='normal')
            self.display_output.delete(0, tk.END)
            self.display_output.insert(0, text)
            self.display_output.config(state='readonly')
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка операции {operation}: {e}")
    
    def process_complex_expression(self, expr):
        """Обрабатывает выражение с комплексными числами - ДОБАВЛЕН ВЫВОД ОТЛАДКИ"""
        try:
            tokens = to_rpn_complex(expr)
            
            result = eval_rpn_complex(tokens)
            
            if result is None:
                raise ValueError("Не удалось вычислить выражение")
            
            self.current_result = result
            
            try:
                real_part = result.real
                imag_part = result.imaginary
                
                real_float = self.rational_to_float(real_part)
                imag_float = self.rational_to_float(imag_part)
                
                self.update_plot(real_float, imag_float)
            except Exception as e:
                print(f"Ошибка обновления графика (но продолжаем): {e}")
                import traceback
                traceback.print_exc()
            
            return result.show_alg()
            
        except Exception as e:
            print(f"Ошибка вычисления: {e}")
            import traceback
            traceback.print_exc()
            raise ValueError(f"Ошибка вычисления: {e}")
        
    def add_to_input(self, value):
        """Добавляет символ в поле ввода"""
        current_text = self.display_input.get()
        self.display_input.delete(0, tk.END)
        self.display_input.insert(0, current_text + str(value))

    def clear(self):
        """Очищает оба поля"""
        self.display_input.delete(0, tk.END)
        self.display_output.config(state='normal')
        self.display_output.delete(0, tk.END)
        self.display_output.config(state='readonly')
        if hasattr(self, 'current_result'):
            self.current_result = None
        
        if hasattr(self, 'canvas') and self.canvas is not None:
            try:
                self.ax.clear()
                self.ax.axhline(y=0, color='k', linewidth=0.5)
                self.ax.axvline(x=0, color='k', linewidth=0.5)
                self.ax.grid(True, alpha=0.3)
                self.ax.set_xlim(-5, 5)
                self.ax.set_ylim(-5, 5)
                self.ax.set_xlabel('Re')
                self.ax.set_ylabel('Im')
                self.ax.set_title('Введите комплексное число')
                self.canvas.draw()
            except Exception as e:
                print(f"Ошибка при очистке графика: {e}")

    def backspace(self):
        """Удаляет последний символ из поля ввода"""
        current_text = self.display_input.get()
        self.display_input.delete(0, tk.END)
        self.display_input.insert(0, current_text[:-1])
    
    def add_power(self, power_type):
        """Добавляет степень переменной в поле ввода"""
        if power_type == 'x²':
            self.add_to_input('^2')
        elif power_type == 'xⁿ':
            self.add_to_input('^')

    def show_result(self):
        """Вычисляет результат для комплексных чисел - ДОБАВЛЕН ОТЛАДОЧНЫЙ ВЫВОД"""
        expression = self.display_input.get()
        
        if expression:
            try:
                result = self.process_complex_expression(expression)
                self.display_output.config(state='normal')
                self.display_output.delete(0, tk.END)
                self.display_output.insert(0, str(result))
                self.display_output.config(state='readonly')
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка вычисления: {e}")
        else:
            messagebox.showwarning("Предупреждение", "Введите выражение")

    def parse_rational(self, s):
        """Парсит строку в Rational (упрощенная версия)"""
        try:
            s = s.strip()

            if not s or s == '0':
                return Rational(Integer(0, 0, [0]), Natural(0, [1]))

            if s == 'i':
                return Rational(Integer(0, 0, [1]), Natural(0, [1]))

            from rational_algebra.TRANS.TRANS_INT_Q import TRANS_INT_Q

            if '.' not in s:
                integer_val = int(s)
                # Преобразуем в Rational через Integer
                integer_obj = Integer(0 if integer_val >= 0 else 1, 
                                    len(str(abs(integer_val))) - 1, 
                                    [int(d) for d in str(abs(integer_val))])
                return TRANS_INT_Q(integer_obj)

            else:
                parts = s.split('.')
                numerator_str = parts[0] + parts[1]
                denominator_str = '1' + '0' * len(parts[1])
                
                numerator = int(numerator_str)
                denominator = int(denominator_str)

                num_integer = Integer(0 if numerator >= 0 else 1,
                                    len(str(abs(numerator))) - 1,
                                    [int(d) for d in str(abs(numerator))])
                den_natural = Natural(len(str(denominator)) - 1,
                                    [int(d) for d in str(denominator)])
                
                return Rational(num_integer, den_natural)
                
        except Exception as e:
            raise ValueError(f"Не удалось распознать число '{s}': {e}")
        
    def rational_to_float(self, rational):
        """Преобразует Rational в float"""
        try:
            if rational is None:
                return 0.0
            
            # Получаем числитель
            if hasattr(rational, 'numerator') and hasattr(rational.numerator, 'A'):
                numerator_digits = rational.numerator.A
                if not numerator_digits or numerator_digits == [0]:
                    numerator = 0
                else:
                    numerator_str = ''.join(str(d) for d in numerator_digits)
                    numerator = int(numerator_str) if numerator_str else 0
                    
                    # Учитываем знак (0 - положительное, 1 - отрицательное)
                    if hasattr(rational.numerator, 's') and rational.numerator.s == 1:
                        numerator = -numerator
            else:
                numerator = 0

            if hasattr(rational, 'denominator') and hasattr(rational.denominator, 'A'):
                denominator_digits = rational.denominator.A
                if not denominator_digits or denominator_digits == [0]:
                    denominator = 1
                else:
                    denominator_str = ''.join(str(d) for d in denominator_digits)
                    denominator = int(denominator_str) if denominator_str else 1
            else:
                denominator = 1

            if denominator == 0:
                return float(numerator) if numerator != 0 else 0.0
            
            return numerator / denominator
        except Exception as e:
            print(f"Ошибка преобразования Rational в float: {e}")
            return 0.0

class ComplexPolynomialCalculator(Calculator):
    def __init__(self, calc_type):
        super().__init__(calc_type)
        self.window.title("Калькулятор комплексных полиномов")
    
    def copy_to_clipboard(self):
        """Копирует текст из поля ввода в буфер обмена"""
        try:
            input_text = self.display_input.get()
            if input_text:
                self.window.clipboard_clear()
                self.window.clipboard_append(input_text)
                self.window.update()
        except Exception as e:
            print(f"Ошибка копирования: {e}")
        
    def process_expression(self, expr):
        """Обрабатывает выражение для комплексных полиномов"""
        try:
            tokens = to_rpn_complex_poly(expr)

            ans = eval_rpn_complex_poly(tokens)
            
            if isinstance(ans, ComplexPolynomial):
                return f"{ans.show_alg()}"
            else:
                return f"Результат: {ans}"
                
        except Exception as e:
            print(f"Ошибка при обработке выражения: {e}")
            import traceback
            traceback.print_exc()
            return f"Ошибка: {e}"
    
    def process_complex_polynomial_expression(self, expr):
        """Обрабатывает выражение с комплексными полиномами"""
        return ComplexPolynomial(0, [Complex(Rational(Integer(0, 0, [1]), Natural(0, [1])), 
                                            Rational(Integer(0, 0, [0]), Natural(0, [1])))])
    
    def create_widgets(self):
        """Переопределяем метод для изменения кнопок"""
        super().create_widgets()

        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and "Тип:" in child.cget("text"):
                        child.config(text="Тип: Комплексные полиномы")
                        break

        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Frame):
                main_frame = widget
                break

        poly_ops_frame = tk.Frame(main_frame)
        poly_ops_frame.grid(row=6, column=0, columnspan=5, sticky='ew', pady=10)

        poly_buttons = [
            ("Значение в точке", self.evaluate_at_point),
            ("Производная", self.calculate_derivative),
        ]
        
        for i, (text, command) in enumerate(poly_buttons):
            btn = tk.Button(
                poly_ops_frame,
                text=text,
                font=('Arial', 10),
                command=command,
                height=2,
                bg='lightyellow'
            )
            btn.grid(row=0, column=i, padx=2, pady=2, sticky='ew')
            poly_ops_frame.columnconfigure(i, weight=1)

    def evaluate_at_point(self):
        """Вычисляет значение полинома в заданной точке"""
        try:
            expression = self.display_input.get()
            if not expression:
                messagebox.showwarning("Предупреждение", "Сначала введите полином")
                return

            tokens = to_rpn_complex_poly(expression)
            poly = eval_rpn_complex_poly(tokens)
            
            if not isinstance(poly, ComplexPolynomial):
                messagebox.showwarning("Предупреждение", "Введите полином")
                return

            x_value = simpledialog.askstring(
                "Значение в точке",
                "Введите значение x (комплексное число в формате a+bi):\n" +
                "Примеры: 2+3i, -1, 4i, 2.5-1.5i",
                parent=self.window
            )
            
            if x_value is None or not x_value.strip():
                return

            try:
                x_complex = parse_complex_str(x_value.strip())

                result = poly.EVAL_P_C(x_complex)

                messagebox.showinfo(
                    "Значение полинома в точке",
                    f"P({x_value}) = {result.show_alg()}\n\n" +
                    f"Действительная часть: {result.real.show()}\n" +
                    f"Мнимая часть: {result.imaginary.show()}"
                )

                self.display_output.config(state='normal')
                self.display_output.delete(0, tk.END)
                self.display_output.insert(0, f"{result.show_alg()}")
                self.display_output.config(state='readonly')
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка парсинга точки x: {e}")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка вычисления: {e}")

    def calculate_derivative(self):
        """Вычисляет производную полинома"""
        try:
            expression = self.display_input.get()
            if not expression:
                messagebox.showwarning("Предупреждение", "Сначала введите полином")
                return

            tokens = to_rpn_complex_poly(expression)
            poly = eval_rpn_complex_poly(tokens)
            
            if not isinstance(poly, ComplexPolynomial):
                messagebox.showwarning("Предупреждение", "Введите полином")
                return

            derivative = poly.DER_P_P()

            messagebox.showinfo(
                "Производная полинома",
                f"Исходный полином: {poly.show_alg()}\n\n" +
                f"Производная: {derivative.show_alg()}"
            )

            self.display_output.config(state='normal')
            self.display_output.delete(0, tk.END)
            self.display_output.insert(0, f"{derivative.show_alg()}")
            self.display_output.config(state='readonly')
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка вычисления производной: {e}")

if __name__ == "__main__":
    selector = CalculatorSelector().run()