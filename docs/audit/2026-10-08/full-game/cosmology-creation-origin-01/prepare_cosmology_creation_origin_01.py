"""Freeze a source-linked creation/origin comparison; no doctrine promotion."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, zipfile
from apply_di7_ap_as_01 import G, A, info, encoded

def main():
    root = A/'cosmology-creation-origin-01'
    archive = A/'DD_Cosmology_Creation_Origin_01.zip'
    preparation = A/'COSMOLOGY_CREATION_ORIGIN_01_PREPARATION.json'
    assert not root.exists() and not archive.exists() and not preparation.exists()
    first = A/'cosmology-source-authority-01'
    received = A/'cosmology-source-authority-01-received'
    hashes = json.loads((received/'SOURCE_HASHES.json').read_bytes())
    index = json.loads((first/'DOCX_PASSAGE_INDEX.json').read_bytes())
    origin = 'The Cosmology of Decennium Descent.docx'
    matrix = 'The Decennium Descent and the Matrix of Oblivion.docx'
    world = 'The_World_of_Aethel_Lore.docx'
    lock = 'docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md'
    silent = 'docs/mechanics/SILENT_ONES_CANON.md'
    def p(name, start, end):
        rows = [x for x in index['documents'][name] if x['part']=='word/document.xml' and start <= x['paragraphIndexZeroBased'] <= end]
        assert len(rows) == end-start+1
        return {'path':name,'part':'word/document.xml','paragraphsInclusive':[start,end],'fullParagraphHashes':[x['textSha256'] for x in rows]}
    def source(name, section): return {'path':name,'section':section,'fileSha256':hashes[name]}
    proposals = [
        {'id':'COR-01','topic':'Heartcell versus Crucible authorship','question':'How should the original First Seal / dungeon creation passages be read after owner Q3, without calling the public builders frauds or making them inventors of the underlying Heartcell?',
         'proposedDisposition':'Owner Q3 controls the two true layers. Preserve original creation prose as source evidence; any current synthesis must explicitly bound public Crucible authorship versus pre-existing Heartcell machinery. Do not silently label all original source words as lies or erase their older cosmological register.',
         'support':[p(origin,14,19),p(matrix,36,50),source(lock,'Q3'),source(silent,'1a. Authorship')]},
        {'id':'COR-02','topic':'Origins of Lumina/Umbra and authority of metaphor','question':'Which original claims are compatible metaphors or source proposals, and which would improperly literalize Lumina/Umbra as independently existing primordial beings?',
         'proposedDisposition':'Apply Q5 and COS-A04: theological abstractions are not literal primordial beings. Preserve original P4 contrary-gesture language and Matrix P12 as source wording; do not promote unowned original origin details merely because they appear compatible.',
         'support':[p(origin,1,12),p(matrix,10,15),source(lock,'Q5')]},
        {'id':'COR-03','topic':'The Sundering event and chronology','question':'The original cosmology emphasizes Asmodeus against Calan’thir/Choir, followed by Ul’nak’s emergence; Matrix P23–34 emphasizes the Old Ones imposing equality and a twenty-cycle Sundering. Can existing evidence establish their exact relationship, or must chronology remain unresolved?',
         'proposedDisposition':'Preserve both accounts. Do not invent two separately dated wars, a precise event mapping, or an opening-cycle conversion for twenty cosmic cycles. Separate compatible shared stakes from missing event-order evidence.',
         'support':[p(origin,31,39),p(origin,41,53),p(matrix,22,34)]},
        {'id':'COR-04','topic':'First Seal, Divine Pact and later public Crucible','question':'Distinguish First Seal, Divine Pact, binding, governing and activation without asserting an unsupported single event or separate events.',
         'proposedDisposition':'The Pact is the Divine Pact per Q2; its custodianship of the Heartcell is controlled by Q3. Exact identity/chronology of every original use of seal/compact/Pact remains a source-comparison question, not a new fact.',
         'support':[p(origin,15,18),p(origin,54,59),p(matrix,36,50),source(lock,'Q2–Q3')]},
        {'id':'COR-05','topic':'Old Ones origin, motive and their own machinery','question':'Compare Great Stillness / collective dreaming, the Matrix elimination-of-difference rationale, and owner-locked builders using loot to seek discovery/release. What is established, and what exact provenance or construction motive is not supplied?',
         'proposedDisposition':'Silent Ones=Old Ones and their Heartcell authorship/loot intent remain locked. Their mechanism being repurposed by the Pact is established. Do not invent an explanation for how or why their original machine became their prison, a benevolent predecessor identity, or a warden/prisoner subgroup split.',
         'support':[p(origin,13,17),p(matrix,15,20),p(matrix,39,50),source(lock,'Q1/Q3'),source(silent,'1. Owner statements; 1a. Authorship')]},
        {'id':'COR-06','topic':'First Choir emergence and exact seven','question':'Separate the locked count and named virtues from the original emergence chronology, and identify whether Matrix awakening during the Sundering actually conflicts with the longer account.',
         'proposedDisposition':'Keep exactly seven and the distinct First Choir, never a fifteen-god substitution. Treat precise maturation/awakening timing as a passage comparison; no new member, forced identity or chronology is introduced.',
         'support':[p(origin,25,35),p(origin,50,58),p(matrix,27,31),source(lock,'Q5'),source('docs/mechanics/APPENDIX_B_FOLK_RELIGION.md','2–3. First Choir')]},
        {'id':'COR-07','topic':'Public explanation and revelation boundaries','question':'Can the proposed public and Director summaries below be used without revealing the Heartcell in public origin material or weakening the public builders into a fraud?',
         'proposedDisposition':'Use the four-stage revelation ladder. Public roleplay starts from the genuine joint Crucible creation tradition; deep machinery, Silent Ones identity, bait intent and full Matrix remain gated. Historical summaries using “public resonance valve” do not automatically authorize a complete player-facing mechanism.',
         'support':[source(lock,'Q3 player knowledge'),source(silent,'1a. Player revelation path; 3. Layer model'),source('DescentReviewChanges/ReviewBible/docs/canon/PLAYER_DIRECTOR_BOUNDARY.md','Safe Player-Facing Truth; Director-Only Truth; Revelation Ladder')]},
        {'id':'COR-08','topic':'Peace, conflict and meaningful difference','question':'Does the proposed summary preserve the distinction between absolute ontological stillness and ordinary political peace, without converting cosmic prose into a measurable mechanic?',
         'proposedDisposition':'A treaty or ceasefire is not the defined catastrophe. Meaningful difference, choice and continued possibility are the stated issue; neither endless war as a moral good nor a numeric resonance threshold is adopted. An operational threshold remains conditional future owner work.',
         'support':[p(matrix,2,8),p(matrix,16,20),p(origin,45,49),source('DescentReviewChanges/ReviewBible/docs/canon/CANON_CORE.md','Why the Dungeon Exists; Guardrails')]},
        {'id':'COR-09','topic':'Adjacent material that must not be silently resolved','question':'Identify adjacent dependencies raised by this origin pass, preserving later phases for gods/planes/history/revelations.',
         'proposedDisposition':'Do not resolve infernal lord rosters, plane ontology, Shardspire origins, World I–VI gaps, or Old God/Binding/Interstice identity while reviewing origin. P56 names Mephistopheles in two realms; flag this for the god/plane pass without choosing a replacement.',
         'support':[p(origin,55,59),p(world,0,13),source('docs/mechanics/LEVEL_97_OLD_GOD_Q6_OPEN.md','Open identity links / guardrails'),source('docs/playtest/DUNGEON_CREATION_PURPOSE.md','3. Explicit gaps')]}
    ]
    summaries = {
        'status':'proposed scoped editorial summaries for joint review; not adopted canon or public export',
        'public':'The accepted tradition credits Calan’thir and Asmodeus with jointly creating the Crucible as a proving ground and a monument of Order and Hell working together. Cultures dispute their shares of the credit. Adventurers enter a dungeon that has shaped Aethel’s fortunes, beliefs and conflicts over generations.',
        'director':'Calan’thir and Asmodeus genuinely built the known Crucible around machinery they did not invent. The Silent Ones—also called the Old Ones—built the older Heartcell, including the hundred-floor resonance structure, ten Gate divisions, opening cycle and reward architecture. Its creators used loot to invite discovery and release. The Divine Pact’s custodians discovered, modified, activated and bound themselves to that machinery; expeditions and their continuing consequences feed its operation. The complete account is discoverable through the owner’s revelation ladder and is never ordinary world knowledge.',
        'originScope':'The surviving original books contain accounts of Great Stillness, contrary gestures, the Weave, Spiral, seals, the Sundering and the Pact. Their preservation does not make every passage authoritative. Use the registered domains and recorded owner decisions for the questions they actually settle; retain unresolved event relations rather than inventing a unified chronology.',
        'peaceScope':'Ordinary political peace is not absolute ontological stillness. The threatened loss is meaningful difference, possibility and agency. No measurable awakening threshold is established by this comparison.'
    }
    local_coverage = {'scope':'Semantic reading performed for this comparison, distinct from hash verification.', 'completePassageRanges':[p(origin,0,59),p(matrix,0,55),p(world,0,18)], 'completeDocumentsRead':[lock,silent,'DescentReviewChanges/ReviewBible/docs/canon/CANON_CORE.md','DescentReviewChanges/ReviewBible/docs/canon/PLAYER_DIRECTOR_BOUNDARY.md','docs/mechanics/APPENDIX_B_FOLK_RELIGION.md'], 'notCompleted':['Remaining original Cosmology chapters','Complete current player and Director books','Full historical chronology','All god/plane/soul/class/revelation dependencies'], 'outsidePacketNotebookSource':'The first reviewer mentioned The_Directors_Crucible.docx. Its exact notebook source bytes remain unbound here; do not treat a similarly titled local file as proven identical.'}
    request = '''COSMOLOGY-CREATION-ORIGIN-01 — next ordered comparison after the preserved COSMOLOGY-SOURCE-AUTHORITY-01 verdict.

The owner requested another progress backup: main 80944e024b1dba5b1f31707b4dd951d53d9f74c8 is now pushed and remotely verified. This is still not whole-game approval. The 34 cosmology sources remain byte-identical to your first packet and its earlier a3f75a0 baseline; no doctrine has changed. Your authority verdict and all four manifest-bound evidence files were downloaded and preserved, with all 34 current/frozen source hashes matching.

Please perform the creation/origin comparison you ordered. Read the complete Cosmology DOCX P0–59 and Matrix P0–55, the relevant surviving World passages and recorded Q1/Q2/Q3/Q5 locks. Full original files and paragraph index are included, so truncated summaries need not stand in for source prose. Compare all nine COR rows and review each proposed public/Director/origin/peace summary. Separate existing owner decisions, compatible source interpretation, real contradictions, audience differences, unresolved provenance, and genuinely new proposals.

Pay particular attention to: genuine public Crucible builders versus older Silent Ones Heartcell; original First Seal/Pact descriptions versus Q3; the two Sundering narratives and the undefined meaning of twenty cosmic cycles; Old Ones motive versus their own machinery; seven Choir emergence; and public/revelation boundaries. Do not invent a repaired chronology or motives to make the books agree. No wholesale rewrite, general-cosmology authority promotion, identity merge, deletion, or public export is requested.

For every COR row return a source-bound disposition and exact supporting file/paragraph or section references. If a summary needs correction, return exact replacement wording separately for review and explain its authority and consequences. Provide a fact/belief/revelation table that can serve the authored campaign candidate, an unresolved-dependency register, and precise semantic coverage. Identify which next gods/pantheons comparisons need additional source files. A missing connection is not an invitation to improvise a new fact.

Two receipt details: your previous COS-A06 Boolean ownerChoiceRequiredNow=true is qualified by its own text “only if/when mechanics require it”; we have not asked the owner a redundant question. The register’s text fields carrying whole-paragraph hashes sometimes paraphrase the original; we preserve them verbatim but do not call them exact full-paragraph quotations. Keep verbatim quotation distinct from your interpretation in this response. The outside-packet Directors Crucible source was reviewer-reported and is not independently file-bound; identify its exact source/version/hash if relying on it.

Return downloadable JSON/Markdown plus an evidence manifest. This conference is creation/origin only; gods/planes/souls/history/divine powers/revelations and complete cosmology acceptance remain later work.
'''
    payloads = {}
    for name, sha in hashes.items():
        raw = (G/name).read_bytes(); assert hashlib.sha256(raw).hexdigest()==sha
        payloads['sources/'+name] = raw
    payloads['DOCX_PASSAGE_INDEX.json']=(first/'DOCX_PASSAGE_INDEX.json').read_bytes()
    payloads['SOURCE_HASHES.json']=(received/'SOURCE_HASHES.json').read_bytes()
    for name in ['COSMOLOGY_SOURCE_AUTHORITY_01_REGISTER.json','COSMOLOGY_SOURCE_AUTHORITY_01_VERDICT.md','SEMANTIC_COVERAGE.json','EVIDENCE_MANIFEST.json']:
        payloads['prior-verdict/'+name]=(received/name).read_bytes()
    payloads['PROPOSED_COMPARISON.json']=encoded({'reviewId':'COSMOLOGY-CREATION-ORIGIN-01','status':'prepared-for-review; no doctrine adopted','issues':proposals,'proposedSummaries':summaries})
    payloads['LOCAL_SEMANTIC_COVERAGE.json']=encoded(local_coverage)
    payloads['REQUEST.txt']=request.encode()
    payloads['LATEST_PUSH_RECEIPT.json']=(G/'docs/audit/2026-10-15/github-snapshot/PUSH_RECEIPT.json').read_bytes()
    payloads['prepare_cosmology_creation_origin_01.py']=Path(__file__).read_bytes()
    manifest={n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in payloads.items()}
    payloads['PACKAGE_MANIFEST.json']=encoded(manifest)
    root.mkdir()
    for name, raw in payloads.items():
        pth=root/name; pth.parent.mkdir(parents=True,exist_ok=True); pth.write_bytes(raw)
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for name,raw in payloads.items():z.writestr(name,raw)
    with zipfile.ZipFile(archive) as z:
        for name,row in manifest.items():
            raw=z.read(name); assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    preparation.write_bytes(encoded({'reviewId':'COSMOLOGY-CREATION-ORIGIN-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'prepared-not-sent','archive':info(archive),'manifest':info(root/'PACKAGE_MANIFEST.json'),'request':info(root/'REQUEST.txt'),'comparison':info(root/'PROPOSED_COMPARISON.json'),'localSemanticCoverage':info(root/'LOCAL_SEMANTIC_COVERAGE.json'),'currentSourceHashesVerified':len(hashes),'payloadsVerified':len(manifest),'comparisonRows':len(proposals),'sourceDoctrineChanges':0,'sourceInformationDeleted':0,'cosmologyCompleted':False}))
    print(json.dumps({'preparation':info(preparation),'archive':info(archive),'payloads':len(manifest),'comparisonRows':len(proposals)}))

if __name__ == '__main__': main()
