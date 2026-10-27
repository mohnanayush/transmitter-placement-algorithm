"""Tests: hand-made cases plus randomized comparison against brute force."""

import itertools
import random
import unittest

from transmitter_placement import is_valid, solve


def brute_force(houses, candidates, radius=500):
    """Try every subset of candidates; return the minimum valid size or None."""
    best = None
    n = len(candidates)
    for k in range(n + 1):
        for subset in itertools.combinations(range(n), k):
            if is_valid(houses, candidates, subset, radius):
                return k
    return best


class HandMadeCases(unittest.TestCase):
    def test_single_house(self):
        s = solve([0], [100])
        self.assertEqual(s.count, 1)
        self.assertEqual(s.positions, [100])

    def test_no_houses(self):
        self.assertEqual(solve([], [10, 20]).count, 0)

    def test_two_far_apart_houses(self):
        s = solve([0, 5000], [0, 5000])
        self.assertEqual(s.count, 2)

    def test_prefers_fewer_transmitters(self):
        # One transmitter at 500 reaches all three; two others would also
        # be valid but use more.
        houses = [0, 400, 800]
        cands = [400, 0, 800]
        s = solve(houses, cands)
        self.assertEqual(s.count, 1)
        self.assertEqual(s.positions, [400])

    def test_no_solution_example(self):
        # Houses at 0, 600, 1200; candidates at 300 and 900 (radius 500).
        # 300 reaches {0, 600}; 900 reaches {600, 1200}.
        # House 600 is reached by both, and each is needed for 0 / 1200,
        # so exactly-one coverage is impossible.
        self.assertIsNone(solve([0, 600, 1200], [300, 900]))

    def test_uncovered_house(self):
        self.assertIsNone(solve([0, 5000], [0]))

    def test_boundary_inclusive(self):
        s = solve([0, 1000], [500])  # both exactly 500 m away
        self.assertEqual(s.count, 1)

    def test_unsorted_input(self):
        s = solve([1200, 0, 600], [900, 300, 0])
        self.assertIsNone(solve([1200, 0, 600], [900, 300]))
        self.assertIsNotNone(s)

    def test_duplicate_positions(self):
        s = solve([0, 0, 0], [0, 0])
        self.assertEqual(s.count, 1)


class RandomVsBruteForce(unittest.TestCase):
    def test_random(self):
        rng = random.Random(12345)
        solved = unsolved = 0
        for _ in range(1500):
            m = rng.randint(0, 7)
            n = rng.randint(0, 8)
            radius = rng.choice([1, 2, 3, 500])
            span = radius * rng.randint(1, 6)
            houses = [rng.randint(0, span) for _ in range(m)]
            cands = [rng.randint(0, span) for _ in range(n)]
            expected = brute_force(houses, cands, radius)
            got = solve(houses, cands, radius)
            if expected is None:
                self.assertIsNone(got, (houses, cands, radius))
                unsolved += 1
            else:
                self.assertIsNotNone(got, (houses, cands, radius))
                self.assertEqual(got.count, expected, (houses, cands, radius))
                self.assertTrue(is_valid(houses, cands, got.indices, radius))
                solved += 1
        # make sure the random test exercised both outcomes
        self.assertGreater(solved, 50)
        self.assertGreater(unsolved, 50)


if __name__ == "__main__":
    unittest.main()
