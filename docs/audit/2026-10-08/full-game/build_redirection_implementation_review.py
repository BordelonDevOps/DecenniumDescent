from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
lines=['''# Exact39-source damage-sharing implementation review

Codex → Calibration Review. Please reply BELOW16,000 characters. Review this exact bounded helper, tests, guide and source binding contracts against your39-source proposal and six corrections. Current88 checks/186 conservation states PASS, plus39 exact originals preserved and2 supporting Tinker engines. Please challenge defects before closure; fullgame/all-source defense order/companion lifecycle remain open.

Concrete remaining questions:
1. Mandatory offers across stages: helper accepts one already legally selected operation, forbids retransfer of retained and transferred branches. Does post-defense mandatory Aegis/Final Stand preempt a pre-mitigation optional Bloodbond offer? Need explicit ordering without a hypothetical defense preview consuming Bloom/prevention twice. Proposed phase ordering: pre-mitigation offers first, and automatic-before-optional only among SAME-STAGE eligible offers; if premitigation transfer used, root guard suppresses postphase transfers. This is a clarification of earlier broadly worded mandatory priority and must be explicit if accepted. Alternatively author a coherent cross-stage procedure.
2. Crown ledger code allows one ordinary+one Crown in either order while Crown active; two ordinary never. Text 'second must Crown' intended permission rather than chronology? If Crown first, is ordinary later legal? Code uses total2/ordinary1 and originalsource state/target legality caller. Crown nominal healing entitlement committed before blocked target healing; no refill.
3. Device helper uses ONLY damage-to0 destruction, no organic Wounds/death saves. Supporting exact Tinkerengine1/2 below. Device reconstruction/companion lifetime remains separate open package. Is that sufficient bounded interface? Emergency transferred damage does not make drone hit by enemy attack; no retaliation consumer. Do not grant unsupplied destruction-resource rewards.
4. GuardianPulse free-counter guard has explicit no-free-attack/no-Action generation and waits full incomingattack resolution; can retarget a freecounter but cannot generate a further freecounter from it. Palmforcecounter NEWroot normaldefenses/no originalattackidentity, with no-free/action/copy guards. Review source restrictions and inherited flags rather than assuming anynewdamageisacopy.

The helper caller contract deliberately leaves ownership/acquisition, source costs/actions/range/willingness, active states, per-source cadence and source-native rider legality to the stated procedure. It is not a complete combat engine. One DamageRoot is ONE original target damage packet, NOT all targets of a cast. Root totals require completed terminal recipients and source qualification filters.
''']
data=json.loads((ROOT/'data/playtest/redirection_bindings.json').read_text(encoding='utf-8'))
lines += ['## Exact source contracts and supporting engines',json.dumps(data,ensure_ascii=False,indent=2)]
for path in ('tools/redirection_playtest_rules.py','tools/validate_redirection_playtests.py',
             'docs/mechanics/REDIRECTION_PLAYTEST_VALIDATION.json','docs/mechanics/REDIRECTION_SOURCE_VALIDATION.json',
             'docs/mechanics/DAMAGE_SHARING_PLAYTEST.md'):
    lines += ['## Exact '+path,(ROOT/path).read_text(encoding='utf-8')]
(HERE/'CODEX_REDIRECTION_IMPLEMENTATION_REVIEW.md').write_text('\n\n'.join(lines),encoding='utf-8')
print('Prepared exact redirection helper/bindings/tests/guide review.')
