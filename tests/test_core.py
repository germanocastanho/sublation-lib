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


def test_synthesis_chains_into_new_thesis():
    t1 = Thesis(True)
    a1 = Antithesis(False)
    s1 = Synthesis(t1, a1)
    t2 = s1.as_thesis()
    assert isinstance(t2, Thesis)
    assert t2.thesis == s1.thesis
    assert t2.antithesis == s1.antithesis
