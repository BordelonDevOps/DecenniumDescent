"""Index three preserved source conferences and refresh owner navigation, no adoption."""
from copy import deepcopy
from collections import Counter
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
 P=R/'data/director/spell_review';oldq=P/'remaining_work_queue_09.json';newq=P/'remaining_work_queue_10.json'
 oldcp=A/'ACTIVE_AUTHORING_CHECKPOINT_DAMAGE25_APPLIED_PERSISTENT_ACTIVE_14.json';cp=A/'ACTIVE_AUTHORING_CHECKPOINT_SOURCE_CONFERENCES_15.json';delta=A/'SOURCE_CONFERENCES_15_NAVIGATION_DELTA.json';report=A/'SOURCE_CONFERENCES_15_CHECK.json';keep=A/'navigation-before-source-conferences-15'
 assert not any(p.exists() for p in [newq,cp,delta,report,keep]);now=datetime.now(timezone.utc).isoformat();checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 q=deepcopy(read(oldq));original=deepcopy(q)
 added=[]
 for group,slug,stem in [('information8','information_8','INFORMATION_8'),('eye-judgement1','eye_judgement_1','EYE_JUDGEMENT_1'),('evocation-rank7-8','evocation_rank7_8','EVOCATION_RANK7_8')]:
  pp=A/f'{stem}_CONFERENCE_01_PREPARATION.json';prep=read(pp);candidate=read(G/prep['candidate']['path']);ids=[r['spellId'] for r in candidate['records']]
  for key in ['candidate','archive','manifest','check','request']:ck('Prepared bytes '+group+' '+key,info(G/prep[key]['path'])==prep[key])
  phase='source-only-conference-prepared-unsent' if group=='evocation-rank7-8' else 'systemic-design-conference-prepared-unsent'
  g={'group':group,'phase':phase,'identities':ids,'identityCount':len(ids),'candidate':prep['candidate'],'preparation':info(pp),'archive':prep['archive'],'adopted':False,'earlierCompleteProcedures':0 if group=='evocation-rank7-8' else len(ids),'newCurrentEncounters':0}
  q['groups'].append(g);added.append(g)
  for row in q['rows']:
   if row['id'] not in ids:continue
   ck('Previously ungrouped '+row['id'],row['currentGroup'] is None)
   row['previousPhaseBeforeConference15']=row['currentPhase'];row.update(currentGroup=group,currentPhase=phase,nextAction='Send the full source conference to actual GPT, preserve its complete reply, then author source-qualified current cases and obtain exact acceptance. No acceptance inferred from preparation.')
  q['sourceBindings'].extend([info(pp),prep['candidate'],prep['archive'],prep['check']])
 q.update(id='REMAINING-WORK-QUEUE-10',recordedAtUtc=now,previousQueue=info(oldq),pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),preparedOrActualReviewIdentityCount=118,otherEarlierCompleteProposalCount=0,originalSourceOrReceiptWorkCount=225)
 q['sourceBindings'].append(info(oldq));ck('343 pending identities/order unchanged',[r['id'] for r in q['rows']]==[r['id'] for r in original['rows']] and len(q['rows'])==343)
 ck('15 disjoint groups /118 identities',len(q['groups'])==15 and sum(g['identityCount'] for g in q['groups'])==len({i for g in q['groups'] for i in g['identities']})==118)
 ck('224 source-only plus1 receipt left ungrouped',sum(r['currentGroup'] is None for r in q['rows'])==225 and q['pendingDistribution']['no-complete-procedure-found-in-current-proposal-directory']==224 and q['pendingDistribution']['receipt-only-pending']==1)
 ck('No ungrouped older full proposal',not any(r['currentPhase']=='earlier-complete-proposal-awaiting-current-reconciliation' for r in q['rows']))
 for before,after in zip(original['rows'],q['rows']):
  ck('Original source and membership preserved '+before['id'],all(before[k]==after[k] for k in ['currentIndexEntryUnchanged','completeCurrentSourceAndAccess','previousAuthoringMapRowUnchanged','semanticAcceptanceClaimed']))
 for b in q['sourceBindings']:ck('Current binding '+b['path'],info(G/b['path'])==b)
 newq.write_bytes(encoded(q))
 start=G/'START_HERE.md';guide=R/'docs/DEVELOPMENT_DIRECTION.md';builder=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json';mapfile=G/'REVIEW_MAP.html';buildfile=A/'REVIEW_MAP_BUILD.json'
 raw={p:p.read_bytes() for p in [start,guide,builder,ledger,mapfile,buildfile]};saved=[]
 for p,b in raw.items():
  dst=keep/p.relative_to(G);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b);saved.append({'source':info(p),'preservedCopy':info(dst)})
 (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
 newpara='''**Remaining spell work:** [Queue10](DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_10.json) retains 343 pending identities: 118 in fifteen active/prepared groups, with 224 other original-source identities and one receipt task. All nine remaining older full proposals now have prepared source conferences: [Information8](docs/audit/2026-10-08/full-game/INFORMATION_8_CONFERENCE_01_PREPARATION.json) and [Eye of Judgement](docs/audit/2026-10-08/full-game/EYE_JUDGEMENT_1_CONFERENCE_01_PREPARATION.json). A separate [rank-seven Evocation8 conference](docs/audit/2026-10-08/full-game/EVOCATION_RANK7_8_CONFERENCE_01_PREPARATION.json) preserves eight source-only records; it has no earlier complete procedures or worked cases. These three packets contain 47 explicit questions and remain UNSENT. [Registry05](DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_05.json) still has 143 exact scoped interfaces. Preparing questions does not approve spells or change the 505/343 membership count. Full companion Current04 is still the next case conference after the active persistent20 review.'''
 def update_text(s,guide_mode=False):
  prefix='../../../' if guide_mode else ''
  s=s.replace('ACTIVE_AUTHORING_CHECKPOINT_DAMAGE25_APPLIED_PERSISTENT_ACTIVE_14.json','ACTIVE_AUTHORING_CHECKPOINT_SOURCE_CONFERENCES_15.json').replace('[checkpoint14]','[checkpoint15]').replace('latest observation was 64% remaining','latest observation was 62% remaining')
  parts=s.split('\n\n');hits=[i for i,p in enumerate(parts) if p.startswith('**Remaining spell work:**')];ck('One remaining-work paragraph '+str(guide_mode),len(hits)==1)
  paragraph=newpara
  if guide_mode:paragraph=paragraph.replace('(docs/audit/','(../../../docs/audit/').replace('(DescentReviewChanges/ReviewBible/data/','(../data/')
  parts[hits[0]]=paragraph
  s='\n\n'.join(parts).replace('new damage25 final/application, persistent20 submission and checkpoint14 are later local progress','damage25 final/application, persistent20 submission, three additional source conferences and checkpoint15 are later local progress')
  return s
 start.write_text(update_text(raw[start].decode('utf8')),encoding='utf8',newline='\n');guide.write_text(update_text(raw[guide].decode('utf8'),True),encoding='utf8',newline='\n')
 cov=read(ledger);oldcov=deepcopy(cov);cov.setdefault('activeOrdinarySpellReviewHistory',[]).append(deepcopy(cov['activeOrdinarySpellReview']));cov['activeOrdinarySpellReview'].update(recordedAtUtc=now,currentQueue=info(newq));ck('All75 domain rows identical',cov['aspects']==oldcov['aspects'] and len(cov['aspects'])==75);ledger.write_bytes(encoded(cov))
 code=raw[builder].decode('utf8');tail=' + read(A / "DAMAGE25_APPLIED_PERSISTENT_ACTIVE_14_NAVIGATION_DELTA.json")["changes"]\n';ck('Unique prior delta tail',code.count(tail)==1);code=code.replace(tail,tail.rstrip('\n')+' + read(A / "SOURCE_CONFERENCES_15_NAVIGATION_DELTA.json")["changes"]\n')
 features=[('Current checkpoint15 — source conferences prepared',cp.relative_to(G).as_posix()),('Current343 pending identities — queue10',newq.relative_to(G).as_posix())]
 code=code.replace('    featured = [\n','    featured = [\n'+''.join('        '+repr(x)+',\n' for x in features),1).replace('Current checkpoint14 — damage25 applied, persistent20 active','Checkpoint14 history — damage25 applied, persistent20 active').replace('Current343 pending identities — queue09','Queue09 history — before three source conferences')
 pending=[('Information8 —18 source questions, unsent','INFORMATION_8_CONFERENCE_01_PREPARATION.json'),('Eye of Judgement —13 cross-class questions, unsent','EYE_JUDGEMENT_1_CONFERENCE_01_PREPARATION.json'),('Rank7 Evocation8 —16 source-only questions, unsent','EVOCATION_RANK7_8_CONFERENCE_01_PREPARATION.json')]
 code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in pending),1)
 scope='Video game only.505 reviewed/343 pending;229 standalone procedures;143 scoped interfaces. Damage25 exact10 accepted and applied. Persistent20 exact07 actual GPT review active. Companion Current04 full packet UNSENT,27 main cases,2 CR2 holds,5 questions. Queue10 has118 identities in15 groups and225 other source/receipt items. New Information8/Eye1/Evocation8 source conferences contain47 questions, all UNSENT, no new current encounters or adoption. All75 domain gates unchanged. GitHub19423ad covers throughcheckpoint13; checkpoint15 remains later local progress. Latest allowance62percentremaining; stopat20percent or completed review.'
 nodes=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];ck('Unique status field',len(nodes)==1);code=code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1);compile(code,str(builder),'exec');builder.write_text(code,encoding='utf8',newline='\n')
 changes=[{'before':next({**b['source'],'preservedCopy':b['preservedCopy']['path']} for b in saved if b['source']['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,builder,ledger]]
 delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'all75DomainGatesUnchanged':True,'newRuleAdoptionsByNavigation':0,'sourceInformationDeleted':0}))
 checkpoint=deepcopy(read(oldcp));checkpoint.update(id='ACTIVE-AUTHORING-SOURCE-CONFERENCES-15',recordedAtUtc=now,status=scope,previousCheckpoint=info(oldcp),currentWorkQueue=info(newq),remainingPreparedGroups=q['groups'],sourceConferencesPrepared15=added,lastUsageObservation={'usedPercent':38,'remainingPercent':62,'windowMinutes':10080,'secondary':'unavailable'},nextAction='Preserve actual persistent20 final and act on its verified exact result. Send full companion Current04 with current progress and five questions next. Then confer on prepared packets; do not mistake prepared source questions for approved procedures. Continue original source backlog while GPT reviews.',coverageLedger=info(ledger),navigationDelta=info(delta),preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'))
 checkpoint['laterLocalWork'].extend(['Information8/Eye1/Evocation8 source conferences prepared unsent','Queue10 and checkpoint15 navigation'])
 cp.write_bytes(encoded(checkpoint));run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8');ck('Review map builds',run.returncode==0);build=read(buildfile);ck('No missing links',not build['missingLinks']);checkpoint['navigation']={'map':info(mapfile),'build':info(buildfile),'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[]};cp.write_bytes(encoded(checkpoint))
 report.write_bytes(encoded({'checkpoint':info(cp),'queue':info(newq),'delta':info(delta),'checks':checks,'checkCount':len(checks),'failures':0,'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[],'all75DomainGatesUnchanged':True,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}));print(json.dumps({'checkpoint':info(cp),'queue':info(newq),'checkCount':len(checks),'links':build['existingDistinctLinks'],'failures':0}))

if __name__=='__main__':main()
