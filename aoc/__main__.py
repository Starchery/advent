import sys
import pathlib
import time

AOC_DIR = pathlib.Path(__file__).parent.absolute()


def bench(func):
    def go(*args, **kwargs):
        start = time.time()
        return (func(*args, **kwargs), time.time() - start)

    return go


def show(answer, time_taken):
    Δt = f"{time_taken:.2E}" if time_taken < 0.01 else f"{time_taken:.2}"
    return f"{answer:10}\t({Δt}s)"


def run(day):
    infile = AOC_DIR / f"day{day}" / "input"

    def go(part):
        solve = eval(f'__import__(f"day{day}").part{part}')
        solution = show(*bench(solve)(infile.open()))
        print(f"Part {part}: {solution}")

    for n in (1, 2):
        go(part=n)


def main(args):
    try:
        day = "0" + args[1] if len(args[1]) == 1 else args[1]
    except IndexError:
        all_days = (day.name for day in AOC_DIR.iterdir() if "day" in day.name)
        most_recent_day = sorted(all_days, reverse=True)[0]
        day = most_recent_day[-2:]

    print(f"{' '*27}Day {day}{' '*27}")
    print("=" * 60)
    try:
        run(day)
    except (ImportError, NotImplementedError, AttributeError) as e:
        print(e)


if __name__ == "__main__":
    main(sys.argv)
