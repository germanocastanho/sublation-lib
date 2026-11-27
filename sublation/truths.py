"""
Copyleft 2026, Germano Castanho
Licensed under the MIT License
"""

THRESHOLD = 0.5


class TruthValue:
    """
    Evidential state of a proposition as a pair of independent degrees: `mu`
    (evidence for) and `lam` (evidence against), both in [0.0, 1.0]. The four
    corners are true (1,0), false (0,1), contradictory (1,1), indeterminate
    (0,0).
    """

    def __init__(self, mu: float, lam: float) -> None:
        """
        Builds a TruthValue from its two evidence degrees, both required to
        fall within [0.0, 1.0]. Out-of-range input raises ValueError right
        away, rather than producing a value that misbehaves later.
        """

        if not (0 <= mu <= 1):
            raise ValueError(f"mu must be within [0.0, 1.0], got {mu}")

        if not (0 <= lam <= 1):
            raise ValueError(f"lam must be within [0.0, 1.0], got {lam}")

        self._mu = mu
        self._lam = lam

    @property
    def mu(self) -> float:
        """
        Degree of evidence in favor of the proposition, independent of lam.
        This is the supporting side of the evidential pair. It is never derived
        from lam, and changing one never touches the other; that independence is
        what keeps contradiction and indeterminacy expressible. Read-only after
        construction.
        """

        return self._mu

    @property
    def lam(self) -> float:
        """
        Degree of evidence against the proposition, independent of mu.
        This is the opposing side of the evidential pair. It is never derived
        from mu, and changing one never touches the other; that independence is
        what keeps contradiction and indeterminacy expressible. Read-only after
        construction.
        """

        return self._lam

    def invert(self) -> "TruthValue":
        """
        Returns this value's negation by swapping the two kinds of evidence:
        what argued FOR now argues AGAINST, and vice versa. Involutive by
        construction, so inverting twice restores the original value, and it
        leaves the knowledge-order operations (consensus, accumulate) untouched
        while exchanging the truth-order connectives under De Morgan's laws.
        """

        truth_value = TruthValue(self.lam, self.mu)
        return truth_value

    def to_bool(self) -> bool:
        """
        Collapses this value to a plain bool by checking which evidence degree
        is larger — a relative comparison (mu > lam), not the same question as
        `is_true`. Always returns an answer, but discards exactly the
        information the type exists to carry: thin, thick, or both ways.
        """

        conversion = self.mu > self.lam
        return conversion

    def __eq__(self, other: object) -> bool:
        """
        Equality of evidence: two values are equal when both degrees match.
        Compares the full (mu, lam) pair rather than object identity, so two
        separately constructed values carrying the same evidence compare equal.
        Returns NotImplemented for non-TruthValue operands so Python falls
        back to the other side's comparison.
        """

        if not isinstance(other, TruthValue):
            return NotImplemented
        return (self.mu, self.lam) == (other.mu, other.lam)

    def __repr__(self) -> str:
        """
        A representation that shows both evidence degrees, useful for debugging
        and logging. Renders as TruthValue(mu=..., lam=...), making the pair
        visible at a glance without inspecting attributes individually.
        """

        return f"TruthValue(mu={self.mu!r}, lam={self.lam!r})"

    @classmethod
    def from_bool(cls, value: bool) -> "TruthValue":
        """
        Lifts a plain bool to a TruthValue on one of the two classical corners:
        true -> (1.0, 0.0), false -> (0.0, 1.0). Total but not surjective —
        contradictory and indeterminate have no classical preimage. Alias for
        the module-level `truth_value_from_bool` helper.
        """

        return truth_value_from_bool(value)

    def is_true(self, threshold: float = THRESHOLD) -> bool:
        """
        Reports whether this value sits in the "true" corner: evidence FOR has
        crossed the threshold while evidence AGAINST has not. A value can be
        neither true nor false (indeterminate) or both at once
        (contradictory); this predicate answers only the true question.
        """

        response = (self.mu >= threshold) and (self.lam < threshold)
        return response

    def is_false(self, threshold: float = THRESHOLD) -> bool:
        """
        Reports whether this value sits in the "false" corner: evidence AGAINST
        has crossed the threshold while evidence FOR has not. The mirror of
        `is_true`, so a false reading means the proposition is opposed, not
        merely unsupported (that would be indeterminate).
        """

        response = (self.lam >= threshold) and (self.mu < threshold)
        return response

    def is_contradictory(self, threshold: float = THRESHOLD) -> bool:
        """
        Reports whether both evidence FOR and evidence AGAINST have crossed the
        threshold at once. A plain bool can never represent this state — it
        forces a choice — which is exactly why TruthValue exists: contradiction
        is a legitimate, determinate evidential state, not an error.
        """

        response = (self.mu >= threshold) and (self.lam >= threshold)
        return response

    def is_indeterminate(self, threshold: float = THRESHOLD) -> bool:
        """
        Reports whether neither evidence FOR nor evidence AGAINST has crossed
        the threshold — "we simply don't know yet". A plain bool forces every
        proposition to a side, so it cannot express this state; TruthValue can,
        and indeterminacy is as much a verdict as true or false.
        """

        response = (self.mu < threshold) and (self.lam < threshold)
        return response


def truth_value_from_bool(value: bool) -> TruthValue:
    """
    Builds a TruthValue from a plain bool, landing on one of the two classical
    corners. Convenience helper because the constructor requires two evidence
    degrees while a bool carries only one. The lifted value infers the
    classical complement: asserting true denies false, and vice versa, which is
    exactly the structural commitment TruthValue exists to relax.
    """

    conversion = TruthValue(1.0, 0.0) if value else TruthValue(0.0, 1.0)
    return conversion
