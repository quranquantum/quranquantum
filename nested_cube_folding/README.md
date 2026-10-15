# One Outcome from 330: A Theorem on Folding Eleven Nested Dimensions into a 3D + 1

Supporting calculation for the paper by Ahmed Macky.

Paper: https://doi.org/10.5281/zenodo.23387817

## What is here

- `nested_cube_checks.py` : a short Python script (standard library only) that reproduces every count used in the paper. It runs in under a second.
- `nested_cube_checks_output.txt` : the full output of the script, as printed in the paper.

## What the script reproduces

- C(11, 4) = 330, and the only four different indices from 1 to 11 adding to 11: (1, 2, 3, 5).
- The 32 equal splits of the indices 1 to 11 into three triples and a left-over pair, by triple sum s.
- The six splits with s = 19 and left-over weight 9, the four of them whose leaders add to 11, and the one whose left-over contains the centre index 6.
- The cubes of 1, 8 and 27 in eleven dimensions: equal splits, and splits meeting s + p = k^3 + 1.
- The depths at which the cubes of 27 and 64 meet the same condition.
- The alternative in which the fourth axis weighs one face of the cube, p = k^2.

## How to run

    python3 nested_cube_checks.py

No packages are needed.

## How to cite

Macky, A. One Outcome from 330: A Theorem on Folding Eleven Nested Dimensions into a 3D + 1. Zenodo. https://doi.org/10.5281/zenodo.23387817
