from enum import Enum, unique, auto
from typing import List


@unique
class Axis(Enum):
    X = auto()
    Y = auto()

    def __str__(self) -> str:
        return self.name


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        return (self.x == other.x) and (self.y == other.y)

    def manhattan_distance(self, other) -> int:
        return abs(other.y - self.y) + abs(other.x - self.x)

    def to(self, other):
        if self.x == other.x:
            return Movement(
                self,
                f"{'U' if self.y <= other.y else 'D'}{abs(other.y-self.y)}")
        else:
            return Movement(
                self,
                f"{'R' if self.x <= other.x else 'L'}{abs(other.x-self.x)}")


class Movement:
    def __init__(self, start: Point, action: str) -> None:
        direction: str = action[0]
        self.start: Point = start
        if direction == 'R' or direction == 'U':
            self.magnitude = int(action[1:])
        elif direction == 'L' or direction == 'D':
            self.magnitude = -(int(action[1:]))

        if direction == 'L' or direction == 'R':
            self.direction: Axis = Axis.X
        elif direction == 'U' or direction == 'D':
            self.direction: Axis = Axis.Y
        self.points: List[Point] = self.points_visited()
        self.stop: Point = self.points[-1]

    def __repr__(self) -> str:
        return f"[{self.start} --{self.direction.name}-> {self.stop}]"

    def overlaps(self, other) -> List[Point]:
        if self.direction == other.direction:
            if self.direction == Axis.X:
                return [
                    Point(x, self.start.y)
                    for x in set(self.range()).intersection(other.range())
                ] if self.start.y == other.start.y else []
            else:  # if self.direction == Axis.Y:
                return [
                    Point(self.start.x, y)
                    for y in set(self.range()).intersection(other.range())
                ] if self.start.x == other.start.x else []
        elif self.direction == Axis.X:  # and other.direction == Axis.Y:
            if self.start.y in other.range() and other.start.x in self.range():
                return [Point(other.start.x, self.start.y)]
            else:
                return []
        else:  # if self.direction == Axis.Y and other.direction == Axis.X:
            if other.start.y in self.range() and self.start.x in other.range():
                return [Point(self.start.x, other.start.y)]
            else:
                return []

    def points_visited(self) -> List[Point]:
        points = []
        if self.direction == Axis.X:
            end = self.start.x + self.magnitude
            end += 1 if self.magnitude >= 0 else -1
            step = -1 if self.magnitude < 0 else 1
            for x in range(self.start.x, end, step):
                points.append(Point(x, self.start.y))
        else:
            end = self.start.y + self.magnitude
            end += 1 if self.magnitude >= 0 else -1
            step = -1 if self.magnitude < 0 else 1
            for y in range(self.start.y, end, step):
                points.append(Point(self.start.x, y))
        return points

    def range(self) -> range:
        first, last = self.points[0], self.points[-1]
        return range(
            first.x if self.direction == Axis.X else first.y,
            last.x if self.direction == Axis.X else last.y,
            1 if self.magnitude >= 0 else -1)


class Wire:
    def __init__(self, movements: List[str]) -> None:
        self.movements: List[Movement] = []
        old_end: Point = Point(0, 0)
        for movement in movements:
            self.movements.append(Movement(old_end, movement))
            old_end = self.movements[-1].stop

    def __repr__(self) -> str:
        return "[" + ", ".join([x.__repr__() for x in self.movements]) + "]"

    def intersections_with(self, other):
        intersections = []
        steps: List[int] = [0, 0]

        for x in self.movements:
            steps[0] += abs(x.magnitude)
            steps[1] = 0
            for y in other.movements:
                steps[1] += abs(y.magnitude)
                if x.overlaps(y) and (not (x.overlaps(y)[0] == Point(0, 0))):
                    tmp = steps[0]
                    steps[0] -= abs(x.magnitude)
                    steps[0] += abs(x.start.to(x.overlaps(y)[0]).magnitude)
                    steps[1] -= abs(y.magnitude)
                    steps[1] += abs(y.start.to(x.overlaps(y)[0]).magnitude)
                    intersections.append((x.overlaps(y)[0], sum(steps)))
                    steps[0], steps[1] = tmp, 0
        return intersections


def main() -> None:
    with open("input.txt", "r") as f:
        wires: List[Wire] = [Wire(line.strip().split(','))
                             for line in f.readlines()]
    ints: List[Point] = wires[0].intersections_with(wires[1])
    distances: List[int] = [
        Point(0, 0).manhattan_distance(x[0])
        for x in ints
    ]

    # print(ints, distances, sep='\n')
    print(f"Closest intersection:", end=" ")
    print(ints[distances.index(min(distances))][0])
    print(f"Manhattan distance: {min(distances)}")

    print(f"\nFewest steps intersection:", end=" ")
    print(min(ints, key=lambda x: x[1])[0])
    print(f"Steps:", end=" ")
    print(min(ints, key=lambda x: x[1])[1])


if __name__ == '__main__':
    main()
