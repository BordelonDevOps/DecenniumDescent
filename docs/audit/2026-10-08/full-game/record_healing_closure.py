"""Publish scoped review status only after real catalog promotion/validation."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[3]
ROOT=PROJECT/'DescentReviewChanges/ReviewBible'
ev='docs/audit/2026-10-08/full-game/GPT_HEALING_FINAL_CLOSURE.md'
assert 'CLOSED as REVIEWED' in (PROJECT/ev).read_text(encoding='utf-8')
manifest=json.loads((ROOT/'data/public/spell_playtests/manifest.json').read_text(encoding='utf-8'))
assert manifest['operationalDrafts']==78 and manifest['blocked']==770
sv=json.loads((ROOT/'docs/mechanics/HEALING_SPELL_CANDIDATE_VALIDATION.json').read_text(encoding='utf-8'))
assert sv['status']=='PASS' and all(s['operationalInCurrentCatalog'] for s in sv['spells'])
p=ROOT/'data/playtest/healing_death_bindings.json';d=json.loads(p.read_text(encoding='utf-8'))
d['status']='REVIEWED / reference-VALIDATED — selected153-source interface only'
for b in d['bindings']:
 if ev not in b['reviewEvidence']:b['reviewEvidence'].append(ev)
 b['status']='REVIEWED / reference-VALIDATED — classified components only'
 if b['sourceKind']=='ordinary-spell-catalog':b['status']='REVIEWED / reference-VALIDATED; promoted operational-playtest draft'
 b['openIssues']=['Full temporal implementation remains in dedicated package.'] if 'DEFER' in (b['classification'] or '') else []
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'tools/validate_healing_playtests.py';s=p.read_text(encoding='utf-8')
s=s.replace('IN_REVIEW; exact implementation not yet submitted','REVIEWED / reference-VALIDATED; selected interfaces only')
s=s.replace('implementation review pending.','bounded GPT closure recorded.')
p.write_text(s,encoding='utf-8')
p=ROOT/'tools/validate_control_playtests.py';s=p.read_text(encoding='utf-8')
s=s.replace('Prior148 checks reviewed; new positive-damage/numeric-damage clarification under healing implementation review','REVIEWED / reference-VALIDATED; original control plus healing damage clarification')
s=s.replace('Prior bounded review retained; healing clarification pending.','Bounded control and healing clarification reviews recorded.')
p.write_text(s,encoding='utf-8')
p=ROOT/'data/playtest/custom_condition_bindings.json';d=json.loads(p.read_text(encoding='utf-8'))
pending=[]
for scope in d.get('pendingScopes',[]):
 if scope['name']=='Suppressed-record cure correction':
  scope['status']='REVIEWED / reference-VALIDATED';scope['reviewEvidence']=ev
  d.setdefault('completedScopes',[]).append(scope)
 else:pending.append(scope)
d['pendingScopes']=pending
for rule in d['familyRules']:
 if rule['id']=='cure-presence-suppression' and ev not in rule['reviewEvidence']:rule['reviewEvidence'].append(ev)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'data/playtest/control_state_bindings.json';d=json.loads(p.read_text(encoding='utf-8'))
pending=[]
for scope in d.get('pendingScopes',[]):
 if scope['name']=='Positive packet versus numeric damage':
  scope['status']='REVIEWED / reference-VALIDATED';scope['reviewEvidence'].append(ev)
  d.setdefault('completedScopes',[]).append(scope)
 else:pending.append(scope)
d['pendingScopes']=pending
for b in d['bindings']:
 if str(b['sourceId']).endswith(('divine-judgment','wrathful-brand','balanced-scales')):
  rule='SUPERSESSION from healing conference: damage-event predicates require resolvedDamage>0 before tempHP, distinct from numeric actualDamageDealt=tempAbsorbed+actualHpDamage. Divine Judgment positive packet/numeric0 reflects minimum1 and consumes actual turn; fully prevented resolved0 does neither. See HEALING_DEATH_PLAYTEST.md; original costs/clocks/riders unchanged.'
  if rule not in b['operationalOverrides']:b['operationalOverrides'].append(rule)
  if ev not in b['reviewEvidence']:b['reviewEvidence'].append(ev)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'docs/mechanics/HEALING_DEATH_PLAYTEST.md';s=p.read_text(encoding='utf-8')
s=s.replace('# Healing, survival and resurrection — working candidate','# Healing, survival and resurrection — playtest interface')
s=s.replace('**IN REVIEW: exact implementation.** Three notebook conferences classify147 class sources and propose6 individual ordinary spell objects. Those spells remain inactive until individual review.','**REVIEWED / reference-VALIDATED — selected scope only.** The [final notebook review](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_FINAL_CLOSURE.md) closes147 classified class passages plus6 individually reviewed ordinary spell objects. Those6 spells are now operational playtest drafts; the catalog has78 operational and770 unfinished entries.')
s=s.replace('## Six ordinary spell candidates — inactive until exact review','## Six ordinary spells — reviewed operational playtest drafts')
s=s.replace('Current selected checks:164','Current selected checks:164')
p.write_text(s,encoding='utf-8')
p=ROOT/'docs/mechanics/CONTROL_STATES_PLAYTEST.md';s=p.read_text(encoding='utf-8')
s=s.replace('**Healing-conference clarification under exact review:**','**Reviewed healing-conference clarification:**')
p.write_text(s,encoding='utf-8')
p=ROOT/'docs/mechanics/DEVELOPMENT_ROADMAP.md';s=p.read_text(encoding='utf-8')
s=s.replace('Six spell designs individually reviewed and metadata validated; final bounded closure/promotion pending.','[GPT closed this bounded interface](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_FINAL_CLOSURE.md); six individually reviewed spells are promoted to the operational overlay.')
s=s.replace('[148 interface checks and9,393 Speed states]','[150 interface checks and9,393 Speed states]')
s=s.replace('First 72 individual drafts reviewed across all nine schools; full 848-ID source accounting, with 776 still unfinished.','78 individual drafts reviewed, including72 starters across nine schools and6 healing/death additions; full848-ID source accounting, with770 still unfinished.')
p.write_text(s,encoding='utf-8')
p=PROJECT/'START_HERE.md';s=p.read_text(encoding='utf-8')
s=s.replace('Supplied control scope reviewed and reference-validated (148 checks)','Supplied control scope reviewed and reference-validated (150 checks including the healing clarification)')
s=s.replace('Source conference and implementation review in progress; six new spells remain inactive.','153-source interface reviewed;164 selected checks. Six spells promoted into the operational overlay;131 further class passages under discussion.')
s=s.replace('72 operational','78 operational').replace('776 unfinished','770 unfinished')
p.write_text(s,encoding='utf-8')
p=HERE/'REVIEW_STATUS.md';s=p.read_text(encoding='utf-8')
s=s.replace('72 ordinary spell drafts reviewed, 776 still unfinished.','78 ordinary spell drafts reviewed,770 still unfinished.')
s=s.replace('including14 suppression/cure corrections under healing implementation review','including14 suppression/cure corrections closed in the healing review')
s=s.split('## Healing and death implementation review in progress')[0]+'''## Healing/death selected interface closed; remaining sources under conference

The [final GPT closure](GPT_HEALING_FINAL_CLOSURE.md) confirms the supplied153-source interface as REVIEWED / reference-VALIDATED. Its [guide](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_DEATH_PLAYTEST.md) has164 selected reference checks and120 unchanged Core damage parity states. Damage quantities, survival order, blocked natural20 recovery, conditional healing, finite reserves, excess conversions, healing causal chains, revival histories and lethal-track collapse now have one stated bounded procedure. Cure-presence and control damage clarifications are closed as part of this review; custom98/control150 checks pass.

All6 individually reviewed death/healing spells have been promoted into the operational playtest overlay. The ordinary catalog retains848 source IDs/936 placements and now has78 operational drafts/770 unfinished. Catalog validation passes42 checks and89,040 access boundaries; specific six-spell validation passes420 class/level boundaries with preserved source access/ranks/levels/RP. Original books, class objects and spell sources remain unchanged.

The [remaining131-source conference](CODEX_HEALING_REMAINING_CONFERENCE.md) has been submitted for individual classifications and concrete conflicts: Paladin recovery cadence, asynchronous Oracle zone upkeep, initial healing pulse costs, actual-gain cure/resource triggers, damage-based healing shares, maximum-HP changes and redirection order. Time Loop's participant field contract is tested, but world/equipment/topology/clocks remain a separate unfinished package. DD24 and the whole-game goal remain open.
'''
p.write_text(s,encoding='utf-8')
p=ROOT/'data/playtest/game_development_coverage.json';d=json.loads(p.read_text(encoding='utf-8'))
for row in d['aspects']:
 if row['number'] in (11,12,13,24):
  if ev not in row['reviewEvidence']:row['reviewEvidence'].append(ev)
  row['openIssues']=[x.replace('72 individual spell drafts reviewed; 776 unfinished.','78 individual spell drafts reviewed;770 unfinished.') for x in row['openIssues']]
 if row['number']==24:
  row['status']='selected-healing-interface-closed-remainder-under-conference'
  row['openIssues']=['Discuss all131 remaining class matches individually and resolve exact identified source conflicts.',
   'Audit healing content in other domains; complete broader body/soul/affliction procedures.',
   'Complete separate temporal topology/equipment/clock package; selected participant field checks are not complete Time Loop execution.']
  for field,path in [('reviewEvidence','docs/audit/2026-10-08/full-game/CODEX_HEALING_REMAINING_CONFERENCE.md'),
                     ('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_SPELL_CANDIDATE_VALIDATION.json')]:
   if path not in row[field]:row[field].append(path)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded153-source bounded closure and6 spell promotions; whole-game scope remains active/open.')
