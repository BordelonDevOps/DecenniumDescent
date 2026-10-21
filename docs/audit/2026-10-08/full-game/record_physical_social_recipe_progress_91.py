"""One-shot checkpoint for completed feat diagnostics and missing-source preparation."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import json,hashlib

G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_RESONANCE_ACCEPTANCE_90.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_PHYSICAL_SOCIAL_RECIPES_91.json'
CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_PHYSICAL_SOCIAL_RECIPES_91_CHECK.json'
REQ=A/'CODEX_BESTIARY_RECIPE_DEPENDENCY_FOLLOWUP_91.txt'
QUAL=A/'FEAT335_PHYSICAL_SOCIAL_COVERAGE_QUALIFICATION_91.json'
BACKUP=A/'navigation-before-physical-social-recipes-91';SAVED=A/Path(__file__).name
for p in [OUT,CHECK,REQ,QUAL,BACKUP,SAVED]:assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def put(p,b):
 with p.open('xb') as f:f.write(b)
checks=[]
def ck(name,c):checks.append({'check':name,'pass':bool(c)});assert c,name
prior=j(PRE);cp=deepcopy(prior)
ck('Checkpoint90 exact',info(PRE)['sha256']=='fbbd221ee955eeec76dbe2fcfcd4a4ce861dcfc8bf14e70046019860eb9c9962')
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]:ck('Canonical baseline unchanged '+row['path'],info(G/row['path'])==row)
physical_path=A/'FEAT335_PHYSICAL_SOCIAL_COMPOSITIONS_91.json';physical=j(physical_path)
deps_path=A/'BESTIARY_LINKED_RECIPE_DEPENDENCIES_91_PREPARATION.json';deps=j(deps_path)
ck('Physical/social77cases136checks passed',physical['caseCount']==77 and physical['passed']==136 and physical['failed']==0 and all(r['pass'] for r in physical['checks']))
ck('Eleven complete selected feat records and18 full sources',len(physical['fullSelectedFeatRecords'])==11 and len(physical['sourceBindings'])==18)
adjudicated=[r['id'] for r in physical['cases'] if 'source-adjudicated' in r['qualification'].lower()]
ck('One expressly source-adjudicated scheduler case',adjudicated==['FP91-M13'])
ck('Parent335 and runtime not accepted',not physical['parent335Accepted'] and physical['runtimeTestsExecuted']==0 and not physical['canonicalImplementationApplied'])
ck('Complete caltrop ownership20pieces',len(physical['finalCaltropPhysicalState']['pieces'])==20)
ck('Full source dependency preparation65checks19files',deps['passed']==65 and deps['failed']==0 and deps['fullSourceFiles']==19 and all(c['pass'] for c in deps['checks']))
ck('Recipe dependency supplement not sent',not deps['actuallySent'])
ck('Both exact linked recipe identities',deps['exactRecipeIds']==['recipe-92','recipe-173'])
ck('Bestiary live generation observed', 'button "Stop"' in (A/'GPT_BESTIARY_ACTIVE_OBSERVATION_91.txt').read_text(encoding='utf-8'))
ck('Resonance acknowledgment remains unsent while GPT generates',not prior['resonanceAcceptanceAcknowledgment90']['actuallySent'])
qualification={'id':'FEAT335-PHYSICAL-SOCIAL-COVERAGE-QUALIFICATION-91','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'report':info(physical_path),'caseCount':77,'calculatedDiagnosticCases':76,'sourceAdjudicatedOnlyCases':adjudicated,'passingChecks':136,'meaning':'All136 checks passed; these include source equality, preserved hashes, arithmetic/state calculations and one expressly source-adjudicated expected boundary. The77-case total is not77 runtime tests. FP91-M13 records the source-required scheduling result but does not execute a scheduler. The other76 cases execute only their described bounded reference calculations/state projections, not complete game operations.','remainingScope':physical['remainingScope'],'sourceFieldsPreserved':True,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'parent335Accepted':False,'canonicalImplementationApplied':False}
ack=(A/'CODEX_RESONANCE_ACCEPTANCE_FOLLOWUP_90.txt').read_text(encoding='utf-8').split('\n\nThis acknowledgment is prepared locally')[0].strip()
request=ack+'''\n\nBestiary follow-through source supplement: while your existing response was generating, I independently confirmed a concrete packet omission. All four full current public Fishing artifacts were absent from V3; recipe-173's review-index label and old crafting-engine effect status therefore did not provide its reviewed operative procedure. I have now prepared DD_Bestiary_Linked_Recipe_Dependencies_91.zip,564856bytes,SHA256019ef9001fa948d02c1df0bb60bf7195bcbfa83485b2e9efaa5c85a4b8c6dd58. The19 full sources and both exact linked recipe identities passed65 source/hash/archive checks. The current exact-review manifests still match all11 underlying authored artifacts, including private counterparts verified by hash only.

Read CURRENT_LINKED_RECIPES.json and the complete attached source files. It retains both original source recipes and full prior audit links, the full current public card texts, both complete public candidates/guides, the actual review/repair evidence and framework sources. Recipe-173 is the reviewed fishing.tackle/Rod-only profile, not a boat supplied by its historical River Fishing Boat name. Its bonus and extra-recovery families are separate; secure capture records one evaluation per actual creature including zero, and additional available reserve units require later lawful harvesting. Recipe-92 retains its complete accepted-feast, temporaryHP, lightning-resistance, actual food and packaging procedure.

Use these existing reviewed sources to resolve only real missing-dependency uncertainty in your completed Bestiary return. Preserve that return as the full baseline and produce complete affected artifacts with exact reversible before/after references if changes are needed. Do not reopen the recipes' settled benefits or infer new ingredient/donor aliases, formula access, catch stock, usable material quantities, boat bodies, monster CR/type or cosmology from names. Original40 printed references,178 harvest occurrences, all material-context comparisons and every other Bestiary question/hold still require their actual dispositions. Older aggregate recipe counts and source-conference pending labels are historical, not current authority. Keep sealed dossiers limited to containment/routing evidence.

Local parent335 review also progressed:77 physical/social cases, comprising76 bounded calculations/state projections and one explicit source-adjudicated scheduling boundary, passed136 checks across11 complete feat records. Locks preserve actual Action/DC and numerical trap-failure margin; caltrops preserve all20 physical pieces through entries, collection and removal; mounted advantages retain separate scopes; Haven appraisal/bargaining retain full30-minute operations; prices, sponsor deductions and greater-of assay fees remain exact. This is a status summary only: that18-source packet is local and is not attached here. Parent335 remains unaccepted. Applied525/323/249/173 and53 accepted-unapplied spell identities remain unchanged. No canonical integration, game runtime, human/balance/cosmology/release approval or deletion occurred.\n'''

cp['id']='ACTIVE-AUTHORING-PHYSICAL-SOCIAL-RECIPES-91';cp['recordedAtUtc']=datetime.now(timezone.utc).isoformat();cp['previousCheckpoint']=info(PRE)
cp['status']='Concrete progress:77 physical/social cases across11 feats preserved with136 successful bounded checks and18 full sources; full current Fishing/Cooking linked-recipe supplement prepared with19 sources/65 checks after confirming an omission in Bestiary V3. GPT still generating the original Bestiary response; no interruption or new send.'
cp['previousGoalTurnClassification']={'turn':90,'classification':'progress','evidence':prior['currentResonanceExactAcceptance90']}
cp['featPhysicalSocial91']={'report':info(physical_path),'archive':info(A/'DD_Feat335_Physical_Social_Compositions_91.zip'),'caseCount':77,'calculatedDiagnosticCases':76,'sourceAdjudicatedOnlyCases':adjudicated,'checks':136,'failed':0,'fullSelectedFeatRecords':11,'fullSourceFiles':18,'archiveMembers':22,'fullCaltropPieceCount':20,'qualification':{'path':QUAL.relative_to(G).as_posix(),'bytes':len(enc(qualification)),'sha256':hashlib.sha256(enc(qualification)).hexdigest()},'remainingScope':physical['remainingScope'],'parent335Accepted':False,'canonicalApplied':False,'runtimeTestsExecuted':0,'actuallySentToGpt':False,'firstPackagingFailurePreserved':physical['priorFailedPackagingAttempt']}
cp['bestiaryLinkedRecipeDependencies91']={'preparation':info(deps_path),'archive':deps['archive'],'model':deps['model'],'fullSourceFiles':19,'checks':65,'failures':0,'actuallySent':False,'reason':'Live Bestiary generation still active; preserve complete response before sending a bounded dependency follow-through.','finding':'The four complete current public Fishing artifacts were absent from V3; both directly catalog-linked source recipes are supplied with their full current operative files and review history. No new game rule.'}
cp['bestiaryNextSafeFollowup91']={'request':{'path':REQ.relative_to(G).as_posix(),'bytes':len(request.encode()),'sha256':hashlib.sha256(request.encode()).hexdigest()},'attachments':[deps['archive']],'containsFullResonanceAcceptanceAcknowledgment':True,'actuallySent':False,'dispatchPrerequisite':'Wait for the actual currently active Bestiary generation to finish. Download/preserve/inspect its full result first. Reconcile this prepared text with the actual findings and current accepted count, then send only the needed source follow-through; do not interrupt or resend original V3/EX58 automatically.'}
cp['previousGptObservationBefore91']=prior['activeGptReviewAtLastVerifiedObservation']
cp['activeGptReviewAtLastVerifiedObservation']['latestObservation91']=info(A/'GPT_BESTIARY_ACTIVE_OBSERVATION_91.txt')
cp['activeGptReviewAtLastVerifiedObservation']['latestObservedStatus']='Live browser still exposes Stop. Latest visible work identifies absent Fishing operative sources for linked recipe-173; local source supplement is complete and unsent. No final Bestiary response observed.'
cp['bestiaryActualDispatch89']['latestObservation91']=info(A/'GPT_BESTIARY_ACTIVE_OBSERVATION_91.txt')
cp['nextAction']='Continue remaining feat native/copy/world and full exact casebook work while Bestiary generation continues. On its actual completion, preserve the return and perform full intake; send the prepared missing recipe-source supplement with Resonance acceptance acknowledgment as needed. Neither the physical/social91 nor healing89 full parent335 packet has been sent. Parent335 remains unaccepted. Canonical implementation remains owner-reserved.'
cp['lastUsageObservation']={'usedPercent':53,'remainingPercent':47,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits near end91'}
cp['laterLocalWork']='Checkpoints73–91 remain local after the last separately verified GitHub backup through72; no push in91.'

nav=[G/'START_HERE.md',G/'DescentReviewChanges/ReviewBible/docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];old={};prepared={}
for p in nav:
 binding=next(x for x in prior['navigation'] if x['path']==p.relative_to(G).as_posix());ck('Current navigation exact '+p.name,info(p)==binding);raw=old[p]=p.read_bytes()
 if p.suffix=='.html':
  pos=raw.find(b'>',raw.find(b'<body'))+1
  note=('<aside><p><strong>Checkpoint91:</strong>77 physical/social feat cases (76 calculated, one source-adjudicated),136 checks; complete Fishing/Cooking source supplement prepared for GPT. Bestiary review still active. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>.53 accepted-unapplied spells; canonical files unchanged.</p></aside>\n').encode()
 else:
  pos=raw.find(b'\n')+1;prefix='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/'
  note=('\n**Current checkpoint — physical/social review:** [Checkpoint91]('+prefix+OUT.name+') preserves77 feat cases (76 calculated and one source-adjudicated) with136 checks, plus the complete19-source Fishing/Cooking dependency supplement for GPT. The Bestiary response is still generating; both the supplement and Resonance acceptance acknowledgment remain unsent.53 accepted-unapplied spells and applied525/323/249/173 remain unchanged.\n').encode()
 ck('Valid insertion '+p.name,pos>0);new=raw[:pos]+note+raw[pos:];ck('Prior navigation bytes preserved '+p.name,new[:pos]+new[pos+len(note):]==raw);prepared[p]=new
ck('Every previous checkpoint field retained',set(prior).issubset(cp))
ck('No count/promotion change',cp['acceptedButUnapplied']==53 and cp['authoredCounts']==prior['authoredCounts'] and not cp['implementationApplied'])
put(REQ,request.encode());put(QUAL,enc(qualification));BACKUP.mkdir();cp['preservedNavigation']=[]
for p in nav:
 dst=BACKUP/p.name;put(dst,old[p]);cp['preservedNavigation'].append(info(dst));p.write_bytes(prepared[p])
cp['navigation']=[info(p) for p in nav];put(SAVED,Path(__file__).read_bytes());put(OUT,enc(cp))
result={'id':'CHECKPOINT91-VALIDATION','checkpoint':info(OUT),'checks':checks,'passed':len(checks),'failed':0,'script':info(SAVED),'anyNewGptMessageSent':False}
put(CHECK,enc(result))
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'passed':len(checks),'failed':0,'newGptMessageSent':False},indent=2))
