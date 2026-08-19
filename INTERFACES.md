# INTERFACES — what crosses each container boundary

**Short, explicit, named.** A container may consume only what is listed here. This is
where every historic conflation in this project lived — the two roads, the three
twelves, the two senses of *internal* — and diffused through prose they recur forever.

**Status: the first boundary is probed, not yet declared.** Probing it changed what the
boundary is.

---

## 6 → 7 · the carrier to the lattice

### What was expected

*"Container 6 hands container 7 the 120 icosians and the codifferent form."*

### What is actually there — measured 2026-08-15

**That is not the interface.** `Closure/IcosianE8.lean` in maths 4 works on `V8 = List Int`,
an 8×8 integer basis `emb` and a Gram matrix `icosianGram`, both **written as literals**.
It does not consume the 120 icosians as objects anywhere. The connection to them exists
in exactly one place: a **comment** at `Closure/IcosianLattice.lean:332` —

> `/-- A Z-basis of the icosian ring -- the Z[phi]-span of the 120 unit icosians`

So the most load-bearing joint in the project is an **answer with its criterion in prose**.
`emb` is the answer. *"the Z[φ]-span of the 120 unit icosians under B(x,y) = Tr(δ⟨x,y⟩)"*
is the criterion, and nothing computes one from the other.

**The derivation step that closes this is the one that does not exist.**

---

## The 120 icosians — three constructions, probed

`containers/06-carrier-2i/interface_probe.py`, exact in ℤ[φ] throughout.

| construction | count | result |
|---|---:|---|
| **A** standard 8 + 16 + 96 (`Rung7/Icosians.lean`'s recipe) | 120 | — |
| **B** cold from two generators s, t (`Rung7/Carrier2I.lean`'s recipe) | 120 | **A = B, exactly** |
| **C** `lattice(1).html`'s `genVertices()` | 120 | **differs from A in 96 of 120** |

**A = B is now checked rather than assumed.** Two independent constructions in maths 4,
in two different arithmetics, produce the identical set. Nothing in that repo said so.

**C is not wrong — and that is the more important half.** It is closed under
multiplication, contains the same 8 Lipschitz and 16 Hurwitz units, and is exactly
**A with a coordinate transposition** (`swap y↔z`; equivalently `swap x↔y`). It is a
legitimate conjugate copy of 2I in the quaternions — the same abstract group, a different
embedding. The cause is one line: its base array reads `[0, ½, φ/2, ψ/2]` where A reads
`[0, ½, φ⁻¹/2, φ/2]`, and swapping two entries composes the even permutations with an odd
one.

**Nothing anywhere says this.** Anyone comparing a vertex index, a coordinate or a clock
assignment between `lattice` and the ledger gets a mismatch, and would read it as a
contradiction. **That is a false-fail generator sitting in the corpus today.**

### The determinacy class this fixes

The 120 icosians are **UNIQUE UP TO conjugation by a coordinate permutation** — *not*
UNIQUE. Declared that way, A and C are both admissible and any comparison between them
happens at orbit level, where it belongs. Declared as an answer, they contradict.

This is the protocol's determinacy field earning its place on the first object it met.

---

## Consequences to settle before declaring 6 → 7

1. **`emb` needs a criterion**, not a literal. Until it has one, containers 6 and 7 are
   joined by a comment.
2. **The 120 must be built once**, with A as the canonical copy (it is what both maths 4
   constructions produce), and C recorded as the conjugate copy it is.
3. **The decomposition may want revisiting.** The E8 line runs off the *rank-6 icosahedral
   module* (`dirs`, `sixDirs` in `IcosianLattice.lean`), which is container 5's object, not
   container 6's. Whether E8 sits downstream of the icosahedron or the carrier is a
   reading, and it is Kevin's.
