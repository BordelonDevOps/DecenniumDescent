"""Save the verified source comparison without adopting the unfinished route or era."""
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    root=A/'cosmology-chronology-research-route-01-return'
    check=A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_RETURN_SOURCE_CHECK_01.json';verified=read(check)
    assert verified['checkCount']==250 and verified['failureCount']==0
    model=read(root/'TIMELINE_AND_RESEARCH_ROUTE.json');register=read(root/'REGISTER.json')
    datafile=R/'data/director/cosmology/chronology_source_reviewed_01.json';chapter=R/'docs/director-only/cosmology/CHRONOLOGY_SOURCE_REVIEWED_01.md';receipt=A/'COSMOLOGY_CHRONOLOGY_SOURCE_01_APPLICATION_CHECK.json'
    assert all(not p.exists() for p in [datafile,chapter,receipt])
    now=datetime.now(timezone.utc).isoformat()
    boundaries=[
      'Preserve original87AE FirstCycle and710AE CurrentCycle. Their623-year gap has remainder3 under an assumed uninterrupted ten-year phase. No supplied bridge resolves it; no date is edited.',
      'Primordial Cycles are qualitative ages, distinct from the400-day mortal year, ten-year mortal rotation and operational Opening/Horn clocks. No unprovided conversion is inferred.',
      'Printed chapter/bullet order does not prove every temporal or causal dependency. Relative original-story sequence remains useful with explicit limits.',
      'Owner FirstChoir attack-response intent controls. Preserve the original nascent-chord/formation passages and the unresolved formal timing seam. Do not restore withdrawn one-to-one Harmony mapping.',
      'The nine-verse statement and seven virtue benefits remain as printed. VariableOmega is named, but no additional virtue/benefit or missing verse is invented.',
      'Keep original ShardofAbsoluteRest andQ6focusingcrystal distinct until explicitly linked. Preserve producesORexposes, no guaranteed kill/drop.',
      'Keep OldGod/survivor/Ulnak/eleventhshard/Heartcellbuilder/Binding/Interstice identities unmerged. FailedSixthGate remains the reliable public expedition ceiling.',
      'OriginalP324 permits explicit independent/multi-era adaptation. It does not automatically place libraries or activate EPI01–17 mechanics.'
    ]
    data={'reviewId':'COSMOLOGY-CHRONOLOGY-SOURCE-01','recordedAtUtc':now,'status':'jointly-reviewed scoped source-reference; creative and operating proposals remain separate',
      'scope':'Source comparison and protected boundaries only. The first route is incomplete and under CR-F01..08 revision. This record does not adopt its Floor68 placement, prospective710AE scheduling, or pre-Proof-War frame.',
      'archive':info(A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_Addendum_and_Evidence.zip'),'verification':info(check),
      'sourceQualifiedTimeline':model['sourceQualifiedTimeline'],'sourceBoundaries':boundaries,'epilogueNextWorkPlanning':model['epilogueNextWork'],
      'conferenceRegisterAsReceived':register,'sourceBindings':read(A/'cosmology-chronology-research-route-01/SOURCE_BINDINGS.json'),
      'ownerQuestionPending':{'subject':'Campaign relationship to original ProofWar','choices':['before','during','after'],'answerReceived':False},
      'proposalsNotAdopted':['prospective710AE scheduling anchor','pre-Proof-War campaign default','WaxLibraryFloor68 and unfinished route','reader-facing implementation changes','epilogue operating mechanics'],
      'actualLocalRenderEvidence':info(A/'COSMOLOGY_COMPANION_RENDER_REVIEW_01.json'),
      'newOperationalRulesAdopted':False,'campaignEpochChosen':False,'sourceDatesEdited':False,'identitiesMerged':False,'epilogueRulesAdopted':False,'runtimeApproved':False,'humanPlaytested':False,'wholeGameApproved':False,'sourceInformationDeleted':0}
    datafile.write_bytes(encoded(data))
    prose=['# Chronology: reviewed source reference','',
      'This is a scoped comparison of the original manuscripts and explicit owner corrections. It preserves source statements and their limits. The [structured record](../../../data/director/cosmology/chronology_source_reviewed_01.json) contains the exact citations, eight dispositions as received, and original-source bindings. Read with [the owner update](HEARTCELL_OWNER_UPDATE_02.md), [Q6](Q6_LATER_LOCK_REVIEWED_01.md) and [the current research rules](SOULS_RESEARCH_REVIEWED_01.md).','',
      '**Still open:** the owner’s campaign-era choice; the historical explanation for87AE/710AE; exact FirstChoir timing and named Harmony mapping; unknown identities; complete research-route authorship; all epilogue mechanics. The first route remains under revision. Its proposed Floor68 placement and710AE scheduling convention are not adopted here.','',
      'The original dates are preserved:87AE FirstCycle and710AE CurrentCycle differ by623years. If one assumes an uninterrupted ten-year phase from87AE, the remainder is3. Neither repetition in the website nor a high research roll supplies the missing historical bridge. Primordial Cycles remain qualitative ages.','',
      'The original nine-verse statement and seven virtue motif benefits are also preserved. VariableOmega is named, but the remaining verse accounting is not supplied; this is not permission to invent another virtue.','',
      '## Relative source sequence','']
    for row in model['sourceQualifiedTimeline']:
        prose += ['### '+row['id']+' — '+row['title'],'',row['sourceFinding'],'','**Limit:** '+row['currentLimit'],'']
    prose+=['## Reader-facing verification','',
      'The local companion was actually rendered during this review. Its Myth & Timeline display still presents the Level97/eleventh-shard Binding assertion and both dates without the current qualifications. Its cosmology reader is reachable from ordinary navigation. The [bounded render record](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_COMPANION_RENDER_REVIEW_01.json) preserves DOM text and screenshots. This is local development evidence, not production, authentication or whole-game approval. Exact player/Director wording and implementation are part of the active conference.','',
      '## Epilogue work ordering','',
      'The established17EPIidentifiers remain unchanged. The following classifications plan the next conference; they do not activate any mechanic.','']
    for row in model['epilogueNextWork']:prose+=['- **'+row['id']+' — '+row['title']+':** '+row['nextWorkClass']+'.']
    chapter.write_text('\n'.join(prose)+'\n',encoding='utf-8',newline='\n')
    assert read(datafile)['sourceQualifiedTimeline']==model['sourceQualifiedTimeline']
    receipt.write_bytes(encoded({'recordedAtUtc':now,'status':'bounded source comparison saved; incomplete operating route remains unadopted','data':info(datafile),'chapter':info(chapter),'sourceCheck':info(check),'sourceChecks':250,'failures':0,'relativeEvents':16,'epiloguePlanningGroups':17,'newOperatingRulesAdopted':False,'campaignEpochChosen':False,'sourceDatesEdited':False,'sourceInformationDeleted':0}))
    print(json.dumps({'data':info(datafile),'chapter':info(chapter),'receipt':info(receipt)}))

if __name__=='__main__':main()
