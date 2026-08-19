/-
  CONTAINER 06 - THE CARRIER . the icosian ring is E8

  GENERATED FROM derivation.json BY check/gen_lean.py. DO NOT EDIT BY HAND --
  every literal below is emitted from the derivation, so there is exactly one
  home for each formula. `python3 gen_lean.py --check` fails if this file and
  the derivation disagree.

  Imports nothing: no Mathlib, no other container. Pure integer arithmetic
  decided by the kernel.

  THE CRITERIA, from the derivation's own `why` fields:
    6.5  a Z-basis of the icosian ring
          expr: HNF( { 2q, 2*phi*q : q in the 120 } )
          determines: UNIQUE
    6.6  the codifferent form
          expr: B(x,y) = Tr(delta <x,y>), delta = phi/sqrt5; on doubled coordinates this is sum_k (m m' + m n' + n m' + 2 n n')
          determines: UNIQUE
    6.7  the Gram of the icosian ring, and its invariants
          expr: G = [B(b_i, b_j)] ; halfGram = G/2
          determines: UNIQUE
    6.8  the isometry onto the textbook E8
          expr: integer M with M M^T = 2G AND every row in L = {y in Z^8 : coordinates of one parity, sum = 0 mod 4}
          determines: UNIQUE UP TO Aut(L)
-/

-- 8x8 Laplace expansion is 8! leaf terms; the kernel needs the raised budget,
-- exactly as maths 4 (Closure/IcosianE8.lean:84) set for the same determinant.
set_option maxHeartbeats 4000000

namespace Container06

abbrev V8 := List Int

def dotp (u v : V8) : Int := (List.zipWith (fun a b => a * b) u v).foldl (· + ·) 0

/-- The codifferent form B(x,y) = Tr(delta <x,y>), delta = phi/sqrt5, on doubled
    Z[phi] coordinates. Step 6.6; see the header for why delta must be totally
    positive. -/
def qForm (x y : V8) : Int :=
  let f : Nat → Int := fun k =>
    let m := x.getD (2*k) 0; let n := x.getD (2*k+1) 0
    let m' := y.getD (2*k) 0; let n' := y.getD (2*k+1) 0
    m*m' + m*n' + n*m' + 2*n*n'
  f 0 + f 1 + f 2 + f 3

/-- Step 6.5. The HNF of the Z-span of {2q, 2*phi*q : q in the 120}. HNF is
    canonical, so this basis is UNIQUE -- not 'a basis obtained by row reduction'. -/
def icosianBasis : List V8 :=
  [[1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 1, 1, 0, 1, -1, 0],
    [0, 0, 0, 1, 1, 0, 1, -1],
    [0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 2]]

def gramOf (m : List V8) (f : V8 → V8 → Int) : List (List Int) :=
  m.map (fun a => m.map (fun b => f a b))

/-- Step 6.7. -/
def icosianGram : List (List Int) := gramOf icosianBasis qForm

def halfGram : List (List Int) :=
  [[2, 2, 1, 1, 1, 1, 1, 1],
    [2, 4, 2, 1, 1, 2, 1, 2],
    [1, 2, 4, 2, 1, 2, -1, -1],
    [1, 1, 2, 2, 1, 1, 0, -1],
    [1, 1, 1, 1, 2, 2, 0, 0],
    [1, 2, 2, 1, 2, 4, 0, 0],
    [1, 1, -1, 0, 0, 0, 2, 2],
    [1, 2, -1, -1, 0, 0, 2, 4]]

/-- Delete the n-th entry of a row. -/
def delNth : Nat → List Int → List Int
  | _, [] => []
  | 0, _ :: xs => xs
  | n+1, x :: xs => x :: delNth n xs

/-- Determinant by Laplace expansion with explicit fuel. Structural recursion on
    Nat reduces under `decide`; an Id.run do loop or well-founded recursion does
    not, and drags in Quot.sound. maths 4's pattern, carried verbatim. -/
def detM : Nat → List (List Int) → Int
  | 0, _ => 1
  | _, [] => 1
  | f+1, r :: rs =>
      (((List.range r.length).zip r).foldl
        (fun acc p =>
          acc + (if p.1 % 2 == 0 then (1 : Int) else -1) * p.2 *
                detM f (rs.map (delNth p.1)))
        0)

def detOf (m : List (List Int)) : Int := detM m.length m

/-! ### the invariants that ARE the identification -/

theorem gram_determinant_is_256 : (detOf icosianGram == 256) = true := by decide

theorem gram_entries_all_even :
    icosianGram.all (fun r => r.all (fun x => x % 2 == 0)) = true := by decide

theorem halfGram_is_the_half :
    (icosianGram.map (fun r => r.map (fun x => x / 2)) == halfGram) = true := by decide

theorem halfGram_is_unimodular : (detOf halfGram == 1) = true := by decide

theorem halfGram_diagonal_is_even :
    (List.range 8).all (fun i => ((halfGram.getD i []).getD i 0) % 2 == 0) = true := by
  decide

/-- Rank 8, even, unimodular, positive definite characterises E8 uniquely. The four
    theorems above are that characterisation; no classification theorem is cited. -/
theorem icosian_ring_is_E8 :
    (icosianBasis.length = 8)
    ∧ ((detOf halfGram == 1) = true)
    ∧ (icosianGram.all (fun r => r.all (fun x => x % 2 == 0)) = true) := by
  refine ⟨by decide, by decide, by decide⟩

/-! ### step 6.8 -- the isometry onto the textbook lattice -/

/-- L = { y : coordinates of one parity, sum y = 0 mod 4 }, the doubled D8+
    presentation of E8. -/
def inL (y : V8) : Bool :=
  ((y.all (fun c => c % 2 == 0)) || (y.all (fun c => c % 2 == 1)))
  && ((y.foldl (· + ·) 0) % 4 == 0)

/-- Step 6.8. Found by search over the criterion, not solved externally.
    DETERMINACY: UNIQUE UP TO Aut(L) -- the criterion fixes the lattice and the
    form, not the frame. -/
def emb : List V8 :=
  [[-2, -2, 0, 0, 0, 0, 0, 0],
    [-3, -1, -1, -1, -1, -1, -1, 1],
    [-3, 1, -1, -1, -1, 1, 1, -1],
    [-2, 0, 0, 0, 0, 0, 0, -2],
    [-2, 0, 0, 0, 2, 0, 0, 0],
    [-3, 1, -1, 1, 1, -1, 1, 1],
    [0, -2, 0, 0, 0, -2, 0, 0],
    [0, -2, 0, -2, 0, -2, 0, 2]]

def twice (m : List (List Int)) : List (List Int) := m.map (fun r => r.map (fun x => 2 * x))

theorem emb_is_an_isometry :
    (gramOf emb dotp == twice icosianGram) = true := by decide

theorem emb_is_nonsingular : (detOf emb == -256) = true := by decide

theorem emb_rows_lie_in_L : emb.all inL = true := by decide

end Container06
