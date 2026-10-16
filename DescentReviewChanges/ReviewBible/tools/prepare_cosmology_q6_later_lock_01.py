"""Prepare a focused, immutable source conference on the later Q6 locks."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p): return json.loads(p.read_bytes())


def main():
    root=A/'cosmology-q6-later-lock-01'
    archive=A/'DD_Cosmology_Q6_Later_Lock_01.zip'
    receipt=A/'COSMOLOGY_Q6_LATER_LOCK_01_PREPARATION.json'
    assert all(not p.exists() for p in [root,archive,receipt])
    source_paths=[
        G/'docs/canon/CANON_MANIFEST.json', R/'docs/canon/CANON_MANIFEST.json',
        G/'docs/mechanics/LEVEL_97_OLD_GOD_Q6_OPEN.md', R/'docs/mechanics/LEVEL_97_OLD_GOD_Q6_OPEN.md',
        R/'docs/director-only/continuity/LEVEL_97_OLD_GOD_Q6_OPEN.md',
        G/'docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md', R/'docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md',
        G/'docs/mechanics/SILENT_ONES_CANON.md', R/'docs/mechanics/WORLD_DUNGEON_LOOP.md',
        G/'docs/activity/2026-07-31.md',G/'docs/activity/2026-08-05.md',
        G/'docs/mechanics/F1_100_RULES_TRACK_2026-07-31.md',
        G/'docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack/Monster_Manual_of_the_Known_Descent_Source/CANON_BOUNDARY.md',
        R/'docs/director-only/continuity/OWNER_COSMOLOGY_LOCKS_2026-07-30.md',
        R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md',
        R/'docs/director-only/cosmology/OWNER_RECONCILIATION_REVIEWED_01.md',
        R/'data/director/cosmology/owner_reconciliation_reviewed_01.json',
        R/'data/director/cosmology/creation_origins_reviewed_01.json',
        R/'data/director/cosmology/gods_pantheons_reviewed_01.json',
        R/'docs/canon/CANON_CORE.md',
        A/'cosmology-source-authority-01-received/COSMOLOGY_SOURCE_AUTHORITY_01_REGISTER.json',
        A/'COSMOLOGY_DIRECTOR_INTERSTICE_SOURCE_CHECK_01.json',
        A/'COSMOLOGY_OWNER_RECONCILIATION_01_RECEIVED_DECISION.json',
        A/'COSMOLOGY_OWNER_RECONCILIATION_01_ADOPTION_CHECK.json',
        A/'COSMOLOGY_OWNER_SOURCE_PRIORITY_2026_10_15_CAPTURE.json',
        A/'COSMOLOGY_OWNER_CORRECTIONS_2026_10_15_MESSAGE_CAPTURE.json',
    ]
    source_paths.extend(G/x['path'] for x in read(A/'COSMOLOGY_DIRECTOR_INTERSTICE_SOURCE_CHECK_01.json')['sources'])
    assert len(set(source_paths))==len(source_paths)
    bindings=[info(p) for p in source_paths]
    manifest=read(source_paths[0]); domain=next(x for x in manifest['domains'] if x['domain']=='floor-97-old-god-endgame')
    assert domain['status']=='canonical' and domain['visibility']=='director'
    assert len({info(p)['sha256'] for p in source_paths[2:5]})==1
    excerpts=[]
    ranges={
        'docs/mechanics/LEVEL_97_OLD_GOD_Q6_OPEN.md':[(1,109)],
        'docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md':[(10,28),(205,215)],
        'docs/activity/2026-07-31.md':[(34,47)],
        'docs/activity/2026-08-05.md':[(44,52)],
        'docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack/Monster_Manual_of_the_Known_Descent_Source/CANON_BOUNDARY.md':[(1,26)]
    }
    for rel,spans in ranges.items():
        p=G/rel; lines=p.read_text(encoding='utf-8-sig').splitlines()
        for first,last in spans:
            assert last<=len(lines)
            excerpts.append({'source':info(p),'firstLineOneBased':first,'lastLineOneBased':last,'lines':[{'line':i+1,'text':lines[i]} for i in range(first-1,last)]})
    issues=[
        {'id':'Q6L-01','question':'Which source owns the current domain?', 'localReading':'CANON_MANIFEST floor-97-old-god-endgame explicitly registers the August 5 holding file as canonical Director authority. Its historical OPEN filename is not its current status.'},
        {'id':'Q6L-02','question':'What is settled about Floor 97?', 'localReading':'Regular zone plus distinct hidden chamber; July 31 whole-floor-hidden-zone shorthand was explicitly superseded. The later October devouring-to-one correction qualifies the plural sleepers language without supplying a new room map or named survivor.'},
        {'id':'Q6L-03','question':'What is the minimum authoritative crystal sequence?', 'localReading':'August 5 final known sequence -> Floor 100 confrontation produces OR exposes focusing crystal -> weakens/makes Old God vulnerable -> confrontation under those conditions. Do not narrow produces/exposes to a guaranteed loot drop or assume victory always required based on July 31 shorthand.'},
        {'id':'Q6L-04','question':'What remains unimplemented?', 'localReading':'Unprepared L30/mind-control/near-wipe is threat intent only. Full crystal handling, weaken procedure, Old God encounter statistics and Floor 97 room/encounter mapping remain open. No numerical invention or runtime promotion.'},
        {'id':'Q6L-05','question':'Which identities remain open?', 'localReading':'Old God, devouring survivor, Ul\'nak references, Binding shard and Interstice are not automatically merged. Keeping identity unresolved must not erase the recorded crystal path.'},
        {'id':'Q6L-06','question':'What is public versus Director-only?', 'localReading':'Public reliable achievement ends at failed Sixth Gate. No reliable Floor 97/100 route, crystal existence/function/acquisition or vulnerability procedure publicly. Binding/Interstice may be false scholarship, corrupted translation, incomplete ritual or historical design; not reliable public mechanics. Director text needs explicit reconciliation, not silent overwrite.'},
        {'id':'Q6L-07','question':'What do existing book and review statements mean now?', 'localReading':'The Director book Ch34/65 Interstice between T7-T8 and Q6 unanswered text are preserved book evidence. Do not infer the crystal path maps to Interstice or that all old Director operations are automatically abolished. Prior reviewed U-09/GP-U06/OR-09 are identity gaps and remain valid. The owner register retained phrase Q6 Floor-97 Old God remains open is too broad if read as the whole domain. July 30 not answered in this round remains historically accurate.'},
        {'id':'Q6L-08','question':'What can proceed before the pending Heartcell-builder answer?', 'localReading':'A source-linked Director companion can clarify the already recorded Q6 scope. Do not decide the ambiguous Use the original version message. Planes review can compare the sources with current boundaries, without inventing a link between cosmological planes, Floor 97, the prison or Interstice.'}
    ]
    audit={'reviewId':'COSMOLOGY-Q6-LATER-LOCK-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'registeredDomain':domain,'sourceBindings':bindings,'exactSourceExcerpts':excerpts,'issues':issues,
           'priorReviewAssessment':'A focused chronology/scope clarification, not a claim that every prior review missed the locks. The source-authority register already cites later Q6 authority and Continuity lines136-215. Creation and gods companions specifically preserve identity gaps. Current planes preparation needs explicit operational/public boundaries, and the recent owner register has one broad Q6-open phrase.',
           'sourceInformationDeleted':0,'originalSourcesModified':False,'bookRewritePerformed':False,'newOwnerRulingCreated':False,'fullCosmologyApproved':False}
    request='''COSMOLOGY-Q6-LATER-LOCK-01 — focused source conference before planes.

The previous owner reconciliation is received and locally verified: 11 exact owner quotes, 34 DOCX citation occurrences, 83 original source bindings; only derived CANON_CORE then changed with its prior bytes preserved. Your conditional Heartcell authorship finding is retained; the human clarification is still pending. No source or original receipt was overwritten.

Please semantically read LOCAL_SOURCE_READING.json and the full current registered Q6 owner-lock file, canon domain entry, main continuity Q6, July31/Aug5 activity records, public boundary, and current owner companion. Compare the supplied current Director Ch34/65 exact passage record to its two DOCX sources as needed (paragraph indices count every w:p, including blanks/tables, zero-based). Prior source-authority review already recognized later Q6 authority, while creation/gods identity gaps remain valid: do not falsely claim none of the previous reviewers knew this. We need a precise successor clarification, not a new owner vote or new lore.

Resolve each Q6L-01 through Q6L-08 with a reasoned disposition and exact path + line range/excerpt (or JSON pointer) citations. Pay particular attention to: Aug5 produces OR exposes wording versus July31 defeat/take wording; regular floor versus hidden chamber; current devouring-to-one versus old plural sleepers; still-open survivor/OldGod/Ul'nak/Binding/Interstice identity; public knowledge ceiling versus existing Director operations; and what a later public-book scrub actually needs. No new encounter math, identity merger, plane connections, chronology or Heartcell-builder decision. Clarify whether an explicit shared identity is required before any future full OldGod/crystal encounter design, versus what can be staged as a clearly provisional anonymous interface.

Return a compact downloadable ZIP named COSMOLOGY_Q6_LATER_LOCK_01_Addendum_and_Evidence.zip with:
REGISTER.json (eight issues, disposition, evidence [{path, firstLineOneBased,lastLineOneBased,excerpt}] or exact jsonPointer evidence; separate remaining dependencies), DIRECTOR_COMPANION.md (usable current source-linked correction/addendum), VERDICT.md (agreement/disagreement and adoption scope), SOURCE_HASHES.json (the 28 source bindings), SEMANTIC_COVERAGE.json (what was actually read, no hash-only semantic claim), EVIDENCE_MANIFEST.json (actual bytes/SHA256 of the five preceding files).
Include no other files and preserve Unicode. Source files are under sources/<repository-relative-path>. SOURCE_BINDINGS.json lists exact uploaded bytes; registry objects and quote excerpts can be verified directly. Do not claim full cosmology/game certification, book rewrite, public export, or human approval.
'''
    root.mkdir()
    (root/'LOCAL_SOURCE_READING.json').write_bytes(encoded(audit))
    (root/'SOURCE_BINDINGS.json').write_bytes(encoded(bindings))
    (root/'REQUEST.txt').write_text(request,encoding='utf-8',newline='\n')
    for p in source_paths:
        dest=root/'sources'/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes());assert dest.read_bytes()==p.read_bytes()
    payloads=[{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(root.rglob('*')) if p.is_file()]
    (root/'PACKAGE_MANIFEST.json').write_bytes(encoded(payloads))
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file(): z.write(p,p.relative_to(root).as_posix())
    receipt.write_bytes(encoded({'reviewId':'COSMOLOGY-Q6-LATER-LOCK-01','archive':info(archive),'sources':len(bindings),'issues':len(issues),'payloads':len(payloads),'localReading':info(root/'LOCAL_SOURCE_READING.json'),'submitted':False,'sourceInformationDeleted':0}))
    print(json.dumps(read(receipt)))


if __name__=='__main__':main()
