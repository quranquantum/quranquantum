"""Cell dimension (positroid cell, Postnikov / Knutson-Lam-Speyer) of every one-signed (Gr>=0) point found by gr4_11_check.py.
Full Gr(4,11) has dimension 28. Exact integer arithmetic, no extra packages."""
import sys, runpy, io, itertools, contextlib, collections
import os
# usage: python3 -I positroid.py datasets   (run from the repository root; needs gr4_11_check.py in the same folder)
SCRIPT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'gr4_11_check.py')
DATA=sys.argv[1]
sys.argv=['x',DATA]
with contextlib.redirect_stdout(io.StringIO()):
    g=runpy.run_path(SCRIPT)
det=g['det']; matrix=g['matrix']
n,k=11,4
def minors(rows):
    return {T:det([[r[j] for j in T] for r in rows]) for T in itertools.combinations(range(n),k)}
def cdim(bases):
    # Grassmann necklace -> bounded affine permutation -> dimension
    def key(B,i): return tuple(sorted(((b-i)%n) for b in B))
    I=[min(bases,key=lambda B:key(B,i)) for i in range(n)]
    f=[0]*n
    for i in range(n):
        A,B=set(I[i]),set(I[(i+1)%n])
        if A==B: f[i]= i+n if i in A else i
        else:
            j=(B-A).pop(); assert A-B=={i}
            f[i]= j if j>i else j+n
    assert sum(f[i]-i for i in range(n))==k*n
    F=lambda x: f[x%n]+(x//n)*n
    l=sum(1 for i in range(n) for j in range(i+1,i+n+1) if F(i)>F(j))
    return k*(n-k)-l, f
# sanity: totally positive Vandermonde
V=[[ (j+1)**r for j in range(n)] for r in range(k)]
m=minors(V); print('sanity TP:',cdim([T for T,v in m.items() if v])[0],'(expect 28)')
res=collections.defaultdict(list)
def run(name,layers):
    M=matrix(*layers)
    for S4 in itertools.combinations(range(9),4):
        m=minors([M[i] for i in S4]); nz=[v for v in m.values() if v]
        if nz and (all(v>0 for v in nz) or all(v<0 for v in nz)):
            d,f=cdim([T for T,v in m.items() if v]); res[name].append((S4,d,len(nz)))
run('62',[g['grey']]); run('62+216',[g['grey'],g['black']]); run('blue only',[g['blue']])
# even-line
EV=g['EVEN_D']; even_lines=[l for l in range(1,30) if g['dgroup'](l) in EV]; rowsD=sorted(EV)
E=[[0]*11 for _ in rowsD]
for (line,col),v in g['blue'].items(): E[rowsD.index(g['dgroup'](line))][even_lines.index(line)]+=v
for om in range(5):
    r=[E[i] for i in range(5) if i!=om]; m=minors(r); nz=[v for v in m.values() if v]
    d,f=cdim([T for T,v in m.items() if v]); res['even'].append((om,d,len(nz)))
for name,L in res.items():
    print(name,len(L),'dims:',sorted(collections.Counter(d for _,d,_ in L).items()),'nonzero-minor counts:',sorted(collections.Counter(c for *_,c in L).items()))
