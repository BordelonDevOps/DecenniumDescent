"""Run only after saving the actually confirmed final clock addendum."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
GAME=HERE.parents[3];ROOT=GAME/'DescentReviewChanges/ReviewBible'
closure='docs/audit/2026-10-08/full-game/GPT_FORM_TEMP_HP_FINAL_CLOSURE.md'
reply=(GAME/closure).read_text(encoding='utf-8')
assert reply.startswith('# GPT confirmed form and temporary-HP closure')
assert '165' in reply and 'REVIEWED / reference-VALIDATED' in reply
path=ROOT/'docs/mechanics/FORM_TEMP_HP_PLAYTEST_VALIDATION.json'
report=json.loads(path.read_text(encoding='utf-8'))
assert report['status']=='PASS' and report['checks']==165 and report['arbitrationDamageScenarios']==1053
report['reviewStatus']='REVIEWED / reference-VALIDATED: selected175+5 form/buffer roles only'
report['reviewClosure']=closure
path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ROOT/'data/playtest/form_temphp_bindings.json';data=json.loads(path.read_text(encoding='utf-8'))
data['status']='REVIEWED / reference-VALIDATED: selected175+5 roles and26 Druid profiles;165 checks/1053 shield-damage scenarios;9 named components remain deferred'
data['reviewClosure']=closure
for r in data['bindings']:
    deferred=r['bindingId'] in data['deferredComponentIds']
    r['status']='DISCUSSED / DEFERRED: named component requires its own completion batch' if deferred else 'REVIEWED / reference-VALIDATED: selected grant/form interface or classified prior/guard boundary only; not full-card completion'
    r['reviewEvidence']=list(dict.fromkeys(r['reviewEvidence']+['GPT_FORM_TEMP_HP_IMPLEMENTATION_FINDINGS.md','GPT_FORM_TEMP_HP_CORRECTION_REVIEW.md','GPT_FORM_TEMP_HP_FINAL_CLOSURE.md']))
    r['operationalOverrides']=list(dict.fromkeys(r['operationalOverrides']+['Final clock correction: one owner phase across regular starts, downtime and actual rests, initially anchored to actual supplied time; source Recharge2 persists across shifts. Form IDs reserved globally in the shared world ledger.']))
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ROOT/'data/playtest/druid_form_profiles.json';profiles=json.loads(path.read_text(encoding='utf-8'))
profiles['status']='REVIEWED / reference-VALIDATED:26 source-qualified profiles within selected form/buffer interface'
profiles['reviewClosure']=closure
for p in profiles['profiles'].values():p['integrationStatus']='REVIEWED: bounded form profile; full individual rider execution remains with canonical systems'
path.write_text(json.dumps(profiles,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ROOT/'docs/mechanics/FORM_TEMP_HP_PLAYTEST.md';text=path.read_text(encoding='utf-8')
old='**Implementation draft; final clock addendum confirmation pending.**'
text=text.replace(old,'**REVIEWED / reference-VALIDATED — selected form and temporary-HP interfaces.**')
text=text.replace('GPT has approved the corrected 163-check reference; two further clock-initialization checks pass and are awaiting final confirmation.',
                  'GPT approved the corrected reference and its clock-initialization addendum; 165 contract checks and 1,053 shield/damage scenarios pass.')
text+='\n[Confirmed notebook closure](../../../../'+closure+') records the bounded approval. The five named transformation/buffer spell proposals continue separately; their original deferred classification is retained as review history.\n'
path.write_text(text,encoding='utf-8')
path=ROOT/'data/playtest/game_development_coverage.json';coverage=json.loads(path.read_text(encoding='utf-8'))
for r in coverage['aspects']:
    if r['id'] not in ('DD-08','DD-09','DD-24','DD-26','DD-35','DD-41'):continue
    r['closure']='open';r['status']='selected-interfaces-closed-remainder-integrating'
    r['reviewEvidence']=list(dict.fromkeys(r['reviewEvidence']+[closure]))
    r['draftEvidence']=list(dict.fromkeys(r['draftEvidence']+['DescentReviewChanges/ReviewBible/docs/mechanics/FORM_TEMP_HP_PLAYTEST.md']))
    r['validationEvidence']=list(dict.fromkeys(r['validationEvidence']+['DescentReviewChanges/ReviewBible/docs/mechanics/FORM_TEMP_HP_PLAYTEST_VALIDATION.json']))
    r['openIssues']=[v for v in r['openIssues'] if not v.startswith('Next form/tempHP corpus175')]
    note='Selected form/tempHP175+5 interface closed with26 Druid profiles,165 contract checks and1053 shield/damage scenarios. Includes exact grant identity/lifetimes, same-body transitions, global instance IDs and combat/downtime recharge. Full cards, equipment/weapon taxonomy and named deferred components remain open.'
    if note not in r.setdefault('completedScopes',[]):r['completedScopes'].append(note)
    note='Continue full domain criteria, including item/anatomy matrix, natural-weapon taxonomy, incomplete feat and spell clauses, Time Loop and runtime. Five named transformation/buffer spell source conference is in progress.'
    if note not in r['openIssues']:r['openIssues'].append(note)
path.write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ('README.md','REVIEW_STATUS.md'):
    path=HERE/name;text=path.read_text(encoding='utf-8')
    text+='\n## Form and temporary-HP bounded closure\n\nThe [confirmed notebook disposition](GPT_FORM_TEMP_HP_FINAL_CLOSURE.md) closes the selected175+5 interface:26 Druid profiles,165 checks and1,053 shield/damage scenarios. Original source objects remain preserved. All nine named deferred components and wider game criteria remain open. The [next five-spell source conference](CODEX_TRANSFORMATION_SPELL_CONFERENCE.md) has been visibly submitted; proposals require separate implementation review before promotion. The [eight-feat follow-up](CODEX_BUFFER_FEAT_COMPLETION_PREPARED.md), including Lifeleech as Soul Cage’s exact dependency, is prepared but not submitted.\n'
    path.write_text(text,encoding='utf-8')
print('Recorded actual bounded175+5 closure; all broader domains and named incomplete components remain open.')
