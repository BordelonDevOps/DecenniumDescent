"""Navigation only: current preservation push and fourteen new unselected rank-seven source records."""
from copy import deepcopy
from collections import Counter
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
 P=R/'data/director/spell_review';oldq=P/'remaining_work_queue_14.json';newq=P/'remaining_work_queue_15.json';oldcp=A/'ACTIVE_AUTHORING_CHECKPOINT_COMPANION_EXACT_ILLUSION_ACTIVE_19.json';cp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_WARDS_MANIFESTATIONS_20.json';delta=A/'RANK7_WARDS_MANIFESTATIONS_20_NAVIGATION_DELTA.json';report=A/'RANK7_WARDS_MANIFESTATIONS_20_CHECK.json';keep=A/'navigation-before-rank7-wards-manifestations-20'
 assert not any(p.exists() for p in [newq,cp,delta,report,keep]);now=datetime.now(timezone.utc).isoformat();checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 q=deepcopy(read(oldq));previous=deepcopy(q);prepared=[]
 for groupid,prefix in [('ward7','WARD_7'),('manifestation7','MANIFESTATION_7')]:
  pp=A/(prefix+'_SOURCE_CONFERENCE_01_PREPARATION.json');prep=read(pp);candidate=read(G/prep['candidate']['path']);ids=[r['spellId'] for r in candidate['records']]
  for k in ['candidate','archive','manifest','check','request']:ck('Exact preparation '+groupid+k,info(G/prep[k]['path'])==prep[k])
  group={'group':groupid,'phase':'source-conference-prepared-unsent','identities':ids,'identityCount':7,'candidate':prep['candidate'],'preparation':info(pp),'archive':prep['archive'],'adopted':False,'earlierCompleteProcedures':0,'newCurrentEncounters':0,'riskCounts':candidate['riskCounts']};q['groups'].append(group);prepared.append(info(pp))
  for row in q['rows']:
   if row['id'] in ids:
    ck('Previously ungrouped '+row['id'],row['currentGroup'] is None);row['previousPhaseBeforeConference20']=row['currentPhase'];row.update(currentGroup=groupid,currentPhase=group['phase'],nextAction='Confer with actual GPT on the complete source packet and all explicit finite decisions. Preserve printed benefits, source access and exact accepted boundaries; preparation is not adoption.')
  q['sourceBindings'].extend([info(pp),prep['candidate'],prep['archive'],prep['check']])
 q.update(id='REMAINING-WORK-QUEUE-15',recordedAtUtc=now,previousQueue=info(oldq),pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),preparedOrActualReviewIdentityCount=136,originalSourceOrReceiptWorkCount=187)
 q['sourceBindings'].append(info(oldq))
 ck('All323 pending identities and order retained',[r['id'] for r in q['rows']]==[r['id'] for r in previous['rows']] and len(q['rows'])==323)
 ck('18 disjoint groups136 identities',len(q['groups'])==18 and sum(g['identityCount'] for g in q['groups'])==len({i for g in q['groups'] for i in g['identities']})==136)
 ck('187 ungrouped source identities',sum(r['currentGroup'] is None for r in q['rows'])==187)
 for before,after in zip(previous['rows'],q['rows']):ck('Source/access/member preserved '+before['id'],all(before[k]==after[k] for k in ['currentIndexEntryUnchanged','completeCurrentSourceAndAccess','previousAuthoringMapRowUnchanged','semanticAcceptanceClaimed']))
 for b in q['sourceBindings']:ck('Queue source '+b['path'],info(G/b['path'])==b)
 pushp=G/'docs/audit/2026-10-18/github-snapshot-companion-illusion/PUSH_RECEIPT.json';push=read(pushp);ck('Verifiedc9c99f1 preservation push',push['commit']==push['remoteMain']=='c9c99f1e477b073efdde469d25fb348fcff72c89' and push['trackedEntriesDeleted']==0)
 start=G/'START_HERE.md';guide=R/'docs/DEVELOPMENT_DIRECTION.md';builder=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json';mapfile=G/'REVIEW_MAP.html';buildfile=A/'REVIEW_MAP_BUILD.json';raw={p:p.read_bytes() for p in [start,guide,builder,ledger,mapfile,buildfile]};edits={}
 added=' Two further rank-seven packets remain UNSENT: [ward7](docs/audit/2026-10-08/full-game/WARD_7_SOURCE_CONFERENCE_01_PREPARATION.json) preserves seven identities/eight placements,20 questions and50 sources; [manifestation7](docs/audit/2026-10-08/full-game/MANIFESTATION_7_SOURCE_CONFERENCE_01_PREPARATION.json) preserves seven identities/seven placements,23 questions and60 sources. Each has three individually assessed B and four C spells. No earlier complete procedures or current cases are claimed. Pending travel and Companion05 retain comparison-only scope.'
 pushpara='**GitHub preservation:** [Verified main `c9c99f1`](docs/audit/2026-10-18/github-snapshot-companion-illusion/PUSH_RECEIPT.json) includes all progress through checkpoint19: actual Companion04 return, Current05 replay and exact05 preparation, actual Illusion12 submission/current context, Vitality/matter10 and the bounded CR2 source search. All24,340 expected blobs verified; all24,265 prior tracked entries retained,0deleted. Ward7/manifestation7 preparations and checkpoint20 are later local work. All75 domain gates remain separate; this backup establishes no whole-game/runtime/human/balance/cosmology or release approval.'
 for p in [start,guide]:
  t=raw[p].decode('utf8').replace(oldcp.name,cp.name).replace('[checkpoint19]','[checkpoint20]').replace('latest observation was 55% remaining','latest observation was 54% remaining');parts=t.split('\n\n')
  for prefix in ['**Remaining spell work:**','**GitHub preservation:**']:ck('Unique paragraph '+p.name+prefix,sum(x.startswith(prefix) for x in parts)==1)
  for n,x in enumerate(parts):
   if x.startswith('**Remaining spell work:**'):
    parts[n]=x.replace('Queue14','Queue15').replace('remaining_work_queue_14.json','remaining_work_queue_15.json').replace('122 in sixteen active/prepared groups and 201','136 in eighteen active/prepared groups and 187')+(added if p==start else added.replace('(docs/audit/','(../../../docs/audit/'))
   elif x.startswith('**GitHub preservation:**'):parts[n]=pushpara if p==start else pushpara.replace('(docs/audit/','(../../../docs/audit/')
  edits[p]='\n\n'.join(parts)
 cov=read(ledger);oldcov=deepcopy(cov);cov.setdefault('activeOrdinarySpellReviewHistory',[]).append(deepcopy(cov['activeOrdinarySpellReview']));cov['activeOrdinarySpellReview']['recordedAtUtc']=now
 code=raw[builder].decode('utf8');tail=' + read(A / "COMPANION_EXACT_ILLUSION_ACTIVE_19_NAVIGATION_DELTA.json")["changes"]\n';ck('Unique delta tail',code.count(tail)==1);code=code.replace(tail,tail.rstrip('\n')+' + read(A / "RANK7_WARDS_MANIFESTATIONS_20_NAVIGATION_DELTA.json")["changes"]\n')
 code=code.replace('    featured = [\n','    featured = [\n'+''.join('        '+repr(x)+',\n' for x in [('Current checkpoint20 — rank-seven wards and manifestations',cp.relative_to(G).as_posix()),('Current323 pending identities — queue15',newq.relative_to(G).as_posix())]),1).replace('Current checkpoint19 — companion exact draft and actual illusion review','Checkpoint19 history — companion exact draft and actual illusion review').replace('Current323 pending identities — queue14','Queue14 history — before ward and manifestation preparation')
 code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in [('Ward7 —20 source questions, threeB/fourC, UNSENT','WARD_7_SOURCE_CONFERENCE_01_PREPARATION.json'),('Manifestation7 —23 source questions, threeB/fourC, UNSENT','MANIFESTATION_7_SOURCE_CONFERENCE_01_PREPARATION.json')]),1)
 scope='Video game only.525 reviewed/323 pending;249 standalone;173 scoped interfaces. Actual Illusion14 Current12 plus current context remains in progress; complete Companion exact05 UNSENT with two exactCR2 content holds. Queue15 has136 identities in18 active/prepared groups and187 other original-source identities. Ward7 and manifestation7 add43 source decisions across14 identities/15 placements, each3B4C; neither adopts rules or supplies current cases. Verified GitHubc9c99f1 covers checkpoint19, all24,340 expected blobs and24,265 prior tracked entries preserved. New ward/manifestation work and checkpoint20 local. All75 domain gates unchanged. Latest allowance54percentremaining; continue until review complete or20percent remains.'
 nodes=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];ck('One status',len(nodes)==1);code=code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1);compile(code,str(builder),'exec')
 saved=[]
 for p,data in raw.items():
  dst=keep/p.relative_to(G);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data);saved.append({'source':info(p),'preservedCopy':info(dst)})
 (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved));newq.write_bytes(encoded(q));cov['activeOrdinarySpellReview']['currentQueue']=info(newq);ck('All75 full aspect rows unchanged',cov['aspects']==oldcov['aspects'] and len(cov['aspects'])==75);ledger.write_bytes(encoded(cov))
 for p,t in edits.items():p.write_text(t,encoding='utf8',newline='\n')
 builder.write_text(code,encoding='utf8',newline='\n');changes=[{'before':next({**s['source'],'preservedCopy':s['preservedCopy']['path']} for s in saved if s['source']['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,builder]]
 delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'newRuleAdoptionsByNavigation':0,'all75DomainGatesUnchanged':True,'sourceInformationDeleted':0}))
 checkpoint=deepcopy(read(oldcp));checkpoint.update(id='ACTIVE-AUTHORING-RANK7-WARDS-MANIFESTATIONS-20',recordedAtUtc=now,status=scope,previousCheckpoint=info(oldcp),currentWorkQueue=info(newq),remainingPreparedGroups=q['groups'],rank7WardAndManifestationSourceConferences=prepared,latestVerifiedGitHubBackup={'commit':push['commit'],'receipt':info(pushp),'coverage':'Includes prior work through checkpoint19. All24,340 expected blobs verified and all24,265 prior tracked entries retained.'},laterLocalWork=['Ward7 source conference,20 questions,50 sources,255 checks','Manifestation7 source conference,23 questions,60 sources,283 checks','Queue15 and checkpoint20 navigation'],lastUsageObservation={'usedPercent':46,'remainingPercent':54,'windowMinutes':10080,'secondary':'unavailable'},nextAction='Preserve actual Illusion14 final and reconcile complete decisions. Submit full Companion exact05 next; retain both content holds and separate native NPC review. Continue actual source/case conferences, including prepared wards/manifestations; stop only at review complete or20percent allowance remaining.',coverageLedger=info(ledger),navigationDelta=info(delta),preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'));cp.write_bytes(encoded(checkpoint))
 run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8');ck('Review map builds '+run.stderr[-1200:],run.returncode==0);build=read(buildfile);ck('No missing links',not build['missingLinks']);checkpoint['navigation']={'map':info(mapfile),'build':info(buildfile),'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[]};cp.write_bytes(encoded(checkpoint));report.write_bytes(encoded({'checkpoint':info(cp),'queue':info(newq),'checks':checks,'checkCount':len(checks),'failures':0,'links':build['existingDistinctLinks'],'all75DomainGatesUnchanged':True,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}));print(json.dumps({'checkpoint':info(cp),'queue':info(newq),'checks':len(checks),'links':build['existingDistinctLinks'],'failures':0}))

if __name__=='__main__':main()
