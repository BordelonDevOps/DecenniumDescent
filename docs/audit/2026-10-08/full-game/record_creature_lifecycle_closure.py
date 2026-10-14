"""Record actual final scoped approval without promoting deferred form/tempHP cards."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
GAME=ROOT.parents[1]
evidence=HERE/'GPT_CREATURE_LIFECYCLE_FINAL_CLOSURE.md'
reply=evidence.read_text(encoding='utf-8')
assert reply.startswith('# GPT confirmed creature lifecycle closure')
assert 'I find no remaining concrete blocker' in reply and 'REVIEWED / reference-VALIDATED' in reply
closure='docs/audit/2026-10-08/full-game/GPT_CREATURE_LIFECYCLE_FINAL_CLOSURE.md'
report_path=ROOT/'docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST_VALIDATION.json'
report=json.loads(report_path.read_text(encoding='utf-8'))
assert report['result']=='PASS' and report['checkCount']==121 and report['rangerConversionStates']==2800
status='REVIEWED / reference-VALIDATED: selected lifecycle roles;100+5 source classifications, full form/tempHP effects deferred'
path=ROOT/'data/playtest/creature_lifecycle_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
data['status']=status;data['reviewClosure']=closure
for r in data['bindings']:
    deferred=r['classification'].startswith(('FORM','THP'))
    r['status']='DISCUSSED / full form-tempHP effects DEFERRED; only stated guard/dependency classified' if deferred else 'REVIEWED / reference-VALIDATED: supplied lifecycle/command/modifier/guard role only'
    r['reviewEvidence']=list(dict.fromkeys(r['reviewEvidence']+['GPT_CREATURE_LIFECYCLE_IMPLEMENTATION_FINDINGS.md','GPT_CREATURE_LIFECYCLE_FINAL_CLOSURE.md']))
    r['operationalOverrides']=[v.replace('Exact original text remains preserved.','Exact original text remains preserved; final approved guide/helper applies only to the stated interface.') for v in r['operationalOverrides']]
    r['openIssues']=[v for v in r['openIssues'] if not v.startswith('Exact implementation review pending.')]
    r['openIssues'].append('Full card effects, full forms/tempHP, wider companion families and runtime remain outside this bounded source-role disposition.')
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report['status']=status;report['reviewClosure']=closure
report_path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
path=ROOT/'docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md'
text=path.read_text(encoding='utf-8').replace('**Implemented candidate; exact GPT implementation review pending.**',
    '**REVIEWED / reference-VALIDATED: 121 targeted checks and 2,800 Ranger conversion states.**')
line='\n[Final notebook disposition](../../../../docs/audit/2026-10-08/full-game/GPT_CREATURE_LIFECYCLE_FINAL_CLOSURE.md) approves only the selected100+5 source roles and interfaces described here. Incidental full-form/tempHP effects remain deferred.\n'
if line not in text:text+=line
path.write_text(text,encoding='utf-8')
path=ROOT/'tools/creature_lifecycle_playtest_rules.py'
text=path.read_text(encoding='utf-8').replace('Bounded creature lifecycle candidate. Exact implementation review pending.',
    'Reviewed bounded creature lifecycle reference; selected100+5 roles only.')
path.write_text(text,encoding='utf-8')
path=ROOT/'data/playtest/game_development_coverage.json'
coverage=json.loads(path.read_text(encoding='utf-8'))
for ident in ('DD-24','DD-35'):
    row=next(r for r in coverage['aspects'] if r['id']==ident)
    row['status']='selected-interfaces-closed-remainder-integrating';row['closure']='open'
    if closure not in row['reviewEvidence']:row['reviewEvidence'].append(closure)
    row['openIssues']=[v for v in row['openIssues'] if not v.startswith(('Five-family creature candidate:','Remaining creature companion, form/tempHP, copy and other catalog interfaces'))]
    note='Selected creature lifecycle/command/body identity:100 source roles+5 frozen supports jointly reviewed;121 checks and2,800 Ranger HP-conversion states. Full forms/tempHP and whole-card execution are excluded.'
    if note not in row.setdefault('completedScopes',[]):row['completedScopes'].append(note)
    note='Next remaining lifecycle slice:80 passages (74 original candidates+6 semantic supplements). Full Druid/forms/tempHP candidate corpus124 includes all66 Druid passages; Core/feat/spell/semantic supplements still needed. Wizard elite binding/return, Beast rest/keen-senses and global corpse cleanup remain open.'
    if note not in row['openIssues']:row['openIssues'].append(note)
path.write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ROOT/'docs/mechanics/DEVELOPMENT_ROADMAP.md'
text=path.read_text(encoding='utf-8')
line='- [Selected creature companion lifecycle](CREATURE_LIFECYCLE_PLAYTEST.md):100 source roles+5 frozen supports jointly reviewed,121 checks and2,800 Ranger conversion states. Shared commands, physical-body identity, Auto-Raise, Mage return, Mirror/Reflective and Druid summon dependencies are bounded. Remaining companions, Wizard elite acquisition/return, full forms/tempHP and broader catalogs stay open.'
if line not in text:text+='\n'+line+'\n'
path.write_text(text,encoding='utf-8')
for name in ('README.md','REVIEW_STATUS.md'):
    path=HERE/name;text=path.read_text(encoding='utf-8')
    note='\n## Creature lifecycle bounded closure\n\n[Final corrected packet](CODEX_CREATURE_LIFECYCLE_BODY_CORRECTION.md) received [GPT confirmed closure](GPT_CREATURE_LIFECYCLE_FINAL_CLOSURE.md).121 checks/2,800 Ranger conversion cases and100+5 source integrity pass; existing device132/1,200 suite also passes. The same real Ranger body becomes unavailable as a corpse on independent resurrection and available again on actual later death without a duplicate identity. Full form/tempHP and other expressly excluded effects remain open. Next prepared lifecycle conference80+5; separate form/tempHP source candidates124 including full66-passage Druid corpus. Whole game remains active/incomplete.\n'
    if '## Creature lifecycle bounded closure' not in text:text+=note
    path.write_text(text,encoding='utf-8')
path=GAME/'START_HERE.md';text=path.read_text(encoding='utf-8')
note='\nThe selected [creature companion rules](DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md) are jointly reviewed:100 source roles+5 shared paragraphs,121 checks and2,800 Ranger conversion cases. Temporary summons, persistent beasts, raised undead, commands and body identity have explicit boundaries. Full forms/tempHP, remaining companions and the rest of the game audit continue.\n'
if note not in text:text+=note
path.write_text(text,encoding='utf-8')
print('Recorded confirmed selected100+5 closure; deferred full effects and75-area goal remain open.')
