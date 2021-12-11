from typing import List

from aocd.models import Puzzle


class Code:
    #  000
    # 1   2
    # 1   2
    #  333
    # 4   6
    # 4   6
    #  555

    def __init__(self, d):
        self.code = d

    @property
    def length(self):
        return len(self.code)

    @property
    def chars(self):
        return list(self.code)

    @property
    def number(self):
        if len(self.code) == 2:
            return 1
        elif len(self.code) == 7:
            return 8
        elif len(self.code) == 3:
            return 7
        elif len(self.code) == 4:
            return 4
        return None


class Line:

    def __init__(self, l: str):
        parts = l.split(" | ")
        self.input = [Code(x) for x in parts[0].split(" ")]
        self.output = [Code(x) for x in parts[1].split(" ")]
        self.decoded = []


def decode(d: str):
    return Line(d)


def a(data: List[Line]):
    count = 0
    for l in data:
        for o in l.output:
            if o.number in (1, 4, 7, 8):
                count += 1
    return count


def findOne(s: str):
    for x in s.split(" "):
        if len(x) == 2:
            return x
    return None


def findFour(s: str):
    for x in s.split(" "):
        if len(x) == 4:
            return x
    return None


def findSeven(s: str):
    for x in s.split(" "):
        if len(x) == 3:
            return x
    return None


def findEight(s: str):
    for x in s.split(" "):
        if len(x) == 7:
            return x
    return None


def charsInANotInB(a: str, b: str):
    _a = list(a)
    _b = list(b)
    return [x for x in list(a) if x not in list(b)]


def charsInAB(a: str, b: str):
    return [x for x in list(a) if x in list(b)]

def decodeB(l: str):
    #  111
    # 0   2
    # 0   2
    #  333
    # 4   6
    # 4   6
    #  555
    positions = ['' for x in range(0, 7)]
    one = findOne(l)
    four = findFour(l)
    seven = findSeven(l)
    eight = findEight(l)

    # position 1, this is the character in 7 and not in 1
    positions[1] = charsInANotInB(seven, one)[0]

    # 6 is the only number of length 6 and with not all of the characters in 1
    six = [x for x in l.split(' ') if len(x) == 6 and not all(c in list(x) for c in list(one))][0]

    # position 2 all the characters in 8 not in 6
    positions[2] = charsInANotInB(eight, six)[0]
    # position 6 all the characters in one and in 6
    positions[6] = charsInAB(one, six)[0]

    nine = [x for x in l.split(' ') if len(x) == 6 and all(c in list(x) for c in list(four))][0]
    positions[4] = charsInANotInB(eight, nine)[0]

    zero = [x for x in l.split(' ') if len(x) == 6 and x != six and x != nine][0]
    positions[3] = charsInANotInB(eight, zero)[0]
    three = [x for x in l.split(' ') if len(x) == 5 and all(c in list(x) for c in list(one))][0]
    positions[0] = charsInANotInB(eight, three + positions[4])[0]
    positions[5] = charsInANotInB(nine, four + positions[1])[0]

    return {c: i for i, c in enumerate(positions)}


def b(data: List[tuple]):
    #  111
    # 0   2
    # 0   2
    #  333
    # 4   6
    # 4   6
    #  555
    ZERO = list("012654")
    ONE = list("26")
    TWO = list("12345")
    THREE = list("12365")
    FOUR = list("0326")
    FIVE = list("10365")
    SIX = list("103465")
    SEVEN = list("126")
    EIGHT = list("0126543")
    NINE = list("012365")
    SEGMENTS = [ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE]
    total = 0
    for i, o in data:
        m = decodeB(i)
        n = ""
        for c in o.split(" "):
            s = "".join([str(m[x]) for x in list(c)])
            for index, seg in enumerate(SEGMENTS):
                if all(c in seg for c in list(s)) and len(s) == len(seg):
                    n += str(index)
                    break
        total += int(n)

    return total


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=8)
    data = list(map(decode, puzzle.input_data.split("\n")))
    # puzzle.answer_a = a(data)
    puzzle.answer_b = b([tuple(x.split(" | ")) for x in puzzle.input_data.split("\n")])
