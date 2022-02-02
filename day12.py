from day1 import get_input, submit_answer

DAY, YEAR = 12, 2021


def create_cave_map(data: list) -> dict:
    """
    Returns a dictionary of each cave (keys) and a set of all caves connected
    to them (values).
    Excludes the 'end' cave since you cannot leave it once there.
    """
    # set of all caves, to be used as keys for the dictionary
    caves = set()
    for connection in data:
        caves = caves | {connection[0]} | {connection[1]}
    # dictionary of all connections
    cave_map = {}
    for cave in caves:
        cave_map[cave] = set()
    for connection in data:
        for i, j in zip((0, 1), (1, 0)):
            if connection[j] != "start":
                cave_map[connection[i]] = \
                    cave_map[connection[i]] | {connection[j]}
    del cave_map["end"]
    return cave_map


def visited_small_twice(cave_map: dict, path: list) -> bool:
    """
    Returns True if any small cave has already been visited twice thus far
    in the path, else False.
    """
    for cave in cave_map:
        if cave.islower() and cave != "start":
            if path.count(cave) > 1:
                return True
    return False


def find_paths(cave_map: dict, paths: list = (["start"],),
               repeat: bool = False) -> list:
    """
    Returns a list of all valid paths (also lists) from 'start' to 'end'.
    If repeat = True, a single small cave may be visited twice, otherwise no
    repeat visits are allowed.
    """
    new_paths = []
    for path in paths:
        # skip path if it has already ended
        if path[-1] == "end":
            new_paths.append(path)
            continue
        # add new destination caves to the path
        for destination in cave_map[path[-1]]:
            # disallow repeating small caves
            if destination.islower() and destination in path and \
                    (not repeat or visited_small_twice(cave_map, path)):
                continue
            new_paths.append(path + [destination])
    if len(new_paths) == len(paths):
        return new_paths
    return find_paths(cave_map, paths=new_paths, repeat=repeat)


def main():
    # get data
    data_raw = get_input(DAY, YEAR, transform="lines")
    data = []
    for connection in data_raw:
        data.append(tuple(connection.split("-")))

    # part 1
    cave_map = create_cave_map(data)
    part1_answer = len(find_paths(cave_map))
    print(f"Part 1 Answer: {part1_answer}")

    # part 2
    part2_answer = len(find_paths(cave_map, repeat=True))
    print(f"Part 2 Answer: {part2_answer}")

    # submit answers
    submit_answer(part1_answer, "a", DAY, YEAR, submit=False)
    submit_answer(part2_answer, "b", DAY, YEAR, submit=False)


if __name__ == "__main__":
    main()
