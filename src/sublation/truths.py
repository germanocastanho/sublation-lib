THRESHOLD = 0.5


class TruthValue:
    """
    This class represents a proposition's evidential state as a pair of independent degrees: `mu`, how much evidence favors it, and `lam`, how much evidence opposes it, both ranging from 0.0 to 1.0. The four values are:

    (mu=1.0, lam=0.0) <-> True (bool);
    (mu=0.0, lam=1.0) <-> False (bool);
    (mu=1.0, lam=1.0) <-> Contradiction
    (mu=0.0, lam=0.0) <-> Indeterminacy
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
        """Degree of evidence in favor."""
        return self._mu

    @property
    def lam(self) -> float:
        """Degree of evidence against."""
        return self._lam

    def invert(self) -> "TruthValue":
        """
        Returns this value's negation by swapping the two kinds of evidence: what argued FOR now argues AGAINST, and vice versa.
        """

        truth_value = TruthValue(self.lam, self.mu)
        return truth_value

    def to_bool(self) -> bool:
        """
        Collapses this value to a plain bool by checking which evidence degree is larger — a relative comparison, **not** the same question as `is_true ()` below.
        """

        conversion = self.mu > self.lam
        return conversion

    def __eq__(self, other: object) -> bool:
        """
        Equality of evidence: two values are equal when both degrees match.
        """

        if not isinstance(other, TruthValue):
            return NotImplemented
        return (self.mu, self.lam) == (other.mu, other.lam)

    def __repr__(self) -> str:
        """
        A representation that shows both degrees, useful for debugging and logging.
        """

        return f"TruthValue(mu={self.mu!r}, lam={self.lam!r})"

    @classmethod
    def from_bool(cls, value: bool) -> "TruthValue":
        """
        Lifts a plain bool to a TruthValue on one of the two classical corners.
        Alias for the module-level `truth_value_from_bool` helper.
        """

        return truth_value_from_bool(value)

    def is_true(self, threshold: float = THRESHOLD) -> bool:
        """
        Reports whether this value sits in the "true" corner: evidence FOR has crossed the threshold and evidence AGAINST has not.
        """

        response = (self.mu >= threshold) and (self.lam < threshold)
        return response

    def is_false(self, threshold: float = THRESHOLD) -> bool:
        """
        The mirror of `is_true`: evidence AGAINST has crossed the threshold and evidence FOR has not.
        """

        response = (self.lam >= threshold) and (self.mu < threshold)
        return response

    def is_contradictory(self, threshold: float = THRESHOLD) -> bool:
        """
        Reports whether both evidence FOR and evidence AGAINST have crossed the threshold at once — the state a plain bool can never represent, and the reason TruthValue exists.
        """

        response = (self.mu >= threshold) and (self.lam >= threshold)
        return response

    def is_indeterminate(self, threshold: float = THRESHOLD) -> bool:
        """
        Reports whether neither evidence FOR nor evidence AGAINST has crossed the threshold — "we simply don't know yet", a legitimate state that plain bool forces away.
        """

        response = (self.mu < threshold) and (self.lam < threshold)
        return response


def truth_value_from_bool(value: bool) -> TruthValue:
    """
    Builds a TruthValue from a plain bool, landing on one of the two classical corners. Utility function for convenience, since the constructor requires two evidence degrees and a bool only has one.
    """

    conversion = TruthValue(1.0, 0.0) if value else TruthValue(0.0, 1.0)
    return conversion
