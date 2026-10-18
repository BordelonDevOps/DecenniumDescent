"""Small executable specifications for six scoped decisions, NOT game adapters.

All acquisition, source eligibility, damage defenses, lawful Action/Reaction
permissions, and phase existence are inputs already decided by an external
engine. These models do not establish an encounter's reachability or a CR.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any
import copy

Time = Fraction

def time(value: int | str | Fraction) -> Time:
    return Fraction(value)

@dataclass
class PrisonRoot:
    caster_id: str
    recipient_id: str
    root_id: str
    null_nonlethal: bool
    admitted: bool = True
    exit_available: bool = True
    departed: bool = False
    events: list[dict[str, Any]] = field(default_factory=list)

    def entry(self, damage: int) -> None:
        if not self.admitted or self.events:
            return
        self.events.append(self.packet('entry', damage))

    def packet(self, kind: str, amount: int) -> dict[str, Any]:
        return {'kind': kind, 'amount': amount, 'root': self.root_id,
                'dealer': self.caster_id, 'recipient': self.recipient_id,
                'nullNonlethal': self.null_nonlethal}

    def source_suppression(self) -> None:
        # Suppression can leave an application able to resume, but consumes exit.
        self.exit_available = False

    def departure(self, reason: str, damage: int, target_alive: bool = True,
                  current_caster_null: bool | None = None) -> bool:
        # current_caster_null is intentionally NOT used to recapture the root.
        if self.departed or not self.admitted:
            return False
        entitled = self.exit_available
        self.exit_available = False  # consumed before any callback/payload
        self.departed = True
        if not entitled or not target_alive or reason in ('source-disabled', 'target-removed'):
            return False
        self.events.append(self.packet('exit', damage))
        return True

@dataclass
class PuppetEnd:
    first_end: Time
    expiry: Time
    resolved: bool = False
    ended: bool = False

    def checkpoint(self, now: Time, *, actual_phase: bool, save_success: bool,
                   start_suppressed: bool = False, end_suppressed: bool = False,
                   distance_travelled: int = 0) -> str:
        if self.ended:
            return 'ended'
        if now >= self.expiry:
            self.ended = True
            return 'expiry-no-save'
        if not actual_phase or now != self.first_end or self.resolved:
            return 'no-save'
        self.resolved = True
        if save_success:
            self.ended = True
        return 'save-success' if save_success else 'save-failure'

@dataclass(frozen=True)
class GeasPermission:
    acquired_hard: bool
    deadline: Time

    def next_instruction(self, now: Time, *, requires_full_action: bool,
                         safe_soft_alternative: bool, voluntary_action_opened_path: bool = False) -> str:
        if now >= self.deadline:
            return 'expired'
        if self.acquired_hard:
            return 'original-hard-permission-subject-to-source-limits'
        if not requires_full_action or safe_soft_alternative or voluntary_action_opened_path:
            return 'soft-only'
        return 'suspend-unexecutable-portion-no-hard-acquisition'

@dataclass
class DominateEnd:
    admission: Time
    expiry: Time
    anchor: Time | None = None
    resolved_event_ids: set[str] = field(default_factory=set)
    last_save_time: Time | None = None

    def __post_init__(self) -> None:
        if self.anchor is None:
            self.anchor = self.admission

    def next_absent_due(self, transition: Time) -> Time:
        assert self.anchor is not None
        n = max(1, (transition - self.anchor) // 6 + 1)
        return self.anchor + 6 * n

    def save(self, event_id: str, now: Time, *, real_phase_end: bool,
             absent_schedule_due: Time | None = None) -> str:
        if now >= self.expiry:
            return 'expiry-no-save'
        if event_id in self.resolved_event_ids or self.last_save_time == now:
            return 'already-consumed'
        if not real_phase_end and now != absent_schedule_due:
            return 'no-save'
        self.resolved_event_ids.add(event_id)
        self.last_save_time = now
        self.anchor = now
        return 'one-wis-save-no-action'


def operative_cr_eligible(value: Any, maximum: int = 10) -> bool:
    # Validation only. This does not infer or approve any profile/rating.
    return type(value) in (int, float) and value >= 0 and value <= maximum

@dataclass
class CopyReadyLedger:
    rp: int = 30
    permission_uses: int = 3
    class_engine_actually_owned: bool = False
    feat_rounds: dict[str, str] = field(default_factory=dict)
    class_rounds: dict[str, str] = field(default_factory=dict)
    hold: dict[str, Any] | None = None
    prep_ids: set[str] = field(default_factory=set)
    completed_ids: set[str] = field(default_factory=set)
    cast_history_updates: int = 0
    counter_windows: int = 0
    components_provided: int = 0
    reaction_spends: int = 0
    action_spends: int = 0
    payloads: int = 0
    concentration: str | None = None

    def snapshot(self) -> dict[str, Any]:
        return copy.deepcopy(self.__dict__)

    def prepare(self, hold_id: str, round_id: str, expiry: Time, *, quote: int = 7,
                legal_action_and_sources: bool = True, countered: bool = False,
                profile: str = 'Strike') -> bool:
        # A true legal_action_and_sources input is a stipulated permission, not
        # an Action granted by this reference implementation.
        if (not legal_action_and_sources or quote < 0 or self.rp < quote or self.permission_uses < 1
            or hold_id in self.prep_ids or round_id in self.feat_rounds
            or (self.class_engine_actually_owned and round_id in self.class_rounds)):
            return False
        self.feat_rounds[round_id] = hold_id
        if self.class_engine_actually_owned:
            self.class_rounds[round_id] = hold_id
        self.rp -= quote
        self.permission_uses -= 1
        self.action_spends += 1
        self.cast_history_updates += 1
        self.counter_windows += 1
        self.components_provided += 1
        self.prep_ids.add(hold_id)
        self.hold = {'id': hold_id, 'prepRound': round_id, 'expiry': expiry, 'profile': profile}
        self.concentration = 'held'
        if countered:
            self.hold = None
            self.concentration = None
        return True

    def release(self, round_id: str, now: Time, *, legal_target_and_sources: bool = True,
                reaction_available: bool = True, trigger_declined: bool = False,
                later_payload_prevented: bool = False) -> str:
        h = self.hold
        if not h:
            return 'no-hold'
        if now >= h['expiry']:
            self.hold = None
            self.concentration = None
            return 'expired'
        if not legal_target_and_sources or not reaction_available or trigger_declined:
            return 'not-committed'
        same = h['prepRound'] == round_id
        if same:
            if self.feat_rounds.get(round_id) != h['id']:
                return 'not-committed'
            if self.class_engine_actually_owned and self.class_rounds.get(round_id) != h['id']:
                return 'not-committed'
        elif (round_id in self.feat_rounds or
              (self.class_engine_actually_owned and round_id in self.class_rounds)):
            return 'not-committed'
        if not same:
            self.feat_rounds[round_id] = h['id']
            if self.class_engine_actually_owned:
                self.class_rounds[round_id] = h['id']
        self.reaction_spends += 1
        self.hold = None
        self.completed_ids.add(h['id'])
        if not later_payload_prevented:
            self.payloads += 1
        self.concentration = ('sustained' if h['profile'] in ('Ward', 'Hindrance', 'Boon')
                              and not later_payload_prevented else None)
        return 'committed-prevented' if later_payload_prevented else 'committed'

    def lose_hold(self) -> None:
        self.hold = None
        self.concentration = None
