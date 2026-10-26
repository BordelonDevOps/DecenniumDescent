from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[5]
AUDIT=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
FULL=ROOT/'docs/audit/2026-10-08/full-game'
GROUP='rank9-knowledge-revelation5'
IDS=['cosmic-awareness','cosmic-revelation','divine-truth','oracle-of-eternity','faction-omniscience-supreme']
AUTHORITY={'reviewedApplied':786,'pending':62,'acceptedUnapplied':0,'completeStandaloneProcedures':510,'scopedInterfaces':173}
INDEX='DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG='DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
QUEUE='docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_196.json'
PENDING='docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT62_PENDING_IDENTITY_AUDIT_196.json'
HANDOFF='docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_196.json'
CANDIDATE='DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_knowledge_revelation_5_source_conference_01.json'
ARCHIVE='docs/audit/2026-10-08/full-game/DD_Rank9_Knowledge_Revelation_5_Source_Conference_01.zip'
NOTES='docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9KNOWLEDGEREVELATION5_NEXT_CONFERENCE_NOTES_129.json'
OUT=AUDIT/'rank9_knowledgerevelation5_current_source_197_prepared'
PACKET_PATH=AUDIT/'RANK9KNOWLEDGEREVELATION5_PACKET_197.json'
PREP_PATH=AUDIT/'RANK9KNOWLEDGEREVELATION5_SOURCE_PREPARATION_197.json'
PENDING_PATH=AUDIT/'CURRENT62_PENDING_IDENTITY_AUDIT_197.json'
QUEUE_PATH=AUDIT/'CURRENT_SPELL_QUEUE_197.json'
HANDOFF_PATH=AUDIT/'CURRENT_HANDOFF_197.json'
SNAPSHOT_PATH=AUDIT/'CURRENT_SPELL_REVIEW_SNAPSHOT_197.md'
CHAT='https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682'
MEMORY_PACKAGE='DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9memorydenial6_reviewed_196'
MEMORY_AUDIT='docs/audit/2026-10-08/full-game/director-spell-review-129'

def sha(raw:bytes)->str:return hashlib.sha256(raw).hexdigest()
def json_bytes(value)->bytes:return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def read(raw:bytes):return json.loads(raw.decode('utf-8-sig'))
def bind(path,raw:bytes)->dict:return {'path':path.relative_to(ROOT).as_posix() if isinstance(path,Path) else path,'bytes':len(raw),'sha256':sha(raw)}
def blob(commit:str,path:str)->bytes:
    return subprocess.check_output(['git','cat-file','blob',f'{commit}:{path}'],cwd=ROOT)
def blob_id(commit:str,path:str)->str:
    return subprocess.check_output(['git','rev-parse',f'{commit}:{path}'],cwd=ROOT,text=True).strip()
def safe_member(name:str)->bool:
    p=PurePosixPath(name)
    return bool(name) and '\\' not in name and not p.is_absolute() and all(x not in ('','.','..') and not x.startswith('.') for x in p.parts)
def write(p:Path,b:bytes):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)

def main():
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    assert branch=='codex/ordinary-spell-review-complete'
    remote=subprocess.check_output(['git','ls-remote','origin',f'refs/heads/{branch}'],cwd=ROOT,text=True).split()[0]
    assert remote==commit,(remote,commit)
    dirty=subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).splitlines()
    assert all(line[3:].startswith('docs/audit/2026-10-08/full-game/director-spell-review-129/__pycache__/') or line[3:]=='docs/audit/2026-10-08/full-game/director-spell-review-129/prepare_knowledge_revelation5_current_197.py' for line in dirty),dirty
    assert not OUT.exists() and not any(p.exists() for p in (PACKET_PATH,PREP_PATH,PENDING_PATH,QUEUE_PATH,HANDOFF_PATH,SNAPSHOT_PATH))

    queue,pending,handoff,index,catalog=[read(blob(commit,p)) for p in (QUEUE,PENDING,HANDOFF,INDEX,CATALOG)]
    assert queue['nextGroup']==handoff['nextGroup']==GROUP
    assert queue['currentAuthority']==handoff['currentAuthority']==AUTHORITY
    assert index['authoredCounts']=={'reviewed':786,'pending':62}
    assert index['representationCounts']['completeReviewedStandaloneProcedures']==510
    assert pending['pendingCount']==len(pending['pendingIds'])==queue['pendingCount']==62
    target=next(x for x in queue['currentPendingGroups'] if x['group']==GROUP)
    assert target['pendingIds']==IDS and target['pendingCount']==5 and target['freshPacketRequiredForCurrentAuthority'] is True
    candidate_raw,archive_raw,notes_raw=[blob(commit,p) for p in (CANDIDATE,ARCHIVE,NOTES)]
    historical,notes=read(candidate_raw),read(notes_raw)
    assert sha(candidate_raw)==target['candidate']['sha256'] and len(candidate_raw)==target['candidate']['bytes']
    assert sha(archive_raw)==target['archive']['sha256'] and len(archive_raw)==target['archive']['bytes']
    assert [x['spellId'] for x in historical['records']]==IDS
    assert len(historical['sourceBindings'])==126
    assert notes['identities']==IDS
    assert len(notes['completeOriginalQuestionsUnchanged'])==26
    assert len(notes['focusedAdditionalQuestions'])==2 and len(notes['allQuestions'])==28
    assert len(notes['requiredNewCases'])==10 and len(notes['originalFutureCaseRequirementsUnchanged'])==9
    entries={x['id']:x for x in index['entries']}
    catalog_rows={x['id']:x for x in catalog['spells']}
    pending_ids=set(pending['pendingIds'])
    assert set(IDS)<=pending_ids
    for sid in IDS:
        assert entries[sid]['authoredStatus']=='pending-authored-procedure'
        assert entries[sid]['sourceStatus']=='blocked-pending-operational-review'
        ptr=int(entries[sid]['wholeCardPointer'].rsplit('/',1)[1])
        assert catalog['spells'][ptr]['id']==sid==catalog_rows[sid]['id']

    historic_members={}
    with zipfile.ZipFile(FULL/Path(ARCHIVE).name) as old:
        names=old.namelist()
        assert old.testzip() is None and len(names)==len(set(names)) and all(safe_member(n) for n in names)
        for source in historical['sourceBindings']:
            raw=old.read('sources/'+source['path'])
            assert len(raw)==source['bytes'] and sha(raw)==source['sha256']
            historic_members[source['path']]=raw

    refreshed,current_sources,changed=[],{},[]
    for old in historical['sourceBindings']:
        path=old['path']
        assert safe_member(path) and not Path(path).is_absolute()
        raw=blob(commit,path)
        row={'path':path,'bytes':len(raw),'sha256':sha(raw),'gitBlobSHA1':blob_id(commit,path)}
        refreshed.append(row)
        current_sources['sources_current/'+path]=raw
        if raw!=historic_members[path]:
            changed.append({'path':path,'historicalBytes':len(historic_members[path]),
                            'historicalSha256':sha(historic_members[path]),'currentBytes':len(raw),
                            'currentSha256':sha(raw)})
    assert len(refreshed)==126 and len({x['path'] for x in refreshed})==126

    now=datetime.now(timezone.utc).isoformat()
    current=copy.deepcopy(historical)
    current['historicalSourceBindings']=copy.deepcopy(historical['sourceBindings'])
    current['sourceBindings']=refreshed
    current['currentSourceCommit']=commit
    current['currentBranch']=branch
    current['currentAuthority']=AUTHORITY
    current['currentPendingGroup']={'group':GROUP,'spellIds':IDS,'count':5}
    current['historicalCandidateBinding']=bind(CANDIDATE,candidate_raw)
    current['queueCandidateBinding']=copy.deepcopy(target['candidate'])
    current['historicalSourceArchiveBinding']=bind(ARCHIVE,archive_raw)
    current['sourceBindingRefresh']={'sourceFiles':len(refreshed),'changedSinceHistoricalCandidate':changed,
                                    'sourceContentsFromGitCommit':commit,'allSourceBindingsRefreshed':True}
    current['countsUnchanged']={'reviewed':786,'pending':62}
    current['status']='CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_786_REVIEWED_62_PENDING_AUTHORITY'
    current['id']='RANK9-KNOWLEDGE-REVELATION5-CURRENT-SOURCE-CONTEXT-197'
    current['recordedAtUtc']=now
    for record in current['records']:
        sid=record['spellId']
        record['historicalIndexEntry']=copy.deepcopy(record['currentIndexEntry'])
        record['currentIndexEntry']=copy.deepcopy(entries[sid])
    current_raw=json_bytes(current)

    memory_paths=[
        f'{MEMORY_PACKAGE}/MODEL.json',
        f'{MEMORY_PACKAGE}/CANDIDATE_PACKAGE_MANIFEST.json',
        f'{MEMORY_PACKAGE}/INDEPENDENT_RETURN_AUDIT.json',
        f'{MEMORY_PACKAGE}/CASE_INDEX.json',
        f'{MEMORY_PACKAGE}/HOLD_REGISTER.json',
        *[f'{MEMORY_PACKAGE}/procedures/{s}.json' for s in [
            'mass-willbreaker','mind-collapse','mind-prison-mass','mind-wipe','unmake-spell','unravel-identity']],
        *[f'{MEMORY_AUDIT}/{n}' for n in [
            'RANK9_MEMORYDENIAL6_EXACT_ACCEPTANCE_196.json',
            'RANK9_MEMORYDENIAL6_APPLICATION_196.json',
            'RANK9_MEMORYDENIAL6_APPLICATION_VALIDATION_196.json',
            'RANK9_MEMORYDENIAL6_DIRECTOR_DECISION_196.json',
            'RANK9_MEMORYDENIAL6_RETURN196_INDEPENDENT_AUDIT.json',
            'RANK9_MEMORYDENIAL6_RETURN196_RECEIPT.json',
            'CURRENT62_PENDING_IDENTITY_AUDIT_196.json',
            'CURRENT_HANDOFF_196.json',
            'CURRENT_SPELL_QUEUE_196.json',
            'CURRENT_SPELL_REVIEW_SNAPSHOT_196.md']]]
    current_paths=[INDEX,CATALOG,QUEUE,PENDING,HANDOFF,'START_HERE.md',*memory_paths]
    current_files={'current/'+p:blob(commit,p) for p in current_paths}

    retained={
        'AG190':{'ids':['absolute-domination','puppetmaster-s-realm'],'blockers':['AG190-B01','AG190-B02']},
        'TF192':{'ids':['time-stop','eternal-prophecy','fate-rewrite','collapse-timeline'],'blockers':['TF192-B01','TF192-B02','TF192-B04','TF192-B05']},
        'CC194':{'ids':['perfect-spell','unholy-ascendance'],'blockers':['CC194-B01','CC194-B04']},
        'MD196':{'ids':['mind-collapse','unravel-identity'],'blockers':['MD196-B01','MD196-B02']}}
    context={
        'id':'RANK9-KNOWLEDGE-REVELATION5-CURRENT-DIRECTOR-CONTEXT-197',
        'recordedAtUtc':now,'sourceCommit':commit,'sourceBranch':branch,'sourceAuthority':AUTHORITY,
        'targetGroup':{'group':GROUP,'pendingIds':IDS,'count':5},
        'currentIndexCounts':index['authoredCounts'],'currentPendingAudit':pending['id'],
        'historicalQueueCandidateBinding':target['candidate'],
        'historicalCandidateBinding':bind(CANDIDATE,candidate_raw),
        'historicalSourceArchiveBinding':bind(ARCHIVE,archive_raw),
        'sourceRefresh':{'sourceFileCount':len(refreshed),'changedSinceCandidate':changed},
        'latestAcceptedOrdinarySpellBatch':{
            'application':'RANK9-MEMORYDENIAL6-APPLICATION-196',
            'acceptedIds':['mass-willbreaker','mind-prison-mass','mind-wipe','unmake-spell'],
            'unacceptedIds':['mind-collapse','unravel-identity'],
            'retainedBlockers':{'mind-collapse':['MD196-B01'],'unravel-identity':['MD196-B02']},
            'countsAfter':AUTHORITY,'runtimeSelectionEnabled':False,
            'procedureModel':f'current/{MEMORY_PACKAGE}/MODEL.json',
            'independentAudit':'current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_MEMORYDENIAL6_RETURN196_INDEPENDENT_AUDIT.json'},
        'retainedNamedBlockersOutsideScope':retained,
        'qualification':'Preparation only. Revalidate every source and accepted context against refreshed source bindings. The historical candidate is provenance, not current authority. Memory denial remains separately bounded: actual accepted Mind Wipe and the four other accepted procedures are static authoring, while MD196-B01 and B02 remain open blockers. No cosmic or divine information capability may infer erased private memory, bypass an information protection, gain future authorization, or claim knowledge absent from the bound world record.',
    }

    request=(
        'GPT director — review exactly the five current pending Rank9 Knowledge/Revelation5 identities in this packet.\n\n'
        f'Source branch and commit: {branch} / {commit}. Current authority: 786 reviewed-applied / 62 pending / 0 accepted-unapplied; 510 complete standalone procedures; 173 scoped interfaces.\n\n'
        'Scope only: cosmic-awareness, cosmic-revelation, divine-truth, oracle-of-eternity, faction-omniscience-supreme. Use the attached refreshed 126-source bindings, current queue, handoff, pending audit, index, catalog and static application context as authority. The historical candidate and conference archive are provenance. Preserve all 26 original questions, both focused addenda, all 10 required new cases, and all 9 future-case requirements. Do not broaden scope or reopen closed feat identities or completed spell cohorts.\n\n'
        'Resolve exact source conflicts separately. Cosmic Awareness promises all events in a 10-mile region while the catalog also supplies 120 feet and Instantaneous; define the center, simultaneous hidden events, source granularity, complete finite snapshot, retained truth and lawful query boundary without silently clipping the promise or inventing a live feed. Cosmic Revelation has a 100-foot all-creature payload, a native resistance override, and no supplied duration; provide meaningful positive and blocked/immune recipient cases, exact source-backed duration and concentration/condition consequences without inventing a rank-nine bypass. Divine Truth promises three substantive truthful answers under compulsion; preserve the genuine payload, exact access to what the target knows, three-question consumption, source-qualified ignorance and agency limits. Oracle of Eternity must produce three useful truthful yes/no answers and handle ambiguous, false-presupposition, protected and contingent-future questions under a precise contract. Supreme Faction Omniscience must bind actual faction past/present and any justified likely future, with assumptions and horizons, separate unrelated private information, distinguish true absence from missing source records, and avoid forced future decisions or membership benefits.\n\n'
        'Treat actual world facts, records, private beliefs, memory, divine truth and forecasts as separate sources. Preserve accepted memory and information protections and their exact scope. Current Memory/Denial6 has four accepted static authored procedures, including Mind Wipe, while Mind Collapse and Unravel Identity remain blocked under MD196-B01/B02. Keep that exact state and do not infer omniscience can recover erased private memory or defeat a protected fact. Carry forward AG190, TF192 and CC194 named blockers unchanged. Do not modify canonical spell cards, change cosmology or rules, or execute supplied programs.\n\n'
        'Return one complete source-faithful static procedure per identity. Include concrete positive, boundary, resistance, protection and failure branches; lifecycle, exact procedure text, accepted-access/class placement, preserved original obligations, question/case dispositions, future obligations, full reversible event/state operations, hold records, exact source bindings and package manifests. Accept only identities independently passing all applicable evidence with accepted=true and applied=false. Give named blockers for every unaccepted identity. Exact accepted identities will be independently audited, applied and pushed; then the review will continue to the next group.'
    )

    files={
        'CURRENT_CONTEXT_197.json':json_bytes(context),
        'CURRENT_SOURCE_CONFERENCE_CANDIDATE_197.json':current_raw,
        'HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json':candidate_raw,
        'HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip':archive_raw,
        'HISTORICAL_NOTES/RANK9KNOWLEDGEREVELATION5_NEXT_CONFERENCE_NOTES_129.json':notes_raw,
        'REQUEST_197.txt':request.encode('utf-8'),
        **current_files,**current_sources}
    assert len(files)==len(set(files)) and all(safe_member(n) for n in files)
    OUT.mkdir(parents=True,exist_ok=False)
    current_candidate_path=OUT/'CURRENT_SOURCE_CONFERENCE_CANDIDATE_197.json'
    write(current_candidate_path,current_raw)
    packet_path=OUT/'DD_Rank9_KnowledgeRevelation5_CurrentSource_197.zip'
    with zipfile.ZipFile(packet_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as packet:
        rows=[]
        for name in sorted(files):
            raw=files[name]
            packet.writestr(name,raw,compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
            rows.append({'path':name,'bytes':len(raw),'sha256':sha(raw),'crc32':f'{zlib.crc32(raw)&0xffffffff:08x}'})
        manifest={'id':'RANK9-KNOWLEDGE-REVELATION5-CURRENT-SOURCE-PACKET-MANIFEST-197',
                  'sourceCommit':commit,'sourceBranch':branch,'sourceAuthority':AUTHORITY,
                  'group':GROUP,'pendingIds':IDS,'memberCountExcludingSelf':len(rows),'members':rows}
        packet.writestr('MANIFEST.json',json_bytes(manifest),compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
    with zipfile.ZipFile(packet_path) as packet:
        names=packet.namelist()
        assert packet.testzip() is None and len(names)==len(rows)+1 and len(names)==len(set(names))
        for row in rows:
            with packet.open(row['path']) as stream:
                h=hashlib.sha256();crc=0;n=0
                for part in iter(lambda:stream.read(1024*1024),b''):
                    n+=len(part);h.update(part);crc=zlib.crc32(part,crc)
            assert n==row['bytes'] and h.hexdigest()==row['sha256'] and f'{crc&0xffffffff:08x}'==row['crc32']

    packet_raw=packet_path.read_bytes()
    packet_binding=bind(packet_path.relative_to(ROOT).as_posix(),packet_raw)
    candidate_binding=bind(current_candidate_path.relative_to(ROOT).as_posix(),current_raw)
    delivery={'id':'RANK9-KNOWLEDGE-REVELATION5-CURRENT-SOURCE-DELIVERY-197',
              'status':'PREPARED_UNSENT','archive':packet_binding,
              'members':len(rows)+1,'manifestBindings':len(rows),
              'sourceCommit':commit,'sourceBranch':branch,'sourceAuthority':AUTHORITY,
              'group':GROUP,'pendingIds':IDS,'candidate':candidate_binding,
              'historicalCandidate':bind(CANDIDATE,candidate_raw),
              'historicalSourceArchive':bind(ARCHIVE,archive_raw),
              'sourceFilesRefreshed':len(refreshed),'sourceFilesChangedSinceHistoricalCandidate':changed,
              'accepted':False,'applied':False,'conversation':CHAT}
    delivery_path=OUT/'DD_Rank9_KnowledgeRevelation5_CurrentSource_197_DELIVERY.json'
    delivery_raw=json_bytes(delivery);write(delivery_path,delivery_raw)
    delivery_binding=bind(delivery_path.relative_to(ROOT).as_posix(),delivery_raw)

    checks=[
        'Packet binds pushed branch head and exact 786/62/0 authority.',
        'Exactly five current pending Knowledge/Revelation identities are next in queue order.',
        'All 126 historical source members match the archived bytes and hashes.',
        'All 126 source bindings are refreshed from the exact current Git commit.',
        'All five current native entries, access routes, and catalog pointers remain exact and pending.',
        'Return196 accepted Memory/Denial6 procedures and its two named blockers are current context.',
        'AG190, TF192, CC194, and MD196 blockers remain expressly retained outside this review scope.',
        'All 26 original questions, 2 addenda, 10 required new cases, and 9 future-case requirements are preserved.',
        'Historical archive, current files, and every packet member SHA/CRC validate.',
    ]
    preparation={'id':'RANK9-KNOWLEDGE-REVELATION5-SOURCE-PREPARATION-197',
                 'recordedAtUtc':now,'status':'PASS','checks':[{'check':s,'passed':True} for s in checks],
                 'checkCount':len(checks),'sourceCommit':commit,'sourceBranch':branch,
                 'sourceAuthority':AUTHORITY,'targetGroup':GROUP,'pendingIds':IDS,
                 'currentCandidate':candidate_binding,'historicalCandidate':bind(CANDIDATE,candidate_raw),
                 'historicalArchive':bind(ARCHIVE,archive_raw),'packet':packet_binding,
                 'deliveryManifest':delivery_binding,'refreshedBindings':len(refreshed),
                 'changedHistoricalBindings':changed,'questions':{'original':26,'addenda':2,'total':28},
                 'requiredMainCases':10,'futureCaseRequirements':9,'canonicalChanges':False,
                 'accepted':False,'applied':False}
    write(PREP_PATH,json_bytes(preparation))
    write(PACKET_PATH,json_bytes({'id':'RANK9KNOWLEDGEREVELATION5-PACKET-197',
                                  'status':'PREPARED_UNSENT','group':GROUP,'pendingIds':IDS,
                                  'sourceAuthority':AUTHORITY,'sourceCommit':commit,
                                  'archive':packet_binding,'deliveryManifest':delivery_binding,
                                  'candidate':candidate_binding,'questions':28,
                                  'requiredMainCases':10,'futureCaseRequirements':9,
                                  'refreshedSourceBindings':len(refreshed),'canonicalChanges':False}))

    pending_audit={'id':'CURRENT62-PENDING-IDENTITY-AUDIT-197','recordedAtUtc':now,
                   'status':'PASSED_EXACT_CURRENT_INDEX_PENDING_SET',
                   'indexBinding':bind(INDEX,blob(commit,INDEX)),
                   'catalogBinding':bind(CATALOG,blob(commit,CATALOG)),
                   'authoredCounts':index['authoredCounts'],'pendingCount':62,
                   'pendingIds':pending['pendingIds'],'allPendingExistInSourceCatalog':set(pending['pendingIds'])<=set(catalog_rows),
                   'acceptedUnapplied':0,
                   'retainedReturn188Blockers':pending.get('retainedReturn188Blockers',{}),
                   'retainedReturn190Blockers':pending.get('retainedReturn190Blockers',{}),
                   'retainedReturn192Blockers':pending.get('retainedReturn192Blockers',{}),
                   'retainedReturn194Blockers':pending.get('retainedReturn194Blockers',{}),
                   'retainedReturn196Blockers':pending.get('retainedReturn196Blockers',{}),
                   'closed335AndCompletedCohortsReopened':False,
                   'currentAuthority':AUTHORITY}
    write(PENDING_PATH,json_bytes(pending_audit))
    packet_request={'group':GROUP,'pendingIds':IDS,'pendingCount':5,
                    'status':'CURRENT_SOURCE_PACKET_PREPARED_UNSENT',
                    'freshPacketRequiredForCurrentAuthority':False,
                    'packet':packet_binding,'deliveryManifest':delivery_binding,
                    'packetRecord':bind(PACKET_PATH,PACKET_PATH.read_bytes()),
                    'sourcePreparation':bind(PREP_PATH,PREP_PATH.read_bytes())}
    q1=copy.deepcopy(queue)
    q1.update({'id':'SPELL-REVIEW-QUEUE-197','recordedAtUtc':now,
               'nextGroup':GROUP,'next':packet_request,'nextPreparedRequest':packet_request,
               'packetStatus':'RANK9_KNOWLEDGE_REVELATION5_PACKET_197_PREPARED_UNSENT_786_62',
               'currentPacket':packet_binding,'currentPacketDelivery':delivery_binding,
               'currentPreparation':bind(PREP_PATH,PREP_PATH.read_bytes()),
               'pendingIdentityAudit':{'path':PENDING_PATH.relative_to(ROOT).as_posix(),
                                       'pending':62,'sha256':sha(PENDING_PATH.read_bytes())}})
    new_groups=[]
    for old in q1['currentPendingGroups']:
        g=copy.deepcopy(old)
        if g['group']==GROUP:
            g.update({'status':'CURRENT_SOURCE_PACKET_PREPARED_UNSENT',
                      'freshPacketRequiredForCurrentAuthority':False,
                      'packet':packet_binding,'deliveryManifest':delivery_binding,
                      'packetRecord':packet_request['packetRecord'],
                      'sourcePreparation':packet_request['sourcePreparation']})
        new_groups.append(g)
    q1['currentPendingGroups']=new_groups
    write(QUEUE_PATH,json_bytes(q1))

    h1=copy.deepcopy(handoff)
    h1.update({'id':'CURRENT-HANDOFF-197','recordedAtUtc':now,
               'status':'RANK9_KNOWLEDGE_REVELATION5_PACKET_197_PREPARED_UNSENT_786_62',
               'currentAuthority':AUTHORITY,
               'nextGroup':GROUP,'nextPendingCount':5,
               'nextPreparedRequest':packet_request,
               'pendingIdentityAudit':{'id':pending_audit['id'],
                                       'path':PENDING_PATH.relative_to(ROOT).as_posix(),
                                       'pendingCount':62,'sha256':sha(PENDING_PATH.read_bytes())},
               'currentQueueBinding':bind(QUEUE_PATH,QUEUE_PATH.read_bytes()),
               'currentPacket':packet_binding,'currentPacketDelivery':delivery_binding,
               'currentPreparation':bind(PREP_PATH,PREP_PATH.read_bytes()),
               'resumePriority':'Upload and submit this fresh Knowledge/Revelation5 packet to GPT; independently audit the return, apply/push exact accepted IDs, and continue through pending spells.'})
    for k in ('directorSubmission','submissionReceipt','currentSubmissionBinding','currentPacket','currentPacketDelivery','currentPreparation'):
        h1.pop(k,None)
    write(HANDOFF_PATH,json_bytes(h1))
    snapshot=('# Current ordinary spell-review checkpoint 197\n\n'
              'Return196 was independently verified and four Memory/Denial6 procedures were applied. '
              'Authority is **786 reviewed / 62 pending / 0 accepted-unapplied**, with 510 complete standalone procedures. '
              'Mind Collapse and Unravel Identity remain pending under MD196-B01/B02; earlier named blockers remain. '
              'Fresh Rank9 Knowledge/Revelation5 packet prepared against the pushed current source commit; '
              'it covers five pending identities, 28 questions, 10 required cases, and nine future obligations. '
              'Awaiting GPT director review. Runtime and downstream approval gates remain disabled.\n')
    write(SNAPSHOT_PATH,snapshot.encode('utf-8'))
    start=ROOT/'START_HERE.md'
    start_raw=blob(commit,'START_HERE.md').decode('utf-8-sig')
    marker='**Current ordinary spell-review handoff [197]('
    if marker not in start_raw:
        start_raw=('**Current ordinary spell-review handoff [197](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_197.json):** Authority is **786 reviewed / 62 pending / 0 accepted-unapplied**. Memory/Denial6 applied four exact acceptances and retained two named blockers. Next group: Rank9 Knowledge/Revelation5; fresh packet is prepared and awaiting GPT.\n\n'+start_raw)
    (ROOT/'START_HERE.md').write_text(start_raw,encoding='utf-8',newline='\n')
    print(json.dumps({'status':'PREPARED_UNSENT','sourceCommit':commit,'authority':AUTHORITY,
                      'group':GROUP,'packet':packet_binding,'delivery':delivery_binding,
                      'refreshedSources':len(refreshed),'changedSources':changed,
                      'questions':28,'mainCases':10,'futureObligations':9,
                      'checks':len(checks)},indent=2))
if __name__=='__main__':main()
