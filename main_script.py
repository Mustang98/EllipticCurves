from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from init_data import primes, n
import methods


def task1():
    print("===========TASK 1===========")
    min_irregularity = None  # Значение минимальной неравномерности Zp
    best_p = None  # Значение p, для которого достигается минимальная неравномерность Zp

    for p in primes:  # Проверяем каждое простое p
        residue_class_size = methods.get_residue_class_sizes(p)  # Получаем размерности классов вычетов Zp
        irregularity = sum((size / n - 1 / p) ** 2 for size in residue_class_size)  # Величина неравномерности для текущего p
        if min_irregularity is None or min_irregularity > irregularity:
            min_irregularity = irregularity
            best_p = p

    print("Best p value: {}".format(best_p))
    print("Minimum irregularity: %.6f" % min_irregularity)


def task2():
    print("===========TASK 2===========")
    max_points_cnt = None
    max_points_p = None
    max_points_a = None
    max_points_b = None
    for p in primes:
        residue_class_size = methods.get_residue_class_sizes(p)  # Размерности классов вычетов Zp на множестве A
        is_quadratic_residue = [False] * p
        for y in range(p):
            is_quadratic_residue[(y * y) % p] = True  # Находим квадратичные вычеты по модулю p

        for a in range(p):
            for b in range(p):
                points_cnt = 0
                for x in range(p):
                    if is_quadratic_residue[(x * x * x + a * x + b) % p]:
                        points_cnt += residue_class_size[x]  # Подсчитываем кол-во точек

                if max_points_cnt is None or points_cnt > max_points_cnt:
                    max_points_cnt = points_cnt  # Обновляем результат
                    max_points_p = p
                    max_points_a = a
                    max_points_b = b

    print("Maximum N(p, a, b) = N({}, {}, {}) = {}".format(max_points_p, max_points_a, max_points_b, max_points_cnt))
    return max_points_p, max_points_a, max_points_b


def task3(p, a, b):
    print("===========TASK 3===========")
    curve_points = methods.get_curve_points(p, a, b)  # Получаем все точки кривой
    print("Order of group: {}".format(len(curve_points) + 1))  # Группу образуют точки кривой и нейтральный элемент

    for point in curve_points:
        point_subgroup = methods.generate_cyclic_subgroup(point)  # Получаем циклическую подгруппу, порожденную точкой
        print("Order of element {}: {}".format(point, len(point_subgroup)))
    print("Order of zero-element: 1")


def task4(p, a, b):
    print("===========TASK 4===========")
    # В качестве алфавита берем пересечение множества абсцисс точек кривой и множества А
    # В качестве текста берем элементы множества А, присутсвующие в алфавите
    alphabet, frequencies = methods.get_alphabet(p, a, b)  # Получаем алфавит с частотами
    text_size = sum(freq for freq in frequencies)  # Размер текста в символах
    haffman_codes = methods.build_haffman_code(frequencies)  # Получаем коды Хаффмана для символов алфавита
    entropy = methods.calculate_entropy([freq / text_size for freq in frequencies])  # Считаем энтропию текста
    # Считаем длину кода для текста
    code_length = sum(freq * len(haffman_codes[sym_ind]) for sym_ind, freq in enumerate(frequencies))
    avg_code_length = code_length / text_size  # Считаем среднюю длину кода
    print("Alphabet (symbol, frequency, code): ")
    print("\n".join("(%d  \t%.4f  \t%s)" % (symbol, freq / text_size, code)
                    for symbol, freq, code in zip(alphabet, frequencies, haffman_codes)))
    print("Shannon entropy: %.6f" % entropy)
    print("Encoded text length: {}".format(code_length))
    print("Average code length: %.6f" % avg_code_length)


def task5(p):
    print("===========TASK 5===========")
    residue_class_size = methods.get_residue_class_sizes(p)  # Размерности классов вычетов Zp на множестве A
    entropies = []
    avg_code_lengths = []
    for a in range(0, p, 5):
        for b in range(0, p, 5):
            alphabet, frequencies = methods.get_alphabet(p, a, b, residue_class_size)
            text_size = sum(freq for freq in frequencies)
            avg_code_length = methods.calculate_average_code_length(frequencies)
            entropy = methods.calculate_entropy([freq / text_size for freq in frequencies])
            entropies.append(entropy)
            avg_code_lengths.append(avg_code_length)

    figure = plt.figure()
    figure.suptitle("Энтропия Шеннона и средняя длина кода для p = {}".format(p))
    entropy_axis = figure.add_subplot(121, projection='3d')
    entropy_axis.set_zlim((0, 20))
    b_range = a_range = range(0, p, 5)
    X, Y = np.meshgrid(b_range, a_range)
    Z = np.array(entropies).reshape(X.shape)
    entropy_axis.plot_surface(X, Y, Z)
    entropy_axis.set_xlabel('b')
    entropy_axis.set_ylabel('a')
    entropy_axis.set_zlabel('entropy')

    code_len_axis = figure.add_subplot(122, projection='3d')
    code_len_axis.set_zlim((0, 20))
    Z = np.array(avg_code_lengths).reshape(X.shape)
    code_len_axis.plot_surface(X, Y, Z)
    code_len_axis.set_xlabel('b')
    code_len_axis.set_ylabel('a')
    code_len_axis.set_zlabel('average code length')
    plt.show()


task1()
curve_p, curve_a, curve_b = task2()
task3(curve_p, curve_a, curve_b)
task4(curve_p, curve_a, curve_b)
task5(curve_p)