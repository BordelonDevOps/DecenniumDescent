"""Three reviewed primitives from131-source discussion; not complete class execution."""
from dataclasses import dataclass
from spell_playtest_rules import integer,SpellRuleError


def zealot_backlash(after_fire_defenses, *, explicitly_suppressed=False):
    """Separate packet after heal ATTEMPT, not conditional on actualHP restored.

    The source minimum modifies resolved DAMAGE, not survivingHP. Caller rolls
    1d4, applies all legal defenses AND prevention, establishes an actual suppression source, then sends
    this result through ordinary tempHP/HP/Wound/death handling.
    """
    integer(after_fire_defenses,'backlash after ordinary fire defenses',0)
    return 0 if explicitly_suppressed else max(1,after_fire_defenses)


def crown_burn_healing(total_actual_fire_damage, recipient_ids, *, shared_cap_total,
                       scale, roll_instance_id):
    """Source base only: predeclared legal recipients; caller validates range/use.

    Numeric qualifying fire damage, not merely positive packet existence. Each
    resulting base runs its own healing pipeline. The source minimum is before
    target reductions/prohibitions; it does not promise1 actualHP through Decay.
    One shared cap roll retains S healing dice for per-die modifiers.
    recipient_ids are locked at activation. A later-ineligible target skips its
    application; never replace it or recalculate the denominator for survivors.
    """
    integer(total_actual_fire_damage,'qualifying numeric actual fire damage',0)
    integer(shared_cap_total,'shared Sd6+M healing-cap result',1)
    integer(scale,'class scaling S',1,4)
    if not roll_instance_id:raise SpellRuleError('Shared healing roll needs identity')
    ids=tuple(recipient_ids)
    if len(ids)>3 or len(ids)!=len(set(ids)):
        raise SpellRuleError('Crown Burn requires0–3 distinct legal recipients')
    if not ids or total_actual_fire_damage==0:return []
    amount=max(1,min(total_actual_fire_damage//len(ids),shared_cap_total))
    return [{'targetId':ident,'sourceBase':amount,'diceCount':scale,
             'rollInstanceId':roll_instance_id} for ident in ids]


@dataclass(frozen=True)
class MendRecord:
    record_id: str
    source_creature_id: str
    target_id: str
    rolled_profile_amount: int
    source_roll_id: str

    def __post_init__(self):
        if not all((self.record_id,self.source_creature_id,self.target_id,self.source_roll_id)):
            raise SpellRuleError('Mend record requires source/record/target/roll identities')
        integer(self.rolled_profile_amount,'legal rolled Mend profile amount',0)


def dual_mend_components(records):
    """Selected two-Mend case of Dual Echo Cast, NOT Echo Fusion.

    Caller pays both RP costs, consumes both eligible captured records and spends
    the one combined release/action before resolving these components. Inputs
    are each legal printed profile total; no critical dice/resource/rider copy.
    Both may target the same legal ally. Numeric halves are flat copied amounts;
    later explicitly added real dice remain a separately tracked modifier.
    """
    if len(records)!=2 or len({r.record_id for r in records})!=2:
        raise SpellRuleError('Dual Echo Cast needs2 distinct records')
    if len({r.source_creature_id for r in records})!=2:
        raise SpellRuleError('Dual Echo Cast records must come from different creatures')
    return [{'targetId':r.target_id,'sourceBase':r.rolled_profile_amount//2,
             'diceCount':0,'recordId':r.record_id,'sourceRollId':r.source_roll_id,
             'copiedNumeric':True} for r in records]
