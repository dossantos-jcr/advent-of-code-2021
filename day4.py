import numpy as np
from day1 import get_input, submit_answer

DAY, YEAR = 4, 2021


def win_checker(array: np.ndarray) -> bool:
    """
    Checks if any row or column contains all True values in
    the array of booleans. Assumes a square array.
    """
    size = len(array)
    for i in range(size):
        if np.all(array[:, i]) or np.all(array[i, :]):
            return True
    return False


def play_bingo(bingo_cards: list, numbers_drawn: int) -> list:
    """
    Returns a list of lists containing the winning bingo card array,
    the array of booleans, the number drawn at the moment that the
    bingo card won and the win order.
    """
    cards = bingo_cards.copy()
    # list containing an array of booleans for each bingo card
    cards_bools = [np.full((5, 5), False, dtype=bool)] * len(cards)

    winning_cards = []
    for i, card in enumerate(cards):
        for win_order, number in enumerate(numbers_drawn):
            cards_bools[i] = np.add(cards_bools[i], card == number)
            if win_checker(cards_bools[i]):
                winning_cards.append([card, cards_bools[i], number, win_order])
                break
    # sorts list by win_order, ie from the first winning card to the last
    return sorted(winning_cards, key=lambda x: x[3])


def score_bingo_card(card: list) -> int:
    """
    Scores a bingo card according to the challenge: multiply last drawn number
    by the sum of unmarked numbers.
    """
    return sum(card[0][~card[1]]) * card[2] \
        if win_checker(card[1]) else 0


def main():
    # get raw data
    data_raw = get_input(DAY, YEAR)
    # extract bingo numbers drawn as a list of ints
    numbers_drawn_raw, _, bingo_cards_raw = data_raw.partition("\n")
    numbers_drawn = [int(number) for number in numbers_drawn_raw.split(",")]
    # extract bingo cards as a list containing individual cards as numpy arrays
    bingo_cards_raw = bingo_cards_raw.splitlines()
    bingo_cards = []
    for i in range(0, len(bingo_cards_raw), 6):
        card = bingo_cards_raw[i + 1: i + 6]
        card_array = np.array([row.split() for row in card], dtype=int)
        bingo_cards.append(card_array)

    # play bingo !
    winning_bingo_cards = play_bingo(bingo_cards, numbers_drawn)

    # part 1
    first_winning_bingo_card = winning_bingo_cards[0]
    part1_answer = score_bingo_card(first_winning_bingo_card)
    print(f"Part 1 Answer: {part1_answer}")

    # part 2
    last_winning_bingo_card = winning_bingo_cards[-1]
    part2_answer = score_bingo_card(last_winning_bingo_card)
    print(f"Part 2 Answer: {part2_answer}")

    # submit answers
    submit_answer(part1_answer, "a", DAY, YEAR, submit=False)
    submit_answer(part2_answer, "b", DAY, YEAR, submit=False)


if __name__ == "__main__":
    main()
