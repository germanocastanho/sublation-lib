# Documentation

This directory documents the `sublation` library in depth. The README states what the library is; these pages state how it behaves, why it behaves that way, and where its edges are. Read this page first — it establishes the evidential frame that every other page presupposes.

# Contents

- [Truth Values](truth-values.md) — the `TruthValue` type, the bilattice operators, the threshold predicates.
- [Dialectics](dialectics.md) — `Thesis`, `Antithesis`, `Synthesis`, and the four dialectical methods.
- [Patterns](patterns.md) — composite usage, chaining, and the caveats worth knowing before relying on the library.

# The Evidential Frame

Classical logic assigns a proposition exactly one of two values, and derives one from the other: asserting `p` denies `¬p`. That derivation is not a discovery about the world but a structural commitment of the formalism, and it makes two ordinary epistemic situations inexpressible. A proposition supported by conflicting evidence cannot be recorded as such — it must be forced to one side. A proposition on which no evidence has yet been gathered is likewise forced, since bivalence admits no third option.

The library replaces the single truth value with a pair of independent degrees. `mu` measures evidence *for* a proposition; `lam` measures evidence *against* it. Neither is computed from the other. Both range over `[0.0, 1.0]`, and values outside that interval raise `ValueError` at construction rather than propagating silently:

```python
from sublation import TruthValue

supported = TruthValue(mu=1.0, lam=0.0)
opposed = TruthValue(mu=0.0, lam=1.0)
contested = TruthValue(mu=1.0, lam=1.0)
unexamined = TruthValue(mu=0.0, lam=0.0)
```

Because the two degrees vary independently, the pair spans four extremal states rather than two. These are the four values of Belnap–Dunn logic (FDE): true, false, both, and neither. The interior of the square — every pair that is not a corner — is the paraconsistent annotated generalization, in the manner of Eτ, where evidence is graded rather than merely present or absent.

### Independence Is the Whole Point

The decisive property is that `lam` is not `1 - mu`. Under that constraint the pair would collapse back into a single degree and reproduce fuzzy logic, where contradiction and ignorance are again inexpressible: both would map to `0.5`. Keeping the degrees independent is what distinguishes "the evidence is evenly split and abundant" from "there is no evidence at all", two states that a single number cannot separate.

```python
contested.mu + contested.lam    # 2.0 — abundant evidence, pulling both ways
unexamined.mu + unexamined.lam  # 0.0 — no evidence in either direction
```

# Reading a Value

A pair of degrees is a measurement, not yet a verdict. To ask which of the four states a value occupies, the library compares each degree against a threshold, `0.5` by default:

```python
from sublation.truths import THRESHOLD

THRESHOLD  # 0.5

contested.is_contradictory()  # True
unexamined.is_indeterminate() # True
```

Each of the four predicates — `is_true`, `is_false`, `is_contradictory`, `is_indeterminate` — accepts a `threshold` argument, so the standard of evidence is a decision belonging to the caller rather than a constant of the logic. For any fixed threshold the four predicates partition the unit square: exactly one holds for any pair of degrees. There is no gap between them and no overlap, which is what makes them safe to use as an exhaustive case analysis.

# Installation

```bash
pip install sublation
```

The package requires Python 3.12 or later and declares no runtime dependencies. It ships a `py.typed` marker, so type checkers consume its annotations directly.

# Public Surface

```python
from sublation import Antithesis, Synthesis, Thesis, TruthValue
```

Those four names constitute the package's `__all__`. Two further names are importable from the submodule that defines them, and are documented here because they are useful rather than incidental:

```python
from sublation.truths import THRESHOLD, truth_value_from_bool
```

The `Dialectical` base class in `sublation.core` is likewise importable, but it exists to share behavior among the three dialectical classes and is not intended as an extension point at this version.

##### On Version Stability

This documentation describes version 0.2.0, whose development status is Alpha. The four-valued semantics of `TruthValue` are stable. `Thesis` and `Antithesis` now accept continuous degrees as well as bools, and the inferred complement is confined to the bool path — code that constructs `TruthValue` directly, or that passes both degrees explicitly, is on firmer ground than code that depends on the inferred-complement behavior described in [Dialectics](dialectics.md).
