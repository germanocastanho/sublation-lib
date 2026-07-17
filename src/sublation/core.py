from typing import Optional


class Thesis:
    def __init__(self, thesis: bool = True, antithesis: Optional[bool] = None):
        self.thesis = thesis
        self.antithesis = (not thesis) if antithesis is None else antithesis
        self.synthesis = None

    def negation(self) -> bool:
        return not self.thesis

    def contradiction(self) -> bool:
        return self.thesis and self.antithesis

    def becoming(self) -> bool:
        return self.thesis and not self.antithesis

    def sublation(self) -> bool:
        return self.thesis or self.antithesis


class Antithesis:
    def __init__(self, antithesis: bool = False, thesis: Optional[bool] = None):
        self.antithesis = antithesis
        self.thesis = (not antithesis) if thesis is None else thesis
        self.synthesis = None

    def negation(self) -> bool:
        return not self.antithesis

    def contradiction(self) -> bool:
        return self.antithesis and self.thesis

    def becoming(self) -> bool:
        return self.antithesis and not self.thesis

    def sublation(self) -> bool:
        return self.thesis or self.antithesis


class Synthesis:
    def __init__(self, thesis: Thesis, antithesis: Antithesis):
        self.thesis = thesis.thesis
        self.antithesis = antithesis.antithesis
        self.synthesis = self.sublation()

    def negation(self) -> bool:
        return not self.thesis

    def contradiction(self) -> bool:
        return self.thesis and self.antithesis

    def becoming(self) -> bool:
        return self.thesis and not self.antithesis

    def sublation(self) -> bool:
        return self.thesis or self.antithesis

    def as_thesis(self) -> Thesis:
        return Thesis(thesis=self.thesis, antithesis=self.antithesis)
