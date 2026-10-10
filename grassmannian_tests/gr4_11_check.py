#!/usr/bin/env python3
"""
Reproducible check of the Gr(4,11) results for the 62 / 99 / 216 grid.

Reads the open datasets from https://github.com/quranquantum/quranquantum
(folder 'datasets'): 62-261_table.csv, Strings Full List-47L-31N-21Y(Sheet1).csv,
The Mathani Dual-Anchor Vector Matrix (15)(Sheet1).csv

Usage:   python3 gr4_11_check.py [path/to/datasets]
Needs:   Python 3 only (no extra packages). Exact integer arithmetic.

Layout used (stated so a reader can challenge it):
  * grid: 29 lines x 9 columns; cell number = 36 + 9*(line-1) + column, cells 37..297
  * D-groups (columns of the 4x11 matrix, natural order D1..D11):
      D1 1-11, D2 12-14, D3 15, D4 16, D5 17-18, D6 19, D7 20-21,
      D8 22-26, D9 27, D10 28, D11 29        (odd D = in between, even D = dynamic)
  * 9x11 matrix: row = grid column (1..9), entry = sum of the values in that
    grid column and D-group.  A test picks 4 of the 9 rows (126 choices) and
    computes all C(11,4)=330 minors.
  * 62 = grey cells read from 62-261_table.csv.
  * 216 = one cell at line 20, column 9.
  * 99 dy (blue): dynamic value = static value, +40 / +80 for the 15 rising names;
      sorted by dynamic value, ties L>N>Y then list position; placed in the 99
      cells of the even lines, ascending from cell 136.
  * 99 st (white): L36..L1, Y21..Y1, N31..N1, L47..L37 placed into the empty
      odd-line cells (not grey, not 216), descending from cell 296.
"""
import csv, itertools, sys, os

DATA = sys.argv[1] if len(sys.argv) > 1 else "datasets"
def path(name): return os.path.join(DATA, name)
def rd(name): return list(csv.reader(open(path(name), encoding="utf-8-sig")))

D = [(1,11),(12,14),(15,15),(16,16),(17,18),(19,19),(20,21),(22,26),(27,27),(28,28),(29,29)]
EVEN_D = {1,3,5,7,9}                      # indices of D2,D4,D6,D8,D10
def dgroup(line):
    for j,(a,b) in enumerate(D):
        if a <= line <= b: return j
def cell(line,col): return 36 + 9*(line-1) + col
def cell_to_lc(n): n -= 37; return n//9 + 1, n%9 + 1

# ---- 62 grey ----
grey = {}
for r in rd("62-261_table.csv"):
    if len(r) > 12 and r[12].strip().isdigit() and int(r[12]) <= 29:
        line = int(r[12])
        for i, col in enumerate(range(9, 0, -1)):
            v = r[3+i].strip()
            if v.isdigit(): grey[(line,col)] = int(v)
assert len(grey) == 62 and sum(grey.values()) == 9795, "grey table check failed"

# ---- the 99 names: static values ----
S = rd("Strings Full List-47L-31N-21Y(Sheet1).csv")
static = {}
for r in S:
    if r[0].strip().isdigit():
        k = int(r[0])
        if r[2].strip().isdigit(): static[("L",k)] = int(r[2])
        if k <= 31 and len(r) > 11 and r[11].strip().isdigit(): static[("N",k)] = int(r[11])
        if k <= 21 and len(r) > 19 and r[19].strip().isdigit(): static[("Y",k)] = int(r[19])
assert sum(static.values()) == 7840 and len(static) == 99, "99 static check failed"

# ---- 15 rising names (list id -> dynamic value), from the Mathani sheet ----
rising = {("Y",14):84,("L",38):86,("L",45):88,("N",1):92,("N",2):94,("Y",20):95,
          ("L",21):96,("L",29):96,("N",28):104,("L",26):108,("L",5):110,
          ("L",13):123,("L",18):211,("L",6):271,("L",14):297}
dynamic = {k:(rising.get(k,v)) for k,v in static.items()}
assert sum(dynamic.values()) == 8560, "99 dynamic check failed"

# ---- blue (dy) ----
even_cells = [cell(l,c) for l in range(1,30) if dgroup(l) in EVEN_D for c in range(1,10)]
assert len(even_cells) == 99
order = sorted(dynamic, key=lambda k:(dynamic[k], "LNY".index(k[0]), k[1]))
blue = {}
for n,k in zip(sorted(even_cells), order):
    blue[cell_to_lc(n)] = dynamic[k]

# ---- white (st) ----
grey_cells = {cell(l,c) for (l,c) in grey}
odd_cells = [cell(l,c) for l in range(1,30) if dgroup(l) not in EVEN_D for c in range(1,10)]
empty = sorted((n for n in odd_cells if n not in grey_cells and n != 216), reverse=True)
assert len(empty) == 99 and empty[0] == 296
seq = [("L",i) for i in range(36,0,-1)]+[("Y",i) for i in range(21,0,-1)] \
    + [("N",i) for i in range(31,0,-1)]+[("L",i) for i in range(47,36,-1)]
white = {cell_to_lc(n): static[k] for n,k in zip(empty, seq)}

black = {(20,9): 216}

# ---- Plucker machinery (exact) ----
def det(m):
    n = len(m)
    if n == 1: return m[0][0]
    return sum((-1)**j * m[0][j] * det([row[:j]+row[j+1:] for row in m[1:]]) for j in range(n))
def matrix(*layers):
    M = [[0]*11 for _ in range(9)]
    for L in layers:
        for (line,col),v in L.items():
            M[col-1][dgroup(line)] += v
    return M
def classify(M):
    out = {"rank4":0,"pos":0,"neg":0,"mixed":0}
    for S4 in itertools.combinations(range(9),4):
        mins = [det([[M[i][j] for j in T] for i in S4]) for T in itertools.combinations(range(11),4)]
        nz = [x for x in mins if x]
        if not nz: continue
        out["rank4"] += 1
        out["pos" if all(x>0 for x in nz) else "neg" if all(x<0 for x in nz) else "mixed"] += 1
    out["Gr>=0"] = out["pos"] + out["neg"]
    return out

print("grey 62 cells:", len(grey), " white:", len(white), " blue:", len(blue), " 216: 1")
print("total:", sum(grey.values())+sum(white.values())+sum(blue.values())+216, "(expected 26411 = 11*7^4)")
print()
tests = [("62", [grey]), ("62+216", [grey,black]), ("62+216+white", [grey,black,white]),
         ("62+216+blue", [grey,black,blue]), ("62+216+white+blue (full)", [grey,black,white,blue]),
         ("white only", [white]), ("blue only (9x11 rows)", [blue])]
for name, layers in tests:
    print(f"{name:28s}", classify(matrix(*layers)))

# ---- even-group (99 dy) test: 5 even D-groups as rows, 11 even lines as columns ----
even_lines = [l for l in range(1,30) if dgroup(l) in EVEN_D]
rowsD = [j for j in sorted(EVEN_D)]
E = [[0]*11 for _ in rowsD]
for (line,col),v in blue.items():
    E[rowsD.index(dgroup(line))][even_lines.index(line)] += v
print("\n99 dy even-line test (rows = D2,D4,D6,D8,D10; columns = the 11 even lines in order)")
for omit in range(5):
    rows_i = [i for i in range(5) if i != omit]
    mins = [det([[E[i][j] for j in T] for i in rows_i]) for T in itertools.combinations(range(11),4)]
    nz = [x for x in mins if x]
    print(f"  omit D{2*(omit+1)}: nonzero {len(nz)} of 330, all >=0: {all(x>=0 for x in mins)}, any<0: {any(x<0 for x in mins)}")
print("  (block layout: each row lives in its own consecutive block of columns, so every")
print("   nonzero minor is a product of one entry per row in increasing column order -> positive")
print("   for any positive entries. The result follows from the layout, not from the values.)")
