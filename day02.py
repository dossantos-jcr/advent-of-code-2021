from day1 import get_input, submit_answer

DAY, YEAR = 2, 2021


class Submarine():
    """
    Class that stores the position, depth and aim of the submarine and contains
    methods to set a new course.
    """

    def __init__(self, part: int,
                 horizontal_pos: int = 0, depth: int = 0, aim: int = 0):
        # 'part' determines which instruction set the course corrections will
        # use
        self.part = part
        self.horizontal_pos = horizontal_pos
        self.depth = depth
        self.aim = aim

    def set_course(self, course: list):
        # instruction set for part 1
        if self.part == 1:
            for instruction in course:
                direction, distance = instruction.split()
                distance = int(distance)
                if direction == "forward":
                    self.horizontal_pos += distance
                elif direction == "down":
                    self.depth += distance
                elif direction == "up":
                    self.depth -= distance
                else:
                    print(f"Incorrect course change: {instruction= }")
        # instruction set for part 2
        elif self.part == 2:
            for instruction in course:
                direction, distance = instruction.split()
                distance = int(distance)
                if direction == "forward":
                    self.horizontal_pos += distance
                    self.depth += self.aim * distance
                elif direction == "down":
                    self.aim += distance
                elif direction == "up":
                    self.aim -= distance
                else:
                    print(f"Incorrect course change: {instruction= }")
        else:
            print(f"Incorrect part specified: {self.part= }")


def main():
    # get data
    data = get_input(DAY, YEAR, transform="lines")

    # part 1
    sub1 = Submarine(1)
    sub1.set_course(data)
    part1_answer = sub1.depth * sub1.horizontal_pos
    print(f"Part 1 Answer: {part1_answer}")

    # part 2
    sub2 = Submarine(2)
    sub2.set_course(data)
    part2_answer = sub2.depth * sub2.horizontal_pos
    print(f"Part 2 Answer: {part2_answer}")

    # submit answers
    submit_answer(part1_answer, "a", DAY, YEAR, submit=False)
    submit_answer(part2_answer, "b", DAY, YEAR, submit=False)


if __name__ == "__main__":
    main()
