import os
import aocd

DAY, YEAR = 1, 2021


def get_input(day: int, year: int, write: bool = True,
              transform: str = None) -> str:
    """
    Returns the input data from the advent of code calender on the
    specified day and year.
    Writes a copy into a txt file if write=True and one doesn't already exist.
    Transforms the raw input data if one is specified.

    Parameters
    ----------
    day : int
        Day of the advent of code calender to get input from
        if in {1, 2, 3, ..., 25}.
    year : int
        Year of the advent of code calender to get input from
        if in {2015, 2016, ..., 2021}.
    write : bool, optional
        Writes raw input data to txt file.
        The default is True.
    transform : str, optional
        Transforms raw data if transform = 'numbers' or 'lines'.
        The default is None.

    Returns
    -------
    str
        raw input data as one large string

    """
    try:
        # get raw data
        if os.path.isfile(f"./{day:02d}_{year}_input.txt"):
            with open(f"{day:02d}_{year}_input.txt", "r") as f:
                data_raw = f.read()
        else:
            data_raw = aocd.get_data(day=day, year=year)
            if write:
                with open(f"{day:02d}_{year}_input.txt", "w") as f:
                    f.write(data_raw)

        # optional data transforms
        if transform == "lines":
            return aocd.transforms.lines(data_raw)
        elif transform == "numbers":
            return aocd.transforms.numbers(data_raw)
        else:
            return data_raw

    except aocd.exceptions.PuzzleLockedError as e:
        print(e)
        return ""
    except ValueError as e:
        print(e)
        return ""


def submit_answer(answer, part: str, day: int, year: int, submit: bool = True):
    if submit:
        aocd.post.submit(answer, part=part, day=day, year=year)


def sliding_window(collection, window_size: int,
                   operation=lambda x: x) -> list:
    """
    Returns a list containing the result of the specified operation on each
    window. By default no operation is performed.

    Parameters
    ----------
    collection
        Any data type that can be indexed on which the sliding window
        will operate.
    window_size : int
        The size of the window that will slide over the collection.
    operation : function, optional
        The operation to be performed on each window.
        The default is lambda x: x.

    Returns
    -------
    list
        A list containing the result of each operation on each window.

    """
    windows = []
    for i in range(len(collection) - window_size + 1):
        windows.append(operation(collection[i: i + window_size]))
    return windows


def pairwise_comparison(collection, comparison) -> int:
    """
    Compares each pair in the collection and returns a count
    of how often comparison is True.
    Note that by 'pairs' is meant a sliding window of size = 2.

    Parameters
    ----------
    collection
        Any datatype that can be indexed.
    comparison : function
        Function used to compare each pair.

    Returns
    -------
    int
        Count of all True comparisons

    """
    count = 0
    for previous, current in sliding_window(collection, 2):
        count += comparison(current, previous)
    return count


def main():
    # get data
    data = aocd.transforms.numbers(get_input(DAY, YEAR))
    # greater than operator
    comparison = lambda x, y: x > y

    # part 1
    part1_answer = pairwise_comparison(data, comparison)
    print(f"Part 1 Answer: {part1_answer}")

    # part 2
    part2_answer = pairwise_comparison(
        sliding_window(data, 3, sum), comparison)
    print(f"Part 2 Answer: {part2_answer}")

    # submit answers
    submit_answer(part1_answer, "a", DAY, YEAR, submit=False)
    submit_answer(part2_answer, "b", DAY, YEAR, submit=False)


if __name__ == "__main__":
    main()
