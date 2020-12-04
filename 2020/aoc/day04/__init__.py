""" --- Day 4: Passport Processing ---

    You arrive at the airport only to realize that you grabbed your North Pole
    Credentials instead of your passport. While these documents are extremely
    similar, North Pole Credentials aren't issued by a country and therefore
    aren't actually valid documentation for travel in most of the world.

    It seems like you're not the only one having problems, though; a very long
    line has formed for the automatic passport scanners, and the delay could
    upset your travel itinerary.

    Due to some questionable network security, you realize you might be able to
    solve both of these problems at the same time.

    The automatic passport scanners are slow because they're having trouble
    detecting which passports have all required fields. The expected fields are
    as follows:

        byr (Birth Year)
        iyr (Issue Year)
        eyr (Expiration Year)
        hgt (Height)
        hcl (Hair Color)
        ecl (Eye Color)
        pid (Passport ID)
        cid (Country ID)

    Passport data is validated in batch files (your puzzle input). Each
    passport is represented as a sequence of key:value pairs separated by
    spaces or newlines.  Passports are separated by blank lines.

    Here is an example batch file containing four passports:

    ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
    byr:1937 iyr:2017 cid:147 hgt:183cm

    iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
    hcl:#cfa07d byr:1929

    hcl:#ae17e1 iyr:2013
    eyr:2024
    ecl:brn pid:760753108 byr:1931
    hgt:179cm

    hcl:#cfa07d eyr:2025 pid:166559648
    iyr:2011 ecl:brn hgt:59in

    The first passport is valid - all eight fields are present. The second
    passport is invalid - it is missing hgt (the Height field).

    The third passport is interesting; the only missing field is cid, so it
    looks like data from North Pole Credentials, not a passport at all! Surely,
    nobody would mind if you made the system temporarily ignore missing cid
    fields. Treat this "passport" as valid.

    The fourth passport is missing two fields, cid and byr. Missing cid is
    fine, but missing any other field is not, so this passport is invalid.

    According to the above rules, your improved system would report 2 valid
    passports.

    Count the number of valid passports - those that have all required fields.
    Treat cid as optional. In your batch file, how many passports are valid?


    --- Part Two ---

    The line is moving more quickly now, but you overhear airport security
    talking about how passports with invalid data are getting through. Better
    add some data validation, quick!

    You can continue to ignore the cid field, but each other field has strict
    rules about what values are valid for automatic validation:

        byr (Birth Year) - four digits; at least 1920 and at most 2002.
        iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        hgt (Height) - a number followed by either cm or in:
            If cm, the number must be at least 150 and at most 193.
            If in, the number must be at least 59 and at most 76.
        hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        pid (Passport ID) - a nine-digit number, including leading zeroes.
        cid (Country ID) - ignored, missing or not.

    Your job is to count the passports where all required fields are both
    present and valid according to the above rules. Here are some example
    values:

    byr valid:   2002
    byr invalid: 2003

    hgt valid:   60in
    hgt valid:   190cm
    hgt invalid: 190in
    hgt invalid: 190

    hcl valid:   #123abc
    hcl invalid: #123abz
    hcl invalid: 123abc

    ecl valid:   brn
    ecl invalid: wat

    pid valid:   000000001
    pid invalid: 0123456789

    Here are some invalid passports:

    eyr:1972 cid:100
    hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

    iyr:2019
    hcl:#602927 eyr:1967 hgt:170cm
    ecl:grn pid:012533040 byr:1946

    hcl:dab227 iyr:2012
    ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

    hgt:59cm ecl:zzz
    eyr:2038 hcl:74454a iyr:2023
    pid:3556412378 byr:2007

    Here are some valid passports:

    pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
    hcl:#623a2f

    eyr:2029 ecl:blu cid:129 byr:1989
    iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

    hcl:#888785
    hgt:164cm byr:2001 iyr:2015 cid:88
    pid:545766238 ecl:hzl
    eyr:2022

    iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719

    Count the number of valid passports - those that have all required fields
    and valid values. Continue to treat cid as optional. In your batch file,
    how many passports are valid?

"""

import pytest


def n_digits(n: int):
    return lambda val: all(c.isdigit() for c in val) and len(val) == n


def clamp(lo, hi, x) -> bool:
    return int(x) in range(lo, hi + 1)


def valid_hgt(val) -> bool:
    return (
        "cm" in val
        and clamp(150, 193, val[:-2])
        or "in" in val
        and clamp(59, 76, val[:-2])
    )


def four_digits_in_range(lo, hi):
    return lambda val: n_digits(4)(val) and clamp(lo, hi, val)


def is_one_of(vals):
    return lambda x: any(x == val for val in vals.split())


def valid_hcl(val):
    return (
        val[0] == "#"
        and len(val) == 7
        and all(("0" <= c <= "9") or ("a" <= c <= "f") for c in val[1:])
    )


REQUIRED = {
    "byr": four_digits_in_range(1920, 2002),
    "iyr": four_digits_in_range(2010, 2020),
    "eyr": four_digits_in_range(2020, 2030),
    "hgt": valid_hgt,
    "hcl": valid_hcl,
    "ecl": is_one_of("amb blu brn gry grn hzl oth"),
    "pid": n_digits(9),
    "cid": lambda _: True,
}


def parsed(infile):
    data = "".join(infile)
    yield from (line.replace("\n", " ") for line in data.split("\n\n"))


def all_fields_present(parsed_infile):
    return all(
        map(
            lambda line: all(field in line for field in REQUIRED),
            parsed_infile,
        )
    )


def part1(infile):
    valids = map(
        lambda line: all(field in line + "cid" for field in REQUIRED),
        parsed(infile),
    )
    return sum(valids)


def part2(infile):
    vals = list(parsed(infile))
    import pprint

    vals = list(
        map(
            lambda line: dict(
                map(
                    lambda pair: tuple(pair.strip().split(":")),
                    line.strip().split(" "),
                )
            ),
            vals,
        )
    )
    # pprint.pprint(list(map(lambda d: list(d.values()), vals)))
    # pprint.pprint(sorted(list(REQUIRED.keys())))

    wig = list(
        filter(
            lambda d: d.keys() >= REQUIRED.keys(),
            map(lambda d: {**d, "cid": ()}, vals),
        )
    )
    pprint.pprint(list(map(lambda d: sorted(list(d.items())), wig)))

    tea = list(map(lambda d: [REQUIRED[k](v) for (k, v) in d.items()], wig))
    from json import dumps

    print(dumps(tea))
    # anioop = list(map(all, tea))
    return tea.count([True] * 8)


@pytest.fixture
def sample_data():
    return [
        "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd\n",
        "byr:1937 iyr:2017 cid:147 hgt:183cm\n",
        "\n",
        "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884\n",
        "hcl:#cfa07d byr:1929\n",
        "\n",
        "hcl:#ae17e1 iyr:2013\n",
        "eyr:2024\n",
        "ecl:brn pid:760753108 byr:1931\n",
        "hgt:179cm\n",
        "\n",
        "hcl:#cfa07d eyr:2025 pid:166559648\n",
        "iyr:2011 ecl:brn hgt:59in\n",
    ]


@pytest.fixture
def invalid_data():
    return [
        "eyr:1972 cid:100\n",
        "hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926\n",
        "\n",
        "iyr:2019\n",
        "hcl:#602927 eyr:1967 hgt:170cm\n",
        "ecl:grn pid:012533040 byr:1946\n",
        "\n",
        "hcl:dab227 iyr:2012\n",
        "ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277\n",
        "\n",
        "hgt:59cm ecl:zzz\n",
        "eyr:2038 hcl:74454a iyr:2023\n",
        "pid:3556412378 byr:2007\n",
        "\n",
    ]


@pytest.fixture
def valid_data():
    return [
        "pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980\n",
        "hcl:#623a2f\n",
        "\n",
        "eyr:2029 ecl:blu cid:129 byr:1989\n",
        "iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm\n",
        "\n",
        "hcl:#888785\n",
        "hgt:164cm byr:2001 iyr:2015 cid:88\n",
        "pid:545766238 ecl:hzl\n",
        "eyr:2022\n",
        "\n",
        (
            "iyr:2010 hgt:158cm hcl:#b6652a ecl:blu "
            + "byr:1944 eyr:2021 pid:093154719\n"
        ),
        "\n",
    ]


def test_part1(sample_data):
    assert part1(sample_data) == 2


def test_invalid_data_part2(invalid_data):
    res = part2(invalid_data)
    assert res == 0


def test_valid_data_part2(valid_data):
    res = part2(valid_data)
    assert res == 4
