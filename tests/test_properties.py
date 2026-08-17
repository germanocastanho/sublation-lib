"""
Property-based invariants for TruthValue. The four combining operations are
defined by min/max alone, so results are exact degrees of the inputs and can
be compared without float tolerance. Values are compared as (mu, lam) tuples,
since TruthValue defines no __eq__.
"""

from hypothesis import given
from hypothesis import strategies as st

from sublation.truths import TruthValue

_degree = st.floats(min_value=0.0, max_value=1.0, allow_nan=False)
_values = st.builds(TruthValue, _degree, _degree)

COMBINING = ["conjunction", "disjunction", "consensus", "accumulate"]


def _deg(value: TruthValue) -> tuple[float, float]:
    return (value.mu, value.lam)


@given(a=_values, op=st.sampled_from(COMBINING))
def test_combining_is_idempotent(a, op):
    combine = getattr(a, op)
    assert _deg(combine(a)) == _deg(a)


@given(a=_values, b=_values, op=st.sampled_from(COMBINING))
def test_combining_is_commutative(a, b, op):
    assert _deg(getattr(a, op)(b)) == _deg(getattr(b, op)(a))


@given(a=_values, b=_values, c=_values, op=st.sampled_from(COMBINING))
def test_combining_is_associative(a, b, c, op):
    left = getattr(getattr(a, op)(b), op)(c)
    right = getattr(a, op)(getattr(b, op)(c))
    assert _deg(left) == _deg(right)


@given(a=_values)
def test_invert_is_involutive(a):
    assert _deg(a.invert().invert()) == _deg(a)


@given(a=_values, b=_values)
def test_invert_satisfies_de_morgan(a, b):
    na, nb = a.invert(), b.invert()
    assert _deg(a.conjunction(b).invert()) == _deg(na.disjunction(nb))
    assert _deg(a.disjunction(b).invert()) == _deg(na.conjunction(nb))


@given(a=_values, b=_values, op=st.sampled_from(["consensus", "accumulate"]))
def test_invert_commutes_with_the_knowledge_order(a, b, op):
    combined = getattr(a, op)(b).invert()
    separately = getattr(a.invert(), op)(b.invert())
    assert _deg(combined) == _deg(separately)


def test_invert_fixes_the_non_classical_corners():
    assert _deg(TruthValue(1.0, 1.0).invert()) == (1.0, 1.0)
    assert _deg(TruthValue(0.0, 0.0).invert()) == (0.0, 0.0)
