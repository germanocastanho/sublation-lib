# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Continuous construction on `Thesis` and `Antithesis`: both constructors now accept a float degree in `[0.0, 1.0]` alongside a bool, reaching the interior of the evidential square. A bool still infers its classical complement; a float infers none, so `Thesis(0.0)` is indeterminate where `Thesis(False)` is denial.

### Changed

- `Synthesis.as_thesis()` now re-posits from the synthesis's raw `mu`/`lam` instead of the thresholded bools, so intermediate certainty survives a chained round instead of collapsing to a corner.

## [0.2.0] - 2026-08-05

### Added

- `sublation.truths` module: `TruthValue`, an evidence pair (`mu` for, `lam` against) implementing the Belnap–Dunn bilattice, with `invert`, `conjunction`, `disjunction`, `consensus`, `accumulate`, `to_bool`, `is_true`, `is_false`, `is_contradictory`, and `is_indeterminate`.
- `truth_value_from_bool()` helper.
- `Dialectical`, a shared base class for `Thesis`, `Antithesis`, and `Synthesis`, removing the duplicated `negation` / `contradiction` / `becoming` / `sublation` logic.
- Test suite for `TruthValue` covering every operator and the four FDE corners (`tests/test_truths.py`).
- Test covering the corrected `negation()` behavior at full indeterminacy.

### Changed

- `Thesis`, `Antithesis`, and `Synthesis` now store a single `TruthValue` internally instead of two independent raw bools.
- `sublation()` is now grounded in `TruthValue.is_indeterminate()` rather than an unmotivated `or`, though its output is unchanged for all existing use.

### Fixed

- `negation()` at full indeterminacy (`mu=0, lam=0`) now correctly returns `False` instead of `True` — the old bool-only implementation ignored `antithesis` entirely when computing this case.

### Removed

- Dead `self.synthesis = None` placeholder on `Thesis`/`Antithesis` (never read anywhere).

## [0.1.0] - 2026-07-17

### Added

- `Thesis` and `Antithesis`, with decoupled `thesis`/`antithesis` fields so
  contradiction and indeterminacy are reachable states, not tautologically
  excluded.
- `Synthesis`, deriving its state from real `Thesis`/`Antithesis` instances
  instead of hardcoded values.
- `negation()`, `contradiction()`, `becoming()`, `sublation()` on all three
  classes.
- `Synthesis.as_thesis()` to chain successive dialectical rounds.
- Test suite covering signature compatibility, contradiction detection,
  tension-free resolution, and round-chaining.

### Changed

- Supported Python range narrowed to 3.12–3.14.
