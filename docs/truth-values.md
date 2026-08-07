# Truth Values

`TruthValue` is the library's foundation: every dialectical class documented in [Dialectics](dialectics.md) is a reading of one. It holds two independent degrees of evidence and provides six operations over them — four that combine values, one that negates, and a family of predicates that interrogate. This page treats the type on its own terms, without reference to the dialectical vocabulary built on top of it.

# Construction

A value is built from its two degrees. Both are required, because neither can be inferred from the other:

```python
from sublation import TruthValue

value = TruthValue(mu=0.8, lam=0.3)
value.mu   # 0.8
value.lam  # 0.3
```

The degrees are ordinary attributes, and the constructor is the only place where they are checked. Each must fall within `[0.0, 1.0]`, and a violation raises immediately rather than producing a value that misbehaves at some later point:

```python
TruthValue(mu=1.5, lam=0.0)   # ValueError: mu must be within [0.0, 1.0]
TruthValue(mu=0.0, lam=-0.1)  # ValueError: lam must be within [0.0, 1.0]
```

### Lifting a Bool

Classical input enters the system through a helper that lands on one of the two classical corners:

```python
from sublation.truths import truth_value_from_bool

affirmed = truth_value_from_bool(True)    # mu=1.0, lam=0.0
denied = truth_value_from_bool(False)     # mu=0.0, lam=1.0
```

The lifting is total but not surjective: every bool becomes a `TruthValue`, while the contradictory and indeterminate corners are unreachable from a bool. This asymmetry is the formal statement of what the library adds — the two extra states have no classical preimage, so they can only arise from evidence gathered as such, or from operations that produce them.

# The Two Orders

The four values do not sit on a single scale. They are organized by two distinct partial orders, and the resulting structure is a bilattice: a set that is a lattice twice over, under two different notions of "greater". The library exposes the meet and join of each.

### The Truth Order

The first order asks how *true* a value is. Under it, false is lowest, true is highest, and the contradictory and indeterminate values sit incomparably between them — neither is truer than the other. Its meet and join are the familiar connectives:

```python
strong = TruthValue(0.9, 0.1)
weak = TruthValue(0.3, 0.6)

conj = strong.conjunction(weak)  # mu=0.3, lam=0.6
disj = strong.disjunction(weak)  # mu=0.9, lam=0.1
```

`conjunction` takes the smaller `mu` and the larger `lam`. The reading is direct: a conjunction is supported only as far as its weaker conjunct is supported, and is opposed as far as its more contested conjunct is opposed. `disjunction` mirrors it exactly, taking the larger `mu` and the smaller `lam`, since a disjunction needs only one side to hold. Both reduce to their classical counterparts on the classical corners, and both extend them coherently everywhere else.

### The Knowledge Order

The second order asks how *much is known*, irrespective of direction. Under it, the indeterminate value is lowest — nothing has been established — and the contradictory value is highest, since it carries evidence on both sides at once. True and false sit incomparably between: each is one determinate claim, and neither knows more than the other.

```python
a = TruthValue(0.9, 0.4)
b = TruthValue(0.3, 0.7)

cons = a.consensus(b)    # mu=0.3, lam=0.4
accu = a.accumulate(b)   # mu=0.9, lam=0.7
```

`consensus` takes the smaller of *both* degrees, retaining only what the two operands jointly warrant; anything one asserts without corroboration from the other is discarded. It is the skeptical combination, and it is how independent sources are reconciled when only their agreement counts. `accumulate` takes the larger of both, pooling every claim either side advances, for and against alike. It is the credulous combination — Belnap's *gullibility* — and it is how evidence is gathered when nothing is to be thrown away.

##### The Asymmetry Worth Noticing

`accumulate` can manufacture contradiction out of two non-contradictory operands, and `consensus` can manufacture indeterminacy out of two determinate ones. This is not a defect but the substance of the knowledge order: pooling a strong case for with a strong case against yields a value that registers the conflict rather than resolving it, and demanding joint warrant from a claim and its denial leaves nothing standing.

```python
supported = TruthValue(1.0, 0.0)
opposed = TruthValue(0.0, 1.0)

supported.accumulate(opposed).is_contradictory()  # True
supported.consensus(opposed).is_indeterminate()   # True
```

##### Why Minima and Maxima

All four operations are defined by `min` and `max` rather than by arithmetic on the degrees. Averaging or summing would let quantity of evidence substitute for its direction, so that abundant weak support could outweigh decisive opposition, and it would destroy the lattice structure — the operations would cease to be idempotent, and repeating an observation would change the result. As defined, all four are idempotent, commutative and associative, so a value combined with itself is unchanged and the order in which sources are folded together does not matter.

# Negation

`invert` swaps the two degrees. What argued for now argues against:

```python
TruthValue(0.8, 0.2).invert()  # mu=0.2, lam=0.8
```

Three properties follow, and together they characterize the operation as a De Morgan negation on the bilattice. It is involutive, so negating twice restores the original value. It exchanges the truth-order connectives, satisfying De Morgan's laws: the negation of a conjunction is the disjunction of the negations, and conversely. And it leaves the knowledge-order operations untouched, commuting with both `consensus` and `accumulate` — negation reverses direction without adding or removing evidence.

```python
a, b = TruthValue(0.9, 0.1), TruthValue(0.3, 0.6)

a.conjunction(b).invert()             # equals
a.invert().disjunction(b.invert())    # this

a.accumulate(b).invert()              # equals
a.invert().accumulate(b.invert())     # this
```

The two non-classical corners are fixed points. Inverting `(1.0, 1.0)` or `(0.0, 0.0)` returns the same value, which is correct: the denial of a contradiction is still contradictory, and the denial of something wholly unexamined remains unexamined. Classical negation has no fixed point, and its absence is precisely what forces bivalence.

# Reading a Value

Combining values produces values. Extracting a verdict requires comparing the degrees against a standard of evidence.

### The Four Predicates

Each predicate tests one quadrant of the unit square:

```python
value = TruthValue(0.9, 0.1)

value.is_true()            # True  — mu over, lam under
value.is_false()           # False
value.is_contradictory()   # False — would need both over
value.is_indeterminate()   # False — would need both under
```

`is_true` holds when `mu` has reached the threshold and `lam` has not; `is_false` is its mirror; `is_contradictory` holds when both have reached it; `is_indeterminate` when neither has. For any fixed threshold these four cases are exhaustive and mutually exclusive, so exactly one predicate holds for any value. An `if`/`elif` chain over all four therefore needs no fallback branch, and any two of them are enough to distinguish the pair a program actually cares about.

### Choosing a Threshold

The default is `0.5`, exported as `THRESHOLD`, but every predicate accepts an override. The threshold is a decision about the standard of evidence, not a constant of the logic, and moving it can move a value between quadrants:

```python
from sublation.truths import THRESHOLD

value = TruthValue(0.6, 0.2)

value.is_true()                  # True  — default threshold of 0.5
value.is_true(threshold=0.8)     # False — a stricter standard
value.is_indeterminate(0.8)      # True  — under it, nothing is settled
```

Raising the threshold makes indeterminacy easier to reach and contradiction harder; lowering it does the reverse. Nothing enforces that a single threshold be used consistently across a program, so a value that reads as true in one place may read as indeterminate in another. Where this matters, fix the threshold once and pass it explicitly.

### Collapsing to a Bool

`to_bool` answers a different question from `is_true`, and confusing the two is the most likely source of error in using this type:

```python
value = TruthValue(0.25, 0.0)

value.to_bool()            # True  — mu exceeds lam
value.is_true()            # False — mu never reached the threshold
value.is_indeterminate()   # True  — the honest reading
```

`to_bool` is a *relative* comparison, `mu > lam`, and always returns an answer because one degree is always at least as large as the other. `is_true` is an *absolute* test against a threshold, and refuses to answer affirmatively when the evidence is thin. The divergence runs in both directions: a value can be `to_bool` true while indeterminate, as above, or while contradictory, as in `TruthValue(1.0, 0.5)`. Use `to_bool` only at the boundary where a bool must be produced regardless — and understand that it discards exactly the information the type exists to carry.

# Comparing Values

`TruthValue` defines neither `__eq__` nor `__repr__` at this version. Two values with identical degrees are therefore unequal under `==`, which compares identity, and printing one yields the default object representation:

```python
TruthValue(1.0, 0.0) == TruthValue(1.0, 0.0)  # False
```

Compare the degrees directly, or compare the verdicts, depending on which question is being asked:

```python
a, b = TruthValue(1.0, 0.0), TruthValue(1.0, 0.0)

(a.mu, a.lam) == (b.mu, b.lam)   # True — same evidence
a.is_true() == b.is_true()       # True — same verdict
```

The two are not interchangeable. Distinct degrees frequently yield the same verdict, since each predicate covers a whole quadrant, so equality of verdicts is the weaker claim.
