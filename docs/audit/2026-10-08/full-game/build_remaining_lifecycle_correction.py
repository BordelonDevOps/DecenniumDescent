from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
code=(ROOT/'tools/remaining_lifecycle_playtest_rules.py').read_text(encoding='utf-8')
tests=(ROOT/'tools/validate_remaining_lifecycle_playtests.py').read_text(encoding='utf-8')
guide=(ROOT/'docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST.md').read_text(encoding='utf-8')
report=json.loads((ROOT/'docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST_VALIDATION.json').read_text(encoding='utf-8'))
assert report['status']=='PASS' and report['checks']==129
lines=['# Remaining lifecycle Choir provenance correction','',
 'Codex → Calibration Review. The one reported blocker is corrected. Please review the exact changed code/guide/regressions below and explicitly dispose of the selected80+5 interface.129 targeted checks now pass; the previous124 transactions remain. No source originals or frozen support paragraphs changed. All other reviewed behavior and excluded full-card/tempHP/form/TimeLoop/global-body/runtime work remain unchanged.',
 '', 'Ordinary outgoing burst no longer imposes generic noDamageTriggers, noDeathTriggers, noRetaliation, noResourceGeneration or noCopyChain. It identifies the Cleric source/owner and only its own no-Choir-healing/no-fanatic-body-resource/no-extra-explosion restrictions. Incoming sealed-zero suppression remains exactly as reviewed. The ambiguous attack profile resourceEligible:false field was also renamed attackerOwnResourcePool:false: a created attacker has no independent resource pool; this no longer suggests blanket suppression of eligible original-owner or target-side features. Actual Dark Conviction encounter/turn/victim/frequency predicates remain caller source checks.',
 '', '## Exact burst and damage functions',code[code.index('    def burst('):code.index('    def end_choir(')],
 '', '## Exact selected creature attack profile',code[code.index('@dataclass\nclass RemainingCreature'):code.index('@dataclass\nclass Structure')],
 '', '## Exact regression segment',tests[tests.index("    suppressed=w.damage"):tests.index("    events=w.end_choir")],
 '', '## Corrected tabletop text',next(p for p in guide.split('\n\n') if p.startswith('Bursts are ordinary source-native')),
 '', '## Validation',json.dumps({'status':report['status'],'checks':report['checks'],'scope':report['scope']},indent=2),
 '', '## Artifact digests']
for name in ['tools/remaining_lifecycle_playtest_rules.py','tools/validate_remaining_lifecycle_playtests.py','docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST.md']:
 lines.append(name+' '+hashlib.sha256((ROOT/name).read_bytes()).hexdigest())
(HERE/'CODEX_REMAINING_LIFECYCLE_CORRECTION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Prepared exact Choir correction and129-check evidence.')
