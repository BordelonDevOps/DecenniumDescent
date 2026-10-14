"""Narrow reference for the new provisional falling bridge, not a combat engine.

The caller owns legal spell activation/expiry, support, initiative, defenses and
resolved damage. Call step only at the existing fixed Fall Marker.
"""
from dataclasses import dataclass
from spell_playtest_rules import integer, SpellRuleError


@dataclass
class Fall:
    height_remaining: int
    initiated_round: int
    regular_slot: int
    total_distance: int = 0
    uncontrolled_distance: int = 0
    slowed: bool = False

    def __post_init__(self):
        integer(self.height_remaining, 'fall height', 1)
        integer(self.initiated_round, 'round', 1)
        integer(self.regular_slot, 'fixed regular initiative slot', 0)
        self.next_round = self.initiated_round + 1

    def set_feather_fall(self, active):
        if not isinstance(active, bool):
            raise SpellRuleError('Feather Fall state must be boolean')
        if self.height_remaining == 0:
            raise SpellRuleError('Cannot change a resolved landing')
        if active != self.slowed:
            self.uncontrolled_distance = 0
        self.slowed = active

    def step(self, round_number, regular_slot):
        integer(round_number, 'round', 1)
        integer(regular_slot, 'fixed regular initiative slot', 0)
        if self.height_remaining == 0:
            raise SpellRuleError('Landing already resolved')
        if (round_number, regular_slot) != (self.next_round, self.regular_slot):
            raise SpellRuleError('Not the next fixed Fall Marker')
        distance = min(self.height_remaining, 60 if self.slowed else 300)
        self.height_remaining -= distance
        self.total_distance += distance
        if not self.slowed:
            self.uncontrolled_distance += distance
        self.next_round += 1
        landed = self.height_remaining == 0
        dice = min(3, self.total_distance // 20) if self.slowed else min(10, self.uncontrolled_distance // 20)
        return {'descended': distance, 'landed': landed, 'damageD6': dice if landed else 0}
