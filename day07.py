from day1 import get_input, submit_answer

DAY, YEAR = 7, 2021


def find_optimal_position(positions: list, constant_rate: bool = True) -> list:
    """
    Returns the fuel consumed to align all the crab submarines at the
    optimal alignment position.
    """
    total_fuel_consumption = []
    # check all possible alignment positions
    for alignment_position in range(max(positions) + 1):
        fuel_consumption = 0
        for position in positions:
            distance_moved = abs(position - alignment_position)
            # if each step consumes the same amount of fuel
            if constant_rate:
                fuel_consumption += distance_moved
            # if each step consumes 1 more fuel than the last
            else:
                # sum of first n natural numbers is (1/2)(n)(n+1)
                # courtesy of Gauss
                fuel_consumption += distance_moved*(distance_moved + 1)//2
        total_fuel_consumption.append(fuel_consumption)
    return min(total_fuel_consumption)


def main():
    # get data
    data = [int(number) for number in get_input(DAY, YEAR).split(",")]

    # part 1
    part1_answer = find_optimal_position(data)
    print(f"Part 1 Answer: {part1_answer}")

    # part 2
    part2_answer = find_optimal_position(data, constant_rate=False)
    print(f"Part 2 Answer: {part2_answer}")

    # submit answers
    submit_answer(part1_answer, "a", DAY, YEAR, submit=False)
    submit_answer(part2_answer, "b", DAY, YEAR, submit=False)


if __name__ == "__main__":
    main()
