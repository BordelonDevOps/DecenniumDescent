"""Package the current voyage proposal with all exact sources and preserved audits."""
from datetime import datetime,timezone
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json,shutil
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
REQUEST='''Review the current three conditional post-epilogue campaign arcs. This is conference packet revision03, a local proposal, not adopted rules or owner direction. It supersedes earlier input packets for eventual submission; preserve all prior history.

Read CURRENT_REVIEW_CONTEXT.json, ARCS_MODEL.json, CASEBOOK.json, SEMANTIC_REVIEW_03.json, VOYAGE_REFINEMENT_04.json and VOYAGE_GEOMETRY_04A.json, then relevant actual supplied sources. The current model is the complete local successor with28case IDs. Source bindings contain42frozen files, including the newly supplied actual equipment-weight reference. Original Cosmology paragraphs319–322 govern the three hooks. All new procedures/numbers are proposed authorship, not recovered cosmological canon.

Current source corrections retain bards across Aethel and random future tune losses, the actual errant-equation cause in the Broken Ladder strand, and Mephistopheles envoy in the Canian patent offer. Do not identify the local errant equation as the missing original cosmic Equation. Keep the owner-corrected Cania-only scope and unresolved identities. The400day Aethel civil year is separate from primordial/celestial intervals. The campaign-era question is unanswered: maintain conditional post-epilogue staging and no assumed AE date, new numbered floor or hidden-identity merge.

Review03 found15issues. Five received narrow local corrections; voyage04/04A now proposes fuller resolutions for the support, inventory, hatch and complete-clock problems. That is not joint approval. Independently review the actual dry-hull/payload/Load and finite stock ledger, crew and PC capacity, foot positions, two-door airlock, purge and protection order, support modes, fuel-zero and missing-crew boundaries, ordinary Falling/canopy distinction, and the real20-interval site schedule. Inspect every remaining paragraph for contradictions with the new fields. Do not approve merely because arithmetic checks pass.

The fully specified ordinary sample now takes32100seconds=8h55m:18000outbound+3726site+7200return+6deployment+3168descent. Powered-idle fuel use28932seconds=482m12s, fuel left117m48s, air left185minutes. The second hood is activated between phases to allow actual return/purge; no hidden extra hour or free boarding. A securely moored engine-off plan spends12powered seconds on site and420m18s overall; it saves fuel, not elapsed air time. Old31968/33768second totals are preserved history and must not be reused as current full-voyage clocks. The sample worker is Burdened toSpeed20, and the printed paths fit that speed. Check these facts independently and correct them if needed while retaining all28IDs.

Outstanding environment interpretation requires exact supplied ancestry/class sources: Mountain Born, cold-climate adaptations, Nomadic Human saves, Mycelian/Undead and actual Mage no-breath, Druid cold card and Warrior timed adaptations. Decide the actual natural/magical, cold, altitude and inhalation components explicitly; honor real permissions and limits without renaming the hazard to defeat them. Include equality between adaptation completion and exposure, resistance/Exhaustion interaction, protection expiry, and genuine full-footprint alternatives. Current EPI01–07 remains authoritative. Any Transition extension to Phase2+3 salvage must be explicitly NEW, with exact shared allowance, beneficiaries, work-order, qualifications, interruption and rounding; do not change existing motifs silently.

Finish the unresolved annual contract operating state: exact numbered annual records, early submission/retirement, bond-return requirement, due/review/grace/default/issuer-absence ordering, paper custody and actual notice. Future due dates stay anchored toT0, one400day interval per year. ARC17-C06 now contains an actual24hour review and must not return to a zero-duration example. Preserve informed choice and source annual obligations, while developing substantial actual patent knowledge and meaningful free-will choices. The current limited demonstrations and paid-choice exercise are proposals to review, not sufficient merely because they have finite numbers. Do not replace real design with arbitrary soul penalties, compulsory character changes or generic machine omnipotence.

Also complete real finite wages/scrap-buyer/reward custody, all scene entry/exit/NPC/item procedures, and EPI15hazard/hostility clocks. Use actual capabilities and ordinary alternatives. Do not promote pending spells, unreviewed bestiary stats or trade recipes. Crafting totals remain687 reviewed trade recipes; a scene does not automatically add a recipe card.

The existing EPI08–14 response is already completed in this actual conversation and reportedly has47cases. Its exact archive has not yet been retrieved or independently reviewed by Codex. Do not reauthor that package or infer joint approval from its existence. Cross-module adoption remains conditional on review of its actual relic/Null rules. If that independent integration remains unavailable, explicitly identify the unresolved interface while completing independent parts.

Produce a complete independently repaired successor and real playable player/Director prose, not merely approval or JSON references. Include finite physical handouts, full actor/craft/contract profiles, ordinary/adverse/equality/missing-access/depletion cases, and numerical complete schedules. Preserve all28current case IDs; correct their assumptions/results explicitly and add cases as necessary. Authored worked cases are not executed runtime tests.

Return DD_Cosmology_Epilogue_Campaign_Arcs_01_Return.zip with exactly8root files:
REGISTER.json; CAMPAIGN_ARCS_MODEL.json; PLAYER_CHAPTER.md; DIRECTOR_CHAPTER.md; CASEBOOK.json; SOURCE_HASHES.json; VERDICT.md; EVIDENCE_MANIFEST.json.
SOURCE_HASHES must reproduce all42 supplied SOURCE_BINDINGS path/bytes/sha256 entries from actual files. Cite original all-w:p zero-based paragraph indices and current sources by exact JSONPointer or one-based line range. JSON root pointer is empty string. Exact excerpts or UTF8SHA256 must match; provenance never makes invented numbers historical. EVIDENCE_MANIFEST lists exact bytes/SHA256 for the other seven outputs, not itself. Keep campaignEpoch, runtime, human, balance, wholeGame and publication gates false. Explain concrete corrections and genuine remaining boundaries, then link the archive.
'''
def main():
    now=datetime.now(timezone.utc).isoformat()
    local=A/'cosmology-epilogue-campaign-arcs-local-draft-01';previous=A/'cosmology-epilogue-campaign-arcs-02'
    packet=A/'cosmology-epilogue-campaign-arcs-03';archive=A/'DD_Cosmology_Epilogue_Campaign_Arcs_03.zip'
    receipt=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_03_PREPARATION.json'
    assert all(not p.exists() for p in [packet,archive,receipt])
    geom=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_VOYAGE_GEOMETRY_04A.json';refine=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_VOYAGE_REFINEMENT_04.json'
    assert read(geom)['model']==info(local/'ARCS_MODEL.json') and read(geom)['casebook']==info(local/'CASEBOOK.json')
    assert read(local/'CASEBOOK.json')['count']==28 and read(refine)['failureCount']==read(geom)['failureCount']==0
    shutil.copytree(previous,packet)
    bindings=read(packet/'SOURCE_BINDINGS.json');equipment=R/'docs/mechanics/EQUIPMENT_SOURCE_BINDINGS.md'
    row=info(equipment);assert row['path'] not in {x['path'] for x in bindings};bindings.append(row)
    dest=packet/'sources'/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(equipment.read_bytes())
    for source in bindings:
        raw=(packet/'sources'/source['path']).read_bytes();assert len(raw)==source['bytes'] and sha(raw)==source['sha256'] and (G/source['path']).read_bytes()==raw
    assert len(bindings)==42
    (packet/'SOURCE_BINDINGS.json').write_bytes(encoded(bindings))
    for name in ['ARCS_MODEL.json','CASEBOOK.json']:(packet/name).write_bytes((local/name).read_bytes())
    for source,name in [(refine,'VOYAGE_REFINEMENT_04.json'),(geom,'VOYAGE_GEOMETRY_04A.json')]:(packet/name).write_bytes(source.read_bytes())
    (packet/'REQUEST.txt').write_text(REQUEST,encoding='utf-8',newline='\n')
    validation={'recordedAtUtc':now,'model':info(local/'ARCS_MODEL.json'),'casebook':info(local/'CASEBOOK.json'),'frozenSourcesVerifiedAgainstCurrentAndPacket':42,'inheritedVoyageChecks':53,'geometryClarificationChecks':6,'failureCount':0,'scope':'Current source/package bytes and inherited explicitly bounded source/arithmetic/geometry checks. Does not certify semantic completeness, runtime or playtest.','baseEvidence':'VOYAGE_REFINEMENT_04.json','successorEvidence':'VOYAGE_GEOMETRY_04A.json','newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False}
    (packet/'LOCAL_VALIDATION.json').write_bytes(encoded(validation))
    context=read(packet/'CURRENT_REVIEW_CONTEXT.json');context.update(recordedAtUtc=now,packetRevision='03',sourceCount=42,authoredCases=28,currentLocalModel=info(local/'ARCS_MODEL.json'),currentLocalCases=info(local/'CASEBOOK.json'),currentValidation=validation,voyageRefinement=info(refine),geometryClarification=info(geom),openJointReviewIssues='All local proposals need joint review. ARC03-02/03/04/05/06 now have concrete local voyage resolutions; environment, annual contract states, finite payment custody, substantive knowledge/choice design and EPI08–14 integration remain unresolved.',status='prepared-not-submitted; all later arc procedures remain unadopted')
    (packet/'CURRENT_REVIEW_CONTEXT.json').write_bytes(encoded(context))
    entries=[{'path':p.relative_to(packet).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(packet.rglob('*')) if p.is_file() and p!=packet/'PACKAGE_MANIFEST.json']
    (packet/'PACKAGE_MANIFEST.json').write_bytes(encoded({'files':entries}))
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for p in sorted(packet.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(packet).as_posix())
    with ZipFile(archive) as z:
        assert set(z.namelist())=={e['path'] for e in entries}|{'PACKAGE_MANIFEST.json'}
        for e in entries:
            raw=z.read(e['path']);assert len(raw)==e['bytes'] and sha(raw)==e['sha256']
    receipt.write_bytes(encoded({'recordedAtUtc':now,'status':'prepared-not-submitted','archive':info(archive),'supersedesForSubmission':info(A/'DD_Cosmology_Epilogue_Campaign_Arcs_02.zip'),'sourceCount':42,'authoredCases':28,'siteIntervals':20,'ordinaryVoyageSeconds':32100,'voyageRefinement':info(refine),'geometryClarification':info(geom),'currentModel':info(local/'ARCS_MODEL.json'),'currentCases':info(local/'CASEBOOK.json'),'sourceInformationDeleted':0,'newRulesAdopted':False,'campaignEpochChosen':False,'runtimeTestsExecuted':0,'humanPlaytested':False,'jointReviewComplete':False,'dependency':'Restore actual GPT exchange and retrieve/review EPI08–14 archive before cross-module adoption.'}))
    print(json.dumps({'preparation':info(receipt),'archive':info(archive),'sources':42,'cases':28,'submitted':False}))
if __name__=='__main__':main()
