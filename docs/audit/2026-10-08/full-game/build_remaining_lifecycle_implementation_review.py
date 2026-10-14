"""Prepare exact implementation review; never infer GPT approval from tests."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/remaining_lifecycle_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
data['status']='IMPLEMENTED CANDIDATE: selected80+5 lifecycle/command/object/guard roles; exact GPT implementation review pending'
evidence=['GPT_REMAINING_LIFECYCLE_FIRST_REVIEW.md','GPT_REMAINING_LIFECYCLE_BOUNDARIES.md','GPT_REMAINING_LIFECYCLE_PROFILES.md']
for r in data['bindings']:
    role=r['classification'];ident=r['bindingId']
    deferred=role.startswith('DEFER') or 'THP details' in role
    r['status']='DISCUSSED / full temporary-HP or Time Loop effect DEFERRED; prior bounded roles preserved' if deferred else 'IMPLEMENTED CANDIDATE: supplied lifecycle/object/guard or prior-component boundary only'
    r['reviewEvidence']=evidence[:]
    base='Apply only the exact source-specific section in docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST.md; original source text/hash preserved.'
    if role.startswith('DEFER'):
        override='No new full temporary-HP, form or Time Loop effect implemented here. Its named lifecycle/guard classification gives no new body, command, corpse, repair or resource rights.'
    elif role.startswith('PREV') or role.startswith('MOD/PREV'):
        override='Preserve previously reviewed healing/control/death/redirection component only. No additional lifecycle or whole-card approval; incidental THP remains in its dedicated corpus.'
    elif role.startswith('GUARD'):
        override='Exact anti-farm, source access, agency, resource, perception, copy or check restriction remains a caller precondition; this passage supplies no new creature/body/object creation or transferable resource rights.'
    elif role.startswith('ZONE'):
        override='Non-HP zone/effect; no attackable body, repair/dismantle/Tinker rights or Palisade Synergy. Apply only printed protection with existing strongest-only defense rules.'
    elif role.startswith('MOD actual'):
        override='Only actual own intact Palisade qualifies. Creation TierII durability is snapshotted; geometry, strongest-only defense and once/own-turn actual ranged-weapon-hit Synergy gates remain exact.'
    else:
        override='Exact bounded creation, costs, identity, lifetime, command/sacrifice, supply and profile decisions are implemented by the named guide procedures and remaining_lifecycle_playtest_rules.py. Shared canonical budgets and caller gates are mandatory.'
    r['operationalOverrides']=[base,override]
    r['openIssues']=['Exact implementation review pending.','Complete card/family effects, global corpse cleanup, temporary HP/forms, Time Loop, general travel timing, balance and runtime remain outside this packet.']
data['implementationGuide']='docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST.md'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=['docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST.md','tools/remaining_lifecycle_playtest_rules.py',
       'tools/validate_remaining_lifecycle_playtests.py','docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST_VALIDATION.json',
       'docs/mechanics/REMAINING_LIFECYCLE_SOURCE_VALIDATION.json']
lines=['# Remaining lifecycle exact implementation review','',
       'Codex → Calibration Review. Review the actual bounded implementation below against all three saved conference decisions.124 targeted checks pass. Shared CreatureWorld change is additive known-created-object identity guarding; prior creature121/2800 regressions pass.80 original source records+5 frozen supports retain their hashes. Please identify concrete semantic defects, not claim the entire card/family complete. If no blockers, explicitly dispose only of selected lifecycle/command/object/guard roles; all exclusions remain.',
       '', 'Questions to scrutinize: canonical owner/target budgets and cross-round reservations; one post-hit interception per actual incoming attack and native zero assignment (caller executes existing creature lifecycle); Choir end snapshots and sealed-trigger/no-heal bursts; on-hit healing at zero damage; true corpse consumption; Palisade inventory/caps/repair; per-use turret quantity without a global2 cap; no Tinker permissions; Echo profile cap; narrative scout return deadline. First-damage DR opportunities are consumed before strongest-only arbitration. ExistingUndeadBuff.attack_bonus is a profile eligibility query; caller certifies the one source-authorized commanded attack, not every hit. No complete attack/condition runtime is asserted.',
       '', 'All source IDs and classifications (exact originals follow):']
for r in data['bindings']:
    lines+=['',r['bindingId']+' — '+r['classification'],json.dumps(r['sourceProcedure'],ensure_ascii=False,separators=(',',':'))]
support=json.loads((HERE/'CREATURE_LIFECYCLE_SUPPORTING_SOURCES.json').read_text(encoding='utf-8'))
lines+=['','## Exact frozen supporting paragraphs',json.dumps(support,ensure_ascii=False)]
for name in files:
    text=(ROOT/name).read_text(encoding='utf-8')
    lines+=['','## '+name,'SHA256 '+hashlib.sha256(text.encode()).hexdigest(),'```',text,'```']
# The actual reused canonical payment/reservation and extra-action adapters.
device=(ROOT/'tools/device_lifecycle_playtest_rules.py').read_text(encoding='utf-8')
lines+=['','## Shared exact Wallet/CommandLedger',device[device.index('@dataclass\nclass Wallet:'):device.index('@dataclass\nclass Entity:')]]
creature=(ROOT/'tools/creature_lifecycle_playtest_rules.py').read_text(encoding='utf-8')
for start,end in [('class Corpse:', '@dataclass\nclass RaiseReservation:'),('class HardDenialLedger:','@dataclass\nclass ReflectiveBond:'),('class CreatureWorld:','    def standard_count')]:
    lines+=['','## Shared exact dependency '+start,creature[creature.index(start):creature.index(end)]]
combat=(ROOT/'tools/combat_playtest_rules.py').read_text(encoding='utf-8')
lines+=['','## Shared exact ExtraActionClock',combat[combat.index('class ExtraActionClock:'):combat.index('def reinforcement_first_round')]]
out=HERE/'CODEX_REMAINING_LIFECYCLE_IMPLEMENTATION.md'
out.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(f'Prepared implementation packet {out.stat().st_size} bytes; no review closure.')
