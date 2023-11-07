import matplotlib.pyplot as plt

class Circle:
    def draw_circle(xc, yc, r):
        x = 0
        y = r
        d = 3 - 2 * r

        points = []

        while x <= y:
            points.append((xc + x, yc + y))
            points.append((xc - x, yc + y))
            points.append((xc + x, yc - y))
            points.append((xc - x, yc - y))
            points.append((xc + y, yc + x))
            points.append((xc - y, yc + x))
            points.append((xc + y, yc - x))
            points.append((xc - y, yc - x))

            if d < 0:
                d += 4 * x + 6
            else:
                d += 4 * (x - y) + 10
                y -= 1
            x += 1

        return points

    # Пример использования:
    # xc, yc, r = 0, 0, 50
    # circle_points = draw_circle(xc, yc, r)

    # # Визуализация окружности
    # x, y = zip(*circle_points)
    # plt.scatter(x, y)
    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.show()

class Ellipse:

    def draw_ellipse(xc, yc, a, b):
        x = 0
        y = b
        a_sqr = a * a
        b_sqr = b * b
        d = 4 * b_sqr - 4 * a_sqr * b + a_sqr

        points = []

        while a_sqr * (2 * y - 1) > 2 * b_sqr * (x + 1):
            points.append((xc + x, yc + y))
            points.append((xc - x, yc + y))
            points.append((xc + x, yc - y))
            points.append((xc - x, yc - y))

            if d < 0:
                d += 4 * b_sqr * (2 * x + 3)
            else:
                d += 4 * b_sqr * (2 * x + 3) - 4 * a_sqr * (2 * y - 2)
                y -= 1
            x += 1

        d = b_sqr * (2 * x + 1) * (2 * x + 1) + 4 * a_sqr * (y - 1) * (y - 1) - 4 * a_sqr * b_sqr

        while y >= 0:
            points.append((xc + x, yc + y))
            points.append((xc - x, yc + y))
            points.append((xc + x, yc - y))
            points.append((xc - x, yc - y))

            if d < 0:
                d += 4 * b_sqr * (2 * x + 2) + a_sqr * (3 - 4 * y)
                x += 1
            else:
                d += 4 * a_sqr * (3 - 2 * y)
            y -= 1

        return points

    # Пример использования:
    # xc, yc, a, b = 100, 100, 40, 80
    # ellipse_points = draw_ellipse(xc, yc, a, b)

    # # Визуализация эллипса
    # x, y = zip(*ellipse_points)
    # plt.scatter(x, y)
    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.show()

class Hyperball:

    def draw_hyperbola(xc, yc, a, b):
        x = 0
        y = b
        a_sqr = a * a
        b_sqr = b * b

        points = []

        # Рисуем верхнюю ветвь гиперболы
        while x * b_sqr <= y * a_sqr:
            points.append((xc + x, yc + y))
            points.append((xc - x, yc + y))

            x += 1
            y = int((b_sqr - b_sqr * x * x / a_sqr) ** 0.5)

        # Рисуем нижнюю ветвь гиперболы
        x = 0
        y = b
        while y > 0:
            points.append((xc + x, yc - y))
            points.append((xc - x, yc - y))

            x += 1
            y = int((b_sqr - b_sqr * x * x / a_sqr) ** 0.5)

        return points

    # Пример использования:
    # xc, yc, a, b = 100, 100, 40, 20
    # hyperbola_points = draw_hyperbola(xc, yc, a, b)

    # # Визуализация гиперболы
    # x, y = zip(*hyperbola_points)
    # plt.scatter(x, y)
    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.show()

class Paraball:
    
    def draw_parabola(a, h, k):
        points = []
        for x in range(-100, 101):
            y = a * (x - h) ** 2 + k
            points.append((x, y))

        return points

    # Пример использования:
    # a, h, k = 0.1, 0, 0  # Параметры a, h, k параболы
    # parabola_points = draw_parabola(a, h, k)

    # # Визуализация параболы
    # x, y = zip(*parabola_points)
    # plt.scatter(x, y)
    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.show()
