from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
reply=(HERE/'GPT_DEVICE_LIFECYCLE_FIRST_REVIEW_PARTIAL.md').read_text(encoding='utf-8')
roles={}
for line in reply.splitlines():
    cells=[v.strip().strip(chr(96)) for v in line.strip('|').split('|')]
    if len(cells)==3 and cells[0].startswith(('tinker.','shaman.')):roles[cells[0]]=(cells[1],cells[2])
path=ROOT/'data/playtest/device_lifecycle_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
assert len(roles)==74 and set(roles)=={r['bindingId'] for r in data['bindings']}
for row in data['bindings']:
    role,proposal=roles[row['bindingId']]
    row['classification']=role
    row['status']='DISCUSSED; exact boundary and implementation review pending'
    row['operationalOverrides']=['First discussion proposal: '+proposal]
    row['reviewEvidence']=['GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md']
    row['openIssues']=['Resolve remaining state/identity/debris/command boundaries before exact implementation. Discussion is not full-card closure.']
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded all74 individual lifecycle discussion roles.')
