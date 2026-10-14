#!/usr/bin/env python3
"""Read-only input verification and bounded authoring/reference checks, not a feat runtime.
Usage: python verify_source_package.py /path/to/DD_Feats_327_Complete_Proposals_EX58_v3.zip [output_report.json]
Run beside the delivered register files. Writes only the specified/default output report.
"""
from pathlib import Path
from fractions import Fraction
import json,hashlib,zipfile,sys,math
HERE=Path(__file__).resolve().parent
EXPECTED='0e68cb0c9aab2ac6142bf6e5b7ca6b833a3ce3504969e83c0d2d27956e4c2ac8'
MANIFEST='48c969f4d98e23ad87c622126ce9e74f2da1e28f3205d0f9132527cd21ab5a8b'
checks=[]
def ck(name,ok,detail=None,kind='executed source/structure check'):
 checks.append({'id':name,'pass':bool(ok),'kind':kind,**({'detail':detail} if detail is not None else {})})
def sha(b):return hashlib.sha256(b).hexdigest()
def read(n):return json.loads((HERE/n).read_text(encoding='utf-8'))
def run(zpath):
 raw=zpath.read_bytes();ck('archive-bytes',len(raw)==65871529);ck('archive-sha',sha(raw)==EXPECTED)
 if sha(raw)!=EXPECTED:raise ValueError('Wrong submission SHA; no comparisons run against a replacement archive.')
 with zipfile.ZipFile(zpath) as z:
  mb=z.read('FILE_MANIFEST.json');ck('manifest-sha',sha(mb)==MANIFEST)
  if sha(mb)!=MANIFEST:raise ValueError('Wrong root manifest SHA')
  m=json.loads(mb);ck('manifest-count',len(m)==707)
  ck('zip-names-unique',len(z.namelist())==len(set(z.namelist())))
  ck('zip-payload-membership',set(z.namelist())==set(m)|{'FILE_MANIFEST.json'})
  for p,v in m.items():
   b=z.read(p);ck('payload:'+p,len(b)==v['bytes'] and sha(b)==v['sha256'])
  reg=read('FEAT_327_AUTHORING_REGISTER.json')['records'];ck('327-identities',len(reg)==327 and len({x['featId'] for x in reg})==327)
  ck('327-question-identities',len({x['questionId'] for x in reg})==327)
  src={p:json.loads(z.read(p)) for p in {x['sourcePath'] for x in reg}}
  submitted={r['featId']:(p,i,r) for p,d in src.items() for i,r in enumerate(d['records'])}
  ck('all-submitted-feats-covered',set(submitted)=={x['featId'] for x in reg})
  for row in reg:
   fid=row['featId'];p,i,r=submitted[fid]
   ck('source:'+fid,row['originalSourceObject']==r['sourceObject'] and row['sourceFileSha256']==m[p]['sha256'])
   ck('question:'+fid,row['originalQuestion']==r.get('originalQuestion',r.get('originalIssue')) and row['questionId']==r.get('questionId',r.get('proposalId')))
   ck('historical-procedure:'+fid,row['submittedProcedure']==r['procedure'] and row['submittedWorkedCases']==r['workedCases'])
   ck('current-complete:'+fid,bool(row['completeAuthoringProcedure']) and bool(row['decision']) and len(row['workedCases'])==len(r['workedCases']))
   ck('not-promoted:'+fid,row['selectionEnabled'] is False and row['exactApproved'] is False and row['runtimeApproved'] is False)
   text=(HERE/'cohorts'/f"{row['cohort'].upper()}.md").read_text(encoding='utf-8')
   ck('manuscript:'+fid,row['completeAuthoringProcedure'] in text and all(x in text for x in row['workedCases']))
   # Submitted manuscript is checked for complete procedure presence, not just the feat title.
   sp='DescentReviewChanges/ReviewBible/docs/feats/'+row['cohort'].upper()+'_FEAT_OPERATING_PROPOSAL.md'
   st=z.read(sp).decode('utf-8-sig')
   ck('submitted-full-procedure-in-manuscript:'+fid,r['procedure'] in st)
  ck('two-deferred', {x['featId'] for x in reg if x['payloadOperational'] is None}=={'astral_projection','planar_binding'})
  ops=read('FEAT_EXACT_REPLACEMENTS.json')['operations'];ri={x['featId']:x for x in reg}
  for op in ops:
   p,i,r=submitted[op['featId']];field=op['pointer'].split('/')[-1]
   target='completeAuthoringProcedure' if field=='procedure' else 'workedCases'
   ck('operation:'+op['id'],op['path']==p and op['pointer']==f'/records/{i}/{field}' and op['old']==r[field] and op['replacement']==ri[op['featId']][target])
  cs=read('FEAT_660_EXAMPLE_DISPOSITIONS.json')['cases'];ck('660-example-identities',len(cs)==660 and len({x['id'] for x in cs})==660)
  for x in cs:
   p,i,r=submitted[x['featId']];k=int(x['sourcePointer'].split('/')[-1])
   ck('example-binding:'+x['id'],x['original']==r['workedCases'][k] and x['completeExpectedOutcome']==ri[x['featId']]['workedCases'][k])
  f=read('FEX_01_15_DISPOSITIONS.json')['issues'];orig=json.loads(z.read('docs/audit/2026-10-08/full-game/FEAT_EX58_JOINT_INTERFACE_REGISTER.json'))['issues']
  ck('15-fex',len(f)==15 and {x['id'] for x in f}=={x['id'] for x in orig})
  for x,y in zip(f,orig):ck('fex:'+x['id'],x['originalQuestion']==y['questionAndLocalRecommendation'] and bool(x['completeResolution']))
  conv=read('FEAT_SHARED_CONVENTION_DISPOSITIONS.json')['entries'];ck('91-conventions',len(conv)==91)
  for x in conv:
   obj=src[x['sourcePath']]
   for key in x['pointer'].strip('/').split('/'):obj=obj[int(key)] if isinstance(obj,list) else obj[key]
   ck('convention:'+x['cohort']+x['pointer'],obj==x['original'] and bool(x['replacement']))
  groups=read('FEAT_SUPPLEMENT_DIRECTIONS.json')['groups'];ck('9-supplement-groups',len(groups)==9)
  for x in groups:
   obj=src[x['sourcePath']][x['pointer'][1:]];ck('supplement:'+x['id'],obj==x['original'] and bool(x['completeAuthoringValue']) and not x['exactApproved'])
  ck('28-additional-cases',len(read('FEAT_ADDITIONAL_BOUNDARY_EXPECTATIONS.json')['cases'])==28)
  full='\n'.join(r['completeAuthoringProcedure'] for r in reg)
  for bad in ['metr own','You cannot target yourself.','reverting to 60 if that other source ends','distinct Crippling Strike can add a separate','eligible only for the attack mode if it is actually melee','these fields discharge after that first eligible trigger']:
   ck('rejected-old-clause:'+bad,bad not in full)
 # Independent reference calculations. These do not execute the feat procedures.
 def ref(n,a,b):ck(n,a==b,{'actual':str(a),'expected':str(b)},'executed bounded reference arithmetic')
 ref('forage-mass',14+56,70);ref('standard-survivalist-food',Fraction(2,2),1);ref('standard-survivalist-water',Fraction(8,2),4)
 ref('large-survivalist-food',Fraction(4,2),2);ref('large-survivalist-water',Fraction(16,2),8)
 ref('flat-feats-class',2+2+max(1,2),6);ref('native-percent',19+math.floor(Fraction(19,10)),20);ref('save-after-percent',math.floor(Fraction(20,2)),10)
 ref('two50percent',10+math.floor(Fraction(10,2))+math.floor(Fraction(10,2)),20)
 ref('strongest-slow',min(30-10,30-10,math.floor(Fraction(30,2))),15)
 ref('lock',3+2+2,7);ref('expert-lock',3+2*2+2,9)
 ref('quick-ritual',6+max(300,math.ceil(Fraction(600,2))),306)
 ref('combined-ritual',min(306,max(306,math.ceil(Fraction(306*3,4)))),306)
 ref('channel-only',max(900,math.ceil(Fraction(1200*3,4))),900)
 ref('assay-payment1',max(Fraction(100,10),3),10);ref('assay-fine1',max(0,Fraction(100,10)-3),7)
 ref('assay-payment2',max(Fraction(100,10),12),12);ref('assay-fine2',max(0,Fraction(100,10)-12),0)
 ref('copy-rank',max(1,4//2),2);ref('copy-cap',min(12,10//2),5);ref('zero-copy-cap',1//2,0)
 ref('capacity-refund',min(3,8-7),1);ref('half-animal-hp',max(1,10*5//10),5)
 ref('endurance-two-causes',sum([0,0,1,1]),2)
 return {'kind':'Executed read-only source/structure/manuscript and bounded arithmetic checks; not a feat runtime, human test or campaign authentication','submissionSha256':EXPECTED,'checks':len(checks),'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'results':checks}
if __name__=='__main__':
 if len(sys.argv)<2:raise SystemExit(__doc__)
 output=Path(sys.argv[2]) if len(sys.argv)>2 else HERE/'FEAT_REPRODUCTION_REPORT.json'
 result=run(Path(sys.argv[1]));output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2));raise SystemExit(1 if result['failed'] else 0)
