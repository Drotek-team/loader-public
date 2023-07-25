from typing import Dict, List, Set

from typing_extensions import TypeAlias

Explanations: TypeAlias = "Dict[str, Explanations | str]"


def print_range(start: int, end: int) -> str:
    if start == end:
        return f"{start}"
    return f"{start}-{end}"


def get_ranges_from_drone_indices(drone_indices: Set[int]) -> str:
    """Return a string with the ranges of drone indices.

    [0,2,3,4,7,8,12,13] -> "0,2-4,7-8,12-13"
    """
    if len(drone_indices) == 0:
        return ""

    indices = sorted(drone_indices)
    ranges: List[str] = []
    start = indices[0]
    end = indices[0]
    for index in indices[1:]:
        if index == end + 1:
            end = index
        else:
            ranges.append(print_range(start, end))
            start = index
            end = index
    ranges.append(print_range(start, end))
    return ",".join(ranges)


def get_drone_indices_from_ranges(ranges: str) -> Set[int]:
    """Return a list of drone indices from a string with ranges.

    "0,2-4,7-8,12-13" -> [0,2,3,4,7,8,12,13]
    """
    if not ranges:
        return set()
    drone_indices: Set[int] = set()
    for range_ in ranges.split(","):
        if "-" in range_:
            start, end = range_.split("-")
            drone_indices.update(range(int(start), int(end) + 1))
        else:
            drone_indices.add(int(range_))
    return drone_indices
