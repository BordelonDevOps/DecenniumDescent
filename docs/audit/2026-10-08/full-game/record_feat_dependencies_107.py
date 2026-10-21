from pathlib import Path
import json,hashlib,datetime,shutil
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_DEPENDENCIES_107.json';assert not OUT.exists()
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def bind(p):
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
def ck(n,r):checks.append({'name':n,'passed':bool(r)});assert r,n
prev=A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_ASSEMBLY_106.json';d=j(prev)
for b in d['canonicalHelperBaselinesUnchanged']+[d['currentAuthoredIndex'],d['currentAcceptedInterfaceRegistry']]:ck('Protected source unchanged '+b['path'],bind(G/b['path'])==b)
receipt=j(A/'FEAT335_SPELL_DEPENDENCIES_RECEIPT_107.json')
for key in ['report','proposal','zip']:
    b=receipt[key];actual=bind(Path(b['path']));ck('Actual dependency delivery '+key,actual['bytes']==b['bytes'] and actual['sha256']==b['sha256'])
mapping=j(A/'FEAT335_ACCEPTANCE_EVIDENCE_MAP_107.json');conflicts=j(A/'FEAT335_FXC03_EXACT_MAPPING_107.json')
ck('Complete12 acceptance gates preserved',len(mapping['gates'])==12)
ck('Exact91/15/8/12 mapping complete',len(conflicts['completeConventions'])==91 and len(conflicts['completeFex']['issues'])==15 and len(conflicts['eightExplicitConflicts'])==8 and len(conflicts['twelveWarriorCounterparts'])==12 and conflicts['failed']==0)
d['id']='ACTIVE_AUTHORING_CHECKPOINT_FEAT_DEPENDENCIES_107';d['recordedAtUtc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
d['previousCheckpoint']=bind(prev);d['previousGoalTurnClassification']='Progress:106 completed full335 derived assembly and current acquisition/allowance mirrors; successful programs not rerun.'
d['status']='Progress: current spell dependencies and finite-table placements verified; one Planar Binding reference divergence prepared for GPT; exact convention/counterpart mapping complete.'
d['featDependencies107']={'receipt':bind(A/'FEAT335_SPELL_DEPENDENCIES_RECEIPT_107.json'),'report':receipt['report'],'proposal':receipt['proposal'],'package':receipt['zip'],
    'dependencyCards':284,'matchingCurrentCards':283,'selectedPlacements':1845,'curriculumPlacements':1838,'ritualPlacements':7,
    'checksPassed':7684,'failed':0,'concreteFinding':'Ordinary Planar Binding was accepted by AC5-EXACT-ACCEPTANCE-05, while its separate null feat wrapper still describes the ordinary spell as undeveloped. Proposed reference-only successor preserves old receipt and keeps feat null/unavailable; no activation or cosmology change.',
    'proposalApplied':False,'parent335Accepted':False,'canonicalApplied':False}
d['featAcceptanceMap107']={'map':bind(A/'FEAT335_ACCEPTANCE_EVIDENCE_MAP_107.json'),'all12OriginalRequirementsPreserved':True,'finiteTableCounts':mapping['finiteTableCounts'],
    'explicitConflictMap':bind(A/'FEAT335_FXC03_EXACT_MAPPING_107.json'),'explicitConflictMapChecks':210,'failed':0,
    'gate03MissingFieldMapNowSupplied':True,'parentAccepted':False,'allGatesFulfilled':False,
    'qualification':'The later FXC03 report supplies the missing91convention/15FEX/8explicit-conflict/12Warrior map identified in the earlier107 overview. Do not repeat that completed mapping.'}
d['preparedGptDependencyFollowup107']={'request':bind(A/'GPT_FEAT_DEPENDENCY_REQUEST_107.txt'),'package':receipt['zip'],'actuallyUploaded':False,'actuallySent':False,
    'timing':'Only after current R105 response is terminal and received; never interrupt active generation. Attach the actual source packet before sending its exact bounded request.'}
d['notebookRecheck107']={'visible':bind(A/'GPT_BESTIARY_RECONCILIATION_VISIBLE_107.txt'),'latestVisible':bind(A/'GPT_BESTIARY_RECONCILIATION_LATEST_107.txt'),
    'status':'Live Stop remains visible with systems-thinking status. GPT has printed measured staged output but no final downloadable response has been observed.',
    'reportedStagedArchiveOnly':{'name':'DD_Bestiary_Final_Reconciliation_105.zip','bytes':334113,'sha256':'a941ca9203a1e4250a2629e9978bbb382bfabbb7b77b1fff881a824e39053a5f'},
    'reportedStagedManifestOnly':{'bytes':2100,'sha256':'4d3010d3b4faa14355420199d83e994307cf58dc17d21f7cee82c8f0b81e6b82'},
    'reportedCountsNotIndependentlyAccepted':{'files':11,'zipMembers':12,'localChecks':3484,'replacementParents':13,'supersededTraces':26,'additionalCases':12,'additionalTransitions':36,'JSONOperations':45,'markdownLocators':24,'summaryReplacements':4},
    'newMessagesSent':0,'newFinalDownloadReceived':False,'generationInterrupted':False,'artifactR105IsNotLocalCheckpoint105':True}
d['lastUsageObservation']={'usedPercent':73,'remainingPercent':27,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits during107 after dependency/map work'}
d['nextAction']='First inspect the same live Part5 browser handle without interrupting. When R105 is actually final, download its real exposed ZIP, verify measured bytes/hash/manifests against the final reply and preserve all original inputs; perform independent full before/after/mirror and replacement-case semantic review without running supplied code or old programs. Once idle, attach DD_Feat335_Spell_Dependencies_107.zip and send the prepared bounded GPT_FEAT_DEPENDENCY_REQUEST_107.txt; proposal is not applied. Continue remaining FXC04-09 named-boundary/evidence mappings using actual source-qualified cases and accepted FT84/current copy sources, not new generic prerequisite conferences. FXC03 exact91/15/8/12 map is done107; all660+28 semantic case reviews and nine cohorts are done105; full335assembly and current177allowance descriptors are done106. Incorporate only agreed dependency wording into a new derived successor, preserving106/107 originals. Then bind and submit the complete exact parent candidate/evidence. Keep525/323/249/173,53accepted-unapplied, two null feat wrappers, private boundaries, four canonical copy helpers, Unity isolation and final joint-flow→verifiedGitHub→cosmology order.'
d['laterLocalWork']='73–107 remain local after last separately verified GitHub baseline. New107 dependency proposal/maps are derived review evidence, not canonical application or push.'
backup=A/'navigation-before-feat-dependencies-107';backup.mkdir();nav=[];prior=[]
for n,b in enumerate(d['navigation']):
    p=G/b['path'];raw=p.read_bytes();bp=backup/(str(n+1)+p.suffix);bp.write_bytes(raw);prior.append(bind(bp));text=raw.decode('utf-8-sig')
    link='docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_FEAT_DEPENDENCIES_107.json'
    summary='All1845 selected spell placements are exact;283of284 retained dependency cards match current sources. Planar Binding needs a reference-only reconciliation while its feat remains null. All91conventions/15FEX/8explicit conflicts/12Warrior pairs now have exact source/current-case maps. Full parent review remains open; no runtime or canonical promotion.'
    if p.suffix=='.html':
        ck('HTML main exists','<main>' in text);text=text.replace('<main>','<main>\n<section class="sequence"><p><strong>Current review checkpoint:</strong> <a href="'+link+'">Checkpoint107</a> '+summary+'</p></section>\n',1)
    else:
        if p.name=='DEVELOPMENT_DIRECTION.md':link='../../../'+link
        first,rest=text.split('\n',1);text=first+'\n\n**Current review checkpoint:** [Checkpoint107]('+link+') '+summary+'\n'+rest
    p.write_text(text,encoding='utf-8');nav.append(bind(p))
d['navigation']=nav;d['preservedNavigation']=prior
OUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for b in prior:ck('Prior navigation retained '+b['path'],bind(G/b['path'])==b)
check={'id':'CHECKPOINT107-REGISTRATION','checkpoint':bind(OUT),'passed':len(checks),'failed':0,'checks':checks,'goalComplete':False}
q=A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_DEPENDENCIES_107_CHECK.json';q.write_text(json.dumps(check,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ['audit_feat_spell_dependencies_107.py','map_feat_acceptance_107.py','map_feat_conflicts_107.py','record_feat_dependencies_107.py']:
    target=A/name;assert not target.exists();shutil.copy2(Path(__file__).parent/name,target)
print(json.dumps({'checkpoint':bind(OUT),'check':bind(q),'passed':len(checks),'failed':0,'usageRemainingPercent':27}))
