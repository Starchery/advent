from itertools import zip_longest
import sys


def main():
    try:
        terminal = int(sys.argv[1])
    except (IndexError, ValueError):
        terminal = 19_690_720

    try:
        with open("input.txt", "r") as f:
            data = f.readline()
    except FileNotFoundError:
        print("'input.txt' was not found.")
        return

    result = values_that_produce(terminal, data)
    if not result:
        print(f"No combination exists that produces {terminal}")
    else:
        print(f"x: {result[0]} y: {result[1]}\n{result[0] * 100 + result[1]}")


def values_that_produce(terminal, data):
    for i in range(100):
        for j in range(100):
            if run(convert_program(data, i, j))[0] == terminal:
                return i, j


def convert_program(program, arg1, arg2):
    table = [list(x) for x in chunks(map(lambda x: int(x), program.split(",")),
                                     4)]
    table[0][1], table[0][2] = arg1, arg2
    return table


def run(program):
    prog = [x for xs in program for x in xs]
    for dir in program:
        if dir[0] == 1:
            prog[dir[3]] = prog[dir[1]] + prog[dir[2]]
        elif dir[0] == 2:
            prog[dir[3]] = prog[dir[1]] * prog[dir[2]]
        else:
            break
    return prog


def chunks(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return list(zip_longest(*args, fillvalue=fillvalue))


if __name__ == '__main__':
    main()
