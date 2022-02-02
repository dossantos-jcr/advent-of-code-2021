import itertools as it
from time import time
from heapq import heapify, heappush, heappop
import numpy as np
import pygame
from day1 import get_input, submit_answer


DAY, YEAR = 15, 2021

BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)


def draw_grid(window: pygame.Surface, grid_shape: tuple) -> None:
    """
    Draws lines on the window to create a grid specified by grid_shape.
    """
    # shape of the window
    width, height = pygame.display.get_surface().get_size()
    # shape of the grid to be drawn
    rows, cols = grid_shape
    window.fill(WHITE)
    # horizontal lines
    for y in range(0, height, height//rows):
        pygame.draw.line(window, BLACK, (0, y), (width, y))
    # vertical lines
    for x in range(0, width, width//cols):
        pygame.draw.line(window, BLACK, (x, 0), (x, height))
    pygame.display.update()


def visualise(grid: np.ndarray, start_position: tuple,
              end_position: tuple) -> None:
    """
    Visualises the A* algorithm as it seeks the shortest path from the
    start_position to the end_position on a grid.
    """
    pygame.init()
    rows, cols = grid.shape
    # create window of at least 400 x 400 pixels, up to 1000x 1000 pixels
    width, height = min(max(8*cols, 400), 1000), min(max(8*rows, 400), 1000)
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(
        f"Visualising A* Algorithm: {rows} x {cols} grid")
    draw_grid(window, (rows, cols))

    running, waiting, algo_running = True, True, True
    while running:
        # waits for user input before starting algorithm
        while waiting:
            font = pygame.freetype.SysFont("arial", 60)
            font.render_to(window, (200, 300), "Press 'Enter' to start", BLACK)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # stop waiting and run algorithm when 'enter' is pressed
                    if event.key == pygame.key.key_code("return"):
                        draw_grid(window, (rows, cols))
                        pygame.display.update()
                        waiting = False
                # exit everything if pygame window is closed
                elif event.type == pygame.QUIT:
                    waiting, algo_running, running = False, False, False
        # runs the A* algorithm
        while algo_running:
            path_length = visual_astar(window,
                                       grid, start_position, end_position)
            if path_length is not None:
                font = pygame.freetype.SysFont("arial", 60)
                font.render_to(window, (200, 600),
                               f"Path Length: {path_length}", BLACK)
                pygame.display.update()
            algo_running = False

        # stops running when pygame window is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


def get_neighbours(point: tuple, shape: tuple) -> list:
    """
    Returns the coordinates (numpy array indices) neighbouring the given point.
    """
    row, col = point
    shape_r, shape_c = shape
    return tuple((row + i, col + j)
                 for i, j in ((0, -1), (0, 1), (-1, 0), (1, 0))
                 if ((0 <= row+i < shape_r) and (0 <= col+j < shape_c)))


def manhattan(u: tuple, v: tuple) -> int:
    """
    Returns the manhattan (rectilinear) distance between the two points.
    """
    return abs(u[0] - v[0]) + abs(u[1] - v[1])


class Node:
    """
    Class that stores the f,g and h values used by the A* algorithm
    for each point (node) in the grid along with the location in the grid
    and parent node.
    """

    def __init__(self, position: tuple, parent: tuple):
        self.position = position
        self.parent = parent
        # sum of g and h
        self.f = 0
        # true distance to start
        self.g = 0
        # estimated distance to end (always equal or less than true distance)
        self.h = 0

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def draw(self, window, colour, grid_shape) -> None:
        """
        Draws the square in the window corresponding to the node with the
        specified colour.
        """
        # window shape
        window_width, window_height = pygame.display.get_surface().get_size()
        # grid shape
        rows, cols = grid_shape
        # square shape
        width, height = window_width//cols, window_height//rows
        y, x = self.position
        # draw square
        pygame.draw.rect(window, colour, (x*width+1, y*height+1,
                                          width-1, height-1))
        pygame.display.update()

    def draw_path(self, window, colour, shape) -> None:
        """
        Traces the lineage of the node and draws all parent nodes on the grid.
        """
        self.draw(window, colour, shape)
        node = self.parent
        # stop when we have reached the start node
        while node is not None:
            # draw ancestors
            node.draw(window, BLUE, shape)
            node = node.parent


def visual_astar(window: pygame.Surface, grid: np.ndarray,
                 start_position: tuple, end_position: tuple) -> int:
    """
    Executes the A* algorithm to find the shortest path from the start and end
    nodes. Draws the nodes on the window, colour coded depending on node type
    and returns the shortest path length.
    """
    start_time = time()
    # grid shape
    shape = grid.shape
    queue, closed = [], set()
    # creating priority queue using a min heap
    heapify(queue)
    # creating start and end nodes
    start, end = Node(start_position, None), Node(end_position, None)
    start.f = start.g = start.h = end.f = end.g = end.h = 0
    # add start node to the queue
    heappush(queue, start)
    # set containing all barriers on the grid
    barriers = set()
    for i in range(shape[0]):
        for j in range(shape[1]):
            if grid[i, j] < 0:
                node = Node((i, j), None)
                barriers.add(node)
                node.draw(window, RED, shape)

    while len(queue) > 0:
        # stop algorithm if 'Esc' key is pressed
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.key.key_code("escape"):
                    return
        # remove node with lowest f value from queue
        parent = heappop(queue)

        # skip if node already in closed set
        if parent in closed:
            continue

        # add node to closed set
        closed.add(parent)
        # draw node in closed set
        parent.draw(window, GREY, shape)

        # check if end node found
        if parent == end:
            time_elapsed = time() - start_time
            print(f"Shortest path length is {parent.g}.",
                  f"Time elapsed: {time_elapsed:.3f} seconds.")
            # draw shortest path
            parent.draw_path(window, BLUE, shape)
            return parent.g

        # create children nodes
        for child_position in get_neighbours(parent.position, shape):
            # create child node
            child = Node(child_position, parent)
            # skip if child is a barrier
            if child in barriers:
                continue
            # skip if child in closed set
            if child in closed:
                continue
            # using manhattan metric as heuristic
            child.g = parent.g + grid[child.position]
            child.h = manhattan(child.position, end.position)
            child.f = child.g + child.h
            # skip if child in queue with larger distance to start
            if len([node for node in queue if
                    child == node and child.g > node.g]) > 0:
                continue
            # add child node to the queue
            heappush(queue, child)
            # draw node in queue
            child.draw(window, GREEN, shape)


def repeat_grid(grid: np.ndarray, repeat: int) -> np.ndarray:
    """
    Returns the grid after repeating the grid the specified number of
    times. 'Repeating' involes incrementing all values and resetting values
    larger than 9 back to 1.
    Intended for use in conjunction with 'create_mega_grid()'.
    """
    new_grid = grid.copy()
    for _ in range(repeat):
        # increment all values by 1 for each repetition
        new_grid += 1
        # all values larger than 9 are reset to 1
        new_grid[new_grid > 9] = 1
    return new_grid


def create_mega_grid(grid: np.ndarray, template: np.ndarray) -> np.ndarray:
    """
    Procedurally generates a new grid using the template, which specifies
    how to repeat the original grid.
    """
    # grid shape
    rows, cols = grid.shape
    # template shape
    mult_rows, mult_cols = template.shape

    mega_grid = np.full((rows * mult_rows, cols * mult_cols), 0)
    for r in range(mult_rows):
        for c in range(mult_cols):
            mega_grid[rows*r: rows*(r+1), cols*c: cols*(c+1)] = \
                repeat_grid(grid, template[r, c])
    return mega_grid


def fast_dijkstra(grid: np.ndarray, start_position: tuple,
                  end_position: tuple) -> int:
    """
    Dijkstra algorithm optimised for speed. Returns the shortest path length
    between the start and end nodes.
    """
    # grid shape
    grid_r, grid_c = grid.shape
    queue, closed = [], set()
    # priority queue
    heapify(queue)
    heappush(queue, (0, start_position))

    while len(queue) > 0:
        # get node with lowest g value
        cost, position = heappop(queue)
        # stop if end node found
        if position == end_position:
            return cost
        # skip if node already in closed set
        if position in closed:
            continue
        # add node to the closed set
        closed.add(position)
        # get all neighbours of the node
        row, col = position
        neighbours = \
            [(row+i, col+j) for i, j in ((0, 1), (1, 0), (-1, 0), (0, -1))
             if (0 <= row+i < grid_r and 0 <= col+j < grid_c)]

        for neighbour in neighbours:
            # skip if neighbouring node in closed set
            if neighbour in closed:
                continue
            # add neighbouring node to the queue
            heappush(queue, (cost + grid[neighbour], neighbour))


def main():
    # get data
    data_raw = get_input(DAY, YEAR, transform="lines")
    rows, cols = len(data_raw), len(data_raw[0])
    data = np.full((rows, cols), 0)
    for i, j in it.product(range(rows), range(cols)):
        data[i, j] = data_raw[i][j]
    # template to procedurally generate larger grid
    template = np.array([[0, 1, 2, 3, 4],
                         [1, 2, 3, 4, 5],
                         [2, 3, 4, 5, 6],
                         [3, 4, 5, 6, 7],
                         [4, 5, 6, 7, 8]])
    # create larger grid
    mega_grid = create_mega_grid(data, template)

    # visualise A* on the grid (uncomment to run)
    # visualise(data, (0, 0), (99,  99))

    # visualise A* on the mega grid (uncomment to run)
    # visualise(mega_grid, (0,0), (499, 499))

    # create grid with barriers, may not be solvable if unlucky
    grid = np.full(data.shape, 1)
    grid = np.random.randint(0, high=10, size=(100, 100))
    grid[0, 0], grid[99, 99] = 1, 1
    grid[grid == 0] = -1
    grid[:80, 20] = -1
    grid[20:, 50] = -1
    grid[20, 50:70] = -1

    # visualise A* on grid with barriers
    visualise(grid, (0, 0), (99, 99))

    # part 1
    start_time = time()
    part1_answer = fast_dijkstra(data, (0, 0), (99, 99))
    print(f"Part 1 Answer: {part1_answer}.",
          f"Time Elapsed: {time() - start_time:.3f}")

    # part
    start_time = time()
    part2_answer = fast_dijkstra(mega_grid, (0, 0), (499, 499))
    print(f"Part 2 Answer: {part2_answer}.",
          f"Time Elapsed: {time() - start_time:.3f}")

    # submit answers
    submit_answer(part1_answer, "a", DAY, YEAR, submit=False)
    submit_answer(part2_answer, "b", DAY, YEAR, submit=False)


if __name__ == "__main__":
    main()
