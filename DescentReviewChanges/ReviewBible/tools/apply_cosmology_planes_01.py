"""Assemble the verified planes reference without promoting spell/design proposals."""
from datetime import datetime,timezone
import json,collections
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    check=A/'COSMOLOGY_PLANES_01_LOCAL_CORRECTED_RETURN_CHECK_V2.json';c=read(check)
    assert c['applicationAllowed'] and c['failureCount']==0
    root=A/'cosmology-planes-01-corrected-return';old=A/'cosmology-planes-01-return'
    register=read(root/'REGISTER.json');index=read(root/'PLANE_AND_COURT_INDEX.json');travel=read(root/'TRAVEL_INTERFACE_MATRIX.json')
    before=read(old/'REGISTER.json')
    for a,b in zip(before['issues'],register['issues']):
        for k in ['id','topic','disposition','decision','retainedFacts','mortalBeliefs','proposedClarifications','unresolvedDependencies']:assert a[k]==b[k],(a['id'],k)
    inventory=read(A/'cosmology-planes-01/sources/DescentReviewChanges/ReviewBible/data/director/cosmology/planes_source_inventory_draft_01.json')
    assert len(index['records'])==len(inventory['records'])==76
    for a,b in zip(inventory['records'],index['records']):assert all(b.get(k)==v for k,v in a.items())
    assert {x['name'] for x in travel['unadoptedCompleteTransportProposals']}=={'Teleport Object','Teleportation Circle'}
    spell_index=R/'data/public/spell_playtests/authored_review_index.json';spell_before=info(spell_index)
    target=R/'data/director/cosmology/planes_reviewed_01.json';chapter=R/'docs/director-only/cosmology/PLANES_REVIEWED_01.md';receipt=A/'COSMOLOGY_PLANES_01_APPLICATION_CHECK.json'
    assert all(not p.exists() for p in [target,chapter,receipt])
    now=datetime.now(timezone.utc).isoformat()
    qualification={
        'scope':'Jointly reviewed source comparison and current-effect boundaries. New policy proposals retain proposed status. No pending spell or numerical planar-time rule is adopted.',
        'authority':'Original cosmology with explicit owner corrections first. Read HEARTCELL_OWNER_UPDATE_02 and Q6_LATER_LOCK_REVIEWED_01 with this chapter.',
        'epiloguePortability':'The subsequently prepared chronology comparison preserves original P324 permission to adapt tables/relics independently of the saga. This qualifies planning without choosing a campaign epoch or adopting epilogue rules.',
        'websiteVisibility':'Saved HTML and viewer are retained as authored source presentations. The example allowing a Director to use the viewer is subject to its later revelation/public-knowledge qualification; this does not authorize an unqualified public export.',
        'sourceVerification':'64 source bindings refer to the exact frozen input. Current navigation files may have changed since upload; hashes are not a claim that every live file is still identical.',
        'stillOpen':['Operational souls/death jurisdiction','Research and Hunt procedures','Campaign epoch and revelation','Precise cross-map equivalences','First Choir chronology and named Harmony mapping','Pending higher travel spells','Runtime implementation and human balance']}
    data={'reviewId':'COSMOLOGY-PLANES-01','recordedAtUtc':now,'status':'jointly-reviewed-scoped-reference; unresolved dependencies retained','currentQualification':qualification,
        'reviewArchive':info(A/'COSMOLOGY_PLANES_01_Corrected_Addendum_and_Evidence.zip'),'localVerification':info(check),
        'sourceBindings':read(A/'cosmology-planes-01/SOURCE_BINDINGS.json'),'sourceBindingScope':'frozen supplied packet',
        'register':register,'planeAndCourtIndex':index,'travelInterfaceMatrix':travel,'directActualCardBindings':c['directActualCardBindings'],'semanticCoverage':read(root/'SEMANTIC_COVERAGE.json'),
        'newSpellApprovals':0,'newOperationalRulesAdopted':False,'fullCosmologyApproved':False,'runtimeApproved':False,'humanPlaytestConfirmed':False,'publicExportEnabled':False,'sourceInformationDeleted':0}
    target.write_bytes(encoded(data))
    prefix='# Planes: reviewed Director reference\n\nThe corrected Part 3 return has been checked against the frozen original sources. Read it with the [latest owner decisions](HEARTCELL_OWNER_UPDATE_02.md) and [Q6 endgame boundary](Q6_LATER_LOCK_REVIEWED_01.md). The [structured record](../../../data/director/cosmology/planes_reviewed_01.json) contains the 11 decisions, 76-claim index, cited travel matrix and exact evidence.\n\nNew policy proposals below remain proposals. The [chronology comparison](CHRONOLOGY_RESEARCH_SITES_DRAFT_01.md) also preserves original P324 permission for independent or multi-era adaptation of the epilogue toolbox; this does not automatically activate its mechanics or choose an epoch. Any use of the viewer remains subject to the chapter’s revelation boundary. No public export is enabled by this review.\n\n---\n\n'
    chapter.write_text(prefix+(root/'DIRECTOR_COMPANION.md').read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
    assert info(spell_index)==spell_before
    receipt.write_bytes(encoded({'recordedAtUtc':now,'status':'verified-scoped-successor-applied','archive':data['reviewArchive'],'localVerification':info(check),'reviewedData':info(target),'chapter':info(chapter),'all11SubstantiveDispositionsUnchangedByCorrection':True,'all76OriginalInventoryRecordsRetained':True,'frozenSourceHashesVerified':64,'verificationCheckCount':c['checkCount'],'verificationFailureCount':0,'ordinarySpellIndexUnchanged':spell_before,'proposalIdentities':['Teleport Object','Teleportation Circle'],'firstReturnPreserved':info(A/'COSMOLOGY_PLANES_01_Addendum_and_Evidence.zip'),'newSpellApprovals':0,'newOperationalRulesAdopted':False,'sourceInformationDeleted':0,'fullCosmologyApproved':False,'runtimeApproved':False}))
    print(json.dumps(read(receipt)))

if __name__=='__main__':main()
