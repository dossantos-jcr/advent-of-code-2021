from collections import Counter
from day1 import get_input, submit_answer

DAY, YEAR = 6, 2021


def simulate_lanternfish(fish_timers: list, days: int) -> int:
    """
    Grows the lanternfish population until the specified day and returns a
    count of the total number of lanternfish on that day.
    """
    counter = Counter(fish_timers)
    # list of the count of timers, where corresponding index is the timer value
    # eg timers[2] is the number of fish with timer = 2
    timers = [counter[timer] for timer in range(9)]

    for _ in range(days):
        births = timers[0]
        # count down all timers
        for t in range(8):
            timers[t] = timers[t+1]
        # new fish born
        timers[8] = births
        # reset birthgivers
        timers[6] += births
    return sum(timers)


def main():
    # get data
    data = [int(number) for number in get_input(DAY, YEAR).split(",")]

    # part 1
    part1_answer = simulate_lanternfish(data, 80)
    print(f"Part 1 Answer: {part1_answer}")

    # part 2
    part2_answer = simulate_lanternfish(data, 256)
    print(f"Part 2 Answer: {part2_answer}")

    # submit answers
    submit_answer(part1_answer, "a", DAY, YEAR, submit=False)
    submit_answer(part2_answer, "b", DAY, YEAR, submit=False)


if __name__ == "__main__":
    main()
