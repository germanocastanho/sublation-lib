# Patterns

The preceding pages describe the types in isolation. This one describes what they are for: folding evidence from several sources, dispatching on the result, moving between this system and the classical one at its boundaries, and the handful of behaviors that will otherwise be discovered the hard way.

# Aggregating Independent Sources

The knowledge-order operations are binary, but both are associative and commutative, so a sequence of observations folds into a single value:

```python
from functools import reduce
from sublation import TruthValue

reports = [
    TruthValue(0.9, 0.0),   # a source strongly in favor
    TruthValue(0.0, 0.7),   # a source against
    TruthValue(0.6, 0.1),   # a third, moderately in favor
]

pooled = reduce(TruthValue.accumulate, reports)   # mu=0.9, lam=0.7
shared = reduce(TruthValue.consensus, reports)    # mu=0.0, lam=0.0
```

The two folds answer different questions about the same testimony, and their disagreement is informative rather than a problem to be settled. `accumulate` reports that the strongest case for and the strongest case against are both substantial — the body of evidence is contradictory. `consensus` reports that nothing survives the demand for unanimous warrant — on what all three sources jointly support, the question is indeterminate. A classical aggregation would have to choose one summary and suppress the other:

```python
pooled.is_contradictory()    # True  — taken together, the sources conflict
shared.is_indeterminate()    # True  — they agree on nothing
```

### Order and Repetition Do Not Matter

Both operations are idempotent as well as associative and commutative, which gives the fold two properties worth relying on. Sources may arrive in any order without changing the result, and the same source counted twice contributes exactly what it contributed once. Deduplicating a stream of observations before folding is therefore unnecessary, and a retry that replays an observation is harmless.

# Exhaustive Dispatch

Because the four predicates partition the unit square at any fixed threshold, a classification needs no fallback branch — the final case is reached exactly when the first three fail:

```python
def classify(value: TruthValue) -> str:
    if value.is_true():
        return "true"
    if value.is_false():
        return "false"
    if value.is_contradictory():
        return "contradictory"
    return "indeterminate"
```

Where only some distinctions matter, test for them directly rather than reconstructing them from a bool. The two states worth handling explicitly are usually contradiction, which calls for adjudication, and indeterminacy, which calls for more evidence — they are failures of different kinds, and the point of the library is that they are told apart.

# Entering the Dialectical Layer

`Thesis` and `Antithesis` accept a bool or a continuous degree. A bool infers its classical complement; a float infers nothing, entering as one degree with the other left at `0.0`. Passing both degrees keeps the graded evidence intact end to end:

```python
from sublation import Antithesis, Synthesis, Thesis

def round_from(evidence_for, evidence_against):
    thesis = Thesis(evidence_for)
    antithesis = Antithesis(evidence_against)
    return Synthesis(thesis, antithesis)

round_from(0.9, 0.8).contradiction()    # True
round_from(0.2, 0.1).sublation()        # False — not enough either way
```

`Synthesis` projects `mu` from the thesis and `lam` from the antithesis, so feeding each side its own continuous degree carries the gradation all the way through, and `0.9` and `0.51` no longer collapse to the same thesis. Only thresholding — the bool path, or `evidence >= threshold` at the boundary — quantizes the degrees; where that gradation carries information, keep the floats. The dialectical vocabulary remains a reading of the value, so `TruthValue` and its predicates are always available directly.

# Leaving the System

At some boundary a plain bool is usually required. `to_bool` produces one from any value, but it answers the relative question `mu > lam` and so reports an answer even where none is warranted. Deciding what the non-classical states should become is better done explicitly than delegated:

```python
value = TruthValue(0.25, 0.0)

value.to_bool()                              # True — thin evidence, still true
value.is_true()                              # False
value.is_true() or value.is_contradictory()  # False — an explicit policy
```

Whether an unexamined proposition leaves the system as `False`, or a contradictory one as `True`, is a decision about the surrounding application. The library declines to make it, and code that reaches for `to_bool` has usually made it by accident.

# Caveats

### Values Are Not Frozen

`mu` and `lam` are ordinary attributes, and the constructor is the only place they are validated. Assigning to them afterwards bypasses the range check entirely:

```python
value = TruthValue(0.9, 0.1)
value.lam = 5.0           # accepted; no error is raised
```

Treat values as immutable once built. Every operation returns a new instance, so there is never a reason to assign to a degree, and doing so can produce a value the constructor would have rejected.

### Operations Never Mutate Their Operands

The four combining operations and `invert` all return new values and leave both operands untouched. A value may be folded into several aggregations, or held as a reference point across a computation, without defensive copying.

### There Is No Equality or Representation

`TruthValue` defines neither `__eq__` nor `__repr__` at this version, so `==` compares identity and printing yields the default object representation. Compare degrees as a tuple, and format explicitly for output:

```python
a, b = TruthValue(1.0, 0.0), TruthValue(1.0, 0.0)

(a.mu, a.lam) == (b.mu, b.lam)     # True — equality of evidence
f"mu={a.mu}, lam={a.lam}"          # 'mu=1.0, lam=0.0'
```

This affects tests most directly: assert on the degrees or on the verdicts, never on the values themselves.

### The Threshold Is Not Global

`THRESHOLD` is a default argument, not a setting. Rebinding the name in `sublation.truths` does not change the four predicates, whose defaults were bound at definition, and nothing prevents different call sites from using different standards. Where a non-default threshold is in use, pass it explicitly at every call, or wrap the predicates once and call the wrapper.

```python
STRICT = 0.8

def settled(value: TruthValue) -> bool:
    return not value.is_indeterminate(STRICT)
```
