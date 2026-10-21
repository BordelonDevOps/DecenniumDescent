#!/usr/bin/env python3
"""Read-only, standard-library artifact/source verifier. Does not execute input code."""
from __future__ import annotations
from pathlib import Path, PurePosixPath
from zipfile import ZipFile
from io import BytesIO
from copy import deepcopy
import argparse,json,hashlib
RET='DD_Rank9_Resonance_Fields_3_Part5_Conference_Return_01.zip'
PK='DD_Resonance_Fields3_Receipt_Followthrough_86.zip'
KEY='wizard.supplement.arcane-feedback'
def sh(b):return hashlib.sha256(b).hexdigest()
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def vh(v):return sh(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def ptr(obj,path):
 for token in path.split('/')[1:]:
  token=token.replace('~1','/').replace('~0','~');obj=obj[int(token)] if isinstance(obj,list) else obj[token]
 return obj

def mutate(obj,path,value=None,remove=False):
 tokens=path.split('/')[1:];p=obj
 for token in tokens[:-1]:
  token=token.replace('~1','/').replace('~0','~');p=p[int(token)] if isinstance(p,list) else p[token]
 token=tokens[-1].replace('~1','/').replace('~0','~')
 if isinstance(p,list):
  if remove:del p[int(token)]
  else:p[int(token)]=deepcopy(value)
 elif remove:del p[token]
 else:p[token]=deepcopy(value)

def safe(z):
 ns=z.namelist()
 return len(ns)==len(set(ns)) and all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n and ':' not in n.split('/')[0] and ((i.external_attr>>16)&0o170000)!=0o120000 for n,i in zip(ns,z.infolist()))

def run(root):
 checks=[]
 def ck(g,n,c):
  checks.append({'category':g,'check':n,'passed':bool(c)})
  if not c:raise AssertionError(g+': '+n)
 def read(n):return json.loads((root/n).read_bytes())
 b=(root/'input'/RET).read_bytes();ck('input','full exact original Return01',len(b)==54459580 and sh(b)=='09e6ea3b629723294d0da5f5551a460c9146e9f428471c8fe359bc394955f30d');z=ZipFile(BytesIO(b))
 pb=(root/'input'/PK).read_bytes();ck('input','exact supplied followthrough packet',len(pb)==937873 and sh(pb)=='3477ed0f3143da0e4e8c8c40bbc31dfbbbcc18760416e8a5f9ee3521f5e6ae09');p=ZipFile(BytesIO(pb))
 for name,zz,count in [(RET,z,36),(PK,p,22)]:
  ck('archive',name+' safe/unique/membercount',safe(zz) and len(zz.namelist())==count);ck('archive',name+' CRC',zz.testzip() is None)
 for record in json.loads(z.read('MANIFEST.json'))['files']:
  bb=z.read(record['path']);ck('history','original return '+record['path'],len(bb)==record['bytes'] and sh(bb)==record['sha256'])
 for record in json.loads(p.read('PACKET_MANIFEST.json'))['files']:
  bb=p.read(record['path']);ck('history','packet '+record['path'],len(bb)==record['bytes'] and sh(bb)==record['sha256'])
  if record['path'].startswith('received-return01/'):
   ck('history','packet exact old member '+record['path'],bb==z.read(record['path'].split('/',1)[1]))
 ck('report','supplied 3099 remains complete report',json.loads(p.read('LOCAL_DIAGNOSTICS.json'))['checkCount']==3099)
 routing=read('ARCHIVE_REFERENCE_ROUTING.json')['legacyArchiveAliases'];archives={}
 for logical,r in routing.items():
  bb=z.read(r['member']);ck('history','complete nested archive '+logical,len(bb)==r['bytes'] and sh(bb)==r['sha256']);a=ZipFile(BytesIO(bb));archives[logical]=a
  ck('archive','nested safe/CRC '+logical,safe(a) and a.testzip() is None)
 sourcez=archives['input/DD_Rank9_Resonance_Fields_3_Source_Conference_01.zip'];contextz=archives['input/DD_Rank9_Resonance_Fields3_Current_Context_80.zip']
 pendingname='sources/docs/audit/2026-10-08/full-game/DD_Rank9_Casting_Cost_5_Source_Conference_01.zip'
 pending=ZipFile(BytesIO(sourcez.read(pendingname)))
 ck('archive','unchanged pending comparison safe/CRC',safe(pending) and pending.testzip() is None)
 sourceSets={'original':sourcez,'context':contextz,'pending-comparison':pending}
 rows=read('SOURCE_BINDING_VERIFICATION.json')
 for label,n in [('original',99),('context',23),('pending-comparison',117)]:
  ck('source','complete binding count '+label,sum(r['set']==label for r in rows)==n)
 for r in rows:
  bb=sourceSets[r['set']].read('sources/'+r['path']);ck('source',r['set']+'/'+r['path'],len(bb)==r['bytes'] and sh(bb)==r['sha256'])
 refs=read('SOURCE_REFERENCES.json')['aliases']
 for name,r in refs.items():
  bb=archives[r['archive']].read(r['member']);ck('source','full alias '+name,len(bb)==r['bytes'] and sh(bb)==r['sha256'])
  if r.get('pointer'):ptr(json.loads(bb),r['pointer']);ck('source','complete pointer '+name,True)
 for r in read('SOURCE_EVIDENCE.json')['sources']:
  bb=(root/r['completeFile']).read_bytes();ar=r['originalArchiveReference'];ck('source','full direct evidence '+r['alias'],len(bb)==r['bytes'] and sh(bb)==r['sha256'] and bb==archives[ar['archive']].read(ar['member']))
 wizard=json.loads((root/'sources/wizard.json').read_bytes())
 for name,card in read('SOURCE_EVIDENCE.json')['completeCards'].items():ck('source','exact card '+name,card==ptr(wizard,name.split('#',1)[1]))
 ck('source','complete ordinary counter record',read('sources/ordinary_counterspell_complete_record.json')==json.loads(sourcez.read(refs['catalog']['member']))['spells'][38])
 oldb=z.read('MODEL.json');old=json.loads(oldb);mb=(root/'MODEL.json').read_bytes();m=json.loads(mb);origb=sourcez.read('CANDIDATE.json');orig=json.loads(origb)
 ck('reconstruction','Return01 original serializer exact',enc(old)==oldb)
 ck('reconstruction','original candidate serializer exact',enc(orig)==origb)
 ck('reconstruction','current serializer exact',enc(m)==mb)
 def operate(start,target,ops,label):
  x=deepcopy(start)
  for i,op in enumerate(ops):
   path=op['path'];before=op['before'];after=op['after']
   if before['present']:
    v=ptr(start,path);ck('reconstruction',f'{label}/{i} full before',ptr(x,path)==v and vh(v)==before['valueSha256'])
   else:
    try:ptr(x,path);exists=True
    except (KeyError,IndexError):exists=False
    ck('reconstruction',f'{label}/{i} genuinely absent',not exists)
   v=ptr(target,path);ck('reconstruction',f'{label}/{i} full after',vh(v)==after['valueSha256']);mutate(x,path,v)
  ck('reconstruction',label+' entire forward bytes',enc(x)==enc(target))
  for i,op in reversed(list(enumerate(ops))):
   ck('reconstruction',f'{label}/{i} exact inverse input',vh(ptr(x,op['path']))==op['after']['valueSha256'])
   if op['before']['present']:mutate(x,op['path'],ptr(start,op['path']))
   else:mutate(x,op['path'],remove=True)
  ck('reconstruction',label+' entire reverse bytes',enc(x)==enc(start))
 plan=read('EXACT_OPERATIONS_FROM_RETURN01.json');ck('reconstruction','incremental6',plan['operationCount']==len(plan['operations'])==6)
 ck('binding','current MODEL exact lengths/hash',plan['successor']['bytes']==len(mb) and plan['successor']['sha256']==sh(mb))
 operate(old,m,plan['operations'],'incremental')
 alt=read('EXACT_OPERATIONS_FROM_SOURCE.json');historical=json.loads(z.read('EXACT_OPERATIONS_FROM_SOURCE.json'))
 ck('reconstruction','preserved original21 complete ops',alt['stage1']['completeOriginalPlan']==historical)
 ck('reconstruction','alternative27 with exact second stage',alt['operationCount']==27 and alt['stage2']==plan)
 operate(orig,old,historical['operations'],'historical-stage1')
 # The two verified full-byte endpoints compose directly; no simultaneous alternate plans.
 ck('reconstruction','alternative exact intermediate binding',historical['successor']['sha256']==sh(oldb) and plan['baseline']['sha256']==sh(oldb))
 expected_paths={'/id','/recordedAtUtc','/status','/currentVectors/4/independentBranches/2','/currentVectors/5/independentBranches/0','/arcaneFeedbackReceiptFollowthrough'}
 ck('preservation','only declared model paths',set(op['path'] for op in plan['operations'])==expected_paths)
 for k in old:
  if k not in ['id','recordedAtUtc','status','currentVectors']:ck('preservation','unchanged root '+k,m[k]==old[k])
 ck('mirror','full receipt contract',m['arcaneFeedbackReceiptFollowthrough']==read('FEEDBACK_RECEIPT_CONTRACT.json'))
 ck('mirror','full current casebook',read('CASE_DISPOSITIONS.json')['cases']==m['currentVectors'])
 doc=(root/'DIRECTOR_REVIEW.md').read_text();newcase=json.dumps(read('CASE_DISPOSITIONS.json'),ensure_ascii=False,indent=2);oldcase=json.dumps(json.loads(z.read('CASE_DISPOSITIONS.json')),ensure_ascii=False,indent=2)
 ck('mirror','Director exact complete casebook',doc.count('```json\n'+newcase+'\n```')==1)
 priorDoc=doc.split('\n\n# Bounded Arcane Feedback receipt follow-through',1)[0].replace(newcase,oldcase,1)
 ck('preservation','complete Director prefix/procedures/questions/holds unchanged',priorDoc.encode()==z.read('DIRECTOR_REVIEW.md'))
 for name in ['PROCEDURES.json','SHARED_RULES.json','QUESTION_DISPOSITIONS.json','ACTOR_TEMPLATES.json','ACTOR_FEATURE_ACCOUNTING.json','SOURCE_REFERENCES.json','HOLD_REGISTER.json','SOURCE_AUTHORITY.json','SOURCE_EXCERPTS.json','SOURCE_BINDING_VERIFICATION.json','SPELL_DISPOSITIONS.json','PLAYER_CHAPTER.md','DECISIONS.md','ALL_MAGIC_CATEGORY_MAP.json','PENDING_COMPARISON_NOT_ADOPTED.json','ORIGINAL_HISTORY.json']:
  ck('preservation','byte-identical '+name,(root/name).read_bytes()==z.read(name))
 changes={(4,2):'E',(5,0):'B'}
 affected=read('AFFECTED_CASES.json')['cases'];ix=0;allCases=[]
 for ci,(oc,nc) in enumerate(zip(old['currentVectors'],m['currentVectors'])):
  allCases.append(nc);allCases.extend(nc['independentBranches'])
  for k in oc:
   if k!='independentBranches':ck('preservation',f'main{ci} complete {k}',nc[k]==oc[k])
  for bi,(ob,nb) in enumerate(zip(oc['independentBranches'],nc['independentBranches'])):
   if (ci,bi) not in changes:ck('preservation',ob['id']+' entire branch unchanged',nb==ob);continue
   a=affected[ix];ix+=1;owner=changes[(ci,bi)]
   ck('mirror',ob['id']+' full before/after record',a['completeBefore']==ob and a['completeAfter']==nb)
   stripped=deepcopy(nb);stripped.pop('feedbackReceiptBinding')
   states=[stripped['initialState']]+[t[k] for t in stripped['timeline'] for k in ['before','after']]+[stripped['finalState']]
   for si,s in enumerate(states):
    ctx=s.pop('numberedRoundContext');l=s['actors'][owner]['limitedUses'].pop(KEY)
    ck('receipt',ob['id']+f'/state{si} genuine fixture round',ctx['ordinal']==1 and ctx['roundId']==oc['id']+':round:1' and ctx['startMarker']==0 and ctx['nextBoundaryMarker']==6)
    ck('receipt',ob['id']+f'/state{si} actual actor/source',l['ownerId']==owner and l['sourceRef']=='wizard#/cards/60')
    for rid,link in l['roundUses'].items():
     rec=l['sourceSettlements'][link['settlementId']]
     ck('receipt',ob['id']+f'/state{si} exact positive award',link['state']=='spent' and rec['roundId']==rid and rec['creditedRP']==1 and rec['rpBeforeRecovery']+1==rec['rpAfterRecovery'] and rec['rpAfterRecovery']<=rec['normalMaxRP']==64)
     cr=s['castRecords'][rec['counterCastId']];tr=s['castRecords'][rec['negatedCastId']]
     ck('receipt',ob['id']+f'/state{si} actual source/target',cr['owner']==owner and cr['state']=='resolved' and tr['state']=='countered' and cr['nativeSourceRef']==rec['nativeCounterSourceRef'])
     ck('receipt',ob['id']+f'/state{si} no new Reaction',s['actors'][owner]['reaction'] is False)
   ck('preservation',ob['id']+' strip annotations restores entire original branch',stripped==ob)
 ck('cases','seven mains28 branches',len(m['currentVectors'])==7 and len(allCases)==35)
 ck('cases','four genuine conditional branches',sum(c['disposition']=='CONDITIONAL_EXTERNAL_PREMISE' for c in allCases)==4)
 for c in allCases:ck('cases',c['id']+' full final mirror',c['timeline'][-1]['after']==c['finalState'])
 ck('preservation','unchanged applied counts',all(m['reviewBoundary'][k]==v for k,v in [('appliedReviewed',525),('appliedPending',323),('standalone',249),('scopedInterfaces',173),('acceptedButUnappliedBeforeThisReview',50)]))
 d=read('FEEDBACK_DIAGNOSTICS.json');ck('diagnostic-report','31 finite diagnostic cases',d['caseCount']==len(d['cases'])==31)
 ck('diagnostic-report','64 actual expectations pass',d['assertionCount']==len(d['assertions'])==64 and d['failures']==0 and all(x['pass'] for x in d['assertions']))
 # This verifies the saved diagnostic, not an execution of its code by this verifier.
 for c in d['cases']:
  before=c['before'];after=c['after'];result=c['result']
  ck('diagnostic-report',c['id']+' actualRP bounded',0<=after['rp']<=after['maxRP'])
  ck('diagnostic-report',c['id']+' reward adds no action/reaction',before['action']==after['action'] and before['reaction']==after['reaction'])
  ck('diagnostic-report',c['id']+' credited amount0/1',result['creditedRP'] in [0,1] and after['rp']-before['rp']==result['creditedRP'])
 reps=read('ARTIFACT_REPLACEMENTS_FROM_RETURN01.json');ck('artifact','replacement count',reps['replacementCount']==len(reps['replacements']))
 for e in reps['replacements']:
  b0=z.read(e['before']['member']);b1=(root/e['after']['file']).read_bytes()
  ck('artifact',e['path']+' full before',len(b0)==e['before']['bytes'] and sh(b0)==e['before']['sha256'])
  ck('artifact',e['path']+' full after',len(b1)==e['after']['bytes'] and sh(b1)==e['after']['sha256'])
  ck('artifact',e['path']+' distinct and reversible whole bytes',b0!=b1 and z.read(e['before']['member'])==b0)
 for e in read('ARTIFACT_BINDINGS.json')['currentAuthorshipAndEvidence']:
  bb=(root/e['file']).read_bytes();ck('binding',e['file'],len(bb)==e['bytes'] and sh(bb)==e['sha256'])
 historical=read('HISTORY_BINDINGS.json')
 for rows,archive in [(historical['allOriginalReturnMembers'],z),(historical['allPacketMembers'],p)]:
  for e in rows:
   bb=archive.read(e['path']);ck('history','full inventory '+e['path'],len(bb)==e['bytes'] and sh(bb)==e['sha256'])
 mf=root/'MANIFEST.json'
 manifestChecked=0
 if mf.exists():
  mfj=read('MANIFEST.json')
  for e in mfj['files']:
   bb=(root/e['path']).read_bytes();ck('manifest',e['path'],len(bb)==e['bytes'] and sh(bb)==e['sha256']);manifestChecked+=1
  ck('manifest','count and no hidden extra file',manifestChecked==mfj['fileCount'] and {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}=={e['path'] for e in mfj['files']}|{'MANIFEST.json'})
 return {'id':'RF9-FEEDBACK-READ-ONLY-VERIFICATION-02','scope':'Source, complete-byte reconstruction, mirror and saved-diagnostic consistency only. Does not run historical or project modules; separate isolated diagnostic execution reported independently.',
         'checkCount':len(checks),'failures':sum(not c['passed'] for c in checks),'manifestFilesChecked':manifestChecked,'checks':checks,
         'gameRuntimeExecuted':False,'historicalReportsRerun':False,'implementationApplied':False}

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--report',type=Path);a=p.parse_args()
 r=run(a.root)
 if a.report:
  if a.report.exists():raise SystemExit('Refusing to overwrite evidence')
  a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_bytes(enc(r))
 print(json.dumps({'checkCount':r['checkCount'],'failures':r['failures'],'manifestFilesChecked':r['manifestFilesChecked']}))
if __name__=='__main__':main()
