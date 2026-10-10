"""Null test with the model's own placement rule (a name sits on the cell equal to its value): other sets of 114 values -> 62-type table -> count Gr>=0. (a) uniform random values in 44..297; (b) resampling the model's own 114 values with replacement. Fixed seed."""
import sys, runpy, io, contextlib, collections, random
import os
# usage: python3 -I null_values.py datasets   (needs gr4_11_check.py in the same folder; ~5 min)
DATA=sys.argv[1]; sys.argv=['x',DATA]
with contextlib.redirect_stdout(io.StringIO()):
    g=runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)),'gr4_11_check.py'))
cl=g['classify']; c2l=g['cell_to_lc']; mat=g['matrix']
real=list(g['static'].values())+[g['dynamic'][k] for k in g['rising']]
def grey_from(vals):
    gen=collections.Counter()
    for v in vals: gen[v]+=v
    return {c2l(n):s for n,s in gen.items()}
def run(vals):
    r=cl(mat(grey_from(vals))); return r['rank4'],r['Gr>=0']
print('real',run(real))
random.seed(1)
lo,hi=min(real),max(real)
res=[]
for t in range(150):
    v=[random.randint(lo,hi) for _ in real]; res.append(run(v))
print('uniform random in',lo,hi,': trials',len(res))
print(' rank4 mean %.1f ; Gr>=0 mean %.1f'%(sum(a for a,b in res)/len(res),sum(b for a,b in res)/len(res)))
print(' fraction Gr>=0 among rank-4: %.2f'%(sum(b for a,b in res)/max(1,sum(a for a,b in res))))
print(' trials with >=39 Gr>=0:',sum(1 for a,b in res if b>=39),'; with rank4>=42:',sum(1 for a,b in res if a>=42))
# also resample the real values with replacement (keeps the model's own value distribution)
res2=[]
for t in range(150):
    v=[random.choice(real) for _ in real]; res2.append(run(v))
print('resample of the real values: rank4 mean %.1f ; Gr>=0 mean %.1f ; fraction %.2f'%(sum(a for a,b in res2)/len(res2),sum(b for a,b in res2)/len(res2),sum(b for a,b in res2)/max(1,sum(a for a,b in res2))))
