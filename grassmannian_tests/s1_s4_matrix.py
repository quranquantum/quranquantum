"""The model's own 4 x 11 matrix: rows S1 (62 grey), S2 (99 white), S3 (216), S4 (99 blue); columns D1..D11; entry = sum of the values in that D-group. All 330 Plucker minors."""
import sys, runpy, io, itertools, contextlib, collections
import os
# usage: python3 -I s1_s4_matrix.py datasets   (needs gr4_11_check.py in the same folder)
DATA=sys.argv[1]; sys.argv=['x',DATA]
with contextlib.redirect_stdout(io.StringIO()):
    g=runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)),'gr4_11_check.py'))
dg=g['dgroup']; det=g['det']
def row(layer):
    r=[0]*11
    for (line,col),v in layer.items(): r[dg(line)]+=v
    return r
rows={'S1 grey62':row(g['grey']),'S2 white':row(g['white']),'S3 216':row(g['black']),'S4 blue':row(g['blue'])}
for k,v in rows.items(): print(k,v,'sum',sum(v))
M=list(rows.values())
mins={T:det([[r[j] for j in T] for r in M]) for T in itertools.combinations(range(11),4)}
nz={T:v for T,v in mins.items() if v}
print('nonzero',len(nz),'pos',sum(v>0 for v in nz.values()),'neg',sum(v<0 for v in nz.values()))
print('without col D7 all zero:',all(mins[T]==0 for T in mins if 6 not in T))
print('nonzero with D7:',len(nz),'of',len([T for T in mins if 6 in T]))
# sub-tests: which columns (D) are used by which rows
for k,v in rows.items(): print(k,'columns used (D index 1-11):',[i+1 for i,x in enumerate(v) if x])
