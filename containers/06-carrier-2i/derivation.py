"""CONTAINER 6 - THE CARRIER . DERIVATION.

    python3 derivation.py            emit derivation.json
    python3 derivation.py --check    recompute and fail on any disagreement

THE DERIVATION IS PRIMARY. The model and the check CONSUME what this emits; they
never restate it. Every value below is COMPUTED FROM ITS OWN CRITERION -- nothing is
typed in, because a typed value is an answer and answers do not reproduce.

Each step carries: what / expr / frm / why / determines / value.
`determines` is load-bearing and is one of

    UNIQUE            exactly one object satisfies the criterion
    UNIQUE UP TO X    determined only modulo a stated symmetry
    CHOSEN            many satisfy it; one was picked and the choice is recorded

A comparison happens at the declared level. Demanding more determinacy than an object
has is a category error, and it is the false-fail this project has bled from.
"""
import json
import sys
from fractions import Fraction as F
from itertools import permutations

# ------------------------------------------------------------------ exact Z[phi]
class Z:
    __slots__ = ("a", "b")
    def __init__(s, a=0, b=0): s.a = F(a); s.b = F(b)
    def __add__(s, o): return Z(s.a + o.a, s.b + o.b)
    def __neg__(s): return Z(-s.a, -s.b)
    def __sub__(s, o): return s + (-o)
    def __mul__(s, o): return Z(s.a * o.a + s.b * o.b, s.a * o.b + s.b * o.a + s.b * o.b)
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))

ZERO, ONE, HALF = Z(0, 0), Z(1, 0), Z(F(1, 2), 0)
PHI, PHIINV = Z(0, 1), Z(-1, 1)

STEPS = []


def step(sid, what, expr, frm, why, determines, value, check=None):
    STEPS.append(dict(id=sid, what=what, expr=expr, frm=frm, why=why,
                      determines=determines, value=value, check=check))
    return value


# ================================================================== 6.1
def even_perms():
    return [p for p in permutations(range(4))
            if sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2 == 0]


step("6.1", "the even permutations of four coordinates",
     "{p in S4 : inv(p) even}", [],
     "the 96-block of the icosians is an EVEN-permutation orbit; taking the odd orbit "
     "instead gives a conjugate copy, which is exactly how lattice(1).html and the "
     "maths 4 ledger came to disagree in 96 of 120 elements",
     "UNIQUE", [list(p) for p in even_perms()])


# ================================================================== 6.2
def icosians_120():
    V = set()
    for i in range(4):                                     # 8 Lipschitz units
        for s in (ONE, -ONE):
            v = [ZERO] * 4
            v[i] = s
            V.add(tuple(v))
    for m in range(16):                                    # 16 Hurwitz units
        V.add(tuple(HALF if (m >> k) & 1 == 0 else -HALF for k in range(4)))
    base = [ZERO, HALF, Z(F(1, 2), 0) * PHIINV, Z(F(1, 2), 0) * PHI]
    for p in even_perms():                                 # 96 golden units
        vals = [base[p[i]] for i in range(4)]
        nz = [i for i in range(4) if not vals[i] == ZERO]
        for m in range(1 << len(nz)):
            v = list(vals)
            for bit, i in enumerate(nz):
                if (m >> bit) & 1:
                    v[i] = -v[i]
            V.add(tuple(v))
    return sorted(V, key=lambda q: [(float(c.a), float(c.b)) for c in q])


Q = icosians_120()
step("6.2", "the 120 unit icosians",
     "8 Lipschitz (+-1,0,0,0) | 16 Hurwitz (+-1/2)^4 | 96 even perms of "
     "(0, 1/2, phi^-1/2, phi/2) with all sign patterns",
     ["6.1"],
     "the unit group of the icosian ring; equivalently the 600-cell's vertices; "
     "equivalently 2I. The descriptions coincide and 6.3 checks that they do",
     "UNIQUE UP TO conjugation by a coordinate permutation",
     len(Q), check="count == 120")
assert len(Q) == 120


# ================================================================== 6.3
def qmul(p, r):
    a, b, c, d = p
    e, f, g, h = r
    return (a * e - b * f - c * g - d * h, a * f + b * e + c * h - d * g,
            a * g - b * h + c * e + d * f, a * h + b * g - c * f + d * e)


def from_generators():
    s = (HALF, HALF, HALF, HALF)
    t = (Z(F(1, 2), 0) * PHI, Z(F(1, 2), 0) * PHIINV, HALF, ZERO)
    V = {(ONE, ZERO, ZERO, ZERO)}
    front = [(ONE, ZERO, ZERO, ZERO)]
    while front:
        nxt = []
        for v in front:
            for g in (s, t):
                w = qmul(v, g)
                if w not in V:
                    V.add(w)
                    nxt.append(w)
        front = nxt
        if len(V) > 400:
            break
    return V


COLD = from_generators()
step("6.3", "the same 120, generated cold from two icosians",
     "closure of {1} under right-multiplication by s = (1+i+j+k)/2 and "
     "t = (phi + phi^-1 i + j)/2",
     ["6.2"],
     "a SECOND, independent construction. Two constructions agreeing is evidence; two "
     "constructions nobody ever compared is a drift vector, which is what maths 4 had",
     "UNIQUE", set(Q) == COLD, check="set equality with 6.2")
assert set(Q) == COLD


# ================================================================== 6.4
def doubled(q):
    out = []
    for c in q:
        m, n = 2 * c.a, 2 * c.b
        assert m.denominator == 1 and n.denominator == 1
        out += [int(m), int(n)]
    return out


def times_phi(v):
    out = []
    for k in range(4):
        m, n = v[2 * k], v[2 * k + 1]
        out += [n, m + n]                 # phi(m + n phi) = n + (m+n) phi
    return out


step("6.4", "the doubled integer coordinates",
     "q |-> 2q, each Z[phi] entry m + n*phi flattened to (m, n)", ["6.2"],
     "icosian coordinates lie in (1/2)Z[phi]; doubling clears the halves so the lattice "
     "is integral. The factor 2 is a coordinate convention and nothing else",
     "UNIQUE", 8, check="8 integers per icosian")


# ================================================================== 6.5
def hnf(rows):
    M = [r[:] for r in rows]
    n = len(M[0])
    piv = 0
    out = []
    for col in range(n):
        p = next((i for i in range(piv, len(M)) if M[i][col] != 0), None)
        if p is None:
            continue
        M[piv], M[p] = M[p], M[piv]
        for i in range(piv + 1, len(M)):
            while M[i][col] != 0:
                if abs(M[piv][col]) > abs(M[i][col]):
                    M[piv], M[i] = M[i], M[piv]
                qq = M[i][col] // M[piv][col]
                M[i] = [a - qq * b for a, b in zip(M[i], M[piv])]
        if M[piv][col] < 0:
            M[piv] = [-a for a in M[piv]]
        for i in range(piv):
            qq = M[i][col] // M[piv][col]
            if qq:
                M[i] = [a - qq * b for a, b in zip(M[i], M[piv])]
        out.append(M[piv])
        piv += 1
    return out


gens = []
for q in Q:
    v = doubled(q)
    gens += [v, times_phi(v)]
BASIS = hnf(gens)
step("6.5", "a Z-basis of the icosian ring",
     "HNF( { 2q, 2*phi*q : q in the 120 } )", ["6.2", "6.4"],
     "the icosian ring is the Z[phi]-span of the 120, so as a Z-module it is generated by "
     "each icosian together with its phi-multiple. HERMITE NORMAL FORM IS CANONICAL -- "
     "that is what turns 'computed externally by row reduction' (an answer, and "
     "basis-dependent) into a criterion whose answer is unique",
     "UNIQUE", BASIS, check="rank 8")
assert len(BASIS) == 8


# ================================================================== 6.6
def B(x, y):
    s = 0
    for k in range(4):
        m, n = x[2 * k], x[2 * k + 1]
        mm, nn = y[2 * k], y[2 * k + 1]
        s += m * mm + m * nn + n * mm + 2 * n * nn
    return s


step("6.6", "the codifferent form",
     "B(x,y) = Tr(delta <x,y>), delta = phi/sqrt5; on doubled coordinates this is "
     "sum_k (m m' + m n' + n m' + 2 n n')", ["6.4"],
     "restriction of scalars from Z[phi] to Z is self-dual only against the CODIFFERENT, "
     "so delta must be drawn from the inverse different (1/sqrt5) and be TOTALLY POSITIVE, "
     "or the form is not positive definite. The plain trace form fails here, and that "
     "failure is on maths 4's dead-ends list",
     "UNIQUE", "mm' + mn' + nm' + 2nn'")


# ================================================================== 6.7
def det(M):
    M = [[F(x) for x in r] for r in M]
    n = len(M)
    d = F(1)
    for i in range(n):
        p = next((r for r in range(i, n) if M[r][i] != 0), None)
        if p is None:
            return 0
        if p != i:
            M[i], M[p] = M[p], M[i]
            d = -d
        d *= M[i][i]
        for r in range(i + 1, n):
            f = M[r][i] / M[i][i]
            M[r] = [a - f * b for a, b in zip(M[r], M[i])]
    return int(d)


G = [[B(a, b) for b in BASIS] for a in BASIS]
H = [[x // 2 for x in r] for r in G]
INV = dict(det_G=det(G),
           all_even=all(x % 2 == 0 for r in G for x in r),
           det_halfGram=det(H),
           half_diag_even=all(H[i][i] % 2 == 0 for i in range(8)))
step("6.7", "the Gram of the icosian ring, and its invariants",
     "G = [B(b_i, b_j)] ; halfGram = G/2", ["6.5", "6.6"],
     "rank 8 + even + unimodular + positive definite characterises E8 uniquely, so these "
     "four facts ARE the identification. No classification theorem is invoked and none is "
     "needed -- which is what retires the uniqueness-theorem citation",
     "UNIQUE", INV,
     check="det G = 256, all entries even, det halfGram = 1, half diagonal even")
assert INV["det_G"] == 256 and INV["all_even"]
assert INV["det_halfGram"] == 1 and INV["half_diag_even"]


# ================================================================== 6.8
def in_L(y):
    return ((all(c % 2 == 0 for c in y)) or (all(c % 2 == 1 for c in y))) and sum(y) % 4 == 0


def vecs_of_norm(n, bound):
    out = []

    def rec(i, rem, cur):
        if i == 8:
            if rem == 0:
                out.append(cur[:])
            return
        if rem < 0:
            return
        m = int(rem ** 0.5)
        for x in range(-min(bound, m), min(bound, m) + 1):
            cur.append(x)
            rec(i + 1, rem - x * x, cur)
            cur.pop()

    rec(0, n, [])
    return out


T = [[2 * x for x in r] for r in G]
_rows = []


def _search(i):
    if i == 8:
        return True
    for v in vecs_of_norm(T[i][i], 3):
        if not in_L(v):
            continue
        if all(sum(a * b for a, b in zip(v, _rows[j])) == T[i][j] for j in range(i)):
            _rows.append(v)
            if _search(i + 1):
                return True
            _rows.pop()
    return False


assert _search(0)
EMB = _rows
step("6.8", "the isometry onto the textbook E8",
     "integer M with M M^T = 2G AND every row in L = {y in Z^8 : coordinates of one "
     "parity, sum = 0 mod 4}", ["6.5", "6.7"],
     "L is the doubled D8+ presentation of E8. THE FIRST VERSION OF THIS CRITERION "
     "OMITTED THE L CONDITION, and the search satisfied it with rows outside L -- a valid "
     "factorisation that is not an isometry onto the textbook lattice. An under-specified "
     "criterion is found by RUNNING it, never by reading it",
     "UNIQUE UP TO Aut(L)", EMB, check="M M^T = 2G, |det| = 256, every row in L")
assert [[sum(a * b for a, b in zip(x, y)) for y in EMB] for x in EMB] == T
assert abs(det(EMB)) == 256 and all(in_L(r) for r in EMB)


# ------------------------------------------------------------------ emit / check
OUT = dict(container="06-carrier-2i", steps=STEPS,
           values=dict(icosians_count=len(Q), basis=BASIS, gram=G, half_gram=H,
                       emb=EMB, invariants=INV))

if __name__ == "__main__":
    import pathlib
    p = pathlib.Path(__file__).parent / "derivation.json"
    new = json.dumps(OUT, indent=1, sort_keys=True)
    if "--check" in sys.argv:
        old = p.read_text(encoding="utf-8") if p.exists() else ""
        if old != new:
            print("DERIVATION IS STALE -- rerun `python3 derivation.py`")
            sys.exit(1)
        print(f"derivation: {len(STEPS)} steps, all recompute")
    else:
        p.write_text(new, encoding="utf-8")
        print(f"wrote derivation.json: {len(STEPS)} steps")
        for s in STEPS:
            print(f"  {s['id']:<5} {s['determines']:<48} {s['what']}")
