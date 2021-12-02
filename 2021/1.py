from aocd.models import Puzzle


def process(data, window_size=1):
    count = 0
    for i in range(0, len(data)):
        if i + window_size == len(data):
            break
        n0 = sum(data[i: i + window_size])
        n1 = sum(data[i + 1: i + 1 + window_size])
        if n0 < n1:
            count += 1
    return count


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=1)
    data = [int(x) for x in puzzle.input_data.split("\n")]
    puzzle.answer_a = process(data)
    puzzle.answer_b = process(data, window_size=3)
