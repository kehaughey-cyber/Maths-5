import Lake
open Lake DSL

package «maths5» where

-- Container 06 (the carrier / E8) imports nothing -- pure integer arithmetic decided
-- by the kernel, the zero-axiom standard. Later containers that need real numbers or
-- Euclidean geometry will `require mathlib`; this one does not, and must not.
lean_lib Container06 where
