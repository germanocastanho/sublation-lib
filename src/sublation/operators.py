from .truths import TruthValue


def conjunction(self, other: "TruthValue") -> "TruthValue":
    """
    Combines two values as logical AND: only as favorably evidenced as the weaker half (min of the two mu), and only as free of doubt as the most doubted half (max of the two lam).
    """

    return TruthValue(
        min(self.mu, other.mu),
        max(self.lam, other.lam),
    )


def disjunction(self, other: "TruthValue") -> "TruthValue":
    """
    The mirror of conjunction: OR takes the stronger mu and the milder lam, since a disjunction only needs one side to hold up.
    """

    return TruthValue(
        max(self.mu, other.mu),
        min(self.lam, other.lam),
    )


def implication(self, other: "TruthValue") -> "TruthValue":
    """
    Material implication in FDE: ¬A ∨ B, i.e. disjunction(self.invert(), other).
    """

    return self.invert().disjunction(other)


def equivalence(self, other: "TruthValue") -> "TruthValue":
    """
    Logical equivalence in FDE: (A → B) ∧ (B → A).
    """

    return self.implication(other).conjunction(other.implication(self))


def consensus(self, other: "TruthValue") -> "TruthValue":
    """
    Keeps only the evidence both operands agree on (min mu, min lam) - a skeptical combination where anything one side claims but the other doesn't corroborate gets dropped.
    """

    return TruthValue(
        min(self.mu, other.mu),
        min(self.lam, other.lam),
    )


def accumulate(self, other: "TruthValue") -> "TruthValue":
    """
    Pools all evidence from both operands, FOR and AGAINST alike (max mu, max lam), without discarding anything either side claims.
    """

    return TruthValue(
        max(self.mu, other.mu),
        max(self.lam, other.lam),
    )


TruthValue.conjunction = conjunction
TruthValue.disjunction = disjunction
TruthValue.implication = implication
TruthValue.equivalence = equivalence
TruthValue.consensus = consensus
TruthValue.accumulate = accumulate
