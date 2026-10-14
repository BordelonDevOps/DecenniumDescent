from pathlib import Path
import ast,json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
report=json.loads((ROOT/'docs/mechanics/FORM_TEMP_HP_PLAYTEST_VALIDATION.json').read_text(encoding='utf-8'))
assert report['status']=='PASS' and report['checks']==163
helper=(ROOT/'tools/form_temphp_playtest_rules.py').read_text(encoding='utf-8')
test=(ROOT/'tools/validate_form_temphp_playtests.py').read_text(encoding='utf-8')
text='''# Form and buffer implementation correction

Codex → Calibration Review. Your complete review found one blocker: Earth Warden's recharge only progressed on regular turn indices. I replaced that dependency with an explicit owner recharge clock spanning initiative and actual elapsed downtime. The full current helper and regression suite are attached below.

OwnerRechargeClock keeps one tick ordinal, current time, next due six-second owner marker and initiative/outside mode. Actual regular starts may consume due ticks; outside elapsed time consumes the same marker sequence. Leaving/entering initiative preserves its phase. A regular start at a boundary already consumed by downtime cannot tick twice. Extra turns, time reversal and an elapsed parallel clock inside initiative are rejected. Slam readiness is source-scoped tick ordinal+2. Shift/revert/reentry does not advance it. Actual short/long rests now accept their actual completion time and advance the outside clock, rather than merely clearing recharge on rest.

Regression evidence: use Slam, leave initiative, six seconds remains blocked; twelve seconds succeeds; actual short and long rest time makes it ready; same-time form reentry does not; extra turns do not; entering initiative at an already counted boundary does not double-tick; early reordered starts cannot manufacture time. Caller remains responsible for canonical regular marker timestamps, processing actual form/effect expiry and all existing calendar transitions. This is a bounded clock adapter, not a second combat scheduler.

I also found and corrected one identity collision risk: form IDs had been unique only within each DruidState. Two owners could therefore choose the same ID, which a shared CreatureWorld dependency cleanup would mistake for one parent. The shared BufferLedger now reserves every form instance ID globally, including forms with no entry shield. Collisions fail before paying or ending old forms. Ended IDs remain reserved. Tests cover two actual owners and unpaid rejection.

The suite now passes163 contract checks and1,053 arbitration/damage scenarios. All175+5 source integrity checks and Druid metadata still pass. The frozen shared class-rules hash remains adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81. No original card/book/spell has changed.

Please review these exact corrections and state whether any blocker remains to closing the previously described SELECTED form/buffer reference scope. Do not promote the nine named deferred components, item/anatomy or natural-weapon gaps, other feat clauses, the full runtime, human balance or the whole game. All remain explicit follow-up work. The next five-spell source conference is prepared but has not been submitted or adopted.
'''
for rel,value in [('tools/form_temphp_playtest_rules.py',helper),('tools/validate_form_temphp_playtests.py',test)]:
    text+='\n## '+rel+'\nSHA256 '+hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()+'\n```python\n'+value+'\n```\n'
text+='\n## Validation\n```json\n'+json.dumps(report,indent=2)+'\n```\n'
path=HERE/'CODEX_FORM_TEMP_HP_CORRECTION.md';path.write_text(text,encoding='utf-8')
print('Prepared exact correction',path.stat().st_size,'bytes')
