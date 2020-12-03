"""
    With the toboggan login problems resolved, you set off toward the airport.
    While travel by toboggan might be easy, it's certainly not safe: there's
    very minimal steering and the area is covered in trees. You'll need to see
    which angles will take you near the fewest trees.

    Due to the local geology, trees in this area only grow on exact integer
    coordinates in a grid. You make a map (your puzzle input) of the open
    squares (.) and trees (#) you can see. For example:

    ..##.......
    #...#...#..
    .#....#..#.
    ..#.#...#.#
    .#...##..#.
    ..#.##.....
    .#.#.#....#
    .#........#
    #.##...#...
    #...##....#
    .#..#...#.#

    These aren't the only trees, though; due to something you read about once
    involving arboreal genetics and biome stability, the same pattern repeats
    to the right many times:

    ..##.........##.........##.........##.........##.........##.......  --->
    #...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
    .#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
    ..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
    .#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
    ..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....  --->
    .#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
    .#........#.#........#.#........#.#........#.#........#.#........#
    #.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...
    #...##....##...##....##...##....##...##....##...##....##...##....#
    .#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#  --->

    You start on the open square (.) in the top-left corner and need to reach
    the bottom (below the bottom-most row on your map).

    The toboggan can only follow a few specific slopes (you opted for a cheaper
            model that prefers rational numbers); start by counting all the
    trees you would encounter for the slope right 3, down 1:

    From your starting position at the top-left, check the position that is
    right 3 and down 1. Then, check the position that is right 3 and down 1
    from there, and so on until you go past the bottom of the map.

    The locations you'd check in the above example are marked here with O where
    there was an open square and X where there was a tree:

    ..##.........##.........##.........##.........##.........##.......  --->
    #..O#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
    .#....X..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
    ..#.#...#O#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
    .#...##..#..X...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
    ..#.##.......#.X#.......#.##.......#.##.......#.##.......#.##.....  --->
    .#.#.#....#.#.#.#.O..#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
    .#........#.#........X.#........#.#........#.#........#.#........#
    #.##...#...#.##...#...#.X#...#...#.##...#...#.##...#...#.##...#...
    #...##....##...##....##...#X....##...##....##...##....##...##....#
    .#..#...#.#.#..#...#.#.#..#...X.#.#..#...#.#.#..#...#.#.#..#...#.#  --->

    In this example, traversing the map using this slope would cause you to
    encounter 7 trees.

    Starting at the top-left corner of your map and following a slope of right
    3 and down 1, how many trees would you encounter?


    --- Part Two ---

    Time to check the rest of the slopes - you need to minimize the probability
    of a sudden arboreal stop, after all.

    Determine the number of trees you would encounter if, for each of the
    following slopes, you start at the top-left corner and traverse the map all
    the way to the bottom:

        Right 1, down 1.
        Right 3, down 1. (This is the slope you already checked.)
        Right 5, down 1.
        Right 7, down 1.
        Right 1, down 2.

    In the above example, these slopes would find 2, 7, 3, 4, and 2 tree(s)
    respectively; multiplied together, these produce the answer 336.

    What do you get if you multiply together the number of trees encountered on
    each of the listed slopes?

"""

import itertools
import math
import pytest
from fractions import Fraction


def iterate(n: int, f):
    def go(x):
        for _ in range(n):
            f(x)

    return go


def drop(n: int, xs):
    iterate(n, next)(xs)


def traverse_forest(fileobj, slope: Fraction):
    forest = map(
        itertools.cycle,
        map(lambda line: filter(lambda s: not s.isspace(), line), fileobj),
    )
    trees = 0
    offset = 0
    for line in forest:
        drop(offset, line)
        if next(line) == "#":
            trees += 1
        try:
            n = slope.numerator - 1
            current_line = None
            prev_line = None
            while n > 0:
                prev_line = current_line
                current_line = next(forest)
                n -= 1
        except StopIteration:
            forest = iter([prev_line])
            offset += slope.denominator
            continue
        offset += slope.denominator

    return trees


def part1(infile, slope=Fraction(1, 3)):
    if not isinstance(infile, list):
        infile.seek(0)
    return traverse_forest(infile, slope)


def part2(infile):
    slopes = [
        Fraction(n, d) for (n, d) in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    ]
    return math.prod(part1(infile, slope) for slope in slopes)


@pytest.fixture
def sample_data():
    return [
        "..##.......",
        "#...#...#..",
        ".#....#..#.",
        "..#.#...#.#",
        ".#...##..#.",
        "..#.##.....",
        ".#.#.#....#",
        ".#........#",
        "#.##...#...",
        "#...##....#",
        ".#..#...#.#",
    ]


def test_part1(sample_data):
    assert part1(sample_data) == 7


def test_part2(sample_data):
    assert part2(sample_data) == 336
