"""Checks for Section 4 (Folding and the time axis).
Every line prints a statement and PASS or FAIL. Standard library plus numpy only.
Run: python3 fold_time_axis_checks.py
"""
from math import gcd
from fractions import Fraction
import numpy as np

fails = 0
def check(text, ok):
    global fails
    print(("PASS  " if ok else "FAIL  ") + text)
    if not ok:
        fails += 1

def lcm(a, b): return a * b // gcd(a, b)

G = (24, 27, 36); SHIFT = 114; CYCLE = 216

# 1 capacities
check("D6 - D3 = 604 - 718 = -114 (capacities taken from the grid, as published)", 604 - 718 == -114)

# 3 meeting times and great cycle
check("lcm(24,36)=72, lcm(27,36)=108, lcm(24,27)=216, lcm(24,27,36)=216",
      (lcm(24,36), lcm(27,36), lcm(24,27), lcm(lcm(24,27),36)) == (72,108,216,216))
check("gcd(114,216)=6 and 216/6=36 matches", gcd(114,216)==6 and CYCLE//6==36)
orb = {(SHIFT*k) % CYCLE for k in range(36)}
check("shift 114 applied k times: 36 distinct positions, all multiples of 6, none repeats before 36",
      len(orb)==36 and all(p%6==0 for p in orb) and all((SHIFT*k)%CYCLE!=0 for k in range(1,36)))
for p,q in ((24,36),(27,36),(24,27)):
    pass
check("gear turns in 216 ticks: 9, 8, 6", tuple(CYCLE//g for g in G)==(9,8,6))

# 4 windings
great = 36*SHIFT
check("great cycle = 36*114 = 4104 = 19*216 (19 half-turns)", great==4104 and great==19*216)
check("4104/432 = 9.5 circles, so the half is exchanged", Fraction(great,432)==Fraction(19,2))
check("two great cycles 8208 = 19*432", 2*great==19*432)
comb = 6*great
check("combined cycle 24624 = 114*216 = 57*432 (114 half-turns)", comb==24624==114*216==57*432)
check("with two orientations: 2*114 = 228", 2*114==228)
check("gear turns in a great cycle: 171, 152, 114", tuple(great//g for g in G)==(171,152,114))
check("meetings per half-turn: 3, 2, 1", (216//72,216//108,216//216)==(3,2,1))
check("meetings in a great cycle: 57, 38, 19 (sum 114); combined 342, 228, 114 (sum 684)",
      (great//72,great//108,great//216)==(57,38,19) and sum((great//72,great//108,great//216))==114
      and (comb//72,comb//108,comb//216)==(342,228,114) and 342+228+114==684)

# 5 rotation number and Farey order 39
check("114/216 = 19/36 in lowest terms", Fraction(114,216)==Fraction(19,36))
F = sorted({Fraction(a,b) for b in range(1,40) for a in range(0,b+1) if gcd(a,b)==1})
check("Farey order 39 has 475 fractions", len(F)==475)
check("numerators sum to 6236, denominators to 12472", sum(f.numerator for f in F)==6236 and sum(f.denominator for f in F)==12472)
check("19/36 lies in Farey order 39", Fraction(19,36) in F)

# 6 Rule 1
Fm = np.array([[np.exp(2j*np.pi*j*k/24) for j in range(24)] for k in range(24)])
check("24 modes: F F* = 24 I and rank 24", np.allclose(Fm@Fm.conj().T, 24*np.eye(24)) and np.linalg.matrix_rank(Fm)==24)
check("-24/24 = -1; level two 24 + 24*25/2 = 324", Fraction(-24,24)==-1 and 24+24*25//2==324)

# 7 Rule 2
check("core sum 7840-1235 = 8560-1955 = 6605", 7840-1235==8560-1955==6605)
rho = lambda i: 115-i
check("rho maps 16..99 onto itself in reverse, rho(rho(i))=i",
      sorted(rho(i) for i in range(16,100))==list(range(16,100)) and all(rho(rho(i))==i for i in range(1,115)))

# 8 Rule 3
check("lines 14+9+4 = 27 spatial, +2 for T = 29", 14+9+4==27 and 27+2==29)

# 9 Rule 4
check("pairs (n,w): 216*36 = 7776 = 6**5 = 36*36*6", 216*36==7776==6**5==36*36*6)
check("95 degrees * w mod 180 gives 36 distinct angles, all multiples of 5",
      len({(95*w)%180 for w in range(36)})==36 and all(((95*w)%180)%5==0 for w in range(36)))
check("n = 6m + r covers 0..215 once", sorted(6*m+r for m in range(36) for r in range(6))==list(range(216)))
mir = lambda s:(s[2],s[1],s[0])
orbit = {((19*k)%36,0,k%36) for k in range(36)}
check("mirror (m,r,w)->(w,r,m) maps the clock orbit onto itself; 216 fixed states",
      {mir(s) for s in orbit}==orbit and sum(1 for m in range(36) for r in range(6) for w in range(36) if m==w)==216)

# 10 Rule 5
def only_2_3_19(n):
    c = 0
    for p in (2,3,19):
        while n%p==0:
            n//=p
            if p==19: c+=1
    return n==1 and c<=1
vals = [216,24,27,36,114,72,108,216,36,4104,24624,19,38,114,228]
check("all clock quantities have the form 2^a 3^b 19^c with c <= 1", all(only_2_3_19(v) for v in vals))

# 11 Rule 6 and the diameter
d12, d23 = 9-8, 8-6
check("relative windings 1, 2, 3 and both threes agree", (d12,d23,d12+d23)==(1,2,3))
check("diameter 36 to 216 is 180 long; 216 = 180 + 36 = 6*36 = 6**3; step 6 of 36 degrees",
      216-36==180==5*36 and 216==180+36==6*36==6**3)

print()
print("ALL PASS" if fails==0 else f"{fails} FAILED")
