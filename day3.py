import numpy as np
from day1 import get_input, submit_answer

DAY, YEAR = 3, 2021


def find_common_bit(array: np.ndarray, criteria: str) -> int:
    """
    Returns the most, or least, common bit in a numpy array.
    Ties are resolved as specified by the challenge.
    Note return is int and not str.
    """
    count1 = sum(array)
    count0 = len(array) - count1
    if "most" in criteria:
        return 0 if count0 > count1 else 1
    elif "least" in criteria:
        return 1 if count1 < count0 else 0
    else:
        print(f"Incorrect {criteria= } specified")
        return None


def most_common_bits(array: np.ndarray) -> str:
    """
    Returns a string of the most common bits in each position.
    """
    columns = array.shape[1]
    bits = ""
    for i in range(columns):
        bits += str(find_common_bit(array[:, i], "most"))
    return bits


def filtered_common_bits(array: np.ndarray, criteria: str) -> str:
    """
    Returns the single row left after filtering the array by the most,
    or least, common bit in each position.
    Will fail and throw an error if no unique row is found (duplicates).
    """
    rows = array.shape[0]
    i = 0
    array_filtered = np.copy(array)
    while rows > 1:
        col_i = array_filtered[:, i]
        array_filtered = array_filtered[col_i ==
                                        find_common_bit(col_i, criteria)]
        i += 1
        rows = array_filtered.shape[0]
    return np.array2string(array_filtered, separator="").strip("[]")


def flip_bits(bits: str) -> str:
    """
    Swaps all the '1's and '0's
    """
    return bits.replace("1", "temp").replace("0", "1").replace("temp", "0")


def main():
    # get data and load it into an numpy array
    get_input(DAY, YEAR)
    data = np.genfromtxt("03_2021_input.txt", dtype="u1", delimiter=1)

    # part 1
    gamma_rate = most_common_bits(data)
    epsilon_rate = flip_bits(gamma_rate)
    part1_answer = int(gamma_rate, 2) * int(epsilon_rate, 2)
    print(f"Part 1 Answer: {part1_answer}")

    # part 2
    oxygen_generator_rating = filtered_common_bits(data, "most")
    co2_scrubber_rating = filtered_common_bits(data, "least")
    part2_answer = int(
        oxygen_generator_rating, 2) * int(co2_scrubber_rating, 2)
    print(f"Part 2 Answer: {part2_answer}")

    # submit answers
    submit_answer(part1_answer, "a", DAY, YEAR, submit=False)
    submit_answer(part2_answer, "b", DAY, YEAR, submit=False)


if __name__ == "__main__":
    main()
