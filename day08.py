from day1 import get_input, submit_answer

DAY, YEAR = 8, 2021


def is_unique_digit(segments: str) -> bool:
    """
    Returns bool whether segments represents a digit with
    unique segments length.
    """
    unique_digit_segments = {2: 1, 3: 7, 4: 4, 7: 8}
    return len(segments) in unique_digit_segments


def find_digit(segments: str) -> int:
    """
    Returns the possible digit(s) represented by the segments.
    key: length of segments, value: digit number(s)
    """
    digit_segments = {2: 1, 3: 7, 4: 4, 5: (2, 3, 5), 6: (0, 6, 9), 7: 8}
    return digit_segments[len(segments)]


def count_unique_digits(data: list) -> int:
    """
    Will detect if digits 1,4,7,8 are present in the outputs and
    return a total count of detections.
    'Unique' digits are those with a unique segments length.
    """
    is_unique = []
    for line in data:
        for output in line[1].split(" "):
            is_unique.append(is_unique_digit(output))
    return sum(is_unique)


def contains_all(string: str, search: str) -> bool:
    """
    Returns True if string contains all set of characters in search,
    else False.
    """
    for character in search:
        if character not in string:
            return False
    return True


def decode_signals(signals_raw: str) -> dict:
    """
    # Returns a dictionary of segments as keys and the corresponding digits
    # as values
    """
    """
        0:      1:      2:      3:      4:
     aaaa    ....    aaaa    aaaa    ....
    b    c  .    c  .    c  .    c  b    c
    b    c  .    c  .    c  .    c  b    c
     ....    ....    dddd    dddd    dddd
    e    f  .    f  e    .  .    f  .    f
    e    f  .    f  e    .  .    f  .    f
     gggg    ....    gggg    gggg    ....

      5:      6:      7:      8:      9:
     aaaa    aaaa    aaaa    aaaa    aaaa
    b    .  b    .  .    c  b    c  b    c
    b    .  b    .  .    c  b    c  b    c
     dddd    dddd    ....    dddd    dddd
    .    f  e    f  .    f  e    f  .    f
    .    f  e    f  .    f  e    f  .    f
     gggg    gggg    ....    gggg    gggg
    """
    signals = signals_raw.split(" ")

    # key: digit(s), value: segments
    signal_dict = {}
    signal_235, signal_069 = [], []
    for signal in signals:
        signal = "".join(sorted(signal))
        signal_digits = find_digit(signal)
        # digit: 1, 4, 7, 8 (length uniquely determines digit)
        if is_unique_digit(signal):
            signal_dict[signal_digits] = signal
        # digits = (2, 3, 5)
        elif signal_digits == (2, 3, 5):
            signal_235.append(signal)
        # digits = (0, 6, 9)
        else:
            signal_069.append(signal)
        signal_dict[(2, 3, 5)] = signal_235
        signal_dict[(0, 6, 9)] = signal_069

    for segments in signal_dict[(0, 6, 9)]:
        # find digit '6', it's the only digit in (0, 6, 9) that
        # doesn't contain all the segments from digit '1'
        if not contains_all(segments, signal_dict[1]):
            signal_dict[6] = segments
        # find digit '9', it's the only digit in (0, 6, 9) that
        # contains all the segments from digit '4'
        elif contains_all(segments, signal_dict[4]):
            signal_dict[9] = segments
        # only digit '0' is left as a possibility
        else:
            signal_dict[0] = segments

    for segments in signal_dict[(2, 3, 5)]:
        # find digit '3', it's the only digit in (2, 3, 5) that
        # contains all the segments from digit '1'
        if contains_all(segments, signal_dict[1]):
            signal_dict[3] = segments
        # find digit '5', it's the only digit in (2, 3, 5) that
        # is fully contained within digit '6'
        elif contains_all(signal_dict[6], segments):
            signal_dict[5] = segments
        # process of elimination leaves digit '2' as the only possibility
        else:
            signal_dict[2] = segments

    return {segment: digit for digit, segment in signal_dict.items()
            if digit not in ((0, 6, 9), (2, 3, 5))}


def decode_output(output_raw: str, decoder: dict) -> int:
    """
    Returns the output value as an integer after applying the decoder
    """
    output_digits = ""
    for output in output_raw.split(" "):
        output = "".join(sorted(output))
        output_digits += str(decoder[output])
    return int(output_digits)


def sum_all_outputs(data: list) -> int:
    """
    Returns the sum of all the output values
    """
    total = 0
    for line in data:
        decoder = decode_signals(line[0])
        total += decode_output(line[1], decoder)
    return total


def main():
    # get data
    data_raw = get_input(DAY, YEAR, transform="lines")
    # data(list) contains each line(tuple) consisting of two tuples:
    # [( (signals: str), (outputs: str) ), ...]
    data = []
    for line in data_raw:
        signals, _, outputs = line.partition(" | ")
        data.append((signals, outputs))

    # part 1
    part1_answer = count_unique_digits(data)
    print(f"Part 1 Answer: {part1_answer}")

    # part 2
    part2_answer = sum_all_outputs(data)
    print(f"Part 2 Answer: {part2_answer}")

    # submit answers
    submit_answer(part1_answer, "a", DAY, YEAR, submit=False)
    submit_answer(part2_answer, "b", DAY, YEAR, submit=False)


if __name__ == "__main__":
    main()
