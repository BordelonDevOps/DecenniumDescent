from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
p=ROOT/'data/playtest/form_temphp_bindings.json';data=json.loads(p.read_text(encoding='utf-8'))
ids={r['bindingId'] for r in data['bindings']};roles={}
reply=(HERE/'GPT_FORM_TEMP_HP_FIRST_REVIEW.md').read_text(encoding='utf-8')
table=reply.split('Exact classification ledger',1)[1].split('The five supports',1)[0]
for line in table.splitlines():
 cells=line.split('\t')
 if len(cells)!=2 or cells[0]=='Role':continue
 role,listed=cells
 for ident in (v.strip() for v in listed.split(';')):
  assert ident in ids and ident not in roles,ident
  roles[ident]=role
assert set(roles)==ids and len(roles)==175
data['status']='SOURCE-AUDITED / DRAFTABLE:175+5 individually discussed; boundary reconciliation and implementation pending'
for r in data['bindings']:
 r['classification']=roles[r['bindingId']]
 r['status']='DISCUSSED; supplied source role only, implementation pending'
 r['reviewEvidence']=['GPT_FORM_TEMP_HP_FIRST_REVIEW.md']
 r['operationalOverrides']=['First conference assigns this exact role. Buffer/form decisions require boundary reconciliation and tested implementation; no whole-card or catalog closure.']
 r['openIssues']=['Resolve grant identity/expiry/payment and exact source/form boundary questions. Incomplete feat/spell/Time Loop and equipment/natural-attack dependencies remain separately visible.']
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded175 unique exact roles once; no implementation closure.')
