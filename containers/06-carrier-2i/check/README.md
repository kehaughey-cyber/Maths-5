# Container 06 · check

**The check CONSUMES the derivation. It never restates it.**

```
derivation.py  --run-->  derivation.json  --gen_lean.py-->  ../../../lean/Container06/Ring.lean
```

Every literal in `Ring.lean` — the basis, the Gram, the half-Gram, `emb` — is emitted
from `derivation.json` by `gen_lean.py`. There is exactly one home for each formula.

## To verify the whole chain

    python3 ../derivation.py --check      # the derivation still recomputes from criteria
    python3 gen_lean.py --check           # the tracked Lean still matches the derivation
    cd ../../../lean && lake build Container06   # the kernel confirms the theorems

If any step disagrees, the container is broken and says which step.

## What the Lean proves (all `decide`, zero axioms — no Mathlib, no native_decide)

| theorem | criterion, from the derivation |
|---|---|
| `gram_determinant_is_256` | 6.7 · det of the codifferent Gram is 256 |
| `gram_entries_all_even` | 6.7 · every Gram entry even |
| `halfGram_is_unimodular` | 6.7 · det(G/2) = 1 |
| `halfGram_diagonal_is_even` | 6.7 · even lattice |
| `icosian_ring_is_E8` | 6.7 · rank 8 + even + unimodular = E8 |
| `emb_is_an_isometry` | 6.8 · M·Mᵀ = 2G |
| `emb_is_nonsingular` | 6.8 · det = −256 |
| `emb_rows_lie_in_L` | 6.8 · every row in doubled D8+ |

## Two Lean-mechanics notes, both learned the hard way and carried from maths 4

- **The determinant is a Laplace expansion with explicit fuel** (`detM`), not an
  `Id.run do` loop. Well-founded recursion and monadic loops do not reduce in the
  kernel — `decide` fails and `Quot.sound` creeps in. Structural recursion on `Nat`
  reduces fine.
- **The theorems use the Bool idiom `(x == y) = true`, not propositional `x = y`.**
  The Bool `==` evaluates to a single Bool the kernel reduces directly; propositional
  `Int` equality goes through a heavier `Decidable` instance tree and times out on the
  8×8. `set_option maxHeartbeats 4000000` is still needed for the 8! expansion.
