#!/usr/bin/env python3
"""
nested_cube_checks.py
Reproduces every count used in "One Outcome from 330: A Theorem on Folding
Eleven Nested Dimensions into a 3D + 1".

Setting: the indices 1..N (N = 11 unless stated) are the weights of N nested
dimensions. A split is three groups of k indices with equal sum s (the axes of
a cube of k^3 positions) and a remainder (the fourth axis) of weight p.
  F2: s + p = k^3 + 1
  F3: one leader is taken from each of the four groups, the four leaders are
      different and add to N.
Section 8 reproduces the counts of the section "The form of the folding".
Run:  python3 nested_cube_checks.py        (standard library only)
"""
from itertools import combinations
from math import comb


def splits(N, k, p_required=None):
    """All splits of 1..N into three unordered groups of k indices with equal
    sum and a remainder. Returns a list of (remainder, (g1, g2, g3))."""
    nums = list(range(1, N + 1))
    total = N * (N + 1) // 2
    r = N - 3 * k
    out = []
    if r < 0:
        return out
    for rem in combinations(nums, r):
        p = sum(rem)
        if p_required is not None and p != p_required:
            continue
        if (total - p) % 3:
            continue
        s = (total - p) // 3
        rest = [x for x in nums if x not in rem]
        seen = set()
        for a in combinations(rest, k):
            if sum(a) != s:
                continue
            r2 = [x for x in rest if x not in a]
            for b in combinations(r2, k):
                if sum(b) != s:
                    continue
                c = tuple(x for x in r2 if x not in b)
                if sum(c) != s:
                    continue
                seen.add(frozenset([a, b, c]))
        for g in seen:
            out.append((rem, tuple(sorted(g))))
    return out


def leader_sets(groups, remainder, N):
    """All ways to pick one leader per group (3 axes + remainder) with the four
    leaders different and adding to N."""
    res = set()
    for l1 in groups[0]:
        for l2 in groups[1]:
            for l3 in groups[2]:
                for l4 in remainder:
                    L = (l1, l2, l3, l4)
                    if len(set(L)) == 4 and sum(L) == N:
                        res.add(tuple(sorted(L)))
    return res


print("=" * 70)
print("1. Choosing four of eleven")
print("=" * 70)
print("C(11,4) =", comb(11, 4))
four = [c for c in combinations(range(1, 12), 4) if sum(c) == 11]
print("four different indices from 1..11 adding to 11:", four)

print()
print("=" * 70)
print("2. Equal splits of 1..11 into three triples and a left-over pair")
print("=" * 70)
sp = splits(11, 3)
by_s = {}
for rem, g in sp:
    s = sum(g[0])
    by_s[s] = by_s.get(s, 0) + 1
print("total splits:", len(sp))
print("  s   p   s+p   splits")
for s in sorted(by_s):
    p = 66 - 3 * s
    print(f"  {s}  {p:2d}   {s + p}    {by_s[s]}")

print()
print("=" * 70)
print("3. F2 (s + p = 28) keeps s = 19; the six splits; F3 on the leaders")
print("=" * 70)
six = [(rem, g) for rem, g in sp if sum(g[0]) == 19]
print("splits with s = 19, p = 9:", len(six))
keep = 0
centre = 0
for rem, g in sorted(six):
    L = leader_sets(g, rem, 11)
    flag = "leaders " + str(sorted(L)) if L else "no leaders adding to 11"
    print("  left-over", set(rem), "groups", [set(x) for x in g], "->", flag)
    if L:
        keep += 1
        if 6 in rem:
            centre += 1
print("splits keeping a leader set that adds to 11:", keep)
print("of these, left-over contains the centre index 6:", centre)

print()
print("=" * 70)
print("4. The three cubes in 11 nested dimensions")
print("=" * 70)
print("k  cube  equal splits  splits meeting F2 (s+p=k^3+1)")
for k in (1, 2, 3):
    sk = splits(11, k)
    ok = [1 for rem, g in sk if sum(g[0]) + sum(rem) == k ** 3 + 1]
    print(f"{k}  {k ** 3:3d}   {len(sk):6d}        {len(ok)}")

print()
print("=" * 70)
print("5. Depth: for which N does a cube of k^3 meet F2 (remainder may have")
print("   any number of indices)?  counts of splits")
print("=" * 70)
for k in (1, 2, 3, 4):
    row = []
    for N in range(3 * k, 19):
        T = N * (N + 1) // 2
        two_s = T - k ** 3 - 1
        if two_s % 2:
            row.append((N, 0))
            continue
        s = two_s // 2
        p = k ** 3 + 1 - s
        if p < 0:
            row.append((N, 0))
            continue
        if k == 4 and N > 17:
            continue
        row.append((N, len([1 for rem, g in splits(N, k, p_required=p)])))
    nonzero = [(N, c) for N, c in row if c]
    print(f"k={k} (cube {k ** 3}): depths with a solution:", nonzero if nonzero else "none up to N=18")

print()
print("6. Cube of 27 formula check: p = 42 - N(N+1)/4")
for N in range(9, 15):
    print(f"  N={N}: p = {42 - N * (N + 1) / 4}")

print()
print("=" * 70)
print("7. Alternative F2': the fourth axis weighs one face, p = k^2 = 9")
print("=" * 70)
for N in range(9, 17):
    print(f"  depth {N}: {len(splits(N, 3, p_required=9))} splits")

print()
print("=" * 70)
print("8. The form of the folding")
print("=" * 70)

# 8a. 1, 2, 3: sum and product
print("1 + 2 + 3 =", 1 + 2 + 3, "  1 x 2 x 3 =", 1 * 2 * 3)
# different positive whole numbers a < b < c with a + b + c = a b c:
# c (ab - 1) = a + b, so c = (a + b) / (ab - 1)
sol = []
for a in range(1, 2001):
    for b in range(a + 1, 2001):
        if a * b - 1 > 0 and (a + b) % (a * b - 1) == 0:
            c = (a + b) // (a * b - 1)
            if c > b:
                sol.append((a, b, c))
print("triples of different positive whole numbers with sum = product (up to 2000):", sol)

# 8b. the leaders of the three axes in each split that keeps the leaders at 11
print()
print("leaders of the three axes, leader of the fourth axis, sum of the three, in each split")
print("that keeps the leaders at 11 (leader sets as in section 3):")
rows = []
for rem, g in sorted(six):
    opts = set()
    for l1 in g[0]:
        for l2 in g[1]:
            for l3 in g[2]:
                for l4 in rem:
                    L = (l1, l2, l3, l4)
                    if len(set(L)) == 4 and sum(L) == 11:
                        opts.add((tuple(sorted((l1, l2, l3))), l4))
    for axes, l4 in sorted(opts):
        rows.append((rem, axes, l4, sum(axes)))
        cube = round(sum(axes) ** (1 / 3)) ** 3 == sum(axes)
        print("  left-over", set(rem), " axes led by", axes, " fourth axis led by", l4,
              " sum of the three =", sum(axes), "(a cube)" if cube else "")
print("sums of the three axis leaders:", sorted(r[3] for r in rows))
print("splits whose left-over contains the centre index 6:",
      [(sorted(r[0]), r[1], r[2], r[3]) for r in rows if 6 in r[0]])
print("1 + 2 + 5 =", 1 + 2 + 5, "= 2^3 =", 2 ** 3, "  1 x 2 x 5 =", 1 * 2 * 5)

# 8c. the volume by cubing a cube
print()
print("level  side  volume   power of 2")
for lvl, side in enumerate((2, 4, 8), start=1):
    v = side ** 3
    e = 3 * lvl
    assert v == 2 ** e
    print(f"  {lvl}     {side}    {side}^3 = {v}   2^{e}")
print("8^3 =", 8 ** 3, "= 2^9 =", 2 ** 9, "= 8 x 64 =", 8 * 64, "= 2 x 4^4 =", 2 * 4 ** 4)
print("2^3 x 2^6 =", 2 ** 3 * 2 ** 6, "= 2^9, and 3 + 6 =", 3 + 6)
print("three levels x three axes =", 3 * 3, "binary dimensions; a fourth level 2^12 =", 2 ** 12,
      "needs", 3 * 4, "binary dimensions")
