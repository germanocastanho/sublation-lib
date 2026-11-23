# TODO

## Core

- [x] Decouple `thesis`/`antithesis` so contradiction and indeterminacy are
      actually reachable (fixed tautology bug)
- [x] Implement `Synthesis` deriving from real `Thesis`/`Antithesis` instances
      instead of hardcoded values
- [x] `Synthesis.as_thesis()` to chain dialectical rounds
- [ ] `Synthesis.as_antithesis()` to chain dialectical rounds in the negative direction
- [x] Extract the duplicated `negation` / `contradiction` / `becoming` / `sublation` logic into a shared base class (`Dialectical`)
- [x] Resolve the dead `self.synthesis = None` attribute on `Thesis`/`Antithesis` (removed)
- [x] Implement a real rule for `sublation()`, grounded in `TruthValue.is_indeterminate()`
- [x] Migrate from plain bool to a Belnap/Eτ-style `TruthValue` (`sublation.truths`)
- [x] Decide whether `Synthesis` should offer an alternate constructor using `TruthValue.accumulate()` — **no**: projection (thesis gives `mu`, antithesis gives `lam`) avoids the spurious contradiction from two "quiet" inputs that `accumulate` produces via the default-inferred complement; explicit pooling stays available on `TruthValue.accumulate()`. Rationale documented in `docs/dialectics.md` ("Why Not Accumulate")
- [x] Expose continuous `mu`/`lam` construction on `Thesis`/`Antithesis` (currently bool-only) once the sorites test below actually needs it
- [x] `as_thesis()` currently round-trips through bool, losing any intermediate certainty — revisit once continuous input exists
- [ ] Corner constructors on `TruthValue`: `true()`, `false()`, `contradictory()`, `indeterminate()` classmethods for readable call sites
- [ ] Pythonic dunders on `TruthValue`: `__invert__` (`~`), `__and__` (`&`), `__or__` (`|`) delegating to `invert`/`conjunction`/`disjunction`

## Validation

- [x] Validate against classical paradoxes (liar, sorites) and against Hegel's own Being/Nothing/Becoming triad — sorites specifically blocked on continuous `mu`/`lam` input, see above
- [x] Add property-based tests (e.g. Hypothesis) to check invariants across random thesis/antithesis combinations, not just the hand-picked cases in `test_core.py`
- [ ] Property-based tests (Hypothesis) on the dialectical layer: `Thesis`/`Antithesis`/`Synthesis` invariants — projection preserves degrees, `as_thesis()` round-trip, thesis/antithesis duality
- [ ] Validate the truthteller ("this sentence is true") as the negation fixed point at the true corner

## Docs

- [x] Decide the interpretive reading adopted (Priest vs. Bordignon)
- [x] Close out CHANGELOG.md `[0.1.0]` with the real release date
- [x] Document `TruthValue`/`truths` in README and CHANGELOG `[Unreleased]`
- [ ] Fix `docs/truth-values.md`: it claims `TruthValue` defines neither `__eq__` nor `__repr__` — both exist; correct the caveats section
- [ ] Add an API reference page listing every public method with its signature

## Tooling

- [x] Migrate the project to `uv init --bare` (pyproject.toml, replacing `setup.py`/`setup.cfg`/`requirements.txt`) — own isolated commit, after this round lands
- [ ] Add `ruff` config to `pyproject.toml` (line length 88, rule set) and run `ruff check` / `ruff format` in CI

## Release

- [x] Decide supported Python range — 3.12–3.14
- [x] Green CI on 3.12–3.14
- [x] Publish 0.1.0 to PyPI (2026-07-17) via `uv build` + `uv publish`
- [x] Publish 0.3.0 to PyPI (2026-08-17) via `uv build` + `uv publish`
- [x] Publish 0.3.1 to PyPI (2026-08-17) via `uv build` + `uv publish`
- [x] Bump version for the next development cycle (`0.2.0`, given the observable `negation()` behavior change)
- [x] Split `operators.py` out of `truths.py` once the truth-value domain grows further — done (commit e17a277)
- [ ] Bump version for the next development cycle (`0.4.0`)
