"""Navigation only: current preservation push and ten new unselected source records."""
from copy import deepcopy
from collections import Counter
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
 P=R/'data/director/spell_review';oldq=P/'remaining_work_queue_12.json';newq=P/'remaining_work_queue_13.json';oldcp=A/'ACTIVE_AUTHORING_CHECKPOINT_PLANAR_CONFERENCE_CONTEXT_17.json';cp=A/'ACTIVE_AUTHORING_CHECKPOINT_VITALITY_MATTER_SOURCE_18.json';delta=A/'VITALITY_MATTER_SOURCE_18_NAVIGATION_DELTA.json';report=A/'VITALITY_MATTER_SOURCE_18_CHECK.json';keep=A/'navigation-before-vitality-matter-source-18'
 assert not any(p.exists() for p in [newq,cp,delta,report,keep]);now=datetime.now(timezone.utc).isoformat();checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 q=deepcopy(read(oldq));previous=deepcopy(q);pp=A/'VITALITY_MATTER_10_SOURCE_CONFERENCE_01_PREPARATION.json';prep=read(pp);candidate=read(G/prep['candidate']['path']);ids=[r['spellId'] for r in candidate['records']]
 for k in ['candidate','archive','manifest','check','request']:ck('Exact preparation '+k,info(G/prep[k]['path'])==prep[k])
 group={'group':'vitality-matter10','phase':'source-conference-prepared-unsent','identities':ids,'identityCount':10,'candidate':prep['candidate'],'preparation':info(pp),'archive':prep['archive'],'adopted':False,'earlierCompleteProcedures':0,'newCurrentEncounters':0,'riskCounts':candidate['riskCounts']};q['groups'].append(group)
 for row in q['rows']:
  if row['id'] in ids:
   ck('Previously ungrouped '+row['id'],row['currentGroup'] is None);row['previousPhaseBeforeConference18']=row['currentPhase'];row.update(currentGroup='vitality-matter10',currentPhase=group['phase'],nextAction='Confer with actual GPT on ten full original spell sources and25 explicit decisions. Preserve printed benefits; Companion04 and the disease source audit remain qualified pending comparison evidence. No new rule from preparation.')
 q.update(id='REMAINING-WORK-QUEUE-13',recordedAtUtc=now,previousQueue=info(oldq),pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),preparedOrActualReviewIdentityCount=122,originalSourceOrReceiptWorkCount=201)
 q['sourceBindings'].extend([info(oldq),info(pp),prep['candidate'],prep['archive'],prep['check']])
 ck('All323 pending identities and order retained',[r['id'] for r in q['rows']]==[r['id'] for r in previous['rows']] and len(q['rows'])==323)
 ck('16 disjoint groups122 identities',len(q['groups'])==16 and sum(g['identityCount'] for g in q['groups'])==len({i for g in q['groups'] for i in g['identities']})==122)
 ck('201 ungrouped source identities',sum(r['currentGroup'] is None for r in q['rows'])==201)
 for before,after in zip(previous['rows'],q['rows']):ck('Source/access/member preserved '+before['id'],all(before[k]==after[k] for k in ['currentIndexEntryUnchanged','completeCurrentSourceAndAccess','previousAuthoringMapRowUnchanged','semanticAcceptanceClaimed']))
 for b in q['sourceBindings']:ck('Queue source '+b['path'],info(G/b['path'])==b)
 pushp=G/'docs/audit/2026-10-18/github-snapshot-persistent20/PUSH_RECEIPT.json';push=read(pushp);ck('Verified032bc7e preservation push',push['commit']==push['remoteMain']=='032bc7e33d941d7e635efa8b9a8b060f9f1742f8' and push['trackedEntriesDeleted']==0)
 start=G/'START_HERE.md';guide=R/'docs/DEVELOPMENT_DIRECTION.md';builder=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json';mapfile=G/'REVIEW_MAP.html';buildfile=A/'REVIEW_MAP_BUILD.json';raw={p:p.read_bytes() for p in [start,guide,builder,ledger,mapfile,buildfile]};edits={}
 added=' The [vitality/matter10 source conference](docs/audit/2026-10-08/full-game/VITALITY_MATTER_10_SOURCE_CONFERENCE_01_PREPARATION.json) preserves 73 sources, ten placements and25 explicit new decisions, with five individually justified tier B and five tier C spells. It has no earlier operational cases and adopts no rules. Its disease audit and Companion04 comparisons retain their pending scope.'
 pushpara='**GitHub preservation:** [Verified main `032bc7e`](docs/audit/2026-10-18/github-snapshot-persistent20/PUSH_RECEIPT.json) includes persistent20 and damage25 applications, registry06, companion Current04 actual submission, prepared source conferences and current acceptance context through checkpoint17. All24,186 expected blobs verified; all23,968 prior tracked entries retained, with0 deleted. Vitality/matter10 preparation and checkpoint18 are later local progress. All75 domain gates remain separate; this backup establishes no whole-game flow, runtime, human balance, cosmology or release approval.'
 for p in [start,guide]:
  t=raw[p].decode('utf8').replace(oldcp.name,cp.name).replace('[checkpoint17]','[checkpoint18]').replace('latest observation was 59% remaining','latest observation was 58% remaining');parts=t.split('\n\n')
  for prefix in ['**Remaining spell work:**','**GitHub preservation:**']:ck('Unique paragraph '+p.name+prefix,sum(x.startswith(prefix) for x in parts)==1)
  for n,x in enumerate(parts):
   if x.startswith('**Remaining spell work:**'):
    parts[n]=x.replace('Queue12','Queue13').replace('remaining_work_queue_12.json','remaining_work_queue_13.json').replace('112 in fifteen active/prepared groups and 211','122 in sixteen active/prepared groups and 201')+(added if p==start else added.replace('(docs/audit/','(../../../docs/audit/'))
   elif x.startswith('**GitHub preservation:**'):parts[n]=pushpara if p==start else pushpara.replace('(docs/audit/','(../../../docs/audit/')
  edits[p]='\n\n'.join(parts)
 cov=read(ledger);oldcov=deepcopy(cov);cov.setdefault('activeOrdinarySpellReviewHistory',[]).append(deepcopy(cov['activeOrdinarySpellReview']));cov['activeOrdinarySpellReview']['recordedAtUtc']=now
 code=raw[builder].decode('utf8');tail=' + read(A / "PLANAR_CONFERENCE_CONTEXT_17_NAVIGATION_DELTA.json")["changes"]\n';ck('Unique delta tail',code.count(tail)==1);code=code.replace(tail,tail.rstrip('\n')+' + read(A / "VITALITY_MATTER_SOURCE_18_NAVIGATION_DELTA.json")["changes"]\n')
 code=code.replace('    featured = [\n','    featured = [\n'+''.join('        '+repr(x)+',\n' for x in [('Current checkpoint18 — vitality/matter source decisions',cp.relative_to(G).as_posix()),('Current323 pending identities — queue13',newq.relative_to(G).as_posix())]),1).replace('Current checkpoint17 — travel source conference and exact review context','Checkpoint17 history — travel source conference and exact review context').replace('Current323 pending identities — queue12','Queue12 history — before vitality/matter preparation')
 code=code.replace('    pending = [\n','    pending = [\n        '+repr(('Vitality/matter10 —25 source decisions, fiveB/fiveC, UNSENT',pp.name))+',\n',1)
 scope='Video game only.525 reviewed/323 pending;249 standalone;173 scoped interfaces. Actual full Companion Current04 conference active. Queue13 has122 identities in16 groups and201 other original-source identities. Vitality/matter10 source conference preserves73 sources/ten placements/25 unselected questions,5B5C,UNSENT; no rules adopted. Other prepared reviews remain pending. Verified GitHub032bc7e covers checkpoint17, preserving all prior tracked entries. New vitality/matter work and checkpoint18 local. All75 domain gates unchanged. Latest allowance58percentremaining; continue until review complete or20percent remains.'
 nodes=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];ck('One status',len(nodes)==1);code=code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1);compile(code,str(builder),'exec')
 saved=[]
 for p,data in raw.items():
  dst=keep/p.relative_to(G);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data);saved.append({'source':info(p),'preservedCopy':info(dst)})
 (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved));newq.write_bytes(encoded(q));cov['activeOrdinarySpellReview']['currentQueue']=info(newq);ck('All75 full aspect rows unchanged',cov['aspects']==oldcov['aspects'] and len(cov['aspects'])==75);ledger.write_bytes(encoded(cov))
 for p,t in edits.items():p.write_text(t,encoding='utf8',newline='\n')
 builder.write_text(code,encoding='utf8',newline='\n');changes=[{'before':next({**s['source'],'preservedCopy':s['preservedCopy']['path']} for s in saved if s['source']['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,builder]]
 delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'newRuleAdoptionsByNavigation':0,'all75DomainGatesUnchanged':True,'sourceInformationDeleted':0}))
 checkpoint=deepcopy(read(oldcp));checkpoint.update(id='ACTIVE-AUTHORING-VITALITY-MATTER-SOURCE-18',recordedAtUtc=now,status=scope,previousCheckpoint=info(oldcp),currentWorkQueue=info(newq),remainingPreparedGroups=q['groups'],vitalityMatter10SourceConference=info(pp),latestVerifiedGitHubBackup={'commit':push['commit'],'receipt':info(pushp),'coverage':'Includes prior work through checkpoint17. All24,186 expected blobs verified and all23,968 prior tracked entries retained.'},laterLocalWork=['Vitality/matter10 full source conference,25 questions and73 sources','Queue13 and checkpoint18 navigation'],lastUsageObservation={'usedPercent':42,'remainingPercent':58,'windowMinutes':10080,'secondary':'unavailable'},nextAction='Preserve actual Companion Current04 final and reconcile its full decisions. Continue actual GPT conferences; full Control15/Illusion14 packets require their prepared current acceptance supplement. Vitality/matter10 and travel6 remain UNSENT. Continue until review complete or20percent allowance remains.',coverageLedger=info(ledger),navigationDelta=info(delta),preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'));cp.write_bytes(encoded(checkpoint))
 run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8');ck('Review map builds '+run.stderr[-1200:],run.returncode==0);build=read(buildfile);ck('No missing links',not build['missingLinks']);checkpoint['navigation']={'map':info(mapfile),'build':info(buildfile),'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[]};cp.write_bytes(encoded(checkpoint));report.write_bytes(encoded({'checkpoint':info(cp),'queue':info(newq),'checks':checks,'checkCount':len(checks),'failures':0,'links':build['existingDistinctLinks'],'all75DomainGatesUnchanged':True,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}));print(json.dumps({'checkpoint':info(cp),'queue':info(newq),'checks':len(checks),'links':build['existingDistinctLinks'],'failures':0}))

if __name__=='__main__':main()
