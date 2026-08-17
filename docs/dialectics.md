# Dialectics

`Thesis`, `Antithesis` and `Synthesis` are the dialectical layer. Each wraps a single [`TruthValue`](truth-values.md) and exposes four methods that name its states in Hegelian rather than evidential vocabulary. The layer adds no logical power — every question it answers could be put directly to the underlying value — but it fixes an interpretation, and it supplies the one operation the truth-value layer has no notion of: passing a resolved position into a further round.

# The Shared Base

All three classes derive from `Dialectical`, which holds no state of its own. Each subclass is responsible for populating three fields in its `__init__`, and the four inherited methods read those fields identically regardless of which subclass produced them:

```python
value: TruthValue   # the evidential state
thesis: bool        # whether mu reached the threshold
antithesis: bool    # whether lam reached the threshold
```

The `thesis` and `antithesis` attributes are thresholded readings of the two degrees, retained as a convenience and as the interface through which rounds are chained. They are derived, never authoritative: `value` is what the methods consult. `Dialectical` is not usable on its own — the three fields are annotations without defaults, so instantiating it directly and calling a method raises `AttributeError`. It is a shared implementation, not an abstract interface, and not an extension point at this version.

# Thesis

A thesis is a proposition asserted as posited. Asserting it ordinarily denies its antithesis, and the constructor performs that inference when the second argument is omitted:

```python
from sublation import Thesis

posited = Thesis(True)          # mu=1.0, lam=0.0
denied = Thesis(False)          # mu=0.0, lam=1.0
```

### Overriding the Inference

The inferred complement is a default, not a law, and it belongs to the bool path alone. Supplying `antithesis` explicitly breaks the classical linkage, one way to reach the two non-classical corners from a `Thesis`:

```python
contested = Thesis(True, True)    # mu=1.0, lam=1.0 — both asserted
unexamined = Thesis(False, False) # mu=0.0, lam=0.0 — neither asserted

contested.contradiction()         # True
unexamined.sublation()            # False — nothing has been settled
```

That a single library call decides between the classical and the non-classical reading is the practical content of the whole design. `Thesis(True)` and `Thesis(True, True)` agree on the evidence for and differ on the evidence against; classical logic cannot express the difference, because it derives the second from the first.

### Continuous Degrees

A degree may also be a float in `[0.0, 1.0]`, and then the interior of the square becomes reachable, not only its corners. A continuous thesis infers *no* complement — asserting evidence for a proposition says nothing about the evidence against it, which is the independence the whole library rests on:

```python
graded = Thesis(0.7)          # mu=0.7, lam=0.0 — nothing asserted against
both = Thesis(0.7, 0.2)       # mu=0.7, lam=0.2 — each degree given verbatim
```

The bool `False` and the float `0.0` therefore diverge, and the divergence is the point: `Thesis(False)` denies the proposition (`mu=0.0, lam=1.0`), while `Thesis(0.0)` merely declines to support it (`mu=0.0, lam=0.0`) and stays indeterminate. Only the bool carries the classical inference; the float carries only what it states.

# Antithesis

An antithesis is a proposition asserted as the negation of a thesis, and it mirrors `Thesis` exactly — including the inference, running in the opposite direction:

```python
from sublation import Antithesis

asserted = Antithesis(True)     # mu=0.0, lam=1.0
withheld = Antithesis(False)    # mu=1.0, lam=0.0
```

### The Asymmetry of the Signatures

The first positional parameter of `Thesis` is `thesis`; the first positional parameter of `Antithesis` is `antithesis`. Each class leads with the proposition it names, so the same positional argument means opposite things in the two constructors, and `Thesis(True)` and `Antithesis(True)` denote contrary positions.

One consequence is worth stating plainly, because it surprises on first encounter:

```python
Thesis().thesis, Thesis().antithesis          # (True, False)
Antithesis().thesis, Antithesis().antithesis  # (True, False) — identical
```

A bare `Antithesis()` defaults its own proposition to `False` — the antithesis is *not* asserted — and the inferred complement then affirms the thesis, producing the same value a bare `Thesis()` produces. The default constructor of `Antithesis` therefore does not represent an antithesis at all. This is deliberate signature compatibility with 0.1.0, pinned by the test suite; construct antitheses explicitly rather than relying on the default.

# Synthesis

A synthesis is built from an actual thesis and an actual antithesis, and it reads each side only on that side's own claim:

```python
from sublation import Synthesis

s = Synthesis(Thesis(True), Antithesis(True))
s.value.mu, s.value.lam   # (1.0, 1.0)
```

### Projection, Not Pooling

`Synthesis` takes `mu` from the thesis and `lam` from the antithesis, and discards the other degree of each. The thesis is trusted about what speaks for the proposition; the antithesis is trusted about what speaks against it; neither is consulted about the other's business. A consequence is that the inferred complement described above is *invisible* to `Synthesis` — the two constructions below yield the same synthesis, because the extra `lam` carried by the second thesis is discarded either way:

```python
a = Synthesis(Thesis(True), Antithesis(True))
b = Synthesis(Thesis(True, True), Antithesis(True))

(a.value.mu, a.value.lam) == (b.value.mu, b.value.lam)   # True
```

The inference therefore matters when a `Thesis` is interrogated on its own, and not when it is fed into a synthesis. Both facts are easy to forget in the other's presence.

##### Why Not Accumulate

Pooling both sides with `accumulate` would be the obvious alternative, and it is wrong here. Because each constructor infers a complement, two *quietly negative* inputs already carry a full claim each, in opposite directions, and pooling them manufactures a contradiction out of two positions that assert nothing:

```python
t, a = Thesis(False), Antithesis(False)

t.value.accumulate(a.value).is_contradictory()   # True — spurious
Synthesis(t, a).value.is_indeterminate()         # True — the honest reading
```

Projection avoids this by never letting an inferred degree cross into the synthesis. An alternative constructor built on `accumulate` remains an open question in `TODO.md`, deferred for exactly this reason.

### The Four Corners

Because the projection reads one degree from each side, the four bool combinations map onto the four states exactly, with no redundancy and no gaps:

```python
Synthesis(Thesis(True), Antithesis(True))    # (1.0, 1.0) contradictory
Synthesis(Thesis(True), Antithesis(False))   # (1.0, 0.0) true
Synthesis(Thesis(False), Antithesis(True))   # (0.0, 1.0) false
Synthesis(Thesis(False), Antithesis(False))  # (0.0, 0.0) indeterminate
```

The last of these is the case classical logic cannot state. A thesis that is not asserted, met by an antithesis that is not asserted either, leaves the question open — it does not, as bivalence would have it, settle it by default.

##### The Synthesis Attribute

`Synthesis` sets one further attribute at construction, `synthesis`, holding the result of `sublation()` at that moment. It is a snapshot rather than a live property, and since the degrees are fixed at construction, it agrees with a later call to `sublation()`.

# The Four Methods

Every dialectical object answers the same four questions. Each delegates to a predicate on the underlying value:

```python
s = Synthesis(Thesis(True), Antithesis(True))

s.negation()        # False — does the denial hold cleanly?
s.contradiction()   # True  — do both sides hold at once?
s.becoming()        # False — is this a clean, uncontested affirmation?
s.sublation()       # True  — has the question been settled either way?
```

`becoming` is `is_true` on the underlying value: the moment at which a position stands affirmed without contest. `contradiction` is `is_contradictory`, the state that motivates the library, and the one a bool cannot hold. `negation` inverts the value and asks whether the result is cleanly true, which is exactly equivalent to asking whether the original is false — evidence against has carried, evidence for has not. `sublation` renders *Aufhebung*: it holds when the value is no longer indeterminate, that is, when it has been determined in some direction, whether by affirmation, by denial, or by standing contradiction.

That last disjunction is the substantive claim of the layer. A contradiction counts as sublated. The tension is not an absence of result to be resolved away, but a determinate outcome in its own right — which is why `contradiction()` and `sublation()` are both true of the first corner above, and why only the wholly unexamined value fails to be sublated.

##### The Threshold Is Fixed Here

The four methods call their predicates without a threshold argument, so they always test against the default of `0.5`. With continuous construction a degree can now land anywhere in `[0.0, 1.0]`, so a value built from floats near the threshold reads differently under a stricter standard than these methods apply. Where a different standard of evidence is required, work directly with the underlying `TruthValue` and pass the threshold explicitly.

# Chaining Rounds

A synthesis is not a terminus. `as_thesis` re-posits it as the thesis of a further round, which is the sense in which the process continues rather than concludes:

```python
first = Synthesis(Thesis(True), Antithesis(False))
second = Synthesis(first.as_thesis(), Antithesis(True))

second.contradiction()   # True — the new antithesis contests the position
```

`as_thesis` reconstructs from the synthesis's own `mu` and `lam`, passing both degrees explicitly so the inferred complement never intervenes and no thresholding occurs. The resulting thesis carries the exact degrees of the synthesis it came from — the four corners as before, and now any interior value as well, so intermediate certainty survives the chaining. Re-positing changes the role a value plays, never the value itself.

Two corners are consequently stable under repetition. A contradictory synthesis re-posited against an antithesis that contests it stays contradictory, and an indeterminate one met with nothing new stays indeterminate. Movement requires a new antithesis bringing evidence the previous round did not have — the library supplies the structure of the rounds, not their content.
