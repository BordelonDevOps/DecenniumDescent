"""Freeze source evidence and proposed identity comparisons for an actual GPT conference."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, zipfile

G = Path('C:/Github/DecenniumDescent')
R = G/'DescentReviewChanges/ReviewBible'
A = G/'docs/audit/2026-10-08/full-game'
P = A/'cosmology-gods-pantheons-01'
ZIP = A/'DD_Cosmology_Gods_Pantheons_01.zip'
REPORT = A/'COSMOLOGY_GODS_PANTHEONS_01_PREPARATION.json'
RID = 'COSMOLOGY-GODS-PANTHEONS-01'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def jraw(data):
    return (json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode()

def write(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f:
        f.write(raw)

def bind(path):
    raw = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}

def main():
    assert not P.exists() and not ZIP.exists() and not REPORT.exists(), 'One-use preparation: preserve existing evidence.'
    previous = json.loads((A/'cosmology-creation-origin-01/SOURCE_HASHES.json').read_bytes())
    for name, digest in previous.items():
        assert sha((G/name).read_bytes()) == digest, name
    names = set(previous)
    publication = json.loads((A/'COSMOLOGY_PUBLICATION_SOURCE_CHECK_01.json').read_bytes())
    for row in publication['sourceBindings']:
        assert bind(G/row['path']) == {k: row[k] for k in ['path','bytes','sha256']}
        names.add(row['path'])
    additional = [
        'docs/mechanics/AUTHOR_REVIEW_QUEUE.md', 'docs/mechanics/UMBRIN_LORE.md',
        'src/data/CONTINUITY_GLOSSARY.md',
        'DescentReviewChanges/ReviewBible/docs/mechanics/UMBRIN_LORE.md',
        'DescentReviewChanges/ReviewBible/src/data/CONTINUITY_GLOSSARY.md',
        'DescentReviewChanges/ReviewBible/src/data/oracle-mysteries.js',
        'DescentReviewChanges/ReviewBible/src/data/paladin-oaths.js',
        'DescentReviewChanges/ReviewBible/src/data/canon-classes.js',
        'DescentReviewChanges/ReviewBible/src/data/class-details.js',
        'DescentReviewChanges/ReviewBible/src/data/class-paths.js',
        'DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Bard_Playtest_v0_1.json',
        'DescentReviewChanges/ReviewBible/data/director/cosmology/creation_origins_reviewed_01.json',
        'DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CREATION_ORIGINS_REVIEWED_01.md',
    ]
    names.update(additional)
    names.update(p.relative_to(G).as_posix() for p in (R/'data/public/class_playtests').glob('*.json'))
    source_bindings = []
    for name in sorted(names):
        src = G/name
        assert src.is_file(), name
        raw = src.read_bytes()
        write(P/'sources'/name, raw)
        source_bindings.append(bind(src))
    write(P/'SOURCE_HASHES.json', jraw({r['path']: r['sha256'] for r in source_bindings}))
    write(P/'SOURCE_BINDINGS.json', jraw(source_bindings))
    for name in ['DOCX_PASSAGE_INDEX.json']:
        write(P/name, (A/'cosmology-source-authority-01'/name).read_bytes())
    write(P/'EXACT_PUBLICATION_PASSAGES.json', (A/'cosmology-publication-source-check-01/EXACT_PUBLICATION_PASSAGES.json').read_bytes())
    for folder in ['cosmology-source-authority-01-received','cosmology-creation-origin-01-received']:
        for src in sorted((A/folder).iterdir()):
            if src.is_file():
                write(P/'prior-verdicts'/folder/src.name, src.read_bytes())
    for name in ['COSMOLOGY_PUBLICATION_SOURCE_CHECK_01.json','COSMOLOGY_CREATION_ORIGIN_01_APPLICATION_CHECK.json']:
        write(P/'prior-evidence'/name, (A/name).read_bytes())
    write(P/'LATEST_PUSH_RECEIPT.json', (G/'docs/audit/2026-10-15/github-snapshot-cosmology/PUSH_RECEIPT.json').read_bytes())
    docs = json.loads((P/'DOCX_PASSAGE_INDEX.json').read_bytes())['documents']
    pub = json.loads((P/'EXACT_PUBLICATION_PASSAGES.json').read_bytes())['playerAppendixB']
    def refs(doc, indices):
        rows = pub['paragraphs'] if doc == 'PLAYER' else docs[doc]
        result = []
        for index in indices:
            row = next(r for r in rows if r['part']=='word/document.xml' and r['paragraphIndexZeroBased']==index)
            result.append({'source': pub['source'] if doc=='PLAYER' else doc, **row})
        return result
    COS = 'The Cosmology of Decennium Descent.docx'
    WORLD = 'The_World_of_Aethel_Lore.docx'
    choir = [('Korvelan','Courage'),('Vaerilune','Balance'),('Delvaran','Law'),('Shaelara','Sorrow'),('Xalarex','Pattern'),('Thalirion','Contradiction'),('Virellian','Passage/Transition')]
    mask_paras = [10021,10022,10023,10024,10025,10028,10029,10030,10031,10032,10035,10036,10037,10038,10039]
    rows = [
        {'id':'GP-01','topic':'Seven Choir identities and their authority','evidence':refs(COS,[78,103])+refs('PLAYER',[9977]),'textSources':['docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md Q5','docs/mechanics/APPENDIX_B_FOLK_RELIGION.md sections 2,3,5'],'finding':'Q5 locks exactly seven. The longer implementation brief explicitly maps the seven names/virtues to the original cosmology, and the current player opening names the same seven. Individual names are source-derived, not a verbatim owner list. No general cosmology domain is registered.','proposal':'Use the seven as a source-supported provisional identity table, keeping the exact owner count distinct from derived identity evidence. Do not add Asmodeus as an eighth because of the missing-voice metaphor in P78; do not replace this Choir with archons or ascendants.','question':'Confirm the precise authority/status label for these seven identities and whether further owner authority is needed before a bounded companion can use them.'},
        {'id':'GP-02','topic':'Fifteenfold worship masks','evidence':refs('PLAYER',[9977,9983,10018,10041,10289,10293]),'textSources':['docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md Q5','both APPENDIX_B_FOLK_RELIGION.md counterparts'],'finding':'The current book preserves fifteen named worship masks and cultural/ascended traditions under an explicit mortal-theology scope.','proposal':'Preserve all fifteen names and taught domains as mortal faith. Do not map them one-for-one to the seven Choir, Old Ones, custodians or legacy World gods. Real devotion or class effects do not prove a literal creator genealogy.','question':'Approve/correct the proposed worship inventory and state what can be taught publicly without revealing the secret hierarchy.'},
        {'id':'GP-03','topic':'Archons, aspirants and awakening are not automatic Choir additions','evidence':refs(COS,[104,106,108,109,110,116,122,124]),'finding':'The chapter distinguishes seven named archon witnesses from seven Thrones and mortal aspirants. Ko Thren, Velin Saal and Arak do not ascend in these passages; Serit blooms as a first Verdant Line possibility; the chapter finale crowns no individual. Later chapters must be checked before final identity status.','proposal':'Keep entities distinct and document the timeline qualifier. Do not automatically turn a Throne, a class title, a potential pantheon or a witness into a new Choir member.','question':'Read all later divine material and provide exact later updates if any. Keep event chronology and ascension mechanics separately open.'},
        {'id':'GP-04','topic':'Infernal roster duplication','evidence':refs(COS,[56,79,111,120,121]),'finding':'P56 puts Mephistopheles in both Maladomini and Cania. P79 and P111 repeat his name within roster-like sequences; P120-121 explicitly associate him with Cania. The scoped search of ReviewBible docs, src/data and data located no independent repair authority beyond original/runtime copies and the prior review.','proposal':'Retain both source claims and flag the disputed Maladomini occupancy. Cania is explicitly attested, but do not choose a replacement ruler, invent dual rule or import another game\'s roster.','question':'Identify all later corroboration/contradictions and the narrowest playable presentation that does not pretend the absent answer is settled.'},
        {'id':'GP-05','topic':'Current public terminology and infernal conflict','evidence':refs('PLAYER',[10319,10322,10323,10325,10327])+refs(COS,[56,58,77,78,79,81]),'finding':'The living player book uses War of Chains and Teeth and Nine Infernal Courts. Older prose/briefs use Blood War and Nine Hells. Current public text keeps rival priestly interpretations of the Pact.','proposal':'Use current public labels in new player prose, retaining older labels as source terminology. Treat theological disagreement as such. P10327\'s absolute-peace rumor cannot become a treaty/ceasefire catastrophe rule under the accepted origin conference.','question':'Confirm audience/status handling and flag any load-bearing sequence conflict without making the player account an omniscient disclosure.'},
        {'id':'GP-06','topic':'World of Aethel legacy named gods','evidence':refs(WORLD,[1,5,7,11,13,17,18,19,25,26,27,28,29,34,43,45,46,54,56,57,62,63,64,70,71,73,74,75,86]),'textSources':['docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md Q7'],'finding':'Q7 retires conflicting older god-as-combat/gate uses and preserves myth-history. The surviving World text has an explicit missing I-VI placeholder; Draethon appears in a song even though not individually named in the Q7 retirement list.','proposal':'Retain the full surviving legacy roster as historical source evidence. Do not promote it into an active pantheon, silently rename it to match the Choir/Fifteen, delete its stories, or infer the missing sections.','question':'Classify each legacy use precisely; preserve Q7\'s scope rather than treating it as blanket erasure of every name or story.'},
        {'id':'GP-07','topic':'Umbrin lore and Lumina/Umbra wording','evidence':refs('PLAYER',[9983,10018]),'textSources':['docs/mechanics/AUTHOR_REVIEW_QUEUE.md section 1','docs/mechanics/UMBRIN_LORE.md','DescentReviewChanges/ReviewBible/docs/mechanics/UMBRIN_LORE.md','both src/data/CONTINUITY_GLOSSARY.md counterparts','docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md Q5'],'finding':'The recorded Umbrin exile/Obsidian Burn decision is lore canon, while its explanations and glossary say primordial Umbra/Lumina. Q5 explicitly makes the Appendix B pair theological abstractions. Same-date summaries and historical draft flags do not establish a new primordial person or erase the exile ruling.','proposal':'Preserve locked exile, names, geography and cult beliefs; qualify cosmological personification as belief rather than proof of creator-beings. Keep any truly irreconcilable owner-level fact open instead of silently deciding it.','question':'Can the proposed Umbrin paragraph reconcile these sources without changing a locked fact? If not, identify the exact owner question and why existing authority cannot answer it.'},
        {'id':'GP-08','topic':'Class patron names and mechanical grants','textSources':['DescentReviewChanges/ReviewBible/src/data/oracle-mysteries.js','DescentReviewChanges/ReviewBible/src/data/CONTINUITY_GLOSSARY.md','DescentReviewChanges/ReviewBible/data/public/class_playtests/','DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Bard_Playtest_v0_1.json'],'finding':'Oracle source patrons include Echo Court, War Chorus, Pale Ledger, Shattered Seal, Veiled Threshold, Crown of First Flame, Verdant Resonance, Hush Beneath the Song, Celestial Concord and Turning Spiral. A patron description or class feature is not by itself evidence that it is a First Choir member, Old One, imprisoned Old God or the Marquis.','proposal':'Preserve named patron identities as source-bound class references with their existing draft/approval status; do not infer cosmological equivalence or new spell grants. Record any public-source revelation risk separately from proof of an actual deployed leak.','question':'Identify exact identity assertions or disclosure conflicts requiring later divine-power/public-packaging review. This conference does not reapprove class mechanics or promote existing draft flags.'},
        {'id':'GP-09','topic':'Folk ascendants, courts and deeper divine hierarchy','evidence':refs('PLAYER',[10289,10295,10299,10309,10312,10313,10314,10315,10331,10343,10355,10363,10367,10395,10407,10614]),'finding':'The public appendix uses strong encyclopedia-style claims about ascendants, courts, divine intervention and a Void Sovereign, inside a mortal-theology disclaimer. The deeper identity of these figures is not established by that voice.','proposal':'Keep named traditions and institutional beliefs usable without declaring a literal identity map. Do not equate the Void Sovereign, Voidus, Old God, Ul\'nak or Hush from superficial similarity. Defer actual planar jurisdiction, death routes, chronology and class-power rules to their ordered reviews.','question':'Provide a source-linked fact/belief/revelation split and a list of unresolved identity dependencies, noting any exact existing authority that actually resolves one.'},
    ]
    summaries = {
        'publicFaith':'Across Aethel, the Fifteenfold Pantheon gives everyday worship familiar names, stories and traditions. These are mortal interpretations of forces whose full nature remains uncertain. Scholars also distinguish the First Choir: seven named virtues associated with the Spiral. The Choir is not another name for the Fifteen. Calan\'thir and Asmodeus are widely credited as the genuine joint builders of the Crucible. A character may sincerely follow a temple, local tradition or philosophy without possessing the setting\'s hidden cosmology.',
        'directorIdentityBoundary':'Keep the owner-locked hierarchy as a distinction between cosmic structure, hidden machinery, custodians and mortal religion, not a new power-ranking or combat system. Exactly seven First Choir members remain separate from the seven named archon witnesses, Throne aspirants, cultural gods, folk ascendants and Oracle patron titles. Do not supply one-to-one equivalences that the sources do not establish. The prior creation/origin review and its unresolved causal and chronological dependencies remain controlling within their scope.',
        'umbrinWording':'The Obsidian Burn and the exile of Umbrin forebears by Calan\'thir and the First Choir remain recorded lore canon. Umbrin are mortals of The Murk, and their name and cult traditions invoke Umbra. Descriptions of Umbra\'s depth or Lumina\'s glare in those traditions do not independently establish two literal creator-beings. Preserve the named people, places and historical ruling while identifying that theological language as interpretation; do not turn a cult\'s account into a new cosmic identity claim.',
        'infernalRosterPolicy':'The original cosmology associates Mephistopheles with Cania and also assigns him Maladomini in a duplicated roster. Preserve both claims as source evidence. Use the attested Cania association with its source label, and leave Maladomini\'s occupancy disputed until supported by an explicit decision. Do not fill the position from an outside setting or invent a dual-rulership explanation. New public prose uses the current book\'s Nine Infernal Courts and War of Chains and Teeth terminology.'
    }
    comparison = {'reviewId':RID,'status':'proposed-for-actual-GPT-review-not-adopted','scope':'Gods/pantheons identities, authority and audience boundaries; not full cosmology closure.','rows':rows,'proposedSummaries':summaries,'proposedInventory':{'firstChoir':[{'name':n,'virtue':v,'status':'source-derived identity; count owner-locked; review pending'} for n,v in choir], 'fifteenfold':refs('PLAYER',mask_paras),'archonWitnessNames':['Myrriel','Valcendyr','Seraphon','Thalxior','Elarin','Quorilith','Shaenira'],'archonWitnessScope':'P106 list only, not an asserted complete universal archon catalog or a second First Choir.','folkAscendantExamples':['Herolux the Brave','Mystara the Archmage','Thorm Ironheart','The Green Mother'],'survivingWorldNamedGodReferences':['Velkyrion','Zeharra','Kharix','Myressa','Elyria','Yshael','Sythrel','Threxian','Naegul','Draethon']},'sourceInformationDeleted':0,'fullCosmologyApproved':False,'ownerChoiceAskedNow':False}
    write(P/'PROPOSED_COMPARISON.json',jraw(comparison))
    coverage = {'reviewId':RID,'type':'local-semantic-coverage-before-submission','originalCosmology':{'newCompleteMainDocumentParagraphRanges':[[56,124]],'priorConferenceCompleteRange':[0,59],'laterParagraphs125to337':'Included completely in full DOCX and passage index; keyword inventory inspected locally, full semantic reading still pending. GPT asked to review complete later divine material and report precise coverage.'},'matrix':{'completeMainDocumentParagraphRange':[0,363],'scope':'Text-run prose read across prior and current conferences; full original DOCX preserved. Math extraction is incomplete and no equation correctness or rendered-layout certification is claimed.'},'world':{'completeMainDocumentParagraphRange':[0,93],'missingSections':'I-VI explicitly absent; not reconstructed.'},'playerAppendixB':{'completeReadRanges':[[9976,10119],[10285,10416],[10604,10627]],'fullExtractIncludedRange':[9976,10678],'otherParagraphs':'Headings inventoried, not yet semantically read in this pass.'},'textDocumentsRead':['OWNER_COSMOLOGY_LOCKS_2026-07-30.md','both APPENDIX_B_FOLK_RELIGION.md counterparts','main UMBRIN_LORE.md','AUTHOR_REVIEW_QUEUE.md','main CONTINUITY_GLOSSARY.md cosmology section'], 'classScope':'Exact named-reference discovery and relevant metadata, not complete class semantic review or mechanics approval. Full current class files provided as context.', 'previousGoalTurnClassification':'progress: new backup pushed and remote commit verified', 'sourceInformationDeleted':0}
    write(P/'LOCAL_SEMANTIC_COVERAGE.json',jraw(coverage))
    # Name inventory is discovery evidence only; it is deliberately not a semantic-completion claim.
    classes = [G/n for n in sorted(names) if '/data/public/class_playtests/' in n or n.endswith('Decennium_Descent_Bard_Playtest_v0_1.json')]
    matcher = re.compile(r"\b(?:Calan.thir|Asmodeus|First Choir|Fifteenfold|Lumina|Umbra|Zeharra|Velkyrion|Myressa|Kharix|Mephistopheles|Echo Court|Turning Spiral|Hush Beneath the Song)\b",re.I)
    hits = []
    def walk(value, path, file):
        if isinstance(value,dict):
            for k,v in value.items(): walk(v,path+'.'+k,file)
        elif isinstance(value,list):
            for i,v in enumerate(value): walk(v,f'{path}[{i}]',file)
        elif isinstance(value,str) and matcher.search(value):
            hits.append({'source':file,'jsonPath':path,'text':value,'textSha256':sha(value.encode())})
    for src in classes:
        walk(json.loads(src.read_bytes()),'$',src.relative_to(G).as_posix())
    write(P/'CLASS_IDENTITY_DISCOVERY.json',jraw({'scope':'Literal name screening only; a non-match does not prove absence of other identity claims.','sourceFiles':len(classes),'hits':hits}))
    request = f'''COSMOLOGY-GODS-PANTHEONS-01 — next careful cosmology conference.

The owner requested and Codex verified another progress backup on main: dff2089b873a22d21b192f7c2d4a40e11f83c059. This is not whole-game approval. Both earlier cosmology reviews and your exact four creation/origin summaries are recorded. Original source files remain unchanged.

Read this complete packet as source evidence. PROPOSED_COMPARISON.json contains nine questions GP-01 through GP-09, four draft summaries and provisional identity inventories. Please accept, correct or defer each row, and return exact replacement wording wherever needed. Nothing in the comparison has been adopted merely by being prepared.

Your requested sources are included: all original cosmology/Matrix/World documents and complete paragraph index; both current Appendix B briefs and owner locks; exact current player-book and Director-book bytes plus complete Appendix B extracted paragraphs; both manifests; Umbrin lore/owner-review records/glossaries; class reference sources and all seventeen authored class candidates. The registered domains do not independently own a general pantheon domain. Do not infer such authority from class-identity registration. Full prior review returns and the latest push receipt are included.

For this review please read the complete post-P59 cosmology divine material, the later Matrix divine material, the current religion/pantheon text, and the complete supplied identity/authority sources. In particular inspect later chapter updates to gods, archons, ascendants and infernal identities rather than stopping at chapter VI. LOCAL_SEMANTIC_COVERAGE.json explicitly distinguishes what Codex has read from what is merely packaged. Report your own actual semantic coverage precisely; do not treat file inclusion, headings or term search as full reading. If a source is inaccessible or a coverage block remains, state the exact block and leave that portion open.

Pay special attention to the repeated Mephistopheles/Maladomini/Cania roster; whether the seven names/virtues are source-supported without falsely calling the list a verbatim owner decision; the difference between archons, First Choir, seven Thrones and mortal aspirants; Q7's precise legacy-name scope; and the Umbrin owner lore versus theological-abstraction wording. Keep real faith/class effects separate from an omniscient identity proof. Keep the public Nine Infernal Courts / War of Chains and Teeth labels. Do not fill missing World I-VI, merge Old God/Old Ones/Ul'nak/Void Sovereign/patron titles, import another setting's infernal roster, change mechanics, promote draft class flags, delete sources or certify full cosmology/public export/whole game.

Return a downloadable ZIP named COSMOLOGY_GODS_PANTHEONS_01_Addendum_and_Evidence.zip containing COSMOLOGY_GODS_PANTHEONS_01_REGISTER.json (row dispositions, exact reviewed summaries, reviewed identity inventory, fact/belief/revelation classification, unresolved dependencies and any specifically necessary owner decisions), COSMOLOGY_GODS_PANTHEONS_01_VERDICT.md, SOURCE_HASHES.json, SEMANTIC_COVERAGE.json and EVIDENCE_MANIFEST.json with SHA-256/byte lengths. Bind every decision to exact source path and paragraph/section/JSON location. Use this packet's source paths/hashes rather than unbound notebook memory. Preserve open issues, and distinguish the current bounded review from the remaining ordered planes, souls/death/resurrection, history, divine powers and campaign-revelation reviews.
'''
    write(P/'REQUEST.txt',request.encode())
    write(P/Path(__file__).name,Path(__file__).read_bytes())
    payloads = []
    for src in sorted(P.rglob('*')):
        if src.is_file():
            raw = src.read_bytes()
            payloads.append({'path':src.relative_to(P).as_posix(),'bytes':len(raw),'sha256':sha(raw)})
    write(P/'PACKAGE_MANIFEST.json',jraw({'reviewId':RID,'createdAtUtc':datetime.now(timezone.utc).isoformat(),'payloads':payloads,'sourceFiles':len(source_bindings),'noOriginalSourcesModified':True,'sourceInformationDeleted':0}))
    with zipfile.ZipFile(ZIP,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for src in sorted(P.rglob('*')):
            if src.is_file(): z.writestr(src.relative_to(P).as_posix(),src.read_bytes())
    for row in source_bindings:
        assert bind(G/row['path'])==row
        assert sha((P/'sources'/row['path']).read_bytes())==row['sha256']
    with zipfile.ZipFile(ZIP) as z:
        assert z.testzip() is None
        for row in payloads:
            assert sha(z.read(row['path']))==row['sha256']
    report={'reviewId':RID,'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'prepared-not-sent','package':bind(ZIP),'packetDirectory':P.relative_to(G).as_posix(),'sourceFiles':len(source_bindings),'payloadsBeforeManifest':len(payloads),'proposalRows':len(rows),'proposedSummaries':len(summaries),'classLiteralIdentityHits':len(hits),'sourceInformationDeleted':0,'originalSourcesUnchanged':True,'fullCosmologyApproved':False,'weeklyUsageLastObservedUsedPercent':19,'ownerStopAtUsedPercent':50}
    write(REPORT,jraw(report))
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':
    main()
