class P(object):
    def __init__(self, x, y, dy):
        self.x = x
        self.y = y
        self.dy = dy


# функция, возвращающая n ближайших по x точек
def getNearPoints(x, n, ps):
    near_ps = []
    size = len(ps)

    if ps[size - 1].x < x:
        for i in range(n):
            near_ps.append(ps[size - 1 - i])
    elif x < ps[0].x:
        for i in range(n):
            near_ps.append(ps[i])
    else:
        low_ind = 0
        up_ind = 0
        for i in range(size - 1):
            if ps[i].x < x < ps[i + 1].x:
                low_ind = i
                up_ind = i + 1
                break

        i = 0
        while i < n:
            if 0 <= low_ind:
                near_ps.append(ps[low_ind])
                low_ind -= 1
                i += 1

            if up_ind < size:
                near_ps.append(ps[up_ind])
                up_ind += 1
                i += 1

        if i > n:
            near_ps.pop()

    return near_ps


# функция, вычисляющая разделенные разности для Ньютона
def getDifs(ps):
    n = len(ps)
    difs = [[0 for j in range(n)] for i in range(n)]

    for i in range(n):
        difs[i][i] = ps[i].y

    for i in range(n - 1):  # счетчик по диагоналям
        for j in range(n - 1 - i):  # счетчик по числу элементов в диагонали
            difs[j][j + i + 1] = (difs[j][j + i] - difs[j + 1][j + i + 1]) / (ps[j].x - ps[j + i + 1].x)

    return difs


# функция, вычисляющая значение полинома Ньютона
def yNewton(x, n, ps):
    near_ps = sorted(getNearPoints(x, n + 1, ps), key=lambda p: p.x)
    y = near_ps[0].y
    f1 = 1
    difs = getDifs(near_ps)

    for i in range(n):
        f1 *= (x - near_ps[i].x)
        y += f1 * difs[0][i + 1]

    return y


# функция, вычисляющая разделенные разности для Эрмита
def getDifs2(ps):
    n = len(ps) * 2
    difs = [[0 for j in range(n)] for i in range(n)]

    for i in range(n - 1):
        if 0 == i % 2:
            difs[i][i + 1] = ps[i // 2].dy
        else:
            difs[i][i + 1] = (ps[i // 2].y - ps[i // 2 + 1].y) / (ps[i // 2].x - ps[i // 2 + 1].x)

    for i in range(1, n - 1):  # счетчик по диагоналям
        for j in range(n - 1 - i):  # счетчик по числу элементов в диагонали
            difs[j][j + i + 1] = (difs[j][j + i] - difs[j + 1][j + i + 1]) / (ps[j // 2].x - ps[(j + i + 1) // 2].x)

    return difs


# функция, вычисляющая значение полинома Эрмита
def yHermit(x, n, ps):
    ps_n = n // 2 + 1
    near_ps = sorted(getNearPoints(x, ps_n, ps), key=lambda p: p.x)
    y = near_ps[0].y
    f1 = 1
    difs = getDifs2(near_ps)

    i = 0
    j = 0
    while j < n:
        f1 *= (x - near_ps[i].x)
        y += f1 * difs[0][j + 1]
        j += 1

        if j < n:
            f1 *= (x - near_ps[i].x)
            y += f1 * difs[0][j + 1]
            j += 1

        i += 1

    return y


if __name__ == "__main__":
    x = float(input("Введите x: "))
    n = int(input("Введите степень n: "))  # степень полинома
    ps = [P(0.00, 1.000000, -1.000000), P(0.15, 0.838771, -1.14944),
          P(0.30, 0.655336, -1.29552), P(0.45, 0.450447, -1.43497),
          P(0.60, 0.225336, -1.56464), P(0.75, -0.018310, -1.68164),
          P(0.90, -0.278390, -1.78333), P(1.05, -0.552430, -1.86742)]

    if n < 0 or n + 1 > len(ps):
        print("Error n")
    else:
        ps = sorted(ps, key=lambda p: p.x)
        print("y(x) Newton = {:.6f}".format(yNewton(x, n, ps)))
        print("y(x) Hermit = {:.6f}".format(yHermit(x, n, ps)))

        for p in ps:
            p.x, p.y = p.y, p.x
        ps = sorted(ps, key=lambda p: p.x)

        print("Корень = {:.6f}".format(yNewton(0, n, ps)))

