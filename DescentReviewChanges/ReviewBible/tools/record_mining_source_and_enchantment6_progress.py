"""One-time preservation/navigation update; no operational content promotion."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

GAME = Path(r'C:\Github\DecenniumDescent')
ROOT = GAME / 'DescentReviewChanges/ReviewBible'
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p, obj): p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
now = datetime.now(timezone.utc).isoformat()
covpath = AUDIT/'FOCUSED_SPELL_SOURCE_PREPARATION_COVERAGE.json'
cov = read(covpath)
assert cov['distinctPreparedPendingSpellIds'] == 279
newfile = 'ENCHANTMENT_RANK6_SOURCE_PREPARATION.json'
assert newfile not in cov['cohortFiles']
files = cov['cohortFiles'] + [newfile]
rows = [read(AUDIT/f) for f in files]
ids = [s['spellId'] for d in rows for s in d['selectedSpells']]
assert len(ids) == len(set(ids)) == 287
assert all(c['pass'] for d in rows for c in d['checks'])
protected = {}
for d in rows:
    for name, digest in d['protectedFiles'].items():
        assert name not in protected or protected[name] == digest, name
        protected[name] = digest
for name, digest in protected.items(): assert sha(GAME/name) == digest, name
status = read(AUDIT/'ENCHANTMENT_RANK6_SOURCE_STATUS.json')
assert sha(AUDIT/status['packetFile']) == status['packetSha256']
assert status['counts']['currentBookBindingsIncludingThisCohort'] == 301
assert status['counts']['prePushPreparedSpellQuestionsIncludingThisCohort'] == 274
newids = {s['spellId'] for s in rows[-1]['selectedSpells']}
assert newids <= set(cov['remainingUnpreparedSpellIds'])
assert all(min(a['rank'] for a in s['fullSourceAndCurrentAccessRecord']['classAccess'].values()) == 6 for s in rows[-1]['selectedSpells'])
mining = read(AUDIT/'MINING_SOURCE_CONFERENCE_CAPTURE.json')
assert sha(AUDIT/mining['file']) == mining['sha256']
assert mining['recipesApproved'] == 0
payload = AUDIT/'CODEX_GATHERING_TOOL_PART2_C_SKINNING.txt'
assert sha(payload) == 'a37403e13b5d0baece9071009588e9c0cb61af4456c50d96361f309a74558342'
paths = [GAME/'START_HERE.md', covpath, AUDIT/'PREPARED_SPELL_SOURCE_INDEX.md', AUDIT/'GPT_REVIEW_CONTINUATION_HANDOFF.md', AUDIT/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json', ROOT/'data/playtest/game_development_coverage.json', AUDIT/'GATHERING_TOOL_PART2_DISPATCH.json']
backup = AUDIT/'navigation-before-mining-source-and-enchantment6'
assert not backup.exists()
backup.mkdir()
manifest = {}
for p in paths:
    shutil.copyfile(p, backup/p.name)
    manifest[str(p.relative_to(GAME)).replace('\\','/')] = sha(p)
write(backup/'MANIFEST.json', manifest)

cov.update(cohortFiles=files, distinctPreparedPendingSpellIds=287, currentBookBindings=301, prePushMechanicalQuestions=274, protectedInputsUnchanged=len(protected), minimumRank6SourceIdentitiesPrepared=16, remainingUnpreparedIdentities=285)
cov['remainingUnpreparedSpellIds'] = sorted(set(cov['remainingUnpreparedSpellIds'])-newids)
cov['remainingUnpreparedByMinimumClassRank']['6'] = 46
cov['postPushReceiptOnlyIds'].append('soul-cage')
write(covpath,cov)

dispatch = read(paths[-1])
dispatch['status'] = 'Mining source verdict captured; complete Skinning Part C dispatched; actual new user turn awaiting connector visibility'
dispatch['parts']['B_SHARED_AND_MINING'].update(actualReplyId=mining['replyId'], verdictPending=False, verdictFile=mining['file'], captureFile='MINING_SOURCE_CONFERENCE_CAPTURE.json', verdictSha256=mining['sha256'])
dispatch['parts']['C_SKINNING'] = {'file':payload.name,'sha256':sha(payload),'characters':len(payload.read_text(encoding='utf-8')),'dispatchTool':'mcp__codex_app__send_message_to_thread','dispatchSucceeded':True,'actualTurnId':None,'actualReplyId':None,'verdictPending':True,'firstObservation':'GATHERING_TOOL_PART2_C_FIRST_OBSERVATION.json','observedThreadStatus':'active','firstObservationStillShowsCompletedPriorMiningTurn':True}
write(paths[-1],dispatch)

p=GAME/'START_HERE.md';s=p.read_text(encoding='utf-8')
s=s.replace('current rules acknowledged; all43 Mining sources sent for a verdict; Skinning and Salvaging follow.', 'current rules acknowledged; the complete [Mining source verdict](docs/audit/2026-10-08/full-game/GPT_MINING_SOURCE_CONFERENCE.md) is preserved; all43 Skinning sources are sent for review, followed by Salvaging. No gathering-tool cards are approved yet.')
s=s.replace('twenty-one unsent cohorts, 279 identities, 290 book bindings, 267 mechanical questions and twelve unchanged post-push receipts.', 'twenty-two unsent cohorts, 287 identities, 301 book bindings, 274 mechanical questions and thirteen unchanged post-push receipts.')
p.write_text(s,encoding='utf-8')

p=AUDIT/'PREPARED_SPELL_SOURCE_INDEX.md';s=p.read_text(encoding='utf-8')
s=s.replace('Twenty-one packets','Twenty-two packets').replace('retain279 distinct unfinished identities and290 exact current-book placements:267 mechanical questions and12 unchanged post-push receipts.','retain287 distinct unfinished identities and301 exact current-book placements:274 mechanical questions and13 unchanged post-push receipts.')
line='| [Rank-six Evocation](EVOCATION_RANK6_SOURCE_AUDIT.md) | 8 | 8 | 0 | 9 | 11 |'
s=s.replace(line,line+'\n| [Rank-six Enchantment](ENCHANTMENT_RANK6_SOURCE_AUDIT.md) | 8 | 7 | 1 | 11 | 11 |')
s=s.replace('Eight rank6 Evocation identities are also prepared;293 higher-rank identities remain.','Sixteen rank6 Evocation/Enchantment identities are also prepared;285 higher-rank identities remain.')
s=s.replace('commune, alignment-scrying, planar-gate.','commune, alignment-scrying, planar-gate, soul-cage.')
s=s.replace('| 6 | 54 |','| 6 | 46 |')
s=s.replace('Mining Part B is awaiting its verdict.','the Mining verdict is preserved and all43 Skinning sources have been sent.')
s += '\nRank-six Enchantment preserves both Mental Prison placements, the conflicting Mass Suggestion durations and the missing Willbreaker duration. Both Soul Cage versions remain unchanged post-push receipts; no soul mechanics or cosmology were reviewed.\n'
p.write_text(s,encoding='utf-8')

p=AUDIT/'GPT_REVIEW_CONTINUATION_HANDOFF.md';s=p.read_text(encoding='utf-8')
s=s.replace('Mining Part B is awaiting its verdict, followed by Skinning and Salvaging.','the [Mining verdict](GPT_MINING_SOURCE_CONFERENCE.md) is captured, all43 Skinning sources are sent, and Salvaging follows.')
s=s.replace('### Current prepared spell coverage — twenty-one cohorts','### Historical prepared spell checkpoint — twenty-one cohorts')
s += '\n### Current checkpoint — Mining source verdict and twenty-two prepared spell cohorts\n\nMining turn `'+mining['turnId']+'`, reply `'+mining['replyId']+'` supplied GT-M01–18 source-authoring directions. The [full verdict](GPT_MINING_SOURCE_CONFERENCE.md) and [capture evidence](MINING_SOURCE_CONFERENCE_CAPTURE.json) are preserved. No gathering cards are approved. Part C contains all43 Skinning originals and is dispatched once; Part D Salvaging follows its completed verdict. Reconcile all three before exact operational authorship.\n\nThe [source index](PREPARED_SPELL_SOURCE_INDEX.md) now covers287 identities and301 book bindings:274 mechanical questions and13 unchanged post-push receipts. All pending minimum-rank0–5 identities and16 at rank6 are prepared;285 remain unprepared,including46 at rank6. Enchantment retains both Mental Prison/Mass Suggestion school versions and both Soul Cage originals; Soul Cage is deferred. All22 spell packets remain unsent; ordinary totals remain276 operational/572 pending.\n'
p.write_text(s,encoding='utf-8')

p=AUDIT/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json';o=read(p)
o['observedAtUtc']=now
o['latestCompletedSourceConference']={'turnId':mining['turnId'],'replyId':mining['replyId'],'file':mining['file'],'captureEvidence':'MINING_SOURCE_CONFERENCE_CAPTURE.json','scope':'GT-M01..18 source-authoring direction only; zero exact approvals'}
o['currentRequest'].update(scope='Skinning43 source/interface review; Mining verdict captured; Salvaging42 follows',partsSentOnce=['A_CURRENT_RULES','B_SHARED_AND_MINING','C_SKINNING'],actualLastObservedTurn=mining['turnId'],actualNewUserTurnPendingConnectorVisibility=True,notebookStatusAsObserved='active')
o['gatheringSourceConference'].update(stage='Mining source verdict captured; Skinning Part C dispatched',miningReplyId=mining['replyId'],miningVerdictFile=mining['file'],partCActualTurnId=None)
o['nextAction']='Capture the actual completed Skinning verdict for Part C, then submit prepared Salvaging Part D once. Reconcile all three source verdicts before authoring exact cards and separate exact review. Final whole-game review precedes push, remote verification and cosmology.'
o['currentGoalTurnClassification']='progress:Mining GT-M01..18 captured;43 Skinning sources dispatched;Enchantment rank6 sources registered'
o['independentProgress'].update(focusedPendingSpellSourcesPrepared=287,preparedSpellCohorts=22,currentBookBindingsAcrossPreparedSpellPackets=301,prePushSpellQuestionsAcrossPreparedPackets=274,postPushSpellReceipts=cov['postPushReceiptOnlyIds'],higherRankUnpreparedSpellIdentities=285,rank6SourcesPrepared=16,enchantmentRank6SourcesPrepared=8)
o['independentProgressUpdatedAtUtc']=now
write(p,o)

p=ROOT/'data/playtest/game_development_coverage.json';g=read(p);a=next(x for x in g['aspects'] if x['id']=='DD-12')
prefix='docs/audit/2026-10-08/full-game/'
a['sourceEvidence'].append(prefix+newfile)
a['validationEvidence'].append(prefix+'ENCHANTMENT_RANK6_SOURCE_STATUS.json')
a['currentPreparedSpellSourceCoverage'].update(identities=287,bookBindings=301,mechanicalQuestions=274,deferredReceipts=cov['postPushReceiptOnlyIds'],higherRankSourcesUnprepared=285,rank6SourcesPrepared=16)
write(p,g)
for name,digest in protected.items(): assert sha(GAME/name)==digest,name
receipt={'status':'PASS source preservation and navigation','cohorts':22,'identities':287,'bookBindings':301,'questions':274,'deferredReceipts':13,'protectedInputsUnchanged':len(protected),'remainingUnprepared':285,'rank6Prepared':16,'rank6Remaining':46,'backup':str(backup.relative_to(GAME)).replace('\\','/'),'miningVerdictSha256':mining['sha256'],'skinningDispatchedOnce':True,'sourceInformationDeleted':0,'newApprovals':0,'cosmology':'post-verified-push only'}
write(AUDIT/'MINING_SOURCE_AND_ENCHANTMENT6_PROGRESS.json',receipt)
print(json.dumps(receipt,ensure_ascii=False))
