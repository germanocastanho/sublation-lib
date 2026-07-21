# TODO

## Core
- [x] Decouple `thesis`/`antithesis` so contradiction and indeterminacy are
      actually reachable (fixed tautology bug)
- [x] Implement `Synthesis` deriving from real `Thesis`/`Antithesis` instances
      instead of hardcoded values
- [x] `Synthesis.as_thesis()` to chain dialectical rounds
- [ ] Extract the duplicated `negation` / `contradiction` / `becoming` /
      `sublation` logic (identical across `Thesis`, `Antithesis`, `Synthesis`)
      into a shared base class or mixin
- [ ] Decide the fate of `self.synthesis = None` on `Thesis`/`Antithesis` —
      currently dead, either remove it or give it a purpose (e.g. caching a
      completed round)
- [ ] Implement a *real* rule for `sublation()` beyond simple `or` — right
      now it's the same permissive rule inherited across all three classes
- [ ] Evaluate migrating from plain bool to a Belnap/Eτ-style `TruthValue`
      (continuous μ, λ) once the bool-based core stabilizes

## Validation
- [ ] Validate against classical paradoxes (liar, sorites) and against
      Hegel's own Being/Nothing/Becoming triad
- [ ] Add property-based tests (e.g. Hypothesis) to check invariants across
      random thesis/antithesis combinations, not just the hand-picked cases
      in `test_core.py`

## Docs
- [ ] Decide and document the interpretive reading adopted (Priest vs.
      Bordignon)
- [x] Close out CHANGELOG.md `[0.1.0]` with the real release date

## Release
- [x] Decide supported Python range — 3.12–3.14
- [x] Green CI on 3.12–3.14
- [x] Publish 0.1.0 to PyPI (2026-07-17) via `uv build` + `uv publish`
- [ ] Bump version for the next development cycle
- [ ] Split `operators.py` out of `core.py` once the truth-value domain grows