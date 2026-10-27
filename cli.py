"""Command-line interface.

Input format (file or stdin), whitespace separated numbers:
    line 1: m n          (number of houses, number of candidate locations)
    line 2: m house positions (metres along the street)
    line 3: n candidate transmitter positions
"""

import argparse
import sys

from .solver import is_valid, solve


def read_instance(text):
    tokens = text.split()
    if len(tokens) < 2:
        raise ValueError("input must start with m and n")
    m, n = int(tokens[0]), int(tokens[1])
    vals = [float(t) for t in tokens[2:]]
    if len(vals) != m + n:
        raise ValueError(f"expected {m + n} positions, got {len(vals)}")
    return vals[:m], vals[m:]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file", nargs="?", help="input file (default: stdin)")
    p.add_argument("-r", "--radius", type=float, default=500.0,
                   help="coverage radius in metres (default 500)")
    args = p.parse_args(argv)

    text = open(args.file).read() if args.file else sys.stdin.read()
    houses, candidates = read_instance(text)
    sol = solve(houses, candidates, args.radius)

    if sol is None:
        print("NO SOLUTION")
        return 1
    assert is_valid(houses, candidates, sol.indices, args.radius)
    print(f"Minimum transmitters: {sol.count}")
    print("Positions: " + " ".join(f"{x:g}" for x in sol.positions))
    return 0


if __name__ == "__main__":
    sys.exit(main())
