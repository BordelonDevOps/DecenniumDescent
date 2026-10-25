"""Fresh local read-only source/preservation/phase/fork checks for Return03."""
from pathlib import Path
import json,hashlib,sys
D=Path(__file__).parent;E=D/'magic7_return03_received';P=D/'magic7_return02_received'
r=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
checks=[];errors=[];errata=[]
def check(n,v):
 checks.append(n)
 if not v:errors.append(n)
pres=r(E/'RETURN02_ALL_MEMBER_PRESERVATION.json')['members']
correct=[]
for b in pres:
 old=P/b['originalPath'];prior=old.read_bytes()
 check('prior-binding:'+b['originalPath'],len(prior)==b['originalBytes'] and sha(prior)==b['originalSha256'])
 claimed=E/b['preservedAt'];found=next((p for p in [claimed,E/'history/return02'/b['originalPath']] if p.is_file() and p.read_bytes()==prior),None)
 check('preserved-bytes:'+b['originalPath'],found is not None)
 if found:
  actual=found.relative_to(E).as_posix();correct.append({**b,'preservedAt':actual})
  if actual!=b['preservedAt']:errata.append({'kind':'preservation-locator-only','originalPath':b['originalPath'],'reportedLocation':b['preservedAt'],'verifiedExactLocation':actual,'bytes':len(prior),'sha256':sha(prior)})
check('all-prior-members',len(pres)==79 and {b['originalPath'] for b in pres}=={p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file()})
for n in r(E/'RETURN03_PRESERVATION_CHECKS.json')['verbatimOperativeAndSourceFiles']:check('verbatim:'+n,(E/n).read_bytes()==(P/n).read_bytes())
cases={}
def visit(c):
 cases[c['id']]=c
 for b in c['branches']:visit(b)
for c in r(E/'CASEBOOK.json')['completeCases']:visit(c)
timing=[];spends=0;forks=0
for c in cases.values():
 if 'forkBinding' in c:
  f=c['forkBinding'];p=cases[f['parentCase']];e=next(e for e in p['timeline'] if e['id']==f['parentEvent'])
  check('exact-fork:'+c['id'],c['initialState']==e[f['side']]);forks+=1
 for e in c['timeline']:
  for aid,a in e['before']['actors'].items():
   b=e['after']['actors'][aid];p=a['phase'];s=p['lastStart'];end=p['lastEnd'];active=s is not None and (end is None or s>end) and s<=e['time']<=s+p['turnSeconds']
   spent=[k for k in ['action','bonusAction'] if a['wallet'][k] and not b['wallet'][k]]
   moved=a['body']!=b['body'];spends+=bool(spent)
   if (spent or moved) and not active and 'outside' not in (e['event']+json.dumps(e['inputs'])+json.dumps(e['observations'])).lower():timing.append({'event':e['id'],'name':e['event'],'actor':aid,'time':e['time'],'spent':spent,'moved':moved,'phase':p})
check('no-unexplained-offturn-action-or-movement',not timing)
c=cases['TU4-09-B']
for t,prior,after in [(12,2,1),(18,1,0)]:
 e=next(e for e in c['timeline'] if e['time']==t)
 check('dispel-recharge:'+str(t),e['before']['actors']['O']['recharge']['wizard.arch.dispel-magic']==prior and e['after']['actors']['O']['recharge']['wizard.arch.dispel-magic']==after)
src=r(E/'RETURN03_CLASS_CASE_SOURCES.json');wiz=r(E/'evidence/WIZARD_CLASS_FULL.json');act=r(E/'ACTOR_TEMPLATES.json')
check('native-bolt-card',src['completeNativeWizardArcaneBolt']==wiz['cards'][5])
for aid,v in src['actualExistingAcquisitions'].items():
 check('bolt-template-card:'+aid,v['entry']['completeCard']==src['completeNativeWizardArcaneBolt'])
 check('bolt-template-acquisition:'+aid,v['entry'] in act[v['existingTemplate']]['selectedAcquisition'])
rounds=[]
for cid in ['TU6-01-A','TU6-01-A/later-same-round']:
 for e in cases[cid]['timeline']:
  g=e['after']['actors']['G']
  check('no-owner-wide-consumption:'+e['id'],not g.get('damageAllowanceUsedRounds'))
  if g.get('protectiveMutationsRecipientRoundUses'):rounds.append({'case':cid,'event':e['id'],'uses':g['protectiveMutationsRecipientRoundUses']})
report={'id':'MAGIC7-RETURN03-FINAL-INDEPENDENT-CHECKS-129','checks':len(checks),'errors':errors,'exactBranchForks':forks,'actionSpendTransitionsInspected':spends,'unexplainedTimingFindings':timing,'priorMembersPreserved':len(correct),'nonOperativePreservationLocatorErrata':errata,'verifiedPriorPreservationMap':correct,'recipientRoundHistories':rounds,'suppliedCodeExecuted':False,'canonicalChanges':False}
(D/'MAGIC7_RETURN03_FINAL_INDEPENDENT_CHECKS_129.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['verifiedPriorPreservationMap','recipientRoundHistories']},indent=2))
if errors:sys.exit(1)
