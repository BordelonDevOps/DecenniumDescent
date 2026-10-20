"""Read-only verification of exact archives, sources, code spans and complete cases.
No delivered project module is imported or executed. Does not apply corrections.
"""
from pathlib import Path,PurePosixPath
from collections import Counter
import argparse,hashlib,json,zipfile,ast
B=Path(__file__).resolve().parent

def digest(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def read(name):return json.loads((B/name).read_text(encoding='utf-8'))
def safe(name):
 p=PurePosixPath(name)
 return bool(name) and not p.is_absolute() and '\\' not in name and '..' not in p.parts and not any(':' in s for s in p.parts)
def pointer(obj,p):
 for part in p.split('/')[1:]:
  key=part.replace('~1','/').replace('~0','~');obj=obj[int(key)] if isinstance(obj,list) else obj[key]
 return obj

def verify(include_manifest=True):
 checks=[]
 def check(kind,key,passed):
  checks.append({'kind':kind,'id':key,'passed':bool(passed)})
  if not passed:raise ValueError(kind+': '+key)
 inp=read('INPUT_BINDINGS.json')['inputs'];union={};members={}
 for meta in inp:
  p=B/meta['path'];check('archive-binding',meta['path'],digest(p.read_bytes())=={k:meta[k] for k in ('bytes','sha256')})
  with zipfile.ZipFile(p) as z:
   names=z.namelist();check('archive-safety',p.name,len(names)==len(set(names)) and all(safe(n) and (i.external_attr>>16)&0o170000!=0o120000 for n,i in zip(names,z.infolist())) and z.testzip() is None)
   m=json.loads(z.read('MANIFEST.json'));entries=m.get('sources',m.get('files',[]));prefix='sources/' if meta['manifestSourceCount'] is not None else ''
   if meta['manifestSourceCount'] is not None:check('source-count',p.name,len(entries)==meta['manifestSourceCount'])
   for e in entries:
    data=z.read(prefix+e['path']);check('member-binding',p.name+'::'+e['path'],digest(data)=={k:e[k] for k in ('bytes','sha256')})
    if prefix:
     if e['path'] in union:check('overlap-identical',e['path'],union[e['path']]==data)
     union[e['path']]=data
   members[p.name]={n:z.read(n) for n in names if not n.endswith('/')}
 check('source-count','unique-source-union',len(union)==78)
 sv=read('SOURCE_VERIFICATION.json')
 for p,meta in sv['uniqueSourceBindings'].items():check('source-binding',p,digest(union[p])=={k:meta[k] for k in ('bytes','sha256')})
 for meta in read('CODE_BINDINGS.json')['files']:
  p=meta['path'];before=(B/'baseline'/p).read_bytes();after=(B/'proposed'/p).read_bytes()
  check('code-binding',p+'/before',digest(before)==meta['before'] and before==union[p])
  check('code-binding',p+'/after',digest(after)==meta['after'])
  ops=[o for o in read('CODE_OPERATIONS.json')['operations'] if o['path']==p]
  current=before.decode('utf-8')
  for o in ops:
   check('forward-full-span',o['id'],current.count(o['before'])==1)
   current=current.replace(o['before'],o['after'],1)
  check('forward-full-file',p,current.encode('utf-8')==after)
  for o in reversed(ops):
   check('reverse-full-span',o['id'],current.count(o['after'])==1)
   current=current.replace(o['after'],o['before'],1)
  check('reverse-full-file',p,current.encode('utf-8')==before)
  ast.parse(after.decode('utf-8'));check('code-syntax',p,True)
 # Complete preserved historical objects and full independently captured replays.
 cd=read('CASE_DISPOSITIONS.json')
 for group,oldkey,reportfield in [('histories','completeOriginalHistory','histories'),('readyLifecycleHistories','completeOriginalHistory','readyLifecycleHistories'),('sourceAcceptanceExamples','completeOriginalExpectationAndDisposition','acceptanceCoverage')]:
  for case in cd[group]:
   ref=case['source'];old=pointer(json.loads(union[ref['path']]),ref['pointer'])
   check('complete-case',case['id'],old==case[oldkey])
   if group=='histories':
    check('complete-baseline-replay',case['id'],old==case['completeBaselineReplayHistory'])
    rpt=read('tests/results/proposed_'+case['package']+'_replay.json');index=int(ref['pointer'].split('/')[-1])
    check('complete-proposed-replay',case['id'],rpt['histories'][index]==case['completeProposedReplayHistory'])
 check('case-counts','complete-groups',[len(cd[k]) for k in ('histories','readyLifecycleHistories','sourceAcceptanceExamples')]==[68,7,13])
 profiles=read('PROFILE_DISPOSITIONS.json')
 for p in profiles['profiles']:
  ref=p['source'];check('complete-profile',p['id'],pointer(json.loads(union[ref['path']]),ref['pointer'])==p['completeAcceptedProfile'])
 for finding in read('FINDINGS.json')['findings']:
  for ref in [finding['evidence']]+finding['sourceRefs']:
   data=union[ref['path']];check('reference-binding',finding['id']+'::'+ref['path'],digest(data)=={k:ref[k] for k in ('bytes','sha256')})
   if 'pointer' in ref:pointer(json.loads(data),ref['pointer'])
   else:check('reference-lines',finding['id']+'::'+ref['symbol'],0<ref['startLine']<=ref['endLine']<=len(data.decode('utf-8').splitlines()))
 prior=members['DD_Part5_Control_Ready_Corrections_01.zip']
 decision=next(x for x in json.loads(prior['SCOPED_DECISIONS.json'])['decisions'] if x['id']=='COPY-READY-ALLOWANCE-01')
 check('prior-exact-decision','Ready unchanged',decision==read('evidence/PROPOSED_COPY_READY_DECISION_UNCHANGED.json')==read('READY_GAP_MATRIX.json')['completeProposedRuleUnchanged'])
 for e in read('SOURCE_PRECEDENCE.json')['fourFeatJsonBaselines']:
  check('prior-rule-baseline',e['path'],prior['baseline/'+e['path']]==union[e['path']])
 control=members['DD_Control_15_Full_Conference_Part5_Return_02.zip']
 check('prior-exact-receipt','Control15',json.loads(control['REVIEW_RECEIPT.json'])==read('evidence/CONTROL15_FULL_RECEIPT_UNCHANGED.json'))
 for suite in ('release','payloads','classes'):
  orig=json.loads(union['docs/audit/2026-10-08/full-game/FEAT335_COPY_'+suite.upper()+'_01_CHECK.json']);rep=read('tests/results/baseline_'+suite+'_replay.json');prop=read('tests/results/proposed_'+suite+'_replay.json')
  for field in ['histories','results']+(['readyLifecycleHistories','acceptanceCoverage'] if suite=='release' else ['coverage'] if suite=='classes' else []):
   check('full-frozen-report-field',suite+'/'+field,orig[field]==rep[field])
  check('reported-reference-checks',suite,orig['checks']==rep['checks']==prop['checks'] and not prop['failures'])
 reg=read('tests/results/new_regressions.json');check('reported-new-tests','47 isolated guards',reg['testsRun']==47 and reg['failures']==reg['errors']==0)
 # These are report-consistency checks on retained probe results, not reexecution.
 oldprobes=read('tests/results/baseline_full_probes.json')['probes']
 newprobes=read('tests/results/proposed_full_probes.json')['probes']
 for i,(old,new) in enumerate(zip(oldprobes,newprobes)):
  check('recorded-adversarial-result',old['id']+'/original',old['outcome']['rejected'] is False)
  check('recorded-adversarial-result',new['id']+'/proposed',old['id']==new['id'] and new['outcome']['rejected']==(i>=2))
 check('recorded-adversarial-result','shared-native-reactions',all(p['extraAfter']['nativeReaction']==0 and p['extraAfter']['captureReaction']==0 for p in newprobes[:2]))
 check('recorded-adversarial-result','native-unconscious-no-heal',oldprobes[3]['extraAfter']['targetHP']==32 and newprobes[3]['extraAfter']['targetHP']==30)
 check('recorded-adversarial-result','native-step-position-guard',oldprobes[5]['extraAfter']['copyWorldPosition']==[-15,0,0] and newprobes[5]['extraAfter']['copyWorldPosition']==[0,0,0] and newprobes[5]['extraAfter']['nativePositionFeet']==0)
 # Revalidate every dictionary source reference with an exact source hash/pointer.
 def scan(obj):
  if isinstance(obj,dict):
   if 'path' in obj and obj['path'] in union and 'sha256' in obj:
    check('cross-reference-source',obj.get('pointer',obj.get('symbol',obj['path'])),digest(union[obj['path']])['sha256']==obj['sha256'])
    if 'pointer' in obj:pointer(json.loads(union[obj['path']]),obj['pointer'])
   for v in obj.values():scan(v)
  elif isinstance(obj,list):
   for v in obj:scan(v)
 for name in ['PROFILE_DISPOSITIONS.json','SOURCE_PRECEDENCE.json']:scan(read(name))
 if include_manifest and (B/'MANIFEST.json').exists():
  m=read('MANIFEST.json')
  for e in m['files']:
   check('return-member',e['path'],safe(e['path']) and digest((B/e['path']).read_bytes())=={k:e[k] for k in ('bytes','sha256')})
 report={'scope':'Independent read-only byte/full-value/source/reference/structure verification, not semantic tests, runtime execution or application.',
         'checkCount':len(checks),'failures':0,'counts':dict(Counter(x['kind'] for x in checks)),'manifestChecked':include_manifest and (B/'MANIFEST.json').exists(),'checks':checks}
 return report,union

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--report');p.add_argument('--without-return-manifest',action='store_true');a=p.parse_args()
 report,_=verify(not a.without_return_manifest)
 if a.report:
  dest=Path(a.report).resolve()
  if dest.is_relative_to(B) and dest.name!='VERIFICATION_REPORT.json':
   raise SystemExit('Write additional verification reports outside the bound return directory.')
  if dest.exists():raise SystemExit('Refusing to overwrite an existing report; choose a new output path.')
  dest.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print(json.dumps({k:report[k] for k in ['checkCount','failures','counts','manifestChecked']}))
