"""Prepare exact source questions; do not activate an unreviewed pipeline."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'REDIRECTION_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
questions='''# Damage sharing, retargeting and prevention — source conference

Codex → Calibration Review. This is the exact39-passage redirection candidate set:32 cards and7 engine passages. It includes prohibited-transfer HP costs, reflection/reduction and non-damage healing redirection as exclusions. Classify every supplied source by exact ID; do not assume the word redirect identifies one universal operation. Preserve original source actions, costs, target willingness, range, clocks and limits.

The existing healing interface is closed only after receiving a resolvedDamage amount. It defines actualDamageDealt=tempAbsorbed+actualHpDamage for numeric drains AFTER recipient life resolution. That measure must not accidentally become the quantity being divided BEFORE tempHP. Original sources remain unchanged; proposed clarifications are review overlays.

Please author a bounded shared sequence and explicit source exceptions, and give adversarial examples for:

1. Guardian Pulse retargets an attack before AC/defenses and later counterattacks. Bloodbond/Veinlock Tether split before each recipient's own mitigation. Paladin/Oracle Life Link/Shared Breath/Soldier/Guardian Tissue/Aegis split after original defenses. Name the exact quantity/phase at each operation and the point at which original save/critical dice have already applied. Distinguish interception, damage prevention, typed transfer, retaliatory new damage, and numeric healing redirection.
2. Bloodbond pre-mitigation: does original attack/save determine raw packet before sharing? Original resistance must affect only retained portion; recipient resistance once on transferred portion. Can original-target flat DR apply before deciding share? No recursion for transferred portions. Multiple owners offering simultaneous transfers must not duplicate damage or multiply life-drain metrics.
3. Post-defense transfers: before original temporaryHP? Does recipient temporaryHP absorb a transfer described cannot-reduce/unmitigated? Aegis explicitly names before original tempHP. Are recipient HP floors/Wards and Core Wound/InstantDeath consequences preserved? Distinguish unpreventable damage from an explicit unpreventable DEATH; do not infer all survival defenses bypassed.
4. Who has actually taken damage, been hit, or become subject to an attached poison/control rider after full transfer? Does recipient suffer critical-at-zero double death failures when original attack was critical but did not hit them? Does its own concentration save use the received post-defense packet even if tempHP absorbs it? Transfer cannot manufacture an attack hit. State exact rules if sources are silent and label NEW.
5. Original-caster damage totals after split: sum actual damage across recipients once or count original only? Preserve per-target/current-turn caps and each source's no-resource/no-retaliation/no-healing flags. Paladin sources bar resource/retaliation; Crown Undying has explicit finite healing and Linked Ward/Unbroken Covenant have explicit tempHP results. Determine actual absorbed basis and priorities without counting overkill. Can blocked/capped healing restore an entitlement? (Expected no.)
6. Limits: shared Paladin1redirection event/round and exactly one Paladin redirection feature/event; Crown Undying permits2 DIFFERENT ally events with totalL+M/round, never2transfers on same event. Final Stand says all damage until next source start but shared cap says1event/round. Is Final Stand a source-specific cap exception, or constrained? Its operation would be materially different: resolve explicitly. Multiple sources owned by different characters also need per-root no-chain rules.
7. Protective Stance reduces ally byS+M and self takes that much unpreventable damage. Cap to actual available damage or can it harm protector for excess nonexistent damage? Shared Breath/Veinlock optional amounts likewise bounded by available packet. Guardian Tissue reduces one-third, Redirecting Palm 'reduce ... by half, rounded down' means preventedfloor(packet/2), retainedceil; forcecounter=min(prevented,L). Confirm source-specific rounding and no second ordinary defense on the transfer, while a NEW forcecounter is a separately defendable event.
8. Preventive Bloom absorbs next10+OracleL damage: finite buffer across packets or only one packet? Expiry/ending rider precise. Pure damage prevention (Ancestral Guardian, Elemental Absorption) isn't transfer and cannot create a corpse/resource event. Transfusion/ChannelLife/BloodSacrifice/ProfaneExchange/Flesh-to-RP costs remain direct HP loss outside the damage pipeline.

We need a procedure and exact binding of each39source, not a claim of full monster/spell/all-game semantics. Identify any additional source evidence needed before implementation.
'''
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
shared=(ROOT/'docs/mechanics/CLASS_PLAYTEST_RULES.md').read_text(encoding='utf-8')
shared=shared.split('## Damage, healing, stacking and companions',1)[1].split('## Ordinary spells:',1)[0]
lines=[questions,'## Preserved shared-class baseline (frozen file; quoted, not edited)\n'+shared]
for r in data['classRecords']:
 if r['kind']=='class-card':
  c=r['card'];lines.extend(['## '+c['id'],json.dumps({k:c.get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')},ensure_ascii=False)])
 else:lines.extend([f"## {r['owner']}.engine[{r['engineIndex']}]",r['text']])
(HERE/'CODEX_REDIRECTION_CONFERENCE.md').write_text('\n\n'.join(lines),encoding='utf-8')
print('Prepared exact39-source conference, not submitted:',sum(len(x) for x in lines),'characters')
