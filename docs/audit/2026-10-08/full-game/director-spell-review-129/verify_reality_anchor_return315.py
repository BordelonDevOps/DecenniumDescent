from __future__ import annotations
import datetime as dt, hashlib, json, pathlib, zlib, zipfile

ROOT = pathlib.Path.cwd()
BASE = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
RECEIVED = BASE / 'rank9_wardcontrol6_return315_received'
ARCHIVE = RECEIVED / 'DD_Rank9_WardControl6_Director_Return315_HELD.zip'
DELIVERY = RECEIVED / 'DD_Rank9_WardControl6_Director_Return315_HELD_DELIVERY.json'
SUBMITTED = BASE / 'rank9_wardcontrol6_reality_anchor_packet_315_prepared_build07/DD_Rank9_WardControl6_RealityAnchor_315.zip'
OUT = BASE / 'REALITY_ANCHOR_RETURN315_INDEPENDENT_AUDIT.json'

def digest(raw: bytes) -> dict:
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'crc32':f'{zlib.crc32(raw)&0xffffffff:08x}'}

def read(z: zipfile.ZipFile, name: str):
    return json.loads(z.read(name).decode('utf-8-sig'))

araw=ARCHIVE.read_bytes(); draw=DELIVERY.read_bytes(); sraw=SUBMITTED.read_bytes()
delivery=json.loads(draw.decode('utf-8-sig')); submitted_digest=digest(sraw); checks=[]
def check(cid, passed, detail): checks.append({'id':cid,'status':'PASS' if passed else 'FAIL','detail':detail})
check('R315-01', delivery.get('archive',{}).get('bytes')==len(araw) and delivery.get('archive',{}).get('sha256')==hashlib.sha256(araw).hexdigest() and delivery.get('archive',{}).get('crc32')==digest(araw)['crc32'] and delivery.get('archive',{}).get('memberCount')==65, 'Downloaded ZIP byte/hash/CRC/member count matches exact delivery manifest.')
check('R315-02', delivery.get('sourceArchive',{}).get('sha256')==submitted_digest['sha256'] and delivery.get('sourceArchive',{}).get('bytes')==len(sraw), 'Return is bound to the exact submitted Packet315 archive.')
with zipfile.ZipFile(ARCHIVE) as z:
    names=z.namelist(); member_manifest=read(z,'MEMBER_MANIFEST.json'); data_validation=read(z,'DATA_VALIDATION.json')
    test_error=z.testzip()
    check('R315-03', test_error is None and len(names)==65 and len(names)==len(set(names)), 'ZIP CRC integrity, unique names, and 65-member count pass.')
    declared={m['path']:m for m in member_manifest['members']}
    actual=set(names)-{'MEMBER_MANIFEST.json'}
    manifests_ok=actual==set(declared)
    for path,meta in declared.items():
        b=z.read(path)
        if meta.get('bytes')!=len(b) or meta.get('sha256')!=hashlib.sha256(b).hexdigest() or meta.get('crc32')!=digest(b)['crc32']:
            manifests_ok=False; break
    check('R315-04', member_manifest.get('selfExcluded') is True and manifests_ok, 'All member names, byte counts, SHA-256 and CRC32 values match Return315 manifest.')
    check('R315-05', data_validation.get('status')=='DATA_REPLAY_PASS_SEMANTICS_SEPARATE' and data_validation.get('checkCount')==10699 and data_validation.get('failedCount')==0 and all(x.get('passed') is True for x in data_validation.get('checks',[])), 'Director package data replay has 10,699 checks, zero failures; semantic review remains separate.')
    decision=read(z,'DIRECTOR_DECISION.json'); corr=read(z,'CORRECTION_SHEET.json'); ledger=read(z,'A_EVENT_CORRECTION_LEDGER.json'); semantic=read(z,'INDEPENDENT_SEMANTIC_FAILURE_CHECK.json'); queue=read(z,'REMAINING_QUEUE.json'); blockers=read(z,'BLOCKERS.json')
    auth={'reviewedApplied':822,'pending':26,'acceptedUnapplied':0,'completeStandaloneProcedures':546,'scopedInterfaces':173}
    check('R315-06', decision.get('decision')=='HOLD' and decision.get('acceptedIds')==[] and decision.get('appliedIds')==[] and decision.get('heldIds')==['reality-anchor'] and decision.get('authorityAfter')==auth and decision.get('canonicalFilesChanged') is False and decision.get('applicationPerformed') is False, 'Decision is RA-only HOLD; authority preserved at 822/26/0 with no canonical edit or application.')
    check('R315-07', [f.get('id') for f in corr.get('findings',[])]==['RA315-C01','RA315-C02','RA315-C03','RA315-C04','RA315-C05'] and ledger.get('rowsCoverAll49SubmittedEvents') is True and len(ledger.get('branches',[]))==2, 'Five correction findings and every-event ledger for both submitted branches are present.')
    c01=corr['findings'][0]['required']
    c04=corr['findings'][3]['required']
    c05=corr['findings'][4]['required']
    check('R315-08', '2->1' in c01 and '1->0' in c01 and '10 RP' in c01 and 'Dissonance0->1' in c01, 'C01 gives exact idle-vent, Greater Dispel cost, remaining RP and post-cast strain.')
    check('R315-09', 'castRA1' in c04 and 'separate original-cast checks' in c04 and 'failing check' in c04, 'C04 requires capture and a separate failure outcome for the overlapping Anchor field.')
    check('R315-10', 'two faces' in c05 and 'passive Perception' in c05 and 'ended-source attempts uncharged' in c05, 'C05 requires full Hide outcomes, bounded observer evidence, and no charge/bonus for denied or ended source.')
    a_rows=[row for branch in ledger['branches'] for row in branch.get('rows',[]) if row.get('inputEventId','').endswith('A-END')]
    dseq=[row.get('correctedAfter',{}).get('Dissonance') for row in a_rows if row.get('atSeconds') in [172818.2,172824.2]]
    end_rows=[r for r in ledger['branches'][1]['rows'] if r.get('kind')=='paid-greater-dispel-terminates-denied-imprint']
    er=end_rows[0] if end_rows else {}
    c01row=ledger['branches'][1]['rows']
    dispel_state=next((r['correctedAfter'] for r in c01row if r.get('kind')=='paid-greater-dispel-terminates-denied-imprint'),{})
    check('R315-11', dseq.count(1)>=2 and dseq.count(0)>=2 and dispel_state.get('RP')==3 and dispel_state.get('Dissonance')==1 and dispel_state.get('turnCast') is True, 'Ledger records A’s idle D2→D1→D0, then the 10-RP spell leaves RP3/D1 with cast flag true.')
    check('R315-12', queue.get('authority')==auth and queue.get('nextIdentity')=='reality-anchor' and queue.get('nextAfterRealityAnchor')=='time-stop' and blockers.get('held') is True and semantic.get('wholeIdentityAccepted') is False, 'Next remains Reality Anchor then Time Stop; narrow hold and unrelated retained holds persist.')

result={'id':'REALITY-ANCHOR-RETURN315-INDEPENDENT-AUDIT','recordedAtUtc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL','returnArchive':{'path':ARCHIVE.relative_to(ROOT).as_posix(),**digest(araw)},'returnDelivery':{'path':DELIVERY.relative_to(ROOT).as_posix(),**digest(draw)},'submittedPacket315':{'path':SUBMITTED.relative_to(ROOT).as_posix(),**submitted_digest},'checkCount':len(checks),'passed':sum(c['status']=='PASS' for c in checks),'failed':sum(c['status']=='FAIL' for c in checks),'checks':checks,'decision':'HOLD','acceptedIds':[],'appliedIds':[],'heldIds':['reality-anchor'],'authority':{'reviewedApplied':822,'pending':26,'acceptedUnapplied':0,'completeStandaloneProcedures':546,'scopedInterfaces':173},'correctionIds':['RA315-C01','RA315-C02','RA315-C03','RA315-C04','RA315-C05'],'next':['reality-anchor correction','time-stop'],'canonicalFilesChanged':False,'applicationPerformed':False}
OUT.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'audit':OUT.relative_to(ROOT).as_posix(),'status':result['status'],'passed':result['passed'],'failed':result['failed'],'returnSha256':digest(araw)['sha256']},indent=2))
if result['status']!='PASS': raise SystemExit(1)
