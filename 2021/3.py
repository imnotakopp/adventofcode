from aocd.models import Puzzle
import pandas as pd

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

def process_b(data: str):
    data = [list(map(int, list(x))) for x in data.split("\n")]
    size = len(data)
    o2 = pd.DataFrame(data)
    cO2 = pd.DataFrame(data)
    for i in range(0, size):
        if len(o2.index) != 1:
            o2 = o2[o2[i] == max(o2[i])]
        if len(cO2.index) != 1:
            value = min(cO2[i])
            cO2 = cO2[cO2[i] == value]

        if len(cO2.index) == 1 and len(o2.index) == 1:
            break
    o2Bits = o2.values.tolist()[0]
    cO2Bits = cO2.values.tolist()[0]
    o2_10 = to_deci(o2Bits)
    cO2_10 = to_deci(cO2Bits)
    print(f'Oxygen {"".join([str(x) for x in o2Bits])} ({o2_10}) * CO2 {"".join([str(x) for x in cO2Bits])} ({cO2_10}) = {o2_10 * cO2_10}')
    return o2_10 * cO2_10

def max(s: pd.Series):
    return s.sum() >= len(s.index) / 2

def min(s: pd.Series):
    return s.sum() < len(s.index) / 2



if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=3)
    puzzle.answer_a = process(puzzle.input_data, digits=12)
    puzzle.answer_b = process_b(puzzle.input_data)
