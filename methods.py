#  Вспомогательные методы для заданий

import math
import queue
from ElCurvePoint import ElCurvePoint
from Node import Node
from init_data import A


# Tasks: 1, 2, 4, 5
# Метод получения размерностей классов вычетов Zp для множества А
def get_residue_class_sizes(p):
    residue_class_size = [0] * p  # Размерности классов вычетов Zp для множества A
    for number in A:
        residue_class_size[number % p] += 1
    return residue_class_size


# Tasks: 3, 4, 5
# Метод получения всех точек, принадлежащих эллиптической кривой с параметрами a, b в поле Zp
def get_curve_points(p, a, b):
    points = []

    # Для каждого квадратичного вычета находим все 'y', квадратом которых он является
    y_squares = [[] for i in range(p)]
    for y in range(p):
        y_squares[(y * y) % p].append(y)

    for x in range(p):
        square_y = (x ** 3 + a * x + b) % p
        for y in y_squares[square_y]:
            points.append(ElCurvePoint(x, y, p, a, b))
    return points


# Tasks: 3
# Метод получений циклической подгруппы, порожденной элементом generator_point
def generate_cyclic_subgroup(generator_point):
    curr_point = generator_point
    point_subgroup = [curr_point.xy_point()]

    while curr_point != generator_point.zero_point():
        point_subgroup.append(curr_point.xy_point())
        curr_point += generator_point

    return point_subgroup


# Tasks: 4, 5
# Метод получения алфавита на основе параметров кривой, а так же частот его символов в множестве А
def get_alphabet(curve_p, curve_a, curve_b, residue_class_size=None):
    # В качестве алфавита берем пересечение множества абсцисс точек кривой и множества А
    if residue_class_size is None:  # Если размерности классов вычетов не получены, то считаем их
        residue_class_size = get_residue_class_sizes(curve_p)
    assert(len(residue_class_size) == curve_p)

    # Получаем абсциссы точек кривой
    curve_x_values = list(set([point.x for point in get_curve_points(curve_p, curve_a, curve_b)]))
    alphabet = []  # Символы алфавита
    frequencies = []  # Соответствующие частоты (количество вхождений в текст А)
    for x in curve_x_values:
        if residue_class_size[x] > 0:  # Если абсцисса присутствует в множестве А, то добавляем ее в алфавит
            alphabet.append(x)
            frequencies.append(residue_class_size[x])
    return alphabet, frequencies


# Tasks: 4, 5
# Метод обхода дерева Хаффмана и сохранения кодов символов
def dfs(curr_node, curr_code, all_codes):
    if curr_node.symbol is not None:
        all_codes[curr_node.symbol] = curr_code
    else:
        dfs(curr_node.left, curr_code + '0', all_codes)
        dfs(curr_node.right, curr_code + '1', all_codes)


# Tasks: 4, 5
# Метод построения дерева Хаффмана на основе массива частот символов
def build_haffman_code(frequencies):
    freq_queue = queue.PriorityQueue()  # Приоритетная очередь с частотами и соответствующими вершинами поддеревьев
    for ind, freq in enumerate(frequencies):  # В качестве символов в вершины дерева записываем исходные индексы частот
        freq_queue.put_nowait((freq, Node(symbol=ind)))

    while freq_queue.qsize() > 1:  # Строим дерево
        freq1, node1 = freq_queue.get_nowait()
        freq2, node2 = freq_queue.get_nowait()
        node3 = Node(left=node1, right=node2)
        freq_queue.put_nowait((freq1 + freq2, node3))

    haffman_codes = [""] * len(frequencies)  # Полученные коды для символов в порядке, соответствующем входным частотам
    dfs(freq_queue.get_nowait()[1], "", haffman_codes)
    return haffman_codes


# Tasks: 4, 5
# Метод подсчета энтропии на основе полной группы частот
def calculate_entropy(frequencies):
    return -sum(p * math.log(p, 2) for p in frequencies)


# Tasks: 5
# Метод подсчета средней длины кода символа на основе частот алфавита
def calculate_average_code_length(frequencies):
    haffman_codes = build_haffman_code(frequencies)  # Строим коды Хаффмана для каждого символа
    text_size = sum(freq for freq in frequencies)  # Считаем размер текста в символах
    # Считаем длину кода всего текста
    code_length = sum(freq * len(haffman_codes[sym_ind]) for sym_ind, freq in enumerate(frequencies))
    return code_length / text_size  # Считаем среднюю длину кода
