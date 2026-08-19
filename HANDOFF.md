# HANDOFF — 2026-08-15

## Where the project is

**A clean repo (`Maths 5`) with the container protocol and one container built.** The old
repo (`maths 4`, frozen at `d9c51b5`) holds 418 kernel-checked theorems and the full
history; nothing is deleted from it, and it is the source for mining `why` fields.

Read `PROTOCOL.md` first, then `INTERFACES.md`, then this file.

## What container 06 (the carrier) delivers

**The claim "the icosian ring is E8" now has a criterion at every step and no literal
anywhere.** The chain:

    the 120 icosians  (unit icosians; equivalently 2I from two generators)
      -> Z-span of {2q, 2*phi*q}, doubled coords
      -> HERMITE NORMAL FORM        (canonical -> the basis is UNIQUE)
      -> Gram under B(x,y)=Tr(delta<x,y>), delta=phi/sqrt5
      -> det 256, even, half-Gram unimodular with even diagonal  ==  E8
      -> emb: integer M, M M^T = 2G AND rows in L,  det -256,  UNIQUE UP TO Aut(L)

All four emits are present (`derivation.py`, a model TODO below, `check/`, `statement.md`)
and the check consumes the derivation via `gen_lean.py`.

## Three findings this container surfaced, all measured

1. **The 6->7 joint was a comment.** maths 4's E8 side worked on an 8x8 integer basis and
   a Gram matrix written as literals, "solved externally". It never consumed the 120
   icosians as objects. The tie existed in one docstring. **That gap is now closed** — the
   basis is derived from the 120 by HNF.

2. **maths 4's `icosianBasis` literal is a DIFFERENT E8 lattice** from the one derived
   here — neither contains the other. Both are even unimodular rank 8. **Not repaired**
   (a finding does not authorise repair in the same pass). Whether it is a convention
   difference in this reconstruction or a defect there is the FIRST thing a repair session
   should settle — see `statement.md`.

3. **`lattice(1).html`'s 120 are a conjugate copy** of the ledger's (differ in 96 of 120,
   a coordinate transposition). Legitimate, and a false-fail generator until declared:
   the 120 are UNIQUE UP TO a coordinate permutation.

## Build status at handoff

The Lean build (`lake build Container06`) was **running in the background at commit time**.
The determinant needed two fixes carried from maths 4 — fuel-recursion Laplace expansion
(not `Id.run do`) and the Bool `(x == y) = true` idiom (not propositional `=`) — plus
`maxHeartbeats 4000000` for the 8! expansion. **A monitor is watching it; its result is
the first thing to confirm.** If it failed, the errors are in `/tmp/ring_build.log` and
the fix is Lean-mechanics, not mathematics — the Python derivation is proven correct
independently.

## Next session — pick ONE

- **A. Confirm the build and wire `lake build Container06` into a container `verify.py`.**
  Smallest, closes container 6. The three-command check (`derivation --check`,
  `gen_lean --check`, `lake build`) becomes one exit code.

- **B. The model emit.** `lattice(1).html` is the container's model but its constants are
  hardcoded (`G5=V[8]`). Rebuild it to import `derivation.json`, so the model consumes the
  derivation like the check does. This is where the watchable-mechanism goal lives.

- **C. Settle finding 2** — is maths 4's `icosianBasis` a different convention or a defect?
  A repair session with that single finding as input, per the protocol.

- **D. Next container.** 5 (icosahedron) feeds 6; 7 (E8) now has its interface. Either is
  a packaging container — largely built in maths 4, needs a derivation.

**Recommendation: A, then B.** A is minutes and closes the loop; B delivers the watchable
model, which is the deliverable that fits "run the simulation in my head at any scale."
C and D are their own sessions.

## The one instrument still to build

`verify.py` at repo root — the protocol's checker: runs each container's three checks,
reports per step, a fail carries step/expected/computed and does not authorise repair.
It does not exist yet; the container-06 checks are run by hand for now. Building it is
part of task A.
