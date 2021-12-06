import math

import pandas as pd
from aocd.models import Puzzle
import re
from functools import reduce
import collections

regex = re.compile(r'(\d+),(\d+)\s\-\>\s(\d+),(\d+)')


def decode(data: str):
    results = []
    for item in data.split("\n"):
        match = regex.match(item)
        coordinates = ((int(match.group(1)), int(match.group(2))), (int(match.group(3)), int(match.group(4))))
        results.append(coordinates)
    return results


def to_func(a: (int, int), b: (int, int)):
    return lambda x: x * (b[1] - a[1] / b[0] - a[0]) - a[1]


def expand(a: (int, int), b: (int, int)):
    coordinates = []
    for x in expand_range(a[0], b[0]):
        for y in expand_range(a[1], b[1]):
            coordinates.append((x, y))
    return coordinates


def expand_range(a: int, b: int):
    if a < b:
        return range(a, b + 1)
    else:
        return range(a, b - 1, -1)


def process_a(data: list):
    c_all = reduce(list.__add__, [expand(*b) for b in data if b[0][0] == b[1][0] or b[0][1] == b[1][1]])
    counter = collections.Counter(c_all)
    count = len([x for x in counter if counter[x] > 1])
    print(f'found {count} overlaps')
    return count


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


def parametric(t: int, AB: ((int, int), (int, int))):
    return add(scale(subtract(AB[1], AB[0]), t), AB[0])


def intersecting_point(AB: ((int, int), (int, int)), CD: ((int, int), (int, int))):
    numerator = multiply(subtract(CD[0], AB[0]), subtract(CD[1], CD[0]))
    denominator = multiply(subtract(CD[1], CD[0]), subtract(AB[1], AB[0]))
    if denominator != 0:
        t = numerator / denominator
        return [parametric(t, AB)]
    # parallel lines, get the overlap
    inter = set(expand_linear(*AB)).intersection(set(expand_linear(*CD)))
    return list(inter)


def expand_linear(A: (int, int), B: (int, int)):
    inverted = False
    if B[0] - A[0] == 0:
        inverted = True
        A = invert(A)
        B = invert(B)
    m = (B[1] - A[1]) / (B[0] - A[0])
    b = A[1] - m * A[0]
    func = lambda x: int(m * x + b)
    start = min(A[0], B[0])
    end = max(A[0], B[0])
    points = []
    for i in range(start, end + 1):
        p = (i, func(i))
        if inverted:
            p = invert(p)
        points.append(p)
    return points


def invert(a: (int, int)):
    return (a[1], a[0])


def subtract(a: (int, int), b: (int, int)):
    return (b[0] - a[0], b[1] - a[1])


def add(a: (int, int), b: (int, int)):
    return (a[0] + b[0], a[1] + b[1])


def scale(a: (int, int), s: int):
    return (s * a[0], s * a[1])


def multiply(a: (int, int), b: (int, int)):
    # U×V=Ux⋅Vy−Uy⋅Vx.
    return a[0] * b[1] - a[1] * b[0]


def half_space(p: (int, int), a: (int, int), b: (int, int)):
    return multiply(subtract(b, a), subtract(p, a))


def print_grind(points: list):
    counter = collections.Counter(points)
    rows = max([x[0] for x in counter]) + 1
    cols = max([x[1] for x in counter]) + 1
    grid = []
    for c in range(0, cols):
        grid.append([])
        for r in range(0, rows):
            grid[c].append('.')

    for point in counter:
        val = counter[point]
        grid[point[1]][point[0]] = val

    with open(".\\grid.txt", "w") as f:
        header = "".ljust(3, " ") + " " + " ".join([f'{str(c)}'.ljust(3, " ") for c in range(0, cols)])
        f.write(header)
        for i, row in enumerate(grid):
            f.write("\n" + f'{i}'.ljust(3, ' ') + " " + " ".join([f'{str(v)}'.ljust(3, " ") for v in row]))
        f.close()
    return


def process_b(data: list):
    points = []
    total = round((len(data) - 1) * len(data) / 2)
    position = 0
    for item in data:
        print(f'round {position} of {len(data)}')
        points.extend(expand_linear(*item))
        position += 1
    # print_grind(points)

    counter = collections.Counter(points)
    points = [x for x in counter if counter[x] > 1]
    count = len(points)
    print(f'found {count} overlaps')

    # this twas a dream....
    # _points = []
    # position = 0
    # for i in range(0, len(data)):
    #     AB = data[i]
    #     for j in range(i + 1, len(data)):
    #         if position % 1000 == 0:
    #             print(f'round {position} of {total} {100 * round(position / total, 2)}%')
    #         position += 1
    #         CD = data[j]
    #         if intersects(AB, CD):
    #             _points.extend(intersecting_point(AB, CD))

    return count


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=5)
    test = """0,9 -> 5,9\n8,0 -> 0,8\n9,4 -> 3,4\n2,2 -> 2,1\n7,0 -> 7,4\n6,4 -> 2,0\n0,9 -> 2,9\n3,4 -> 1,4\n0,""" \
           + """0 -> 8,8\n5,5 -> 8,2"""
    input_data = decode(puzzle.input_data)
    puzzle.answer_a = process_a(input_data)
    puzzle.answer_b = process_b(input_data)
