"""Unit tests for rule parsing and RuleSet functionality."""

import pytest

from src.rules import HIGHLIFE, DAY_NIGHT, RuleSet, parse_rule_string


def test_parse_rule_string_valid():
    """Parse standard B/S notation strings."""
    born, survive = parse_rule_string("B3/S23")
    assert born == {3}
    assert survive == {2, 3}

    born, survive = parse_rule_string("B36/S23")
    assert born == {3, 6}
    assert survive == {2, 3}

    born, survive = parse_rule_string("B3678/S34678")
    assert born == {3, 6, 7, 8}
    assert survive == {3, 4, 6, 7, 8}


def test_parse_rule_string_empty_sets():
    """Parse rules with missing born or survive digits."""
    born, survive = parse_rule_string("B/S")
    assert born == set()
    assert survive == set()

    born, survive = parse_rule_string("B3/S")
    assert born == {3}
    assert survive == set()

    born, survive = parse_rule_string("B/S23")
    assert born == set()
    assert survive == {2, 3}


def test_parse_rule_string_invalid():
    """Malformed rule strings raise ValueError."""
    with pytest.raises(ValueError):
        parse_rule_string("")
    with pytest.raises(ValueError):
        parse_rule_string("B3S23")
    with pytest.raises(ValueError):
        parse_rule_string("B3/S23/extra")
    with pytest.raises(ValueError):
        parse_rule_string("B3/S2a")


def test_rule_set_from_string():
    """Create RuleSet instances from B/S strings."""
    rule = RuleSet.from_string("Conway", "B3/S23")
    assert rule.name == "Conway"
    assert rule.born == {3}
    assert rule.survive == {2, 3}
    assert str(rule) == "B3/S23"


def test_rule_set_applies_to_cell():
    """Test cell state transitions based on neighbor counts."""
    rule = RuleSet.from_string("Conway", "B3/S23")

    # Dead cells become alive with exactly 3 neighbors
    assert rule.applies_to_cell(alive=False, neighbor_count=3) is True
    assert rule.applies_to_cell(alive=False, neighbor_count=2) is False
    assert rule.applies_to_cell(alive=False, neighbor_count=4) is False

    # Live cells survive with 2 or 3 neighbors
    assert rule.applies_to_cell(alive=True, neighbor_count=2) is True
    assert rule.applies_to_cell(alive=True, neighbor_count=3) is True
    assert rule.applies_to_cell(alive=True, neighbor_count=1) is False
    assert rule.applies_to_cell(alive=True, neighbor_count=4) is False


def test_highlife_preset():
    """HighLife preset (B36/S23) has correct born/survive sets."""
    assert HIGHLIFE.name == "HighLife"
    assert HIGHLIFE.born == {3, 6}
    assert HIGHLIFE.survive == {2, 3}
    assert str(HIGHLIFE) == "B36/S23"


def test_highlife_applies_to_cell():
    """Test HighLife-specific cell transitions."""
    rule = HIGHLIFE

    # Dead cells become alive with 3 or 6 neighbors
    assert rule.applies_to_cell(alive=False, neighbor_count=3) is True
    assert rule.applies_to_cell(alive=False, neighbor_count=6) is True
    assert rule.applies_to_cell(alive=False, neighbor_count=2) is False
    assert rule.applies_to_cell(alive=False, neighbor_count=4) is False

    # Live cells survive with 2 or 3 neighbors
    assert rule.applies_to_cell(alive=True, neighbor_count=2) is True
    assert rule.applies_to_cell(alive=True, neighbor_count=3) is True
    assert rule.applies_to_cell(alive=True, neighbor_count=1) is False
    assert rule.applies_to_cell(alive=True, neighbor_count=6) is False


def test_day_night_preset():
    """Day & Night preset (B3678/S34678) has correct born/survive sets."""
    assert DAY_NIGHT.name == "Day & Night"
    assert DAY_NIGHT.born == {3, 6, 7, 8}
    assert DAY_NIGHT.survive == {3, 4, 6, 7, 8}
    assert str(DAY_NIGHT) == "B3678/S34678"


def test_day_night_applies_to_cell():
    """Test Day & Night-specific cell transitions."""
    rule = DAY_NIGHT

    # Dead cells become alive with 3, 6, 7, or 8 neighbors
    for n in (3, 6, 7, 8):
        assert rule.applies_to_cell(alive=False, neighbor_count=n) is True
    assert rule.applies_to_cell(alive=False, neighbor_count=2) is False
    assert rule.applies_to_cell(alive=False, neighbor_count=4) is False

    # Live cells survive with 3, 4, 6, 7, or 8 neighbors
    for n in (3, 4, 6, 7, 8):
        assert rule.applies_to_cell(alive=True, neighbor_count=n) is True
    assert rule.applies_to_cell(alive=True, neighbor_count=2) is False
    assert rule.applies_to_cell(alive=True, neighbor_count=5) is False


def test_rule_set_str():
    """String representation matches B/S notation."""
    rule = RuleSet(name="Test", born={1, 2}, survive={4, 5})
    assert str(rule) == "B12/S45"

    rule = RuleSet(name="Empty", born=set(), survive=set())
    assert str(rule) == "B/S"
