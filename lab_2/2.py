class P(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


def getIndex(ps, x):
    dif = abs(ps[0].x - x)
    ind = 0

    for i in range(len(ps)):
        if abs(ps[i].x - x) <= dif:
            dif = abs(ps[i].x - x)
            ind = i

    return ind


def getWorkingPoints(ps, ind, n):
    left = ind
    right = ind

    for i in range(n - 1):
        if i % 2 == 0:
            if left == 0:
                right += 1
            else:
                left -= 1
        else:
            if right == len(ps) - 1:
                left -= 1
            else:
                right += 1

    return ps[left:right + 1]


def getDifs(ps):
    n = len(ps)
    difs = [[0 for j in range(n)] for i in range(n)]

    for i in range(n):
        difs[i][i] = ps[i].y

    for i in range(n - 1):
        for j in range(n - 1 - i):
            difs[j][j + i + 1] = (difs[j][j + i] - difs[j + 1][j + i + 1]) / (ps[j].x - ps[j + i + 1].x)

    return difs


def yNewton(x, n, ps):
    index = getIndex(ps, x)
    near_ps = getWorkingPoints(ps, index, n + 1)

    y = near_ps[0].y
    f1 = 1
    difs = getDifs(near_ps)

    for i in range(n):
        f1 *= (x - near_ps[i].x)
        y += f1 * difs[0][i + 1]

    return y, near_ps


def interpolation2(table, nx, ny, x, y):
    res = []

    for i in range(len(table)):
        ps = []

        for j in range(len(table)):
            ps.append(P(j, table[i][j]))

        y2, arr = yNewton(x, nx, ps)
        res.append(P(i, y2))

    y2, arr = yNewton(y, ny, res)

    for p in arr:
        print(p.y, end=' ')
    print('\ny = {:.3f}'.format(y2))

    return y2


def interpolation3(table, nx, ny, nz, x, y, z):
    ps = []
    for i in range(len(table)):
        ps.append(P(i, interpolation2(table[i], nx, ny, x, y)))

    z2, arr = yNewton(z, nz, ps)
    return z2


if __name__ == "__main__":
    z0 = [[0, 1, 4, 9, 16],
          [1, 2, 5, 10, 17],
          [4, 5, 8, 13, 20],
          [9, 10, 13, 18, 25],
          [16, 17, 20, 25, 32]]

    z1 = [[1, 2, 5, 10, 17],
          [2, 3, 6, 11, 18],
          [5, 6, 9, 14, 21],
          [10, 11, 14, 19, 26],
          [17, 18, 21, 26, 33]]

    z2 = [[4, 5, 8, 13, 20],
          [5, 6, 9, 14, 21],
          [8, 9, 12, 17, 24],
          [13, 14, 17, 22, 29],
          [20, 21, 24, 29, 36]]

    z3 = [[9, 10, 13, 18, 25],
          [10, 11, 14, 19, 26],
          [13, 14, 17, 22, 29],
          [18, 19, 22, 27, 34],
          [25, 26, 29, 34, 41]]

    z4 = [[16, 17, 20, 25, 32],
          [17, 18, 21, 26, 33],
          [20, 21, 24, 29, 36],
          [25, 26, 29, 34, 41],
          [32, 33, 36, 41, 48]]

    table = [z0, z1, z2, z3, z4]
    nx = ny = nz = x = y = z = rc = 0
    max_cnt = len(table)

    try:
        nx = int(input("Введите степень nx: "))

        if nx <= 0 or nx >= max_cnt:
            print("Недопустимое значение")
            rc = -1
        else:
            ny = int(input("Введите степень ny: "))

            if ny <= 0 or ny >= max_cnt:
                print("Недопустимое значение")
                rc = -1
            else:
                nz = int(input("Введите степень nz: "))

                if nz <= 0 or nz >= max_cnt:
                    print("Недопустимое значение")
                    rc = -1
                else:
                        try:
                            x = float(input("\nВведите x: "))
                            y = float(input("Введите y: "))
                            z = float(input("Введите z: "))
                        except:
                            print("Надо вводить числа")
                            rc = -1
    except:
        print("Надо вводить целые числа")
        rc = -1

    if 0 == rc:
        res = interpolation3(table, nx, ny, nz, x, y, z)
        print("\nРезультат = %.2f\n" % res)
