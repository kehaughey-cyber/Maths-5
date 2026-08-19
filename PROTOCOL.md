# PROTOCOL — the working agreement

**The goal is transmissible truth**: a result someone else can rebuild from what is
written, without trusting the session that wrote it.

## The container

The unit of work is a **container** — one step of the argument. It emits four things
that must agree, and the agreement is mechanical:

| emit | rule |
|---|---|
| **derivation** (`derivation.py` → `derivation.json`) | ordered steps, each with expression, dependencies, **why**, **determinacy**, exact value. COMPUTES its values from its criteria. `--check` recomputes and fails on drift. |
| **model** | runnable, watchable, self-verifying on open. CONSUMES the derivation's values. |
| **check** (`check/` → `lean/`) | Lean where the axiom report is the deliverable; exact computation elsewhere. Generated FROM the derivation by `gen_lean.py`; `--check` fails on drift. |
| **statement** (`statement.md`) | capped. What this establishes and what it does not, citing step numbers. |

**One formula, one home.** A literal in the model or the check was emitted from the
derivation, never typed twice. Two copies of a number is how maths 4 built the 120
icosians four times and never noticed they had drifted.

## Determinacy — the field that stops false fails

Every derivation step declares what it pins down:

- **UNIQUE** — exactly one object satisfies the criterion.
- **UNIQUE UP TO X** — determined only modulo a stated symmetry.
- **CHOSEN** — many satisfy it; one was picked, and the choice is recorded.

**Comparison happens at the declared level.** Demanding more determinacy than an object
has is a category error — it fails a correct object for being written differently. The
120 icosians are UNIQUE UP TO a coordinate permutation; `lattice(1).html`'s copy differs
from the ledger's in 96 of 120 and is not wrong. Declared as UNIQUE they contradict;
declared correctly they agree at orbit level.

## Criteria reproduce; answers don't

Most of what maths 4 lost was **answers recorded where criteria belonged** — an index,
a picked basis, a "solved externally". A step states the property that SELECTS its
object, so the object can be re-found rather than re-trusted. A genuine search records
**the search criterion plus the witness it returned** — still reproducible, because the
criterion is the formula and the witness is checkable against it.

## Guards — the burden is asymmetric

A false pass costs one re-run; a false fail costs a rebuild of something correct, and
the rebuild is where conflation enters. So the fail carries the higher burden.

- Compare where the claim lives (set as set, orbit as orbit, exact arithmetic).
- Report **per step**, never per container.
- **A fail emits a finding and STOPS. Repair is a separate session** with that finding
  as its only input. A finding does not authorise repair in the pass that found it.
- An under-specified criterion is found by **running** it, not by reading it — step 6.8
  proved this on its first use: `M·Mᵀ = 2G` alone admitted a wrong M until the L
  condition was added.

## Lean

One lake project under `lean/`, one directory per container. Pins copied verbatim from
maths 4 so its 418 theorems compile unchanged. Container 6 imports nothing — pure
integer arithmetic, `decide`, zero axioms. Later containers may `require mathlib`.
