"""GENERATE THE LEAN FROM THE DERIVATION.

    python3 gen_lean.py            emit ../../../lean/Container06/Ring.lean
    python3 gen_lean.py --check    fail if the tracked Lean disagrees with the derivation

THIS IS THE JOINT THE WHOLE PROTOCOL TURNS ON. The check must CONSUME the derivation,
not restate it -- but Lean cannot import a Python module, so the crossing is made here:
every literal in the emitted Lean is written from `derivation.json`, and `--check`
fails if the tracked file has drifted from it.

Without this, the Lean would hold a second copy of the basis and the Gram, and a second
copy is exactly how maths 4 ended up with four constructions of the 120 icosians and no
statement that they agree.

The emitted file imports NOTHING -- no Mathlib, no other container. Pure integer
arithmetic decided by the kernel, which is the zero-axiom standard.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
DERIV = HERE.parent / "derivation.json"
OUT = HERE.parent.parent.parent / "lean" / "Container06" / "Ring.lean"


from fractions import Fraction as _F


def _det(M):
    M = [[_F(x) for x in r] for r in M]
    n = len(M); d = _F(1)
    for i in range(n):
        p = next((r for r in range(i, n) if M[r][i] != 0), None)
        if p is None: return 0
        if p != i: M[i], M[p] = M[p], M[i]; d = -d
        d *= M[i][i]
        for r in range(i+1, n):
            f = M[r][i]/M[i][i]; M[r] = [a - f*b for a, b in zip(M[r], M[i])]
    return int(d)


def lean_list(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def lean_matrix(rows, indent="    "):
    body = (",\n" + indent + " ").join(lean_list(r) for r in rows)
    return "[" + body + "]"


def build():
    d = json.loads(DERIV.read_text(encoding="utf-8"))
    v = d["values"]
    basis, gram, half, emb = v["basis"], v["gram"], v["half_gram"], v["emb"]
    inv = v["invariants"]
    emb_det = _det(emb)
    steps = {s["id"]: s for s in d["steps"]}

    L = []
    A = L.append
    A("/-")
    A("  CONTAINER 06 - THE CARRIER . the icosian ring is E8")
    A("")
    A("  GENERATED FROM derivation.json BY check/gen_lean.py. DO NOT EDIT BY HAND --")
    A("  every literal below is emitted from the derivation, so there is exactly one")
    A("  home for each formula. `python3 gen_lean.py --check` fails if this file and")
    A("  the derivation disagree.")
    A("")
    A("  Imports nothing: no Mathlib, no other container. Pure integer arithmetic")
    A("  decided by the kernel.")
    A("")
    A("  THE CRITERIA, from the derivation's own `why` fields:")
    for sid in ("6.5", "6.6", "6.7", "6.8"):
        s = steps[sid]
        A(f"    {sid}  {s['what']}")
        A(f"          expr: {s['expr']}")
        A(f"          determines: {s['determines']}")
    A("-/")
    A("")
    A("-- 8x8 Laplace expansion is 8! leaf terms; the kernel needs the raised budget,")
    A("-- exactly as maths 4 (Closure/IcosianE8.lean:84) set for the same determinant.")
    A("set_option maxHeartbeats 4000000")
    A("")
    A("namespace Container06")
    A("")
    A("abbrev V8 := List Int")
    A("")
    A("def dotp (u v : V8) : Int := (List.zipWith (fun a b => a * b) u v).foldl (· + ·) 0")
    A("")
    A("/-- The codifferent form B(x,y) = Tr(delta <x,y>), delta = phi/sqrt5, on doubled")
    A("    Z[phi] coordinates. Step 6.6; see the header for why delta must be totally")
    A("    positive. -/")
    A("def qForm (x y : V8) : Int :=")
    A("  let f : Nat → Int := fun k =>")
    A("    let m := x.getD (2*k) 0; let n := x.getD (2*k+1) 0")
    A("    let m' := y.getD (2*k) 0; let n' := y.getD (2*k+1) 0")
    A("    m*m' + m*n' + n*m' + 2*n*n'")
    A("  f 0 + f 1 + f 2 + f 3")
    A("")
    A("/-- Step 6.5. The HNF of the Z-span of {2q, 2*phi*q : q in the 120}. HNF is")
    A("    canonical, so this basis is UNIQUE -- not 'a basis obtained by row reduction'. -/")
    A("def icosianBasis : List V8 :=")
    A("  " + lean_matrix(basis, "   "))
    A("")
    A("def gramOf (m : List V8) (f : V8 → V8 → Int) : List (List Int) :=")
    A("  m.map (fun a => m.map (fun b => f a b))")
    A("")
    A("/-- Step 6.7. -/")
    A("def icosianGram : List (List Int) := gramOf icosianBasis qForm")
    A("")
    A("def halfGram : List (List Int) :=")
    A("  " + lean_matrix(half, "   "))
    A("")
    A("/-- Delete the n-th entry of a row. -/")
    A("def delNth : Nat → List Int → List Int")
    A("  | _, [] => []")
    A("  | 0, _ :: xs => xs")
    A("  | n+1, x :: xs => x :: delNth n xs")
    A("")
    A("/-- Determinant by Laplace expansion with explicit fuel. Structural recursion on")
    A("    Nat reduces under `decide`; an Id.run do loop or well-founded recursion does")
    A("    not, and drags in Quot.sound. maths 4's pattern, carried verbatim. -/")
    A("def detM : Nat → List (List Int) → Int")
    A("  | 0, _ => 1")
    A("  | _, [] => 1")
    A("  | f+1, r :: rs =>")
    A("      (((List.range r.length).zip r).foldl")
    A("        (fun acc p =>")
    A("          acc + (if p.1 % 2 == 0 then (1 : Int) else -1) * p.2 *")
    A("                detM f (rs.map (delNth p.1)))")
    A("        0)")
    A("")
    A("def detOf (m : List (List Int)) : Int := detM m.length m")
    A("")
    A("/-! ### the invariants that ARE the identification -/")
    A("")
    A(f"theorem gram_determinant_is_256 : (detOf icosianGram == {inv['det_G']}) = true := by decide")
    A("")
    A("theorem gram_entries_all_even :")
    A("    icosianGram.all (fun r => r.all (fun x => x % 2 == 0)) = true := by decide")
    A("")
    A("theorem halfGram_is_the_half :")
    A("    (icosianGram.map (fun r => r.map (fun x => x / 2)) == halfGram) = true := by decide")
    A("")
    A(f"theorem halfGram_is_unimodular : (detOf halfGram == {inv['det_halfGram']}) = true := by decide")
    A("")
    A("theorem halfGram_diagonal_is_even :")
    A("    (List.range 8).all (fun i => ((halfGram.getD i []).getD i 0) % 2 == 0) = true := by")
    A("  decide")
    A("")
    A("/-- Rank 8, even, unimodular, positive definite characterises E8 uniquely. The four")
    A("    theorems above are that characterisation; no classification theorem is cited. -/")
    A("theorem icosian_ring_is_E8 :")
    A("    (icosianBasis.length = 8)")
    A("    ∧ ((detOf halfGram == 1) = true)")
    A("    ∧ (icosianGram.all (fun r => r.all (fun x => x % 2 == 0)) = true) := by")
    A("  refine ⟨by decide, by decide, by decide⟩")
    A("")
    A("/-! ### step 6.8 -- the isometry onto the textbook lattice -/")
    A("")
    A("/-- L = { y : coordinates of one parity, sum y = 0 mod 4 }, the doubled D8+")
    A("    presentation of E8. -/")
    A("def inL (y : V8) : Bool :=")
    A("  ((y.all (fun c => c % 2 == 0)) || (y.all (fun c => c % 2 == 1)))")
    A("  && ((y.foldl (· + ·) 0) % 4 == 0)")
    A("")
    A("/-- Step 6.8. Found by search over the criterion, not solved externally.")
    A("    DETERMINACY: UNIQUE UP TO Aut(L) -- the criterion fixes the lattice and the")
    A("    form, not the frame. -/")
    A("def emb : List V8 :=")
    A("  " + lean_matrix(emb, "   "))
    A("")
    A("def twice (m : List (List Int)) : List (List Int) := m.map (fun r => r.map (fun x => 2 * x))")
    A("")
    A("theorem emb_is_an_isometry :")
    A("    (gramOf emb dotp == twice icosianGram) = true := by decide")
    A("")
    A(f"theorem emb_is_nonsingular : (detOf emb == {emb_det}) = true := by decide")
    A("")
    A("theorem emb_rows_lie_in_L : emb.all inL = true := by decide")
    A("")
    A("end Container06")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    text = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if "--check" in sys.argv:
        cur = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if cur != text:
            print("LEAN IS STALE against derivation.json -- rerun `python3 gen_lean.py`")
            sys.exit(1)
        print(f"lean: {OUT.name} agrees with the derivation")
    else:
        OUT.write_text(text, encoding="utf-8")
        print(f"wrote {OUT} ({len(text.splitlines())} lines) from derivation.json")
