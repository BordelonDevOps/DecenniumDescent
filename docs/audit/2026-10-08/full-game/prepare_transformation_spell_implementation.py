"""Validate candidate and assemble the exact actual-code notebook review packet."""
from pathlib import Path
import json, subprocess, sys, hashlib

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
form_report=ROOT/'docs/mechanics/FORM_TEMP_HP_PLAYTEST_VALIDATION.json'
previous=json.loads(form_report.read_text(encoding='utf-8'))
for script in ('validate_transformation_spell_sources.py','validate_transformation_spell_playtests.py','validate_form_temphp_playtests.py'):
    run=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools'/script)],capture_output=True,text=True,encoding='utf-8')
    print(run.stdout.strip())
    if run.returncode:raise SystemExit(run.stderr)
current=json.loads(form_report.read_text(encoding='utf-8'))
assert current['checks']==previous['checks'] and current['arbitrationDamageScenarios']==previous['arbitrationDamageScenarios']
# Preserve actual old-scope closure; candidate admission bridge is separately pending.
current.update({k:v for k,v in previous.items() if k not in current or k=='reviewStatus'})
current['candidateSpellBridge']={'status':'REGRESSION PASS; GPT review pending','change':'Shared spell_anatomies registry + Druid admission guard only',
    'evidence':'CODEX_TRANSFORMATION_SPELL_IMPLEMENTATION.md'}
form_report.write_text(json.dumps(current,indent=2)+'\n',encoding='utf-8')

names=['data/playtest/spell_drafts/candidate_transformations.json','data/playtest/spell_form_profiles.json',
       'docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md','tools/transformation_spell_playtest_rules.py',
       'tools/validate_transformation_spell_playtests.py','docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST_VALIDATION.json',
       'docs/mechanics/TRANSFORMATION_SPELL_SOURCE_VALIDATION.json']
manifest=[{'path':n,'sha256':hashlib.sha256((ROOT/n).read_bytes()).hexdigest(),'bytes':(ROOT/n).stat().st_size} for n in names]
packet='''# Five-spell actual implementation review

Please independently review this actual candidate implementation against your first proposals, twelve boundary decisions and seven final interfaces. These are Harmonic Bulwark, Polymorph, Shapechange, True Polymorph, Mass Polymorph. All five remain inactive candidate records: the active catalog is still78 operational/770 unfinished. No original spell objects, class gates or frozen class rules were changed.

Validation:191 contract checks plus729 Mass occupancy scenarios compare the pairwise preflight against exhaustive independent save outcomes. All5 exact sources and6 Core entries plus1 possible alias validate. Existing form/buffer suite still passes165 checks plus1053 damage/arbitration cases. The frozen class packet hash remains adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81.

The ONLY existing-helper change is BufferLedger.spell_anatomies={} and DruidState.shift rejects while its owner appears in that shared registry, before payment. Suppression leaves the entry occupied; actual ending removes it. The full new helper, data, readable guide, actual tests and reports follow below. They are contract references, not a whole runtime engine or numerical balance claim.

Review particular integration choices:

1. Same-caster new concentration preflight projects the old target link back to root anatomy before deciding prospective target eligibility and footprint. It skips precedence against that already-ending old record. A slot released by the mandatory end of shaping concentration can be used by a newly created object creature. A permanent occupied slot still blocks preflight. This avoids both transient creature-target-to-object mistakes and charging an impossible cast. Confirm the derived transaction interpretation.
2. Slot sponsorship persists through another caster's successful creature-profile replacement; close-and-recapture equipment occurs atomically, without releasing that sponsor. Actual object output releases it. Failed or countered replacement leaves only the anatomy appropriate to the earlier concentration commit.
3. Suppression keeps the original meld set and does not expose/rebuild/recapture it in this candidate helper. It returns root anatomy and queues a placement check. Please explicitly settle whether original melded items become temporarily usable while suppressed, or remain inaccessible; your last answer fixed identities/recapture but did not expressly state accessibility. This is the only known remaining equipment interpretation needing your exact ruling.
4. A suppressed shaping link keeps concentration and its deadline and may stabilize. The helper prohibits using its suppressed profile attack/internal Shapechange switch; underlying root-anatomy actions are handled by the normal character engine. Confirm switching is not newly authorized while the spell is suppressed.
5. Mandatory-reversion geometry is an explicit whole-game dependency. This helper requests a same-anchor placement check, exposes placementConflict, and never teleports or invents crushing damage. No claim that the geometry subsystem is complete.
6. Spellgranted natural attacks have the agreed printed damage types, no automatic caster spell/weapon-only proc authorization. Magical-vs-physical-defense recognition beyond an exact source is deliberately not invented here. Confirm whether the new finite profiles should expressly carry a magical-attack flag, or retain the ordinary exact-source taxonomy.

Please distinguish actual blockers in these five bounded procedures from broader future systems/balance work. If there are blockers, give reproducible cases and the precise desired behavior. Do not close or promote the package while any actual blocker remains. If the candidate is otherwise sound, settle the named interpretation choices and state its exact review scope. All original information remains preserved.

## Exact file manifest

'''+json.dumps(manifest,indent=2)+'\n'
for name in names:
    path=ROOT/name
    packet+='\n## '+name+'\n\n```'+('python' if path.suffix=='.py' else 'json' if path.suffix=='.json' else 'markdown')+'\n'+path.read_text(encoding='utf-8')+'\n```\n'
packet+='\n## Existing Druid bridge exact additions\n\n```python\n# BufferLedger.__init__:\nself.spell_anatomies={}\n# DruidState.shift, before all payment:\nrequire(self.owner not in self.buffers.spell_anatomies,\n        "End active spell anatomy through its legal procedure before Druid Shapeshift")\n```\n'
(HERE/'CODEX_TRANSFORMATION_SPELL_IMPLEMENTATION.md').write_text(packet,encoding='utf-8')
(HERE/'TRANSFORMATION_SPELL_IMPLEMENTATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Prepared actual implementation packet:',len(packet.encode('utf-8')),'bytes; NOT submitted yet.')
