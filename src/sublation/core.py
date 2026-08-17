from .truths import THRESHOLD, TruthValue


class Dialectical:
    """
    Shared behavior for Thesis, Antithesis, and Synthesis. Each subclass is only responsible for building self.value, self.thesis, and self.antithesis in its own __init__ — the four methods below read those fields the same way regardless of which subclass created them.
    """

    value: TruthValue
    thesis: bool
    antithesis: bool

    def negation(self) -> bool:
        """
        Whether the negation of this value holds cleanly true. Inverts the `mu` and `lam` of the underlying TruthValue and checks whether that inverted value is true.
        """

        negation = self.value.invert().is_true()
        return negation

    def contradiction(self) -> bool:
        """
        Whether evidence for and against are both strong at once. State that a plain bool can never represent - True and False at the same time -, but that TruthValue can.
        """

        contradiction = self.value.is_contradictory()
        return contradiction

    def becoming(self) -> bool:
        """
        Whether this value is a clean, uncontested affirmation. State that a plain bool can represent, but that TruthValue can also represent. This method is just a convenience for when you want to check for the simplest case.
        """

        becoming = self.value.is_true()
        return becoming

    def sublation(self) -> bool:
        """
        Whether this value has been determined at all, either way. Corresponds to the Hegelian notion of `Aufhebung`. In this case, it means that the TruthValue has crossed the threshold in either direction, so it is no longer indeterminate and has been "sublated" (Aufgehoben).
        """

        sublation = not self.value.is_indeterminate()
        return sublation


class Thesis(Dialectical):
    """
    Thesis: a proposition asserted as posited. A bool thesis infers its complement (asserting the thesis denies its antithesis), a continuous degree does not (it asserts nothing against). Either inference can be overridden by passing antithesis explicitly.
    """

    def __init__(
        self,
        thesis: bool | float = True,
        antithesis: bool | float | None = None,
    ) -> None:
        if antithesis is None:
            antithesis = (not thesis) if isinstance(thesis, bool) else 0.0

        self.value = TruthValue(mu=float(thesis), lam=float(antithesis))
        self.thesis = self.value.mu >= THRESHOLD
        self.antithesis = self.value.lam >= THRESHOLD


class Antithesis(Dialectical):
    """
    Antithesis: a proposition asserted as the negation of a thesis. A bool antithesis infers its complement (asserting the antithesis denies the thesis), a continuous degree does not (it asserts nothing for). Either inference can be overridden by passing thesis explicitly.
    """

    def __init__(
        self,
        antithesis: bool | float = False,
        thesis: bool | float | None = None,
    ) -> None:
        if thesis is None:
            thesis = (not antithesis) if isinstance(antithesis, bool) else 0.0

        self.value = TruthValue(mu=float(thesis), lam=float(antithesis))
        self.thesis = self.value.mu >= THRESHOLD
        self.antithesis = self.value.lam >= THRESHOLD


class Synthesis(Dialectical):
    """
    Synthesis: combines a Thesis and an Antithesis - it trusts the thesis only on its own claim (mu) and the antithesis only on its own claim (lam), rather than pooling everything either side happens to carry.
    """

    def __init__(self, thesis: Thesis, antithesis: Antithesis) -> None:
        self.value = TruthValue(mu=thesis.value.mu, lam=antithesis.value.lam)

        self.thesis = self.value.mu >= THRESHOLD
        self.antithesis = self.value.lam >= THRESHOLD
        self.synthesis = self.sublation()

    def as_thesis(self) -> Thesis:
        """
        The synthesys generates a new Thesis for the next round of dialectical evaluation. The new thesis will have a new antithesis, which will be the negation of this synthesis. At the end of the next round, the new thesis will be evaluated against its antithesis etc.
        """

        next_round = Thesis(thesis=self.thesis, antithesis=self.antithesis)
        return next_round
