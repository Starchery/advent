def calculate_fuel(module):
    return (module // 3) - 2


def total_fuel(fuel):
    if calculate_fuel(fuel) <= 0:
        return 0
    else:
        return calculate_fuel(fuel) + total_fuel(calculate_fuel(fuel))


def main():
    try:
        with open("input.txt", "r") as f:
            print(sum(
                [total_fuel(int(line.strip())) for line in f.readlines()]))
    except FileNotFoundError:
        print("'input.txt' was not found")


if __name__ == '__main__':
    main()
