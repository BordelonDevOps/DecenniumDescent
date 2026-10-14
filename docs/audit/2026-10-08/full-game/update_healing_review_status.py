from pathlib import Path
import json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
p=HERE/'REVIEW_STATUS.md';s=p.read_text(encoding='utf-8')
s=s.split('## Healing and death conference in progress')[0]+'''## Healing and death implementation review in progress

The [first proposal](GPT_HEALING_DEATH_FIRST_REVIEW.md), [68-source supplement review](GPT_HEALING_SUPPLEMENT_REVIEW.md) and [seven final boundaries](GPT_HEALING_FINAL_BOUNDARIES.md) classify147 exact class passages and propose six individual ordinary spells. All153 source records pass integrity checks. The [remaining131 source packet](CODEX_HEALING_REMAINING_CONFERENCE.md) is prepared for its separate discussion; no source has been discarded based on a lexical scan.

The [working guide](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_DEATH_PLAYTEST.md), helper code,155 tests and120 unchanged Core damage states have been sent in the [exact implementation packet](CODEX_HEALING_IMPLEMENTATION_REVIEW.md). This includes two-pass healing, damage metrics, survival ordering, death-save rerolls, delayed recovery, retained lethal tracks, persistent resurrection histories, identity duplication prevention and causal healing limits. The passive-regeneration excess-conversion eligibility and Spiral/Ward phase interaction remain explicit review questions.

Control passes150 checks plus9,393 Speed states; its prior148-case closure remains recorded, with2 new damage-quantity clarification cases under this healing review. Custom conditions pass98 cases, with14 cure-presence corrections awaiting exact closure. All six complete spell drafts remain inactive; the operational catalog is still72 drafts with776 unfinished. Temporal participant fields are tested, but full world/equipment/clock restoration is deferred to its own source conference. DD24 and the whole-game goal remain open.
'''
p.write_text(s,encoding='utf-8')
p=ROOT/'docs/mechanics/DEVELOPMENT_ROADMAP.md';s=p.read_text(encoding='utf-8')
s=s.replace('37 selected','155 selected').replace('37 checks','155 checks').replace('37 reference','155 reference')
p.write_text(s,encoding='utf-8')
p=ROOT/'data/playtest/game_development_coverage.json';d=json.loads(p.read_text(encoding='utf-8'))
for row in d['aspects']:
 if row['number']==24:
  row['status']='healing-death-exact-implementation-review'
  for field,paths in {
   'reviewEvidence':['GPT_HEALING_SUPPLEMENT_REVIEW.md','GPT_HEALING_FINAL_BOUNDARIES.md','CODEX_HEALING_IMPLEMENTATION_REVIEW.md'],
   'sourceEvidence':['HEALING_REMAINING_SOURCE_CANDIDATES.json']}.items():
   for name in paths:
    path='docs/audit/2026-10-08/full-game/'+name
    if path not in row[field]:row[field].append(path)
  row['openIssues']=['Exact implementation review of153 selected source records; six complete ordinary spell objects remain inactive.',
   'Discuss all131 remaining class matches individually and audit healing content in other domains.',
   'Resolve passive Reserve excess conversion and Spiral/Ward phase clarification.',
   'Complete separate temporal topology/equipment/clock package; no full Time Loop activation here.']
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'data/playtest/control_state_bindings.json';d=json.loads(p.read_text(encoding='utf-8'))
scope={'name':'Positive packet versus numeric damage','status':'IN_REVIEW exact healing implementation',
 'rule':'Wrathful Brand/when-damaged predicates use resolvedDamage>0; numeric actualDamageDealt is temp absorption plus actual HP packet loss. Divine Judgment positive numeric0 reflects minimum1 and consumes actual turn; resolved0 does neither.',
 'reviewEvidence':['docs/audit/2026-10-08/full-game/GPT_HEALING_FINAL_BOUNDARIES.md']}
d['pendingScopes']=[s for s in d.get('pendingScopes',[]) if s['name']!=scope['name']]+[scope]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Updated live status; preserved historical closures and open whole-game gates.')
