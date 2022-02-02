import numpy as np
from day1 import get_input, submit_answer

DAY, YEAR = 9, 2021


def get_neighbours(point: tuple, grid: np.ndarray,
                   return_coords: bool = False, max_height: int = 10) -> list:
    """
    Returns a list containing all the values of the neighbours of a point
    in a grid.
    Diagonal neighbours do not count.
    Returns the coordinates instead of the values if return_coords = True.
    Only returns neighbours whose values are under the max_height,
    if specified.
    """
    # padding grid to facilitate corner and edge points
    g = np.pad(grid, 1, mode="constant", constant_values=10)
    i, j = point
    coords = ((i, j-1), (i, j+1), (i-1, j), (i+1, j))
    return [(row, col) for row, col in coords if g[row+1, col+1] < max_height] \
        if return_coords else \
        [g[row+1, col+1] for row, col in coords
         if g[row+1, col+1] < max_height]


def find_local_minima(grid: np.ndarray) -> np.ndarray:
    """
    Returns an array of booleans of all minimum values in the grid.
    Diagonal neighbours do not count.
    """
    rows, columns = grid.shape
    grid_bools = np.full(grid.shape, -1, dtype=bool)
    for i in range(rows):
        for j in range(columns):
            grid_bools[i, j] = grid[i, j] < min(get_neighbours((i, j), grid))
    return grid_bools


def sum_risk_level(grid: np.ndarray, grid_bools: np.ndarray) -> int:
    """
    Returns the sum of all the minima risk levels (height +1).
    """
    return np.sum(grid[grid_bools]) + np.sum(grid_bools)


def get_basin_neighbours(points: set, grid: np.ndarray):
    """
    Recursively finds all neighbours within a basin, starting with the minima.
    """
    basin_points = points
    for point in basin_points:
        basin_points = basin_points | \
            set(get_neighbours(point, grid, return_coords=True, max_height=9))

    if len(basin_points) > len(points):
        return get_basin_neighbours(basin_points, grid)
    else:
        return basin_points


def find_basins(grid: np.ndarray, grid_bools: np.ndarray) -> list:
    """
    Returns a list of tuples containing all the coordinates(aka points) of
    each basin along with its size(number of points).
    """
    minima_rows, minima_columns = np.where(grid_bools == True)
    minima_coords = list(zip(minima_rows, minima_columns))
    basins = []
    for point in minima_coords:
        basin_points = get_basin_neighbours({point}, grid)
        basins.append((basin_points, len(basin_points)))
    return sorted(basins, key=lambda x: x[1], reverse=True)


def main():
    # get data
    data_raw = get_input(DAY, YEAR, transform="lines")
    data = np.full((len(data_raw), len(data_raw)), 0, dtype="u1")
    for i, row in enumerate(data_raw):
        for j, number in enumerate(row):
            data[i, j] = number

    # part 1
    minima = find_local_minima(data)
    part1_answer = sum_risk_level(data, minima)
    print(f"Part 1 Answer: {part1_answer}")

    # part 2
    basins = find_basins(data, minima)
    product = 1
    for basin_size in basins[:3]:
        product = product * basin_size[1]
    part2_answer = product
    print(f"Part 2 Answer: {part2_answer}")

    # submit answers
    submit_answer(part1_answer, "a", DAY, YEAR, submit=False)
    submit_answer(part2_answer, "b", DAY, YEAR, submit=False)


if __name__ == "__main__":
    main()
