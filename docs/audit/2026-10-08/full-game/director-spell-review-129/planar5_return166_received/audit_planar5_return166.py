from __future__ import annotations
import hashlib, json, zipfile, zlib, stat, io
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[6]
FULL = ROOT / 'docs/audit/2026-10-08/full-game'
AUDIT = FULL / 'director-spell-review-129'
RECV = AUDIT / 'planar5_return166_received'
RETURN = RECV / 'DD_Rank8_Planar5_Director_Return166.zip'
DELIVERY = RECV / 'DD_Rank8_Planar5_Director_Return166_DELIVERY.json'
PACKET = FULL / 'DD_Rank8_Planar_5_Source_Conference_02.zip'
CANDIDATE = ROOT / 'DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_planar_5_source_conference_02.json'
INDEX = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
OUT = RECV / 'PLANAR5_RETURN166_LOCAL_AUDIT.json'
EXTRACTED = FULL / 'p5ret166x'
IDS = ['demiplane','maze','planar-seal','seal-of-banishment','gloom-bind']
AUTH = {'reviewedApplied':730,'pending':118,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':454}

def sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def canonical(x) -> bytes: return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
def readj(path: Path): return json.loads(path.read_text(encoding='utf-8-sig'))
checks=[]
def ck(name, passed, detail=None):
    checks.append({'check':name,'passed':bool(passed), **({'detail':detail} if detail is not None else {})})

def run():
    delivery=readj(DELIVERY); raw=RETURN.read_bytes(); expected_zip=delivery['archive'];
    ck('Return ZIP matches delivery byte count and SHA-256', len(raw)==expected_zip['bytes'] and sha(raw)==expected_zip['sha256'], {'bytes':len(raw),'sha256':sha(raw)})
    ck('Delivery says accepted, unapplied, exact batch, no canonical edits', delivery['accepted'] is True and delivery['applied'] is False and delivery['acceptedIds']==IDS and delivery['canonicalFilesChanged'] is False)
    ck('Delivery authority matches live pre-application authority', delivery['authorityUsed']==AUTH)
    ck('Local packaging checks report no failures or hidden members', delivery['localPackagingChecks']['failed']==0 and delivery['localPackagingChecks']['hiddenOrTempMembers']==0 and delivery['localPackagingChecks']['allowlist']=='exact' and delivery['localPackagingChecks']['CRC']=='pass')
    with zipfile.ZipFile(RETURN) as z:
        infos=z.infolist(); names=[i.filename for i in infos]; name_set=set(names)
        ck('ZIP CRC test passes and member names are unique', z.testzip() is None and len(names)==len(name_set))
        safe=True
        for i in infos:
            p=PurePosixPath(i.filename)
            mode=(i.external_attr >> 16) & 0o170000
            if p.is_absolute() or '..' in p.parts or '\\' in i.filename or not i.filename or mode==stat.S_IFLNK: safe=False
        ck('ZIP member paths are safe regular paths', safe)
        manifest=json.loads(z.read('MEMBER_MANIFEST.json'))
        external_rows={r['path']:r for r in delivery['members']}
        internal_rows={r['path']:r for r in manifest['members']}
        ck('Exact 67-member allowlist agrees across ZIP, internal manifest and delivery', set(names)==set(manifest['archiveAllowlist']) and set(names)==(set(internal_rows)|{'MEMBER_MANIFEST.json'}) and set(names)==set(external_rows) and len(names)==manifest['archiveMemberCount']==delivery['archive']['memberCount']==67)
        ck('Self-binding policy excludes only manifest recursion', 'intentionally excluded' in manifest['selfBinding'] and 'MEMBER_MANIFEST.json' in manifest['archiveAllowlist'] and 'MEMBER_MANIFEST.json' in external_rows)
        member_hashes=True; extracted=[]
        for n in names:
            b=z.read(n); extracted.append((n,b))
            a=internal_rows.get(n); e=external_rows.get(n,{})
            crc=f'{zlib.crc32(b)&0xffffffff:08x}'
            member_hashes &= len(b)==e.get('bytes') and sha(b)==e.get('sha256') and crc==e.get('crc32')
            if a is not None:
                member_hashes &= len(b)==a.get('bytes') and sha(b)==a.get('sha256') and crc==a.get('crc32')
        ck('Every member byte count, SHA-256 and CRC matches both manifests',member_hashes)
        d={n:json.loads(z.read(n)) for n in ['COUNTS.json','DIRECTOR_DECISION.json','SOURCE_VERIFICATION.json','VALIDATION.json','CASEBOOK.json','CASE_DISPOSITIONS.json','PROCEDURES.json','QUESTION_DISPOSITIONS.json','HOLD_REGISTER.json','FUTURE_CASE_DISPOSITIONS.json','PROPOSED_CHANGES.json','ORIGINAL_OBLIGATIONS.json','ACCEPTED_INTERFACES.json','source/MANIFEST.json','source/CANDIDATE.json','source/CURRENT_AUTHORITY_UPDATE.json','source/SOURCE_CHECK.json']}
        counts=d['COUNTS.json']; decision=d['DIRECTOR_DECISION.json']; source=d['SOURCE_VERIFICATION.json']; validation=d['VALIDATION.json']; cases=d['CASEBOOK.json']; cdisp=d['CASE_DISPOSITIONS.json']; procedures=d['PROCEDURES.json']; qd=d['QUESTION_DISPOSITIONS.json']; holds=d['HOLD_REGISTER.json']; futures=d['FUTURE_CASE_DISPOSITIONS.json']; changes=d['PROPOSED_CHANGES.json']; obligations=d['ORIGINAL_OBLIGATIONS.json']; interfaces=d['ACCEPTED_INTERFACES.json']; source_manifest=d['source/MANIFEST.json']; source_candidate=d['source/CANDIDATE.json']; authority_update=d['source/CURRENT_AUTHORITY_UPDATE.json']; source_check=d['source/SOURCE_CHECK.json']
        nested_packet=z.read('source/DD_Rank8_Planar_5_Source_Conference_02.zip')
        packet_archive=zipfile.ZipFile(io.BytesIO(nested_packet))
        ck('Director decision is exact acceptance, unapplied, without rejects or blockers', decision['accepted'] is True and decision['applied'] is False and decision['acceptedIds']==IDS and decision['rejectedIds']==[] and decision['knownBlockingDefects']==[] and decision['authorityUsed']==AUTH and decision['canonicalAuthorityAfterThisWork'].startswith('Unchanged'))
        ck('Delivery and archive decision agree exactly', delivery['acceptedIds']==decision['acceptedIds'] and delivery['counts']==counts==decision['counts'] and delivery['applied']==decision['applied'])
        ck('All exact procedures present and still marked unapplied', [p['spellId'] for p in procedures]==IDS and all(p['applied'] is False for p in procedures) and all(ch['spellId']==sid and ch['applied'] is False for ch,sid in zip(changes,IDS)))
        ck('All 24 questions are selected and each answer matches its selected source option', len(qd)==counts['sourceQuestions']==24 and counts['answeredDispositions']==24 and all(q['selectedOptionIndex'] is not None and q['selectedOptionExact']==q['originalQuestion']['options'][q['selectedOptionIndex']] for q in qd))
        ck('All five exact proposed-change records are reversible two-operation proposals', [c['spellId'] for c in changes]==IDS and sum(len(c['forward'])+len(c['inverse']) for c in changes)==counts['proposalOperations']==20 and all(c['applied'] is False for c in changes))
        ck('Future obligations and historical obligations are preserved', len(futures)==counts['originalFutureObligations']==7 and len(obligations['questions'])==24 and len(obligations['futureCaseRequirements'])==7 and len(obligations['records'])==5 and all(x['qualificationsRetained'] for x in futures))
        ck('Casebook and dispositions agree on all 29 exact cases', len(cases)==len(cdisp)==counts['totalCases']==29 and {c['id'] for c in cases}=={c['id'] for c in cdisp} and all(next(x for x in cdisp if x['id']==c['id'])['finalSHA256']==c['finalSHA256'] for c in cases))
        event_count=sum(len(c['events']) for c in cases)
        event_ops=sum(len(e.get('forward',[]))+len(e.get('inverse',[])) for c in cases for e in c['events'])
        event_trace=True
        for c in cases:
            prior=None
            for e in c['events']:
                event_trace &= sha(canonical(e['before']))==e['beforeSHA256'] and sha(canonical(e['after']))==e['afterSHA256']
                if prior is not None: event_trace &= canonical(e['before'])==canonical(prior)
                prior=e['after']
            if c['events']:
                event_trace &= canonical(c['events'][-1]['after'])==canonical(c['finalState']) and sha(canonical(c['finalState']))==c['finalSHA256']
        ck('Event totals and canonical before/after/final state hash chains validate', event_count==counts['events']==213 and event_ops==counts['eventOperations']==852 and event_trace, {'events':event_count,'operations':event_ops})
        whole_held=[c['id'] for c in cases if c['wholeCaseHeld']]
        ck('All 17 holds retained and exactly 10 cases remain wholly held', len(holds)==counts['retainedHolds']==17 and all(h['status']=='retained' for h in holds) and len(whole_held)==counts['wholeCaseHeld']==10)
        ck('Both Gloom Bind main cases and both branches remain wholly held', {'P5-GLOOM-A','P5-GLOOM-B','P5-GLOOM-A/corpse-source-expiry','P5-GLOOM-B/actual-freeing'} <= set(whole_held))
        ck('No runtime, human-play, balance, cosmology, release or domain-closure approval is claimed', isinstance(decision['qualifications'],list) and any('No runtime, human play, balance, cosmology, release or domain closure approval' in q for q in decision['qualifications']) and validation.get('failed')==0)
        ck('Director validation reports all 7,770 checks passed', validation.get('checkCount')==7770 and validation.get('passed')==7770 and validation.get('failed')==0)
        ck('31 accepted comparison interfaces have hash rechecks',len(interfaces['comparisons'])==counts['acceptedComparisonInterfaces']==31 and len(source['interfaceEntryChecks'])==31 and all(x['authorityHashRecomputedMatches'] is True for x in source['interfaceEntryChecks']))
        ck('All 89 packet current-source bindings are verified and embedded byte-exactly',len(source['currentBindings'])==counts['sourceFilesBound']==89 and all(x['verified'] is True and len(packet_archive.read('sources/'+x['path']))==x['bytes'] and sha(packet_archive.read('sources/'+x['path']))==x['sha256'] for x in source['currentBindings']))
        live_sources=True
        for row in source['currentBindings']:
            p=ROOT/row['path']
            live_sources &= p.is_file() and p.stat().st_size==row['bytes'] and sha(p.read_bytes())==row['sha256']
        ck('All 89 source bindings still match current local working-tree files',live_sources)
        conference01=zipfile.ZipFile(io.BytesIO(packet_archive.read('historical/Conference01_ARCHIVE.zip')))
        historical_ok=True
        for row in source['resolvedRecordedBindings']:
            if 'declared' in row:
                b=conference01.read(row['resolvedMember']); decl=row['declared']
                historical_ok &= len(b)==decl['bytes'] and sha(b)==decl['sha256'] and row.get('verified') is True
            else:
                b=z.read(row['deliverable'])
                historical_ok &= len(b)==row['bytes'] and sha(b)==row['sha256']
        ck('All resolved historical accepted bindings match their archived or delivered bytes; five unavailable references remain listed separately',historical_ok and len(source['resolvedRecordedBindings'])==49 and len(source['unresolvedRecordedBindings'])==5)
        nested_packet=z.read('source/DD_Rank8_Planar_5_Source_Conference_02.zip')
        ck('Returned nested source conference is byte-exact to submitted Planar5 packet',nested_packet==PACKET.read_bytes() and sha(nested_packet)==decision['sourceArchive']['sha256'] and len(nested_packet)==decision['sourceArchive']['bytes'])
        ck('Returned candidate and source check match the submitted packet authority',z.read('source/CANDIDATE.json')==CANDIDATE.read_bytes() and source_check['failures']==0 and source_check['reviewIds']==IDS and source_check['currentAuthority']['reviewedApplied']==730 and source_check['currentAuthority']['pending']==118)
        ck('Returned source manifest binds the exact 89 current sources and source archive',len(source_manifest['currentSourceBindings'])==89 and source_manifest['candidate']['sha256']==sha(CANDIDATE.read_bytes()) and source_manifest['check']['sha256']==sha(z.read('source/SOURCE_CHECK.json')))
        ck('Submitted baseline index and catalog are unchanged at authority 730/118/0',source['authority']['reviewedApplied']==730 and source['authority']['pending']==118 and source['authority']['acceptedUnapplied']==0 and source['authority']['index']['sha256']==sha(INDEX.read_bytes()) and source['authority']['catalog']['sha256']==sha(CATALOG.read_bytes()))
        ck('Exact five IDs remain pending and no other status is changed by the return',authority_update['scopeIds']==IDS and authority_update['authority']=={**AUTH,'scopedInterfaces':173} and all(authority_update['index']['sha256']==sha(INDEX.read_bytes()) for _ in [0]) and all(source_candidate['currentAuthority'][k]==AUTH[k] for k in AUTH))
        ck('Return contains no new domain/runtime/playtest/release approval',source_candidate['newRuleAdoptions']==0 and source_candidate['runtimeTestsExecuted']==0 and source_candidate['humanPlaytests']==0 and source_candidate['wholeGameComplete'] is False and source['programsExecutedFromPacket'] is False)
        # Ensure exact submitted conference source archive has intact CRC and candidate checks too.
        with zipfile.ZipFile(PACKET) as pz:
            ck('Submitted Planar5 source archive CRC remains valid', pz.testzip() is None and len(pz.namelist())==98)
        # Preserve the exact return archive members for later application traceability.
        EXTRACTED.mkdir(exist_ok=True)
        for n,b in extracted:
            target=EXTRACTED/PurePosixPath(n)
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(b)
    passed=sum(1 for c in checks if c['passed'])
    report={'id':'PLANAR5-RETURN-INDEPENDENT-AUDIT-166','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if passed==len(checks) else 'FAIL','checkCount':len(checks),'checksPassed':passed,'checksFailed':len(checks)-passed,'checks':checks,'archive':{'path':RETURN.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':sha(raw),'members':expected_zip['memberCount']},'acceptedIds':IDS,'authorityBefore':AUTH,'counts':delivery['counts'],'extractedDirectory':EXTRACTED.relative_to(ROOT).as_posix()}
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':report['status'],'checkCount':len(checks),'checksPassed':passed,'checksFailed':len(checks)-passed,'failed':[c for c in checks if not c['passed']],'report':OUT.relative_to(ROOT).as_posix()},ensure_ascii=False,indent=2))
    if passed!=len(checks): raise SystemExit(2)

if __name__=='__main__': run()
