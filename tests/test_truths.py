import pytest

from sublation.truths import TruthValue, truth_value_from_bool


def test_from_bool_round_trips_through_to_bool():
    assert truth_value_from_bool(True).to_bool() is True
    assert truth_value_from_bool(False).to_bool() is False


def test_invert_swaps_evidence():
    negated = TruthValue(mu=0.8, lam=0.2).invert()
    assert negated.mu == 0.2
    assert negated.lam == 0.8


def test_conjunction_takes_the_weaker_and_more_doubted_half():
    result = TruthValue(0.9, 0.1).conjunction(TruthValue(0.3, 0.6))
    assert result.mu == 0.3
    assert result.lam == 0.6


def test_disjunction_takes_the_stronger_and_less_doubted_half():
    result = TruthValue(0.9, 0.1).disjunction(TruthValue(0.3, 0.6))
    assert result.mu == 0.9
    assert result.lam == 0.1


def test_consensus_keeps_only_shared_evidence():
    result = TruthValue(0.9, 0.4).consensus(TruthValue(0.3, 0.7))
    assert result.mu == 0.3
    assert result.lam == 0.4


def test_accumulate_pools_all_evidence():
    result = TruthValue(0.9, 0.4).accumulate(TruthValue(0.3, 0.7))
    assert result.mu == 0.9
    assert result.lam == 0.7


@pytest.mark.parametrize(
    "mu, lam, expected",
    [
        (1.0, 0.0, "true"),
        (0.0, 1.0, "false"),
        (1.0, 1.0, "contradictory"),
        (0.0, 0.0, "indeterminate"),
    ],
)
def test_the_four_fde_corners(mu, lam, expected):
    value = TruthValue(mu, lam)
    assert value.is_true() == (expected == "true")
    assert value.is_false() == (expected == "false")
    assert value.is_contradictory() == (expected == "contradictory")
    assert value.is_indeterminate() == (expected == "indeterminate")


def test_rejects_out_of_range_evidence():
    with pytest.raises(ValueError):
        TruthValue(mu=1.5, lam=0.0)
    with pytest.raises(ValueError):
        TruthValue(mu=0.0, lam=-0.1)
