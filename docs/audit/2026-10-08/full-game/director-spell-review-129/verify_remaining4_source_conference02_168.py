from __future__ import annotations
import hashlib,json,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[5];FULL=ROOT/'docs/audit/2026-10-08/full-game';AUDIT=FULL/'director-spell-review-129'
ARCHIVE=FULL/'DD_Rank8_Remaining_4_Source_Conference_02.zip';CANDIDATE=ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_remaining_4_source_conference_02.json'
OUTPUT=FULL/'rank8-remaining4-source-conference-02-168';CHECK=FULL/'RANK8_REMAINING_4_SOURCE_CONFERENCE_02_CHECK.json';PREP=FULL/'RANK8_REMAINING_4_SOURCE_CONFERENCE_02_PREPARATION.json';REQUEST=FULL/'RANK8_REMAINING_4_SOURCE_CONFERENCE_02_REQUEST.txt'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json';CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
OLD_ARCHIVE=FULL/'DD_Rank8_Remaining_4_Source_Conference_01.zip';OLD_PREP=FULL/'RANK8_REMAINING_4_SOURCE_CONFERENCE_01_PREPARATION.json'
QUEUE_BEFORE=AUDIT/'CURRENT_SPELL_QUEUE_167.json';HANDOFF_BEFORE=AUDIT/'CURRENT_HANDOFF_167.json';PENDING=AUDIT/'CURRENT113_PENDING_IDENTITY_AUDIT_167.json';QUEUE=AUDIT/'CURRENT_SPELL_QUEUE_168.json';HANDOFF=AUDIT/'CURRENT_HANDOFF_168.json'
REPORT=AUDIT/'RANK8_REMAINING_4_SOURCE_CONFERENCE_02_VERIFICATION_168.json'
IDS=['prismatic-wall','faction-convergence','divine-intervention-lesser','reality-patch'];AUTH={'reviewedApplied':735,'pending':113,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':459,'scopedInterfaces':173}
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def chk(checks,n,ok):checks.append({'check':n,'passed':bool(ok)})
def main():
 checks=[];fail=[];raw=ARCHIVE.read_bytes();candraw=CANDIDATE.read_bytes();prep=read(PREP);check_doc=read(CHECK);candidate=read(CANDIDATE);index=read(INDEX);catalog=read(CATALOG);pending=read(PENDING);queue=read(QUEUE);handoff=read(HANDOFF)
 chk(checks,'Fresh packet preparation binds exact candidate bytes and archive bytes',len(candraw)==prep['candidate']['bytes'] and sha(candraw)==prep['candidate']['sha256'] and len(raw)==prep['archive']['bytes'] and sha(raw)==prep['archive']['sha256'])
 chk(checks,'Candidate identity, authority and exact four IDs are current',candidate['id']=='RANK8-REMAINING4-SOURCE-CONFERENCE02-168' and candidate['countsUnchanged']=={'reviewed':735,'pending':113,'acceptedUnapplied':0} and candidate['currentPendingIds']==IDS and candidate['currentAuthority']['reviewedApplied']==735 and candidate['currentAuthority']['pending']==113)
 chk(checks,'Current live authority and pending identity audit equal 735/113/0',index['authoredCounts']=={'reviewed':735,'pending':113} and len(pending['pendingIds'])==113 and pending['indexBinding']['sha256']==sha(INDEX.read_bytes()))
 chk(checks,'All 22 source questions are preserved exactly and remain unselected',len(candidate['questions'])==22 and all(q['decisionSelected'] is False for q in candidate['questions']) and candidate['questions']==read(OUTPUT/'historical/Conference01_CANDIDATE.json')['questions'])
 chk(checks,'Only four current pending identities are in this packet and bind live records',len(candidate['records'])==4 and [r['spellId'] for r in candidate['records']]==IDS and all(next(r for r in index['entries'] if r['id']==x)['authoredStatus']=='pending-authored-procedure' for x in IDS))
 chk(checks,'Queue and handoff show the exact freshly prepared next group',queue['currentAuthority']==handoff['currentAuthority']==AUTH and queue['nextGroup']=='rank8-remaining4' and queue['currentPendingGroups'][0]['pendingIds']==IDS and queue['packetStatus']=='FRESH_REMAINING4_PACKET_PREPARED_UNSENT' and handoff['status']=='REMAINING4_FRESH_PACKET_PREPARED_UNSENT')
 chk(checks,'Packet check reports zero failures and all listed checks pass',check_doc['failures']==0 and len(check_doc['checks'])==10 and all(c['passed'] for c in check_doc['checks']))
 with zipfile.ZipFile(ARCHIVE) as z:
  names=z.namelist();chk(checks,'Packet ZIP CRC passes with 124 unique members',z.testzip() is None and len(names)==len(set(names))==124==prep['archiveMemberCount'])
  chk(checks,'Candidate, request and source check match local packet deliverables',z.read('CANDIDATE.json')==candraw and z.read('REQUEST.txt')==REQUEST.read_bytes() and json.loads(z.read('SOURCE_CHECK.json'))['failures']==0)
  m=json.loads(z.read('MANIFEST.json'));rows=m['currentSourceBindings'];chk(checks,'Packet manifest enumerates 113 unique current source bindings',len(rows)==113 and len({r['path'] for r in rows})==113)
  all_source=True
  for r in rows:
   b=z.read('sources/'+r['path']);p=ROOT/r['path'];all_source &= len(b)==r['bytes'] and sha(b)==r['sha256'] and p.is_file() and p.read_bytes()==b
  chk(checks,'All 113 source members match both the manifest and current local files',all_source)
  chk(checks,'Historical Conference01 archive and candidate are byte-exact',z.read('historical/Conference01_ARCHIVE.zip')==OLD_ARCHIVE.read_bytes() and z.read('historical/Conference01_CANDIDATE.json')==(OUTPUT/'historical/Conference01_CANDIDATE.json').read_bytes())
  chk(checks,'No new global rules, runtime, human playtests or release states are adopted',candidate['newRuleAdoptions']==candidate['runtimeTestsExecuted']==candidate['humanPlaytests']==0 and candidate['wholeGameComplete'] is False)
  chk(checks,'Prior accepted/applied cohorts remain outside this review scope',candidate['nonAcceptanceOfLaterSourceChanges'].find('prior accepted/applied spell cohorts remain closed')>=0)
  chk(checks,'Packet source check authority, request and prep all identify this exact group',json.loads(z.read('SOURCE_CHECK.json'))['currentAuthority']==AUTH and json.loads(z.read('SOURCE_CHECK.json'))['reviewIds']==IDS and prep['reviewIds']==IDS and prep['questionCount']==22 and prep['sourceBindingCount']==113)
  chk(checks,'Old Conference01 archive remains CRC-valid and its prep hash matches',zipfile.ZipFile(OLD_ARCHIVE).testzip() is None and sha(OLD_ARCHIVE.read_bytes())==read(OLD_PREP)['archive']['sha256'])
 for c in checks:
  if not c['passed']:fail.append(c['check'])
 report={'id':'RANK8-REMAINING4-SOURCE-CONFERENCE02-VERIFICATION-168','status':'PASS' if not fail else 'FAIL','recordedAtUtc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'checkCount':len(checks),'checksPassed':len(checks)-len(fail),'failures':len(fail),'failedChecks':fail,'checks':checks,'reviewIds':IDS,'currentAuthority':AUTH,'candidate':{'path':CANDIDATE.relative_to(ROOT).as_posix(),'bytes':len(candraw),'sha256':sha(candraw)},'archive':{'path':ARCHIVE.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':sha(raw),'members':124},'sourceBindingCount':113}
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'status':report['status'],'checkCount':len(checks),'checksPassed':report['checksPassed'],'failures':len(fail),'failedChecks':fail,'report':REPORT.relative_to(ROOT).as_posix()},indent=2))
 if fail:raise SystemExit(2)
 # Bind the independent result into the prepared queue and handoff after it has passed.
 q=read(QUEUE);h=read(HANDOFF);bind={'path':REPORT.relative_to(ROOT).as_posix(),'bytes':REPORT.stat().st_size,'sha256':sha(REPORT.read_bytes())}
 q['sourceConferencePrepared']['verification']=bind;q['nextPreparedRequest']=q['sourceConferencePrepared'];QUEUE.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 h=read(HANDOFF);h['nextPreparedRequest']=q['sourceConferencePrepared'];h['directorSubmission']['verification']=bind
 h['currentQueueBinding']={'path':QUEUE.relative_to(ROOT).as_posix(),'bytes':QUEUE.stat().st_size,'sha256':sha(QUEUE.read_bytes())};HANDOFF.write_text(json.dumps(h,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
