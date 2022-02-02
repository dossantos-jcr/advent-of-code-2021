from day1 import get_input, submit_answer

DAY, YEAR = 10, 2021


def remove_chunks(line: str) -> str:
    """
    Removes all empty chunks in each iteration until there are none left.
    Returns the remaining characters.
    """
    old_length = len(line)
    reduced_line = line.replace("()", "").replace("[]", ""). \
        replace("{}", "").replace("<>", "")
    # break condition
    if len(reduced_line) == old_length:
        return reduced_line
    return remove_chunks(reduced_line)


def is_corrupted(line: str) -> bool:
    """
    Returns True if the line is corrupted, otherwise False.
    """
    closing_chars = ")]}>"
    for char in closing_chars:
        # any remaining closing characters left indicate a corrupted line
        if char in remove_chunks(line):
            return True
    return False


def score_corrupted_lines(data: list) -> int:
    """
    Finds the first closing character in corrupted lines and adds its
    corresponding score.
    Returns the sum of all scores.
    """
    score = 0
    get_score = {")": 3, "]": 57, "}": 1197, ">": 25137}
    for line in data:
        if is_corrupted(line):
            for char in remove_chunks(line):
                if char in ")]}>":
                    score += get_score[char]
                    break
    return score


def score_incomplete_lines(data: list) -> int:
    """
    Finds the closing characters required to complete each lines and
    adds the corresponding score. (Always an odd number of incomplete lines).
    Returns the median score.
    """
    score_sum = []
    get_score = {"(": 1, "[": 2, "{": 3, "<": 4}
    for line in data:
        if not is_corrupted(line):
            score = 0
            for char in remove_chunks(line)[::-1]:
                score = score*5 + get_score[char]
            score_sum.append(score)

    return sorted(score_sum)[len(score_sum) // 2]


def main():
    # get data
    data = get_input(DAY, YEAR, transform="lines")
    # check data for complete lines, code assumes none exist
    for line in data:
        if len(remove_chunks(line)) == 0:
            print("Complete line detected!")
            break

    # part 1
    part1_answer = score_corrupted_lines(data)
    print(f"Part 1 Answer: {part1_answer}")

    # part 2
    part2_answer = score_incomplete_lines(data)
    print(f"Part 2 Answer: {part2_answer}")

    # submit answers
    submit_answer(part1_answer, "a", DAY, YEAR, submit=False)
    submit_answer(part2_answer, "b", DAY, YEAR, submit=False)


if __name__ == "__main__":
    main()
