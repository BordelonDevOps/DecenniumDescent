from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import hashlib, json, zipfile

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
OLD=A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_TIME_PROVISIONS_83.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_WORK_COMPOSITIONS_84.json'
CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_WORK_COMPOSITIONS_84_CHECK.json'
BACKUP=A/'navigation-before-feat-work-compositions-84'
REQUEST=A/'GPT_FEAT_TIME_INTERFACES_REQUEST_84.txt'
PREP=A/'FEAT_TIME_INTERFACES_DISPATCH_PREPARATION_84.json'
SAVED=A/Path(__file__).name
for p in [OUT,CHECK,BACKUP,REQUEST,PREP,SAVED]:assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
def ck(label,value):
 checks.append({'check':label,'pass':bool(value)})
 if not value:raise AssertionError(label)
cp=j(OLD)
ck('Exact prior checkpoint83',info(OLD)['sha256']=='a1ff3a9a6e3aa7d87ecd8287cbdb5b50c57f767dfb73e5a17564569d51796388')
reportfile=A/'FEAT335_WORK_COMPOSITIONS_84.json';checkfile=A/'FEAT335_WORK_COMPOSITIONS_CHECK_84.json';archive=A/'DD_Feat335_Work_Compositions_84.zip'
report=j(reportfile);validation=j(checkfile)
ck('Exact passing159check diagnostic',validation['checkCount']==159 and validation['failures']==0 and all(x['pass'] for x in validation['checks']) and info(reportfile)==validation['report'] and info(archive)==validation['archive'])
ck('78case variants29groups14full records16full source files',report['caseCount']==78 and len(report['cases'])==78 and report['topLevelCaseCount']==29 and len(report['fullSelectedFeatRecords'])==14 and len(report['sourceBindings'])==16)
ck('Three unselected source-interface dispositions',len(report['openDispositions'])==3 and all(q['disposition'].startswith('UNSELECTED') for q in report['openDispositions']))
ck('No runtime, candidate or parent feat approval',not any(report['approvalBoundaries'].values()) and validation['runtimeTestsExecuted']==0)
for row in report['sourceBindings']:ck('Current full source exact '+row['path'],info(G/row['path'])==row)
with zipfile.ZipFile(archive) as z:
 ck('Full archived report matches',z.read('REPORT.json')==reportfile.read_bytes())
 mf=json.loads(z.read('MANIFEST.json'))
 ck('Full manifest membership',set(z.namelist())==set(mf)|{'MANIFEST.json'})
 ck('Archive CRC',z.testzip() is None)
 for name,binding in mf.items():
  b=z.read(name);ck('Exact archive member '+name,len(b)==binding['bytes'] and hashlib.sha256(b).hexdigest()==binding['sha256'])
protected=[cp['currentAuthoredIndex'],cp['currentAcceptedInterfaceRegistry'],cp['currentWorkQueue'],*cp['canonicalHelperBaselinesUnchanged']]
for row in protected:ck('Canonical authority exact '+row['path'],info(G/row['path'])==row)
ck('50accepted-unapplied unchanged',cp['acceptedButUnapplied']==50 and not cp['implementationApplied'])
prior=cp['featTimeProvisionsDiagnostics']
for key in ['report','archive','validation']:ck('Prior83 evidence exact '+key,info(G/prior[key]['path'])==prior[key])
browser=A/'GPT_PART5_RESONANCE_FIELDS3_HANDOFF_84.txt';bt=browser.read_text(encoding='utf-8')
ck('Same GPT generation live at1h5m28s','Working for 1h 5m 28s' in bt and 'button "Stop"' in bt and 'Packaged and verified the complete artifact bundle' in bt)

request=('Prepared, UNSENT. Send only after the current Resonance Fields3 generation has completed and its full return is preserved.\n\n'
 'Please resolve three exact remaining feat time interfaces using the attached complete source files in DD_Feat335_Work_Compositions_84.zip. This is a targeted continuation of the completed FEAT327 source conference, not a request to reopen its settled rules or promote the parent335 candidate. REPORT.json preserves14 complete relevant feat records, all three unselected questions, actual recipe121, the full FA13 source expectation and78 conditional specification cases. All16 full input files are in sources/. The companion DD_Feat335_Time_Provisions_Cases_83.zip preserves the completed local Forager/Endurance cases and exact EX58 source.\n\n'
 'The new local checks passed159 and88 respectively. These are self-contained specification diagnostics; no downloaded/project Python, full character acquisition, game runtime or campaign world ran. Sources, selection flags, spell index, canonical helpers and owner implementation reservation are unchanged. Applied ordinary-spell coverage remains525reviewed/323pending/249standalone with173interfaces;50accepted spell identities remain unapplied. This request does not change those counts.\n\n'
 '\n\n'.join(q['id']+' — '+q['subject']+'\n'+q['exactSourceIssue']+'\n'+q['request'] for q in report['openDispositions'])+
 '\n\nPreserve source benefits and every original statement. Explicitly separate an existing rule interpretation from any NEW narrow completion. Return full selected wording with original before values, exact source hashes/pointers, complete reasoned dispositions and useful positive/negative cases with actual time, stock and progress ledgers. Include whole-job versus staged-tail behavior and interrupted-phase/rounding boundaries only where relevant. Do not narrow otherwise lawful copying or creation simply to make tests easier. Keep one-per-source use histories, all costs, assistants, prerequisites, real uninterrupted work, unrelated fixed waits and public/private boundaries. No canonical implementation, full335acceptance, runtime, balance, cosmology or release approval is requested.\n')
REQUEST.write_text(request,encoding='utf-8')
PREP.write_bytes(enc({'status':'PREPARED_UNSENT','primary':info(archive),'supplement':prior['archive'],'request':info(REQUEST),'sourceQuestionCount':3,'questions':report['openDispositions'],'actualGptMessageId':None,'canonicalChange':False,'sourceInformationDeleted':0}))
navs=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html']
for row in cp['navigation']:ck('Previous navigation exact '+row['path'],info(G/row['path'])==row)
originals={p:p.read_bytes() for p in navs};BACKUP.mkdir()
for p,b in originals.items():(BACKUP/p.name).write_bytes(b)
base='docs/audit/2026-10-08/full-game/'
for p,prefix in [(navs[0],''),(navs[1],'../../../')]:
 b=originals[p];pos=b.index(b'\n')+1
 notice=('\n**Current checkpoint — 20 October 2026:** [Checkpoint84]('+prefix+base+OUT.name+') preserves78 work/repair specification cases and159passing checks, in addition to the prior Forager/Endurance evidence. Three exact source-interface questions are prepared for GPT: ritual copying, research phases and feat-granted construction. No parent feat or runtime approval is claimed. [The75-domain map]('+prefix+base+'FULL_GAME_CURRENT_REVIEW_MAP_82.md) remains current; canonical spell counts and50accepted-unapplied identities are unchanged.\n').encode('utf-8')
 p.write_bytes(b[:pos]+notice+b[pos:]);ck('All prior navigation bytes preserved '+p.name,p.read_bytes().replace(notice,b'',1)==b)
p=navs[2];b=originals[p];pos=b.index(b'</h1>')+5
notice=('<section class="sequence" aria-label="Current work and repair diagnostic checkpoint"><p><strong>Checkpoint84: work, time and repair interfaces.</strong>78 conditional specification cases pass159checks. Three source-interface questions remain unselected for GPT; full feat and engine gates stay open. <a href="'+base+OUT.name+'">Current checkpoint</a> · <a href="'+base+'FULL_GAME_CURRENT_REVIEW_MAP_82.md">75-domain review map</a></p></section>').encode('utf-8')
p.write_bytes(b[:pos]+notice+b[pos:]);ck('All prior review-map bytes preserved',p.read_bytes().replace(notice,b'',1)==b)
cp['previousGptObservationBefore84']=deepcopy(cp['activeGptReviewAtLastVerifiedObservation'])
cp['activeGptReviewAtLastVerifiedObservation'].update(browserObservation=info(browser),activeGenerationVerified=True,completedResponseReceived=False,latestObservedStatus='Same actual Resonance Fields3 review live at1h5m28s. Visible progress now includes complete bundle packaging/verification; Stop remains visible. No final response or archive received yet, and no interruption or restart.')
cp.update(id='ACTIVE-AUTHORING-FEAT-WORK-COMPOSITIONS-84',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(OLD),status='78 additional work/repair specification cases passed159checks. Three exact source-interface dispositions preserved unselected with an unsent byte-bound GPT request. Same active ResonanceFields3 review has reached packaging but has not returned.',featWorkCompositionsDiagnostics={'report':info(reportfile),'archive':info(archive),'validation':info(checkfile),'caseCount':78,'topLevelCaseCount':29,'checkCount':159,'failures':0,'fullSourceFiles':16,'fullSelectedRecords':14,'parentFeatApproved':False,'runtimeTestsExecuted':0},featTimeInterfacesNextConference=info(PREP),navigation=[info(p) for p in navs],preservedNavigation=[info(BACKUP/p.name) for p in navs],previousGoalTurnClassification='83 made concrete progress: preserved20Forager/Endurance groups28variants88checks and exact sources. Current84adds78work/repair cases159checks, with genuine3source-interface questions identified and prepared rather than silently decided.',laterLocalWork='All73–84work remains local after the verified GitHub backup through72.',nextAction='Preserve and independently review the same active ResonanceFields3 return when it completes. Confer on the three prepared exact feat time interfaces using both complete83/84archives; carry those dispositions into full335review. Bestiary V3 and its current EX58 supplement also remain ready and unsent. Continue all remaining75domain integration and authoring gates without promoting runtime or changing owner-reserved canonical implementation.')
OUT.write_bytes(enc(cp))
for row in protected:ck('Canonical authority unchanged at completion '+row['path'],info(G/row['path'])==row)
for row in report['sourceBindings']:ck('Full original source unchanged at completion '+row['path'],info(G/row['path'])==row)
SAVED.write_bytes(Path(__file__).read_bytes());CHECK.write_bytes(enc({'checkpoint':info(OUT),'checks':checks,'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'newDomainClosures':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'scope':'Exact preservation, conditional diagnostic evidence and unselected source-interface preparation; no parent feat completion.'}))
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'preparedRequest':info(REQUEST),'preparation':info(PREP),'checks':len(checks),'failures':0}))
