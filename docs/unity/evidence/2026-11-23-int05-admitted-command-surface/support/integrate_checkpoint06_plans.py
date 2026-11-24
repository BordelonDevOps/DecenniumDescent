import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
PACKET=ROOT/'docs/unity/evidence/2026-11-23-int05-admitted-command-surface'
ART=Path(__file__).resolve().parent
for original,retained,sha in [
    ('MANAGEMENT_BRANCH_QUALIFICATION_PLAN.json','MANAGEMENT_BRANCH_QUALIFICATION_PLAN.json','2504176c2ecd3eb745775a8e72bc7a1667df00b37ebba1457934373126c4dcac'),
    ('MAGIC_AND_CARE_BRANCH_QUALIFICATION_PLAN.json','MAGIC_AND_CARE_BRANCH_QUALIFICATION_PLAN.json','e2d4d521f92fc5bb8ae02a13e4c2d1405e7d3a41c5af5454b7bf4b45f03d6e82'),
    ('public-denial-vocabulary-proposal.json','PUBLIC_DENIAL_VOCABULARY_PROPOSAL.json','c2a05bd07e9b89f136c85916f669e8415ebda30248ca8bbe05d8f1d4d6601e5d'),
    ('checkpoint06-parent-plan-cross-review.json','CHECKPOINT_06_PARENT_PLAN_REVIEW.json','a42bbd4e61f0c961f6ae0d47eb93de9b1dfc8e6298e725d203da8ff2be96976e'),
]:
    data=(ART/original).read_bytes();assert hashlib.sha256(data).hexdigest()==sha
    (PACKET/retained).write_bytes(data);print(retained,sha)
before=PACKET/'support/review-inputs'
before.mkdir(parents=True,exist_ok=True)
aliases=[]
for name in ['PROFILE_AND_CHECKPOINT_QUALIFICATION_PLAN.json','SPATIAL_SPEED_PRESSURE_READ_PLAN.json']:
    source=PACKET/name;target=before/('CHECKPOINT06_BEFORE_'+name)
    if not target.exists(): target.write_bytes(source.read_bytes())
    aliases.append({'originalPath':source.relative_to(ROOT).as_posix(),'retainedPath':target.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
(PACKET/'INPUT_VERSION_RECONCILIATION_06.json').write_text(json.dumps({'historicalInputs':aliases,'meaning':'Exact frozen parent inputs independently reviewed before two source corrections; not earlier runtime.'},indent=2)+'\n',encoding='utf-8')
p=PACKET/'SPATIAL_SPEED_PRESSURE_READ_PLAN.json';d=json.loads(p.read_text(encoding='utf-8'))
row=next(x for x in d['entries'] if x['id']=='S08')
row['privacy']='Do not conflate initial eligibility with a predicted contact/clock result. Actual BeginWorldStep may directly enter the first tactical encounter when StartsEncounter is true (SharedWorldCommandQueries98-132; ResolveCore1071-1076); no traversal edge or clock advancement is required for that branch. Later Ferry/Recovery/Later traversal contacts occur during their actual advancement paths. Pure reads perform neither transition.'
d['independentCorrection']='CHECKPOINT_06_PARENT_PLAN_REVIEW: S08 direct first-contact transition corrected; original reviewed input retained in INPUT_VERSION_RECONCILIATION_06.json.'
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

order_path=PACKET/'CONTRACT_DECISION_ORDER.json';order=json.loads(order_path.read_text(encoding='utf-8'))
if not any(x['order']==9 for x in order['effectiveDocuments']):
    order['effectiveDocuments'].append({'order':9,'path':'ADMISSION_DECISIONS_08.md','scope':'Actual GPT08 exact unit table, effective grant/freshness/native revision order, finite mining candidate sampling, distinct IDs and condition materialization precision.'})
order['latestActualReview']={'requestId':'bfbf095e-fab4-4c53-b648-3f19a0167ea9','responseId':'1c4cf155-c167-5d01-a9d3-c2d143ecd8f0'}
order_path.write_text(json.dumps(order,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
