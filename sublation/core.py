"""
Copyleft 2026, Germano Castanho
Licensed under the MIT License
"""

from .truths import THRESHOLD, TruthValue


class Dialectical:
    """
    Shared behavior for Thesis, Antithesis, and Synthesis. Each subclass only
    builds self.value, self.thesis, and self.antithesis in its own __init__;
    the four inherited methods read those fields identically regardless of
    which subclass produced the instance.
    """

    value: TruthValue
    thesis: bool
    antithesis: bool

    def negation(self, threshold: float = THRESHOLD) -> bool:
        """
        Whether the negation of this value holds cleanly true — inverts mu and
        lam and checks the result. Equivalent to asking whether the original is
        false; at contradictory and indeterminate corners it is a fixed point.
        """

        negation = self.value.invert().is_true(threshold=threshold)
        return negation

    def contradiction(self, threshold: float = THRESHOLD) -> bool:
        """
        Whether evidence for and against are both strong at once. A plain bool
        can never represent this state — it forces True or False — but
        TruthValue can: both degrees crossing the threshold is contradiction,
        the state that motivates the whole library and the one a dialectical
        round must be able to name without collapsing.
        """

        contradiction = self.value.is_contradictory(threshold=threshold)
        return contradiction

    def becoming(self, threshold: float = THRESHOLD) -> bool:
        """
        Whether this value is a clean, uncontested affirmation — evidence FOR
        has crossed the threshold and evidence AGAINST has not. A plain bool
        can represent this, and so can TruthValue; the method exists as a
        convenience for the simplest case, the one classical logic mistakes
        for the only case.
        """

        becoming = self.value.is_true(threshold=threshold)
        return becoming

    def sublation(self, threshold: float = THRESHOLD) -> bool:
        """
        Whether this value has been determined at all, either way — Hegelian
        Aufhebung: the TruthValue has crossed the threshold in either
        direction, so it is no longer indeterminate and has been sublated.
        """

        sublation = not self.value.is_indeterminate(threshold=threshold)
        return sublation


class Thesis(Dialectical):
    """
    A proposition asserted as posited. A bool thesis infers its classical
    complement; a continuous degree infers nothing. Either inference can be
    overridden by passing antithesis explicitly.
    """

    def __init__(
        self,
        thesis: bool | float = True,
        antithesis: bool | float | None = None,
    ) -> None:
        """Builds a thesis from a proposition and its negation degree. A bool
        infers the classical complement (lam becomes 1.0 when thesis is False,
        0.0 when True). A float infers nothing — it asserts only what it
        states and leaves lam at 0.0 unless overridden. Passing antithesis
        explicitly breaks the inference, reaching the non-classical corners.
        """

        if antithesis is None:
            antithesis = (not thesis) if isinstance(thesis, bool) else 0.0

        self.value = TruthValue(mu=float(thesis), lam=float(antithesis))
        self.thesis = self.value.mu >= THRESHOLD
        self.antithesis = self.value.lam >= THRESHOLD


class Antithesis(Dialectical):
    """
    A proposition asserted as the negation of a thesis. A bool antithesis
    infers its classical complement; a continuous degree infers nothing.
    Either inference can be overridden by passing thesis explicitly.
    """

    def __init__(
        self,
        antithesis: bool | float = False,
        thesis: bool | float | None = None,
    ) -> None:
        """Builds an antithesis from a negated proposition and its affirmation
        degree. Mirrors Thesis in the opposite direction: a bool infers its
        classical complement on the thesis side; a float infers nothing,
        leaving mu at 0.0 unless overridden. Passing thesis explicitly breaks
        the inference.
        """

        if thesis is None:
            thesis = (not antithesis) if isinstance(antithesis, bool) else 0.0

        self.value = TruthValue(mu=float(thesis), lam=float(antithesis))
        self.thesis = self.value.mu >= THRESHOLD
        self.antithesis = self.value.lam >= THRESHOLD


class Synthesis(Dialectical):
    """
    Combines a Thesis and an Antithesis, trusting the thesis only on its own
    claim (mu) and the antithesis only on its own claim (lam), rather than
    pooling everything either side carries.
    """

    def __init__(self, thesis: Thesis, antithesis: Antithesis) -> None:
        """
        Combines a thesis and an antithesis, taking mu from the thesis and
        lam from the antithesis, discarding each side's other degree. Each
        side is trusted only about its own claim — the inferred complement is
        invisible here. Pooling both sides with `accumulate` would manufacture
        spurious contradiction; projection stays the rule.
        """

        self.value = TruthValue(mu=thesis.value.mu, lam=antithesis.value.lam)

        self.thesis = self.value.mu >= THRESHOLD
        self.antithesis = self.value.lam >= THRESHOLD
        self.synthesis = self.sublation()

    def as_thesis(self) -> Thesis:
        """
        Re-posits this synthesis as the thesis of the next round. Both degrees
        are passed explicitly, so the new thesis carries the exact mu/lam
        rather than a thresholded bool — intermediate certainty survives the
        chaining into a fresh antithesis.
        """

        next_round = Thesis(thesis=self.value.mu, antithesis=self.value.lam)
        return next_round

    @classmethod
    def from_values(cls, mu: float, lam: float) -> "Synthesis":
        """
        Builds a Synthesis directly from evidence degrees, without fabricating
        disposable Thesis/Antithesis instances. Equivalent to
        Synthesis(Thesis(mu), Antithesis(lam)).
        """

        return cls(Thesis(mu), Antithesis(lam))
