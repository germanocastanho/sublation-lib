from sublation import Antithesis, Synthesis, Thesis


def test_matches_original_signature_defaults():
    assert Thesis().thesis is True
    assert Thesis().antithesis is False
    assert Antithesis().thesis is True
    assert Antithesis().antithesis is False


def test_contradiction_is_detectable():
    t = Thesis(True)
    a = Antithesis(True)
    s = Synthesis(t, a)
    assert s.contradiction() is True
    assert s.becoming() is False


def test_empty_antithesis_resolves_without_tension():
    t = Thesis(True)
    a = Antithesis(False)
    s = Synthesis(t, a)
    assert s.contradiction() is False
    assert s.becoming() is True


def test_continuous_thesis_keeps_its_degree_without_inferring_a_complement():
    t = Thesis(0.7)
    assert (t.value.mu, t.value.lam) == (0.7, 0.0)


def test_continuous_antithesis_keeps_its_degree_without_inferring_a_complement():
    a = Antithesis(0.7)
    assert (a.value.mu, a.value.lam) == (0.0, 0.7)


def test_continuous_degrees_are_taken_verbatim_when_both_are_given():
    t = Thesis(0.7, 0.2)
    assert (t.value.mu, t.value.lam) == (0.7, 0.2)


def test_float_zero_is_indeterminate_unlike_bool_false():
    quiet = Thesis(0.0)
    denied = Thesis(False)
    assert (quiet.value.mu, quiet.value.lam) == (0.0, 0.0)
    assert quiet.sublation() is False
    assert (denied.value.mu, denied.value.lam) == (0.0, 1.0)
    assert denied.sublation() is True


def test_synthesis_chains_into_new_thesis():
    t1 = Thesis(True)
    a1 = Antithesis(False)
    s1 = Synthesis(t1, a1)
    t2 = s1.as_thesis()
    assert isinstance(t2, Thesis)
    assert t2.thesis == s1.thesis
    assert t2.antithesis == s1.antithesis


def test_as_thesis_preserves_continuous_degrees():
    s = Synthesis(Thesis(0.7), Antithesis(0.2))
    t = s.as_thesis()
    assert (t.value.mu, t.value.lam) == (0.7, 0.2)


def test_dialectical_methods_accept_threshold():
    # becoming: is_true on the underlying value
    s = Synthesis(Thesis(0.6), Antithesis(0.2))
    assert s.becoming() is True
    assert s.becoming(threshold=0.8) is False

    # contradiction: is_contradictory on the underlying value
    s = Synthesis(Thesis(0.8), Antithesis(0.8))
    assert s.contradiction() is True
    assert s.contradiction(threshold=0.9) is False

    # sublation: not is_indeterminate on the underlying value
    s = Synthesis(Thesis(0.6), Antithesis(0.2))
    assert s.sublation() is True
    assert s.sublation(threshold=0.8) is False

    # negation: invert().is_true() on the underlying value
    s = Synthesis(Thesis(0.2), Antithesis(0.6))
    assert s.negation() is True
    assert s.negation(threshold=0.8) is False


def test_synthesis_from_values_matches_thesis_antithesis_flow():
    s = Synthesis.from_values(0.7, 0.2)
    assert s.value.mu == 0.7
    assert s.value.lam == 0.2

    reference = Synthesis(Thesis(0.7), Antithesis(0.2))
    assert (s.value.mu, s.value.lam) == (reference.value.mu, reference.value.lam)
