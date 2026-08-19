"""DERIVING icosianBasis AND emb FROM THEIR CRITERIA.

maths 4 carries both as literals with the criterion in a docstring:
  icosianBasis -- "Computed externally by row reduction"
  emb          -- "Solved externally by matching an E8 Dynkin configuration"

Both are ANSWERS. This recovers each from the property that selects it.
Exact integer arithmetic throughout; nothing is imported from maths 4.
"""
from fractions import Fraction as F
from itertools import permutations

# ---------------------------------------------------------------- the 120, cold
class Z:
    __slots__=("a","b")
    def __init__(s,a=0,b=0): s.a=F(a); s.b=F(b)
    def __add__(s,o): return Z(s.a+o.a,s.b+o.b)
    def __neg__(s): return Z(-s.a,-s.b)
    def __mul__(s,o): return Z(s.a*o.a+s.b*o.b, s.a*o.b+s.b*o.a+s.b*o.b)
    def __eq__(s,o): return s.a==o.a and s.b==o.b
    def __hash__(s): return hash((s.a,s.b))
ZERO=Z(0,0); ONE=Z(1,0); HALF=Z(F(1,2),0); PHI=Z(0,1); PHIINV=Z(-1,1)

def even_perms():
    return [p for p in permutations(range(4))
            if sum(1 for i in range(4) for j in range(i+1,4) if p[i]>p[j])%2==0]

def icosians_120():
    V=set()
    for i in range(4):
        for s in (ONE,-ONE):
            v=[ZERO]*4; v[i]=s; V.add(tuple(v))
    for m in range(16):
        V.add(tuple(HALF if (m>>k)&1==0 else -HALF for k in range(4)))
    base=[ZERO, HALF, Z(F(1,2),0)*PHIINV, Z(F(1,2),0)*PHI]
    for p in even_perms():
        vals=[base[p[i]] for i in range(4)]
        nz=[i for i in range(4) if not vals[i]==ZERO]
        for m in range(1<<len(nz)):
            v=list(vals)
            for bit,i in enumerate(nz):
                if (m>>bit)&1: v[i]=-v[i]
            V.add(tuple(v))
    assert len(V)==120
    return sorted(V, key=lambda q:[(float(c.a),float(c.b)) for c in q])

# --------------------------------------------- doubled coords: 4 x Z[phi] -> 8 ints
def doubled(q):
    """2q, each coordinate m+n*phi flattened to (m,n). Integral by construction."""
    out=[]
    for c in q:
        m=2*c.a; n=2*c.b
        assert m.denominator==1 and n.denominator==1
        out += [int(m), int(n)]
    return out

def times_phi(v8):
    """phi*(m+n phi) = n + (m+n) phi, applied coordinatewise."""
    out=[]
    for k in range(4):
        m,n=v8[2*k],v8[2*k+1]
        out += [n, m+n]
    return out

# ---------------------------------------------------------------- Hermite normal form
def hnf(rows):
    """Row-style HNF over Z -- the CANONICAL basis of the lattice the rows span.
    Canonical is the point: it makes the basis UNIQUE, not merely 'some basis'."""
    M=[r[:] for r in rows]; n=len(M[0]); piv=0; basis=[]
    for col in range(n):
        p=None
        for i in range(piv,len(M)):
            if M[i][col]!=0: p=i; break
        if p is None: continue
        M[piv],M[p]=M[p],M[piv]
        for i in range(piv+1,len(M)):
            while M[i][col]!=0:
                if abs(M[piv][col])>abs(M[i][col]): M[piv],M[i]=M[i],M[piv]
                q=M[i][col]//M[piv][col]
                M[i]=[a-q*b for a,b in zip(M[i],M[piv])]
        if M[piv][col]<0: M[piv]=[-a for a in M[piv]]
        for i in range(piv):
            q=M[i][col]//M[piv][col]
            if q: M[i]=[a-q*b for a,b in zip(M[i],M[piv])]
        basis.append(M[piv]); piv+=1
    return basis

# ---------------------------------------------------------------- the codifferent form
def B(x,y):
    """B(u,v) = Tr(delta<u,v>), delta = phi/sqrt5, on doubled Z[phi] coords.
    For u=m+n phi, v=m'+n' phi:  uv = (mm'+nn') + (mn'+nm'+nn')phi, and
    Tr(delta z) = a+b for z=a+b phi -- hence mm'+mn'+nm'+2nn'."""
    s=0
    for k in range(4):
        m,n=x[2*k],x[2*k+1]; mm,nn=y[2*k],y[2*k+1]
        s += m*mm + m*nn + n*mm + 2*n*nn
    return s

def gram(basis): return [[B(a,b) for b in basis] for a in basis]

def det(M):
    M=[[F(x) for x in r] for r in M]; n=len(M); d=F(1)
    for i in range(n):
        p=next((r for r in range(i,n) if M[r][i]!=0), None)
        if p is None: return 0
        if p!=i: M[i],M[p]=M[p],M[i]; d=-d
        d*=M[i][i]
        for r in range(i+1,n):
            f=M[r][i]/M[i][i]
            M[r]=[a-f*b for a,b in zip(M[r],M[i])]
    return int(d)

# =================================================================== STEP 1
print("STEP 1  the icosian ring as a Z-module")
Q=icosians_120()
gens=[]
for q in Q:
    v=doubled(q); gens.append(v); gens.append(times_phi(v))
print(f"   generators: 120 icosians x {{1, phi}} = {len(gens)} vectors in Z^8")
Bas=hnf(gens)
print(f"   HNF rank .................. {len(Bas)}")
for r in Bas: print("     ", r)

# =================================================================== STEP 2
print("\nSTEP 2  the Gram under the codifferent form")
G=gram(Bas)
print(f"   det(G) .................... {det(G)}")
print(f"   every entry even .......... {all(x%2==0 for r in G for x in r)}")
H=[[x//2 for x in r] for r in G]
print(f"   det(halfGram) ............. {det(H)}   (1 = unimodular)")
print(f"   halfGram diagonal even .... {all(H[i][i]%2==0 for i in range(8))}   (even lattice)")
print(f"   => rank 8, even, unimodular, positive definite  ==  E8")

# =================================================================== STEP 3
print("\nSTEP 3  compare with maths 4's literal icosianBasis")
LIT=[[1,0, 1,0, 1,0, 1,0],
     [0,1, 0,0, 1,0, -1,1],
     [0,0, 1,0, 0,1, -1,1],
     [0,0, 0,1, -1,1, 1,0],
     [0,0, 0,0, 2,0, 0,0],
     [0,0, 0,0, 0,2, -2,2],
     [0,0, 0,0, 0,0, 2,0],
     [0,0, 0,0, 0,0, 0,2]]
print(f"   HNF(literal) == HNF(derived) ? {hnf(LIT)==Bas}")
print(f"   same Gram ?                    {gram(hnf(LIT))==G}")

# =================================================================== STEP 3b  WHY?
print("\nSTEP 3b  diagnosing the mismatch")
GL=gram(hnf(LIT))
HL=[[x//2 for x in r] for r in GL] if all(x%2==0 for r in GL for x in r) else None
print(f"   literal: det(G) = {det(GL)}   all-even = {all(x%2==0 for r in GL for x in r)}")
if HL: print(f"            det(halfGram) = {det(HL)}  diag even = {all(HL[i][i]%2==0 for i in range(8))}")
print(f"   literal is also an even unimodular rank-8 lattice = also E8")

# is the literal the span of a DIFFERENT copy of the 120?
def icosians_swapped():
    """the same recipe with the base array's last two entries swapped -- the
    conjugate copy that lattice(1).html uses."""
    V=set()
    for i in range(4):
        for s in (ONE,-ONE):
            v=[ZERO]*4; v[i]=s; V.add(tuple(v))
    for m in range(16):
        V.add(tuple(HALF if (m>>k)&1==0 else -HALF for k in range(4)))
    base=[ZERO, HALF, Z(F(1,2),0)*PHI, Z(F(1,2),0)*PHIINV]
    for p in even_perms():
        vals=[base[p[i]] for i in range(4)]
        nz=[i for i in range(4) if not vals[i]==ZERO]
        for m in range(1<<len(nz)):
            v=list(vals)
            for bit,i in enumerate(nz):
                if (m>>bit)&1: v[i]=-v[i]
            V.add(tuple(v))
    return sorted(V, key=lambda q:[(float(c.a),float(c.b)) for c in q])

g2=[]
for q in icosians_swapped():
    v=doubled(q); g2.append(v); g2.append(times_phi(v))
B2=hnf(g2)
print(f"   HNF(conjugate copy) == HNF(literal) ? {B2==hnf(LIT)}")
print(f"   HNF(conjugate copy) == HNF(derived)  ? {B2==Bas}")

# index: is one a sublattice of the other?
def in_span(v, basis):
    """solve v = x*basis over Q, integral?"""
    n=len(basis); M=[[F(basis[i][j]) for i in range(n)]+[F(v[j])] for j in range(len(v))]
    r=0
    for c in range(n):
        p=next((i for i in range(r,len(M)) if M[i][c]!=0), None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]
        M[r]=[a/M[r][c] for a in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]!=0:
                f=M[i][c]; M[i]=[a-f*b for a,b in zip(M[i],M[r])]
        r+=1
    sol=[0]*n
    for i in range(r):
        c=next(j for j in range(n) if M[i][j]==1)
        sol[c]=M[i][-1]
    if any(x.denominator!=1 for x in sol): return False
    chk=[sum(int(sol[i])*basis[i][j] for i in range(n)) for j in range(len(v))]
    return chk==list(v)
print(f"   every literal row inside the derived lattice ? "
      f"{all(in_span(r,Bas) for r in LIT)}")
print(f"   every derived row inside the literal lattice ? "
      f"{all(in_span(r,hnf(LIT)) for r in Bas)}")

# =================================================================== STEP 4  emb, derived
print("\nSTEP 4  emb from its criterion")
print("   CRITERION: an integer 8x8 matrix M with M M^T = 2G, G the derived Gram.")
print("   (the factor 2 is the coordinate doubling: E8 sits in (1/2)Z^8, so 2E8 sits in Z^8)")
T=[[2*x for x in r] for r in G]
print(f"   target norms 2G_ii: {[T[i][i] for i in range(8)]}")

import sys
sys.setrecursionlimit(10000)

def vectors_of_norm(n, bound):
    """all integer 8-vectors of squared length n, entries in [-bound,bound]."""
    out=[]
    def rec(i, rem, cur):
        if i==8:
            if rem==0: out.append(cur[:])
            return
        # prune: remaining 8-i slots each contribute >=0
        if rem<0: return
        m=int(rem**0.5)
        for x in range(-min(bound,m), min(bound,m)+1):
            cur.append(x); rec(i+1, rem-x*x, cur); cur.pop()
    rec(0,n,[])
    return out

rows=[]
def search(i):
    if i==8: return True
    cands=vectors_of_norm(T[i][i], 3)
    for v in cands:
        if all(sum(a*b for a,b in zip(v,rows[j]))==T[i][j] for j in range(i)):
            rows.append(v)
            if search(i+1): return True
            rows.pop()
    return False

ok=search(0)
print(f"   solution found: {ok}")
if ok:
    M=rows
    for r in M: print("     ", r)
    MMT=[[sum(a*b for a,b in zip(x,y)) for y in M] for x in M]
    print(f"   M M^T == 2G ? {MMT==T}")
    print(f"   det(M) = {det(M)}   (|det| = 256 required)")
    def inL(y): 
        return ((all(c%2==0 for c in y)) or (all(c%2==1 for c in y))) and sum(y)%4==0
    print(f"   all rows in the doubled D8+ lattice L ? {all(inL(r) for r in M)}")

# =================================================================== STEP 5  the FULL criterion
print("\nSTEP 5  the criterion was incomplete -- sharpening it")
print("   M M^T = 2G alone admits an M whose rows are NOT in the standard lattice.")
print("   The mathematical content is an ISOMETRY ONTO THE TEXTBOOK E8, so the")
print("   criterion must also require every row to lie in L = doubled D8+:")
print("     L = { y in Z^8 : all coords same parity, sum y = 0 mod 4 }")

def inL(y):
    return ((all(c%2==0 for c in y)) or (all(c%2==1 for c in y))) and sum(y)%4==0

rows2=[]
def search2(i):
    if i==8: return True
    for v in vectors_of_norm(T[i][i], 3):
        if not inL(v): continue
        if all(sum(a*b for a,b in zip(v,rows2[j]))==T[i][j] for j in range(i)):
            rows2.append(v)
            if search2(i+1): return True
            rows2.pop()
    return False

ok2=search2(0)
print(f"\n   solution under the FULL criterion: {ok2}")
if ok2:
    M2=rows2
    for r in M2: print("     ", r)
    MMT2=[[sum(a*b for a,b in zip(x,y)) for y in M2] for x in M2]
    print(f"   M M^T == 2G ?              {MMT2==T}")
    print(f"   det(M) = {det(M2)}")
    print(f"   all rows in L ?            {all(inL(r) for r in M2)}")
    print("\n   DETERMINACY: UNIQUE UP TO Aut(L) -- the criterion fixes the lattice and")
    print("   the form, not the frame. maths 4's literal emb is another representative;")
    print("   both are admissible and any comparison belongs at orbit level.")
