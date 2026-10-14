from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
guide=ROOT/'docs/mechanics/CONTROL_STATES_PLAYTEST.md'
guide.write_text(guide.read_text(encoding='utf-8').replace('has123 targeted checks','has148 targeted checks'),encoding='utf-8')
parts=['''# Final control clock correction — exact implementation

Your remaining future-end phase finding is corrected. Please give explicit bounded REVIEWED / reference-VALIDATED closure if sound; identify only concrete remaining defects within the supplied control interface scope. DD16/DD18 and the full game remain OPEN.

All reference consumers now require typed ClockMarker deadlines. SpeedRecord, GuidingStarMark, WrathfulBrand reject ambiguous numeric expiries. regular_control_endpoint adapts the unchanged reviewed combat marker_deadline helper to phase20 for ALL future turn ends (source, target, Nth), phase0 for starts. current_turn_endpoint uses phase20 for actual current ends. absolute_deadline usesphase0. Balanced Elements requires its following target end atphase20; governing source maximum retains its actual start/end/absolute phase.

Combat marker_deadline returns exact Fraction seconds. ClockMarker now preserves exact Fraction values (including fractional virtual markers) instead of truncating or rejecting them; finite nonnegative numeric times only, bool/NaN/infinity rejected. It orders by seconds thenphase. This adds event order, not an epsilon offset.

PASS148 control checks and9,393 Speed invariants. New lifecycle tests prove futuretarget/sourceend at(9,10) remains active, at(9,20) expires, at(9,30) absent; hostile2rounds gets(15,20); stronger expires after finalend effects thenweaker resumes; GuidingStar worksduringendphase10; fractional9.5markerspreserved. Old arithmetic tests explicitly use absolute_deadline rather than pretending to model turn ends.

219 exact sources/219bindings/180component identities and previously accepted fourfixes unchanged. Selected helpers are not a full card engine. The next source conference will address healing/death/zeroHP/resurrection.
''']
for rel in ('tools/control_playtest_rules.py','tools/validate_control_playtests.py'):
 parts.extend([f'\n## {rel}\n\n```python\n',(ROOT/rel).read_text(encoding='utf-8'),'\n```\n'])
(HERE/'CODEX_CONTROL_CLOCK_FINAL.md').write_text(''.join(parts),encoding='utf-8')
print(f'Clock disposition packet saved: {sum(map(len,parts))} characters')
