import operator as op
from itertools import product as cartesian_product
from functools import reduce


def parse(fileobj, factory=float):
    return map(factory, fileobj)


def n_nums_that_sum_to(total, xs, n=2):
    return next(
        filter(lambda ns: sum(ns) == total, cartesian_product(xs, repeat=n))
    )


def product(*args):
    return reduce(op.mul, args, 1)


def part1(input):
    return product(*n_nums_that_sum_to(2020, parse(input, int)))


def part2(input):
    return product(*n_nums_that_sum_to(2020, parse(input, int), n=3))
