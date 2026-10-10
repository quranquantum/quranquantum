"""Layout or values? Every cell value is replaced by 1 (cells stay where they are) and the classification is repeated."""
import sys, runpy, io, itertools, contextlib, collections
import os
# usage: python3 -I layout_vs_values.py datasets   (needs gr4_11_check.py in the same folder)
DATA=sys.argv[1]; sys.argv=['x',DATA]
with contextlib.redirect_stdout(io.StringIO()):
    g=runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)),'gr4_11_check.py'))
one=lambda L:{k:1 for k in L}
cl=g['classify']; mat=g['matrix']
print('62 real   ',cl(mat(g['grey'])))
print('62 ones   ',cl(mat(one(g['grey']))))
print('62+216 real',cl(mat(g['grey'],g['black'])))
print('62+216 ones',cl(mat(one(g['grey']),one(g['black']))))
print('blue real ',cl(mat(g['blue'])))
print('blue ones ',cl(mat(one(g['blue']))))
# which 62 choices are one-signed in real vs ones
def onesigned(M):
    s=set()
    for S in itertools.combinations(range(9),4):
        nz=[v for T in itertools.combinations(range(11),4) if (v:=g['det']([[M[i][j] for j in T] for i in S]))]
        if nz and (all(v>0 for v in nz) or all(v<0 for v in nz)): s.add(S)
    return s
a=onesigned(mat(g['grey'])); b=onesigned(mat(one(g['grey'])))
print('62: same set of one-signed choices real vs ones:',a==b,len(a),len(b))
# S1-S4 matrix with ones
def s14(ls):
    rows=[]
    for L in ls:
        r=[0]*11
        for (l,c),v in L.items(): r[g['dgroup'](l)]+=v
        rows.append(r)
    nz=[v for T in itertools.combinations(range(11),4) if (v:=g['det']([[r[j] for j in T] for r in rows]))]
    return len(nz),sum(v>0 for v in nz),sum(v<0 for v in nz)
print('S1-S4 real',s14([g['grey'],g['white'],g['black'],g['blue']]))
print('S1-S4 ones',s14([one(g['grey']),one(g['white']),one(g['black']),one(g['blue'])]))
