from pathlib import Path
import json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
reply=(HERE/'GPT_CREATURE_LIFECYCLE_FIRST_REVIEW_PARTIAL.md').read_text(encoding='utf-8')
roles={}
pattern=re.compile(r'(?:druid|mage|mirrorsage|ranger|wizard)\.(?:engine\[\d+\]|[a-z0-9][a-z0-9.-]*)')
for line in reply.splitlines():
    if not line.startswith('|'):continue
    cells=[c.strip() for c in line.strip('|').split('|')]
    if len(cells)!=3:continue
    for ident in pattern.findall(cells[1]):roles[ident]=cells[2].strip()
path=ROOT/'data/playtest/creature_lifecycle_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
assert set(roles)=={r['bindingId'] for r in data['bindings']},{
    'missing':sorted({r['bindingId'] for r in data['bindings']}-set(roles)),
    'extra':sorted(set(roles)-{r['bindingId'] for r in data['bindings']})}
data['status']='SOURCE-AUDITED / DRAFTABLE; unresolved boundaries and exact implementation pending'
for row in data['bindings']:
    row['classification']=roles[row['bindingId']]
    row['status']='DISCUSSED; supplied role only, not implemented closure'
    row['reviewEvidence']=['GPT_CREATURE_LIFECYCLE_FIRST_REVIEW.md']
    row['operationalOverrides']=['See full first conference for source-specific proposed lifecycle decisions; further boundary review controls before implementation.']
    row['openIssues']=['Resolve timing, control, corpse, persistent-state and acquisition evidence boundaries; form/tempHP classifications remain deferred as indicated.']
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded all100 exact source classifications; no rule closure.')
