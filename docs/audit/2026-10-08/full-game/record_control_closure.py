"""Record the actual bounded notebook disposition without closing broad domains."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
GAME=HERE.parents[3]
ROOT=GAME/'DescentReviewChanges/ReviewBible'
evidence='docs/audit/2026-10-08/full-game/GPT_CONTROL_FINAL_REVIEW.md'
assert 'REVIEWED / reference-VALIDATED' in (GAME/evidence).read_text(encoding='utf-8')
def read(rel):return json.loads((ROOT/rel).read_text(encoding='utf-8'))
def save(rel,data):(ROOT/rel).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
data=read('data/playtest/control_state_bindings.json')
data['status']='REVIEWED / reference-VALIDATED — supplied control scope only'
data['reviewEvidence']=[evidence]
for b in data['bindings']:
 b['status']='REVIEWED control-scope disposition; not complete-card execution'
 if evidence not in b['reviewEvidence']:b['reviewEvidence'].append(evidence)
save('data/playtest/control_state_bindings.json',data)
bindings={b['bindingId']:b for b in data['bindings']}
coverage=read('data/playtest/control_state_coverage.json')
for r in coverage['candidates']:
 r['status']='REVIEWED control-scope disposition'
 r['bindingIds']=[r['candidateId']]
 if evidence not in r['reviewEvidence']:r['reviewEvidence'].append(evidence)
 r['openIssues']=[x for x in r['openIssues'] if 'Exact candidate implementation review is pending' not in x]
 if bindings[r['candidateId']]['classification']=='DEFER':
  note='Deferral/classification reviewed only; substantive non-control mechanics remain in their own development scope.'
  if note not in r['openIssues']:r['openIssues'].append(note)
save('data/playtest/control_state_coverage.json',coverage)
game=read('data/playtest/game_development_coverage.json')
scope='Supplied219-source control interface jointly reviewed and reference-validated:148 checks,9393 Speed states,219 bindings/180 component identities. Source-qualified clocks, riders, control and named metadata only; not full card execution.'
for r in game['aspects']:
 if r['number'] in (16,18):
  r['status']='reviewed-in-bounded-control-scope; broader-domain-open'
  if evidence not in r['reviewEvidence']:r['reviewEvidence'].append(evidence)
  if scope not in r.setdefault('completedScopes',[]):r['completedScopes'].append(scope)
  r['openIssues']=[x.replace('Complete root/slow/mark and curse/disease metadata and exhaustive semantic coverage across active class/spell effects. Bounded generic conditions, periodic families and Strain namespacing are reviewed; DD16 remains open.','Complete remaining all-source condition semantics and actual disease/curse catalogs; supplied219 control interfaces are reviewed. DD16 remains open.') for x in r['openIssues']]
 if r['number']==24:
  r['status']='healing-death-source-conference-in-progress'
  conference='docs/audit/2026-10-08/full-game/CODEX_HEALING_DEATH_CONFERENCE.md'
  if conference not in r['reviewEvidence']:r['reviewEvidence'].append(conference)
save('data/playtest/game_development_coverage.json',game)
p=ROOT/'docs/mechanics/CONTROL_STATES_PLAYTEST.md'
s=p.read_text(encoding='utf-8').replace('**IN REVIEW — authored candidate.**','**REVIEWED / reference-VALIDATED — supplied scope only.**')
s=s.replace('##', '##',1)
s+='\n[Final notebook disposition](../../../../docs/audit/2026-10-08/full-game/GPT_CONTROL_FINAL_REVIEW.md) approves this supplied interface after correcting pre-roll mark bonuses, binding roles, fallback tags and all turn-end clock phases.\n'
p.write_text(s,encoding='utf-8')
p=ROOT/'tools/validate_control_playtests.py'
s=p.read_text(encoding='utf-8').replace("'IN_REVIEW; selected helpers only'","'REVIEWED / reference-VALIDATED; selected helpers only'").replace('states. Review pending.','states. Bounded review recorded.')
p.write_text(s,encoding='utf-8')
p=ROOT/'docs/mechanics/DEVELOPMENT_ROADMAP.md'
s=p.read_text(encoding='utf-8').replace('[107 interface checks and9,393 Speed states]','[148 interface checks and9,393 Speed states]').replace('pass; exact GPT implementation review is pending. Whole-source semantic coverage remains open.','pass; [GPT closed this bounded scope](../../../../docs/audit/2026-10-08/full-game/GPT_CONTROL_FINAL_REVIEW.md). Whole-source semantic coverage remains open.')
p.write_text(s,encoding='utf-8')
p=GAME/'START_HERE.md'
s=p.read_text(encoding='utf-8').replace('Exact implementation review is in progress; wider condition and class semantics remain open.','Supplied control scope reviewed and reference-validated (148 checks); wider condition and class semantics remain open.')
p.write_text(s,encoding='utf-8')
p=HERE/'REVIEW_STATUS.md'
s=p.read_text(encoding='utf-8').replace('## Control-state candidate in exact review','## Control-state bounded closure')
start=s.index('The candidate passes107 targeted helper checks')
end=s.index('\n\nThe next healing/death inventory',start)
s=s[:start]+'''The candidate passes148 targeted helper checks and9,393 Speed states. Integrity checks cover219 exact procedures and180 component identities; these include alternative modes and do not prove all-card implementation. The [final GPT review](GPT_CONTROL_FINAL_REVIEW.md) closes the supplied interface after corrected pre-roll bonuses, modifier/reference roles, conditional slowed tags and phase-aware turn-end deadlines. DD16/DD18 remain open. Historical discussion excerpts are non-authoritative where corrected by the operational guide. Original source objects remain unchanged.'''+s[end:]
s=s.replace('will be conferred next','are now under notebook conference')
p.write_text(s,encoding='utf-8')
print('Recorded bounded control closure; all broader gates preserved.')
