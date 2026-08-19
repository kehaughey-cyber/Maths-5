# Maths 5 — the Prime Framework, in containers

**The goal is transmissible truth**: a result someone else can rebuild from what is
written, without trusting the session that wrote it.

The unit of work is a **container** — one step of the argument, emitting four things
that must agree:

| emit | what it is |
|---|---|
| `derivation.py` | ordered steps: expression, dependencies, **why**, determinacy, exact value. **Computes its own values from its own criteria.** |
| `model/` | runnable and watchable; generates its objects cold and self-verifies |
| `check/` | Lean where it reaches, exact computation where it doesn't, with the axiom report |
| `statement.md` | capped; what this establishes and what it does not, citing step numbers |

**The model and the check CONSUME the derivation. They never restate it.**

`PROTOCOL.md` is the working agreement. `INTERFACES.md` declares what crosses each
container boundary. Everything before 2026-08-15 is in `../maths 4`, frozen.

## Lean

One lake project under `lean/`, one directory per container. Pins copied verbatim from
maths 4 so its 418 existing theorems compile unchanged:

    leanprover/lean4:v4.33.0-rc1     mathlib @ 7d6261f2dc0f

A floating Mathlib may not compile these files. Do not update the pins casually.
