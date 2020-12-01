import sys
from pathlib import Path
from time import time


def bench(func):
    def go(*args, **kwargs):
        start = time()
        return (func(*args, **kwargs), time() - start)

    return go


def show(answer, time_taken):
    if time_taken < 0.01:
        return f"{answer:10}\t({time_taken:.2E}s)"
    return f"{answer:10}\t({time_taken:.2}s)"


def run(day):
    def go(part):
        print(
            f"Part {part}: ",
            show(
                *bench(eval(f'__import__(f"day{day}").part{part}'))(
                    (
                        Path(__file__).parent.absolute()
                        / f"day{day}"
                        / "input"
                    ).open()
                ),
            ),
        )

    go(1)
    go(2)


def main(args):
    day = "0" + args[1] if len(args[1]) == 1 else args[1]
    print(f"{' '*27}Day {day}{' '*27}")
    print("=" * 60)
    try:
        run(day)
    except (ImportError, NotImplementedError, AttributeError) as e:
        print(e)


if __name__ == "__main__":
    main(sys.argv)
