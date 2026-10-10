#!/usr/bin/env python3
"""Regenerate the 62 grey cells from the 99 + 15 name values and compare with the table.

Rule (the author's): a name sits on the cell whose number equals its value. The 114 names are the
99 static values plus the 15 rising names at their dynamic values. Names with the same value share a
cell, so that cell is multi-use and its net value is the sum of the names on it.
Usage: python3 -I regenerate_62.py datasets   (needs gr4_11_check.py in the same folder)
"""
import sys, os, io, runpy, contextlib, collections
DATA = sys.argv[1]; sys.argv = ['x', DATA]
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gr4_11_check.py'))
table = {g['cell'](l, c): v for (l, c), v in g['grey'].items()}          # the 62 table as given
vals = list(g['static'].values()) + [g['dynamic'][k] for k in g['rising']]  # 99 static + 15 dynamic = 114
gen = collections.Counter()
for v in vals: gen[v] += v                                               # name at cell = its value; net = sum
print("names:", len(vals), " sum:", sum(vals))
print("regenerated cells:", len(gen), " table cells:", len(table))
print("IDENTICAL (cell numbers and net values):", dict(gen) == table)
print("single-name cells:", sum(1 for v, s in gen.items() if s == v), " multi-name cells:", sum(1 for v, s in gen.items() if s != v))
