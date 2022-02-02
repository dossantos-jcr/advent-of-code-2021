import numpy as np
from day1 import get_input, submit_answer

DAY, YEAR = 13, 2021


def generate_paper(points: tuple) -> np.ndarray:
    """
    Returns a numpy array of '0's and '1's with '1's at each provided point.
    """
    rows = max(points, key=lambda x: x[0])[0] + 1
    cols = max(points, key=lambda x: x[1])[1] + 1
    grid = np.full((rows, cols), 0)
    for point in points:
        grid[point] = 1
    return grid


def fold_paper(paper: np.ndarray, instruction: tuple) -> np.ndarray:
    """
    Returns the paper array after folding it per the instruction.
    All points being mapped to are assigned '1' if any input points are '1'.
    Vertical (axis = 'col') folds maps points to the right of the fold
    onto the left side, ie the paper is 'folded to the left'.
    Similarly, horizontal folds are 'folded up'.
    """
    grid = paper.copy()
    rows, cols = paper.shape
    axis, index = instruction
    if axis == "col":
        for i in range(rows):
            for j in range(1, cols - index):
                # compares columns on either side of the fold <-|-> ... <--|-->
                grid[i, index - j] = grid[i, index - j] or grid[i, index + j]
        return grid[:, :index]
    else:
        for j in range(cols):
            for i in range(1, rows - index):
                # compares rows on either side of the fold
                grid[index - i, j] = grid[index - i, j] or grid[index + i, j]
        return grid[:index, :]


def get_activation_code(paper: np.ndarray, instructions: tuple) -> np.ndarray:
    """
    Folds the paper repeatedly until all instructions have been performed and
    then prints the activation code. Returns the folded paper nump array.
    """
    grid = paper.copy()
    for instruction in instructions:
        grid = fold_paper(grid, instruction)
    # converts the numpy array into a more readable form
    code = ""
    for row in range(grid.shape[0]):
        code_row = ""
        for x in np.nditer(grid[row, :]):
            code_row += str(x)
        code += code_row + "\n"
    print(code.replace("0", ".").replace("1", "@"))
    return grid


def main():
    # get data
    data_raw = get_input(DAY, YEAR, transform="lines")
    points_raw = data_raw[:data_raw.index("")]
    instructions_raw = data_raw[data_raw.index("") + 1:]
    # tuple containing each point's indices as (row, column)
    points = []
    for point in points_raw:
        col, row = point.split(",")
        points.append((int(row), int(col)))
    points = tuple(points)

    # tuple containing each instruction as (axis, index)
    instructions = []
    for instruction in instructions_raw:
        instruction = instruction.strip("fold along")
        instruction = instruction.replace("x", "col").replace("y", "row")
        instruction = instruction.split("=")
        instruction[1] = int(instruction[1])
        instruction = tuple(instruction)
        instructions.append(instruction)
    instructions = tuple(instructions)

    # part 1
    paper = generate_paper(points)
    part1_answer = np.sum(fold_paper(paper, instructions[0]))
    print(f"Part 1 Answer: {part1_answer}")

    # part 2
    code = get_activation_code(paper, instructions)
    part2_answer = "HECRZKPR"
    print(f"Part 2 Answer: {part2_answer}")

    # submit answers
    submit_answer(part1_answer, "a", DAY, YEAR, submit=False)
    submit_answer(part2_answer, "b", DAY, YEAR, submit=False)


if __name__ == "__main__":
    main()
