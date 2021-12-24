from typing import List


from aocd.models import Puzzle

puzzle = Puzzle(year=2021, day=9)


def points(data: List[List[int]]):
    for i, row in enumerate(data):
        iPrev = i - 1
        iNext = i + 1
        for j, v in enumerate(row):
            jPrev = j - 1
            jNext = j + 1
            a = v + 1 if iPrev < 0 else data[iPrev][j]
            b = v + 1 if iNext >= len(data) else data[iNext][j]
            c = v + 1 if jPrev < 0 else row[jPrev]
            d = v + 1 if jNext >= len(row) else row[jNext]
            if v < a and v < b and v < c and v < d:
                yield i, j


def processA(data):
    data = [list(map(int, list(l))) for l in data.split("\n")]
    riskLevel = 0
    for i, j in points(data):
        riskLevel += data[i][j] + 1
    return riskLevel


def processB(data):
    data = [list(map(int, list(l))) for l in data.split("\n")]
    basins = []
    for r, c in points(data):
        _basin = [].copy()
        _basin = expand(data, Point(r, c), _basin)
        basins.append(_basin)

    basins.sort(key=lambda a: len(a), reverse=True)
    total = 1
    for x in list(map(len, basins[0:3])):
        total *= x
    return total

class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __gt__(self, other):
        return self.x >= other.x and self.y >= other.y

    def adjacent(self):
        return [
            Point(self.x - 1, self.y),
            Point(self.x, self.y - 1),
            Point(self.x, self.y),
            Point(self.x, self.y + 1),
            Point(self.x + 1, self.y),
        ]

    def boundaries(self):
        return [
            Point(self.x - 1, self.y - 1),
            Point(self.x - 1, self.y),
            Point(self.x - 1, self.y + 1),
            Point(self.x, self.y - 1),
            Point(self.x, self.y),
            Point(self.x, self.y + 1),
            Point(self.x + 1, self.y - 1),
            Point(self.x + 1, self.y),
            Point(self.x + 1, self.y + 1)
        ]


def expand(data, center: Point, basin: List[Point] = []):
    # get the boundary positions if they exist
    for p in center.adjacent():
        v = None
        if p.x < 0 or p.x >= len(data):
            # outside the map
            v = 9
        elif p.y < 0 or p.y >= len(data[0]):
            # y is outside the map
            v = 9
        else:
            # point is within the data set
            v = data[p.x][p.y]

        # if v is < 9 the point is within the basin
        if v < 9 and p not in basin:
            basin.append(p)
            basin = expand(data, p, basin)
    return basin


test = """2199943210\n3987894921\n9856789892\n8767896789\n9899965678"""
# puzzle.answer_a = processA(puzzle.input_data)
puzzle.answer_b = processB(puzzle.input_data)
