import collections
from statistics import median, mode

from aocd.models import Puzzle


def distance(x: int, y: int):
    return abs(y - x)


def intersects(AB: ((int, int), (int, int)), CD: ((int, int), (int, int))):
    hC = half_space(CD[0], *AB)
    hD = half_space(CD[1], *AB)
    if hD == 0 and hC == 0:
        return min(CD[0][0], CD[1][0]) <= max(AB[0][0], AB[1][0]) \
               and max(CD[0][0], CD[1][0]) >= min(AB[0][0], AB[1][0]) \
               and min(CD[0][1], CD[1][1]) <= max(AB[0][1], AB[1][1]) \
               and max(CD[0][1], CD[1][1]) >= min(AB[0][1], AB[1][1])
    else:
        h = hD * hC
        g = half_space(AB[0], *CD) * half_space(AB[1], *CD)
        return h <= 0 and g <= 0


def half_space(p: (int, int), a: (int, int), b: (int, int)):
    return multiply(subtract(b, a), subtract(p, a))


def subtract(a: (int, int), b: (int, int)):
    return (b[0] - a[0], b[1] - a[1])


def add(a: (int, int), b: (int, int)):
    return (a[0] + b[0], a[1] + b[1])


def scale(a: (int, int), s: int):
    return (s * a[0], s * a[1])


def multiply(a: (int, int), b: (int, int)):
    # U×V=Ux⋅Vy−Uy⋅Vx.
    return a[0] * b[1] - a[1] * b[0]


def a(ls: list):
    tMode = mode(ls)
    tMedian = int(median(ls))
    totalMedian = sum([distance(tMedian, x) for x in ls])
    totalMode = sum([distance(tMode, x) for x in ls])
    return min(totalMedian, totalMode)


def points(ls: list):
    """
    calculate the
    :param ls:
    :return:
    """
    distinct = collections.Counter(ls)
    points = [0] * (max(ls) + 1)
    for n in range(0, len(points)):
        total = 0
        for c in distinct:
            if c <= n:
                total += int(distinct[c] * distianceB(n, c))
        points[n] = total
    return points


def points_inverse(ls: list):
    distinct = collections.Counter(ls)
    points = [0] * (max(ls) + 1)
    for n in range(len(points) - 1, -1, -1):
        total = 0
        for c in distinct:
            if c >= n:
                total += int(distinct[c] * distianceB(n, c))
        points[n] = total
    return points


def b(ls: list):
    r = ls.copy()
    r.reverse()
    forward = points(ls)
    backwards = points_inverse(r)
    total = []
    for i in range(0, len(forward)):
        total.append(forward[i] + backwards[i])
    gas = min(total)
    _t = total[480:500]
    print(f'gas: {gas}')
    return gas


def distianceB(x: int, y: int):
    diff = distance(x, y)
    return diff * (diff + 1) / 2


if __name__ == '__main__':
    test = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    b(test)
    puzzle = Puzzle(year=2021, day=7)
    data = list(map(int, puzzle.input_data.split(",")))
    # puzzle.answer_a = a(data)
    puzzle.answer_b = b(data)
