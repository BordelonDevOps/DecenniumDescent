"""Preserve a new correction packet; never overwrite the submitted first review."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
report=json.loads((ROOT/'docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST_VALIDATION.json').read_text(encoding='utf-8'))
assert report['status']=='PASS' and report['checks']==216 and report['massOccupancyScenarios']==729
names=['tools/transformation_spell_playtest_rules.py','tools/validate_transformation_spell_playtests.py',
       'docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md','data/playtest/spell_drafts/candidate_transformations.json',
       'data/playtest/spell_form_profiles.json','docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST_VALIDATION.json']
manifest=[{'path':n,'sha256':hashlib.sha256((ROOT/n).read_bytes()).hexdigest()} for n in names]
text='''# Transformation correction review, then eight exact feat sources

## First: independently review the two actual corrections

Your full implementation findings are preserved as GPT_TRANSFORMATION_SPELL_IMPLEMENTATION_FINDINGS.md. Neither blocker was ignored or promoted. Both are corrected in the actual code below;191 existing checks now become216 with25 explicit regressions, and all729 Mass occupancy scenarios still pass. Source objects/class access/frozen class rules remain unchanged. The previously tested Druid guard and its165/1053 regression result are unchanged by this correction.

Blocker1 correction: preflight recognizes an active True object anatomy as an existing transformation record, so a legal True replacement does not require a false fresh-outside-object certificate. Genuinely fresh outside objects still require it. Creature-origin identity now retains its initial CON save against an unwilling creature-profile replacement even while expressed as an object. Object-output replacement of that person requires willingness. Object-origin identities retain all restrictions and slot behavior. Tests cover both save success/failure, unwilling/willing object replacement, original HP identity, no new companion slot for a person, and object-origin object recasting into a fresh companion manifestation.

Blocker2 correction: reject() admits suppressed links, then checks current expressed action capability and creature origin. Willing Polymorph/Mass/shaping-True recipients can spend their original regular-turn Action while root creature anatomy is expressed under suppression, including a suppressed creature→object form. Unsuppressed object anatomy stays actionless. Object-origin identities receive no player-style rejection. Shapechange continues to use concentration release and cannot internally switch while suppressed. Tests cover each case and registry cleanup.

The guide and candidate cards also explicitly preserve your six dispositions: projected-root preflight, sponsor/control separation, inaccessible original meld set under suppression, no suppressed internal Shapechange switch, same-anchor geometry handoff and no generic magical-attack bypass flag. The wider geometry/item/attack-taxonomy/runtime/balance/human-playtest dependencies remain open.

Please inspect the actual corrections and regressions, then state whether these FIVE bounded spells and12 profiles are REVIEWED / reference-VALIDATED for provisional catalog promotion, or identify any remaining reproducible blocker. Do not imply the wider catalogs or game are complete. We have not promoted these candidates yet.

## Second, only if the five-spell corrections close

Continue our user-authorized comprehensive game development by discussing the eight EXACT full-feat sources appended after the implementation. Those feats are the next named incomplete clauses from our buffer audit. This is source discussion and candidate design only, not feat promotion or implementation approval. If a transformation blocker remains, prioritize that finding and defer the feat conference until corrected.

## Corrected implementation manifest

'''+json.dumps(manifest,indent=2)+'\n'
for n in names:
    p=ROOT/n
    text+='\n## '+n+'\n\n```'+('python' if p.suffix=='.py' else 'json' if p.suffix=='.json' else 'markdown')+'\n'+p.read_text(encoding='utf-8')+'\n```\n'
text+='\n# NEXT CONFERENCE — exact8 feats and prior reviewed interfaces\n\n'+(HERE/'CODEX_BUFFER_FEAT_CONFERENCE_READY.md').read_text(encoding='utf-8')
(HERE/'CODEX_TRANSFORMATION_CORRECTION_AND_FEAT_CONFERENCE.md').write_text(text,encoding='utf-8')
(HERE/'TRANSFORMATION_CORRECTION_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Prepared new correction plus conditional next conference:',len(text.encode('utf-8')),'bytes; NOT yet submitted.')
