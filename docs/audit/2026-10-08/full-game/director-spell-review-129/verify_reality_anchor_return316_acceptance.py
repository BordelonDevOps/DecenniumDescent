from __future__ import annotations
import hashlib, json, zipfile, zlib
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
RECEIVED = BASE / 'rank9_wardcontrol6_reality_anchor_return316_received'
ARCHIVE = RECEIVED / 'DD_Rank9_WardControl6_Director_Return316_ACCEPTED.zip'
DELIVERY = RECEIVED / 'DD_Rank9_WardControl6_Director_Return316_ACCEPTED_DELIVERY.json'
OUT = BASE / 'REALITY_ANCHOR_RETURN316_INDEPENDENT_AUDIT.json'
INDEX = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
QUEUE = BASE / 'CURRENT_SPELL_QUEUE_316.json'
HANDOFF = BASE / 'CURRENT_HANDOFF_316.json'
PENDING = BASE / 'CURRENT26_PENDING_IDENTITY_AUDIT_316.json'
PACKET = BASE / 'rank9_wardcontrol6_reality_anchor_packet_316_prepared_build04/DD_Rank9_WardControl6_RealityAnchor_316.zip'
PACKET_DELIVERY = BASE / 'rank9_wardcontrol6_reality_anchor_packet_316_prepared_build04/DD_Rank9_WardControl6_RealityAnchor_316_DELIVERY.json'

assert not OUT.exists(), f'Refusing to overwrite {OUT}'
checks=[]
def ck(name, ok, details=None):
    checks.append({'name':name,'status':'PASS' if bool(ok) else 'FAIL','details':details or {}})
    if not ok: raise AssertionError(checks[-1])
def sha(b): return hashlib.sha256(b).hexdigest()
def bind(b): return {'bytes':len(b),'sha256':sha(b),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
def readj(raw): return json.loads(raw)
archive_raw=ARCHIVE.read_bytes(); delivery_raw=DELIVERY.read_bytes(); d=readj(delivery_raw)
ck('archive-binding', bind(archive_raw)=={k:d['archive'][k] for k in ['bytes','sha256','crc32']}, bind(archive_raw))
ck('delivery-authority-before',d['authority']=={'reviewedApplied':822,'pending':26,'acceptedUnapplied':0,'completeStandaloneProcedures':546,'scopedInterfaces':173})
ck('canonical-authority-unchanged',d['canonicalAuthorityUnchanged']==d['authority'])
ck('accepted-applied-held-scope',d['acceptedIds']==['reality-anchor'] and d['appliedIds']==[] and d['heldIds']==[])
ck('projected-authority',d['projectedAuthorityAfterIndependentApplication']=={'reviewedApplied':823,'pending':25,'acceptedUnapplied':0,'completeStandaloneProcedures':547,'scopedInterfaces':173})
ck('next-priority',d['nextPendingGroup']=='rank9-time-fate6' and d['nextPendingIdentity']=='time-stop' and d['nextBlockerId']=='TF192-B01' and d['remainingClosureTasks']==25)
ck('semantic-scope',d['semanticStatus']=='PASS_FOR_STATIC_AUTHORED_SCOPE' and d['canonicalFilesChanged'] is False and d['applicationPerformed'] is False)
with zipfile.ZipFile(ARCHIVE) as z:
    names=z.namelist(); ck('zip-crc',z.testzip() is None); ck('unique-members',len(names)==len(set(names))==d['archive']['memberCount'])
    ck('safe-members',all(not n.startswith('/') and '..' not in PurePosixPath(n).parts and '\\' not in n for n in names))
    manifest=readj(z.read('MEMBER_MANIFEST.json'))
    rows=manifest.get('members',manifest.get('files',[]))
    ck('manifest-complete',len(rows)==len(names)-1 and {r['path'] for r in rows}==set(names)-{'MEMBER_MANIFEST.json'})
    for r in rows:
        raw=z.read(r['path']); actual=bind(raw)
        for key in ('bytes','sha256','crc32'):
            ck('member:'+r['path']+':'+key,actual[key]==r.get(key))
    decision=readj(z.read('DIRECTOR_DECISION.json'))
    acceptance=readj(z.read('EXACT_ACCEPTANCE.json'))
    proc_raw=z.read('procedures/reality-anchor.json'); proc=readj(proc_raw)
    witness_raw=z.read('witness/REALITY_ANCHOR_WITNESS_SUPPLEMENT_316.json')
    counts=readj(z.read('COUNTS.json'))
    ck('director-decision',decision['decision']=='ACCEPT' and decision['acceptedIds']==['reality-anchor'] and decision['appliedIds']==[] and decision['heldIds']==[] and decision['decisions'][0]['closedBlockerIds']==['WC188-B02'])
    ck('director-no-side-effects',decision['canonicalFilesChanged'] is False and decision['applicationPerformed'] is False and decision['githubChanges'] is False and decision['sourceProgramsExecuted'] is False and decision['runtimeExecuted'] is False)
    ck('exact-acceptance',acceptance['accepted'] is True and acceptance['applied'] is False and acceptance['acceptedIds']==['reality-anchor'] and acceptance['appliedIds']==[] and acceptance['heldIds']==[] and acceptance['closedBlockerIds']==['WC188-B02'] and acceptance['remainingBlockerIds']==[] and acceptance['sourceStatusPromotionAuthorized'] is False)
    ck('accepted-procedure-binding',bind(proc_raw)=={k:acceptance['acceptedProcedure'][k] for k in ['bytes','sha256','crc32']} and proc['spellId']=='reality-anchor' and proc['accepted'] is True and proc['applied'] is False)
    ck('accepted-witness-binding',bind(witness_raw)=={k:acceptance['acceptedIntegratedWitness'][k] for k in ['bytes','sha256','crc32']})
    ck('one-identity-only',decision['scopeIds']==['reality-anchor'] and acceptance['otherIdentityAccepted'] is False and counts['acceptedCount']==1 and counts['appliedCount']==0 and counts['heldCountInScope']==0)
    ck('semantic-counts',counts['dataChecks']==11536 and counts['dataFailures']==0 and counts['semanticChecks']==1029 and counts['semanticFailures']==0 and counts['combinedDataSemanticChecks']==12565)
    ck('event-replay-counts',counts['newIntegratedBranches']==2 and counts['newEvents']==55 and counts['newForwardOperations']==663 and counts['newInverseOperations']==663 and counts['closedCorrectionCount']==5)
    pending=readj(z.read('REMAINING_QUEUE.json'))
    ck('remaining-pending-excludes-accepted',pending['decisionLedger']['acceptedUnapplied']==1 and pending['remainingClosureTaskCount']==25 and pending['nextIdentity']=='time-stop' and pending['nextBlocker']=='TF192-B01')
    ck('wave-hold-preserved','nullification-wave' in pending['remainingHeldPendingIds'])
    idx_raw=z.read('authority/authored_review_index.json'); cat_raw=z.read('authority/catalog.json')
    ck('index-byte-exact-current',idx_raw==INDEX.read_bytes())
    ck('catalog-byte-exact-current',cat_raw==CATALOG.read_bytes())
    index=readj(idx_raw); catalog=readj(cat_raw)
    row=next(x for x in index['entries'] if x['id']=='reality-anchor')
    ck('pre-application-row-pending',row['authoredStatus']=='pending-authored-procedure' and row['sourceStatus']=='blocked-pending-operational-review')
    ck('pre-application-authority',index['authoredCounts']=={'reviewed':822,'pending':26} and index['representationCounts']['completeReviewedStandaloneProcedures']==546)
    card=next(x for x in catalog['spells'] if x['id']=='reality-anchor')
    ck('native-card-preserved',proc['nativeCardUnchanged']==card)
    ck('procedure-static-only',acceptance['acceptedScope']['kind']=='static-authored-procedure' and acceptance['runtimeSelectionEnabled'] is False and acceptance['sourceStatusPromotionAuthorized'] is False)
    ck('local-queue-binding',z.read('authority/CURRENT_SPELL_QUEUE_316.json')==QUEUE.read_bytes() and z.read('authority/CURRENT_HANDOFF_316.json')==HANDOFF.read_bytes() and z.read('authority/CURRENT26_PENDING_IDENTITY_AUDIT_316.json')==PENDING.read_bytes())
    packet_raw=PACKET.read_bytes(); packet_delivery_raw=PACKET_DELIVERY.read_bytes()
    source=d['sourceArchive']
    ck('submitted-packet-binding',bind(packet_raw)=={k:source[k] for k in ['bytes','sha256','crc32']})
    incoming_manifest=next(r for r in d['members'] if r['path']=='input/DD_Rank9_WardControl6_RealityAnchor_316_DELIVERY.json')
    ck('submitted-packet-delivery-binding',bind(packet_delivery_raw)=={k:incoming_manifest[k] for k in ['bytes','sha256','crc32']})

report={
 'id':'REALITY-ANCHOR-RETURN316-INDEPENDENT-AUDIT','recordedAtUtc':'2026-10-31T05:30:00Z','status':'PASS_STATIC_AUTHORED_SCOPE','archive':{'path':ARCHIVE.relative_to(ROOT).as_posix(),**bind(archive_raw)},
 'delivery':{'path':DELIVERY.relative_to(ROOT).as_posix(),**bind(delivery_raw)},'checkCount':len(checks),'passedChecks':len(checks),'failedChecks':0,'checks':checks,
 'acceptedIds':['reality-anchor'],'appliedIds':[],'heldIds':[],'closedBlockerIds':['WC188-B02'],'authorityBefore':d['authority'],'projectedAuthorityAfterApplication':d['projectedAuthorityAfterIndependentApplication'],
 'semanticStatus':'PASS_FOR_STATIC_AUTHORED_SCOPE','runtimeSelectionEnabled':False,'sourceStatusPromotionAuthorized':False,'canonicalFilesChanged':False,'applicationPerformed':False}
OUT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(OUT)
print(json.dumps({'status':report['status'],'checks':report['checkCount'],'archiveSha256':report['archive']['sha256'],'acceptance':report['acceptedIds'],'authority':report['authorityBefore'],'projected':report['projectedAuthorityAfterApplication']},indent=2))
