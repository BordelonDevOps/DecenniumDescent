"""Integrate the exact jointly accepted 16-spell AC5 manuscript, preserving all sources."""
from copy import deepcopy
from datetime import datetime, timezone
import json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at

def read(p): return json.loads(p.read_bytes())

def main():
    candidate=A/'ac5-local-final-05-candidate'
    authority=A/'ac5-exact-acceptance-05/ACCEPTANCE.json'
    receipt=A/'AC5_EXACT_ACCEPTANCE_05_RECEIPT.json'; report=A/'AC5_EXACT_ACCEPTANCE_05_APPLICATION_CHECK.json'
    operations=A/'AC5_EXACT_ACCEPTANCE_05_OPERATIONS.json'; keep=A/'source-before-ac5-exact-acceptance-05'
    public=R/'data/public/spell_candidates/abjuration_conjuration_rank5_reviewed_05.json'
    cases_target=R/'data/playtest/spell_candidates/abjuration_conjuration_rank5_cases_05.json'
    player=R/'docs/spells/candidates/ABJURATION_CONJURATION_RANK5_REVIEWED_05.md'
    director=R/'docs/director-only/spells/ABJURATION_CONJURATION_RANK5_REVIEWED_05.md'
    statusfile=R/'docs/mechanics/ABJURATION_CONJURATION_RANK5_REVIEW_STATUS.json'
    assert not any(p.exists() for p in [receipt,report,operations,keep,public,cases_target,player,director,statusfile])
    checks=[]
    def ck(name,passed):
        checks.append({'name':name,'passed':bool(passed)})
        assert passed,name
    auth=read(authority); now=datetime.now(timezone.utc).isoformat()
    ck('Exact downloaded acceptance bytes',info(authority)['bytes']==5736 and info(authority)['sha256']=='2ff61a8cd7157201ab234e5d92185ebdad92ce43c965ab36e97e146a6661597d')
    archive=A/'DD_AC5_Exact_Acceptance_05.zip'
    ck('Exact downloaded archive',info(archive)['bytes']==3536 and info(archive)['sha256']=='605a2a872e462c44eb53b338ef07aeb938da6610f42e6e1b5fd55d4c7671018c')
    with zipfile.ZipFile(archive) as z:
        ck('Two safe unique acceptance members',len(z.namelist())==2 and set(z.namelist())=={'ACCEPTANCE.json','VERDICT.md'})
        ck('Acceptance matches archive',z.read('ACCEPTANCE.json')==authority.read_bytes())
        ck('Verdict matches archive',z.read('VERDICT.md')==(authority.parent/'VERDICT.md').read_bytes())
    ck('Affirmative bounded verdict',auth['verdict']=='ACCEPT_FOR_AUTHORED_CAMPAIGN_PLAYTEST_INTEGRATION' and auth['coherenceVerdict']['blockingAuthoredCoherenceFindingsRemaining']==0)
    reviewed=info(A/'DD_AC5_Local_Final_05.zip')
    ck('Exact accepted submission',all(reviewed[k]==auth['reviewedArchive'][k] for k in ['bytes','sha256']))
    expected={'REGISTER.json','SPELLS_MODEL.json','PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md','CASEBOOK.json','SOURCE_HASHES.json','VERDICT.md','EVIDENCE_MANIFEST.json'}
    ck('Exactly eight accepted payload bindings',len(auth['acceptedArtifactBindings'])==8 and {x['name'] for x in auth['acceptedArtifactBindings']}==expected)
    for b in auth['acceptedArtifactBindings']:
        ck('Exact accepted payload '+b['name'],all(info(candidate/b['name'])[k]==b[k] for k in ['bytes','sha256']))
    for b in read(candidate/'EVIDENCE_MANIFEST.json')['files']:
        ck('Candidate manifest independently agrees '+b['name'],all(info(candidate/b['name'])[k]==b[k] for k in ['bytes','sha256']))
    sources=read(candidate/'SOURCE_HASHES.json')['bindings']
    ck('92 reviewed source bindings',len(sources)==92 and auth['sourceVerification']['bindingCount']==92 and auth['sourceVerification']['allFrozenSourceBytesAndHashesVerified'] and not auth['sourceVerification']['failures'])
    for b in sources: ck('Reviewed source exact immediately before integration '+b['path'],info(G/b['path'])==b)
    ck('Prior independent full return verification passed',read(A/'AC5_REPAIR_RETURN_04_STRUCTURAL_CHECK.json')['failureCount']==0)
    local=read(A/'AC5_LOCAL_FINAL_05_CORRECTIONS.json')
    ck('Independent local corrections checks passed',local['checkCount']==617 and local['failureCount']==0)
    ck('All three local corrections agreed',[x['id'] for x in auth['local05Dispositions']]==['AC5-L05-01','AC5-L05-02','AC5-L05-03'] and all(x['verdict']=='AGREE' for x in auth['local05Dispositions']))
    model=read(candidate/'SPELLS_MODEL.json'); cb=read(candidate/'CASEBOOK.json'); ids=[s['id'] for s in model['spells']]
    ck('16 accepted spell identities',len(ids)==len(set(ids))==16 and ids==auth['moduleIdentity']['spellIds'])
    ck('17 original placements',sum(len(s['completeSourceAndAccess']['source']['original']['placements']) for s in model['spells'])==17==auth['moduleIdentity']['placementCount'])
    ck('61 exact unique accepted case IDs',len(cb['cases'])==len({c['id'] for c in cb['cases']})==61 and [c['id'] for c in cb['cases']]==auth['moduleIdentity']['caseIds'])
    original=read(A/'ac5-repair-04-input/ORIGINAL_REVIEW_INPUT.json')
    originals={s['spellId']:s for s in original['selectedRecords']}
    historical={c['id']:c['originalText'] for c in original['originalExamples']}
    ck('22 historical originals',len(historical)==22==auth['moduleIdentity']['historicalOriginalTextCount'])
    for c in cb['cases']:
        if c['id'] in historical: ck('Original case text preserved '+c['id'],c['historicalOriginalText']==historical[c['id']])
    catalog=R/'data/public/spell_playtests/catalog.json'; catalog_binding=info(catalog); catalog_data=read(catalog)
    byid={s['id']:s for s in catalog_data['spells']}
    for s in model['spells']:
        ident=s['id']; ck('Complete source/access current '+ident,s['completeSourceAndAccess']==byid[ident]==originals[ident]['completeCurrentSourceAndAccess'])
        ck('Original question preserved '+ident,s['historicalQuestion']==originals[ident]['historicalQuestionUnchanged'])
        for chapter in [candidate/'PLAYER_CHAPTER.md',candidate/'DIRECTOR_REVIEW.md']:
            ck('Full procedure in '+chapter.name+' '+ident,s['procedure'] in chapter.read_text(encoding='utf8'))
    ck('No runtime/human/balance claims',all(auth['testsClaimed'][k] is False for k in ['runtime','human','balance']))
    # Exact-byte copies, including historical candidate labels: adoption authority is the separate receipt/index.
    copies=[(public,candidate/'SPELLS_MODEL.json'),(cases_target,candidate/'CASEBOOK.json'),(player,candidate/'PLAYER_CHAPTER.md'),(director,candidate/'DIRECTOR_REVIEW.md')]
    public_binding=info(public,(candidate/'SPELLS_MODEL.json').read_bytes())
    aliases={'SPELLS_MODEL.json':public.relative_to(G).as_posix(),'REGISTER.json':(candidate/'REGISTER.json').relative_to(G).as_posix(),'CASEBOOK.json':cases_target.relative_to(G).as_posix()}
    rec={'reviewId':auth['id'],'recordedAtUtc':now,'status':'exact-authored-acceptance-applied','acceptanceAuthority':info(authority),'acceptanceArchive':info(archive),'reviewedArchive':reviewed,'actualGptReply':info(A/'AC5_EXACT_ACCEPTANCE_05_ACTUAL_NATIVE.json'),'actualBrowserReply':info(A/'AC5_EXACT_ACCEPTANCE_05_ACTUAL_BROWSER.txt'),'acceptedArtifactBindings':[info(candidate/b['name']) for b in auth['acceptedArtifactBindings']],'independentStructuralReview':info(A/'AC5_REPAIR_RETURN_04_STRUCTURAL_CHECK.json'),'independentLocalCorrectionReview':info(A/'AC5_LOCAL_FINAL_05_CORRECTIONS.json'),'acceptedSpellIds':ids,'sourceFiles':92,'placements':17,'authoredCases':61,'preservedHistoricalScenarioTexts':22,'canonicalCopies':[{'source':info(src),'destination':info(dst,src.read_bytes()),'byteIdentical':True} for dst,src in copies],'completeEnvelope':public_binding,'normalization':'None. Exact accepted model copied byte-for-byte; identity field is id. Acceptance status lives in this receipt, status file and authored index. Historical candidate labels remain historical.','caseSourceReferenceAliases':aliases,'authoredCountsBefore':{'reviewed':435,'pending':413},'authoredCountsAfter':{'reviewed':451,'pending':397},'historicalCandidateLabelsPreserved':True,'catalogSourceAndAccessUnchanged':True,'runtimeSelectionEnabled':False,'runtimeImplemented':False,'runtimeTestsExecuted':0,'humanBalanceApproved':False,'wholeGameFlowConfirmed':False,'sourceInformationDeleted':0,'pushed':False}
    receipt_raw=encoded(rec); receipt_binding=info(receipt,receipt_raw)
    indexp=R/'data/public/spell_playtests/authored_review_index.json'; before_index=indexp.read_bytes(); oldindex=json.loads(before_index); index=deepcopy(oldindex)
    ck('435/413 baseline',index['authoredCounts']=={'reviewed':435,'pending':413})
    ck('Current catalog binding',index['sourceCatalogSha256']==catalog_binding['sha256'])
    for n,ident in enumerate(ids):
        e=next(e for e in index['entries'] if e['id']==ident); ck('Pending before integration '+ident,e['authoredStatus']=='pending-authored-procedure')
        e['sourceCatalogWholeCardPointer']=e['wholeCardPointer']
        e.update(authoredStatus='reviewed-authored-operational-playtest',procedureFile='../spell_candidates/abjuration_conjuration_rank5_reviewed_05.json',procedurePointer=f'/spells/{n}',wholeCardPointer=f'/spells/{n}',wholeCardIdField='id',procedureTextPointer=f'/spells/{n}/procedure',sharedRulesPointer='/sharedRules',manuscript='../../../docs/spells/candidates/ABJURATION_CONJURATION_RANK5_REVIEWED_05.md',reviewId=auth['id'],runtimeSelectionEnabled=False,completeEnvelopeBinding=public_binding,authoredAcceptanceReceipt=receipt_binding,historicalCandidateLabelsPreserved=True,caseSourceReferenceAliases=aliases)
        ck('Discovery whole-card and procedure resolve '+ident,at(model,e['wholeCardPointer'])['id']==ident and at(model,e['procedureTextPointer'])==model['spells'][n]['procedure'])
    index['authoredCounts']={'reviewed':451,'pending':397}
    ck('159 prior complete standalone procedures',index['representationCounts']['completeReviewedStandaloneProcedures']==159)
    index['representationCounts']['completeReviewedStandaloneProcedures']=175
    index.setdefault('additionalStandaloneEnvelopes',[]).append({'file':'../spell_candidates/abjuration_conjuration_rank5_reviewed_05.json','binding':public_binding,'reviewId':auth['id'],'acceptedIds':ids,'authority':info(authority),'receipt':receipt_binding})
    for old,new in zip(oldindex['entries'],index['entries']):
        if old['id'] not in ids: ck('Unrelated authored record unchanged '+old['id'],old==new)
    ck('All 848 identities/order preserved',[e['id'] for e in oldindex['entries']]==[e['id'] for e in index['entries']] and len(index['entries'])==848)
    ck('451 reviewed memberships',sum(e['authoredStatus']=='reviewed-authored-operational-playtest' for e in index['entries'])==451)
    ck('396 pending-procedure plus one preserved receipt-only membership',sum(e['authoredStatus']=='pending-authored-procedure' for e in index['entries'])==396 and sum(e['authoredStatus']=='receipt-only-post-push-cosmology' for e in index['entries'])==1)
    guide=R/'docs/mechanics/SPELL_INTEGRATION_RULES.md'; before_guide=guide.read_bytes(); newline='\r\n' if b'\r\n' in before_guide else '\n'
    addition=newline.join(['','','## Rank-five Abjuration and Conjuration — reviewed provisional interfaces','','The [complete sixteen-spell manuscript](../spells/candidates/ABJURATION_CONJURATION_RANK5_REVIEWED_05.md), [exact structured model](../../data/public/spell_candidates/abjuration_conjuration_rank5_reviewed_05.json), and [exact GPT acceptance and application receipt](../../../../docs/audit/2026-10-08/full-game/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json) govern these sixteen ordinary spells for authored campaign-playtest integration. The accepted model and both chapters are exact-byte copies; earlier candidate labels and rejected examples remain preserved historical evidence. Use the receipt and authored index for their current approval status. The source catalog and all class/access placements remain unchanged.','','The cohort supplies Antimagic Field (Lesser), Banish Elemental, Greater Dispel, Spell Resistance, Wall of Force, Resonance Barrier, Planar Protection, Reputation Shield, Summon Greater Fire Pet, Massive Elemental Blast, Living Magma, Elemental Banishment, Planar Binding, Resonance Nexus, Faction Champion and Alignment Portal. Planar Binding retains both printed placements. AC5-ANTIMAGIC-IO-04, AC5-WALL-PANELS-04 and AC5-PORTAL-GEOMETRY-04 supersede their corresponding 03 rules as explicitly recorded in the accepted model. The local05 geometry fixes and additive portal movement rule are jointly accepted.','','All 61 authored cases, 22 original example texts and 92 frozen sources remain available. The companion HP-healing and antimagic rules apply only to their named AC5 summons; the Banishment extension applies only to the two stated AC5 exiles. Alignment Portal is a planar physical gateway classified as nonteleportation; formation and actual transit are separate tests. No rule here silently settles an unrelated pending spell, creature origin or named cosmology.','','This is authored playtest integration. It does not enable runtime selection or certify human playtesting, numerical balance, cosmology canon, whole-game flow or publication readiness.','']).encode('utf8')
    planned=[(indexp,before_index,encoded(index),'Sixteen reviewed memberships and exact complete-model discovery'),(guide,before_guide,before_guide+addition,'Append scoped accepted interfaces; retain all earlier text')]
    preserved=[]
    for p,before,after,scope in planned:
        ck('Mutation target unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==before)
        q=keep/p.relative_to(G);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(before)
        ck('Prior bytes preserved '+p.relative_to(G).as_posix(),q.read_bytes()==before)
        preserved.append({'before':{**info(p,before),'preservedCopy':q.relative_to(G).as_posix()},'after':info(p,after),'scope':scope})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded([p['before'] for p in preserved]))
    for dst,src in copies:
        dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(src.read_bytes());ck('Exact canonical copy '+dst.relative_to(G).as_posix(),dst.read_bytes()==src.read_bytes())
    receipt.write_bytes(receipt_raw)
    for p,before,after,_ in planned:
        assert p.read_bytes()==before;p.write_bytes(after);ck('Exact planned mutation '+p.relative_to(G).as_posix(),p.read_bytes()==after)
    ck('Original catalog wholly unchanged',info(catalog)==catalog_binding)
    for b in sources:
        p=G/b['path']
        if p not in [indexp,guide]:ck('Unmodified reviewed source after application '+b['path'],info(p)==b)
        else:ck('Changed reviewed source preserved exactly '+b['path'],all(info(keep/p.relative_to(G))[k]==b[k] for k in ['bytes','sha256']))
    statusfile.write_bytes(encoded({'reviewId':auth['id'],'status':'REVIEWED authored operational-playtest manuscript; runtime and human balance pending','receipt':info(receipt),'completeExactModel':info(public),'playerChapter':info(player),'directorChapter':info(director),'authoredCases':info(cases_target),'caseSourceReferenceAliases':aliases,'acceptedSpellIds':ids,'caseCount':61,'sourceInformationDeleted':0,'runtimeSelectionEnabled':False}))
    operations.write_bytes(encoded({'recordedAtUtc':now,'authority':info(authority),'receipt':info(receipt),'changes':preserved,'canonicalCopies':[info(p) for p,_ in copies],'sourceInformationDeleted':0,'originalCatalogUnchanged':True}))
    report.write_bytes(encoded({'recordedAtUtc':now,'scope':'Exact acceptance, independent source preservation and authored application checks; no runtime or human tests','authority':info(authority),'receipt':info(receipt),'operations':info(operations),'checks':checks,'checkCount':len(checks),'failureCount':0,'authoredCounts':index['authoredCounts'],'runtimeTestsExecuted':0,'humanPlaytested':False,'sourceInformationDeleted':0}))
    print(json.dumps({'receipt':info(receipt),'applicationCheck':info(report),'checks':len(checks),'failures':0,'authoredCounts':index['authoredCounts'],'existingFilesChanged':len(planned),'newCanonicalFiles':len(copies)+1}))

if __name__=='__main__': main()
