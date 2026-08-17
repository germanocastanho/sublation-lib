"""
Validation against three canonical cases: the liar paradox, the sorites,
and Hegel's Being/Nothing/Becoming triad. Each test encodes only what the
library actually models, and comments where the mapping is interpretive.
"""

from itertools import pairwise

from sublation import Antithesis, Synthesis, Thesis, TruthValue


def test_liar_is_a_stable_contradiction_not_an_explosion():
    """
    "This sentence is false": its truth entails its falsity and vice versa,
    so evidence lands on both sides at once. That is the contradictory corner,
    and `invert` (its own negation) is a fixed point there — the paradox is
    recorded as a determinate state instead of blowing the logic up.
    """

    liar = TruthValue(mu=1.0, lam=1.0)
    assert liar.is_contradictory() is True

    negated = liar.invert()
    assert (negated.mu, negated.lam) == (liar.mu, liar.lam)

    assert Thesis(True, True).sublation() is True


def test_sorites_passes_through_indeterminacy_without_a_sharp_cutoff():
    """
    Removing grains one at a time: as evidence-for a heap fades from 1.0 to
    0.0, the verdict does not flip crisply true -> false. A middle band reads
    indeterminate, which is the sorites' point — there is no single grain at
    which "heap" becomes "not a heap".
    """

    gradient = [i / 10 for i in range(10, -1, -1)]
    verdicts = [Thesis(mu).becoming() for mu in gradient]

    assert verdicts[0] is True
    assert verdicts[-1] is False

    middle = [Thesis(mu) for mu in gradient if 0.0 < mu < 0.5]
    assert all(t.sublation() is False for t in middle)

    transitions = sum(1 for a, b in pairwise(verdicts) if a != b)
    assert transitions == 1


def test_being_and_nothing_are_indeterminate_becoming_is_their_unity():
    """
    Being and Nothing are each pure and empty — nothing determinate is
    asserted either way — which is the indeterminate corner. Their unity as
    a synthesis is likewise undetermined: the movement is real, but no side
    has yet settled it. (Interpretive mapping of Hegel's opening triad.)
    """

    being = Thesis(0.0)
    nothing = Antithesis(0.0)
    assert being.value.is_indeterminate() is True
    assert nothing.value.is_indeterminate() is True

    becoming = Synthesis(being, nothing)
    assert becoming.value.is_indeterminate() is True
    assert becoming.sublation() is False
