from pathlib import Path
import json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
evidence='docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md'
reply=(HERE/'GPT_HEALING_DEATH_FIRST_REVIEW.md').read_text(encoding='utf-8')
table=reply.split('14. Classification of every supplied class source',1)[1].split('These classifications follow',1)[0]
roles={}
for line in table.splitlines():
 if '\t' not in line:continue
 ident,role=line.split('\t',1)
 if ident=='Source':continue
 if '.engine[' in ident:
  owner,index=re.fullmatch(r'(.+)\.engine\[(\d+)\]',ident).groups();key=f'class-engine:{owner}:{index}'
 else:key=f'class-card:{ident.split(".")[0]}:{ident}'
 roles[key]=role
assert len(roles)==79,len(roles)
p=ROOT/'data/playtest/healing_death_bindings.json';d=json.loads(p.read_text(encoding='utf-8'))
for b in d['bindings']:
 if b['bindingId'] in roles:
  b['classification']=roles[b['bindingId']]
  b['status']='DISCUSSED; operational implementation/review pending'
  if evidence not in b['reviewEvidence']:b['reviewEvidence'].append(evidence)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'data/playtest/custom_condition_bindings.json';d=json.loads(p.read_text(encoding='utf-8'))
rule={'id':'cure-presence-suppression','rule':'SUPERSESSION: Cure/removal tests existing unexpired presence, not current effect activity. Medicine selects one present eligible Bleed; positive-potential legal magical healing invokes each present eligible endpoint (Blood Curse retains CON save); Action/full immersion ends all present ordinary-extinguishable fires. Suppression/acquired condition immunity does not bar these cures or existing permitted ending saves. Damage arbitration and active-effect hooks still exclude suppressed/immune records. Initial immunity prevents new application; ended records cannot resume.',
      'reviewEvidence':[evidence]}
if not any(r['id']==rule['id'] for r in d['familyRules']):d['familyRules'].append(rule)
for row in d['definitions']:
 if not row.get('periodic'):continue
 cure=row.get('cure',{})
 cure['presenceRule']='Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required.'
 if 'magicalHealingScope' in cure:cure['magicalHealingScope']=cure['magicalHealingScope'].replace('active record','present record')
 if 'endingSave' in cure:cure['endingSave']['eligibility']='record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining'
 row['ending']=row['ending'].replace('one active eligible Bleed record','one present eligible Bleed record')
 if evidence not in row['reviewEvidence']:row['reviewEvidence'].append(evidence)
scope={'name':'Suppressed-record cure correction','status':'source-conferred; implementation exact review pending',
       'scope':'Present Bleed/fire records remain curable while suppressed; source-specific methods, immunity prevention and active hooks unchanged. 98 current custom-interface checks pass, including14 added cases.',
       'reviewEvidence':evidence}
if not any(s['name']==scope['name'] for s in d.setdefault('pendingScopes',[])):d['pendingScopes'].append(scope)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'data/playtest/game_development_coverage.json';d=json.loads(p.read_text(encoding='utf-8'))
for row in d['aspects']:
 if row['number']==24:
  for value in (evidence,'docs/audit/2026-10-08/full-game/CODEX_HEALING_SUPPLEMENT_CONFERENCE.md'):
   if value not in row['reviewEvidence']:row['reviewEvidence'].append(value)
  row['status']='healing-death-proposal-and-supplement-under-review'
  row['draftEvidence'].append('DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_DEATH_SOURCE_BINDINGS.md') if 'DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_DEATH_SOURCE_BINDINGS.md' not in row['draftEvidence'] else None
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded79 source classifications and supplied cure correction; healing scope remains open.')
