"""Preserve the actual Fishing exact verdict, evidence and pre-repair revision."""
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import shutil
import zipfile
from build_fishing_recipe_candidate import ROOT, GAME, AUDIT, read, sha, dump


def main():
    downloads = Path(r'C:\Users\cbord\Downloads')
    verdict = downloads / 'FISHING_EXACT_OPERATIONAL_VERDICT.md'
    archive = downloads / 'Fishing_exact_review_audit.zip'
    prefix = read(AUDIT / 'GPT_FISHING_EXACT_REPLY_PREFIX.json')
    full = verdict.read_text(encoding='utf-8')
    def normalized(text):
        text = '\n'.join(line for line in text.splitlines() if not line.startswith(':chatgpt-content-reference'))
        return re.sub('[^a-z0-9]', '', text.casefold())
    downloaded_prefix = normalized(full.split('## FI-E10')[0])
    actual_prefix = normalized(prefix['text'].split('## FI-E10')[0])
    assert downloaded_prefix == actual_prefix, 'Downloaded verdict does not match actual reply through FI-E09'
    headings = re.findall(r'^## (FI-E\d\d) ', full, re.M)
    assert headings == [f'FI-E{i:02}' for i in range(1,12)], headings
    assert 'completion of these eleven repairs' in full.lower()
    assert '392/687' in full and '251/433' in full and '348/687' in full
    evidence = AUDIT / 'fishing-exact-review-gpt-evidence'
    with zipfile.ZipFile(archive) as z:
        names = z.namelist(); assert len(names) == 13
        for name in names:
            path = PurePosixPath(name)
            assert not path.is_absolute() and '..' not in path.parts and path.parts[0] == 'Fishing_exact_review_audit'
        hashes = json.loads(z.read('Fishing_exact_review_audit/AUDIT_FILE_HASHES.json'))
        for name, expected in hashes.items():
            assert hashlib.sha256(z.read('Fishing_exact_review_audit/' + name)).hexdigest() == expected
        assert z.read('Fishing_exact_review_audit/FISHING_EXACT_OPERATIONAL_VERDICT.md') == verdict.read_bytes()
        assert hashes['fishing_reference_submitted.py'] == sha(ROOT / 'tools/fishing_reference.py')
        if evidence.exists():
            assert all((evidence / n).read_bytes() == z.read(n) for n in names)
        else:
            for name in names:
                dest = (evidence / name).resolve(); assert dest.is_relative_to(evidence.resolve())
                dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(z.read(name))
    dest = AUDIT / 'GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md'
    if dest.exists(): assert dest.read_bytes() == verdict.read_bytes()
    else: shutil.copy2(verdict, dest)
    zip_dest = AUDIT / archive.name
    if zip_dest.exists(): assert sha(zip_dest) == sha(archive)
    else: shutil.copy2(archive, zip_dest)
    submitted = read(AUDIT / 'fishing-exact-submission-original/MANIFEST.json')
    assert all(sha(AUDIT / 'fishing-exact-submission-original' / p) == h for p, h in submitted.items())
    assert all(sha(GAME / p) == h for p, h in submitted.items() if not p.endswith('FISHING_EXACT_PART2_SUBMISSION.json'))
    backup = AUDIT / 'fishing-before-exact-review-repairs'
    paths = {GAME / p for p in submitted}
    paths.update([ROOT / 'tools/build_fishing_recipe_candidate.py', ROOT / 'tools/templates/fishing_rules.md',
                  AUDIT / 'FISHING_AUTHORING_STATUS.json', AUDIT / 'FISHING_HISTORICAL_TRANSPORT_BACKLOG.json',
                  GAME / 'START_HERE.md', AUDIT / 'GPT_REVIEW_CONTINUATION_HANDOFF.md',
                  AUDIT / 'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json'])
    if not backup.exists():
        manifest = {}
        for p in sorted(paths):
            rel = p.relative_to(GAME); target = backup / rel; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target); manifest[rel.as_posix()] = sha(p)
        dump(backup / 'MANIFEST.json', manifest)
    else:
        manifest = read(backup / 'MANIFEST.json'); assert all(sha(backup / p) == h for p, h in manifest.items())
    capture = {'status':'completed exact verdict captured; eleven required repairs; no promotion yet',
        'threadId':prefix['notebookId'],'turnId':prefix['turnId'],'replyId':prefix['replyId'],
        'capturedAtUtc':datetime.now(timezone.utc).isoformat(),'file':dest.name,'characters':len(full),
        'bytes':dest.stat().st_size,'sha256':sha(dest),'actualReplyPrefixCharacters':len(prefix['text']),
        'normalizedActualReplyMatchThrough':'FI-E09','requiredRepairIds':headings,
        'evidenceZip':zip_dest.name,'evidenceZipSha256':sha(zip_dest),'archiveMembers':len(names),
        'verifiedMemberHashes':len(hashes),'submittedHelperMatchesGptTranscription':True,
        'preRepairBackup':backup.relative_to(AUDIT).as_posix(),'preRepairFiles':len(manifest),
        'authorization':'Complete FI-E01..11 and specified full-candidate checks, then promote44 without another generic conference or full exact-card review.',
        'recipesApproved':0,'currentReviewedRecipes':348,'publicReviewed':223,
        'sourceInformationDeleted':False,'githubPushPerformed':False,'cosmology':'post-push only'}
    dump(AUDIT / 'FISHING_EXACT_REVIEW_CAPTURE.json', capture)
    plan = {'status':'required repairs not yet complete','authority':dest.name,'authoritySha256':sha(dest),
            'scope':'Submitted44 cards plus bounded FI-E01..11 corrections; no broader redesign',
            'repairs':[{'id':ident,'title':re.search(r'^## '+ident+r' — (.+)$',full,re.M).group(1),'status':'pending',
                        'requirements':full.split('## '+ident+' — ',1)[1].split('\n## ',1)[0]} for ident in headings],
            'promotionGate':'All eleven repairs, complete candidate/projection parity, actual positive/negative checks and fresh hashes required',
            'recipesPromoted':0,'sourceInformationDeleted':False,'cosmology':'post-push only'}
    plan_path = AUDIT / 'FISHING_EXACT_REPAIR_PROGRESS.json'
    if not plan_path.exists(): dump(plan_path, plan)
    print(json.dumps(capture))


if __name__ == '__main__': main()
