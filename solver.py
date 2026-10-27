"""Exact-cover transmitter placement on a line.

Problem
-------
Houses lie at positions on a street, and transmitters may be built only at
a given set of candidate positions.  A transmitter at position c "reaches"
every house h with |h - c| <= radius (radius = 500 m in the problem).
We need a set of transmitters such that EVERY house is reached by EXACTLY ONE
chosen transmitter, using as few transmitters as possible.

Key observation
---------------
Sort the houses.  The houses reached by a candidate form a *contiguous block*
of the sorted order, i.e. a half-open index interval [l, r).  So the
problem becomes: choose intervals that partition {0, ..., m-1} exactly
(no gaps, no overlaps), minimising the number of intervals.

Dynamic programme
-----------------
dp[i] = minimum number of transmitters whose intervals partition exactly the
first i houses (dp[0] = 0, dp[i] = INF if impossible).
An interval [l, r) gives the transition dp[r] <- dp[l] + 1.
Processing intervals in increasing order of r guarantees dp[l] (l < r) is
final when it is used.  The answer is dp[m]; INF means no solution exists.

Complexity: O(m log m + n log n + n log m) time, O(m + n) space.
"""

from bisect import bisect_left, bisect_right
from typing import List, NamedTuple, Optional, Sequence

INF = float("inf")


class Solution(NamedTuple):
    count: int                 # number of transmitters built
    indices: List[int]         # indices into the ORIGINAL candidates list
    positions: List[float]     # their positions, in increasing order


def solve(
    houses: Sequence[float],
    candidates: Sequence[float],
    radius: float = 500,
) -> Optional[Solution]:
    """Return an optimal Solution, or None if no exact placement exists."""
    hs = sorted(houses)
    m = len(hs)
    if m == 0:
        return Solution(0, [], [])

    # Build the interval [l, r) of houses reached by each candidate.
    intervals = []  # (r, l, candidate_index)
    for j, c in enumerate(candidates):
        l = bisect_left(hs, c - radius)
        r = bisect_right(hs, c + radius)
        if l < r:  # candidates reaching no house are never useful
            intervals.append((r, l, j))
    intervals.sort()

    dp = [INF] * (m + 1)
    parent = [None] * (m + 1)  # parent[r] = (l, candidate_index)
    dp[0] = 0
    for r, l, j in intervals:
        if dp[l] + 1 < dp[r]:
            dp[r] = dp[l] + 1
            parent[r] = (l, j)

    if dp[m] == INF:
        return None

    chosen = []
    i = m
    while i > 0:
        l, j = parent[i]
        chosen.append(j)
        i = l
    chosen.sort(key=lambda j: candidates[j])
    return Solution(int(dp[m]), chosen, [candidates[j] for j in chosen])


def is_valid(
    houses: Sequence[float],
    candidates: Sequence[float],
    indices: Sequence[int],
    radius: float = 500,
) -> bool:
    """Check that every house is reached by exactly one chosen transmitter."""
    for h in houses:
        if sum(1 for j in indices if abs(h - candidates[j]) <= radius) != 1:
            return False
    return True
