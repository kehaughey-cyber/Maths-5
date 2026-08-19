# Container 6 — the carrier · statement

**Capped. What this establishes and what it does not.** Every claim cites a step in
`derive_emb.py` or `interface_probe.py`; nothing here paraphrases a result.

## What is established

**The Z[φ]-span of the 120 unit icosians is E8 — derived, not asserted.** Taking the 120
icosians, the ℤ-module they generate together with the φ-action, and the Hermite normal
form of that generating set, gives a rank-8 lattice whose Gram under the codifferent form
`B(x,y) = Tr(δ⟨x,y⟩)` has determinant 256, all entries even, and half-Gram unimodular with
even diagonal. **Rank 8, even, unimodular, positive definite — that is E8.**

No basis is typed in. The HNF is canonical, so the basis is **UNIQUE**, not "a basis
obtained by row reduction".

**An isometry onto the textbook lattice exists and is constructed.** An integer matrix `M`
with `M·Mᵀ = 2G` and every row in `L = { y ∈ ℤ⁸ : coordinates of one parity, Σy ≡ 0 mod 4 }`,
the doubled D8+ presentation. Found by search over the criterion, `det M = −256`.
**Determinacy: UNIQUE UP TO Aut(L)** — the criterion fixes the lattice and the form, not the
frame.

**The two maths 4 constructions of the 120 agree exactly** — the standard 8+16+96 and the
cold generation from two generators, in two different arithmetics, give the identical set.

## What is not established

**This does not settle maths 4's `icosianBasis`.** That literal is also an even unimodular
rank-8 lattice, but it is **not the lattice derived here** — neither contains the other.
Whether that is a convention difference in this reconstruction or a defect there is **not
settled**, and per the protocol a finding does not authorise repair in the same pass.

What *is* settled is the shape of the gap: **every check on maths 4's E8 side verifies
E8-ness** — determinant, evenness, unimodularity, minimum norm, the 240 minimal vectors,
the isometry — **and none of them verifies that the lattice is the icosian ring.** The tie
to the 120 icosians exists in one comment. The conclusion is true — this container derives
it — but the evidence chain there had a hole exactly where a criterion was replaced by an
answer.

**No claim about chirality.** `lattice(1).html` uses a conjugate copy of the 120 (differing
in 96 of 120, a coordinate transposition). Both are legitimate; nothing here privileges one.

**Nothing toward alpha.** No cost, no coupling, no dynamics.
