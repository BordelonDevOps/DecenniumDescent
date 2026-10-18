"""Apply the exact Director-accepted AC6 package without rewriting accepted payloads."""
from copy import deepcopy
from datetime import datetime, timezone
import json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at

def read(p): return json.loads(p.read_bytes())

def leaves(value):
    if isinstance(value,str): yield value
    elif isinstance(value,dict):
        for child in value.values(): yield from leaves(child)
    elif isinstance(value,list):
        for child in value: yield from leaves(child)

def main():
    now = datetime.now(timezone.utc).isoformat()
    candidate = A/'ac6-semantic-current-06'
    authority = A/'ac6-exact-acceptance-06/REVIEW.json'
    archive = A/'DD_AC6_Semantic_Current_06_Review.zip'
    input_archive = A/'DD_AC6_Semantic_Current_06.zip'
    receipt = A/'AC6_EXACT_ACCEPTANCE_06_RECEIPT.json'
    report = A/'AC6_EXACT_ACCEPTANCE_06_APPLICATION_CHECK.json'
    operations = A/'AC6_EXACT_ACCEPTANCE_06_OPERATIONS.json'
    keep = A/'source-before-ac6-exact-acceptance-06'
    public = R/'data/public/spell_candidates/abjuration_conjuration_rank6_reviewed_06.json'
    cases_target = R/'data/playtest/spell_candidates/abjuration_conjuration_rank6_cases_06.json'
    player = R/'docs/spells/candidates/ABJURATION_CONJURATION_RANK6_REVIEWED_06.md'
    director = R/'docs/director-only/spells/ABJURATION_CONJURATION_RANK6_REVIEWED_06.md'
    statusfile = R/'docs/mechanics/ABJURATION_CONJURATION_RANK6_REVIEW_STATUS.json'
    assert not any(p.exists() for p in [receipt, report, operations, keep, public, cases_target, player, director, statusfile])
    checks = []
    def ck(name, passed):
        checks.append({'name': name, 'passed': bool(passed)})
        assert passed, name
    auth = read(authority)
    ck('Exact recovered archive', info(archive)['bytes'] == 6039 and info(archive)['sha256'] == '26b1bb61248744f1fdd8bec3d728a694cc7a9cadcc6a1f2b91bdd2f86e53be7a')
    with zipfile.ZipFile(archive) as z:
        ck('Two safe unique review members', sorted(z.namelist()) == ['REVIEW.json', 'VERDICT.md'])
        for name in z.namelist(): ck('Exact recovered member '+name, z.read(name) == (authority.parent/name).read_bytes())
    native = read(A/'AC6_EXACT_ACCEPTANCE_06_ACTUAL_NATIVE.json')
    turn = native['turns'][0]
    reply = next(x for x in turn['items'] if x['type'] == 'agentMessage')
    ck('Actual notebook recovery turn', turn['id'] == '8dadecd9-9a83-4263-b977-f357a81414d5' and reply['id'] == '76d2a680-1cb9-4266-b8f0-2cd76f10ef23')
    ck('Actual notebook identifies review archive', info(archive)['sha256'] in reply['text'] and auth['id'] in reply['text'])
    ck('Affirmative bounded verdict', auth['verdict'] == 'ACCEPT_BYTE_IDENTICAL_FOR_PROVISIONAL_AUTHORED_AC6_CAMPAIGN_PLAYTEST_CANDIDATE' and auth['finalCoherenceFinding']['blockingAuthoredCoherenceFindingsRemaining'] == 0 and auth['moduleIdentity']['currentFilesMayRemainByteIdentical'])
    ck('Exact accepted submission', all(info(input_archive)[k] == auth['reviewedInputArchive'][k] for k in ['bytes', 'sha256']))
    expected = {'REGISTER.json', 'SPELLS_MODEL.json', 'PLAYER_CHAPTER.md', 'DIRECTOR_REVIEW.md', 'CASEBOOK.json', 'SOURCE_HASHES.json', 'VERDICT.md', 'EVIDENCE_MANIFEST.json'}
    ck('Eight accepted bindings', len(auth['acceptedCurrentArtifactBindings']) == 8 and {b['name'] for b in auth['acceptedCurrentArtifactBindings']} == expected)
    sources = read(candidate/'SOURCE_HASHES.json')['bindings']
    with zipfile.ZipFile(input_archive) as z:
        original = json.loads(z.read('CURRENT_REVIEW_INPUT.json'))
        for b in auth['acceptedCurrentArtifactBindings']:
            ck('Accepted payload exact '+b['name'], all(info(candidate/b['name'])[k] == b[k] for k in ['bytes', 'sha256']))
            ck('Submission payload exact '+b['name'], z.read('current/'+b['name']) == (candidate/b['name']).read_bytes())
        ck('103 frozen bindings', len(sources) == auth['sourceVerification']['frozenBindingCount'] == 103 and auth['sourceVerification']['allFrozenSourceBytesAndHashesVerified'] and not auth['sourceVerification']['failures'])
        for b in sources:
            ck('Current source exact '+b['path'], info(G/b['path']) == b)
            ck('Submitted frozen source exact '+b['path'], z.read('sources/'+b['path']) == (G/b['path']).read_bytes())
    for b in read(candidate/'EVIDENCE_MANIFEST.json')['files']:
        ck('Manifest binding '+b['name'], all(info(candidate/b['name'])[k] == b[k] for k in ['bytes', 'sha256']))
    local = read(A/'AC6_SEMANTIC_CURRENT_06_CHECK.json')
    ck('Bound independent focused check', local['checkCount'] == 851 and local['failureCount'] == 0 and info(A/'AC6_SEMANTIC_CURRENT_06_CHECK.json') == read(A/'AC6_SEMANTIC_CURRENT_06_PREPARATION.json')['independentCheck'])
    ck('All eight local dispositions agreed', [x['id'] for x in auth['dispositions']] == [f'AC6-L06-{i:02}' for i in range(1,9)] and all(x['verdict'] == ('AGREE_WITH_NEW_SCOPED_AUTHORSHIP' if x['id'] == 'AC6-L06-06' else 'AGREE') for x in auth['dispositions']))
    model, cb, register = [read(candidate/n) for n in ['SPELLS_MODEL.json', 'CASEBOOK.json', 'REGISTER.json']]
    ids = [s['id'] for s in model['spells']]
    ck('14 identities and order', len(ids) == len(set(ids)) == 14 and ids == register['spellIds'] == [s['spellId'] for s in original['records']])
    ck('16 printed placements', sum(len(s['completeSourceAndAccess']['source']['original']['placements']) for s in model['spells']) == 16 == auth['moduleIdentity']['printedPlacementCount'])
    ck('55 current cases', len(cb['cases']) == len({c['id'] for c in cb['cases']}) == auth['moduleIdentity']['currentCaseCount'] == 55)
    ck('51 original scenario identities retained', [c['id'] for c in cb['cases'][:51]] == [c['id'] for c in original['currentExamples']] == [c['caseId'] for c in register['caseScenarioCoverage']])
    ck('22 exact historical texts', cb['historicalOriginalTexts'] == original['originalExamplesUnchanged'] and len(cb['historicalOriginalTexts']) == 22)
    ck('All original scenario requirements retained', cb['originalRequiredExamples'] == original['originalRequiredExamplesUnchanged'])
    catalog = R/'data/public/spell_playtests/catalog.json'
    catalog_binding = info(catalog)
    byid = {s['id']: s for s in read(catalog)['spells']}
    for s, old in zip(model['spells'], original['records']):
        ck('Complete original source/access '+s['id'], s['completeSourceAndAccess'] == old['completeSourceAndAccess'] == byid[s['id']])
        ck('Historical question and record '+s['id'], s['historicalQuestionAndRecord'] == old['historicalQuestionAndRecord'])
        for chapter in ['PLAYER_CHAPTER.md', 'DIRECTOR_REVIEW.md']:
            text=(candidate/chapter).read_text(encoding='utf8')
            for part,leaf in enumerate(leaves(s['procedure'])):
                ck('Complete procedure in '+chapter+' '+s['id']+':'+str(part), leaf in text)
    ck('Bounded acceptance claims retained', all(v is False for v in auth['boundedStatus'].values()))
    copies = [(public, candidate/'SPELLS_MODEL.json'), (cases_target, candidate/'CASEBOOK.json'), (player, candidate/'PLAYER_CHAPTER.md'), (director, candidate/'DIRECTOR_REVIEW.md')]
    public_binding = info(public, (candidate/'SPELLS_MODEL.json').read_bytes())
    aliases = {'SPELLS_MODEL.json': public.relative_to(G).as_posix(), 'REGISTER.json': (candidate/'REGISTER.json').relative_to(G).as_posix(), 'CASEBOOK.json': cases_target.relative_to(G).as_posix()}
    rec = {'reviewId': auth['id'], 'recordedAtUtc': now, 'status': 'exact-authored-acceptance-applied', 'developmentDirection': 'video-game-only', 'acceptanceAuthority': info(authority), 'acceptanceArchive': info(archive), 'reviewedArchive': info(input_archive), 'actualGptReply': info(A/'AC6_EXACT_ACCEPTANCE_06_ACTUAL_NATIVE.json'), 'acceptedArtifactBindings': [info(candidate/b['name']) for b in auth['acceptedCurrentArtifactBindings']], 'independentLocalCorrectionReview': info(A/'AC6_SEMANTIC_CURRENT_06_CHECK.json'), 'acceptedSpellIds': ids, 'sourceFiles': 103, 'placements': 16, 'authoredCases': 55, 'originalScenarioObligations': 51, 'preservedHistoricalScenarioTexts': 22, 'canonicalCopies': [{'source': info(src), 'destination': info(dst, src.read_bytes()), 'byteIdentical': True} for dst,src in copies], 'completeEnvelope': public_binding, 'normalization': 'None. Exact accepted payloads copied byte-for-byte; current acceptance lives in receipt/status/index. Historical candidate and campaign-playtest wording retained as source history under video-game-only direction.', 'caseSourceReferenceAliases': aliases, 'authoredCountsBefore': {'reviewed':451,'pending':397}, 'authoredCountsAfter': {'reviewed':465,'pending':383}, 'catalogSourceAndAccessUnchanged': True, 'runtimeSelectionEnabled': False, 'runtimeImplemented': False, 'runtimeTestsExecuted': 0, 'humanBalanceApproved': False, 'wholeGameFlowConfirmed': False, 'sourceInformationDeleted': 0, 'pushed': False}
    receipt_raw = encoded(rec)
    receipt_binding = info(receipt, receipt_raw)
    indexp = R/'data/public/spell_playtests/authored_review_index.json'
    before_index = indexp.read_bytes(); oldindex = json.loads(before_index); index = deepcopy(oldindex)
    ck('451/397 baseline', index['authoredCounts'] == {'reviewed':451,'pending':397})
    ck('Catalog binding', index['sourceCatalogSha256'] == catalog_binding['sha256'])
    for n, ident in enumerate(ids):
        e = next(e for e in index['entries'] if e['id'] == ident)
        ck('Pending before application '+ident, e['authoredStatus'] == 'pending-authored-procedure')
        e['sourceCatalogWholeCardPointer'] = e['wholeCardPointer']
        e.update(authoredStatus='reviewed-authored-operational-playtest', procedureFile='../spell_candidates/abjuration_conjuration_rank6_reviewed_06.json', procedurePointer=f'/spells/{n}', wholeCardPointer=f'/spells/{n}', wholeCardIdField='id', procedureTextPointer=f'/spells/{n}/procedure', sharedRulesPointer='/sharedRules', manuscript='../../../docs/spells/candidates/ABJURATION_CONJURATION_RANK6_REVIEWED_06.md', reviewId=auth['id'], runtimeSelectionEnabled=False, completeEnvelopeBinding=public_binding, authoredAcceptanceReceipt=receipt_binding, historicalCandidateLabelsPreserved=True, caseSourceReferenceAliases=aliases)
        ck('Complete index discovery '+ident, at(model,e['wholeCardPointer'])['id'] == ident and at(model,e['procedureTextPointer']) == model['spells'][n]['procedure'])
    index['authoredCounts'] = {'reviewed':465,'pending':383}
    ck('175 prior standalone procedures', index['representationCounts']['completeReviewedStandaloneProcedures'] == 175)
    index['representationCounts']['completeReviewedStandaloneProcedures'] = 189
    index.setdefault('additionalStandaloneEnvelopes',[]).append({'file':'../spell_candidates/abjuration_conjuration_rank6_reviewed_06.json','binding':public_binding,'reviewId':auth['id'],'acceptedIds':ids,'authority':info(authority),'receipt':receipt_binding})
    for old,new in zip(oldindex['entries'],index['entries']):
        if old['id'] not in ids: ck('Unrelated entry unchanged '+old['id'], old == new)
    ck('All 848 identity order retained', len(index['entries']) == 848 and [x['id'] for x in index['entries']] == [x['id'] for x in oldindex['entries']])
    ck('Membership counts', sum(x['authoredStatus']=='reviewed-authored-operational-playtest' for x in index['entries']) == 465 and sum(x['authoredStatus']=='pending-authored-procedure' for x in index['entries']) == 382 and sum(x['authoredStatus']=='receipt-only-post-push-cosmology' for x in index['entries']) == 1)
    # Preserve the current integration guide's exact bytes for registry inheritance.
    # Discovery of the newly accepted cohort is supplied by this status file and index.
    q = keep/indexp.relative_to(G); q.parent.mkdir(parents=True,exist_ok=True); q.write_bytes(before_index)
    ck('Original index preserved', q.read_bytes() == before_index)
    change = {'before':{**info(indexp,before_index),'preservedCopy':q.relative_to(G).as_posix()},'after':info(indexp,encoded(index)),'scope':'Fourteen exact accepted memberships and complete-model discovery; no source catalog edits'}
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded([change['before']]))
    for dst,src in copies:
        dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes(src.read_bytes()); ck('Exact canonical copy '+dst.name, dst.read_bytes() == src.read_bytes())
    receipt.write_bytes(receipt_raw)
    assert indexp.read_bytes() == before_index
    indexp.write_bytes(encoded(index))
    ck('Exact planned index', info(indexp) == change['after'])
    ck('Original catalog unchanged', info(catalog) == catalog_binding)
    for b in sources:
        p=G/b['path']
        ck('Reviewed source preserved after application '+b['path'], info(p) == b if p != indexp else all(info(q)[k] == b[k] for k in ['bytes','sha256']))
    statusfile.write_bytes(encoded({'reviewId':auth['id'],'status':'Reviewed authored video-game candidate; runtime, gameplay and balance pending','receipt':info(receipt),'completeExactModel':info(public),'playerChapter':info(player),'directorChapter':info(director),'authoredCases':info(cases_target),'caseSourceReferenceAliases':aliases,'acceptedSpellIds':ids,'caseCount':55,'historicalPayloadLabelsPreserved':True,'sourceInformationDeleted':0,'runtimeSelectionEnabled':False}))
    operations.write_bytes(encoded({'recordedAtUtc':now,'authority':info(authority),'receipt':info(receipt),'changes':[change],'canonicalCopies':[info(p) for p,_ in copies],'sourceInformationDeleted':0,'originalCatalogUnchanged':True}))
    report.write_bytes(encoded({'recordedAtUtc':now,'scope':'Exact acceptance, source preservation, scenario identity/text preservation and authored application; no new semantic review or engine execution','receipt':info(receipt),'operations':info(operations),'checks':checks,'checkCount':len(checks),'failureCount':0,'authoredCounts':index['authoredCounts'],'runtimeTestsExecuted':0,'humanPlaytested':False,'sourceInformationDeleted':0}))
    print(json.dumps({'receipt':info(receipt),'applicationCheck':info(report),'checks':len(checks),'failures':0,'authoredCounts':index['authoredCounts']}))

if __name__ == '__main__': main()
