import operator
import itertools
import functools


def parse(fileobj, factory=int):
    return map(factory, fileobj)


def n_nums_that_sum_to(total, xs, n=2):
    return next(
        filter(lambda ns: sum(ns) == total, itertools.product(xs, repeat=n))
    )


def product(*args):
    return functools.reduce(operator.mul, args, 1)


def part1(infile, n=2):
    return product(*n_nums_that_sum_to(2020, parse(infile), n))


def part2(infile):
    return part1(infile, n=3)
