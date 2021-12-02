from aocd.models import Puzzle
import re

regex = re.compile(r'(\w+)\s(\-?\d+)')


def extract(cmd):
    match = regex.match(cmd)
    direction = match.group(1)
    magnitude = int(match.group(2))
    return direction, magnitude


def process_a(data):
    cmd_vector = {
        'forward': {'x': 0, 'y': 1},
        'up': {'x': 1, 'y': -1},
        'down': {'x': 1, 'y': 1}
    }
    position = [0, 0]
    for cmd in data:
        direction, magnitude = extract(cmd)
        vector = cmd_vector[direction]
        position[vector.get("x")] += vector.get("y") * magnitude
    print(f'({position[0]}, {position[1]}) = {position[0] * position[1]}')
    return position[0] * position[1]


def process_b(data):
    cmd_vector = {
        'forward': {'x': 0, 'y': 1},
        'up': {'x': 2, 'y': -1},
        'down': {'x': 2, 'y': 1}
    }
    position = [0, 0, 0]  # horizontal, depth, aim
    for cmd in data:
        direction, magnitude = extract(cmd)
        vector = cmd_vector[direction]
        position[vector.get("x")] += vector.get("y") * magnitude
        if direction == "forward":
            # adjust the depth based off the aim
            position[1] += magnitude * position[2]
    print(f'({position[0]}, {position[1]}) = {position[0] * position[1]}')
    return position[0] * position[1]


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=2)
    data = puzzle.input_data.split("\n")
    puzzle.answer_a = process_a(data)
    puzzle.answer_b = process_b(data)
