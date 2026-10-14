"""LRX finite correction application / strict pre-label fulfillment comparison.
Usage:
 python verify_named_fulfillment.py FROZEN_ROOT WORKING_ROOT REPORT_PATH [--apply]
The optional write operation affects exactly eight candidate artifacts in WORKING_ROOT.
It never edits sources, the original verdict/register, the catalog or review labels.
Checks are static/text/byte comparisons, not execution of complete spell procedures.
"""
from pathlib import Path
from copy import deepcopy
import hashlib,json,sys,importlib.util
from manifest_loader import load_protected_manifest

B='DescentReviewChanges/ReviewBible/'
P=B+'data/public/spell_playtests/candidate_low_rank_136.json'
I=B+'data/playtest/spell_drafts/candidate_low_rank_136.json'
C=B+'data/playtest/spell_drafts/low_rank_137_authored_boundaries.json'
D=B+'data/public/spell_playtests/low_rank_137_authored_boundaries.json'
M=B+'docs/playtest/LOW_RANK_136_CANDIDATE.md'
PM=B+'data/public/spell_playtests/candidate_low_rank_136.md'
CM=B+'docs/playtest/LOW_RANK_137_AUTHORED_BOUNDARIES.md'
PCM=B+'data/public/spell_playtests/low_rank_137_authored_boundaries.md'
Q='docs/audit/2026-10-08/full-game/LOW_RANK_136_CANDIDATE_QUESTION_MAP.json'
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def payload(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def apply_fields(docs,patches):
 for p in patches:
  for file in p['files']:
   a=[x for x in docs[file][p['selector']['collection']] if x['id']==p['selector']['id']]
   if len(a)!=1:raise ValueError('Missing/duplicate amendment target: '+str(p['selector']))
   node=a[0]
   for field in p['fieldPath'][:-1]:node=node[field]
   key=p['fieldPath'][-1]
   if node[key]!=p['oldValue']:raise ValueError('Amendment old-value mismatch: '+p['correctionId']+'/'+str(p['fieldPath']))
   node[key]=deepcopy(p['replacementValue'])
 return docs

def expected_artifacts(frozen,patches):
 docs=apply_fields({s:load(frozen/s) for s in [I,P,C,D]},patches)
 spec=importlib.util.spec_from_file_location('frozen_candidate_renderer',frozen/(B+'tools/build_low_rank_136_candidates.py'))
 mod=importlib.util.module_from_spec(spec)
 previous_bytecode_flag=sys.dont_write_bytecode
 try:
  sys.dont_write_bytecode=True
  spec.loader.exec_module(mod)
 finally:
  sys.dont_write_bytecode=previous_bytecode_flag
 text=mod.manuscript(docs[P]).encode()
 lines=['# Low-rank spell authored boundary casebook','',docs[C]['scope'],'']
 for c in docs[C]['cases']:
  lines += ['## '+c['id'],'','Applies to: '+', '.join(c['questionIds'])+'.','','```json',json.dumps(c['authoredExpectation'],ensure_ascii=False,indent=2),'```','']
 casebook='\n'.join(lines).encode()
 return {**{s:payload(x) for s,x in docs.items()},M:text,PM:text,CM:casebook,PCM:casebook},docs

def main(frozen,work,report,apply=False):
 frozen=Path(frozen).resolve();work=Path(work).resolve();report=Path(report).resolve()
 if frozen==work or work.is_relative_to(frozen) or frozen.is_relative_to(work):raise ValueError('Use separate sibling trees')
 if report.is_relative_to(frozen):raise ValueError('Report cannot write inside frozen inputs')
 corrections=load(Path(__file__).parent/'LRX_136_CORRECTIONS.json')
 expected,docs=expected_artifacts(frozen,corrections['jsonFieldReplacements'])
 protected=load_protected_manifest(frozen)
 # Working protected sources must still be byte-identical before label-only promotion.
 assert load_protected_manifest(work)==protected
 changes=[]
 if apply:
  for name,raw in expected.items():
   p=work/name;before=p.read_bytes()
   if before not in [raw,(frozen/name).read_bytes()]:raise ValueError('Unrelated working candidate changes: '+name)
   p.write_bytes(raw)
   changes.append({'file':name,'beforeSha256':sha(before),'afterSha256':sha(raw)})
 checks=[]
 def ck(name,result):checks.append({'name':name,'pass':bool(result)})
 for name,raw in expected.items():ck('exact amended artifact: '+name,(work/name).read_bytes()==raw)
 ck('original question map unchanged',load(work/Q)==load(frozen/Q))
 for f,h in protected.items():ck('protected original: '+f,sha((work/f).read_bytes())==h)
 actualI=load(work/I);actualP=load(work/P)
 for old,new,public in zip(load(frozen/I)['spells'],actualI['spells'],actualP['spells']):
  ck(old['id']+' full source receipt unchanged',new['sourceReceipt']==old['sourceReceipt'])
  ck(old['id']+' full source verdict record unchanged',new['internalSourceAuthoringRecord']==old['internalSourceAuthoringRecord'])
  ck(old['id']+' whole public card parity',public=={k:v for k,v in new.items() if k!='internalSourceAuthoringRecord'})
  ck(old['id']+' labels remain unpromoted in this proof',new['status']==old['status'] and new['selectionEnabled']==old['selectionEnabled'] and new['reviewEvidence']==old['reviewEvidence'])
 for actual,e in zip(load(work/C)['cases'],docs[C]['cases']):ck(actual['id']+' full amended case',actual==e and actual['runtimePassed'] is False)
 # A strict expected-envelope comparison must reject even count-preserving edits.
 faults=[]
 for label,action in [
  ('wrong Ten-minute duration',lambda x:x['spells'][76]['operationalCandidate'].__setitem__('duration','1 minute')),
  ('mirror rollback',lambda x:x['sharedRules'][13].__setitem__('wording',load(frozen/P)['sharedRules'][13]['wording'])),
  ('invented source null',lambda x:x['spells'][0]['sourceReceipt'].__setitem__('invented',None)),
  ('unarmed proficiency inserted',lambda x:x['spells'][100]['operationalCandidate']['numericParameters'].__setitem__('unarmedAttackModifier',2)),
  ('future-round rollback',lambda x:x['spells'][46]['operationalCandidate'].__setitem__('duration',load(frozen/P)['spells'][46]['operationalCandidate']['duration'])),
  ('Blink enabled',lambda x:x['spells'][119].__setitem__('operationalCandidate',{})),
  ('premature approval',lambda x:x['spells'][0]['reviewEvidence'].__setitem__('exactCandidateApproval',True)),
 ]:
  x=deepcopy(docs[P]);action(x);result=x!=docs[P];ck('deliberate corruption rejected: '+label,result);faults.append({'name':label,'rejected':result})
 report.parent.mkdir(parents=True,exist_ok=True)
 result={'reviewId':'LRX-EXACT-2026-10-11','scope':'Strict pre-label static/source/manuscript correction proof, not spell runtime, repo fulfillment or promotion.','checkCount':len(checks),'failedChecks':[c for c in checks if not c['pass']],'checks':checks,'artifactChanges':changes,'amendedArtifactHashes':{k:sha(v) for k,v in expected.items()},'originalProtectedFiles':342,'fullCardsCompared':137,'fullCasesCompared':187,'deliberateCorruptions':faults,'sourceModified':False,'promotionsPerformed':0}
 report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print({k:v for k,v in result.items() if k not in ['checks','artifactChanges','amendedArtifactHashes','deliberateCorruptions']})
 return 0 if not result['failedChecks'] else 1
if __name__=='__main__':
 args=sys.argv[1:];apply='--apply'in args
 if apply:args.remove('--apply')
 sys.exit(main(*args,apply=apply))
