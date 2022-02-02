import numpy as np
from day1 import get_input, submit_answer

DAY, YEAR = 11, 2021


def update_neighbours(grid: np.ndarray, point: tuple) -> np.ndarray:
    """
    Returns an updated array where the energy levels of all neighbours of the
    point are incremented if they have not already flashed this cycle.
    """
    # padding to facilitate corners and edges
    g = np.pad(grid, 1, mode="constant", constant_values=100)
    # to account for padding
    row, col = point[0] + 1, point[1] + 1
    # increments all neighbours energy levels unless they have already flashed
    for i in (row-1, row, row+1):
        for j in (col-1, col, col+1):
            if g[i, j] != 0:
                g[i, j] += 1
    # sets energy level of point that flashed
    g[row, col] = 0
    # doesn't return padding
    return g[1: -1, 1: -1]


def update_energy_levels(grid: np.ndarray, flash_count: int = 0) -> tuple:
    """
    Returns an updated array of energy levels that have been incremented and
    flashes have been accounted for.
    Also returns the total number of flashes that occured.
    """
    rows, cols = grid.shape
    g = grid.copy()
    new_flashes = 0
    # only increments energy levels once
    if flash_count == 0:
        g += 1
    for i in range(rows):
        for j in range(cols):
            if g[i, j] > 9:
                new_flashes += 1
                g = update_neighbours(g, (i, j))
    new_flash_count = flash_count + new_flashes
    # must re-check all values in case flashing caused chain reaction
    if new_flashes > 0:
        return update_energy_levels(g, flash_count=new_flash_count)
    return (g, new_flash_count)


def count_flashes(data: np.ndarray, steps: int) -> int:
    """
    Returns the total of number of flashes that occured after the specified
    number of steps (cycles).
    """
    step, count = 0, 0
    grid = data.copy()
    while step < steps:
        grid, flash_count = update_energy_levels(grid)
        count += flash_count
        step += 1
    return count


def find_giga_flash(data: np.ndarray, max_steps: int = 1000) -> int:
    """
    Returns the number of steps (cycles) it took for all octopuses to flash
    simultaneously.
    """
    grid = data.copy()
    grid_giga_flash = np.full(grid.shape, 0)
    for step in range(1, max_steps):
        grid = update_energy_levels(grid)[0]
        # checks if all octopuses flashed
        if np.array_equal(grid, grid_giga_flash):
            return step
    print(f"No giga flash found after {max_steps} steps")
    return None


def main():
    # get data
    data_raw = get_input(DAY, YEAR, transform="lines")
    data = np.full((len(data_raw), len(data_raw)), 0, dtype="u1")
    for i, row in enumerate(data_raw):
        for j, number in enumerate(row):
            data[i, j] = number

    # part 1
    part1_answer = count_flashes(data, 100)
    print(f"Part 1 Answer: {part1_answer}")

    # part 2
    part2_answer = find_giga_flash(data)
    print(f"Part 2 Answer: {part2_answer}")

    # submit answers
    submit_answer(part1_answer, "a", DAY, YEAR, submit=False)
    submit_answer(part2_answer, "b", DAY, YEAR, submit=False)


if __name__ == "__main__":
    main()
