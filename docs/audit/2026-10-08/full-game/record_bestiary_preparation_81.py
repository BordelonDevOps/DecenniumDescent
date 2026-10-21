from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import hashlib,json
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
old=A/'ACTIVE_AUTHORING_CHECKPOINT_ALL_PENDING_GROUPED_80.json';out=A/'ACTIVE_AUTHORING_CHECKPOINT_BESTIARY_REFRESH_81.json';check=A/'ACTIVE_AUTHORING_CHECKPOINT_BESTIARY_REFRESH_81_CHECK.json';backup=A/'navigation-before-bestiary-refresh-81';saved=A/Path(__file__).name
for p in [out,check,backup,saved]:assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
def ck(s,b):
 checks.append({'check':s,'pass':bool(b)})
 if not b:raise AssertionError(s)
cp=j(old);prepfile=A/'BESTIARY_COMPLETE_FILE_HANDOFF_V3_PREPARATION_81.json';prep=j(prepfile)
ck('Exact checkpoint80',info(old)['sha256']=='7993ad5564b0ac39348e7d0ed0d2b2c1f3937aa9524b64498618af32050bf7cb')
ck('Current spell queue67 unchanged',info(G/cp['currentWorkQueue']['path'])==cp['currentWorkQueue'])
ck('All323pending grouped in56groups;50accepted but unapplied',cp['groupedPendingIdentities']==323 and cp['ungroupedPendingIdentities']==0 and cp['preparedGroupCount']==56 and cp['acceptedButUnapplied']==50 and not cp['implementationApplied'])
ck('Bestiary refresh remains source preparation',prep['status']=='PASS_COMPLETE_SOURCE_PREPARATION_UNSENT' and prep['sent'] is False and prep['checks']==1525 and prep['failures']==0)
for key in ['archive','previousArchive','previousPreparation','report','checkReport']:ck('Prepared exact '+key,info(G/prep[key]['path'])==prep[key])
for row in prep['canonicalBaselines']:ck('Unchanged protected authority '+row['path'],info(G/row['path'])==row)
browser=A/'GPT_PART5_RESONANCE_FIELDS3_HANDOFF_81.txt';bt=browser.read_text(encoding='utf-8')
ck('Same live GPT source conference', 'Working for 27m 50s' in bt and 'button "Stop"' in bt and 'DD_Rank9_Resonance_Fields3_Current_Context_80.zip' in bt)
nativefile=A/'GPT_PART5_PERTINENT_RECHECK_81_NATIVE.json';nwrap=j(nativefile);nv=json.loads(next(x['text'] for x in nwrap['content'] if x['type']=='text'))
ck('Native latest dispatch retains actual turn',nv['turns'][0]['id']=='fcee2fb1-a2d9-4ee5-b2dc-9c9fb75f9194')
unityfile=A/'UNITY_DIRECTIONS_PERTINENT_RECHECK_81_NATIVE.json';uv=json.loads(next(x['text'] for x in j(unityfile)['content'] if x['type']=='text'))
ck('Unity latest requested brief unchanged',uv['turns'][0]['id']=='41d5797f-d115-4cce-90fd-8ccc835b86cb' and any(x.get('id')=='b0572b7f-e15c-4d11-8353-86853e0329c6' for x in uv['turns'][0]['items']))
ub=A/'unity-development-directions-75/Decennium_Descent_Unity_Codex_Directions.md';ck('Full Unity brief still exact',info(ub)['sha256']=='cfca586c7351f7ac913523a3b9cde076bc3e92f4301404f1f78b608db6145369')
for row in cp['navigation']:ck('Prior navigation exactly preserved before new entry '+row['path'],info(G/row['path'])==row)
navs=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];originals={p:p.read_bytes() for p in navs};backup.mkdir()
for p,b in originals.items():(backup/p.name).write_bytes(b)
base='docs/audit/2026-10-08/full-game/'
for p,prefix in [(navs[0],''),(navs[1],'../../../')]:
 b=originals[p];pos=b.index(b'\n')+1
 notice=('\n**Current review checkpoint — 20 October 2026:** [Checkpoint 81]('+prefix+base+out.name+') adds the refreshed [complete bestiary conference]('+prefix+base+prepfile.name+'): 67 dossiers, 66 stat blocks, 162 actions, 178 harvest entries, 27 unselected questions, and 1,525 preservation/source checks. Prepared and unsent. GPT is still developing Resonance Fields3. [Queue 67]('+prefix+cp['currentWorkQueue']['path']+') remains current; 50 accepted but unapplied; applied 525/323/249 and 173 interfaces unchanged.\n').encode('utf-8')
 p.write_bytes(b[:pos]+notice+b[pos:]);ck('Every prior navigation byte retained '+p.name,p.read_bytes().replace(notice,b'',1)==b)
p=navs[2];b=originals[p];pos=b.index(b'</h1>')+5
notice=('<section class="sequence" aria-label="Current bestiary preparation"><p><strong>Checkpoint 81: complete bestiary evidence refreshed.</strong>67 dossiers,162 actions,178 harvest entries;27 unselected questions. Prepared and unsent. GPT Resonance Fields3 review remains active. Spell Queue67 and canonical rules unchanged. <a href="'+base+out.name+'">Current checkpoint</a></p></section>').encode('utf-8')
p.write_bytes(b[:pos]+notice+b[pos:]);ck('Every prior review-map byte retained',p.read_bytes().replace(notice,b'',1)==b)
cp['previousGptObservationBefore81']=deepcopy(cp['activeGptReviewAtLastVerifiedObservation'])
cp['activeGptReviewAtLastVerifiedObservation'].update(browserObservation=info(browser),activeGenerationVerified=True,completedResponseReceived=False,latestObservedStatus='Same actual Resonance Fields3 generation active at27m50s with Stop visible; native read exposes the user dispatch but no final. No resend or interruption.')
cp.update(id='ACTIVE-AUTHORING-BESTIARY-REFRESH-81',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(old),status='Complete current bestiary source packet prepared and independently source-checked; no creature authorship or additional spell acceptance. Actual GPT Resonance Fields3 review continues.',bestiaryCurrentSourcePreparation=info(prepfile),bestiaryCurrentSourceInventory=info(A/'BESTIARY_CURRENT_SOURCE_INTERFACES_81.json'),bestiaryUnsentArchive=prep['archive'],pertinentNotebookRecheck81={'part5':info(nativefile),'unity':info(unityfile),'fullUnityBrief':info(ub),'finding':'No new Unity direction beyond the preserved18-section brief. Part5 active conference not finalized.'},navigation=[info(p) for p in navs],preservedNavigation=[info(backup/p.name) for p in navs],lastUsageObservation={'usedPercent':40,'remainingPercent':60,'stopAtRemainingPercent':20,'resetsAt':1793110625},laterLocalWork='All73–81 work remains local after verified GitHub backup through72.',previousGoalTurnClassification='Current81 refreshed all370previous bestiary dependencies, preserved7changed fullbefore/current pairs and the entire V2archive, added current accepted spell/language/crafting/Null context, mapped27unselected source questions and performed396modifier/119exact-rational mean diagnostics.1525preservation/sourcechecks passed; no rule adoption.',nextAction='Receive and preserve the same live ResonanceFields3 final and archive; review its complete selected rules and cases independently. Then dispatch the prepared full bestiary V3 conference after checking any intervening relevant decisions. Retain all holds, originals and owner-reserved canonical implementation.')
out.write_bytes(enc(cp))
for row in prep['canonicalBaselines']:ck('Protected rules/helpers/75domain gate data remain unchanged '+row['path'],info(G/row['path'])==row)
ck('Queue67 retained exactly after handoff',info(G/cp['currentWorkQueue']['path'])==cp['currentWorkQueue'])
saved.write_bytes(Path(__file__).read_bytes());check.write_bytes(enc({'checkpoint':info(out),'checks':checks,'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'scope':'Exact source preparation, live notebook and handoff preservation; no review completion or game runtime proof.'}))
print(json.dumps({'checkpoint':info(out),'checkReport':info(check),'checks':len(checks),'failures':0,'queueUnchanged':cp['currentWorkQueue']}))
