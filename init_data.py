# Исходные данные для заданий

from random import randint


# Метод проверки числа на простоту
def is_prime(a):
    for i in range(2, round(a ** 0.5) + 1):
        if a % i == 0:
            return False
    return True


n = 10000  # Мощность множества А
max_value = 1e9  # Максимальное значение элемента мн-ва А
p_range = (100, 300)  # Интервал рассматриваемых чисел p
A = [randint(1, max_value) for i in range(n)]  # Инициализация множества А случайными числами
primes = [a for a in range(p_range[0], p_range[1] + 1) if is_prime(a)]  # Простые числа в вышезаданном интервале
