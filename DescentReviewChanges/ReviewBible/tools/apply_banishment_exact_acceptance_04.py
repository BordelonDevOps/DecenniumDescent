"""Apply the jointly accepted ordinary Banishment manuscript with preserved sources."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest


def read(p):
    return json.loads(p.read_bytes())


def main():
    candidate = A / 'banishment-repair-04-return'
    authority = A / 'banishment-exact-acceptance-04/ACCEPTANCE.json'
    acceptance_manifest = A / 'banishment-exact-acceptance-04/EVIDENCE_MANIFEST.json'
    receipt = A / 'BANISHMENT_EXACT_ACCEPTANCE_04_RECEIPT.json'
    report = A / 'BANISHMENT_EXACT_ACCEPTANCE_04_APPLICATION_CHECK.json'
    operations = A / 'BANISHMENT_EXACT_ACCEPTANCE_04_OPERATIONS.json'
    keep = A / 'source-before-banishment-exact-acceptance-04'
    exact = R / 'data/public/spell_candidates/banishment_exact_model_04.json'
    public = R / 'data/public/spell_candidates/banishment_reviewed_04.json'
    case_target = R / 'data/playtest/spell_candidates/banishment_cases_04.json'
    player = R / 'docs/spells/candidates/BANISHMENT_REVIEWED_04.md'
    director = R / 'docs/director-only/spells/BANISHMENT_REVIEWED_04.md'
    statusfile = R / 'docs/mechanics/BANISHMENT_REVIEW_STATUS.json'
    assert not any(p.exists() for p in [receipt,report,operations,keep,exact,public,case_target,player,director,statusfile])
    auth = read(authority)
    checks = []

    def ck(name, passed):
        checks.append({'name':name,'passed':bool(passed)})
        assert passed, name

    ck('exact acceptance authority bytes', info(authority)['bytes']==5925 and info(authority)['sha256']=='e8eb20e62bcd8b82c953101b99b29e78185610eac3987b65d4295a1a7dafc176')
    ck('affirmative bounded verdict',auth['verdict']=='ACCEPT FOR PROVISIONAL AUTHORED PLAYTEST APPLICATION' and auth['finalCoherenceFinding']['blockingAuthoredCoherenceFindingsRemaining']==0)
    reviewed = info(A/'DD_Banishment_Repair_04_Return.zip')
    ck('exact reviewed archive',all(reviewed[k]==auth['reviewedArtifact'][k] for k in ['bytes','sha256']))
    ck('acceptance manifest agrees',read(acceptance_manifest)['acceptedArtifactBindings']==auth['acceptedArtifactBindings'])
    for b in auth['acceptedArtifactBindings']:
        ck('accepted payload '+b['name'],all(info(candidate/b['name'])[k]==b[k] for k in ['bytes','sha256']))
    sources = read(candidate/'SOURCE_HASHES.json')['bindings']
    for b in sources:
        ck('reviewed source current before application '+b['path'],info(G/b['path'])==b)
    audit = read(A/'BANISHMENT_REPAIR_04_LOCAL_AUDIT.json')
    ck('independent review passed',audit['failureCount']==0 and not audit['remainingBlockingFindings'])
    model = read(candidate/'SPELL_MODEL.json')
    cases = read(candidate/'CASEBOOK.json')
    ck('37 accepted case identities',auth['preservation']['caseIds']==[c['id'] for c in cases['cases']] and len(cases['cases'])==37)
    ck('7 scoped authored rules',auth['preservation']['newScopedRuleIds']==[r['id'] for r in read(candidate/'REGISTER.json')['newScopedRules']])
    catalog = R/'data/public/spell_playtests/catalog.json'
    catalog_before = info(catalog)
    ck('source card exact',read(catalog)['spells'][46]==model['sourceAndAccess'])
    # A discovery envelope adds only identity/authority metadata. Every accepted model key/value is retained.
    card = {'spellId':'banishment','name':'Banishment',**deepcopy(model)}
    wrapper = {'schemaVersion':'1.0','status':'Reviewed authored operational-playtest manuscript; runtime and human balance pending',
               'reviewId':auth['id'],'acceptedExactModel':info(exact,(candidate/'SPELL_MODEL.json').read_bytes()),
               'acceptanceAuthority':info(authority),'normalization':'Adds spellId/name and an outer discovery envelope only; all accepted model key/value pairs remain exact.',
               'spells':[card]}
    ck('all accepted model values retained in discovery card',{k:card[k] for k in model}==model)
    public_bytes = encoded(wrapper)
    public_binding = info(public,public_bytes)
    copies = [(exact,candidate/'SPELL_MODEL.json'),(case_target,candidate/'CASEBOOK.json'),(player,candidate/'PLAYER_CHAPTER.md'),(director,candidate/'DIRECTOR_REVIEW.md')]
    aliases = {'SPELL_MODEL.json':exact.relative_to(G).as_posix()}
    now = datetime.now(timezone.utc).isoformat()
    rec = {
        'reviewId':auth['id'],'recordedAtUtc':now,'status':'exact-authored-acceptance-applied',
        'acceptanceAuthority':info(authority),'acceptanceArchive':info(A/'DD_Banishment_Exact_Acceptance_04.zip'),
        'reviewedArchive':reviewed,'observedTerminalReply':info(A/'BANISHMENT_EXACT_ACCEPTANCE_04_ACTUAL_DOM.txt'),
        'acceptedArtifactBindings':[info(candidate/b['name']) for b in auth['acceptedArtifactBindings']],
        'independentReview':info(A/'BANISHMENT_REPAIR_04_LOCAL_AUDIT.json'),
        'acceptedSpellIds':['banishment'],'sourceFiles':49,'authoredCases':37,'preservedHistoricalScenarioObjects':28,
        'newScopedRuleIds':auth['preservation']['newScopedRuleIds'],
        'canonicalCopies':[{'source':info(src),'destination':info(dst,src.read_bytes()),'byteIdentical':True} for dst,src in copies],
        'discoveryEnvelope':public_binding,'discoveryNormalization':'Metadata-only outer wrapper and identity labels; complete accepted model retained.',
        'caseSourceReferenceAliases':aliases,
        'authoredCountsBefore':{'reviewed':434,'pending':414},'authoredCountsAfter':{'reviewed':435,'pending':413},
        'historicalCandidateLabelsPreserved':True,'catalogSourceAndAccessUnchanged':True,
        'runtimeSelectionEnabled':False,'runtimeImplemented':False,'runtimeTestsExecuted':0,
        'humanBalanceApproved':False,'wholeGameFlowConfirmed':False,'sourceInformationDeleted':0,'pushed':False,
    }
    receipt_bytes = encoded(rec)
    receipt_binding = info(receipt,receipt_bytes)
    indexp = R/'data/public/spell_playtests/authored_review_index.json'
    before_index = indexp.read_bytes()
    oldindex = json.loads(before_index)
    index = deepcopy(oldindex)
    ck('current434/414 baseline',index['authoredCounts']=={'reviewed':434,'pending':414})
    ck('source catalog binding valid',index['sourceCatalogSha256']==catalog_before['sha256'])
    entry = next(e for e in index['entries'] if e['id']=='banishment')
    ck('Banishment still pending before application',entry['authoredStatus']=='pending-authored-procedure')
    entry['sourceCatalogWholeCardPointer']=entry['wholeCardPointer']
    entry.update(authoredStatus='reviewed-authored-operational-playtest',procedureFile='../spell_candidates/banishment_reviewed_04.json',procedurePointer='/spells/0',wholeCardPointer='/spells/0',wholeCardIdField='spellId',structuredProcedurePointer='/spells/0/procedure',manuscript='../../../docs/spells/candidates/BANISHMENT_REVIEWED_04.md',reviewId=auth['id'],runtimeSelectionEnabled=False,completeEnvelopeBinding=public_binding,authoredAcceptanceReceipt=receipt_binding,historicalCandidateLabelsPreserved=True,caseSourceReferenceAliases=aliases)
    index['authoredCounts']={'reviewed':435,'pending':413}
    ck('prior standalone representation158',index['representationCounts']['completeReviewedStandaloneProcedures']==158)
    index['representationCounts']['completeReviewedStandaloneProcedures']=159
    index.setdefault('additionalStandaloneEnvelopes',[]).append({'file':'../spell_candidates/banishment_reviewed_04.json','binding':public_binding,'reviewId':auth['id'],'acceptedIds':['banishment'],'authority':info(authority),'receipt':receipt_binding})
    for old,new in zip(oldindex['entries'],index['entries']):
        if old['id']!='banishment':
            ck('unrelated authored entry preserved '+old['id'],old==new)
    ck('all848identities/order retained',[x['id'] for x in oldindex['entries']]==[x['id'] for x in index['entries']])
    ck('actual435 reviewed memberships',sum(e['authoredStatus']=='reviewed-authored-operational-playtest' for e in index['entries'])==435)
    guide = R/'docs/mechanics/SPELL_INTEGRATION_RULES.md'
    before_guide = guide.read_bytes()
    newline = '\r\n' if b'\r\n' in before_guide else '\n'
    addition = newline.join([
        '', '', '## Ordinary Banishment — reviewed provisional interface', '',
        'The [complete Banishment manuscript](../spells/candidates/BANISHMENT_REVIEWED_04.md), [structured discovery record](../../data/public/spell_candidates/banishment_reviewed_04.json), and [exact acceptance receipt](../../../../docs/audit/2026-10-08/full-game/BANISHMENT_EXACT_ACCEPTANCE_04_RECEIPT.json) now govern this one ordinary spell. Earlier source-only or pre-push sequencing labels remain historical evidence. Cleric Banish Unholy remains separate.', '',
        'The accepted procedure preserves the original source/access and explicitly authors its CHA save, 60 elapsed-second concentration, shared hard-control and one-live guards. BAN-TRANSPORT-CLASS-02 treats this spell only as planar/extradimensional displacement rather than teleportation; exact Paladin predicates remain distinct. Mandatory body endings, all real clocks and custody identities persist. BAN-CLOSE-03 ends exile on time and returns extant identities to the recorded origin plane, with only its stated terminal transport-prevention exception. Physical fitting uses the existing body placement order. NEW BAN-CONFLICT-04 supplies a fixed logical anchor only for a resulting Banishment-origin placement conflict, preserving actual source/terrain tests and independent legal relocation; it does not change the global body rule or grant legal occupancy, generic immunity or movement.', '',
        'This acceptance is a source-linked authored playtest procedure. It does not enable runtime selection, establish named cosmology or natural/soul origins, or certify numerical balance, human playtesting or whole-game completion.', ''
    ]).encode('utf8')
    after_guide = before_guide + addition
    planned = [(indexp,before_index,encoded(index),'one authored membership and explicit complete procedure discovery'),(guide,before_guide,after_guide,'append scoped accepted interface; all existing text preserved')]
    preserved = []
    for p,before,after,scope in planned:
        ck('current mutation target '+str(p),p.read_bytes()==before)
        q=keep/p.relative_to(G);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(before)
        ck('preserved exact prior bytes '+str(p),q.read_bytes()==before)
        preserved.append({'before':{**info(p,before),'preservedCopy':q.relative_to(G).as_posix()},'after':info(p,after),'scope':scope})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded([p['before'] for p in preserved]))
    for dst,src in copies:
        dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(src.read_bytes())
        ck('canonical exact copy '+dst.relative_to(G).as_posix(),dst.read_bytes()==src.read_bytes())
    public.write_bytes(public_bytes)
    receipt.write_bytes(receipt_bytes)
    for p,before,after,_ in planned:
        assert p.read_bytes()==before;p.write_bytes(after)
        ck('applied exact planned bytes '+str(p),p.read_bytes()==after)
    ck('catalog wholly unchanged',info(catalog)==catalog_before)
    ck('discovery model retained after write',{k:read(public)['spells'][0][k] for k in model}==model)
    ck('all37canonical cases exact',read(case_target)==cases)
    statusfile.write_bytes(encoded({'reviewId':auth['id'],'status':'REVIEWED authored operational-playtest manuscript; runtime and human balance pending','receipt':info(receipt),'exactModel':info(exact),'completeDiscoveryEnvelope':info(public),'playerChapter':info(player),'directorChapter':info(director),'authoredCases':info(case_target),'caseSourceReferenceAliases':aliases,'acceptedSpellIds':['banishment'],'caseCount':37,'sourceInformationDeleted':0,'runtimeSelectionEnabled':False}))
    operations.write_bytes(encoded({'recordedAtUtc':now,'authority':info(authority),'receipt':info(receipt),'changes':preserved,'canonicalCopies':[info(p) for p,_ in copies],'discoveryEnvelope':info(public),'sourceInformationDeleted':0,'originalCatalogUnchanged':True}))
    report.write_bytes(encoded({'recordedAtUtc':now,'scope':'Exact acceptance, source preservation and authored application checks; no runtime or human tests','authority':info(authority),'receipt':info(receipt),'operations':info(operations),'checks':checks,'checkCount':len(checks),'failureCount':0,'authoredCounts':index['authoredCounts'],'runtimeTestsExecuted':0,'humanPlaytested':False,'sourceInformationDeleted':0}))
    print(json.dumps({'receipt':info(receipt),'applicationCheck':info(report),'checks':len(checks),'failures':0,'authoredCounts':index['authoredCounts'],'existingFilesChanged':len(planned),'newCanonicalFiles':5}))


if __name__=='__main__':
    main()
