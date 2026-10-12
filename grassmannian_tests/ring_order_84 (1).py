#!/usr/bin/env python3
"""Order of the 84 core names around the 114 ring (positions 16-99): by value (grey cell number) ascending,
within a cell L > N > Y, then list position (author's rule, confirmed 12 Oct 2026). The order read from
'Original Names Table.xlsx' is compared and any difference is printed.  Risers are skipped.
Prints position, list id, cell, value, name, and the partner under rho(i) = 115 - i.
Usage: python3 -I ring_order_84.py datasets      Needs: openpyxl"""
import csv, re, sys, os, openpyxl
DATA = sys.argv[1] if len(sys.argv) > 1 else "datasets"
def norm(s):
    s = re.sub(r'[^ء-ي]', '', s)
    for a, b in (('ى','ي'),('أ','ا'),('إ','ا'),('آ','ا'),('ة','ه'),('ؤ','و'),('ئ','ي'),('ٱ','ا')): s = s.replace(a, b)
    return s
def num(s):
    s = s.strip().replace(',', '')
    return int(s) if s.isdigit() else None
rows = list(csv.reader(open(os.path.join(DATA, "Strings Full List-47L-31N-21Y(Sheet1).csv"), encoding='utf-8-sig')))
names = {}
for r in rows:
    k = num(r[0]) if r else None
    if k is None: continue
    if k <= 47 and r[1].strip() and num(r[2]) is not None: names[('L', k)] = (r[1].strip(), num(r[2]))
    if k <= 31 and len(r) > 11 and r[10].strip() and num(r[11]) is not None: names[('N', k)] = (r[10].strip(), num(r[11]))
    if k <= 21 and len(r) > 19 and r[18].strip() and num(r[19]) is not None: names[('Y', k)] = (r[18].strip(), num(r[19]))
rising = {("Y",14):84,("L",38):86,("L",45):88,("N",1):92,("N",2):94,("Y",20):95,("L",21):96,("L",29):96,
          ("N",28):104,("L",26):108,("L",5):110,("L",13):123,("L",18):211,("L",6):271,("L",14):297}
byname = {}
for k, (n, v) in names.items(): byname.setdefault(norm(n), []).append(k)
ws = openpyxl.load_workbook(os.path.join(DATA, "Original Names Table.xlsx"), data_only=True).active
seq = []
for r in range(2, 31):
    for c in range(7, 16):
        v = ws.cell(r, c).value
        if not v or str(v).strip().isdigit(): continue
        cellno = 37 + 9 * (r - 2) + (c - 7)
        for nm, val, mk in re.findall(r'([^\d#Ʉ]+?)\s*(\d+)\s*([#Ʉ]?)', str(v).replace('Ỗ', '')):
            if mk: continue
            nm = norm(nm.strip(' -')); val = int(val)
            ks = [k for k in byname.get(nm, []) if names[k][1] == val and k not in rising]
            if len(ks) != 1:   # spelling differs between table and list: match by value among names not yet used
                ks = [k for k in names if names[k][1] == val and k not in rising and k not in [s[1] for s in seq]]
                print("matched by value (spelling differs):", cellno, nm, val, ks)
            seq.append((cellno, ks[0], val))
assert len(seq) == 84 and len({s[1] for s in seq}) == 84
core = [k for k in names if k not in rising]
rule = sorted(core, key=lambda k: (names[k][1], "LNY".index(k[0]), k[1]))
tab_ids = [s_[1] for s_ in seq]
print("differences between the names-workbook order and the rule order:",
      [(16 + i, a, b) for i, (a, b) in enumerate(zip(tab_ids, rule)) if a != b] or "none")
seq = [(names[k][1], k, names[k][1]) for k in rule]
pos = {16 + i: s_ for i, s_ in enumerate(seq)}
print("pos  id    cell value name | partner pos id value name")
for p in range(16, 100):
    cn, k, val = pos[p]; q = 115 - p; cn2, k2, val2 = pos[q]
    print(p, k, cn, val, names[k][0], "|", q, k2, val2, names[k2][0])
