#!/usr/bin/env python3
"""Read-only source/structure/full-value reconstruction checks; never imports project code."""
from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,copy,ast,argparse
ROOT=Path(__file__).resolve().parent

def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
def get(x,p):
 for k in p.strip('/').split('/') if p else []:
  k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
 return x

def apply(x,op,reverse=False):
 parts=op['pointer'].strip('/').split('/');parent=x
 for k in parts[:-1]:parent=parent[int(k)] if isinstance(parent,list) else parent[k.replace('~1','/').replace('~0','~')]
 key=parts[-1].replace('~1','/').replace('~0','~');key=int(key) if isinstance(parent,list) else key
 expected=op['after'] if reverse else op['before'];exists=op['afterExists'] if reverse else op['beforeExists']
 present=0<=key<len(parent) if isinstance(parent,list) else key in parent
 if present!=exists or (exists and parent[key]!=expected):raise ValueError('Complete value or presence mismatch: '+op['pointer'])
 output_exists=op['beforeExists'] if reverse else op['afterExists'];value=op['before'] if reverse else op['after']
 if output_exists:parent[key]=copy.deepcopy(value)
 else:del parent[key]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path);ap.add_argument('--manifest',action='store_true');a=ap.parse_args();checks=[]
 def check(label,ok,category='source/structure'):
  checks.append({'id':label,'category':category,'pass':bool(ok)})
  if not ok:raise AssertionError(label)
 raw=(ROOT/'inputs/DD_Rank7_Identity_Casting_5_Source_Conference_01.zip').read_bytes()
 check('original ZIP exact bytes',len(raw)==4534073);check('original ZIP SHA256',sha(raw)=='fad1e1d4b5146782305d94f62194f8856300dde461a2aec4ef1b5b37e61490ec')
 with zipfile.ZipFile(ROOT/'inputs/DD_Rank7_Identity_Casting_5_Source_Conference_01.zip') as z:
  names=z.namelist();check('72 members',len(names)==72);check('unique safe names',len(set(names))==len(names) and all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n and ':' not in n for n in names));check('ZIP CRC',z.testzip() is None)
  braw=(ROOT/'baseline/CANDIDATE.json').read_bytes();check('candidate is original ZIP bytes',braw==z.read('CANDIDATE.json'));check('candidate exact bytes/hash',len(braw)==829217 and sha(braw)=='bdfba569485e0100dadda7ef41b36eb54d810bc2966b547c680836ac1c236766')
  base=json.loads(braw);check('68 bindings',len(base['sourceBindings'])==68);source={};sjson={}
  for sb in base['sourceBindings']:
   p=sb['path'];data=z.read('sources/'+p);source[p]=data;check('bound source '+p,len(data)==sb['bytes'] and sha(data)==sb['sha256'])
   text=data.decode('utf-16') if data.startswith((b'\xff\xfe',b'\xfe\xff')) else data.decode('utf-8-sig');check('readable complete text '+p,bool(text))
   if p.endswith('.json'):sjson[p]=json.loads(text);check('parse JSON '+p,True)
   if p.endswith('.py'):ast.parse(text);check('parse only Python '+p,True)
  contexts=json.loads((ROOT/'CONTEXT_BINDINGS.json').read_bytes());check('10 later complete contexts',len(contexts)==10)
  for r in contexts:
   d=(ROOT/r['path']).read_bytes();check('later context binding '+r['path'],len(d)==r['bytes'] and sha(d)==r['sha256']);json.loads(d)
  c13=json.loads((ROOT/'context/CONTROL13_MODEL.json').read_bytes());c14=json.loads((ROOT/'context/CONTROL14_MODEL.json').read_bytes());check('Control procedures unchanged13to14',c13['spells']==c14['spells']);check('Control current cases unchanged13to14',c13['currentExamples']==c14['currentExamples'])
  modelraw=(ROOT/'MODEL.json').read_bytes();m=json.loads(modelraw);plan=json.loads((ROOT/'EXACT_OPERATIONS_FROM_SOURCE.json').read_bytes())
  check('successor exact binding',len(modelraw)==plan['successor']['bytes'] and sha(modelraw)==plan['successor']['sha256']);check('stable full original serialization',enc(base)==braw);check('successor stable serialization',enc(m)==modelraw)
  f=copy.deepcopy(base)
  for op in plan['operations']:apply(f,op);check('full forward '+op['pointer'],True,'full-value replay')
  check('complete forward bytes equal MODEL',enc(f)==modelraw,'full-value replay')
  for op in reversed(plan['operations']):apply(f,op,True);check('full reverse '+op['pointer'],True,'full-value replay')
  check('complete reverse bytes equal original',enc(f)==braw,'full-value replay')
  check('operation count',len(plan['operations'])==plan['operationCount']==27)
  allowed={'id','recordedAtUtc','status','records','currentVectors'}
  for k,v in base.items():
   if k not in allowed:check('original root unchanged '+k,m[k]==v,'preservation')
  check('original rank7 prior operational cases empty',base['earlierOperationalWorkedCases']==[])
  cat=sjson['DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'];catidx={v['id']:i for i,v in enumerate(cat['spells'])};core=sjson['DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json'];js=source['DescentReviewChanges/ReviewBible/src/data/spells.js'].decode();dec=json.JSONDecoder();naccess=0;nplacements=0
  for i,r in enumerate(base['records']):
   cur=m['records'][i]
   for k,v in r.items():check('native/history unchanged '+r['spellId']+'/'+k,cur[k]==v,'preservation')
   native=r['completeCurrentCatalogSourceAndAccess'];check('whole actual catalog object '+r['spellId'],native==cat['spells'][catidx[r['spellId']]])
   marker=json.dumps(r['spellId'])+':';start=js.index('{',js.index(marker));obj,_=dec.raw_decode(js[start:]);check('full native JavaScript object '+r['spellId'],obj==native['source']['original'])
   for row in native['source']['coreEntries']:check('full Core row '+r['spellId']+'/'+str(row['index']),core['spells'][row['index']]==row['original']);nplacements+=1
   for cls,ac in native['classAccess'].items():
    naccess+=1;orig=native['source']['original'];check('actual access '+r['spellId']+'/'+cls,ac['rank']==orig['classRanks'][cls]==7 and ac['minimumClassLevel']==orig['classLearnLevels'][cls] and ac['school']==orig['classSchools'][cls] and ac['baseRpCost']==17)
   check('individual C retained '+r['spellId'],r['riskTier']==cur['riskTier']=='C')
   check('full procedure rendered player '+r['spellId'],cur['proposedProcedure'] in (ROOT/'PLAYER_CHAPTER.md').read_text())
   check('full procedure rendered director '+r['spellId'],cur['proposedProcedure'] in (ROOT/'DIRECTOR_REVIEW.md').read_text())
  check('25 access rows six placements',naccess==25 and nplacements==6)
  for k,comp in enumerate(base['completeAcceptedCounterparts']):check('complete actual counterpart '+comp['spellId'],get(sjson[comp['source']['path']],comp['pointer'])==comp['completeCurrentCard'])
  reg=sjson['DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json']
  for comp in base['currentAcceptedInterfaceComparisons']:check('actual registry comparison '+comp['registryPointer'],get(reg,comp['registryPointer'])==comp['completeEntryUnchanged'])
  for q,new in zip(base['questions'],m['selectedQuestionDispositions']):check('question exact plus disposition '+q['id'],new['completeOriginalQuestionUnchanged']==q and bool(new['selectedAnswer']))
  check('24 questions',len(m['selectedQuestionDispositions'])==24)
  for r in m['selectedSharedRules']:
   check('shared text player '+r['id'],r['wording'] in (ROOT/'PLAYER_CHAPTER.md').read_text());check('shared text director '+r['id'],r['wording'] in (ROOT/'DIRECTOR_REVIEW.md').read_text())
  prof=json.loads((ROOT/'ACTOR_FEATURE_ACCOUNTING.json').read_bytes())['profiles']
  for pid,p in prof.items():
   d=sjson[p['source']['path']];cards={x['id']:x for x in d['cards']};schedule={x['classLevel']:x for x in d['schedule']};seen=set()
   for row in p['selectedAcquisition']:
    lv=row['classLevel'];sc=schedule[lv];check('selection count '+pid+'/'+str(lv),len(row['cards'])==sc['choose'])
    active=0
    for card in row['cards']:
     check('full card source '+pid+'/'+card['id'],card==cards[card['id']]);check('card unique level gate '+pid+'/'+card['id'],card['id'] not in seen and card['minimumClassLevel']<=lv and card['acquisition']=='selection' and card['band'] in sc['bands']);seen.add(card['id']);active+=card['sourceKind']=='active'
     if card.get('path') and card['band']=='Hero':check('actual hero path '+pid+'/'+card['id'],card['path']==p.get('hero','Archmage'))
    check('minimum active choices '+pid+'/'+str(lv),active>=sc['minimumActives'])
   for card in p['automaticCards']:check('full automatic card '+pid+'/'+card['id'],card==cards[card['id']] and card['acquisition']=='automatic' and card['minimumClassLevel']<=13)
   check('RP max actual13 '+pid,d['rpByClassLevel'][12]==p['maxRp'])
  check('no Elementalist automatic on Spellbinder',all(x.get('path') in (None,'Spellbinder') for x in prof['W13I']['automaticCards']))
  check('five actual cantrips no matrix occupation',len(prof['W13I']['bookAndPreparation']['ordinaryKnownCantrips'])==5 and prof['W13I']['bookAndPreparation']['count']==12)
  check('five actual rank7 Wizard additions',len(prof['W13I']['bookAndPreparation']['newRank7BookAdditionsAt13'])==5)
  check('one actual Mage rank7 addition',sum(cat['spells'][catidx[x]]['classAccess']['Mage']['rank']==7 for x in prof['M13L']['ordinaryKnown'])==1)
  check('Wizard ability/school/DC accounting',(prof['W13I']['PB'],prof['W13I']['spellDc'],prof['W13I']['schoolDc'],prof['W13I']['maxRp'])==(5,17,19,48))
  cases=json.loads((ROOT/'CASE_DISPOSITIONS.json').read_bytes());check('whole case arrays equal MODEL',cases['cases']==m['currentVectors']);check('10 main cases',len(cases['cases'])==10);check('two main cases each',all(sum(x['spellId']==r['spellId'] for x in cases['cases'])==2 for r in m['records']))
  count=0;cond=0;ids=set()
  for ca in cases['cases']:
   for bb in [ca]+ca['independentBranches']:
    check('unique full case '+bb['id'],bb['id'] not in ids and bool(bb['initialState']) and bool(bb['timeline']) and bool(bb['expectedFinalState']) and bool(bb['actorDefinitions']) and bool(bb['sourceRefs']));ids.add(bb['id'])
    check('case final state '+bb['id'],bb['timeline'][-1]['after']==bb['expectedFinalState'])
    check('case timeline order '+bb['id'],[e['timeSeconds'] for e in bb['timeline']]==sorted(e['timeSeconds'] for e in bb['timeline']))
    for e in bb['timeline']:check('complete event '+bb['id']+'/'+str(e['timeSeconds']),bool(e['before']) and bool(e['after']) and 'rng' in e and 'sourceRefs' in e)
    check('actor source profile completeness '+bb['id'],set(bb['initialState']['actors'])==set(bb['actorDefinitions']))
    if bb is not ca:count+=1;cond+=bb['disposition'].startswith('CONDITIONAL')
  check('39 branches,11 conditional',count==39 and cond==11)
  # Every machine source pointer used in dispositions resolves in exact original or exact context bytes.
  cache={**sjson};refcount=0
  def scan(x):
   nonlocal refcount
   if isinstance(x,dict):
    if 'pointer' in x:
     ptr=x['pointer'];path=None;obj=None
     if x.get('member','').startswith('sources/'):
      path=x['member'][8:];data=source[path];check('reference hash '+str(refcount),len(data)==x['bytes'] and sha(data)==x['sha256']);obj=cache.get(path)
     elif x.get('path','').startswith('context/'):
      path=x['path'];data=(ROOT/path).read_bytes();check('context reference hash '+str(refcount),len(data)==x['bytes'] and sha(data)==x['sha256']);obj=json.loads(data)
     elif x.get('path')=='MODEL.json':obj=m
     if obj is not None and ptr.startswith('/'):
      get(obj,ptr);check('reference pointer '+str(refcount),True)
     refcount+=1
    for v in x.values():scan(v)
   elif isinstance(x,list):
    for v in x:scan(v)
  for fn in ['SOURCE_REFERENCES.json','QUESTION_DISPOSITIONS.json','SPELL_DISPOSITIONS.json']:
   scan(json.loads((ROOT/fn).read_bytes()))
  di=json.loads((ROOT/'DI7_COMPARISON.json').read_bytes());dpaths=di['sourceRefs'];dg=json.loads(source[dpaths['director']['member'][8:]]);check('14 full original DI7 narratives',di['all14OriginalExampleDispositionsUnchanged']==dg['originalExampleDispositions'] and len(di['all14OriginalExampleDispositionsUnchanged'])==14)
  for field,k in [('completeExpectationsUnchanged','expectations'),('complete93CaseDispositionsUnchanged','cases'),('completeEvidenceScopeAddendumUnchanged','scope')]:check('DI7 full preserved '+field,di[field]==json.loads(source[dpaths[k]['member'][8:]]))
  check('DI7 actual total93 not runtime',di['complete93CaseDispositionsUnchanged']['totalCases']==93 and di['complete93CaseDispositionsUnchanged']['all93AreFullSpellRuntimeTests'] is False)
  hold=json.loads((ROOT/'HOLD_REGISTER.json').read_bytes());check('five external whole-case holds',set(['IN6-09-A','IN6-09-B','EN5-01-A','EN5-01-B','EN6-03-B']).issubset({h['id'] for h in hold['holds']}));check('project-adoption/runtime flags stay false',m['newRuleAdoptions']==0 and m['runtimeTestsExecuted']==0 and m['wholeGameComplete'] is False)
  spec=json.loads((ROOT/'SPECIFICATION_REPORT.json').read_bytes());check('isolated specification report passes',spec['failures']==spec['errors']==0 and spec['projectRuntimeTests']==0)
 if a.manifest:
  mf=json.loads((ROOT/'MANIFEST.json').read_bytes())
  for item in mf['files']:
   b=(ROOT/item['path']).read_bytes();check('manifest '+item['path'],len(b)==item['bytes'] and sha(b)==item['sha256'],'return-manifest')
 report={'id':'RIC5-PART5-READONLY-VERIFICATION-01','scope':'Source bytes, exact full-value forward/reverse reconstruction, native access, acquisition gates, complete authoring records and preservation. No downloaded preparation script or actual project/game module executed. Semantic judgments are the separately labelled review, not inferred from hash counts.','checkCount':len(checks),'failures':sum(not x['pass'] for x in checks),'runtimeTestsExecuted':0,'checks':checks}
 if a.report:a.report.write_bytes(enc(report))
 print(json.dumps({'checks':len(checks),'failures':report['failures'],'manifestIncluded':a.manifest}));return 0
if __name__=='__main__':raise SystemExit(main())
