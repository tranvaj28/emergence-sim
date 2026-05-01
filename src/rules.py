"""
Rule set definitions and B/S notation parser for cellular automata.
"""

from dataclasses import dataclass
import re
from typing import Set


@dataclass
class RuleSet:
    """A cellular automaton rule expressed in B/S notation."""

    name: str
    born: Set[int]  # neighbor counts that cause a dead cell to become alive
    survive: Set[int]  # neighbor counts that allow a live cell to stay alive

    def applies_to_cell(self, alive: bool, neighbor_count: int) -> bool:
        """
        Determine whether a cell should be alive in the next generation.

        Args:
            alive: Whether the cell is currently alive.
            neighbor_count: Number of alive neighbors (0‑8).

        Returns:
            True if the cell should be alive in the next generation.
        """
        if alive:
            return neighbor_count in self.survive
        else:
            return neighbor_count in self.born

    def __str__(self) -> str:
        """Return the rule in standard B/S notation."""
        born_str = "".join(str(d) for d in sorted(self.born))
        survive_str = "".join(str(d) for d in sorted(self.survive))
        return f"B{born_str}/S{survive_str}"

    @classmethod
    def from_string(cls, name: str, rule_string: str) -> "RuleSet":
        """
        Create a RuleSet from a B/S notation string.

        Args:
            name: Human‑readable name for the rule.
            rule_string: Rule in B/S notation (e.g., 'B3/S23').

        Returns:
            A new RuleSet instance.

        Raises:
            ValueError: If the rule string is malformed or contains invalid digits.
        """
        born, survive = parse_rule_string(rule_string)
        return cls(name=name, born=born, survive=survive)


def parse_rule_string(rule_string: str) -> tuple[Set[int], Set[int]]:
    """
    Parse a B/S notation rule string into born and survive sets.

    Args:
        rule_string: Rule string (e.g., 'B3/S23', 'b36/s23').

    Returns:
        Tuple of (born_set, survive_set).

    Raises:
        ValueError: If the string format is invalid or digits are out of range.
    """
    # Normalize: uppercase, remove whitespace
    rule_string = rule_string.upper().replace(" ", "")

    # Match pattern: B followed by digits (optional), slash, S followed by digits (optional)
    pattern = r"^B([0-8]*)/S([0-8]*)$"
    match = re.match(pattern, rule_string)
    if not match:
        raise ValueError(
            f"Invalid rule string format: {rule_string}. Expected 'B<digits>/S<digits>'"
        )

    born_digits, survive_digits = match.groups()

    # Convert digit strings to sets of integers (empty strings produce empty sets)
    born = {int(d) for d in born_digits} if born_digits else set()
    survive = {int(d) for d in survive_digits} if survive_digits else set()

    # Validate digit range (pattern ensures 0‑8, but double‑check)
    for digit_set in (born, survive):
        for d in digit_set:
            if not 0 <= d <= 8:
                raise ValueError(f"Digit {d} out of range 0‑8")

    return born, survive


# Preset rule definitions
CONWAY = RuleSet(name="Conway's Game of Life", born={3}, survive={2, 3})

HIGHLIFE = RuleSet(name="HighLife", born={3, 6}, survive={2, 3})

DAY_NIGHT = RuleSet(name="Day & Night", born={3, 6, 7, 8}, survive={3, 4, 6, 7, 8})

# Map of preset rules by name
PRESETS = {
    "conway": CONWAY,
    "highlife": HIGHLIFE,
    "day_night": DAY_NIGHT,
}

# Map of shortcut keys to preset rules (for keyboard shortcuts)
SHORTCUT_TO_RULE = {
    "1": CONWAY,
    "2": HIGHLIFE,
    "3": DAY_NIGHT,
}
