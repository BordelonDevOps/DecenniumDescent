"""Preserve a preliminary plane comparison and actual spell dependencies, without promotion."""
from datetime import datetime, timezone
from collections import Counter
import hashlib, json, re
from apply_di7_ap_as_01 import G, R, A, info, encoded


def main():
    output = A/'COSMOLOGY_PLANES_SOURCE_CONCORDANCE_01.json'
    assert not output.exists()
    idx_path = A/'cosmology-gods-pantheons-01/DOCX_PASSAGE_INDEX.json'
    pub_path = A/'cosmology-gods-pantheons-01/EXACT_PUBLICATION_PASSAGES.json'
    idx = json.loads(idx_path.read_bytes())['documents']
    cosmology = {x['paragraphIndexZeroBased']:x for x in idx['The Cosmology of Decennium Descent.docx'] if x['part']=='word/document.xml'}
    public = {x['paragraphIndexZeroBased']:x for x in json.loads(pub_path.read_bytes())['playerAppendixB']['paragraphs']}
    index_path = R/'data/public/spell_playtests/authored_review_index.json'
    catalog_path = R/'data/public/spell_playtests/catalog.json'
    higher_path = R/'data/director/higher_spell_operating_proposal_index.json'
    spell_index = json.loads(index_path.read_bytes())
    catalog = {x['id']:x for x in json.loads(catalog_path.read_bytes())['spells']}
    higher = {x['spellId']:x for x in json.loads(higher_path.read_bytes())['entries']}
    pattern = r'plane|planar|astral|ethereal|teleport|gate|portal|banish|dimension|blink|rift|summon'
    selected = [x for x in spell_index['entries'] if re.search(pattern,x['id'],re.I)]
    spell_rows = [{'authoredIndexEntry':x,'wholeCurrentCatalogCard':catalog[x['id']],'higherProposalIndexEntry':higher.get(x['id'])} for x in selected]
    public_names = {
        'material':[(10115,'Material Plane')],
        'transitive':[(10131,'Ethereal Plane'),(10143,'Astral Plane'),(10155,'Veiled Expanse'),(10167,'Verdant Reflection')],
        'elemental':[(10187,'Plane of Earth'),(10188,'Plane of Water'),(10189,'Plane of Air'),(10190,'Plane of Fire')],
        'paraElemental':[(10193,'Plane of Ice'),(10194,'Plane of Magma'),(10195,'Plane of Ooze'),(10196,'Plane of Smoke')],
        'energy':[(10204,'Plane of Positive Energy'),(10205,'Plane of Negative Energy'),(10206,'Plane of Arcane Energy'),(10207,'Plane of Psionic Energy')],
        'upper':[(10219,'Fields of Grace'),(10220,'Sevenfold Ascent'),(10221,'Wildbloom Courts'),(10222,'Ordered Marches'),(10223,'Twin Hearths')],
        'lower':[(10231,'Nine Infernal Courts'),(10232,'Abyss'),(10233,'Red Prison'),(10234,'Ashen Waste'),(10235,'Cinder Slopes')],
        'neutral':[(10243,'Clockwork Mandala'),(10244,'Chaos Sea'),(10245,'Concordant Expanse'),(10246,"Hero's Reach"),(10247,'War-Cube Marches')],
    }
    names = []
    for group, values in public_names.items():
        for paragraph, name in values:
            assert name in public[paragraph]['text'], name
            names.append({'name':name,'group':group,'authority':'Current Appendix B mortal cosmographic teaching, under Q5 and P9977/P10113; not a proven universal topology.','sourceParagraph':public[paragraph]})
    assert len(names)==32
    def row(identifier,topic,finding,action,cosmo=(),player=(),other=()):
        return {'id':identifier,'topic':topic,'localFinding':finding,'proposedReviewAction':action,'originalCosmologyParagraphs':[cosmology[n] for n in cosmo],'currentPlayerParagraphs':[public[n] for n in player],'otherSources':list(other),'jointReviewCompleted':False}
    issues = [
        row('PL-01','Two plane maps have different authority',
            'The original Planes Ascendant narrative has four principal realms. Current Appendix B teaches a Wheel of Testimony containing 32 individually listed plane labels. Q5 makes the Great Wheel mortal cosmography.',
            'Preserve both accounts and their authority. Do not force a one-to-one equivalence or conclude that a mortal map proves its worlds fictitious.',range(60,75),[9977,10111,10113]),
        row('PL-02','Veiled Expanse name overlap',
            'The original twilight/memory dominion and the player shadow-reflection account share a name; the current Shadow Conclave adds claims of death jurisdiction.',
            'Compare the accounts without silently deciding whether every geographical, ruler and soul-route claim is objectively identical.',[64,65,272],[10155,10157,10159,10355,10363]),
        row('PL-03','Fire realm and dungeon echo',
            'Bastion of Flame has a source origin and Choir stewardship; Appendix B has Plane of Fire and the Eternal Flame court. The World/Dungeon guide separately labels Brogi a Plane of Fire echo.',
            'Distinguish plane, court, site and dungeon echo; determine which links are explicit and which remain unproved.',[63,64,271],[10190,10331,10337],['DescentReviewChanges/ReviewBible/docs/mechanics/WORLD_DUNGEON_LOOP.md']),
        row('PL-04','Dream, thought, Astral and Fey',
            'Radiant Currents, Boundless Void, Astral Plane and Verdant Reflection overlap thematically while having different descriptions and authority.',
            'Do not merge dream/thought/Fey places by theme. Separate planar identity from a particular travel or perception effect.',[65,66,67,68,273,274],[10143,10145,10147,10167,10169,10171,10343]),
        row('PL-05','Connections and tributary realms',
            'Confluence Straits mediate inter-plane exchanges; P71 names four tributary realms. Public teaching separately lists natural portals, touchpoints and magical routes.',
            'Preserve source connections while leaving operational endpoint, access, cost, consent, return and hazard rules to explicit procedures.',[68,69,71,73],list(range(10251,10284))),
        row('PL-06','Court and ruler authority',
            'The public text names four Elemental Courts, four Fey Courts, four Shadow Conclave members and four Astral Dominions. The gods review leaves objective jurisdiction open.',
            'Inventory each named institution and its taught domain. Do not promote a folk rank into cosmic seniority or fill the Maladomini ruler gap.',[56,79,120,121],list(range(10329,10376))),
        row('PL-07','Planar time and the Opening clock',
            'Dream and Astral source descriptions bend time; the source epilogue adds home-plane rest rewards. Owner Q4 sets the Opening and Horn clocks.',
            'Require explicit travel/time/return rules; do not let descriptive time language silently stop the campaign clock or grant rests, durations or resource recovery.',[66,276],[10135,10145,10283],['docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md']),
        row('PL-08','Actual spell status and transit permission',
            'Plane Shift, Planar Gate and other central transit effects are still pending authored procedures. Blink is receipt-only pending cosmology. Reviewed local portals and other name matches have their own limited procedures.',
            'Reconcile topology with actual operational spell sources and pending proposals. A named plane, portal service price or source spell summary is not a complete travel permission.',[],[10277,10278,10279,10280,10281],['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json','DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json','DescentReviewChanges/ReviewBible/data/director/higher_spell_operating_proposal_index.json']),
        row('PL-09','Epilogue map and campaign epoch',
            'P270-P276 offers a Spiral Map and home-plane choices at session zero after the source saga. The current campaign revelation ladder restricts common knowledge of the hidden machinery.',
            'Keep the source map and game rules inventoried. Decide epoch and disclosure before using it as a current player handout; no automatic home-plane benefits.',range(270,277),[9977],['DescentReviewChanges/ReviewBible/docs/canon/PLAYER_DIRECTOR_BOUNDARY.md','docs/audit/2026-10-08/full-game/ORIGINAL_COSMOLOGY_EPILOGUE_RULE_INVENTORY_01.json']),
        row('PL-10','Void labels and souls',
            'Boundless Void is a questioning dominion, whereas the public Void Sovereign is an entity claim. Astral soul transit and Shadow soul collection are further distinct claims.',
            'Preserve distinctions among place, title, being and state. Carry soul/death jurisdiction and Interstice/Old-God identity to their ordered reviews.',[67,154,274],[10145,10363,10407]),
    ]
    paths = [
        G/'The Cosmology of Decennium Descent.docx',G/'The Decennium Descent and the Matrix of Oblivion.docx',G/'The_World_of_Aethel_Lore.docx',
        G/'books/player/Decennium_Descent_Player_Rulebook_v6.docx',G/'docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md',G/'docs/mechanics/APPENDIX_B_FOLK_RELIGION.md',
        R/'docs/canon/PLAYER_DIRECTOR_BOUNDARY.md',R/'docs/mechanics/WORLD_DUNGEON_LOOP.md',
        R/'docs/mechanics/expedition/EXPEDITION_BOUNDARY_WALKTHROUGHS.md',idx_path,pub_path,index_path,catalog_path,higher_path,
        A/'ORIGINAL_COSMOLOGY_EPILOGUE_RULE_INVENTORY_01.json',A/'COSMOLOGY_GODS_PANTHEONS_01_RECEIVED_DECISION.json',
    ]
    bindings = [info(p) for p in paths]
    document = {
        'concordanceId':'COSMOLOGY-PLANES-SOURCE-CONCORDANCE-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'preliminary source concordance; not yet submitted to GPT or adopted',
        'sourceBindings':bindings,'originalPrimaryRealms':['Bastion of Flame','Veiled Expanse','Radiant Currents','Boundless Void'],
        'originalTributaryRealmsAtP71':['Molten Glass Tapestries','Luminous Dusk','Whispering Archive','Calculated Pyre'],
        'publicNamedPlaneLabels':names,'publicNamedPlaneLabelCount':len(names),'issues':issues,
        'spellDependencyDiscovery':{'method':'Case-insensitive name/ID screening of all 848 current authored-index entries using '+pattern,
            'limits':'Finite discovery only; not an exhaustive semantic dependency audit. Summoned objects and local movement matches may not actually use another plane. Existing authored status is preserved; source inclusion is not approval.',
            'matchedCount':len(spell_rows),'matchedAuthoredStatuses':dict(Counter(x['authoredIndexEntry']['authoredStatus'] for x in spell_rows)),
            'rows':spell_rows},
        'semanticReadForThisConcordance':['Original Cosmology P60-P76 and P270-P276','Current Player Appendix B P10111-P10287 and P10329-P10387','Owner Q3-Q7 and current Player/Director boundary','Plane Shift, Planar Gate and Blink whole catalog cards; targeted higher proposal status records; transport price-versus-permission example'],
        'remainingBeforePlanesConference':['Receive and verify gods/pantheons follow-up','Read actual relevant Director plane passages and Matrix plane/crossing accounts in full context','Review existing authored transit/summoning procedures and frozen receipts, including Blink','Resolve authority provenance for later World/Dungeon notes rather than treating their status labels alone as new owner decisions','Check any separately completed owner cosmology decisions before applying dependent changes'],
        'sourceInformationDeleted':0,'originalSourcesModified':False,'newRulesAdopted':0,'fullCosmologyApproved':False,
    }
    for binding in bindings: assert info(G/binding['path']) == binding
    output.write_bytes(encoded(document))
    print(json.dumps({'concordance':info(output),'issueRows':len(issues),'publicNamedPlaneLabels':len(names),'spellNameMatches':len(spell_rows),'statusCounts':document['spellDependencyDiscovery']['matchedAuthoredStatuses']}))


if __name__ == '__main__': main()
