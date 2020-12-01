""" --- Day 1: Report Repair ---

Before you leave, the Elves in accounting just need you to fix your expense
report (your puzzle input); apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then
multiply those two numbers together.

For example, suppose your expense report contained the following:

1721
979
366
299
675
1456

In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying
them together produces 1721 * 299 = 514579, so the correct answer is 514579.

Of course, your expense report is much larger. Find the two entries that sum to
2020; what do you get if you multiply them together?


--- Part Two ---

The Elves in accounting are thankful for your help; one of them even offers you
a starfish coin they had left over from a past vacation. They offer you a
second one if you can find three numbers in your expense report that meet the
same criteria.

Using the above example again, the three entries that sum to 2020 are 979, 366,
and 675. Multiplying them together produces the answer, 241861950.

In your expense report, what is the product of the three entries that sum to
2020?
"""

import operator
import itertools
import functools


def parse(fileobj, factory=int):
    yield from map(factory, fileobj)


def n_nums_that_sum_to(total, xs, n=2):
    yield from next(
        filter(lambda ns: sum(ns) == total, itertools.product(xs, repeat=n))
    )


def product(*args):
    return functools.reduce(operator.mul, args, 1)


def part1(infile, n=2):
    return product(*n_nums_that_sum_to(2020, parse(infile), n))


def part2(infile):
    return part1(infile, n=3)
