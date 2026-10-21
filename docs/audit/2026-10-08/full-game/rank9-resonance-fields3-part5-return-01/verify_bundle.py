#!/usr/bin/env python3
"""Read-only full-byte/source/pointer/mirror verification. No game/project imports."""
from pathlib import Path, PurePosixPath
import argparse, copy, hashlib, io, json, zipfile

ROOT=Path(__file__).resolve().parent
ORIG='DD_Rank9_Resonance_Fields_3_Source_Conference_01.zip'
CTX='DD_Rank9_Resonance_Fields3_Current_Context_80.zip'
EXPECTED={ORIG:(48727634,'9d92814a69f5ddbf8ec47a8d5dc6fd9d1f972e9e923bb7efff2e5d1468147e41'),CTX:(4857325,'7acaa6e544b29e9bbace3f16dc7ecbbd057ce1776877ad842e2daa890573f601')}
CHECKS=[]
def ck(group,label,condition):
 CHECKS.append({'category':group,'check':label,'passed':bool(condition)})
 if not condition: raise AssertionError(f'{group}: {label}')
def sh(b):return hashlib.sha256(b).hexdigest()
def read(n):return json.loads((ROOT/n).read_text(encoding='utf-8'))
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def canon(v):return sh(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def ptr(obj,path):
 for t in path.split('/')[1:]:obj=obj[int(t)] if isinstance(obj,list) else obj[t.replace('~1','/').replace('~0','~')]
 return obj
def change(obj,path,value=None,delete=False):
 parts=path.split('/')[1:];p=obj
 for t in parts[:-1]:p=p[int(t)] if isinstance(p,list) else p[t.replace('~1','/').replace('~0','~')]
 k=parts[-1].replace('~1','/').replace('~0','~')
 if isinstance(p,list):
  if delete:del p[int(k)]
  else:p[int(k)]=copy.deepcopy(value)
 elif delete:del p[k]
 else:p[k]=copy.deepcopy(value)
def safe(z):
 names=z.namelist()
 return len(names)==len(set(names)) and all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n and ':' not in PurePosixPath(n).parts[0] and ((i.external_attr>>16)&0o170000)!=0o120000 for n,i in zip(names,z.infolist()))

def run():
 archives={}
 for n,(size,digest) in EXPECTED.items():
  b=(ROOT/'input'/n).read_bytes();ck('input','exact archive '+n,len(b)==size and sh(b)==digest);z=zipfile.ZipFile(io.BytesIO(b));archives[n]=z
  ck('archive','safe and unique '+n,safe(z));ck('archive','CRC '+n,z.testzip() is None)
 z=archives[ORIG];cz=archives[CTX]
 ck('archive','original103 members',len(z.namelist())==103);ck('archive','context25 members',len(cz.namelist())==25)
 old_bytes=z.read('CANDIDATE.json');old=json.loads(old_bytes);model=read('MODEL.json')
 ck('input','original candidate exact',len(old_bytes)==687992 and sh(old_bytes)=='317cc5338ba34e22ee4ed7e22a5a497250e8cad5a6692945b879a8629a7b8262')
 ck('replay','original serializer equals all bytes',enc(old)==old_bytes)
 pending_member='sources/docs/audit/2026-10-08/full-game/DD_Rank9_Casting_Cost_5_Source_Conference_01.zip'
 pb=z.read(pending_member);pz=zipfile.ZipFile(io.BytesIO(pb));ck('archive','pending exact',len(pb)==43210762 and sh(pb)=='5db60cddf70e20656474e0aac2f126ce3dd3bc2d0ac18aa4ddcf6390702aafb1')
 ck('archive','pending safe/unique/CRC',safe(pz) and pz.testzip() is None and len(pz.namelist())==121)
 sets={'original':z,'context':cz,'pending-comparison':pz};rows=read('SOURCE_BINDING_VERIFICATION.json')
 for label,n in [('original',99),('context',23),('pending-comparison',117)]:ck('source','bound source count '+label,sum(x['set']==label for x in rows)==n)
 for r in rows:
  b=sets[r['set']].read('sources/'+r['path'])
  ck('source',r['set']+' bytes '+r['path'],len(b)==r['bytes']);ck('source',r['set']+' sha256 '+r['path'],sh(b)==r['sha256'])
 nested=[]
 for name in pz.namelist():
  if name.endswith('.zip'):
   zz=zipfile.ZipFile(io.BytesIO(pz.read(name)));ck('nested-history','safe/CRC '+name,safe(zz) and zz.testzip() is None);nested.append(name)
 ck('nested-history','five nested complete archives',len(nested)==5)
 psrc=json.loads(pz.read('CANDIDATE.json'));pcomparison=read('PENDING_COMPARISON_NOT_ADOPTED.json')
 ck('pending','32 complete questions remain exact/unselected',pcomparison['completeQuestionsUnselected']==psrc['questions'] and len(psrc['questions'])==32)
 ck('pending','five complete source records retained',pcomparison['originalIdentityRecords']==psrc['records'] and pcomparison['selectedProceduresFromThatCohort']==0)
 current=json.loads(cz.read('CURRENT_CONTEXT.json'))
 ck('context','complete actual current context unchanged',model['selectedCurrentContext']['fullContextUnchanged']==current)
 ck('context','applied baseline and fifty unchanged',model['reviewBoundary']['appliedReviewed']==525 and model['reviewBoundary']['appliedPending']==323 and model['reviewBoundary']['standalone']==249 and model['reviewBoundary']['scopedInterfaces']==173 and model['reviewBoundary']['acceptedButUnappliedBeforeThisReview']==50)
 aliases=read('SOURCE_REFERENCES.json')['aliases']
 for name,r in aliases.items():
  zz=archives[Path(r['archive']).name];b=zz.read(r['member']);ck('reference','exact full source alias '+name,len(b)==r['bytes'] and sh(b)==r['sha256'])
  if r.get('pointer'):ptr(json.loads(b),r['pointer']);ck('reference','resolvable source pointer '+name,True)
 # Original keyed material survives; selected arrays/metadata are the only declared changes.
 opfile=read('EXACT_OPERATIONS_FROM_SOURCE.json');ops=opfile['operations'];fwd=copy.deepcopy(old)
 ck('replay','operation count',len(ops)==opfile['operationCount']==21)
 for i,op in enumerate(ops):
  p=op['path']
  if op['before']['present']:
   v=ptr(old,p);ck('replay',f'op{i} exact before',ptr(fwd,p)==v and canon(v)==op['before']['valueSha256'])
  else:
   try:ptr(fwd,p);exists=True
   except KeyError:exists=False
   ck('replay',f'op{i} truly absent before',not exists)
  v=ptr(model,p);ck('replay',f'op{i} complete after binding',canon(v)==op['after']['valueSha256']);change(fwd,p,v)
 mb=(ROOT/'MODEL.json').read_bytes();ck('replay','entire forward byte equality',enc(fwd)==mb)
 rev=copy.deepcopy(model)
 for i,op in reversed(list(enumerate(ops))):
  ck('replay',f'op{i} exact inverse input',canon(ptr(rev,op['path']))==op['after']['valueSha256'])
  if op['before']['present']:change(rev,op['path'],ptr(old,op['path']))
  else:change(rev,op['path'],delete=True)
 ck('replay','entire reverse original byte equality',enc(rev)==old_bytes)
 ck('binding','complete successor binding',opfile['successor']['bytes']==len(mb) and opfile['successor']['sha256']==sh(mb))
 for key in old:
  if key not in ['id','recordedAtUtc','status','records','currentVectors','newRuleAdoptions']:ck('preservation','unchanged original root '+key,old[key]==model[key])
 for i,r in enumerate(old['records']):
  for k in r:ck('preservation',f'complete original record{i}/{k}',r[k]==model['records'][i][k])
  source=r['completeCurrentCatalogSourceAndAccess'];ck('access','tierC '+r['spellId'],r['riskTier']=='C')
  for cl,a in source['classAccess'].items():ck('access',r['spellId']+'/'+cl,a['rank']==9 and a['minimumClassLevel']==17 and a['baseRpCost']==26)
 ck('access','native access count8',sum(len(r['completeCurrentCatalogSourceAndAccess']['classAccess']) for r in old['records'])==8)
 procs=read('PROCEDURES.json')['procedures'];shared=read('SHARED_RULES.json')['rules'];questions=read('QUESTION_DISPOSITIONS.json')['questions'];cases=read('CASE_DISPOSITIONS.json')['cases'];disps=read('SPELL_DISPOSITIONS.json')['dispositions']
 ck('mirrors','full case array',cases==model['currentVectors']);ck('mirrors','full questions',questions==model['selectedQuestionDispositions']);ck('mirrors','full shared clauses',shared==model['selectedSharedRules'])
 for i,p in enumerate(procs):
  ck('mirrors','full procedure '+p['id'],p['procedure']==model['records'][i]['procedure']==disps[i]['completeSelectedProcedure'])
  ck('mirrors','full original source envelope '+p['id'],disps[i]['completeNativeSourceAndAccessUnchanged']==old['records'][i]['completeCurrentCatalogSourceAndAccess'])
  ck('mirrors','shared routing '+p['id'],p['sharedRuleIds']==model['records'][i]['sharedRuleIds'] and disps[i]['applicableFullSharedRules']==[s for s in shared if s['id'] in p['sharedRuleIds']])
 for i,q in enumerate(questions):ck('preservation',q['id']+' full original question',q['originalQuestionUnchanged']==old['questions'][i] and old['questions'][i]['decisionSelected'] is False)
 for name in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:
  txt=(ROOT/name).read_text()
  for p in procs:ck('render',name+' full procedure '+p['id'],p['procedure'] in txt)
  for s in shared:ck('render',name+' full shared '+s['id'],s['text'] in txt)
 ck('render','Director full exact casebook JSON',json.dumps(read('CASE_DISPOSITIONS.json'),ensure_ascii=False,indent=2) in (ROOT/'DIRECTOR_REVIEW.md').read_text())
 ck('render','Director complete decision prose',(ROOT/'DECISIONS.md').read_text() in (ROOT/'DIRECTOR_REVIEW.md').read_text())
 templates={t['id']:t for t in read('ACTOR_TEMPLATES.json')['templates']};ck('mirrors','all complete actor templates',list(templates.values())==model['actorTemplates']==read('ACTOR_FEATURE_ACCOUNTING.json')['templates'])
 catalog=json.loads(z.read(aliases['catalog']['member']))['spells'];catalog={r['id']:r for r in catalog}
 for tid,t in templates.items():
  native=json.loads(z.read(aliases[t['class'].lower()]['member']));selected=[]
  ck('actor',tid+' HP/stat math',t['maxHP']==6+16*4+17*2==104 and t['PB']==6 and t['S']==4 and t['M']==4 and t['dissonanceLimit']==12)
  ck('actor',tid+' actual RP row',t['maxRP']==native['rpByClassLevel'][16])
  for h in t['selectedClassHistory']:
   lv=h['classLevel'];row=next(r for r in native['schedule'] if r['classLevel']==lv);cards=[native['cards'][c['cardIndex']] for c in h['selectedCards']]
   expected=row['choose']-(1 if t['class']=='Wizard' and t['heroPath']=='Elementalist' and lv==10 else 0)
   ck('acquisition',tid+f' level{lv} selection',len(cards)==expected and all(c['minimumClassLevel']<=lv and c['acquisition']=='selection' and c['path'] in [None,t['heroPath']] and c['band'] in row['bands'] for c in cards))
   selected.extend(c['id'] for c in cards)
  ck('acquisition',tid+' no duplicate selections',len(selected)==len(set(selected)))
  if t['class']=='Wizard':
   known=[]
   for h in t['ordinaryAcquisitionHistory']:
    ids=h['chosenSpellIds'];lv=h['classLevel'];ck('acquisition',tid+f' full book level{lv}',len(ids)==h['levelUpAllowance'] and all(catalog[x]['classAccess']['Wizard']['minimumClassLevel']<=lv and x not in known for x in ids));known+=ids
    if 'schoolBonusSpell' in h:known.append(h['schoolBonusSpell'])
   ck('acquisition',tid+' complete book and prepared',known==t['ordinaryBook'] and len(known)==67 and set(t['preparedOrdinary'])<=set(known) and len(t['preparedOrdinary'])<=t['preparedLimit'])
   ck('acquisition',tid+' separate five real cantrips',len(t['knownCantrips'])==5 and all(catalog[x]['classAccess']['Wizard']['rank']==0 for x in t['knownCantrips']))
 # Full fixture states: numeric bounds, direct new cast action debits, immutable origin/credit identity.
 allcases=[x for c in cases for x in [c]+c['independentBranches']]
 ck('case','7 mains28 branches',len(cases)==7 and len(allcases)==35)
 ck('case','4 disclosed conditional branches',sum(c['disposition']=='CONDITIONAL_EXTERNAL_PREMISE' for c in allcases)==4)
 for c in allcases:
  ck('case',c['id']+' complete final',bool(c['timeline']) and c['timeline'][-1]['after']==c['finalState'])
  for j,e in enumerate(c['timeline']):
   b,a=e['before'],e['after'];ck('state',c['id']+f'/{j} time',b['time']==a['time']==e['time'])
   ck('state',c['id']+f'/{j} complete actor bounds',all(0<=x['rp']<=x['maxRP'] and 0<x['hp']<=x['maxHP'] and 0<=x['D'] and x['movementSpent']<=30 for x in a['actors'].values()))
   for cid,r in a['castRecords'].items():
    if cid not in b['castRecords']:
     owner=r['owner'];before=b['actors'][owner];after=a['actors'][owner]
     # Any new genuine commitment has spent exactly its real declared Action/Reaction/BA; callbacks never create a fresh budget.
     ck('action',c['id']+f'/{j}/{cid} one actual budget',sum(bool(before[k]) and not bool(after[k]) for k in ['action','bonusAvailable','reaction'])==1)
     ck('cost',c['id']+f'/{j}/{cid} bounded price',r['quote']['total']==sum(r['quote'][k] for k in ['base','extra','dampening','burden','protectedPrincipal']))
     feedback=1 if r['name']=='wizard.base.counterspell' and r['state']=='resolved' and any(x.get('ArcaneFeedback')==1 or x.get('actualArcaneFeedback')==1 for x in a['observations'][len(b['observations']):]) else 0
     ck('cost',c['id']+f'/{j}/{cid} actual RP transition',before['rp']-after['rp']==r['quote']['total']-feedback)
     ck('action',c['id']+f'/{j}/{cid} declared real budget',before[r['actualBudgetSpent']] is True and after[r['actualBudgetSpent']] is False)
   for rid,r in a['conversionReceipts'].items():
    if r['state']=='spent-before-credit':ck('conversion',c['id']+f'/{j}/{rid} settled finite once',r['credited']+r['overflowOrDenied']==r['nominalConversion'] and r['credited']>=0)
   for rid,r in a['damageRootRecords'].items():
    ck('provenance',c['id']+f'/{j}/{rid} actual dealer',r['dealer']==a['castRecords'][r['generatingCast']]['owner'] and r['fieldModifiersDoNotChangeDealer'] is True)
 native_refs={r['nativeSourceRef'] for c in allcases for e in c['timeline'] for r in e['after']['castRecords'].values()}
 for ref in sorted(native_refs):
  alias,p=ref.split('#',1)
  if alias=='MODEL':obj=model;path=p
  else:
   binding=aliases[alias];obj=json.loads(archives[Path(binding['archive']).name].read(binding['member']));path=binding.get('pointer','')+p
  ptr(obj,path);ck('reference','actual cast full pointer '+ref,True)
 # Does not rerun historical project scripts. Delivered report claims and binding themselves are checked as data.
 ab=read('ARTIFACT_BINDINGS.json')
 for r in ab['artifacts']:
  b=(ROOT/r['path']).read_bytes();ck('artifact','binding '+r['path'],len(b)==r['bytes'] and sh(b)==r['sha256'])
 if (ROOT/'MANIFEST.json').exists():
  manifest=read('MANIFEST.json');actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
  ck('manifest','no missing or surplus return files',actual=={r['path'] for r in manifest['files']})
  for r in manifest['files']:
   b=(ROOT/r['path']).read_bytes();ck('manifest','exact '+r['path'],len(b)==r['bytes'] and sh(b)==r['sha256'])
 categories={k:sum(c['category']==k for c in CHECKS) for k in sorted({c['category'] for c in CHECKS})}
 return {'scope':'read-only input/source/full-value reconstruction/mirror/fixture structure; not semantic proof, engine execution or balance','checkCount':len(CHECKS),'failures':sum(not c['passed'] for c in CHECKS),'categories':categories,'checks':CHECKS}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path);args=ap.parse_args();r=run()
 if args.report:
  p=args.report.resolve();p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(enc(r))
 print(json.dumps({k:v for k,v in r.items() if k!='checks'},indent=2))
