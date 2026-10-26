import copy, hashlib, json, subprocess, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
FULL=ROOT/'docs/audit/2026-10-08/full-game'; AUD=FULL/'director-spell-review-129'
PREP=FULL/'RANK9_PSYCHIC_FEAR7_SOURCE_CONFERENCE_02_PREPARATION_180.json'
CHECK=FULL/'RANK9_PSYCHIC_FEAR7_SOURCE_CONFERENCE_02_CHECK_180.json'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def source_bytes(rel):
 try: return subprocess.check_output(['git','cat-file','blob',f'HEAD:{rel}'],cwd=ROOT,stderr=subprocess.DEVNULL)
 except subprocess.CalledProcessError: return (ROOT/rel).read_bytes()
def main():
 prep=read(PREP); candidate_path=ROOT/prep['candidate']['path']; cand_raw=candidate_path.read_bytes(); c=json.loads(cand_raw); archive_path=ROOT/prep['archive']['path']; archive_raw=archive_path.read_bytes(); qpath=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_180.json'; hpath=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_180.json'; pending_path=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT93_PENDING_IDENTITY_AUDIT_180.json'; idx=read(INDEX); cat=read(CATALOG); q=read(qpath); h=read(hpath); pending=read(pending_path); checks=[]
 def ck(name,ok,details=None): checks.append({'check':name,'passed':bool(ok),'details':details}); assert ok,name
 ck('Preparation records the exact active branch and base commit',prep['sourceGitBranch']=='codex/ordinary-spell-review-complete' and prep['sourceGitCommit']==c['sourceGitCommit'])
 ck('Live authority agrees across current index/catalog-derived handoff, queue and packet',c['currentAuthority']['reviewedApplied']==q['currentAuthority']['reviewedApplied']==h['currentAuthority']['reviewedApplied']==755 and c['currentAuthority']['pending']==q['currentAuthority']['pending']==h['currentAuthority']['pending']==93 and c['currentAuthority']['acceptedUnapplied']==0)
 ids=['phantom-armageddon','phantom-cataclysm','psychic-scream','frightful-sovereignty','mass-phantom-killer','weird','reality-break']
 ck('Exact next seven identities match current queue and pending audit',q['nextGroup']=='rank9-psychic-fear7' and q['next']['group']=='rank9-psychic-fear7' and q['next']['pendingCount']==7 and c['currentPendingIds']==ids and set(ids)<=set(pending['pendingIds']))
 ck('Current pending count and exact index-derived pending set equal 93',len(pending['pendingIds'])==93 and pending['pendingCount']==93 and idx['authoredCounts']=={'reviewed':755,'pending':93} and {r['id'] for r in idx['entries'] if r.get('authoredStatus')=='pending-authored-procedure'}==set(pending['pendingIds']))
 ck('Archive size and digest match the recorded fresh packet',len(archive_raw)==prep['archive']['bytes'] and sha(archive_raw)==prep['archive']['sha256'])
 ck('Candidate file size and digest match the recorded source candidate',len(cand_raw)==prep['candidate']['bytes'] and sha(cand_raw)==prep['candidate']['sha256'])
 with zipfile.ZipFile(archive_path) as z:
  names=z.namelist(); manifest=read_from_bytes(z.read('MANIFEST.json'))
  ck('ZIP passes CRC test and contains no duplicate paths',z.testzip() is None and len(names)==len(set(names)))
  ck('ZIP member count matches the manifest',len(names)==manifest['memberCount']+1)
  ck('ZIP candidate exactly equals the prepared candidate',z.read('CANDIDATE.json')==cand_raw)
  ck('ZIP request exactly matches the submitted request file',z.read('REQUEST.txt')==(FULL/'RANK9_PSYCHIC_FEAR7_SOURCE_CONFERENCE_02_REQUEST_180.txt').read_bytes())
  source_rows=c['sourceBindings']; ck('Candidate and manifest enumerate all 94 current source bindings',len(source_rows)==94 and len(manifest['liveCurrentSourceBindings'])==94)
  all_sources=True
  for row in source_rows:
   b=source_bytes(row['path'])
   if len(b)!=row['bytes'] or sha(b)!=row['sha256'] or z.read(row['packetPath'])!=b: all_sources=False; break
  ck('Every current source binding is byte-exact in checkout and ZIP',all_sources)
  manifest_ok=all(row['path'] in names and len(z.read(row['path']))==row['bytes'] and sha(z.read(row['path']))==row['sha256'] for row in manifest['members'])
  ck('Manifest byte counts and hashes verify every package member',manifest_ok)
 ck('All 25 question dispositions remain open for the director',len(c['allQuestions'])==25 and len({r['id'] for r in c['allQuestions']})==25 and all(not x.get('decisionSelected') for x in c['allQuestions']))
 ck('Fourteen required new cases cover exactly two cases per each of seven spells',len(c['requiredNewCaseObligations'])==14 and {x['spellId'] for x in c['requiredNewCaseObligations']}==set(ids))
 ck('All seven cards remain pending in current index and match current catalog',all(next(r for r in c['records'] if r['spellId']==sid)['completeCurrentCatalogSourceAndAccess']==next(r for r in cat['spells'] if r['id']==sid) and next(r for r in c['records'] if r['spellId']==sid)['currentIndexEntry']==next(r for r in idx['entries'] if r['id']==sid) for sid in ids))
 ck('Latest Return177 exact acceptance and application validation are included',read(AUD/'RANK9_STORMCONTROL6_EXACT_ACCEPTANCE_177.json')['acceptedIds']==['cosmic-implosion','frozen-eternity','hellstorm','storm-of-vengeance','thunder-wrath','storm-cage'] and read(AUD/'RANK9_STORMCONTROL6_APPLICATION_VALIDATION_179.json')['status']=='PASS')
 ck('Canonical index remains byte-exact and Windows catalog CRLF normalizes exactly to GitHub blob',source_bytes(INDEX.relative_to(ROOT).as_posix())==INDEX.read_bytes() and CATALOG.read_bytes().replace(b'\r\n',b'\n')==source_bytes(CATALOG.relative_to(ROOT).as_posix()))
 ck('Static authoring packet makes no runtime, human-play, balance, cosmology or release claim',c['newRuleAdoptions']==c['runtimeTestsExecuted']==c['humanPlaytests']==c['cosmologyDecisions']==0 and c['wholeGameComplete'] is False)
 audit={'id':'RANK9-PSYCHIC-FEAR7-PACKET-INDEPENDENT-AUDIT-180','status':'PASS','reviewIds':ids,'authority':{'reviewedApplied':755,'pending':93,'acceptedUnapplied':0},'archive':{'path':prep['archive']['path'],'bytes':len(archive_raw),'sha256':sha(archive_raw),'memberCount':len(names)},'candidate':{'path':prep['candidate']['path'],'bytes':len(cand_raw),'sha256':sha(cand_raw)},'questionCount':len(c['allQuestions']),'requiredCaseCount':len(c['requiredNewCaseObligations']),'sourceBindingCount':len(c['sourceBindings']),'checkCount':len(checks),'checksFailed':0,'checks':checks}
 out=FULL/'RANK9_PSYCHIC_FEAR7_PACKET_INDEPENDENT_AUDIT_180.json'; out.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps({'status':audit['status'],'checkCount':len(checks),'auditPath':str(out),'archiveBytes':len(archive_raw),'sourceBindings':len(c['sourceBindings'])},indent=2))
def read_from_bytes(b): return json.loads(b.decode('utf-8-sig'))
if __name__=='__main__': main()
