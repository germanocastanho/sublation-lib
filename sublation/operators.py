"""
Copyleft 2026, Germano Castanho
Licensed under the MIT License
"""

from .truths import TruthValue


def conjunction(self, other: "TruthValue") -> "TruthValue":
    """
    Combines two values as logical AND: only as favorably evidenced as the
    weaker half (min mu), and only as free of doubt as the most doubted half
    (max lam). Supported as far as the weakest conjunct is supported; reduces
    to classical conjunction on the classical corners.
    """

    return TruthValue(
        min(self.mu, other.mu),
        max(self.lam, other.lam),
    )


def disjunction(self, other: "TruthValue") -> "TruthValue":
    """
    The mirror of conjunction: OR takes the stronger mu and the milder lam,
    since a disjunction only needs one side to hold up. Evidence for the
    disjunction is as strong as its best-supported disjunct, and evidence
    against it only as strong as the weakest objection to either side.
    """

    return TruthValue(
        max(self.mu, other.mu),
        min(self.lam, other.lam),
    )


def implication(self, other: "TruthValue") -> "TruthValue":
    """
    Material implication in FDE: ¬A ∨ B, computed as disjunction(self.invert(), other).
    Unlike classical implication this is not a truth-function of a single
    degree; it inverts the antecedent and disjoins it with the consequent, so
    the resulting mu reflects both how strongly A fails and how strongly B
    holds. Reflexive implication need not yield the true corner.
    """

    return self.invert().disjunction(other)


def equivalence(self, other: "TruthValue") -> "TruthValue":
    """
    Logical equivalence in FDE: (A → B) ∧ (B → A), the conjunction of both
    material implications. Symmetric by construction, and reflexive equivalence
    need not collapse to the true corner — two identical non-classical values
    remain exactly as they are.
    """

    return self.implication(other).conjunction(other.implication(self))


def consensus(self, other: "TruthValue") -> "TruthValue":
    """
    Keeps only the evidence both operands agree on (min mu, min lam) — a
    skeptical combination where anything one side claims but the other does
    not corroborate gets dropped. It is the meet of the knowledge order:
    demanding joint warrant from a claim and its denial leaves nothing
    standing, which is the point, not a defect.
    """

    return TruthValue(
        min(self.mu, other.mu),
        min(self.lam, other.lam),
    )


def accumulate(self, other: "TruthValue") -> "TruthValue":
    """
    Pools all evidence from both operands, FOR and AGAINST alike (max mu, max
    lam), without discarding anything either side claims. Credulous
    combination: pooling a strong case for with a strong case against yields a
    contradictory value rather than resolving the conflict, which is Belnap's
    gullibility and the substance of the knowledge order's join.
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
