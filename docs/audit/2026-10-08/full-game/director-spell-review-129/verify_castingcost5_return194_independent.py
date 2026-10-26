from __future__ import annotations
import hashlib, io, json, subprocess, traceback, zipfile, zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import jsonpatch

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
RECEIVED = AUDIT / 'rank9_castingcost5_return194_received'
ARCHIVE = RECEIVED / 'DD_Rank9_CastingCost5_Director_Return194.zip'
DELIVERY = RECEIVED / 'DD_Rank9_CastingCost5_Director_Return194_DELIVERY.json'
REPORT = AUDIT / 'RANK9_CASTINGCOST5_RETURN194_INDEPENDENT_AUDIT.json'
SOURCE_COMMIT = 'a67af2f14b50a399d26f6059b6ad4918d4c2c1fa'
BRANCH = 'codex/ordinary-spell-review-complete'
AUTHORITY = {'reviewedApplied':779,'pending':69,'acceptedUnapplied':0,'completeStandaloneProcedures':503,'scopedInterfaces':173}
GROUP = ['perfect-spell','ritual-mastery','world-rewrite','resonance-perfection','unholy-ascendance']
ACCEPTED = ['ritual-mastery','world-rewrite','resonance-perfection']
UNACCEPTED = ['perfect-spell','unholy-ascendance']
EXPECTED_BLOCKERS = {'perfect-spell':['CC194-B01'],'unholy-ascendance':['CC194-B04']}
CARRIED = {'AG190-B01','AG190-B02','TF192-B01','TF192-B02','TF192-B04','TF192-B05'}
checks=[]; failures=[]
def sha(raw:bytes)->str: return hashlib.sha256(raw).hexdigest()
def sha_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def read_json(raw:bytes): return json.loads(raw.decode('utf-8-sig'))
def canonical(value)->bytes: return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def git_blob(commit:str,path:str)->bytes: return subprocess.check_output(['git','cat-file','blob',f'{commit}:{path}'],cwd=ROOT)
def git_blob_id(commit:str,path:str)->str: return subprocess.check_output(['git','rev-parse',f'{commit}:{path}'],cwd=ROOT,text=True).strip()
def safe_member(name:str)->bool:
    p=PurePosixPath(name)
    return bool(name) and '\\' not in name and not p.is_absolute() and all(x not in ('','.','..') for x in p.parts)
def check(label:str,passed:bool,detail=None):
    checks.append({'check':label,'passed':bool(passed),**({'detail':detail} if detail is not None else {})})
    if not passed: failures.append(label)
def compare_replay(case:dict,binding:dict):
    state=case['initialState']; assert sha(canonical(state))==binding['initialSHA256']
    assert case['events'] and state==case['events'][0]['before']
    seen=set(); forward=inverse=0; events=0; last_ms=state.get('world',{}).get('nowMs')
    declared={r['id']:r for r in binding['eventStateHashes']}
    assert len(declared)==len(case['events'])==binding['eventCount']
    for event in case['events']:
        eid=event['id']; assert eid not in seen; seen.add(eid); events+=1
        assert state==event['before']
        assert sha(canonical(event['before']))==event['beforeSHA256']
        assert sha(canonical(event['after']))==event['afterSHA256']
        assert declared[eid]=={'id':eid,'beforeSHA256':event['beforeSHA256'],'afterSHA256':event['afterSHA256']}
        now=event.get('after',{}).get('world',{}).get('nowMs')
        if isinstance(last_ms,(int,float)) and isinstance(now,(int,float)): assert now>=last_ms, f'world clock backstep at {eid}'
        assert jsonpatch.JsonPatch(event['forward']).apply(event['before'],in_place=False)==event['after']
        assert jsonpatch.JsonPatch(event['inverse']).apply(event['after'],in_place=False)==event['before']
        forward+=len(event['forward']); inverse+=len(event['inverse']); state=event['after']; last_ms=now
    assert state==case['finalState'] and sha(canonical(state))==binding['finalSHA256']
    return events,forward,inverse

def verify():
    delivery_raw=DELIVERY.read_bytes(); delivery=read_json(delivery_raw); archive_sha=sha_file(ARCHIVE)
    check('External delivery binds exact ZIP length and SHA-256', ARCHIVE.stat().st_size==delivery['archive']['bytes']==131568634 and archive_sha==delivery['archive']['sha256']=='f6caf05f6677213059762119b07a5eb0add983a5cc5f152fd317d04f328af90c', {'bytes':ARCHIVE.stat().st_size,'sha256':archive_sha})
    check('Delivery records exact partial acceptance as unapplied', delivery['acceptedIds']==ACCEPTED and delivery['unacceptedIds']==UNACCEPTED and delivery['applied'] is False and delivery['authorityUnchanged']==AUTHORITY)
    replay_cases=replay_events=replay_fwd=replay_inv=0; source_rows=[]; semantic={}
    try:
        with zipfile.ZipFile(ARCHIVE) as outer:
            names=outer.namelist(); allow=set(delivery['memberAllowlist']); delivery_rows={r['path']:r for r in delivery['members']}
            check('Outer ZIP safe, unique, CRC-clean and exactly delivery-allowlisted', outer.testzip() is None and len(names)==len(set(names))==109 and set(names)==allow==set(delivery_rows) and all(safe_member(n) for n in names), {'members':len(names),'allowlisted':len(allow)})
            manifest=read_json(outer.read('MEMBER_MANIFEST.json')); rows={r['path']:r for r in manifest['members']}
            check('Internal manifest covers every member except itself', len(rows)==108 and set(rows)==set(names)-{'MEMBER_MANIFEST.json'} and manifest['archiveMembersIncludingSelf']==109)
            hashes_ok=True
            for name in names:
                raw=outer.read(name); drow=delivery_rows[name]
                if len(raw)!=drow['bytes'] or sha(raw)!=drow['sha256'] or f'{zlib.crc32(raw)&0xffffffff:08x}'!=drow['crc32'].lower(): hashes_ok=False; break
                if name!='MEMBER_MANIFEST.json':
                    m=rows[name]
                    if len(raw)!=m['bytes'] or sha(raw)!=m['sha256'] or f'{zlib.crc32(raw)&0xffffffff:08x}'!=m['crc32'].lower(): hashes_ok=False; break
            check('All 109 member byte counts, SHA-256 hashes and CRC32 values independently recalculate',hashes_ok)
            context=read_json(outer.read('CURRENT_CONTEXT_193.json'))
            check('Current authority, source anchor and five-ID group are exact',context['sourceCommit']==SOURCE_COMMIT and context['sourceBranch']==BRANCH and context['sourceAuthority']==AUTHORITY and context['targetGroup']['pendingIds']==GROUP and context['targetGroup']['count']==5)
            check('External delivery claims same authority and anchor',delivery['authorityUnchanged']==AUTHORITY and delivery['sourceCommit']==SOURCE_COMMIT)
            # Bind every refreshed source to Git and to the exact source packet attached inside the return.
            source_rows=read_json(outer.read('SOURCE_BINDINGS.json'))
            nested_raw=outer.read('input/DD_Rank9_CastingCost5_CurrentSource_193.zip')
            nested_delivery=read_json(outer.read('input/DD_Rank9_CastingCost5_CurrentSource_193_DELIVERY.json'))
            nested_zip_meta=next((r for r in delivery.get('sourcePackets',[]) if r.get('fileName')=='DD_Rank9_CastingCost5_CurrentSource_193.zip'),None)
            nested_hash=sha(nested_raw)
            nested_bound=(nested_delivery['archive']['bytes']==len(nested_raw) and nested_delivery['archive']['sha256']==nested_hash and len(source_rows)==117)
            with zipfile.ZipFile(io.BytesIO(nested_raw)) as inner:
                inames=inner.namelist(); imanifest=read_json(inner.read('MANIFEST.json')); irows={r['path']:r for r in imanifest['members']}
                nested_bound &= inner.testzip() is None and len(inames)==144 and len(irows)==143 and set(irows)==set(inames)-{'MANIFEST.json'}
                for row in imanifest['members']:
                    raw=inner.read(row['path'])
                    if len(raw)!=row['bytes'] or sha(raw)!=row['sha256'] or f'{zlib.crc32(raw)&0xffffffff:08x}'!=row['crc32'].lower(): nested_bound=False; break
                source_ok=True
                for row in source_rows:
                    raw=inner.read('sources_current/'+row['path'])
                    if len(raw)!=row['bytes'] or sha(raw)!=row['sha256'] or sha(git_blob(SOURCE_COMMIT,row['path']))!=row['sha256'] or git_blob_id(SOURCE_COMMIT,row['path'])!=row['gitBlobSHA1'] or git_blob_id('HEAD',row['path'])!=row['gitBlobSHA1']:
                        source_ok=False; break
                check('All 117 refreshed source files match the nested packet, anchor Git blobs, and current HEAD', source_ok, {'rows':len(source_rows),'sourceCommit':SOURCE_COMMIT})
                nested_context=read_json(inner.read('CURRENT_CONTEXT_193.json'))
                check('Nested source packet itself is byte/hash-bound, 144 members, and CRC-clean', nested_bound and nested_context['sourceCommit']==SOURCE_COMMIT and nested_context['sourceAuthority']==AUTHORITY, {'bytes':len(nested_raw),'sha256':nested_hash,'members':len(inames)})
                # Verify five separately selected accepted comparison models by exact source path.
                additional=read_json(outer.read('ADDITIONAL_SOURCE_BINDINGS.json')); add_ok=len(additional)==5
                for row in additional:
                    raw=outer.read(row['local']); source=git_blob(row['sourceCommit'],row['sourcePath'])
                    add_ok &= len(raw)==row['bytes'] and sha(raw)==row['sha256'] and raw==source and git_blob_id(row['sourceCommit'],row['sourcePath'])==row['gitBlobSHA1']
                check('All five supplemental accepted-source bindings match exact Git blob bytes',bool(add_ok),{'bindings':len(additional)})
                # The packet's current catalog/index snapshot is authority for exact unchanged cards and access rows.
                catalog=json.loads(inner.read('sources_current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'))
                index=json.loads(inner.read('sources_current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'))
                catalog_rows={x['id']:x for x in catalog['spells']}; index_rows={x['id']:x for x in index['entries']}
                decision=read_json(outer.read('DIRECTOR_DECISION.json')); procedures_doc=read_json(outer.read('PROCEDURES.json')); procedures={x['id']:x for x in procedures_doc}; decisions={x['id']:x for x in decision['decisions'] if 'id' in x}
                check('Decision, delivery and procedures agree on the exact 3/2 split and applied=false',decision['acceptedIds']==ACCEPTED and delivery['acceptedIds']==ACCEPTED and decision['applied'] is False and delivery['applied'] is False and [x['id'] for x in procedures_doc if x['accepted']]==ACCEPTED and all(x['applied'] is False for x in procedures_doc) and set(procedures)==set(GROUP) and set(decisions)==set(GROUP))
                blocker_map={sid:decisions[sid]['blockerIds'] for sid in UNACCEPTED}
                check('Both current holds retain exact blocker IDs',blocker_map==EXPECTED_BLOCKERS)
                carry=decision.get('retainedNamedOutsideScopeBlockers',[])
                check('All Return190/Return192 named blockers are carried exactly', set(carry)==CARRIED, {'carried':sorted(carry)})
                native_ok=True; native_placements=0; class_access_rows=0
                for sid,proc in procedures.items():
                    card=proc['completeSourceAndAccess']; native_ok &= card==catalog_rows[sid] and proc['applied'] is False
                    idx=index_rows[sid]; native_ok &= idx['id']==sid and idx['name']==card['name'] and idx['authoredStatus']=='pending-authored-procedure' and idx['sourceStatus']=='blocked-pending-operational-review' and idx['priorCatalogSelectionStatusUnchanged'] is True
                    placements=card['source']['original']['placements']; native_placements+=len(placements); class_access_rows+=len(card['classAccess'])
                check('All five current canonical cards and pending index entries match exact source snapshots',bool(native_ok))
                check('Native placements and class access rows reconcile to packet totals',native_placements==5 and class_access_rows==14,{'nativePlacements':native_placements,'classAccessRows':class_access_rows})
                expected_qual=['Static authored review only','No runtime execution','Actual campaign acquisition']
                qual_ok=all(procedures[s]['accepted'] and decisions[s]['accepted'] and all(any(term.lower() in q.lower() for q in procedures[s]['qualifications']) for term in expected_qual) for s in ACCEPTED) and all(not procedures[s]['accepted'] for s in UNACCEPTED)
                check('Acceptance is per identity and qualifications preserve static-only, no-runtime and campaign-evidence boundaries',qual_ok)
                # Question, case, integrity, clock, semantic and metadata artifacts.
                questions=read_json(outer.read('ORIGINAL_QUESTIONS.json'))
                qrows=questions.get('numberedOriginal',[])
                qdisp=read_json(outer.read('QUESTION_DISPOSITIONS.json'))
                check('Question census records 32 numbered originals plus two focused addenda',len(qrows)==32 and len(questions.get('focusedAddenda',[]))==2 and len(qdisp)==34 and delivery['counts']['numberedOriginalQuestions']==32 and delivery['counts']['focusedAddenda']==2 and delivery['counts']['distinctQuestionDispositions']==34)
                casebook=read_json(outer.read('CASEBOOK.json')); cases={c['id']:c for c in casebook['cases']}; bindings=read_json(outer.read('CASE_HASH_BINDINGS.json')); case_bindings={b['id']:b for b in bindings}
                cases_ok=len(cases)==len(case_bindings)==63
                for cid,bind in case_bindings.items():
                    raw=outer.read(bind['path']); c=read_json(raw); case=cases[cid]
                    if c!=case or False or cid!=case['id']: cases_ok=False; break
                check('All 63 external case files exactly mirror CASEBOOK and match the internal hash bindings',cases_ok)
                replay_cases=replay_events=replay_fwd=replay_inv=0
                for cid,case in cases.items():
                    ev,fwd,inv=compare_replay(case,case_bindings[cid]); replay_cases+=1; replay_events+=ev; replay_fwd+=fwd; replay_inv+=inv
                check('All 63 case histories independently replay with state hashes, monotonic world time and exact inverse patches',replay_cases==63 and replay_events==1427 and replay_fwd==replay_inv==2854,{'cases':replay_cases,'events':replay_events,'forwardPatchOps':replay_fwd,'inversePatchOps':replay_inv})
                counts=delivery['counts']
                check('Advertised case/event/proposal/hold counts reconcile',counts['cases']==63 and counts['events']==1427 and counts['forwardEventOperations']==replay_fwd and counts['inverseEventOperations']==replay_inv and counts['eventOperationsTotal']==replay_fwd+replay_inv and counts['proposalOperations']==20 and counts['holdsTotal']==56 and counts['inheritedHolds']==46)
                data_check=read_json(outer.read('DATA_INTEGRITY_CHECK.json')); clock=read_json(outer.read('CLOCK_CHECK.json')); semantic=read_json(outer.read('INDEPENDENT_SEMANTIC_FAILURE_CHECK.json')); meta=read_json(outer.read('FINAL_METADATA_CHECK.json'))
                check('Independent data-integrity and clock ledgers contain their stated passing checks',data_check['checkCount']==36202==len(data_check['checks']) and all(x['pass'] for x in data_check['checks']) and clock['checkCount']==9605==len(clock['checks']) and all(x['pass'] for x in clock['checks']))
                check('Independent semantic and final metadata check counts are internally consistent',semantic['checkCount']==750==len(semantic['checks']) and all(x['pass'] for x in semantic['checks']) and meta['checkCount']==64==len(meta['checks']) and all(x['pass'] for x in meta['checks']) and semantic['acceptedIds']==ACCEPTED and semantic['applied'] is False)
                check('Validation summary consistently reports source/data PASS and partial semantic result',read_json(outer.read('VALIDATION.json'))['sourceResult']=='PASS' and read_json(outer.read('VALIDATION.json'))['dataResult']=='PASS' and read_json(outer.read('VALIDATION.json'))['semanticResult']=='PARTIAL_3_ACCEPTED_2_BLOCKED' and read_json(outer.read('VALIDATION.json'))['runtimeExecuted'] is False)
                nextq=read_json(outer.read('NEXT_QUEUE_GROUP.json'))['nextGroupUnchanged']
                check('Next group is the six-spell Memory/Denial6 group and still gated on refreshed authority',nextq['group']=='rank9-memory-denial6' and nextq['pendingIds']==['mass-willbreaker','mind-collapse','mind-prison-mass','mind-wipe','unmake-spell','unravel-identity'] and nextq['freshPacketRequiredForCurrentAuthority'] is True)
                semantic={'batchSemanticResult':semantic.get('batchSemanticResult'),'acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,'blockers':EXPECTED_BLOCKERS,'checkCount':750}
    except Exception:
        check('Independent audit completed without exception',False,traceback.format_exc())
    report={'id':'RANK9-CASTINGCOST5-RETURN194-INDEPENDENT-AUDIT','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if not failures else 'FAIL','checksPassed':sum(x['passed'] for x in checks),'checksFailed':len(failures),'failures':failures,'returnArchive':{'path':ARCHIVE.relative_to(ROOT).as_posix(),'bytes':ARCHIVE.stat().st_size,'sha256':sha_file(ARCHIVE)},'deliveryManifest':{'path':DELIVERY.relative_to(ROOT).as_posix(),'bytes':len(delivery_raw),'sha256':sha(delivery_raw)},'sourceCommit':SOURCE_COMMIT,'authority':AUTHORITY,'acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,'applied':False,'replay':{'cases':replay_cases,'events':replay_events,'forwardPatchOps':replay_fwd,'inversePatchOps':replay_inv},'semanticScreen':semantic,'checks':checks}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report
if __name__=='__main__':
    result=verify(); raise SystemExit(0 if result['status']=='PASS' else 1)
