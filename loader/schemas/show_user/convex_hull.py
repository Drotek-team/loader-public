from typing import Iterable, List, Tuple, TypeVar

TPosition = TypeVar("TPosition", Tuple[float, float], Tuple[int, int])


class AngleOutOfBoundsError(Exception):
    pass


def get_p0(positions: Iterable[TPosition]) -> TPosition:
    return min(positions, key=lambda p: (p[1], p[0]))


def calculate_angle(
    position0: TPosition,
    position: TPosition,
) -> Tuple[float, float]:
    x = position[0] - position0[0]
    y = position[1] - position0[1]
    if y > 0:
        return (-x / y, y)
    if x >= 0 and y == 0:
        return (float("-inf"), x)
    raise AngleOutOfBoundsError


def sort_positions(positions: List[TPosition]) -> List[TPosition]:
    p0 = get_p0(positions)
    return sorted(positions, key=lambda p: calculate_angle(p0, p))


def cross_product(
    p0: TPosition,
    p1: TPosition,
    p2: TPosition,
) -> float:
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0])


def calculate_convex_hull(
    positions: List[TPosition],
) -> List[TPosition]:
    sorted_positions = sort_positions(positions)
    stack: List[TPosition] = []

    for p in sorted_positions:
        while len(stack) > 1 and cross_product(stack[-1], stack[-2], p) >= 0:
            stack.pop()
        stack.append(p)
    return stack
