import hashlib,json,subprocess,zipfile,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];D=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
PREP=D/'RANK9ILLUSIONREALITY5_SOURCE_PREPARATION_206.json'; PACKET=D/'rank9_illusionreality5_current_source_206_prepared/DD_Rank9_IllusionReality5_CurrentSource_206.zip'; REPORT=D/'RANK9ILLUSIONREALITY5_PACKET206_INDEPENDENT_VERIFICATION.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def check(rows,label,ok,detail=None):rows.append({'check':label,'passed':bool(ok),'detail':detail})
def main():
 prep=json.loads(PREP.read_text(encoding='utf-8-sig')); checks=[]
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
 remote=subprocess.check_output(['git','ls-remote','origin',f'refs/heads/{branch}'],cwd=ROOT,text=True).split()
 check(checks,'Preparation binds current pushed HEAD and intended branch',prep['sourceCommit']==head==remote[0] and branch==prep['sourceBranch'],{'head':head,'remote':remote[0],'branch':branch})
 assert prep['status']=='PASS' and prep['canonicalChanges'] is False and prep['accepted'] is False and prep['applied'] is False
 index=json.loads(subprocess.check_output(['git','cat-file','blob',f'HEAD:DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'],cwd=ROOT).decode('utf-8-sig'))
 check(checks,'Exact authority remains 798 reviewed / 50 pending / 0 accepted-unapplied',prep['sourceAuthority']=={'reviewedApplied':798,'pending':50,'acceptedUnapplied':0,'completeStandaloneProcedures':522,'scopedInterfaces':173} and index['authoredCounts']=={'reviewed':798,'pending':50} and index['representationCounts']['completeReviewedStandaloneProcedures']==522)
 ids=['supreme-illusion','mirrored-world','ethereal-disjunction','illusory-reality','soul-reflection']
 with zipfile.ZipFile(PACKET) as z:
  names=z.namelist(); assert z.testzip() is None and len(names)==len(set(names))
  manifest=json.loads(z.read('MANIFEST.json')); rows=manifest['members']; check(checks,'Packet manifest covers every unique ZIP member',len(names)==len(rows)+1 and manifest['pendingIds']==ids and manifest['sourceAuthority']==prep['sourceAuthority'])
  valid=True
  for row in rows:
   b=z.read(row['path']); valid &= len(b)==row['bytes'] and sha(b)==row['sha256'] and f'{zlib.crc32(b)&0xffffffff:08x}'==row['crc32']
  check(checks,'All archive entries match exact length, SHA-256 and CRC',valid,{'members':len(rows)})
  candidate=json.loads(z.read('CURRENT_SOURCE_CONFERENCE_CANDIDATE_206.json'))
  hist=json.loads(z.read('HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json'))
  notes=json.loads(z.read('NOTES/INDEPENDENT_CONFERENCE_206.json'))
  request=z.read('REQUEST_206.txt').decode()
  check(checks,'Exactly five current spells remain individually pending',candidate['currentPendingGroup']['spellIds']==ids and [r['spellId'] for r in candidate['records']]==ids and all(next(e for e in index['entries'] if e['id']==sid)['authoredStatus']=='pending-authored-procedure' for sid in ids))
  check(checks,'All 157 historical source members are preserved and refreshed from HEAD',len(candidate['historicalSourceBindings'])==len(candidate['sourceBindings'])==157 and candidate['currentSourceCommit']==head and candidate['sourceBindingRefresh']['allSourceBindingsRefreshed'] is True)
  source_ok=True
  for row in candidate['sourceBindings']:
   raw=subprocess.check_output(['git','cat-file','blob',f'HEAD:{row["path"]}'],cwd=ROOT)
   source_ok &= len(raw)==row['bytes'] and sha(raw)==row['sha256'] and row['gitBlobSHA1']==subprocess.check_output(['git','rev-parse',f'HEAD:{row["path"]}'],cwd=ROOT,text=True).strip()
   source_ok &= ('sources_current/'+row['path']) in names
  check(checks,'Every refreshed source binding equals committed Git bytes and is attached',source_ok,{'sources':157})
  old_archive=z.read('HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip')
  old_queue=json.loads(subprocess.check_output(['git','cat-file','blob',f'HEAD:docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_205.json'],cwd=ROOT).decode('utf-8-sig'))
  target=old_queue['nextPreparedRequest']['archive']
  check(checks,'Original source conference ZIP is byte-preserved',len(old_archive)==target['bytes'] and sha(old_archive)==target['sha256'])
  with zipfile.ZipFile(__import__('io').BytesIO(old_archive)) as oz:
   exact=True
   for row in hist['sourceBindings']:
    b=oz.read('sources/'+row['path']); exact &= len(b)==row['bytes'] and sha(b)==row['sha256']
  check(checks,'Historical candidate source proofs remain exact in original archive',exact,{'sourceCount':len(hist['sourceBindings'])})
  check(checks,'All 33 questions, 10 required cases, and five future case requirements remain',len(candidate['questions'])==31 and len(notes['focusedAdditionalQuestions'])==2 and len(notes['allQuestions'])==33 and len(notes['requiredNewCases'])==10 and len(notes['originalFutureCaseRequirementsUnchanged'])==5)
  check(checks,'Only the exact 5-identity scope is submitted; feats and completed 16 are excluded',all(sid in request for sid in ids) and 'Do not reopen feats, the completed 16' in request and 'exactly these five' in request)
  check(checks,'Newest applied Return205 context and retained Reverse Gravity blocker are attached',all(n.startswith('current/docs/audit/2026-10-08/full-game/director-spell-review-129/') for n in names if 'RETURN205' in n or 'APPLICATION_205' in n) and 'IE204-B02' in z.read('CURRENT_CONTEXT_206.json').decode() and 'reverse-gravity-field' in z.read('CURRENT_CONTEXT_206.json').decode())
 report={'id':'RANK9-ILLUSION-REALITY5-PACKET206-INDEPENDENT-VERIFICATION','recordedAtUtc':prep['recordedAtUtc'],'status':'PASS' if all(x['passed'] for x in checks) else 'FAIL','checksPassed':sum(x['passed'] for x in checks),'checksFailed':sum(not x['passed'] for x in checks),'checks':checks,'sourceCommit':head,'sourceAuthority':prep['sourceAuthority'],'packet':prep['packet'],'accepted':False,'applied':False}
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'status':report['status'],'checksPassed':report['checksPassed'],'checksFailed':report['checksFailed'],'packetBytes':PACKET.stat().st_size,'packetSha256':sha(PACKET.read_bytes()),'report':str(REPORT.relative_to(ROOT))},indent=2))
if __name__=='__main__':main()
