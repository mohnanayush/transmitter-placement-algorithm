# Transmitter Placement (exact coverage)

Implementation for Question 8 of the *Design and Analysis of Algorithms* project.

**Problem.** `m` houses lie on a street; transmitters may be built at `n`
candidate locations. Every house must have **exactly one** transmitter within
500 m. Find a placement using the minimum number of transmitters, or report
that none exists.

## Idea

After sorting the houses, the set of houses a candidate reaches is a contiguous
block of indices `[l, r)`. The task becomes choosing blocks that partition
`0..m-1` exactly (no gaps, no overlaps) with as few blocks as possible.

`dp[i]` = fewest transmitters that exactly cover the first `i` houses.
Processing blocks in increasing order of `r`, each block gives
`dp[r] = min(dp[r], dp[l] + 1)`. The answer is `dp[m]`; infinity means no
solution. Parent pointers recover the chosen transmitters.

Time: `O(m log m + n log n + n log m)`. Space: `O(m + n)`.

## Requirements

Python 3.8+, standard library only.

## Run

From the repository root:

```bash
python -m transmitter_placement examples/solvable.txt
python -m transmitter_placement examples/no_solution.txt
cat examples/solvable.txt | python -m transmitter_placement      # stdin
python -m transmitter_placement examples/solvable.txt -r 500     # custom radius
```

Input format (whitespace separated):

```
m n
<m house positions>
<n candidate positions>
```

Output is either `Minimum transmitters: k` plus the positions, or
`NO SOLUTION` (exit code 1).

## Use as a library

```python
from transmitter_placement import solve
sol = solve(houses=[0, 300, 700, 1100], candidates=[200, 450, 900, 1000, 5000])
print(sol)   # Solution(count, indices, positions) or None
```

## Tests

```bash
python -m unittest discover -s tests -v
```

Includes hand-made cases (including the no-solution example from the report)
and 1500 random instances checked against an exhaustive brute force.

## Report

The LaTeX source of the project report is in `report/report.tex`
(a compiled `report/report.pdf` is included). To rebuild it:

```bash
cd report && pdflatex report.tex && pdflatex report.tex
```

Before submitting, edit the author line and the GitHub link in `report.tex`.

## Layout

```
transmitter_placement/   solver.py (algorithm), cli.py, __main__.py
tests/                   test_solver.py
examples/                solvable.txt, no_solution.txt
report/                  report.tex, report.pdf
```
