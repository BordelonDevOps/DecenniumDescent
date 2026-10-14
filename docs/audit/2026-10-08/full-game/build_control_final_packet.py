from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
data=json.loads((ROOT/'data/playtest/control_state_bindings.json').read_text(encoding='utf-8'))
report=json.loads((ROOT/'docs/mechanics/CONTROL_PLAYTEST_VALIDATION.json').read_text(encoding='utf-8'))
parts=['''# Implemented disposition of exact control findings

All four material findings are fixed. Please inspect these exact updated helpers/tests and the changed binding excerpt, then explicitly give bounded closure if sound, or identify a remaining concrete defect. DD16/DD18, all-card execution, disease/curse catalogs, death/replacement/resurrection and other previously named broader work remain OPEN.

1. Guiding Star now exposes begin_ally_attack before rolling, consumes/returns the +2 and issues a unique mark-specific attack token. resolve_ally_attack resolves once after outcome; foreign/duplicate tokens reject. Suppression/illegal starts create no token/spend. Expiry/suppression before hit resolution grants no S; no refund to prior bonus. Tests include natural12+modifier1+pre-roll2 reachingAC15, miss then later hit, suppression and cross-mark replay.
2. Current-turn endpoint now returns ordered ClockMarker(seconds,phase): application/resolution10, expiry20, next event30; ordinary absolute timestamps usephase0. SpeedRecord operative/refresh and Balanced Elements extension understand phase ordering. A real SpeedRecord created at time3 during end-resolution is operative at(3,10), expiredat(3,20), gonebefore(3,30). No epsilon. Existing unrelated regular marker helpers remain unchanged. New tests exercise the actual lifecycle and Balanced Elements' connection to phased records.
3. All seven listed fallback components have conditional slowed-foe metadata. Spiral Opens has separate player-speed-zero component; forced-echo is not tagged. Binding validator asserts these memberships and exclusions.
4. Stars Revelation Mastery is HOOK. modifiers/reader references are separate fields; it authorizes a later enhanced Guiding Bolt component only when its option is selected. Actual Guiding Bolt lists that conditional component. Mage Arch Mastery explicitly modifies Coldflat/Glacier and all three already-reviewed Focus fire profiles (including Elemental Bolt). Flask BOOK wrapper references Burn/Root/Weaken, applies none itself. Enhanced Attunement and Balanced Elements have modifier links.

The two ordinary cold slows now have explicitly reviewed elemental tags. Fusion records the NEW missing Fire+Cold endpoint; Cascade's source clocks are explicit. The guide already correctly limits Carrion history to source-family/corpse, across owners. Corrected guide also preserves that Incapacitated by itself does NOT prohibit movement.

PASS123 interface cases +9,393 Speed states. PASS219 exact source objects; PASS219bindings/180component identities with modifier/reference link roles. Original source cards, books, spells untouched. Existing57custom/14hook/114source periodic registry unchanged except the reviewed JudgmentBrand3target-round endpoint clarification.

The next independent candidate inventory contains74classcards5engines and6dormant ordinary spell objects about healing/death. Those spells remain dormant, no operational promotion yet. After this bounded closure we will confer on death/zeroHP/HP-floor/recovery/resurrection/soul interfaces against those exact sources.

## Exact corrected files
''']
for rel in ('tools/control_playtest_rules.py','tools/validate_control_playtests.py','tools/validate_control_bindings.py'):
 parts.extend([f'\n### {rel}\n\n```python\n',(ROOT/rel).read_text(encoding='utf-8'),'\n```\n'])
parts.append('\n## Changed application/modifier/reference bindings and metadata\n\n```json\n')
selected=('stars-revelation-mastery','guiding-bolt','flask-use','elemental-mastery','enhanced-elemental-attunement','balanced-elements','the-spiral-opens','elemental-fusion','cascade-storm','ray-of-frost','frost-arrow')
parts.append(json.dumps([{k:b[k] for k in ('bindingId','classification','componentIds','modifiesComponents','referencesComponents','operationalOverrides')} for b in data['bindings'] if str(b['sourceId']).split('.')[-1] in selected],ensure_ascii=False,indent=2))
parts.append('\n```\n\n```json\n')
parts.append(json.dumps([c for c in data['componentIndex'] if 'soft-fallback' in c['mechanicalId'] or c['mechanicalId'] in ('oracle.spiral-opens.forced-echo','oracle.spiral-opens.player-speed-zero','ordinary.ray-of-frost.slow','ordinary.frost-arrow.slow')],ensure_ascii=False,indent=2))
parts.append('\n```\n')
(HERE/'CODEX_CONTROL_FINAL_DISPOSITION.md').write_text(''.join(parts),encoding='utf-8')
print(f'Final disposition exact packet: {sum(map(len,parts))} characters')
