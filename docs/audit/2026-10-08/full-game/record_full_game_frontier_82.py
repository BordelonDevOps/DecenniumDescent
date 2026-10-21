from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,re
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
old=A/'ACTIVE_AUTHORING_CHECKPOINT_BESTIARY_REFRESH_81.json';out=A/'ACTIVE_AUTHORING_CHECKPOINT_FULL_GAME_FRONTIER_82.json';report=A/'ACTIVE_AUTHORING_CHECKPOINT_FULL_GAME_FRONTIER_82_CHECK.json';backup=A/'navigation-before-full-game-frontier-82';saved=A/Path(__file__).name
for p in [out,report,backup,saved]:assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
def ck(s,b):
 checks.append({'check':s,'pass':bool(b)})
 if not b:raise AssertionError(s)
cp=j(old);front=A/'FULL_GAME_CURRENT_EVIDENCE_FRONTIER_82.json';reader=A/'FULL_GAME_CURRENT_REVIEW_MAP_82.md';frontcheck=A/'FULL_GAME_CURRENT_EVIDENCE_FRONTIER_82_CHECK.json';fr=j(front);fc=j(frontcheck)
suppfile=A/'BESTIARY_CURRENT_EX58_CONTEXT_82_PREPARATION.json';sp=j(suppfile)
ck('Exact previous checkpoint81',info(old)['sha256']=='a2284feab326a9cbeffd366d6b959135bf54a05d5c8e713c993951225c376946')
ck('Frontier exact whole75domain evidence',fc['checkCount']==5335 and fc['failures']==0 and fr['counts']['domains']==75 and fr['counts']['uniqueEvidencePaths']==1135 and fr['counts']['evidenceRoleUses']==4088 and fr['counts']['missingReferences']==0 and info(front)==fc['frontier'] and info(reader)==fc['reader'])
ck('Original ledger and all domain declarations untouched',info(G/fr['baseLedger']['path'])==fr['baseLedger'] and fr['counts']['newDomainClosures']==0)
rt=reader.read_text(encoding='utf-8');links=re.findall(r'\]\(([^)]+)\)',rt)
ck('Reader has all75rows and32resolving local links',len(re.findall(r'^\| DD-\d\d \|',rt,re.M))==75 and len(links)==32 and all((reader.parent/p).resolve().exists() for p in links))
ck('Full EX58 supplement89checks passed andunsent',sp['checks']==89 and sp['failures']==0 and not sp['sent'])
for k in ['primary','supplement','request','check']:ck('Exact paired bestiary context '+k,info(G/sp[k]['path'])==sp[k])
ck('Queue67 and50accepted butunapplied unchanged',info(G/cp['currentWorkQueue']['path'])==cp['currentWorkQueue'] and cp['acceptedButUnapplied']==50 and not cp['implementationApplied'])
protected=[cp['currentAuthoredIndex'],cp['currentAcceptedInterfaceRegistry'],*cp['canonicalHelperBaselinesUnchanged']]
for row in protected:ck('Protected current authority '+row['path'],info(G/row['path'])==row)
browser=A/'GPT_PART5_RESONANCE_FIELDS3_HANDOFF_82.txt';bt=browser.read_text(encoding='utf-8')
ck('Specific same GPT process still live','Working for 37m 1s' in bt and 'button "Stop"' in bt and 'DD_Rank9_Resonance_Fields3_Current_Context_80.zip' in bt)
navs=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];originals={p:p.read_bytes() for p in navs}
for row in cp['navigation']:ck('Prior navigation exact '+row['path'],info(G/row['path'])==row)
backup.mkdir()
for p,b in originals.items():(backup/p.name).write_bytes(b)
base='docs/audit/2026-10-08/full-game/'
for p,prefix in [(navs[0],''),(navs[1],'../../../')]:
 b=originals[p];pos=b.index(b'\n')+1
 notice=('\n**Current whole-game map — 20 October 2026:** [Read the 75-domain review map]('+prefix+base+reader.name+') and [Checkpoint 82]('+prefix+base+out.name+'). All 1,135 listed evidence paths resolve. Later exact EX58 expedition and LAX language approvals supersede their old preliminary pending labels within scope. The bestiary V3 packet now has a full current EX58 supplement. GPT is still reviewing Resonance Fields3; applied 525/323/249, 173 interfaces, and 50 accepted but unapplied remain unchanged. No whole-domain gate was newly closed.\n').encode('utf-8')
 p.write_bytes(b[:pos]+notice+b[pos:]);ck('Every prior navigation byte retained '+p.name,p.read_bytes().replace(notice,b'',1)==b)
p=navs[2];b=originals[p];pos=b.index(b'</h1>')+5;notice=('<section class="sequence" aria-label="Current whole-game review map"><p><strong>Checkpoint 82: current evidence across all 75 domains.</strong>All 1,135 listed evidence paths resolve. Exact expedition and language scopes remain accepted; broader gates stay open. <a href="'+base+reader.name+'">Read the current review map</a> · <a href="'+base+out.name+'">Current checkpoint</a></p></section>').encode('utf-8');p.write_bytes(b[:pos]+notice+b[pos:]);ck('Every prior review-map byte retained',p.read_bytes().replace(notice,b'',1)==b)
cp['previousGptObservationBefore82']=deepcopy(cp['activeGptReviewAtLastVerifiedObservation']);cp['activeGptReviewAtLastVerifiedObservation'].update(browserObservation=info(browser),activeGenerationVerified=True,completedResponseReceived=False,latestObservedStatus='Same actual Resonance Fields3 source conference working at37m1s; Stop visible and additional thinking notice shown. No new request, restart or interruption.')
cp.update(id='ACTIVE-AUTHORING-FULL-GAME-FRONTIER-82',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(old),status='All75domain requirements and1135listed evidence paths reconciled into a current reader; exact EX58/LAX bytes verified. Complete EX58 dependency supplement prepared for bestiary V3. Actual ResonanceFields3 reply remains active.',currentFullGameEvidenceFrontier=info(front),currentFullGameReviewMap=info(reader),fullGameEvidenceAudit=info(frontcheck),bestiaryCurrentExpeditionContextPreparation=info(suppfile),bestiaryNextDispatchArchives=[sp['primary'],sp['supplement']],bestiaryNextDispatchRequest=sp['request'],navigation=[info(p) for p in navs],preservedNavigation=[info(backup/p.name) for p in navs],lastUsageObservation={'usedPercent':41,'remainingPercent':59,'stopAtRemainingPercent':20,'resetsAt':1793110625},previousGoalTurnClassification='Previous81madeconcreteprogress: completebestiarysourcepacket438currentfiles453members27questions1525checks. Current82auditsall75requirements,1135explicitpaths/4088uses; verifies8EX58and7LAXcurrentartifacts; preservesallrows; prepares23fileEX58context toavoidduplicate preliminaryexpeditionreview.',laterLocalWork='All73–82 work remains local after verified GitHub backup through72.',nextAction='Receive and independently review the same active ResonanceFields3 return. Then confer on bestiary V3 plus the complete current EX58 supplement; do not repeat fulfilled expedition26 or LAX preliminaries. Continue all pending spell and feat review and remaining75domain integration gates with originals and owner reservation retained.')
out.write_bytes(enc(cp))
for row in protected:ck('Protected authority unchanged at completion '+row['path'],info(G/row['path'])==row)
ck('Original coverage ledger unchanged at completion',info(G/fr['baseLedger']['path'])==fr['baseLedger'])
saved.write_bytes(Path(__file__).read_bytes());report.write_bytes(enc({'checkpoint':info(out),'checks':checks,'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'newDomainClosures':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'scope':'Current evidence navigation and exact dependency preservation; no broader semantic completion claim.'}))
print(json.dumps({'checkpoint':info(out),'report':info(report),'checks':len(checks),'failures':0}))
