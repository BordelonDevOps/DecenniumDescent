"""Integrate the exact accepted AC4 manuscript and scoped alignment interface reversibly."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
from zipfile import ZipFile
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded,digest,node

def read(p):return json.loads(p.read_bytes())

def main():
    candidate=A/'ac4-exact-case-patch-03/candidate'
    receipt=A/'AC4_EXACT_ACCEPTANCE_03_RECEIPT.json';report=A/'AC4_EXACT_ACCEPTANCE_03_APPLICATION_CHECK.json'
    operations=A/'AC4_EXACT_ACCEPTANCE_03_OPERATIONS.json';keep=A/'source-before-ac4-exact-acceptance-03'
    authority=A/'AC4_EXACT_ACCEPTANCE_03.json';archive=A/'DD_AC4_Exact_Acceptance_03.zip'
    public=R/'data/public/spell_candidates/abjuration_conjuration_rank4_reviewed_03.json'
    case_target=R/'data/playtest/spell_candidates/abjuration_conjuration_rank4_cases_03.json'
    player=R/'docs/spells/candidates/ABJURATION_CONJURATION_RANK4_REVIEWED_03.md'
    director=R/'docs/director-only/spells/ABJURATION_CONJURATION_RANK4_REVIEWED_03.md'
    statusfile=R/'docs/mechanics/ABJURATION_CONJURATION_RANK4_REVIEW_STATUS.json'
    assert not any(p.exists() for p in [receipt,report,operations,keep,authority,archive,public,case_target,player,director,statusfile])
    incoming=Path(r'C:\Users\cbord\Downloads\DD_AC4_Exact_Acceptance_03.zip');raw=incoming.read_bytes()
    assert len(raw)==2432 and digest(raw)=='91e2fdee129a229045f8ae84544f09365c72b19d6811a6383ebf507aa3af96e0'
    with ZipFile(incoming) as z:
        assert z.namelist()==['AC4_EXACT_ACCEPTANCE_03.json'];authraw=z.read('AC4_EXACT_ACCEPTANCE_03.json')
    assert len(authraw)==4824 and digest(authraw)=='c1c266c3f9d894acb3f682b77652c094b870adb0c51fa4e681e5134f75f51572'
    auth=json.loads(authraw);assert auth['finalModuleVerdict']['verdict']=='ACCEPT'
    checks=[]
    def ck(name,ok):
        checks.append({'name':name,'passed':bool(ok)})
        assert ok,name
    submitted=info(A/'DD_AC4_Exact_Case_Patch_03.zip')
    ck('Exact accepted submission archive',all(auth['reviewedPatchArchive'][k]==submitted[k] for k in ['bytes','sha256']))
    for b in auth['acceptedArtifactBindings']:
        ck('Exact accepted payload '+b['name'],all(info(candidate/b['name'])[k]==b[k] for k in ['bytes','sha256']))
    supplied=read(A/'ac4-current-review-01-input/CURRENT_REVIEW_INPUT.json')
    for b in supplied['sourceBindings']:ck('Current reviewed source before integration '+b['path'],info(G/b['path'])==b)
    model=read(candidate/'SPELLS_MODEL.json');cases=read(candidate/'CASEBOOK.json');ids=auth['acceptedSpellIds']
    ck('15 exact spell identities',len(ids)==15 and ids==[c['spellId'] for c in model['spells']])
    ck('48 unique authored examples',len(cases['cases'])==len({c['id'] for c in cases['cases']})==48)
    for a,b in zip(cases['cases'][:30],supplied['originalExamples']):ck(a['id']+' original example identity/text',a['id']==b['id'] and a['originalText']==b['originalText'])
    for a,b in zip(model['spells'],supplied['records']):ck(a['spellId']+' full source/access preserved',a['sourceAndAccess']==b['fullSourceAndCurrentAccessRecord'])
    ck('Banishment excluded and receipt retained','banishment' not in ids and model['banishmentSourceOnlyReceipt']==supplied['banishmentSourceOnlyReceipt'])
    ck('Prior independent corrected-return checks passed',read(A/'AC4_CORRECTIONS_02_RETURN_SOURCE_CHECK.json')['failureCount']==0)
    # Acceptance itself is preserved before recording any derived rule changes.
    archive.write_bytes(raw);authority.write_bytes(authraw)
    planned=[]
    def json_change(p,edits):
        before=p.read_bytes();old=json.loads(before);crlf=before==encoded(old,True);assert before==encoded(old,crlf)
        new=deepcopy(old)
        for pointer,expected,replacement in edits:
            parent,key=node(new,pointer);assert parent[key]==expected,(str(p),pointer);parent[key]=deepcopy(replacement)
        reverse=deepcopy(new)
        for pointer,expected,replacement in reversed(edits):parent,key=node(reverse,pointer);assert parent[key]==replacement;parent[key]=deepcopy(expected)
        ck('Exact reversible JSON '+p.relative_to(G).as_posix(),encoded(reverse,crlf)==before)
        after=encoded(new,crlf);planned.append((p,before,after,[{'pointer':q,'old':o,'replacement':n} for q,o,n in edits]));return new,after
    def text_change(p,edits):
        before=p.read_bytes();after=before
        for old,new in edits:
            ob,nb=old.encode(),new.encode();assert after.count(ob)==1,(str(p),old[:60]);after=after.replace(ob,nb,1)
        reverse=after
        for old,new in reversed(edits):assert reverse.count(new.encode())==1;reverse=reverse.replace(new.encode(),old.encode(),1)
        ck('Exact reversible prose '+p.relative_to(G).as_posix(),reverse==before)
        planned.append((p,before,after,[{'old':o,'replacement':n} for o,n in edits]));return after
    catalog=R/'data/public/spell_playtests/catalog.json';oldcat=read(catalog)
    assert oldcat['spells'][329]['id']=='alignment-suggestion'
    oldres=oldcat['spells'][329]['operational']['resolution']
    newres=oldres.replace('Retain all other independent actual alignment effects/records.','Under the NEW scoped AC4-ALIGN-01 exception, also exclude all Alignment Lock/Alignment Anchor overlays on this target when computing this baseline. Retain all other independent actual alignment effects/records.',1)
    newres=newres.replace('an actual Purge on the caster still makes its effective orientation Neutral/Neutral.','an actual Purge on the caster still supplies Neutral/Neutral, subject to that caster\'s own active AC4 Lock/Anchor snapshot for the final effective read.',1)
    newres=newres.replace('An unsuppressed Purge on the target covers the resulting live Suggestion values until Purge ends or is suppressed.','An unsuppressed Purge on the target covers the resulting live Suggestion values until Purge ends or is suppressed; an eligible active Alignment Lock/Alignment Anchor snapshot applies last under AC4-ALIGN-01, without deleting, pausing or refreshing these lower records.',1)
    assert newres!=oldres and newres.count('AC4-ALIGN-01')==2
    oldeffect=oldcat['spells'][329]['operational']['effect']
    effectnote=' NEW scoped AC4-ALIGN-01: effective-alignment reads evaluate this live Suggestion overlay and the reviewed AP-AS-01 Purge interaction first, then apply the eligible active Alignment Lock/Alignment Anchor snapshot last. Lock/Anchor ending or inactivity exposes the then-live lower result with its original history/deadline; no ended overlay is restored. This adds no general alignment priority system.'
    neweffect=oldeffect+effectnote
    newcat,catbytes=json_change(catalog,[('/spells/329/operational/resolution',oldres,newres),('/spells/329/operational/effect',oldeffect,neweffect)])
    catbinding=info(catalog,catbytes)
    for rel in ['data/playtest/spell_drafts/candidate_enchantment_rank1.json','data/playtest/spell_drafts/batch_enchantment_rank1.json']:
        p=R/rel;assert read(p)['spells'][9]['id']=='alignment-suggestion';json_change(p,[('/spells/9/resolution',oldres,newres),('/spells/9/effect',oldeffect,neweffect)])
    dep=R/'data/public/feat_candidates/exact_01/spell_dependencies.json';olddep=read(dep)
    edits=[('/spells/alignment-suggestion/completeCurrentProcedureCard/operational/resolution',oldres,newres),('/spells/alignment-suggestion/completeCurrentProcedureCard/operational/effect',oldeffect,neweffect)];bound=0
    for ident,row in olddep['spells'].items():
        b=row['binding']
        if b['file']!=catalog.relative_to(G).as_posix():continue
        index=int(b['pointer'].split('/')[-1]);assert row['completeCurrentProcedureCard']==oldcat['spells'][index] and oldcat['spells'][index]['id']==ident
        assert all(b[k]==info(catalog)[k] for k in ['bytes','sha256']);bound+=1
        for k in ['bytes','sha256']:edits.append((f'/spells/{ident}/binding/{k}',b[k],catbinding[k]))
    ck('202 active catalog dependency bindings',bound==202);newdep,_=json_change(dep,edits)
    for ident,row in newdep['spells'].items():
        ck('Feat original source unchanged '+ident,row['originalCatalogRecord']==olddep['spells'][ident]['originalCatalogRecord'])
        if row['binding']['file']==catalog.relative_to(G).as_posix():ck('Current feat dependency '+ident,row['completeCurrentProcedureCard']==newcat['spells'][int(row['binding']['pointer'].split('/')[-1])])
    cohort=R/'data/director/feat_candidates/exact_01/cohorts/general_combat.json';beforecohort=read(cohort)
    newcohort,_=json_change(cohort,[('/completeCurrentSpellDependencies/alignment-suggestion/completeCurrentProcedureCard/operational/resolution',oldres,newres),('/completeCurrentSpellDependencies/alignment-suggestion/completeCurrentProcedureCard/operational/effect',oldeffect,neweffect)])
    ck('Feat cohort records and original source preserved',newcohort['records']==beforecohort['records'] and newcohort['completeCurrentSpellDependencies']['alignment-suggestion']['completeOriginalCatalogObject']==beforecohort['completeCurrentSpellDependencies']['alignment-suggestion']['completeOriginalCatalogObject'])
    text_change(R/'docs/mechanics/SPELL_PLAYTEST_STARTER.md',[(oldres,newres),(oldeffect,neweffect)])
    text_change(R/'docs/feats/exact-candidate-01/SPELL_PAYLOADS.md',[(json.dumps(oldres,ensure_ascii=False),json.dumps(newres,ensure_ascii=False)),(json.dumps(oldeffect,ensure_ascii=False),json.dumps(neweffect,ensure_ascii=False))])
    guide=R/'docs/mechanics/SPELL_INTEGRATION_RULES.md';guidetext=guide.read_text(encoding='utf8');paragraph=next(x for x in guidetext.splitlines() if x.startswith('**Alignment Suggestion:**'))
    lock=next(x for x in model['spells'] if x['spellId']=='alignment-lock')['procedure'].split('CURRENT INTERFACE — ',1)[1]
    text_change(guide,[(paragraph,paragraph+'\n\n**AC4-ALIGN-01 — reviewed Lock/Anchor integration.** '+lock+'\n\nThe [complete fifteen-spell AC4 chapter](../spells/candidates/ABJURATION_CONJURATION_RANK4_REVIEWED_03.md) and [review receipt](../../../../docs/audit/2026-10-08/full-game/AC4_EXACT_ACCEPTANCE_03_RECEIPT.json) govern the exact accepted authored procedures, including separate Alignment Anchor placements, finite summon profiles and all scoped interfaces. These manuscript acceptances do not enable runtime selection or certify human balance.')])
    indexp=R/'data/public/spell_playtests/authored_review_index.json';oldindex=read(indexp);index=deepcopy(oldindex)
    ck('Pre-integration419/429',index['authoredCounts']=={'reviewed':419,'pending':429})
    ck('Pre-integration catalog binding',index['sourceCatalogSha256']==info(catalog)['sha256'])
    now=datetime.now(timezone.utc).isoformat()
    copies=[(public,candidate/'SPELLS_MODEL.json'),(case_target,candidate/'CASEBOOK.json'),(player,candidate/'PLAYER_CHAPTER.md'),(director,candidate/'DIRECTOR_REVIEW.md')]
    accepted_bindings=[info(candidate/b['name']) for b in auth['acceptedArtifactBindings']]
    receipt_data={'reviewId':auth['id'],'recordedAtUtc':now,'status':'exact-authored-acceptance-recorded','acceptanceAuthority':info(authority),'acceptanceArchive':info(archive),'submittedArchive':submitted,'observedTerminalReply':info(A/'AC4_EXACT_ACCEPTANCE_03_ACTUAL_DOM.txt'),
      'acceptedArtifactBindings':accepted_bindings,'acceptedSpellIds':ids,'authoredCases':48,'sourceFiles':70,'operativeCorrectionsRemaining':0,'sourceIntegrityCheck':info(A/'AC4_CORRECTIONS_02_RETURN_SOURCE_CHECK.json'),
      'canonicalCopies':[{'source':info(src),'destination':info(dst,src.read_bytes()),'byteIdentical':True} for dst,src in copies],
      'activeInterfaceIntegration':'AC4-ALIGN-01 adds target-side Lock/Anchor baseline exclusion and final snapshot precedence to current Suggestion readers; old sources preserved in reversible operations.',
      'authoredCountsBefore':{'reviewed':419,'pending':429},'authoredCountsAfter':{'reviewed':434,'pending':414},'historicalCandidateLabelsPreserved':True,
      'runtimeSelectionEnabled':False,'runtimeImplemented':False,'runtimeTestsExecuted':0,'humanBalanceApproved':False,'wholeGameFlowConfirmed':False,'pushed':False,'sourceInformationDeleted':0}
    receiptbytes=encoded(receipt_data);receiptbinding=info(receipt,receiptbytes);publicbinding=info(public,(candidate/'SPELLS_MODEL.json').read_bytes())
    for i,ident in enumerate(ids):
        e=next(x for x in index['entries'] if x['id']==ident);assert e['authoredStatus']=='pending-authored-procedure'
        e['sourceCatalogWholeCardPointer']=e['wholeCardPointer']
        e.update(authoredStatus='reviewed-authored-operational-playtest',procedureFile='../spell_candidates/abjuration_conjuration_rank4_reviewed_03.json',procedurePointer=f'/spells/{i}',procedureTextPointer=f'/spells/{i}/procedure',wholeCardPointer=f'/spells/{i}',wholeCardIdField='spellId',sharedRulesPointer='/sharedRules',manuscript='../../../docs/spells/candidates/ABJURATION_CONJURATION_RANK4_REVIEWED_03.md',reviewId=auth['id'],runtimeSelectionEnabled=False,completeEnvelopeBinding=publicbinding,authoredAcceptanceReceipt=receiptbinding,historicalCandidateLabelsPreserved=True)
        if ident=='faction-ally':e['supportingProfilePointers']=['/factionAllyProfile']
    index['authoredCounts']={'reviewed':434,'pending':414};index['representationCounts']['completeReviewedStandaloneProcedures']=158;index['sourceCatalogSha256']=catbinding['sha256']
    index.setdefault('additionalStandaloneEnvelopes',[]).append({'file':'../spell_candidates/abjuration_conjuration_rank4_reviewed_03.json','binding':publicbinding,'reviewId':auth['id'],'acceptedIds':ids,'authority':info(authority),'receipt':receiptbinding})
    for b,a in zip(oldindex['entries'],index['entries']):
        if b['id'] not in ids:ck('Unrelated authored entry unchanged '+b['id'],b==a)
    ck('434 actual reviewed memberships',sum(x['authoredStatus']=='reviewed-authored-operational-playtest' for x in index['entries'])==434)
    ck('All848 original IDs/order preserved',[e['id'] for e in oldindex['entries']]==[e['id'] for e in index['entries']])
    indexbefore=indexp.read_bytes();planned.append((indexp,indexbefore,encoded(index),[{'scope':'15 exact authored memberships, current catalog binding, additional accepted envelope and aggregate counts','oldCounts':oldindex['authoredCounts'],'newCounts':index['authoredCounts']}]))
    # Preserve every existing edited file before any mutation.
    changes=[]
    for p,b,a,edits in planned:
        assert p.read_bytes()==b;q=keep/p.relative_to(G);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
        ck('Preserved before mutation '+p.relative_to(G).as_posix(),q.read_bytes()==b)
        changes.append({'before':{**info(p,b),'preservedCopy':q.relative_to(G).as_posix()},'after':info(p,a),'operations':edits})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded([c['before'] for c in changes]))
    for dst,src in copies:dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(src.read_bytes());ck('Exact canonical copy '+dst.relative_to(G).as_posix(),dst.read_bytes()==src.read_bytes())
    receipt.write_bytes(receiptbytes)
    for p,b,a,_ in planned:assert p.read_bytes()==b;p.write_bytes(a);ck('Applied bytes '+p.relative_to(G).as_posix(),p.read_bytes()==a)
    for b in accepted_bindings:ck('Accepted candidate unchanged after integration '+b['path'],info(G/b['path'])==b)
    for old,new in zip(oldcat['spells'],read(catalog)['spells']):
        ck('Original catalog source/access preserved '+old['id'],old['source']==new['source'] and old['classAccess']==new['classAccess'])
        if old['id']!='alignment-suggestion':ck('Unrelated catalog card unchanged '+old['id'],old==new)
    statusfile.write_bytes(encoded({'reviewId':auth['id'],'status':'REVIEWED authored operational-playtest manuscript; runtime and human balance pending','receipt':info(receipt),'completeModel':info(public),'playerChapter':info(player),'directorChapter':info(director),'authoredCases':info(case_target),'acceptedSpellIds':ids,'caseCount':48,'sourceInformationDeleted':0,'runtimeSelectionEnabled':False}))
    operations.write_bytes(encoded({'recordedAtUtc':now,'authority':info(authority),'receipt':info(receipt),'changes':changes,'newExactCanonicalCopies':[info(p) for p,_ in copies],'sourceInformationDeleted':0,'activeCatalogDependencyBindingsRefreshed':bound,'historicalSourceRecordsUnchanged':True}))
    report.write_bytes(encoded({'recordedAtUtc':now,'scope':'Exact acceptance/source/preservation/application checks; no spell runtime or human tests','authority':info(authority),'receipt':info(receipt),'operations':info(operations),'checkCount':len(checks),'failureCount':0,'checks':checks,'authoredCounts':index['authoredCounts'],'runtimeTestsExecuted':0,'humanPlaytested':False,'sourceInformationDeleted':0}))
    print(json.dumps({'receipt':info(receipt),'report':info(report),'authoredCounts':index['authoredCounts'],'checks':len(checks),'failures':0,'changedExistingFiles':len(planned),'exactCanonicalCopies':len(copies)}))

if __name__=='__main__':main()
