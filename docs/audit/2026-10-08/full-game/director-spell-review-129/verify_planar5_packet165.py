from __future__ import annotations
import hashlib, json, zipfile
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
FULL=ROOT/'docs/audit/2026-10-08/full-game'
AUDIT=FULL/'director-spell-review-129'
ARCHIVE=FULL/'DD_Rank8_Planar_5_Source_Conference_02.zip'
CANDIDATE=ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_planar_5_source_conference_02.json'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
PREP=FULL/'RANK8_PLANAR_5_SOURCE_CONFERENCE_02_PREPARATION.json'
REPORT=AUDIT/'PLANAR5_PACKET_INDEPENDENT_VERIFICATION_165.json'
IDS=['demiplane','maze','planar-seal','seal-of-banishment','gloom-bind']
AUTH={'reviewedApplied':730,'pending':118,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':454,'scopedInterfaces':173}
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 prep=read(PREP); candidate=read(CANDIDATE); index=read(INDEX); catalog=read(CATALOG)
 pending=read(AUDIT/'CURRENT118_PENDING_IDENTITY_AUDIT_164.json')
 queue=read(AUDIT/'CURRENT_SPELL_QUEUE_165.json'); handoff=read(AUDIT/'CURRENT_HANDOFF_165.json')
 checks=[]
 def ck(name,ok):
  checks.append({'check':name,'passed':bool(ok)})
  if not ok: raise AssertionError(name)
 archive=ARCHIVE.read_bytes(); candraw=CANDIDATE.read_bytes()
 ck('Preparation is marked prepared-unsent',prep['status']=='PREPARED_UNSENT')
 ck('Archive bytes and SHA match preparation',len(archive)==prep['archive']['bytes'] and sha(archive)==prep['archive']['sha256'])
 ck('Candidate bytes and SHA match preparation',len(candraw)==prep['candidate']['bytes'] and sha(candraw)==prep['candidate']['sha256'])
 ck('Exact current authority is 730/118/0 with 454/173',prep['currentAuthority']==AUTH and candidate['currentAuthority']['reviewedApplied']==730 and candidate['currentAuthority']['pending']==118 and candidate['currentAuthority']['acceptedUnapplied']==0)
 ck('Exact five Planar5 IDs match queue head',candidate['currentPendingIds']==IDS and queue['currentPendingGroups'][0]['pendingIds']==IDS)
 ck('Live index and pending audit have the same 118 identities',len(pending['pendingIds'])==118 and {e['id'] for e in index['entries'] if e['authoredStatus']=='pending-authored-procedure'}==set(pending['pendingIds']))
 ck('All five IDs remain pending in the current index',all(next(e for e in index['entries'] if e['id']==sid)['authoredStatus']=='pending-authored-procedure' for sid in IDS))
 ck('All 24 questions remain unselected',len(candidate['questions'])==24 and all(q['decisionSelected'] is False for q in candidate['questions']))
 ck('Five records bind exact current catalog cards and index entries',len(candidate['records'])==5 and all(r['completeCurrentCatalogSourceAndAccess']==next(s for s in catalog['spells'] if s['id']==r['spellId']) and r['currentIndexEntry']==next(e for e in index['entries'] if e['id']==r['spellId']) for r in candidate['records']))
 ck('Current source binding inventory has 89 unique files',len(candidate['sourceBindings'])==89 and len({r['path'] for r in candidate['sourceBindings']})==89)
 with zipfile.ZipFile(ARCHIVE) as z:
  names=z.namelist(); ck('Archive CRC and member names are valid',z.testzip() is None and len(names)==prep['archiveMemberCount']==len(set(names)))
  ck('Archive candidate matches canonical packet candidate',z.read('CANDIDATE.json')==candraw)
  manifest=json.loads(z.read('MANIFEST.json'))
  ck('Manifest enumerates all 89 source bindings',len(manifest['currentSourceBindings'])==89)
  exact=True
  for row in manifest['currentSourceBindings']:
   raw=z.read('sources/'+row['path'])
   exact=exact and len(raw)==row['bytes'] and sha(raw)==row['sha256']
  ck('All 89 embedded current source files match their hashes',exact)
  ck('Conference01 is retained as byte-exact historical evidence',z.read('historical/Conference01_ARCHIVE.zip')==(FULL/'DD_Rank8_Planar_5_Source_Conference_01.zip').read_bytes())
  ck('Request and source check are included and passing',b'730 applied-reviewed / 118 pending' in z.read('REQUEST.txt') and json.loads(z.read('SOURCE_CHECK.json'))['failures']==0)
 ck('Queue and handoff state fresh packet prepared but unsent',queue['packetStatus']=='FRESH_PLANAR5_PACKET_PREPARED_UNSENT' and handoff['status']=='PLANAR5_FRESH_PACKET_PREPARED_UNSENT' and queue['currentAuthority']==handOffAuthority(handoff)==AUTH)
 ck('No rule, runtime, human-play, balance, cosmology or release approval claimed',candidate['newRuleAdoptions']==0 and candidate['runtimeTestsExecuted']==0 and candidate['humanPlaytests']==0 and candidate['wholeGameComplete'] is False)
 report={'id':'PLANAR5-PACKET-INDEPENDENT-VERIFICATION-165','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PASS','checkCount':len(checks),'failures':0,'checks':checks,'candidate':prep['candidate'],'archive':prep['archive'],'currentAuthority':AUTH,'reviewIds':IDS}
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'status':'PASS','checkCount':len(checks),'failures':0,'archiveBytes':len(archive),'archiveSha256':sha(archive),'report':REPORT.relative_to(ROOT).as_posix()},indent=2))
def handOffAuthority(h): return h['currentAuthority']
if __name__=='__main__':main()
