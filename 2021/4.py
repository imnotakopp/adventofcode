from aocd.models import Puzzle
import re

bingo_numbers = []
bingo_index_map = {}


def card_to_matrix(card: str, mapper: None):
    return [[mapper(n) if mapper else n for n in re.split(r'\s+', x.strip())] for x in card.split("\n")]


def transpose(card: list):
    _c = []
    for cIndex in range(0, len(card[0])):
        _c.append([])
        for r in card:
            _c[cIndex].append(r[cIndex])
    return _c


def sum_of_unmarked_in_card(card: str, up_to_index: int):
    _bingo_numbers = bingo_numbers[0:up_to_index + 1]
    _bingo_map = {n: i for i, n in enumerate(_bingo_numbers)}
    _card = card_to_matrix(card, mapper=lambda x: 0 if x in _bingo_map else int(x))
    row = [sum(r) for r in _card]
    return sum(row)


def proccess_a(cards):
    winning_indices = list(map(winning_index_for_card, cards))
    winning_number_index = min(winning_indices)
    winning_number = int(bingo_numbers[winning_number_index])
    winning_card_index = winning_indices.index(winning_number_index)
    winning_card = cards[winning_card_index]
    sum_of_unmarked = sum_of_unmarked_in_card(winning_card, winning_number_index)
    print(
        f'#{winning_card_index} card wins with number {winning_number}. Answer = {winning_number} * {sum_of_unmarked} '
        f'( sum of unmarked ) = {winning_number * sum_of_unmarked}')
    return winning_number * sum_of_unmarked


def proccess_b(cards):
    winning_indices = list(map(winning_index_for_card, cards))
    winning_number_index = max(winning_indices)
    winning_number = int(bingo_numbers[winning_number_index])
    winning_card_index = winning_indices.index(winning_number_index)
    winning_card = cards[winning_card_index]
    sum_of_unmarked = sum_of_unmarked_in_card(winning_card, winning_number_index)
    print(
        f'#{winning_card_index} card wins with number {winning_number}. Answer = {winning_number} * {sum_of_unmarked} '
        f'( sum of unmarked ) = {winning_number * sum_of_unmarked}')
    return winning_number * sum_of_unmarked


def winning_index_for_card(card: str):
    _card = card_to_matrix(card, mapper=lambda x: bingo_index_map[x] if x in bingo_index_map else -1)
    # get the max for each row and column
    row_max = min([max(r) for r in _card])
    T = transpose(_card)
    col_max = max([max(r) for r in T])
    return min(row_max, col_max)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=4)
    input_data = puzzle.input_data
    bingo_numbers = puzzle.input_data.split("\n")[0].split(",")
    bingo_index_map = {n.strip(): i for i, n in enumerate(bingo_numbers)}
    cards = puzzle.input_data.split("\n\n")[1:-1]
    puzzle.answer_a = proccess_a(cards)
    puzzle.answer_b = proccess_b(cards)
