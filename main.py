from collections import OrderedDict

from formula_parser import Parser


print('====== Система мониторинга с использованием нечеткой временной логики ======')

# variables_number = int(input('Введите количество переменных: '))

# print('Введите имена переменных:')

# for i in range(variables_number):
#     variables[input()] = 0

# print('В системе будет {} переменных: {}'.format(variables_number, ', '.join(variable_names)))

print('Определим функцию пропусков по значениям в конкретных точках; значения в точках между указанных будут убывать линейно')
avoiding_function_points_number = int(input('Введите количество точек функции пропусков, которые будут иметь значение меньше 1 но больше 0: ' ))

avoiding_function_points = {}

for i in range(avoiding_function_points_number):
    j = int(input('Введите координату j, в которой хотите определить функцию: '))
    value = float(input('Введите значение функции в данной точке, используя в качестве разделителя точку: '))
    assert(0 < value < 1)
    avoiding_function_points[j] = value

avoiding_function_points[int(input('Введите координату j, в которой функция достигнет 0: '))] = 0

# print(avoiding_function_points)

formulas_number = int(input('Введите количество формул: '))

print(
    'Синтаксис формул:\n'
    '! - не\n'
    '\\/ - или\n'
    '/\\ - и\n'
    '-> - следование\n'
    'G - всегда\n'
    'AG - всегда\n'
    'Пример формулы: G(a->(b /\\ c))\n'
)
print('Введите формулы:')

parser = Parser()

formulas = []
variables = OrderedDict()
for i in range(formulas_number):
    (formula, new_variables) = parser.parse(input())
    formulas.append(formula)
    for variable in new_variables:
        variables[variable] = 0

threshold = float(input('Введите порог удовлетворения правил (от 0 до 1): '))

step = 1
while True:
    print('step: {}'.format(step))

    for variable in variables.keys():
        variables[variable] = float(input('Введите значение переменной {}: '.format(variable)))
    print('Проверяю все существующие формулы')
    new_formulas = []
    for formula in formulas:
        (result, formulas_to_evaluate) = formula.evaluate(variables)
        print('{}: {}'.format(str(formula), result))
        if result < threshold:
            print('Значение формулы {} опустилось ниже порога: {} < {}'.format(formula, result, threshold))
            continue
        for formula in formulas_to_evaluate:
            new_formulas.append(formula)
    formulas = new_formulas
    print('Проверка завершена')
    step += 1
        


