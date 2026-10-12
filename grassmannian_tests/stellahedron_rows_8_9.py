#!/usr/bin/env python3
"""Stellahedron face counts by direct enumeration of tubings of the star graph,
dimensions 2..9, then the h-vector by the inverse Pascal transform.
Rule: sum_k f_k x^k = sum_i h_i (x+1)^i.   Needs Python 3 only, no data files.
Prints, for each dimension d: f-vector, h-vector, position n of the 2-face in the
triangle read row by row (row d has d+1 entries; rows start at d=1), and a check
that the vertex count equals sum_k d!/k!.   Run time: a few minutes up to d=9."""
from math import comb, factorial
import sys

def fvec(n):
    tubes = [('c', m) for m in range(1 << n) if m != (1 << n) - 1] + [('l', a) for a in range(n)]
    def comp(x, y):
        if x == y: return False
        (tx, vx), (ty, vy) = x, y
        if tx == 'c' and ty == 'c': return (vx & vy) == vx or (vx & vy) == vy
        if tx == 'l' and ty == 'l': return True
        if tx == 'l': (tx, vx), (ty, vy) = y, x
        return (vx >> vy) & 1 == 1
    N = len(tubes)
    adj = [[comp(tubes[i], tubes[j]) for j in range(N)] for i in range(N)]
    cnt = [0] * (n + 1)
    def rec(c, s):
        cnt[s] += 1
        for k, i in enumerate(c):
            rec([j for j in c[k + 1:] if adj[i][j]], s + 1)
    rec(list(range(N)), 0)
    return [cnt[n - i] for i in range(n + 1)]

def h_from_f(f):
    h = [0] * len(f)
    for k, fk in enumerate(f):
        for j in range(k + 1):
            h[j] += fk * comb(k, j) * (-1) ** (k - j)
    return h

top = int(sys.argv[1]) if len(sys.argv) > 1 else 9
for d in range(2, top + 1):
    f = fvec(d); h = h_from_f(f)
    n2 = (d - 1) * (d + 2) // 2 + 3
    assert h == h[::-1]
    assert f[0] == sum(factorial(d) // factorial(k) for k in range(d + 1))
    print(f"d={d}  f={f}\n      h={h}\n      2-face = {f[2]} at position n={n2}", flush=True)
