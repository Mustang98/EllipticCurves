# Класс точки эллиптической кривой
class ElCurvePoint:
    x = None
    y = None
    curve_a = None
    curve_b = None
    curve_p = None

    def __init__(self, x, y, p, a, b):
        self.x = x
        self.y = y
        self.curve_a = a
        self.curve_b = b
        self.curve_p = p

    # Оператор сложения двух точек кривой
    def __add__(self, other):
        assert (self.curve_a == other.curve_a and self.curve_b == other.curve_b and self.curve_p == other.curve_p)
        mod = self.curve_p
        sum_point = self.zero_point()

        if self.x is None:
            sum_point.x = other.x
            sum_point.y = other.y
        elif other.x is None:
            sum_point.x = self.x
            sum_point.y = self.y
        elif self.x != other.x:
            denominator = (other.x - self.x + mod) % mod
            denominator = pow(denominator, mod - 2, mod)
            alpha = ((other.y - self.y + mod) * denominator) % mod
            sum_point.x = (alpha ** 2 - self.x - other.x + 3 * mod) % mod
            sum_point.y = (-self.y + alpha * (self.x - sum_point.x + mod) + mod) % mod
        elif self.x == other.x and self.y == other.y and self.y != 0:
            alpha = (pow(2 * self.y, mod - 2, mod) * (3 * self.x ** 2 + self.curve_a)) % mod
            sum_point.x = (alpha ** 2 - 2 * self.x + 3 * mod) % mod
            sum_point.y = (-self.y + alpha * (self.x - sum_point.x + mod) + 2 * mod) % mod

        return sum_point

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return str((self.x, self.y))

    def xy_point(self):
        return (self.x, self.y)

    # "Нулевая" точка кривой (нейтральный элемент группы) - точка с координатами (None, None)
    def zero_point(self):
        return ElCurvePoint(None, None, self.curve_p, self.curve_a, self.curve_b)