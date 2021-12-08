from datetime import datetime

from aocd.models import Puzzle
from math import trunc


def a(start: int, days: int, log=False):
    # puzzle = Puzzle(year=2021, day=6)
    # fish = [int(x) for x in puzzle.input_data.split(",")]
    # fish = [LanternFish(int(x)) for x in "3,4,3,1,2".split(",")]
    # fish = [int(x) for x in "1".split(",")]
    fish = [start]
    for day in range(0, days):
        spawn = 0
        for i, f in enumerate(fish):
            if f == 0:
                fish[i] = 6
                spawn += 1
            else:
                fish[i] -= 1
        for i in range(0, spawn):
            fish.append(8)
        if log:
            print(f'Days left {str(days - day).rjust(2, " ")}:  {", ".join(list(map(str, fish)))}')
    # print(f'{len(fish)} fish created from banging')
    return len(fish)
    # puzzle.answer_a = len(fish)


def all(y: int, t: int):
    """

    :param y: start position
    :param t: number of iterations
    :return:
    """
    offset = t - y
    count = trunc(offset / 7)
    doubles = d7(offset)
    print(f'd7({str(offset)}) => {str(doubles).rjust(2, " ")}')
    total = 1
    for i in range(0, doubles):
        _offset = offset - 7 * (i + 1)
        if _offset < 0:
            continue
        _all = all(2, _offset)
        print(f'child {str(i + 1).rjust(2, " ")}; all(2, {str(_offset).rjust(2, " ")}) => {_all}')
    return total


def d7(t: int):
    """
    the value
    :param t:
    :return:
    """
    dLife = 7
    if t < dLife:
        return 0
    offset = 0
    if t % dLife == 0:
        offset = -1
    return trunc(t / dLife) + offset  # x.xxx => x
    # res = 2 ** power - 1
    # return res


def func(t: int):
    if t <= 7:
        return 0
    count = d7(t)
    _count = count
    for i in range(0, count):
        _t = t - 2 - 7 * (i + 1)
        c = func(_t)
        count += c
        # print(f'path: {path}/{_t} count: {_count} d7({_t}) => {c}; running count {count}')
    return count


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=6)
    input_data = list(map(int, puzzle.input_data.split(",")))
    # distinct = set(input_data)
    # days = 256
    m = {
        "1": 6206821033,
        "2": 5617089148,
        "3": 5217223242,
        "4": 4726100874,
        "5": 4368232009
    }
    # for start in distinct:
    #     started = datetime.now()
    #     print(f'num {start} - {started.isoformat()}')
    #     m[start] = func(days + 7 - start) + 1
    #     ended = datetime.now()
    #     print(f'num {start} - {ended.isoformat()} - total {m[start]}')
    total = 0
    for x in input_data:
        total += m[str(x)]
    print(total)
    # start = 3
    # days = 35
    # d7(15)
    # res = d7(days + 7 - start)  # 3
    # print(f'parent: d7({str(days + 7 - start)}) => {str(res).rjust(2, " ")}')
    # child1 = d7(days - start - 2 - 1)  # 1
    # print(f'child1: d7({str(days - start - 2 - 1)}) => {str(child1).rjust(2, " ")}')
    # child2 = d7(days - start - 2 - 7 - 1)  # 0
    # print(f'child2: d7({str(days - start - 2 - 7 - 1)}) => {str(child2).rjust(2, " ")}')
    # actual = a(start, days, log=False)
    # print(f'actual: {str(actual).rjust(2, " ")}')
    # print(f'd7({days + 7 - start}) => {d7(days + 7 - start)}')
    # result = func(days + 7 - start)
    # print(f'result: {str(result).rjust(2, " ")}')
