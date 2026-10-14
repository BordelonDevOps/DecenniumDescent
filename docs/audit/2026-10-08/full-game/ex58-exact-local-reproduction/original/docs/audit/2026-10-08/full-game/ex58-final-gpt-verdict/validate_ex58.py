#!/usr/bin/env python3
"""Read-only source preservation and small reference arithmetic audit.
Not a gameplay/runtime adapter. Uses Python standard library only.
Writes only the requested report; never edits the submitted archive or real saves.
"""
import argparse, hashlib, io, json, math, re
from collections import Counter
from fractions import Fraction
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

EXPECTED_SHA='be4ea5aaf98a44faa05c2f270ceb25f3877c8c9be761cac7c99389d62cbe9b93'
EXPECTED_BYTES=21078954
A='docs/audit/2026-10-08/full-game/'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def sha(b):return hashlib.sha256(b).hexdigest()
def ceilq(x):return -((-x.numerator)//x.denominator)
def floorq(x):return x.numerator//x.denominator
def readq(x):
 if isinstance(x,dict):return Fraction(x['numerator'],x['denominator'])
 return Fraction(str(x))
def task_degree(die,mod,dc):
 m=die+mod-dc
 d=3 if m>=10 else 2 if m>=0 else 1 if m>=-9 else 0
 return max(0,min(3,d+(1 if die==20 else -1 if die==1 else 0)))
def severity(p,n,mod=0,rerolled=False):
 if not(0<=p<=6 and 1<=n<=6):raise ValueError('invalid pressure/die')
 if p==0:return 'none'
 if p==6:return 'Severe'
 r=n+mod
 if r>p:return 'none'
 if n==1:return 'Severe'
 if r==p and (mod!=0 or rerolled):return 'Minor'
 return 'Standard'
def checkpoints(mapping,length):
 L=Fraction(length)
 if L<=0:return []
 if mapping=='Mapped':return [L/2,L] if L>=6 else [L]
 if mapping=='Secured':return [L] # actual extra transitions belong to the real route record
 step=3 if mapping=='Sketched' else 2
 return [Fraction(i) for i in range(step,ceilq(L),step) if i<L]+[L]
def standing(opening,deltas):return max(-3,min(3,opening+max(-2,min(2,sum(deltas)))))
def valid_score(x):return type(x) is int and -3<=x<=3

def run(archive,package):
 checks=[]
 def ck(cat,name,cond,detail=None):checks.append({'category':cat,'name':name,'passed':bool(cond),'detail':detail})
 def jl(name):return json.loads((package/name).read_text(encoding='utf-8'))
 b=archive.read_bytes(); ck('archive','exact bytes/SHA',len(b)==EXPECTED_BYTES and sha(b)==EXPECTED_SHA,{'bytes':len(b),'sha256':sha(b)})
 z=ZipFile(io.BytesIO(b));mf=json.loads(z.read('FILE_MANIFEST.json'))
 ck('archive','304 manifest payloads',len(mf)==304)
 ck('archive','305 unique ZIP entries',len(z.namelist())==305 and len(set(z.namelist()))==305)
 for name,e in mf.items():
  raw=z.read(name);ck('source preservation',name,len(raw)==e['bytes'] and sha(raw)==e['sha256'])
 hist=json.loads(z.read(A+'EXPEDITION_INTEGRATED_V3_SOURCE_HISTORY.json'))
 reg=jl('EX58_AUTHORING_REGISTER.json');by={r['id']:r for r in reg['directions']}
 ck('authoring coverage','58 unique directions',len(by)==len(reg['directions'])==58)
 for q in hist['questions']:
  old=q['originalQuestion'];r=by.get(old['id']);ck('original questions',old['id'],r is not None and r['originalQuestion']==old and len(r['authoringWording'])>300)
 cnt=Counter('RP-A' if k.startswith('RP-A') else k.split('-')[0] for k in by)
 ck('authoring coverage','26/12/14/6',dict(cnt)=={'FL':26,'SO':12,'TR':14,'RP-A':6},dict(cnt))
 for row in hist['historicalCurrentPairs']:
  old=z.read(row['preservedOriginalPath']);cur=z.read(row['currentPath'])
  ck('revision history',row['currentPath'],sha(old)==row['originalV2']['sha256'] and sha(cur)==row['current']['sha256'])
 old_archive=hist['originalV2Archive'];old_bytes=z.read(old_archive['path']);old_zip=ZipFile(io.BytesIO(old_bytes));old_manifest=json.loads(old_zip.read('FILE_MANIFEST.json'))
 ck('revision history','exact nested V2 archive',len(old_bytes)==old_archive['bytes'] and sha(old_bytes)==old_archive['sha256'])
 pair={r['currentPath']:r['preservedOriginalPath'] for r in hist['historicalCurrentPairs']}
 for name,old_meta in old_manifest.items():
  old=old_zip.read(name);dest=pair.get(name,name)
  ck('full original V2 preservation',name,len(old)==old_meta['bytes'] and sha(old)==old_meta['sha256'] and z.read(dest)==old)
 # Parse exact actual DOCX XML, not just a preparation assertion.
 cache={}
 def doc(path):
  if path not in cache:
   dz=ZipFile(io.BytesIO(z.read(path)));root=ET.fromstring(dz.read('word/document.xml'));body=root.find('w:body',NS)
   text=lambda p:''.join(t.text or '' for t in p.findall('.//w:t',NS))
   allp=[text(p) for p in root.findall('.//w:p',NS)];direct=[text(p) for p in body.findall('w:p',NS)]
   tables=[[[[text(p) for p in c.findall('w:p',NS)] for c in row.findall('w:tc',NS)] for row in t.findall('w:tr',NS)] for t in body.findall('w:tbl',NS)]
   cache[path]=(allp,direct,tables)
  return cache[path]
 exp=json.loads(z.read(A+'EXPEDITION_HAVEN_FLOW_SOURCE_PREPARATION.json'))
 for key in ('playerExpeditionSource','coreEconomySource'):
  sec=exp[key];path=sec.get('sourceFile',sec.get('file'));pp=doc(path)[0]
  for p in sec.get('paragraphs',sec.get('passages',[])):
   ck('actual book paragraph',f'{key}:{p["paragraph"]}',pp[p['paragraph']]==p['text'])
 tp=json.loads(z.read(A+'TRANSPORT_SOURCE_PREPARATION.json'));profiles=jl('EX58_TRANSPORT_PROFILES.json');pby={p['id']:p for p in profiles['profiles']}
 ck('transport coverage','29 unique source rows and4 distinct auxiliaries',len(pby)==len(profiles['profiles'])==29 and len(profiles['auxiliaryProfiles'])==4)
 for old in tp['sourceEquipmentRecords']:
  p=pby.get(old['id']);ck('transport source equality',old['id'],p is not None and p['sourceRecord']==old)
 for row in tp['actualBookBindings']:
  ck('transport actual book binding',row['id'],doc('books/player/Decennium_Descent_Player_Rulebook_v6.docx')[1][row['paragraphIndex']]==row['exactBookRow'])
 for blockset in tp['selectedSourceBlocks']:
  dd=doc(blockset['source'])
  for block in blockset['blocks']:
   if block['kind']=='paragraph':good=dd[1][block['paragraphIndex']]==block['text']
   elif block['kind']=='table':good=dd[2][block['tableIndex']]==block['rows']
   else:continue
   ck('transport actual source blocks',blockset['source']+':'+str(block.get('paragraphIndex','table'+str(block.get('tableIndex')))),good)
 sp=json.loads(z.read(A+'SOCIAL_FACTION_SOURCE_PREPARATION.json'))
 for blockset in sp['selectedSourceBlocks']:
  dd=doc(blockset['source'])
  for block in blockset['blocks']:
   if block['kind']=='paragraph':good=dd[1][block['paragraphIndex']]==block['text']
   elif block['kind']=='table':good=dd[2][block['tableIndex']]==block['rows']
   else:continue
   ck('social actual source blocks',blockset['id']+':'+str(block.get('paragraphIndex','table'+str(block.get('tableIndex')))),good)
 main=doc('docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx');mirror=doc('DescentReviewChanges/ReviewBible/docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx');mc=sp['directorMirrorComparison']
 for (a,b),(c,d) in zip(mc['mainRanges'],mc['mirrorRanges']):ck('Director mirror','paragraph window'+str([a,b,c,d]),main[1][a:b]==mirror[1][c:d])
 for t in [65,66,67,74]:ck('Director mirror','full table'+str(t),main[2][t]==mirror[2][t])
 cc=jl('EX58_CLASS_INTERFACE_DISPOSITIONS.json');count=0
 for cf in cc['classFiles']:
  raw=z.read(cf['path']);actual=json.loads(raw);cards=actual['cards'];count+=len(cards)
  ck('class preservation',cf['path'],sha(raw)==cf['fileSha256'] and len(cards)==cf['cardCount'] and sha(json.dumps(cards,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==cf['completeCardsCanonicalSha256'])
  ids={c['id']:c for c in cards}
  for q in cf['selectedFullCards']:ck('selected complete class record',q['id'],ids.get(q['id'])==q['card'])
 ck('class coverage','17 complete arrays/1223 cards',len(cc['classFiles'])==17 and count==1223)
 ck('pending comparisons','mounted feats unchanged',cc['pendingMountedFeatComparisons']==tp['pendingFeatComparisons'])
 rp=jl('EX58_REPUTATION_SOURCE_BINDINGS.json');probes=json.loads(z.read(A+'REPUTATION_PRESERVATION_RUNTIME_PROBES.json'))
 ck('reputation preservation','all44 exact faction records',rp['fullOriginalFactionRecords']==probes['fullOriginalFactionRecords'] and len(rp['fullOriginalFactionRecords'])==44)
 ck('reputation coverage','20 backgrounds and12 probe dispositions',len(rp['backgrounds'])==20 and len(rp['probeFinalDispositions'])==12)
 for bg in rp['backgrounds']:ck('background original map',bg['name'],bg['originalRuntimeMap']==probes['fullOriginalBackgroundMappings'][bg['name']])
 wk=jl('EX58_WORKED_SEQUENCES.json');old=json.loads(z.read(A+'SOCIAL_FACTION_PROPOSAL_PREPARATION.json'))['authoredScenarios'];sby={s['id']:s for s in wk['originalProposalScenarios']}
 for s in old:ck('preserved proposal scenario',s['id'],sby[s['id']]['originalScenario']==s and len(sby[s['id']]['finalExpected'])>50)
 covered=set(wk['integratedSequence']['questionIds'])
 for q in wk['additionalBoundaries']:covered.update(q['questionIds'])
 for q in wk['originalProposalScenarios']:covered.add(q['sourceQuestion'])
 ck('authored expectations','all58 questions mapped to examples',set(by)<=covered,{'missing':sorted(set(by)-covered)})
 ck('authored expectations','28 boundaries/24 proposal dispositions/21 integrated events',len(wk['additionalBoundaries'])==28 and len(wk['originalProposalScenarios'])==24 and len(wk['integratedSequence']['events'])==21)
 fc=jl('EX58_FIELD_CONTRACTS.json');ck('field contracts','15 complete contracts',len(fc['contracts'])==15 and all(len(c['requiredFields'])>=6 and len(c['invariants'])>=3 for c in fc['contracts']))
 # All cited operative paths must resolve to frozen source or a packaged authoring file.
 for row in reg['directions']:
  for ref in row['sourceReferences']:
   m=re.match(r'^(.+?\.(?:md|json|docx|js|tsx|txt|csv))(?=\s|:|$)',ref)
   ck('source reference path',row['id']+':'+ref,m is not None and (m[1] in mf or (package/m[1]).is_file()))
 if (package/'EX58_AUTHORING_VERDICT.md').exists():
  text=(package/'EX58_AUTHORING_VERDICT.md').read_text(encoding='utf-8')
  for row in reg['directions']:ck('full verdict wording parity',row['id'],row['authoringWording'] in text)
 if (package/'EX58_EXACT_CANDIDATE_CONTRACT.json').exists():
  ac=jl('EX58_EXACT_CANDIDATE_CONTRACT.json');ck('candidate contract','58 mappings/15finiteareas/no generic blocker',len(ac['questionMap'])==58 and len(ac['acceptanceChecks'])==15 and ac['genuineRemainingAuthoringBlockers']==[])
 # Explicit finite numerical reference trials; these do not run full procedures.
 refs=[]
 def num(name,actual,expected):
  good=actual==expected;refs.append({'name':name,'actual':str(actual),'expected':str(expected),'passed':good});ck('reference arithmetic',name,good)
 num('basket cp',50+1+10+2,63);num('basket with2newskins cp',63+40,103)
 num('basket mass',Fraction(2+8+1)+Fraction(1,4),Fraction(45,4));num('basket plus2tares',Fraction(45,4)+2,Fraction(53,4))
 num('half-pint source-profile filledflask mass',Fraction(1,4)+Fraction(3,4)*Fraction(1,2),Fraction(5,8))
 num('forage3 critical ceiling',3+math.ceil(3/2),5);num('forward marks',3+2+3,8);num('forward newstock pounds',20+300+50+500,870);num('forward newstock gp',2+60+25+100,187)
 num('Contestedtravel minutes',Fraction(480)*Fraction(5,4),600);num('Contested+pause',600+60,660);num('Strain5 travel minutes',Fraction(480)*Fraction(5,4)*Fraction(3)/Fraction(3,2),1200)
 num('ForcedMarch3medium1large',3+2,5);num('Class2to6 surchargeincrement',min(3,6//2)-min(3,2//2),2)
 num('extraction modifierscap',13+min(7,4+1+1+3)+2-2,20)
 num('N_eff multiplier4.5',max(Fraction(1,5),1+Fraction(1,5)*(Fraction(9,2)-4)),Fraction(11,10));num('Standardbudget4.5',90*Fraction(11,10),99)
 num('CRquarter vlevel1bin',math.floor(Fraction(1,4)-1),-1)
 num('retreat round1success',task_degree(11,5,16),2);num('retreat natural20critical',task_degree(20,5,16),3)
 num('rowboatpayload',150+20+300+40+30,540);num('rowboatoverload',540+100,640)
 num('keelboatshoring',3000*Fraction(1,100),30);num('keelboatrepair',3000*Fraction(1,4),750);num('keelboat9hours',max(1,Fraction(90,10)),9)
 num('Casualtyphysical',150+20+10,180);num('CasualtyhalfLoad',Fraction(6+2+1,2),Fraction(9,2));num('Petrifiedbody',150*10,1500)
 num('Integrity2cart30',floorq(Fraction(30*2,3)),20);num('Cartrepairgp',15*Fraction(1,4),Fraction(15,4));num('Cartrepairhours',max(1,Fraction(30,10)),3)
 num('fractional sale',floorq(Fraction(7,3)),2);num('fractional purchase',ceilq(Fraction(7,3)),3);num('teleport12.01Loadwholebill',ceilq(Fraction(1201,100))*100,1300)
 num('sale tax',ceilq(Fraction(12000*5,100)),600);num('sponsorbase',12000-600-200,11200);num('sponsorshare',ceilq(Fraction(11200*20,100)),2240);num('net',12000-600-200-2240,8960)
 num('operatingprofit',8960-2020,6940);num('profitdistribution',6940-2000,4940);num('eachdistribution',Fraction(4940,4),1235)
 num('firstinsurancepartial',max(0,Fraction(9,10)*40-20),16);num('insurancewhole',max(0,Fraction(9,10)*100-20),70);num('insuranceadditional',70-16,54)
 num('Cultinitreplay',-1+1,0);num('standingfirst',standing(2,[2]),3);num('standingoffsetsameScene',standing(2,[2,-2]),2)
 num('XP25percentgap1200',Fraction(1200*25,100),300);num('XP60percentcap',Fraction(1200*60,100),720)
 st=wk['integratedSequence']['numericSummary'];
 calc={'outboundMovingSeconds':28800,'outboundPauseSeconds':60,'arrivalSeconds':28800+60,'retrievalSeconds':1200,'retreatSeconds':12,'loadSeconds':60,'returnMovingSeconds':28800,'returnPauseSeconds':60,'exitPositionSeconds':28800+60+1200+12+60+28800+60,'verificationSeconds':60}
 calc['HavenEntrySeconds']=calc['exitPositionSeconds']+60;calc['HavenWorkSeconds']=(10+10+30+30+30+30+10+10+60)*60;calc['firstRestStart']=calc['HavenEntrySeconds']+calc['HavenWorkSeconds'];calc['firstRestEnd']=calc['firstRestStart']+28800;calc['restDebtDeadline']=40*3600;calc['nextDeparture']=48*3600
 calc.update(initialPreallocationCartPayloadLb=90+20+48+28+2,initialGrossDrawLb=200+188,grossSaleCp=12000,taxCp=600,mandatoryCp=200,sponsorCp=2240,netCp=8960,otherOperatingCostsCp=504+16+600+800+100,profitCp=6940,startingCapitalCp=3000,cashBeforeProfitDistributionCp=9940,nextReserveCp=2000,distributionCp=4940,perCharacterCp=1235,cashAfterDistributionCp=5000,nextProcurementCp=520,cashAtNextDepartureCp=4480,remainingEarmarkCp=1480,insurancePayoutCp=0,rosterCount=4)
 for k,v in calc.items():num('integrated:'+k,v,st[k])
 num('integrated:oil8pints',readq(st['mainLampOilPints'])+readq(st['backupLampOilPints']),8)
 num('integrated:secondRestnotbeneficial',st['nextDeparture']-st['firstRestEnd']<86400,True)
 # Small totality/invariant grids, NOT whole-procedure execution.
 sevrows=[]
 for pressure in range(7):
  for n in range(1,7):
   for mod in range(-2,3):
    for rr in (False,True):
     val=severity(pressure,n,mod,rr);sevrows.append({'pressure':pressure,'natural':n,'modifier':mod,'rerolled':rr,'severity':val})
     ck('severity reference totality',str((pressure,n,mod,rr)),val in {'none','Minor','Standard','Severe'} and (pressure!=0 or val=='none') and (pressure!=6 or val=='Severe'))
 for key,args,expected in [('untouched equality',(3,3,0,False),'Standard'),('modified equality',(3,4,-1,False),'Minor'),('rerolled equality',(3,3,0,True),'Minor'),('natural1trigger',(3,1,0,False),'Severe'),('modified1nontrigger',(3,1,3,False),'none')]:num('severity:'+key,severity(*args),expected)
 for L in [Fraction(1),Fraction(2),Fraction(5,2),Fraction(3),Fraction(6),Fraction(7),Fraction(20)]:
  for m in ['Mapped','Secured','Sketched','Unknown']:
   pts=checkpoints(m,L);ck('checkpoint reference',str((m,L)),pts==sorted(set(pts)) and pts[-1]==L and all(0<p<=L for p in pts))
 for opening in range(-3,4):
  for a in range(-2,3):
   for b in range(-2,3):
    ck('standing reference',str((opening,a,b)),standing(opening,[a,b])==standing(opening,[b,a]) and -3<=standing(opening,[a,b])<=3)
 # Raw roundtrip and deliberately bad state trials are reference guards, not an app migration.
 raw_cases=[b'{"war-veterans":0}',b'{}',b'{"x":null}',b'{"x":false}',b'{"x":"1.7"}',b'{"x":5}',b'{"unknown-key":2,"x":{"unknown":[null,false]}}',b'{"x":1,"x":2}']
 for raw in raw_cases:
  pairs=json.loads(raw,object_pairs_hook=lambda xs:xs);backing=bytes(raw)
  ck('raw preservation reference',raw.decode(),raw==backing and sha(raw)==sha(backing) and pairs is not None)
 for bad in [None,True,False,'2','1.7',1.7,5,-5,{},[]]:ck('deliberate invalidscore rejection',repr(bad),not valid_score(bad))
 result={'reviewId':'EX58-SOURCE-2026-10-11','scope':'Executed Python-standard-library archive/source/record equality and bounded reference arithmetic/totality only. No gameplay procedure runtime, JavaScript save migration, actor/world authentication or human balance.','checks':len(checks),'passed':sum(c['passed'] for c in checks),'failed':[c for c in checks if not c['passed']],'categoryCounts':dict(Counter(c['category'] for c in checks)),'sourcePayloads':304,'originalQuestions':58,'transportRows':29,'classArrays':17,'classCardRecordsParsed':1223,'referenceArithmeticTrials':len(refs),'severityReferenceTrials':len(sevrows),'details':checks,'referenceArithmetic':refs,'severityTable':sevrows,'realSavesRead':0,'realSavesWritten':0,'runtimeImplemented':False,'sourceFilesWritten':0,'newPromotions':0}
 return result

def main():
 p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--package',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--report',type=Path,default=None);a=p.parse_args();r=run(a.archive,a.package);dest=a.report or a.package/'EX58_EXECUTED_CHECKS.json';dest.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:r[k] for k in ['checks','passed','failed','categoryCounts','referenceArithmeticTrials','severityReferenceTrials']},indent=2));raise SystemExit(1 if r['failed'] else 0)
if __name__=='__main__':main()
