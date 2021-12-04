from aocd.models import Puzzle


def to_deci(bits):
    num = 0
    for i in range(len(bits), 0, -1):
        power = 2 ** (len(bits) - i)
        num += bits[i - 1] * power
    return num


def process(data: str, digits):
    data = data.replace("\n", "")
    arrs = [[] for i in range(0, digits)]
    for i in range(0, len(data)):
        arrs[i % digits].append(int(data[i]))
    gamma = [int(sum(x) > len(x) / 2) for x in arrs]
    epsilon = [0 if x == 1 else 1 for x in gamma]
    g = to_deci(gamma)
    e = to_deci(epsilon)
    print(f'gamma {"".join([str(x) for x in gamma])} ({g}) * epsilon {"".join([str(x) for x in epsilon])} ({e}) = {g * e}')
    return e * g


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=3)
    puzzle.answer_a = process(puzzle.input_data, digits=12)
