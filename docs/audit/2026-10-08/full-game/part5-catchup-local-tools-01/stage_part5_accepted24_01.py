"""Preserve reviewable accepted-spell integration inputs without applying membership."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import difflib
import hashlib
import json
import zipfile

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
OUT = A / 'part5-accepted24-integration-staging-01'
CHECK = A / 'PART5_ACCEPTED24_INTEGRATION_STAGING_01_CHECK.json'

def raw(p): return Path('\\\\?\\' + str(p)).read_bytes()
def obj(p): return json.loads(raw(p))
def digest(b): return hashlib.sha256(b).hexdigest()
def binding(p, b=None):
    b = raw(p) if b is None else b
    return {'path': p.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': digest(b)}
def exact(b, ref): return len(b) == ref['bytes'] and digest(b) == ref['sha256']
def enc(v): return (json.dumps(v, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
def pointer(v, p):
    for part in p.lstrip('/').split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        v = v[int(part)] if isinstance(v, list) else v[part]
    return v
def walk(v):
    yield v
    if isinstance(v, dict):
        for x in v.values(): yield from walk(x)
    elif isinstance(v, list):
        for x in v: yield from walk(x)

def main():
    assert not OUT.exists() and not CHECK.exists(), 'One-shot output already exists'
    checks = []
    def ck(label, condition):
        checks.append({'check': label, 'passed': bool(condition)})
        assert condition, label
    now = datetime.now(timezone.utc).isoformat()
    indexp = R / 'data/public/spell_playtests/authored_review_index.json'
    catalogp = R / 'data/public/spell_playtests/catalog.json'
    coveragep = R / 'data/playtest/game_development_coverage.json'
    registry = R / 'data/director/spell_review/accepted_interface_registry_06.json'
    protected = {p: raw(p) for p in (indexp, catalogp, coveragep, registry)}
    old = json.loads(protected[indexp]); preview = deepcopy(old)
    catalog = {x['id']: x for x in json.loads(protected[catalogp])['spells']}
    ck('Current applied index binding', digest(protected[indexp]) == '6f9b86e21f6a69c7ba2469aba89d5907aa08da567226a2c4bd3ced9e09409857')
    ck('Applied counts remain 525/323/249', old['authoredCounts'] == {'reviewed':525,'pending':323} and old['representationCounts']['completeReviewedStandaloneProcedures'] == 249)
    ck('All848 catalog and index identities present', len(catalog) == len(old['entries']) == 848 and set(catalog) == {e['id'] for e in old['entries']})
    nativep = A / 'GPT_PART5_EXACT_ACCEPTANCES_01_NATIVE.json'
    native = obj(nativep)
    defs = [
        ('companion-life10-exact-05', 'companion-life10-exact05-part5-return-01', 'DD_Companion_Life_10_Exact_05.zip', 'DD_Companion_Life_10_Exact_05_Part5_Return_01.zip', '161f6920c754e7a0c2d9ea4326be73ba22866912b9b7c81c8421f9d104d52522', 'bcc687cc-3169-46a9-a080-a287cbcb6c97', 10, 27, 20),
        ('illusion-perception14-exact-13', 'illusion-perception14-exact13-part5-return-01', 'DD_Illusion_Perception_14_Exact_13.zip', 'DD_Illusion_Perception_14_Exact_13_Part5_Return_01.zip', 'c75df814489fe42924ec03fe425565c2474e0080c62764f5188f49472be6eb19', '5f15c8ef-4194-43d9-98e1-ae2e945b21b6', 14, 28, 28),
    ]
    cohorts = []; changes = []; copies = []; staged_bytes = {}; drift = []; ids = []
    for slug, ret, submitted_name, returned_name, returnsha, replyid, count, casecount, originalcount in defs:
        root = A / slug; returnroot = A / ret; authp = returnroot / 'ACCEPTANCE.json'
        auth = obj(authp); reg = obj(root/'REGISTER.json'); model = obj(root/'SPELLS_MODEL.json'); cases = obj(root/'CASEBOOK.json'); sourcehash = obj(root/'SOURCE_HASHES.json')
        reply = next(v for v in walk(native) if isinstance(v, dict) and v.get('id') == replyid)
        ck(slug+' actual final and archive binding', auth['verdict'] in reply['text'] and returnsha in reply['text'] and digest(raw(A/returned_name)) == returnsha)
        expectedinput = auth['inputArchive'] if 'inputArchive' in auth else next(v for v in auth['inputArchives'] if v['filename'] == submitted_name)
        ck(slug+' submitted input exact', exact(raw(A/submitted_name), expectedinput))
        currentids = [s['id'] for s in model['spells']]
        dispositions = auth.get('individualSpellDispositions',auth.get('individualIdentityDispositions'))
        ck(slug+' accepted identities and order', currentids == reg['spellIds'] == [v.get('spellId',v.get('id')) for v in dispositions] and len(set(currentids)) == count and auth['acceptedSelectedIdentityCount'] == count)
        ck(slug+' zero artifact mutations', auth['artifactMutationCount'] == 0 and auth.get('operationCount',auth.get('requiredPointerOperations')) == 0)
        ck(slug+' runtime selection disabled', model['runtimeSelectionEnabled'] is False)
        candidatep = G / model['candidate']['path']; candidate = obj(candidatep)
        ck(slug+' complete selected candidate unchanged', exact(raw(candidatep), model['candidate']))
        with zipfile.ZipFile(A/submitted_name) as z, zipfile.ZipFile(A/returned_name) as rz:
            ck(slug+' original and returned ZIP integrity', z.testzip() is None and rz.testzip() is None)
            ck(slug+' acceptance preserved exactly', rz.read('ACCEPTANCE.json') == raw(authp))
            ck(slug+' eight unique accepted artifacts', len(auth['exactAcceptedArtifacts']) == len({b.get('filename',b.get('name')) for b in auth['exactAcceptedArtifacts']}) == 8)
            for b in auth['exactAcceptedArtifacts']:
                name = b.get('filename',b.get('name')); payload = raw(root/name)
                ck(slug+' four-way accepted bytes '+name, exact(payload,b) and payload == z.read('current/'+name) == rz.read('accepted/current/'+name) == raw(returnroot/'accepted/current'/name))
            for key, values in sourcehash.items():
                if not isinstance(values,list): continue
                for b in values:
                    if not isinstance(b,dict) or 'archivePath' not in b: continue
                    frozen = z.read(b['archivePath'])
                    ck(slug+' frozen full source '+key+' '+b['path'], exact(frozen,b))
                    if key == 'currentSources':
                        live = raw(G/b['path'])
                        if not exact(live,b):
                            ck(slug+' drift limited to direction progress', b['path'] == 'DescentReviewChanges/ReviewBible/docs/DEVELOPMENT_DIRECTION.md')
                            before = frozen.decode('utf-8-sig'); after = live.decode('utf-8-sig')
                            ck(slug+' direction contract unchanged', before.split('## Current continuation')[0] == after.split('## Current continuation')[0])
                            staged_bytes['evidence/DEVELOPMENT_DIRECTION_frozen.md'] = frozen
                            staged_bytes['evidence/DEVELOPMENT_DIRECTION_live_at_staging.md'] = live
                            delta = ''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='frozen',tofile='live'))
                            staged_bytes['evidence/DEVELOPMENT_DIRECTION_progress_only.diff'] = delta.encode('utf-8')
                            drift.append({'cohort':slug,'frozen':b,'live':binding(G/b['path']),'classification':'Progress/navigation/source-packet preparation changes only; video-game contract prefix unchanged. Reviewed full diff. Later status labels are themselves historical and superseded by actual acceptances.','delta':'evidence/DEVELOPMENT_DIRECTION_progress_only.diff'})
                        else: ck(slug+' live source exact '+b['path'],True)
        ck(slug+' full original and current case counts', len(cases['cases']) == casecount and len(cases['originalScenarioTextsUnchanged']) == originalcount)
        copy_map = reg['applicationPlan']['canonicalByteCopies']
        for name,dest in copy_map.items():
            p = G/dest; payload = raw(root/name)
            ck(slug+' canonical destination still absent '+name,not p.exists())
            stage = 'proposed-canonical/'+dest
            staged_bytes[stage] = payload
            copies.append({'cohort':slug,'source':binding(root/name),'stagedPath':stage,'proposedCanonicalDestination':binding(p,payload),'operation':'CREATE_BYTE_IDENTICAL_AFTER_AUTHORIZATION_AND_REVALIDATION','applied':False})
        public = G/copy_map['SPELLS_MODEL.json']; publicbinding = binding(public,raw(root/'SPELLS_MODEL.json'))
        aliases = {'SPELLS_MODEL.json':copy_map['SPELLS_MODEL.json'],'CASEBOOK.json':copy_map['CASEBOOK.json'],'REGISTER.json':(root/'REGISTER.json').relative_to(G).as_posix()}
        for n,s in enumerate(model['spells']):
            ident = s['id']; ids.append(ident)
            ck('Full source and access unchanged '+ident,s['completeSourceAndAccess'] == catalog[ident])
            ck('Selected full procedure unchanged '+ident,pointer(candidate,s['selectedProcedureSource']['pointer']) == s['procedure'])
            needed = s.get('sharedRuleIds',s.get('requiredSharedRuleIds'))
            ck('Every referenced shared clause present '+ident, bool(needed) and all(k in model['sharedRules'] for k in needed))
            entry = next(e for e in preview['entries'] if e['id'] == ident); before = deepcopy(entry)
            ck('Currently pending identity '+ident,entry['authoredStatus'] == 'pending-authored-procedure')
            entry['sourceCatalogWholeCardPointer'] = entry['wholeCardPointer']
            entry.update(authoredStatus='reviewed-authored-operational-playtest',procedureFile='../spell_candidates/'+public.name,procedurePointer=f'/spells/{n}',wholeCardPointer=f'/spells/{n}',wholeCardIdField='id',procedureTextPointer=f'/spells/{n}/procedure',sharedRulesPointer='/sharedRules',manuscript='../../../docs/spells/candidates/'+Path(copy_map['PLAYER_CHAPTER.md']).name,reviewId=auth['id'],runtimeSelectionEnabled=False,completeEnvelopeBinding=publicbinding,historicalCandidateLabelsPreserved=True,caseSourceReferenceAliases=aliases)
            ck('Proposed pointer resolves full identity '+ident,pointer(model,entry['wholeCardPointer'])['id'] == ident and pointer(model,entry['procedureTextPointer']) == s['procedure'])
            changes.append({'id':ident,'before':before,'proposedAfterWithoutApplicationReceipt':deepcopy(entry),'deferredRequiredBinding':'authoredAcceptanceReceipt must bind the actual separately verified future application receipt; no acceptance/application receipt is invented by this staging.'})
        holds = auth.get('wholeCaseContentHolds',auth.get('explicitHoldsUnchanged'))
        if count == 10:
            ck('Two exact CR2 whole-case holds retained with zero credit', [h['id'] for h in holds] == ['IN6-09-A','IN6-09-B'] and all(h['completionCredit'] == 0 and pointer(cases,h['caseRef']['pointer'])['id'] == h['id'] for h in holds))
        else:
            ck('All nine exact Illusion hold records retained',len(holds) == 9)
            ck('All three Illusion supplements retained',len(cases['supplementalCases']) == 3)
        cohorts.append({'id':slug,'actualAssistantMessageId':replyid,'acceptance':binding(authp),'verdict':auth['verdict'],'acceptedArchive':binding(A/submitted_name),'actualReturnArchive':binding(A/returned_name),'acceptedArtifactBindings':auth['exactAcceptedArtifacts'],'acceptedIds':currentids,'holdsVerbatim':holds,'explicitNonApprovalsVerbatim':auth['explicitNonApprovals'],'sharedRules':list(model['sharedRules']),'currentCases':casecount,'originalScenarios':originalcount,'applicationPerformed':False})
    ck('Exactly24 distinct accepted identities',len(ids) == len(set(ids)) == 24)
    ck('Exactly8 proposed byte-identical canonical copies',len(copies) == 8)
    unchanged = [a['id'] for a,b in zip(old['entries'],preview['entries']) if a['id'] not in ids and a == b]
    ck('All824 unrelated entries unchanged in memory',len(unchanged) == 824)
    ck('All848 identities and ordering preserved in memory',[e['id'] for e in old['entries']] == [e['id'] for e in preview['entries']])
    ck('Projected549 reviewed and299 unreviewed including preserved Blink receipt',sum(e['authoredStatus']=='reviewed-authored-operational-playtest' for e in preview['entries']) == 549 and sum(e['authoredStatus']!='reviewed-authored-operational-playtest' for e in preview['entries']) == 299)
    plan = {'id':'PART5-ACCEPTED24-INTEGRATION-STAGING-01','recordedAtUtc':now,'status':'PREPARED_NOT_APPLIED','developmentDirection':'video-game-only','scope':'Reviewable exact integration inputs only. Owner reserved implementation for a later Codex instruction. Neither live membership nor canonical destinations are changed.','actualNativeFinals':binding(nativep),'sourcePreservationReceipt':binding(A/'GPT_PART5_PERTINENT_RETURNS_01_RECEIPT.json'),'liveIndexPrecondition':binding(indexp),'sourceCatalogPrecondition':binding(catalogp),'cohorts':cohorts,'canonicalCopies':copies,'membershipChanges':changes,'sourceSnapshotDrift':drift,'appliedCountsUnchanged':{'reviewed':525,'pending':323,'standalone':249},'projectedCountsAfterFutureVerifiedApplication':{'reviewed':549,'pending':299,'standalone':273},'additionalEnvelopeRegistrationsRequired':[{'file':'../spell_candidates/'+Path(c['proposedCanonicalDestination']['path']).name,'binding':c['proposedCanonicalDestination'],'receipt':'DEFERRED_ACTUAL_APPLICATION_RECEIPT_REQUIRED'} for c in copies if c['source']['path'].endswith('/SPELLS_MODEL.json')],'remainingApplicationSteps':['Obtain the owner instruction reserved in actual GPT turn ee46d85a-5148-43c3-b3cb-a695ba7e783d.','Revalidate every input, current source, live index and destination. If membership changed, recompute from the actual current index and preserve unrelated entries.','Write actual per-cohort application receipts binding unchanged exact artifacts, actual acceptances, preserved holds and live before/after counts.','Copy eight exact canonical files, add the24 entries and two standalone envelope records using the real receipt bindings, then validate all references and unchanged catalog/domain gates.','Update live navigation/queue/checkpoint only after application; preserve every prior snapshot.'],'sixControlReadyCorrections':'Separate proposed change set; not applied or included in these exact payloads. Control15 full conference is still in progress.','liveIndexModified':False,'canonicalDestinationsCreated':False,'runtimeSelectionEnabled':False,'runtimeTestsExecuted':0,'humanPlaytested':False,'numericalBalanceApproved':False,'cosmologyCanonModified':False,'domainGatesChanged':False,'sourceInformationDeleted':0,'pushed':False}
    staged_bytes['INTEGRATION_PLAN.json'] = enc(plan)
    staged_bytes['evidence/authored_review_index_before.json'] = protected[indexp]
    staged_bytes['README.md'] = ("# Part5 accepted24 — prepared integration, not applied\n\nActual GPT accepted Companion10 Exact05 and Illusion14 Exact13 with unchanged bytes and existing holds. This directory stages eight canonical copies and a complete24-entry change plan. It changes no live rules, membership, canonical destinations or runtime flags.\n\nThe applied baseline remains **525 reviewed /323 pending /249 standalone**. **549/299/273 is a projection only.** `INTEGRATION_PLAN.json` preserves full before entries, proposed after fields, actual acceptance bindings and all11 hold records. A real future application receipt must be generated; no placeholder receipt is operative.\n\nBoth Command Undeath cases retain zero completion credit. Illusion's nine holds remain unchanged. The six Control/Ready corrections are separate proposed work. The owner reserved implementation for a later instruction.\n\nThe single source drift is the direction document's progress/navigation section; the unchanged video-game contract and complete before/after bytes plus diff are preserved. The historical status labels inside frozen artifacts remain historical.\n\nNo engine testing, human playtesting, balance, cosmology,75-domain, whole-game or release approval is inferred. Nothing has been deleted.\n").encode('utf-8')
    OUT.mkdir()
    for name,payload in staged_bytes.items():
        p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(payload)
        ck('Staged bytes verified '+name,raw(p)==payload)
    for p,b in protected.items(): ck('Protected live file unchanged '+p.relative_to(G).as_posix(),raw(p)==b)
    for copy in copies: ck('No canonical installation '+copy['proposedCanonicalDestination']['path'],not (G/copy['proposedCanonicalDestination']['path']).exists())
    manifest={'id':'PART5-ACCEPTED24-INTEGRATION-STAGING-01-MANIFEST','files':[binding(OUT/name) for name in staged_bytes],'scope':'Staged inputs, not operative project files.'}
    (OUT/'MANIFEST.json').write_bytes(enc(manifest))
    CHECK.write_bytes(enc({'recordedAtUtc':now,'scope':'Source/artifact preservation, pending identity and staged pointer checks only; no applied membership or runtime tests.','plan':binding(OUT/'INTEGRATION_PLAN.json'),'manifest':binding(OUT/'MANIFEST.json'),'checkCount':len(checks),'failureCount':0,'checks':checks,'appliedCounts':plan['appliedCountsUnchanged'],'projectedCounts':plan['projectedCountsAfterFutureVerifiedApplication'],'sourceDriftCount':len(drift),'sourceInformationDeleted':0,'runtimeTestsExecuted':0}))
    print(json.dumps({'plan':binding(OUT/'INTEGRATION_PLAN.json'),'check':binding(CHECK),'checks':len(checks),'applied':False,'counts':plan['appliedCountsUnchanged'],'proposedCanonicalCopies':len(copies),'sourceDrifts':len(drift)}))

if __name__ == '__main__': main()
