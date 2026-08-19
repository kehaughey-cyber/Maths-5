"""INTERFACE PROBE — do the constructions of the 120 icosians agree?

Not a derivation yet. A measurement, run before declaring the interface, because
maths 4 builds the 120 at least three times in three arithmetics and nothing in
the repo says they are the same set.

Exact throughout: a coordinate is a+b*phi with a,b rational (Fraction), phi^2=phi+1.
"""
from fractions import Fraction as F
from itertools import permutations

class Z:                      # a + b*phi, exact
    __slots__=("a","b")
    def __init__(s,a=0,b=0): s.a=F(a); s.b=F(b)
    def __add__(s,o): return Z(s.a+o.a, s.b+o.b)
    def __neg__(s):   return Z(-s.a,-s.b)
    def __sub__(s,o): return s+(-o)
    def __mul__(s,o): return Z(s.a*o.a + s.b*o.b, s.a*o.b + s.b*o.a + s.b*o.b)
    def __eq__(s,o):  return s.a==o.a and s.b==o.b
    def __hash__(s):  return hash((s.a,s.b))
    def __repr__(s):  return f"{s.a}+{s.b}f"
ZERO=Z(0,0); ONE=Z(1,0); HALF=Z(F(1,2),0); PHI=Z(0,1); PHIINV=Z(-1,1)  # phi^-1 = phi-1

def q(*c): return tuple(c)
def qmul(p,r):
    a,b,c,d=p; e,f,g,h=r
    return (a*e-b*f-c*g-d*h, a*f+b*e+c*h-d*g, a*g-b*h+c*e+d*f, a*h+b*g-c*f+d*e)
def qneg(p): return tuple(-x for x in p)

def even_perms():
    out=[]
    for p in permutations(range(4)):
        inv=sum(1 for i in range(4) for j in range(i+1,4) if p[i]>p[j])
        if inv%2==0: out.append(p)
    return out

# ---------------------------------------------------------------- A. STANDARD 8+16+96
def build_standard():
    V=set()
    for i in range(4):
        for s in (ONE,-ONE):
            v=[ZERO]*4; v[i]=s; V.add(q(*v))
    for m in range(16):
        V.add(q(*[HALF if (m>>k)&1==0 else -HALF for k in range(4)]))
    base=[ZERO, HALF, Z(F(1,2),0)*PHIINV, Z(F(1,2),0)*PHI]   # 0, 1/2, phi^-1/2, phi/2
    for p in even_perms():
        vals=[base[p[i]] for i in range(4)]
        nz=[i for i in range(4) if not vals[i]==ZERO]
        for m in range(1<<len(nz)):
            v=list(vals)
            for bit,i in enumerate(nz):
                if (m>>bit)&1: v[i]=-v[i]
            V.add(q(*v))
    return V

# ---------------------------------------------------------------- B. COLD FROM 2 GENERATORS
def build_from_generators():
    s=q(HALF,HALF,HALF,HALF)                                   # (1+i+j+k)/2
    t=q(Z(F(1,2),0)*PHI, Z(F(1,2),0)*PHIINV, HALF, ZERO)       # (phi + phi^-1 i + j)/2
    V={q(ONE,ZERO,ZERO,ZERO)}
    frontier=[q(ONE,ZERO,ZERO,ZERO)]
    while frontier:
        nxt=[]
        for v in frontier:
            for g in (s,t):
                w=qmul(v,g)
                if w not in V: V.add(w); nxt.append(w)
        frontier=nxt
        if len(V)>400: break
    return V

# ---------------------------------------------------------------- C. LATTICE.HTML's genVertices
def build_lattice_html():
    V=set()
    for i in range(4):
        for s in (ONE,-ONE):
            v=[ZERO]*4; v[i]=s; V.add(q(*v))
    for m in range(16):
        V.add(q(*[-HALF if (m>>k)&1 else HALF for k in range(4)]))
    base=[ZERO, HALF, Z(F(1,2),0)*PHI, Z(F(1,2),0)*PHIINV]     # 0, .5, PHI/2, PSI/2
    for p in even_perms():
        v0=[base[p[i]] for i in range(4)]
        nz=[i for i in range(4) if not v0[i]==ZERO]
        for m in range(1<<len(nz)):
            v=list(v0)
            for bit,i in enumerate(nz):
                if (m>>bit)&1: v[i]=-v[i]
            V.add(q(*v))
    return V

A=build_standard(); B=build_from_generators(); C=build_lattice_html()
print(f"  A  standard 8+16+96 ............ {len(A)}")
print(f"  B  cold from two generators .... {len(B)}")
print(f"  C  lattice.html genVertices .... {len(C)}")
print()
print(f"  A == B ? {A==B}    A == C ? {A==C}    B == C ? {B==C}")
if A!=B: print(f"     A\B {len(A-B)}   B\A {len(B-A)}")
if A!=C: print(f"     A\C {len(A-C)}   C\A {len(C-A)}")

# ------------------------------------------------- WHY DO A AND C DIFFER, AND IS C A GROUP?
print("\n--- diagnosis ---")
def closed(V):
    Vs=set(V)
    for x in list(Vs)[:120]:
        for y in list(Vs)[:120]:
            if qmul(x,y) not in Vs: return False
    return True
print(f"  A closed under multiplication ... {closed(A)}")
print(f"  C closed under multiplication ... {closed(C)}")
# the 8 and 16 blocks
units=set()
for i in range(4):
    for s in (ONE,-ONE):
        v=[ZERO]*4; v[i]=s; units.add(q(*v))
hur={q(*[HALF if (m>>k)&1==0 else -HALF for k in range(4)]) for m in range(16)}
print(f"  the 8 Lipschitz units in both ... {units<=A and units<=C}")
print(f"  the 16 Hurwitz units in both .... {hur<=A and hur<=C}")
print(f"  so the difference is the 96-block only: A96={len(A-units-hur)} C96={len(C-units-hur)}")
# is C the mirror (conjugate) of A?
def conj(p): a,b,c,d=p; return (a,-b,-c,-d)
print(f"  C == conjugate(A) ? .............. {C=={conj(x) for x in A}}")
# is C A with a coordinate transposition?
def swap23(p): a,b,c,d=p; return (a,b,d,c)
print(f"  C == swap(y,z) of A ? ............ {C=={swap23(x) for x in A}}")
def swap12(p): a,b,c,d=p; return (a,c,b,d)
print(f"  C == swap(x,y) of A ? ............ {C=={swap12(x) for x in A}}")
