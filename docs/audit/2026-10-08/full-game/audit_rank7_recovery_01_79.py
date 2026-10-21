from pathlib import Path
from copy import deepcopy
from decimal import Decimal
from datetime import datetime, timezone
import json,hashlib

G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
R=A/'rank7-identity-casting5-part5-ready-deadline-recovery-01'
OLD=A/'rank7-identity-casting5-part5-correction-return-02'
OUT=A/'RANK7_READY_DEADLINE_RECOVERY_01_SEMANTIC_RECONCILIATION_79.json'
assert not OUT.exists(),'One-shot report already exists'
checks=[]
def ck(s,b):
 checks.append({'check':s,'passed':bool(b)})
 if not b:raise AssertionError(s)
def j(p):return json.loads(p.read_bytes())
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def ptr(v,p):
 for s in p.strip('/').split('/'):
  s=s.replace('~1','/').replace('~0','~');v=v[int(s)] if isinstance(v,list) else v[s]
 return v
def apply(v,ops,reverse=False):
 for i,o in enumerate(reversed(ops) if reverse else ops):
  p=o['pointer'];parent=ptr(v,p.rsplit('/',1)[0]) if p.count('/')>1 else v;k=p.rsplit('/',1)[1].replace('~1','/').replace('~0','~');k=int(k) if isinstance(parent,list) else k
  pre='after' if reverse else 'before';post='before' if reverse else 'after'
  exists=(0<=k<len(parent)) if isinstance(parent,list) else k in parent
  ck(('Reverse ' if reverse else 'Forward ')+p+' input '+str(i),exists==o.get(pre+'Exists',True) and (not exists or parent[k]==o[pre]))
  if o.get(post+'Exists',True):parent[k]=deepcopy(o[post])
  else:del parent[k]
 return v
model=j(R/'MODEL.json');old=j(OLD/'MODEL.json');raw=(R/'MODEL.json').read_bytes()
prior=A/'RANK7_IDENTITY_CASTING5_PART5_CORRECTION_RETURN_02_SEMANTIC_RECONCILIATION_74.json';pr=j(prior)
ck('Prior semantic report has exactly one remaining deadline finding',pr['diagnosticCheckCount']==554 and pr['diagnosticFailures']==1 and pr['findingsCount']==1)
allops={}
for label,baseline,n in [('Return02','RETURN02_MODEL.json',6),('Return01','RETURN01_MODEL.json',17),('Source','CANDIDATE.json',44)]:
 op=j(R/('EXACT_OPERATIONS_FROM_'+label.upper()+'.json'));ops=op['operations'];allops[label]=ops;b=(R/'baseline'/baseline).read_bytes();ck(label+' exact operation count',len(ops)==n)
 ck(label+' forward reproduces every target byte',enc(apply(json.loads(b),ops))==raw)
 ck(label+' reverse restores every baseline byte',enc(apply(deepcopy(model),ops,True))==b)
 if label!='Return02':ck(label+' alternative paths explicitly documented',op['alternativeOnly']=='Choose this complete path OR the incremental Return02 path OR the other complete path. Never apply complete paths cumulatively.')
ck('Return02 baseline equals original local full MODEL',(R/'baseline/RETURN02_MODEL.json').read_bytes()==(OLD/'MODEL.json').read_bytes())
ck('Exactly six 62-to-61 MODEL changes',all(o['before']==62 and o['after']==61 and o['pointer'].startswith('/currentVectors/2/independentBranches/0/') and o['pointer'].endswith('/sourceLedger/hold/deadline') for o in allops['Return02']))
for label in ['Return01','Source']:
 earlier=j(OLD/('EXACT_OPERATIONS_FROM_'+label.upper()+'.json'))['operations'];ck(label+' original complete operation values preserved',allops[label][:-6]==earlier)
for k in model:
 if k!='currentVectors':ck('All unchanged MODEL authorship '+k,model[k]==old[k])
for i,(c,c0) in enumerate(zip(model['currentVectors'],old['currentVectors'])):
 if i!=2:ck('Unchanged entire main case '+c['id'],c==c0)
ck('Ten main cases and39branches',len(model['currentVectors'])==10 and sum(len(c['independentBranches']) for c in model['currentVectors'])==39)
ck('Complete main case mirror',j(R/'CASE_DISPOSITIONS.json')['cases']==model['currentVectors'])
ck('Complete worked case mirror',j(R/'evidence/worked_cases.json')==model['currentVectors'])
ck('Five unchanged shared clauses',len(model['selectedSharedRules'])==5 and j(R/'evidence/shared_rules.json')==model['selectedSharedRules'])
ck('24complete question dispositions',len(model['selectedQuestionDispositions'])==24 and j(R/'QUESTION_DISPOSITIONS.json')['dispositions']==model['selectedQuestionDispositions'])
spells=j(R/'SPELL_DISPOSITIONS.json')['dispositions'];procs=j(R/'evidence/procedures.json');qs=j(R/'evidence/decision_selections.json')
for rec in model['records']:
 sid=rec['spellId'];s=next(s for s in spells if s['spellId']==sid)
 ck('Full procedure mirror '+sid,procs[sid]==rec['proposedProcedure']==s['fullSelectedProcedure'])
 ck('Standalone full procedure '+sid,(R/('evidence/procedure_'+sid+'.md')).read_text(encoding='utf-8').strip()==rec['proposedProcedure'].strip())
for q in model['selectedQuestionDispositions']:ck('Full question evidence '+q['id'],qs[q['id']]==[q['disposition'],q['selectedAnswer']])
holds=j(R/'HOLD_REGISTER.json');ck('All explicit holds preserved',holds['holds']==model['explicitHolds']==old['explicitHolds']);ck('All11conditional qualifications preserved',holds['conditionalBranches']==model['conditionalBranchRegister']==old['conditionalBranchRegister'] and len(model['conditionalBranchRegister'])==11)
mirror=j(R/'MIRROR_OPERATIONS_FROM_RETURN02.json');ck('Five files25mirror operations',len(mirror['files'])==5 and sum(len(x['operations']) for x in mirror['files'])==25)
for f in mirror['files']:
 before=(OLD/f['file']).read_bytes();after=(R/f['file']).read_bytes()
 ck('Complete mirror forward '+f['file'],enc(apply(json.loads(before),f['operations']))==after)
 ck('Complete mirror reverse '+f['file'],enc(apply(json.loads(after),f['operations'],True))==before)
inherited=j(R/'INHERITED_MIRROR_RECONCILIATION.json');ck('Exactly two identified inherited omissions',{f['id'] for f in inherited['findings']}=={'RIC5-SI03','RIC5-SI05'} and not inherited['modelChanged'] and not inherited['authorshipReopened'])
for f in inherited['findings']:
 q=ptr(model,f['authority']['pointer']);ck('Corrected evidence already exists in oldMODEL '+f['id'],q==ptr(old,f['authority']['pointer']) and f['after']==[q['disposition'],q['selectedAnswer']]);ck('Complete prior evidence retained '+f['id'],f['before']==j(OLD/f['file'])[f['id']])
oldline='Current complete examples and full states are in CASE_DISPOSITIONS.json and evidence/worked_cases.json. See FINDING_DISPOSITIONS.json and ACTION_AUDIT.json for all corrected ledgers and three related cadence clarifications. Original procedures, examples and reports remain in the preserved incoming/Return01 archives. No gameplay engine or source acquisition is implemented by these examples.'
newline='Current complete examples and full states are in CASE_DISPOSITIONS.json and evidence/worked_cases.json. See history/return02/FINDING_DISPOSITIONS.json and ACTION_AUDIT.json for the prior corrected ledgers and three related cadence clarifications; FINDING_DISPOSITIONS.json records the recovery-only deadline disposition. Original procedures, examples and reports remain in the preserved incoming/Return01 archives. No gameplay engine or source acquisition is implemented by these examples.'
for n in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:
 text=(R/n).read_text(encoding='utf-8');prior_text=(OLD/n).read_text(encoding='utf-8');prefix=prior_text.replace(oldline,newline,1)
 ck('Complete earlier chapter retained with corrected history link '+n,oldline in prior_text and text.startswith(prefix) and text[len(prefix):].lstrip().startswith('# Recovery01'))
source=(R/'sources/DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md').read_bytes();ck('Exact current Ready source',source==(G/'DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md').read_bytes());ck('Ready source next ownSTART expiry',b'It expires next regular own-turn start.' in source)
branch=model['currentVectors'][2]['independentBranches'][0];events=branch['timeline'];ck('Original56.1/60.5/60.9 event times',[e['timeSeconds'] for e in events]==[56.1,60.5,60.9]);before=events[-1]['before'];after=events[-1]['after']
ck('Actual55/61cadence and paid snapshot',before['actors']['mage']['regularStart']==55 and before['actors']['mage']['nextRegularStart']==61 and before['sourceLedger']['hold']['deadline']==61 and before['sourceLedger']['hold']['preparation']==56.1)
ck('No regularSTART added at release',events[-1]['regularStartsBeforeEvent']==[])
expected=deepcopy(before);expected['actors']['mage']['reaction']=False;expected['actors']['mage']['concentration']=None;expected['actors']['target']['hp']-=6;expected['sourceLedger']['hold']['state']='consumed';expected['sourceLedger']['hold']['paidMetamagicCharge']=0
ck('Entire positive state has only authorized release transitions',expected==after==branch['expectedFinalState'])
ck('Supplied attack arithmetic and hit',events[-1]['rng']['attack']==[7,9,16] and 7+9==16 and 16>=branch['actorDefinitions']['target']['AC'] and events[-1]['rng']['1d8']==[6])
diag=j(R/'READY_DEADLINE_DIAGNOSTIC.json');ck('Boundary diagnostics are isolated',not diag['schedulerScope']['regularStartDispatched'] and not diag['schedulerScope']['actionOrReactionRefreshGranted'] and not diag['schedulerScope']['actualFullStateAt61Or61_1Asserted'])
ck('Exactly three boundary inputs',[c['triggerTime'] for c in diag['independentBoundaryCases']]==['60.9','61','61.1'])
for c in diag['independentBoundaryCases']:
 t=Decimal(c['triggerTime']);ck('Complete independent paid reset '+str(t),c['completeBefore']==before);exp=deepcopy(before);live=t<Decimal(61)
 ck('Strict deadline predicate '+str(t),c['correctedTimeLessThan61']==live and c['obsoleteTimeLessThan62']==(t<Decimal(62)))
 if live:exp=deepcopy(expected)
 else:exp['sourceLedger']['hold']['state']='expired';exp['actors']['mage']['concentration']=None
 ck('Full isolated expected state '+str(t),c['completeAfter']==exp)
 receipt={'payloadApplications':int(live),'reactionDebits':int(live),'holdEnds':1,'concentrationEnds':1}
 ck('Single-use full receipt '+str(t),c['receiptAfter']==receipt)
 mage=exp['actors']['mage'];ck('No recast or extra budgets '+str(t),mage['rp']==38 and mage['dissonance']==0 and mage['refrain']==0 and mage['metaspellUses']==0 and mage['action'] is False and mage['lastSpell']=='ray-of-frost')
 for i,repeat in enumerate(c['repeatCallbacks']):ck('Idempotent callback '+str(t)+'/'+str(i),repeat['completeAfter']==exp and repeat['receiptAfter']==receipt)
ck('Three independently scoped release-gate negatives',len(diag['preExpiryGateDiagnostics'])==3)
for c in diag['preExpiryGateDiagnostics']:
 ck('Rejected release unchanged '+c['gate'],c['completeAfter']==c['completeBefore'] and all(x==0 for x in c['receiptAfter'].values()))
 if c['gate']=='no-reaction':ck('No-reaction actual input',c['completeBefore']['actors']['mage']['reaction'] is False)
cp=j(A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_MASS_UNDEATH_78.json');protected=[cp['currentAuthoredIndex'],cp['currentAcceptedInterfaceRegistry'],*cp['canonicalHelperBaselinesUnchanged']]
for x in protected:ck('Canonical unchanged '+x['path'],info(G/x['path'])==x)
ck('Catalog unchanged',info(G/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json')['sha256']=='f52cf6a4a4673897615a74c7c67dcba798c431362d4357e71ee552cc7c5d31f8')
(A/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
OUT.write_bytes(enc({'id':'RANK7-READY-DEADLINE-RECOVERY01-SEMANTIC-RECONCILIATION-79','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'verdict':'REMAINING_READY_DEADLINE_FINDING_RECONCILED_COMPLETE_MIRRORS_VERIFIED','model':info(R/'MODEL.json'),'priorIndependentSemanticReview':info(prior),'preservationReceipt':info(A/'RANK7_READY_DEADLINE_RECOVERY_01_PRESERVATION_79.json'),'script':info(A/Path(__file__).name),'checkCount':len(checks),'failures':0,'checks':checks,'resolvedFinding':'Six62-to-61stored Ready deadlines now match actual nextSTART61. Complete positive60.9state and isolated equality/late expiry branches verified.','documentaryCorrections':['SI03projectile resolution/durable lineage restored from existing selected answer','SI05living-zero snapshot/recovery qualifications restored from existing selected answer'],'inheritedReviewScope':'The prior553passing semantic checks are inherited by exact completeMODEL preservation except the six identified corrected fields; they are not reported as fresh reruns. Nine withdrawn overly strict START diagnostics remain withdrawn.','qualifications':'All18explicit holds and11conditional branch prerequisites preserved, including five independent whole positive-case holds. Boundary diagnostics freeze scheduler inputs and do not demonstrate full runtime START behavior.','downloadedCodeExecuted':False,'runtimeTestsExecuted':0,'humanPlaytests':0,'balanceApproval':False,'cosmologyChanges':0,'sourceInformationDeleted':0,'canonicalChanges':0,'wholeGameComplete':False,'releaseApproval':False,'acceptedCountChangeRecordedSeparately':True}))
print(json.dumps({'report':str(OUT),'checkCount':len(checks),'failures':0}))
