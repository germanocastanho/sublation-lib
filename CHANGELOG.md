# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]
### Added
- Initial package skeleton: `Thesis`, `Antithesis`, `Synthesis`.
- `Synthesis.as_thesis()` to chain dialectical rounds.

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