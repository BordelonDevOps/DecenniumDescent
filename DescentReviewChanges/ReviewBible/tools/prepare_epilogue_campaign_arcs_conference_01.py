"""Freeze current arc drafts and actual dependencies for later joint review."""
from datetime import datetime,timezone
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p):return json.loads(p.read_bytes())

REQUEST='''Review these three conditional post-epilogue campaign arcs in the existing Part3 collaboration after the current EPI08–14 review is recovered. Do not resend or restart that existing review. This packet is a local proposal, not adopted rules or owner direction.

Read CURRENT_REVIEW_CONTEXT.json, ARCS_MODEL.json and CASEBOOK.json, then the actual supplied source manuscripts and current operating rules. OriginalCosmologyP319–322 govern the three hooks; the World source has a400day civil year, separate from primordial/celestial intervals. The owner has not selected a campaign epoch. Preserve each arc's beyond-epilogue condition and conditional actual-site placement. No assumed710AE anchor, identity merge or new numbered floor.

The local draft has already been corrected to preserve bards across Aethel, random future tune losses and the named Canian patent-heir role. The three musicians are only the party's entry point, not the whole affected population. Their initially fixed losses are openly authored setup; later events use the written uniform roll. The actual strand-release event ends future losses; later delivery only proves custody/payment. The current contract has a concrete annual obligation secured by actual50gp, not a cost-free binding that can be erased without fulfilling anything. These operating choices remain NEW and may be improved with explicit reasons.

Please perform a full independent semantic and source review, repair concrete defects and produce complete playable player/Director chapters. Do not merely approve the seven or37 earlier mechanical file checks; they never proved semantic completeness. Check source fidelity, agency, meaningful stakes, actual geography/entry/exit, finite rewards and stock, all NPC/vehicle/item/condition envelopes, crew and action reservations, training, full footprints and payload, air/fuel/breathing/ancestry/class defenses, falling and emergency-descent timing, actual rest/travel clocks, Phase1/2/3 eligibility and interrupted work, proposed Transition extension, original Null interactions afterEPI08–14 review, and the complete contract's due/review/grace/default/retirement/issuer-absence states. Restore meaningful source scope if a proposal inadvertently made the hook merely smaller, safer or trivial. A bounded ordinary failure outcome is legitimate NEW design, but never present it as source text.

Preserve all19 current case IDs and their history, correcting operative examples as needed. Include numerical adverse/equality/missing-access/depletion cases. Especially retain the distinction between the400day due offset34560000seconds and the later12hour review completion34603200seconds. Default voyage uses actual480powered minutes and total31968seconds only for the explicitly stated powered-idle60minute site plan; switching off at a secure mooring changes actual fuel consumption, not air elapsed time.

Do not silently modify current EPI01–07. Any extension, such as Transition affecting the new strand-salvage phases, must be an explicit reviewed addition with exact scope. Do not borrow a pending spell, unreviewed bestiary profile or a source-null vehicle field. All new actor/craft/contract numbers are authored proposals. Broader ordinary-spell/feat/bestiary/crafting catalogs remain unchanged. Existing trade recipes remain687; this module does not auto-add recipe cards.

If EPI08–14 remains unavailable, you may review the independent parts, but list the exact unresolved integration rather than claiming the entire arc candidate approved. Do not choose the owner's campaign era or demand the same unanswered question again.

Return DD_Cosmology_Epilogue_Campaign_Arcs_01_Return.zip with exactly eight root files:
REGISTER.json; CAMPAIGN_ARCS_MODEL.json; PLAYER_CHAPTER.md; DIRECTOR_CHAPTER.md; CASEBOOK.json; SOURCE_HASHES.json; VERDICT.md; EVIDENCE_MANIFEST.json.
The model must be a complete self-contained successor with all three arcs, actor/vehicle profiles, physical handouts and procedures. The two chapters must contain actual usable play text, not just references back toJSON. CASEBOOK must preserve all19 IDs and add any needed cases, explicitly authored/not executed. SOURCE_HASHES must reproduce every supplied SOURCE_BINDINGS.json path/bytes/sha256 from actual files. Cite original paragraphs by all-w:p zero-based index and current records by exact JSONPointer or one-based line range. A JSON root pointer is empty string. Whole quoted location text or its UTF8SHA256 must match; provenance cannot justify invented numbers. EVIDENCE_MANIFEST lists exact bytes/SHA256 for the other seven output files, not itself. Keep runtime/human/balance/wholegame/publication and campaignEpoch gates false. Explain concrete changes and remaining genuine boundaries, then provide the archive link.
'''

def main():
    local=A/'cosmology-epilogue-campaign-arcs-local-draft-01'
    packet=A/'cosmology-epilogue-campaign-arcs-01'
    archive=A/'DD_Cosmology_Epilogue_Campaign_Arcs_01.zip'
    validation=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_LOCAL_DRAFT_01_VALIDATION_02.json'
    receipt=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_01_PREPARATION.json'
    assert all(not p.exists() for p in [packet,archive,validation,receipt])
    d=read(local/'ARCS_MODEL.json');c=read(local/'CASEBOOK.json');checks=[]
    for x in read(local/'MANIFEST.json')['files']:
        raw=(local/x['path']).read_bytes();checks.append({'name':'manifest '+x['path'],'pass':len(raw)==x['bytes'] and hashlib.sha256(raw).hexdigest()==x['sha256']})
    for x in read(local/'SOURCE_BINDINGS.json'):
        raw=(local/'sources'/x['path']).read_bytes();checks.append({'name':'source preservation '+x['path'],'pass':len(raw)==x['bytes'] and hashlib.sha256(raw).hexdigest()==x['sha256']})
    lookup={x['id']:x for x in c['cases']}
    prior=read(local/'history/before-semantic-refinement-02/CASEBOOK.json')
    checks += [
      {'name':'three sourcehook IDs','pass':[x['id'] for x in d['arcs']]==['EPI-15','EPI-16','EPI-17']},
      {'name':'19unique authored cases','pass':c['count']==len(c['cases'])==len(lookup)==19},
      {'name':'all13priorcase IDs retained','pass':all(x['id'] in lookup for x in prior['cases'])},
      {'name':'all gates remain false','pass':all(x is False for x in d['common']['approvalGates'].values())},
      {'name':'firstfragment1830seconds','pass':600+18+600+12+600==lookup['ARC15-C01']['elapsedSeconds']},
      {'name':'defaultflight31968seconds','pass':480*60+528*6==lookup['ARC16-C01']['elapsedSeconds']},
      {'name':'detourflight33768seconds','pass':510*60+528*6==lookup['ARC16-C02']['elapsedSeconds']},
      {'name':'hoodcanopy3174seconds','pass':6+528*6==lookup['ARC16-C03']['elapsedSeconds']},
      {'name':'400daydue34560000seconds','pass':400*24*3600==lookup['ARC17-C01']['dueOffsetSeconds']},
      {'name':'12hourreviewelapsed34603200seconds','pass':400*24*3600+12*3600==lookup['ARC17-C01']['elapsedSeconds']},
      {'name':'11daydeliveryandgrace950400seconds','pass':11*24*3600==lookup['ARC17-C02']['elapsedSeconds']}
    ]
    failures=[x for x in checks if not x['pass']];assert not failures,failures
    now=datetime.now(timezone.utc).isoformat()
    validation.write_bytes(encoded({'recordedAtUtc':now,'model':info(local/'ARCS_MODEL.json'),'casebook':info(local/'CASEBOOK.json'),
      'checks':checks,'checkCount':len(checks),'failureCount':0,'scope':'Files/source preservation, stable case IDs, structure and selected arithmetic only; not semantic acceptance, runtime or human playtesting.',
      'semanticRefinement':info(A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_LOCAL_DRAFT_01_SEMANTIC_REFINEMENT_02.json'),'newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False}))
    paths=[G/x['path'] for x in read(local/'SOURCE_BINDINGS.json')]
    paths += sorted(p for p in (R/'data/public/class_playtests').glob('*.json') if p.name!='manifest.json')
    paths += [R/'data/public/Decennium_Descent_Bard_Playtest_v0_1.json']
    paths += [R/'docs/mechanics'/name for name in ['ANCESTRY_BACKGROUND_PLAYTEST.md','ANCESTRY_BACKGROUND_SOURCE_BINDINGS.md',
      'BODY_EQUIPMENT_PLAYTEST.md','EQUIPMENT_ITEM_PROCEDURES.md','LANGUAGE_COMMUNICATION_PLAYTEST.md','COMBAT_ACTION_PLAYTEST.md',
      'CONDITIONS_PLAYTEST.md','CHARACTER_FOUNDATION_TABLES.md','CRAFTING_HARVEST_PLAYTEST.md']]
    paths += [R/'docs/playtest/SESSION_ZERO_PLAYTEST.md',R/'data/director/cosmology/souls_research_reviewed_01.json',
      R/'data/director/cosmology/chronology_research_route_reviewed_01.json',A/'COSMOLOGY_EPILOGUE_CHARACTER_01_APPLICATION_CHECK.json']
    paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
    packet.mkdir();rows=[]
    for p in paths:
        row=info(p);out=packet/'sources'/row['path'];out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(p.read_bytes());rows.append(row)
    for name in ['ARCS_MODEL.json','CASEBOOK.json']:(packet/name).write_bytes((local/name).read_bytes())
    (packet/'SOURCE_BINDINGS.json').write_bytes(encoded(rows));(packet/'REQUEST.txt').write_text(REQUEST,encoding='utf-8',newline='\n')
    (packet/'LOCAL_VALIDATION.json').write_bytes(validation.read_bytes())
    (packet/'CURRENT_REVIEW_CONTEXT.json').write_bytes(encoded({'reviewId':'COSMOLOGY-EPILOGUE-CAMPAIGN-ARCS-01','recordedAtUtc':now,
      'status':'prepared,not submitted; all local proposals unadopted','currentCharacterModule':'EPI01–07 exactLP01–LP10 jointly confirmed/applied;110authored cases.',
      'relicNullReview':'EPI08–14 already submitted in actualPart3,83sources; response not yet retrieved because browser observations time out. Do not infer generation stopped or silently replace it.',
      'epoch':'Owner question before/during/afterProofWar remains unanswered. Conditional post-epilogue frame only; no date chosen.',
      'sourceCount':len(rows),'arcs':3,'authoredCases':19,'spellCoverage':{'reviewed':419,'pending':429},
      'gateReminder':'No runtime,human,balance,wholegame,publication orcosmologicalcanon approval. Original sources and explicitowner corrections govern.',
      'currentLocalModel':info(local/'ARCS_MODEL.json'),'currentLocalCases':info(local/'CASEBOOK.json'),'currentValidation':info(validation),
      'newRulesAdopted':False,'sourceInformationDeleted':0}))
    manifest=[{'path':p.relative_to(packet).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(packet.rglob('*')) if p.is_file()]
    (packet/'PACKAGE_MANIFEST.json').write_bytes(encoded({'files':manifest}))
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for p in sorted(packet.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(packet).as_posix())
    receipt.write_bytes(encoded({'recordedAtUtc':now,'status':'prepared-not-submitted','archive':info(archive),'sourceCount':len(rows),
      'arcs':3,'authoredCases':19,'localValidation':info(validation),'newRulesAdopted':False,'sourceInformationDeleted':0,'campaignEpochChosen':False,
      'runtimeTestsExecuted':0,'humanPlaytested':False,'dependency':'Recover and review the existingEPI08–14 response before closingcross-module adoption.'}))
    print(json.dumps({'preparation':info(receipt),'archive':info(archive),'sources':len(rows),'cases':19,'localChecks':len(checks),'failures':0,'submitted':False}))
if __name__=='__main__':main()
