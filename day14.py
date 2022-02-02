import itertools as it
from day1 import get_input, submit_answer


DAY, YEAR = 14, 2021


def generate_fresh_dicts(template: str, insertion_rules: list) -> tuple:
    """
    Returns two dictionaries, one of all possible unique pairs of letters
    and one of all possible unique single letters.
    Key: Letter(s) , Value: Count of Letter(s), with all counts set to 0.
    """
    unique_letters = set(template)
    for pair in insertion_rules:
        unique_letters = unique_letters | set(pair)
    letters = sorted(list(unique_letters))
    pairs = {"".join(pair): 0 for pair in it.product(letters, repeat=2)}
    duplicates = {letter: 0 for letter in letters}
    return pairs, duplicates


def polymerize(template: str, insertion_rules: list, steps: int) -> tuple:
    """
    Executes the insertion rules to insert new letters in between each pair.
    Returns a dictionary of all pairs after polymerisation as well as a
    dictionary that tracks duplicate letters, to facilitate counting unique
    elements later.
    Key: Letter(s) , Value: Count of Letter(s)
    """
    # Converts the template string into a dictionary of pairs, while keeping
    # track of how many duplicate letters this process produces.
    # eg. 'ABC' -> 'AB' 'BC' adds one extra 'B'
    pairs, duplicates = generate_fresh_dicts(template, insertion_rules)
    for i in range(len(template)-1):
        pair = template[i:i+2]
        pairs[pair] += 1
        duplicates[pair[1]] += 1
    # compensating for final pair added (no duplicate letter)
    duplicates[template[-1]] -= 1

    # polymerises the chain the specified number of times
    for _ in range(steps):
        new_pairs = generate_fresh_dicts(template, insertion_rules)[0]
        for pair, count in pairs.items():
            # letter to be inserted
            insert = insertion_rules[pair]
            # new pairs added
            new_pairs[pair[0] + insert] += count
            new_pairs[insert + pair[1]] += count
            # keeping track of all duplications
            duplicates[insert] += count
        pairs = new_pairs
    return pairs, duplicates


def get_answer(pairs: dict, duplicates: dict) -> int:
    """
    Returns the difference between the count of the most common element and
    the count of the least common element.
    """
    letters_count = {letter: -count for letter, count in duplicates.items()}
    for pair, count in pairs.items():
        letters_count[pair[0]] += count
        letters_count[pair[1]] += count
    return max(letters_count.values()) - min(letters_count.values())


def main():
    # get data
    data_raw = get_input(DAY, YEAR, transform="lines")
    template = data_raw[:data_raw.index("")][0]
    insertion_rules_raw = data_raw[data_raw.index("")+1:]
    insertion_rules = {}
    for rule in insertion_rules_raw:
        pair, insert = rule.split(" -> ")
        insertion_rules[pair] = insert

    # part 1
    polymer_10 = polymerize(template, insertion_rules, 10)
    part1_answer = get_answer(*polymer_10)
    print(f"Part 1 Answer: {part1_answer}")

    # part 2
    polymer_40 = polymerize(template, insertion_rules, 40)
    part2_answer = get_answer(*polymer_40)
    print(f"Part 2 Answer: {part2_answer}")

    # submit answers
    submit_answer(part1_answer, "a", DAY, YEAR, submit=False)
    submit_answer(part2_answer, "b", DAY, YEAR, submit=False)


if __name__ == "__main__":
    main()
