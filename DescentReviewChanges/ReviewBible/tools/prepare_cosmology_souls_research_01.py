"""Freeze the souls/Equation conference only after the planes return is verified."""
from datetime import datetime,timezone
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    root=A/'cosmology-souls-research-01';archive=A/'DD_Cosmology_Souls_Research_01.zip';receipt=A/'COSMOLOGY_SOULS_RESEARCH_01_PREPARATION.json'
    assert all(not p.exists() for p in [root,archive,receipt])
    planes=A/'COSMOLOGY_PLANES_01_APPLICATION_CHECK.json'
    assert planes.exists(),'Verify and apply the actual planes return before preparing this follow-on.'
    roots=[R/'data/director/cosmology'/n for n in ['souls_death_hunt_conference_draft_01.json','equation_library_source_inventory_01.json','equation_research_interface_draft_01.json','chronology_research_sites_draft_01.json']]
    readings=[A/n for n in ['COSMOLOGY_SOULS_DEATH_SOURCE_READING_01.json','COSMOLOGY_SOULS_DEATH_INTERFACE_READING_02.json','COSMOLOGY_SOULS_CONTRACT_READING_03.json','COSMOLOGY_TAINT_RESEARCH_SOURCE_READING_04.json']]
    sources={}
    def add(p):row=info(p);sources[row['path']]=row
    for p in roots+readings:
        add(p)
        for row in read(p).get('sourceBindings',[]):
            assert info(G/row['path'])==row,('Source changed since bounded reading',row['path'])
            add(G/row['path'])
    extras=[
        R/'docs/director-only/cosmology'/n for n in ['CURRENT_COSMOLOGY_READ_FIRST.md','SOULS_DEATH_HUNT_CONFERENCE_DRAFT_01.md','EQUATION_LIBRARY_SOURCE_INVENTORY_01.md','EQUATION_RESEARCH_INTERFACE_DRAFT_01.md','CHRONOLOGY_RESEARCH_SITES_DRAFT_01.md','HEARTCELL_OWNER_UPDATE_02.md','Q6_LATER_LOCK_REVIEWED_01.md','GODS_PANTHEONS_REVIEWED_01.md','PLANES_REVIEWED_01.md','EQUATION_OF_OBLIVION_NOTEBOOK_DRAFTS_01.md']
    ]+[
        R/'data/director/cosmology'/n for n in ['heartcell_owner_update_02.json','q6_later_lock_reviewed_01.json','gods_pantheons_reviewed_01.json','planes_reviewed_01.json','equation_of_oblivion_notebook_drafts_01.json']
    ]+[
        A/n for n in ['COSMOLOGY_SOULS_DEATH_AUTHORED_STATUS_CORRECTION_01.json','COSMOLOGY_SOULS_DEATH_HUNT_DRAFT_01_CITATION_CHECK.json','COSMOLOGY_EQUATION_LIBRARY_SOURCE_INVENTORY_01_CHECK.json','COSMOLOGY_EQUATION_RESEARCH_INTERFACE_DRAFT_01_CHECK.json','COSMOLOGY_CHRONOLOGY_RESEARCH_SITES_DRAFT_01_CHECK.json','ORIGINAL_COSMOLOGY_EPILOGUE_RULE_INVENTORY_01.json','HEARTCELL_OWNER_UPDATE_02_APPLICATION_CHECK.json','HEARTCELL_OWNER_UPDATE_02_RECEIVED_DECISION.json','COSMOLOGY_Q6_LATER_LOCK_01_APPLICATION_CHECK.json','LANGUAGE_EXACT_FULFILLMENT.json','CALIBRATION_REVIEW_PART_3_SUBMISSION_RECEIPT_01.json']
    ]+[planes,R/'data/public/spell_playtests/authored_review_index.json']
    for p in extras:add(p)
    for row in read(roots[2])['languageExactApprovalVerification']['currentFinalArtifactsMatched']:
        assert info(G/row['path'])==row;add(G/row['path'])
    bindings=list(sources.values());now=datetime.now(timezone.utc).isoformat()
    scope={'reviewId':'COSMOLOGY-SOULS-RESEARCH-01','recordedAtUtc':now,
        'primaryIssues':[{'id':x['id'],'title':x['title']} for p in [roots[0],roots[2]] for x in read(p)['sections']],
        'contextOnly':{'libraryRecords':22,'chronologyIssues':8,'existingEpilogueGroups':17},
        'currentContinuation':'Owner-created Part 3 is active. Old draft statements about awaiting Part 3 are historical creation-status text; no owner approval is pending.',
        'sourceAuthority':'Original manuscripts first with explicit owner corrections. Distinguish sourced facts, current operating rules, and newly recommended designs.',
        'unchangedBaseline':{'ordinarySpellsReviewed':419,'ordinarySpellsPending':429,'ordinarySpellTotal':848,'fullCosmologyApproved':False,'runtimeApproved':False,'humanPlaytestConfirmed':False},
        'sourceInformationDeleted':0}
    request='''COSMOLOGY-SOULS-RESEARCH-01 — concrete souls, Equation research, taint and Hunt discussion.

The owner asked Codex and this actual GPT notebook to develop every aspect of the game, using original lore first and preserving all information. The planes conference has now been verified locally; read its supplied current successor and application evidence. Part 3 is active. Some earlier draft status sentences say Part 3 was pending when they were created; CURRENT_REVIEW_CONTEXT.json supersedes those historical workflow sentences, not their source evidence.

Read the 12 SH sections and 20 situations in souls_death_hunt_conference_draft_01.json and its readable chapter, and the nine ER sections/14 situations in equation_research_interface_draft_01.json. Check their whole cited original paragraphs/cards and current operating procedures in the supplied actual source files. The four earlier bounded reading records are extraction aids; their older pending-only status is qualified by COSMOLOGY_SOULS_DEATH_AUTHORED_STATUS_CORRECTION_01.json. Soul Mirror is reviewed-authored in candidate_low_rank_136.json /spells/124, an ordinary reflecting ward, not soul custody. Ordinary spells remain 419 reviewed/429 pending of 848. Do not approve pending spells just by discussing them.

Preserve owner directions: primordial cycles are ages; original lore first; underlying Heartcell builder and the survivor/Old God/Ulnak/Interstice identities remain unresolved. Research across multiple Descent libraries can yield functional understanding and taint; voice/proximity taint independently starts on Descent level 5 and beyond. The more they know, the more corruption matters. Hunt-triggered death is normally final with extremely rare Divine/Abyssal intervention. Neither an absolute intervention ban nor an already-adopted seven-stage/numeric system follows. New Equation inscriptions are commissioned design drafts, not recovered missing math. Q6's Floor100 confrontation produces OR exposes a focusing crystal, and Floor97 has a distinct hidden chamber. No source proves this is the original Shard of Absolute Rest.

Please do more than restate missing decisions. For each SH and ER issue, identify the sourced boundary, critique the Codex proposal and recommend a concrete playable treatment wherever the owner direction permits it. Label every new threshold, duration, state transition, clue, cost or exception as NEW PROPOSED DESIGN. Separate your recommended candidate from the source record; Codex will inspect it before applying anything. If an essential choice truly requires the owner rather than routine design judgment, present the precise alternatives and practical consequences. Do not invent cosmological identities, lost manuscript content, actor names, a current epoch or source-established locations to close a design gap.

Priority decisions:
1. Research as an activity versus a new skill: the reviewed character foundation has 20 basic skills; Research is not one. The Core's Matrix research lead personally needs high ranks in Arcana, History, Religion, Nature and Engineering, but the selected sources do not operationalize high ranks. Recommend a compatibility interpretation, explain what it would change and provide a progression path; do not silently substitute team coverage for personal qualification.
2. Functional understanding: distinguish possession, copied symbols, literal translation, inferred meaning, demonstrated operational understanding, execution and enforcement. Propose what a player can demonstrate at the table without demanding real-world mathematics. Design graded, truthful clue feedback and forward progress on failed research while respecting actual language critical-failure rules. Recommend the amount/type of evidence required with clear provenance; no unearned complete formula from a name or copied diagram.
3. Existing language and class tools: preserve ordinary translation scaling, eight-hour/250-word decipher work, one qualified assistant +1, proficiency counted once, supported literal/encoded meaning, and information retained after temporary competence expires. Wizard Knowledge Transfer really grants a known spoken language or an existing proficient skill for one hour; it does not grant Expertise/memories/secrets. Decide explicitly whether/how that temporary real proficiency satisfies a proposed personal research gate across the work period. Oracle Tongues I gives its actual Lore/Insight bonus; Language Insight is a distinct tracked resource. One real work clock governs research, rest, travel and protection. Do not nullify useful tools merely because this puzzle is important.
4. Taint and pursuit: recommend how knowledge-based taint and level5+ proximity/voice exposure are recorded separately and combined if needed. Distinguish those causes from Unity, ordinary Corrupted, source Null Veil, generic curse and Forbidden Pact attention. A six-tick clock/DC12+tier from another system is not already an Equation rule. Preserve ordinary defenses/cures within their actual scope. Give an understandable warning/revelation progression and specify what actually initiates Hunt. Keep any numerical model visibly proposed, not owner-selected.
5. Death sequence: resolve real survival/prevention procedures before an actual death. Distinguish ordinary resurrection, free/willing-soul requirements, custody claims and the exceptional Hunt-death prohibition. Ordinary spell access does not automatically supply an extremely rare Divine/Abyssal exception. Recommend concrete exception criteria, cost/aftermath/consent and a persistent record without inventing which named being owns every soul. Separate retrieval of a corpse from custody or return of its soul. Existing soul capture/contract descriptions do not establish universal afterlife law.
6. Scope of copies/time: classify the actual reviewed/pending/unsupported effects, including Soul Mirror, Arcane Clone, Clone and Time Loop. Use actual text and decisions rather than labels; no automatic unsupported duplication or rewind escape, and no blanket cancellation of reviewed local effects.

Use the 22-record library inventory as the source constraint for route design: 22 records are not 22 established Descent libraries. Cantor's Archive is mapped to Floor47; Wax Library is an original chamber seed with no fixed floor. The chronology draft establishes its post-Infinite-Yield source frame AND original P324 permission for independent/multi-era adaptation. Neither automatic starting availability nor an absolute earlier-era ban is supported. Propose a feasible research-route structure with unassigned slots if needed; do not silently relocate the Unbound Academy, Citadel, Silent Library or cosmic archives into the Dungeon, merge Shifting Sigils with Sigil Navigators Library, or assign Equation fragments as recovered canon. A new location/fragment may be recommended as new design, with why it fits and what decision remains.

The chronology draft and existing17EPI groups are context for this review. Do not choose the whole campaign epoch, solve the conditional 87/710AE cadence tension, activate epilogue benefits or retime the Proof War here. Preserve original portability and current public failed-Sixth-Gate boundary. Separate player-facing signals from Director secrets.

Return one downloadable COSMOLOGY_SOULS_RESEARCH_01_Addendum_and_Evidence.zip with exactly:
REGISTER.json — all12 SH and9 ER dispositions with source facts, accepted/revised/rejected proposed interfaces, recommended new designs and unresolved dependencies;
DIRECTOR_COMPANION.md — a readable integrated chapter with distinct source/current-rule/proposed-rule labels and usable procedures;
RESEARCH_ROUTE_AND_STATE_MODEL.json — recommended evidence/qualification/research/taint/Hunt/death/intervention records and transitions, distinguishing established procedures from new proposals; library slots and provenance;
CASEBOOK.json — disposition all20 SH and14 ER supplied situations, adding explicit edge cases needed for your recommended designs; these are authored examples, not executed software or human playtests;
SOURCE_HASHES.json — exact uploaded paths/bytes/SHA256;
SEMANTIC_COVERAGE.json — whole passages/cards actually read, with precise citations and bounded reading claims;
VERDICT.md — what this review establishes, exact designs requiring follow-up and why, and what remains open;
EVIDENCE_MANIFEST.json — bytes/SHA256 of the other seven outputs.

Use repository-relative paths, zero-based all-w:p DOCX paragraph indices including blanks/tables, exact JSON pointers, or one-based text lines with faithful excerpts. Verify citations from source bytes; do not label paraphrases as verbatim. Hash agreement alone is not semantic review. Preserve all source information; no public export, pending spell promotion, implementation, human balance, whole-game approval or publication certification occurs by this conference.
'''
    root.mkdir();(root/'CURRENT_REVIEW_CONTEXT.json').write_bytes(encoded(scope));(root/'SOURCE_BINDINGS.json').write_bytes(encoded(bindings));(root/'REQUEST.txt').write_text(request,encoding='utf-8',newline='\n')
    for row in bindings:
        p=G/row['path'];dest=root/'sources'/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes());assert dest.read_bytes()==p.read_bytes()
    payloads=[{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(root.rglob('*')) if p.is_file()]
    (root/'PACKAGE_MANIFEST.json').write_bytes(encoded(payloads))
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    receipt.write_bytes(encoded({'reviewId':scope['reviewId'],'archive':info(archive),'sources':len(bindings),'payloads':len(payloads),'primaryIssues':21,'submitted':False,'sourceInformationDeleted':0}))
    print(json.dumps(read(receipt)))

if __name__=='__main__':main()
