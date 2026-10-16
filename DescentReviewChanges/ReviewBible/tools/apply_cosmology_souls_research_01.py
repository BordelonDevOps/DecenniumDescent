"""Apply the source-verified integrated conference and its explicit GPT patch."""
from datetime import datetime, timezone
from copy import deepcopy
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p): return json.loads(p.read_bytes())

def main():
    root=A/'cosmology-souls-research-01-return-integrated'
    check=A/'COSMOLOGY_SOULS_RESEARCH_01_RETURN_SOURCE_CHECK_integrated-v2.json'
    confirmed=A/'COSMOLOGY_SOULS_RESEARCH_01_PATCH_CONFIRMATION_DOM.txt'
    target=R/'data/director/cosmology/souls_research_reviewed_01.json'
    chapter=R/'docs/director-only/cosmology/SOULS_RESEARCH_REVIEWED_01.md'
    receipt=A/'COSMOLOGY_SOULS_RESEARCH_01_APPLICATION_CHECK.json'
    patch=A/'COSMOLOGY_SOULS_RESEARCH_01_CONFIRMED_PATCH.json'
    assert all(not p.exists() for p in [target,chapter,receipt,patch])
    validation=read(check);assert validation['checkCount']==392 and validation['failureCount']==0
    proof=confirmed.read_text(encoding='utf-8')
    assert 'Confirmed. I see' in proof and 'no conflict' in proof and 'Response complete' in proof
    now=datetime.now(timezone.utc).isoformat()
    original=read(root/'RESEARCH_ROUTE_AND_STATE_MODEL.json');model=deepcopy(original)
    cases=read(root/'CASEBOOK.json');before_cases=deepcopy(cases);register=read(root/'REGISTER.json')
    assert len(register['issues'])==21 and len(cases['suppliedCases'])==34
    assert len(cases['additionalProposedEdgeCases'])==8 and len(cases['targetedRevisionExamples'])==14 and len(cases['integrationTargetedExamples'])==8
    first=read(A/'cosmology-souls-research-01-return/CASEBOOK.json')
    for key in ['suppliedCases','additionalProposedEdgeCases']:
        assert [v['id'] for v in cases[key]]==[v['id'] for v in first[key]]
    duration='Until the end of the creature’s next regular turn in initiative, or 1 minute outside initiative.'
    model['taint']['knowledgeSymptoms']['KT3 Compromised']['duration']=duration
    scene=model['taint']['completeDefaultVoiceProximityEncounter']['scene'];assert 'PT1 Pressed' in scene
    model['taint']['completeDefaultVoiceProximityEncounter']['scene']=scene.replace('PT1 Pressed','PT1 Whispered')
    changes=[{'pointer':'/taint/knowledgeSymptoms/KT3 Compromised/duration','before':None,'after':duration},
             {'pointer':'/taint/completeDefaultVoiceProximityEncounter/scene','before':scene,'after':model['taint']['completeDefaultVoiceProximityEncounter']['scene']}]
    for row in cases['suppliedCases']:
        if row['id']=='SH-T17':
            old=row['reviewDisposition'];row['reviewDisposition']=old.replace('the seven-field protocol','the complete current exceptional-intervention record')
            assert row['reviewDisposition']!=old
            changes.append({'caseId':row['id'],'before':old,'after':row['reviewDisposition']})
        if row['id']=='SH-T20':
            old=row['reviewDisposition'];row['reviewDisposition']='Reject the six-tick canonical claim. The owner did not select that model. This jointly reviewed, explicitly NEW provisional operating candidate is now adopted locally within its bounded Director/playtest scope; runtime, human balance, whole-game and original-canon approval remain open.'
            changes.append({'caseId':row['id'],'before':old,'after':row['reviewDisposition']})
    guard=R/'data/public/spell_playtests/authored_review_index.json';guard_before=info(guard)
    archives=[info(A/n) for n in ['COSMOLOGY_SOULS_RESEARCH_01_Addendum_and_Evidence.zip','COSMOLOGY_SOULS_RESEARCH_01_Revised_Addendum_and_Evidence.zip','COSMOLOGY_SOULS_RESEARCH_01_Integrated_Addendum_and_Evidence.zip']]
    patch.write_bytes(encoded({'recordedAtUtc':now,'status':'explicitly confirmed by actual GPT in Part3','confirmation':info(confirmed),'visibleProof':info(A/'COSMOLOGY_SOULS_RESEARCH_01_PATCH_CONFIRMATION.png'),'changes':changes,'chapterCarryForward':'Faithful current-model details restored to the readable chapter; no new rule choices.','priorArchives':archives,'sourceInformationDeleted':0}))
    data={'reviewId':'COSMOLOGY-SOULS-RESEARCH-01','recordedAtUtc':now,'status':'jointly-reviewed NEW provisional Director/playtest operating candidate; locally adopted',
          'authority':'Original sources and explicit owner directions remain distinct from the new qualification, research, taint, Hunt and intervention defaults. Unknown identities, epoch and universal soul jurisdiction remain open.',
          'reviewArchive':archives[-1],'priorArchives':archives[:-1],'localSourceVerification':info(check),'confirmedApplicationPatch':info(patch),
          'sourceBindings':read(A/'cosmology-souls-research-01/SOURCE_BINDINGS.json'),'sourceBindingScope':'frozen 79-source conference packet; not an assertion that all mutable live navigation files are unchanged',
          'currentStateModel':model,'currentCasebook':cases,'reviewRegister':register,'semanticCoverage':read(root/'SEMANTIC_COVERAGE.json'),
          'scopeCounts':{'issues':21,'originalSituations':34,'firstAdditionalCases':8,'revisionExamples':14,'integrationExamples':8},
          'newProvisionalOperatingRulesAdopted':True,'recoveredCanonAdded':False,'ordinarySpellApprovals':0,'campaignEpochChosen':False,'epilogueRulesAdopted':False,
          'runtimeImplemented':False,'humanPlaytested':False,'balanceApproved':False,'wholeGameFlowConfirmed':False,'fullCosmologyApproved':False,'publicExportEnabled':False,'sourceInformationDeleted':0}
    target.write_bytes(encoded(data))
    prose=(root/'DIRECTOR_COMPANION.md').read_text(encoding='utf-8')
    old_status=next(s for s in prose.splitlines() if s.startswith('**Status:**'))
    current_status='**Status:** Locally adopted **NEW PROVISIONAL DESIGN** Director/playtest reference after source verification and explicit GPT confirmation of the small application patch. It is not recovered canon. Runtime implementation, human playtest, balance, whole-game flow, campaign epoch, chronology/epilogue adoption, unresolved identities and pending spells remain open.'
    prose=prose.replace(old_status,current_status,1)
    prose=prose.replace('## 1. Current-rule and history boundary','Read with [the owner corrections](HEARTCELL_OWNER_UPDATE_02.md), [Q6](Q6_LATER_LOCK_REVIEWED_01.md) and [the planes reference](PLANES_REVIEWED_01.md). The [structured current record](../../../data/director/cosmology/souls_research_reviewed_01.json) preserves all 21 issue dispositions and 64 authored situations/examples. These examples are not runtime or human tests.\n\n## 1. Current-rule and history boundary',1)
    def before(heading,addition):
        nonlocal prose
        assert prose.count(heading)==1
        prose=prose.replace(heading,addition+'\n\n'+heading,1)
    before('## 4. Four-hour synthesis and fixed-DC resolution',
        '### Functional Model evidence gate\n\nRequire authenticated evidence from **two distinct Descent libraries**, **one mechanism observation**, **one seasonal/change observation**, and **one rare drop or physical clue**. These are categories, not five recovered Equation fragments. '+model['functionalModelGate']['antiInflation'])
    before('### Complete fictional worked case',
        '### Assistance and difficulty\n\n'+model['researchBlock']['assistance']+'. Assistants never supply a missing personal qualification; apply the actual PB/Expertise rules once.\n\n'+model['researchBlock']['difficultySelection']['recommendedBands'])
    before('## 6. Knowledge Taint (KT)',model['predictionTests']['procedure'])
    needle='On failure, apply **actual Dazed only**:';assert prose.count(needle)==1
    prose=prose.replace(needle,'On failure, apply Dazed **until the end of the creature’s next regular turn in initiative, or for 1 minute outside initiative**. Apply **actual Dazed only**:',1)
    before('## 10. Whole-event death resolution under Hunt',
        '### Hunt triggers\n\n'+ '\n'.join('- '+v for v in model['hunt']['candidateTriggers'])+'\n\nThe separate attention states are None, Observed and Pursued. They do not themselves impose Hunt. Possession, copying, literal translation, a taint stage or mere level-5+ proximity is insufficient. Blind/accidental action without supported operational understanding is not this voluntary trigger, unless an exact authored event independently imposes Hunt.')
    before('## 12. Stable boundaries',
        '### Complete exceptional-intervention record\n\n'+'\n'.join('- '+v for v in model['exceptionalIntervention']['requiredFields'])+'\n\n'+model['exceptionalIntervention']['minimumCostRule']+' No gold/RP-only routine service or class name creates an exception.\n\n### Research route slots\n\n'+'\n'.join('- **'+s['slot']+' — '+s['site']+'**: '+s['placement']+'. '+s['equationHolding']+'.' for s in model['researchRoute']['slots'])+'\n\n'+model['researchRoute']['chronology']+' Existing cosmic institutions are not silently relocated into the Descent. Actual holdings, clue scenes and L2 placement are the next authorship work.')
    chapter.write_text(prose,encoding='utf-8',newline='\n')
    assert info(guard)==guard_before
    # Exact bounded diffs ensure this application does not silently revise the accepted model.
    restored=deepcopy(model);del restored['taint']['knowledgeSymptoms']['KT3 Compromised']['duration'];restored['taint']['completeDefaultVoiceProximityEncounter']['scene']=scene
    assert restored==original
    for key in ['additionalProposedEdgeCases','targetedRevisionExamples','integrationTargetedExamples']:assert cases[key]==before_cases[key]
    assert not cases['executedAsSoftwareTests'] and not cases['humanPlaytested']
    assert 'end of the creature’s next regular turn' in prose and 'two distinct Descent libraries' in prose
    receipt.write_bytes(encoded({'recordedAtUtc':now,'status':'verified integrated candidate and confirmed patch applied','data':info(target),'chapter':info(chapter),'patch':info(patch),
       'localSourceVerification':info(check),'sourceChecks':392,'sourceCheckFailures':0,'frozenSources':79,'issues':21,'authoredSituationsAndExamples':64,
       'applicationAssertions':'All original IDs retained; exactly two confirmed model changes and two confirmed case-wording changes; other case cohorts unchanged; spell index unchanged.',
       'manifestSchemaNote':'Initial integrated check did not recognize entries and recorded a manifest-count failure. The preserved successor recognizes files/outputs/entries; all seven actual output hashes and392totalchecks passed.',
       'ordinarySpellIndexUnchanged':guard_before,'priorArchivesPreserved':archives,'newProvisionalOperatingRulesAdopted':True,'runtimeImplemented':False,'humanPlaytested':False,'wholeGameFlowConfirmed':False,'sourceInformationDeleted':0}))
    print(json.dumps({'data':info(target),'chapter':info(chapter),'receipt':info(receipt),'patch':info(patch)}))

if __name__=='__main__':main()
