"""Freeze the complete current local arc proposal for actual GPT review."""
from datetime import datetime, timezone
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib, json, shutil
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())
def sha(b): return hashlib.sha256(b).hexdigest()

REQUEST = '''Decennium Descent: EPI-15–17 campaign arcs, current revision 05.

This is a proposed continuation beyond the manuscript's epilogue, not permission to choose the owner's unresolved campaign era. Original manuscripts and explicit owner corrections govern. Every new NPC, machine, salary, contract procedure and encounter statistic in this local draft is provisional adaptation authorship. No original source was deleted. The current model and casebook contain the complete local proposal with 67 authored cases. Earlier receipts are preserved history, not current approval.

Read SOURCE_BINDINGS.json and verify all 44 supplied source files against their exact hashes. Read ARCS_MODEL.json, CASEBOOK.json, CURRENT_REVIEW_CONTEXT.json and the preserved review/refinement evidence. Independently challenge the current proposal against those sources; do not accept a local preservation/arithmetic check as semantic, runtime or balance approval.

Resolve all 15 questions from semantic review 03 against the current successors: voyage 04 and geometry 04A, annual contract 05, atmosphere interfaces 06, economy/patents 07, and scene boundaries 07A. Earlier statements that these topics have not yet been drafted are superseded by the current model. None of the proposed resolutions has joint approval. Retain the stable case IDs; an incorrect expectation should receive an explicit before/after correction, not silent deletion.

Review the complete mass/Load, crew, fuel, air, airlock, mooring, canopy, repair and actual work/Transition procedures. The ordinary powered-idle voyage remains 32100 seconds with 117m48s fuel and 185m air remaining; an advance wage payment changes its actual manifest. Preserve real source costs, timing markers, anatomy, qualifications and independent weight/Load limits. Review all 14 environment dispositions, especially NEW climate-acclimation, component selection and automatic-completion interpretations; no class or ancestry source has changed.

Check annual record opening/due dates, timely review/notice, the one first-rejection grace, actual channel outages, informed exit, refund/forfeiture, true death and the one original bond. The new patent content must agree with that unchanged contract-state model. The knowledge benefit now includes a complete local CF-pattern proof-press procedure, diagnostic evidence, retained readable diagrams and finite appointment/access privileges. It is not a general engine power or ownership of Cania's Frozen Engine. Check whether those rights and practical benefits justify the annual-contradiction hook, and propose explicit alternatives if they do not.

The refusal scene now concerns real access to the first finite new set of patent plates: guild inspection, public reading or agreed shared access. ACCEPT there never signs the annual contract. Critique the scene as adventure design as well as mechanics: the reasons and consequences should be meaningful, both stakeholders should be credible, and the follow-through should create playable decisions. Preserve actual consent, ordinary departure and no requirement for a player's private beliefs. Verify the six cells, two seals, six print sheets, six impressions, existing claimant copy set, actual pressure/drive states and the one 25 gp fee. A permission or promise cannot create physical stock.

Payment pools are separate actual 150/200/40/6/25 gold coins. Coin weight comes from the included equipment acquisition guide. Examine named custody, 10 gp per actual crew member per sortie, abort/advance/missing funds, three stable scrap serials and no double payment. ARC15-C01 deliberately no longer asserts a fixed hostile-site duration: use its actual site clock, with initiative before lens manipulation. Preserve the original constellation 'flickers out nightly' premise, not merely dimming. Exact Equinox placement and every detailed local ending remain explicit proposed authoring choices.

Dependency: your EPI-08–14 return was reported finished (70386 bytes; SHA256 24eeecec44d1ed248e96adf1d58b80b5c7f8434a3fdb487bdf7443c272de4699), but those exact bytes have not been recovered locally. Do not claim that cross-module review or adoption is complete. Identify any dependency on those exact relic/Null/chamber rules and preserve source-specific differences. Do not silently revise earlier adopted EPI-01–07 to make these later arcs fit.

Return one ZIP named DD_Cosmology_Epilogue_Campaign_Arcs_01_Return.zip with exactly these eight root files:
REGISTER.json, CAMPAIGN_ARCS_MODEL.json, PLAYER_CHAPTER.md, DIRECTOR_CHAPTER.md, CASEBOOK.json, SOURCE_HASHES.json, VERDICT.md, EVIDENCE_MANIFEST.json.

REGISTER: dispositions for every source hook and all fifteen review issues, exact source locations, NEW design labels, remaining seams and explicit correction reasons. MODEL: complete reviewed candidate, not a patch-only fragment. PLAYER_CHAPTER: useful handouts, visible risks/choices and actual benefits without concealed Director material. DIRECTOR_CHAPTER: complete runnable scenes, maps/positions, NPC motivations/profiles, inventory/custody, clocks, interruption/withdrawal/failure procedures, rewards and follow-through. CASEBOOK: all 67 stable incoming cases, explicitly corrected where needed, plus necessary new cases. SOURCE_HASHES: all 44 exact input source identities. VERDICT: distinguish authored-candidate review from unresolved epoch, runtime, human playtesting, balance, publication and whole-game gates. EVIDENCE_MANIFEST: byte length and SHA256 of every other returned root file, plus any explicit schema/version information needed to read it. Do not include self-referential manifest hashes.

Supply archive byte length and SHA256 in your final message. No source deletions, implied owner campaign answer, automatic catalog promotions or claim that local example counts represent human playtests.
'''

def main():
    now=datetime.now(timezone.utc).isoformat()
    local=A/'cosmology-epilogue-campaign-arcs-local-draft-01'
    packet=A/'cosmology-epilogue-campaign-arcs-05'; archive=A/'DD_Cosmology_Epilogue_Campaign_Arcs_05.zip'
    receipt=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_05_PREPARATION.json'
    assert all(not p.exists() for p in [packet,archive,receipt])
    economy=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ECONOMY_PATENTS_07.json'
    scenes=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_SCENE_BOUNDARIES_07A.json'
    assert read(scenes)['model']==info(local/'ARCS_MODEL.json') and read(scenes)['casebook']==info(local/'CASEBOOK.json')
    assert read(local/'CASEBOOK.json')['count']==67 and read(economy)['failureCount']==read(scenes)['failureCount']==0
    shutil.copytree(A/'cosmology-epilogue-campaign-arcs-04',packet)
    bindings=read(packet/'SOURCE_BINDINGS.json'); currency=R/'docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md'; row=info(currency)
    assert row['path'] not in {x['path'] for x in bindings}; bindings.append(row)
    dest=packet/'sources'/row['path']; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(currency.read_bytes())
    for item in bindings:
        raw=(packet/'sources'/item['path']).read_bytes()
        assert len(raw)==item['bytes'] and sha(raw)==item['sha256'] and (G/item['path']).read_bytes()==raw
    assert len(bindings)==44; (packet/'SOURCE_BINDINGS.json').write_bytes(encoded(bindings))
    for name in ['ARCS_MODEL.json','CASEBOOK.json']:(packet/name).write_bytes((local/name).read_bytes())
    for p,name in [(economy,'ECONOMY_PATENTS_07.json'),(scenes,'SCENE_BOUNDARIES_07A.json')]:(packet/name).write_bytes(p.read_bytes())
    (packet/'REQUEST.txt').write_text(REQUEST,encoding='utf-8',newline='\n')
    validation={'recordedAtUtc':now,'model':info(local/'ARCS_MODEL.json'),'casebook':info(local/'CASEBOOK.json'),'frozenSourcesVerifiedAgainstCurrentAndPacket':44,'economyPatentsChecks':54,'sceneBoundaryChecks':7,'failureCount':0,'scope':'Exact package/source bytes, preserved case IDs, unchanged earlier procedures and selected finite-stock/time arithmetic. Evidence counts overlap and are not independent gameplay runs.','newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False}
    (packet/'LOCAL_VALIDATION.json').write_bytes(encoded(validation))
    context=read(packet/'CURRENT_REVIEW_CONTEXT.json')
    context.update(recordedAtUtc=now,packetRevision='05',sourceCount=44,authoredCases=67,currentLocalModel=info(local/'ARCS_MODEL.json'),currentLocalCases=info(local/'CASEBOOK.json'),currentValidation=validation,economyPatents=info(economy),sceneBoundaries=info(scenes),openJointReviewIssues='All local proposals require real GPT semantic review, including the substantive knowledge/access scene and source-specific EPI08–14 integration. Runtime, human, balance, epoch, whole-game and publication gates remain false.',status='prepared-not-submitted; all later arc procedures remain unadopted')
    (packet/'CURRENT_REVIEW_CONTEXT.json').write_bytes(encoded(context))
    entries=[{'path':p.relative_to(packet).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(packet.rglob('*')) if p.is_file() and p!=packet/'PACKAGE_MANIFEST.json']
    (packet/'PACKAGE_MANIFEST.json').write_bytes(encoded({'files':entries}))
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for p in sorted(packet.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(packet).as_posix())
    with ZipFile(archive) as z:
        assert set(z.namelist())=={x['path'] for x in entries}|{'PACKAGE_MANIFEST.json'}
        for x in entries:
            raw=z.read(x['path']); assert len(raw)==x['bytes'] and sha(raw)==x['sha256']
    receipt.write_bytes(encoded({'recordedAtUtc':now,'status':'prepared-not-submitted','archive':info(archive),'supersedesForSubmission':info(A/'DD_Cosmology_Epilogue_Campaign_Arcs_04.zip'),'sourceCount':44,'authoredCases':67,'economyPatents':info(economy),'sceneBoundaries':info(scenes),'currentModel':info(local/'ARCS_MODEL.json'),'currentCases':info(local/'CASEBOOK.json'),'sourceInformationDeleted':0,'newRulesAdopted':False,'campaignEpochChosen':False,'runtimeTestsExecuted':0,'humanPlaytested':False,'jointReviewComplete':False,'dependency':'Restore actual GPT exchange and recover/review the exact EPI08–14 return before cross-module adoption.'}))
    print(json.dumps({'preparation':info(receipt),'archive':info(archive),'sources':44,'cases':67,'submitted':False}))

if __name__=='__main__':main()
