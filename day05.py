import numpy as np
from day1 import get_input, submit_answer

DAY, YEAR = 5, 2021


def draw_vents(lines: list, shape: tuple,
               allow_diag: bool = False) -> np.ndarray:
    """
    Draws vents 0n a grid of '0's, where '1' corresponds to a vent point.
    Each overlapping vent point increments this value by 1, the final value is
    the 'height' of the vent.
    """
    """
    |    ---> +ve x axis
    |     0 0 0 0 0
    |     0 0 0 0 0
    V     0 0 0 0 0
    +ve   0 0 0 0 0
    y     0 0 0 0 0
    axis
    """
    grid = np.full(shape, 0, dtype=int)
    for line in lines:
        x0, y0, x1, y1 = line[0][0], line[0][1], line[1][0], line[1][1]
        grid_new_vent = np.full(shape, 0, dtype=int)

        # skips diagonal lines if diagonals are not allowed
        if x0 != x1 and y0 != y1 and not allow_diag:
            continue
        # single vent drawn on temporary grid
        for point in generate_points(line):
            grid_new_vent[point[1], point[0]] = 1
        # vent grid combined with the others
        grid = np.add(grid, grid_new_vent)
    return grid


def generate_points(line: list) -> list:
    """
    Returns a list of the points contained in the vent described by the line.
    eg. Line: '0, 0 -> 2, 2' returns points: [(0,0), (1,1), (2,2)]
    """
    x0, y0, x1, y1 = line[0][0], line[0][1], line[1][0], line[1][1]
    x, y = x0, y0
    points = [(x0, y0)]
    # increments (or decrements) each coordinate until they both match
    while x != x1 or y != y1:
        x = x + np.sign(x1 - x)
        y = y + np.sign(y1 - y)
        points.append((x, y))
    return points


def count_tall_vents(grid: np.ndarray, height: int = 1) -> int:
    """
    Returns a count of all the vents above the specified height in the grid.
    The height of a vent point is the numeric value at that point in the grid.
    """
    heights, counts = np.unique(grid, return_counts=True)
    return sum([counts[i] for i, h in enumerate(heights) if h > height])


def main():
    # get raw data
    data_raw = get_input(DAY, YEAR, transform="lines")
    # list containing tuples of tuples of start and end coordinates
    line_segments = []
    # determines required size of the array to be created
    max_x, max_y = 0, 0
    # processing raw data
    for line_raw in data_raw:
        coords_raw = line_raw.split(" -> ")
        x0, _, y0 = coords_raw[0].partition(",")
        x1, _, y1 = coords_raw[1].partition(",")
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        line_segments.append(((x0, y0), (x1, y1)))
        max_x, max_y = max(max_x, x0, x1), max(max_y, y0, y1)
    # taking into account of 0
    max_x += 1
    max_y += 1

    # part 1
    part1_answer = count_tall_vents(draw_vents(line_segments, (max_y, max_x)))
    print(f"Part 1 Answer: {part1_answer}")

    # part 2
    part2_answer = count_tall_vents(
        draw_vents(line_segments, (max_y, max_x), allow_diag=True))
    print(f"Part 2 Answer: {part2_answer}")

    # submit answers
    submit_answer(part1_answer, "a", DAY, YEAR, submit=False)
    submit_answer(part2_answer, "b", DAY, YEAR, submit=False)


if __name__ == "__main__":
    main()
