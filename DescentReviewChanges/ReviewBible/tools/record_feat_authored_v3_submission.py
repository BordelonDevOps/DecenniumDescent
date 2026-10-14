"""Record the observed GPT dispatch and update navigation, preserving snapshots."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, re

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
OUT = A / 'FEAT_AUTHORED_V3_SUBMISSION.json'
BACKUP = A / 'navigation-before-feat-v3-dispatch'


def read(p): return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b = p.read_bytes()
    return {'path': p.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': sha256(b).hexdigest()}
def write(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    assert not OUT.exists() and not BACKUP.exists(), 'One-use receipt; preserve existing revision'
    package_path = A / 'FEAT_AUTHORED_V3_PACKAGE.json'
    package = read(package_path)
    archive = G / package['archive']
    assert info(archive)['sha256'] == package['sha256']
    browser = A / 'FEAT_AUTHORED_V3_SENT_BROWSER.txt'
    screenshot = A / 'FEAT_AUTHORED_V3_SENT.jpg'
    prompt = A / 'CODEX_FEAT_AUTHORED_V3_ACTUAL_REQUEST.txt'
    assert archive.name in browser.read_text('utf-8')
    assert 'ChatGPT is responding' in browser.read_text('utf-8')
    assert screenshot.read_bytes().startswith(b'\xff\xd8\xff')
    index = R / 'data/director/feat_operating_proposal_index.json'
    manuscript = R / 'docs/feats/FEAT_OPERATING_PROPOSAL_INDEX.md'
    nav_builder = R / 'tools/build_review_map.py'
    before = {}
    for p in [index, manuscript, R / 'tools/build_feat_operating_proposal_index.py',
              A / 'FEAT_OPERATING_PROPOSAL_INDEX_CHECK.json', nav_builder,
              R / 'tools/review_map_template.html', G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        target = BACKUP / p.relative_to(G)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(p.read_bytes())
        before[p.relative_to(G).as_posix()] = {'original': info(p), 'preserved': info(target)}
    write(BACKUP / 'PRESERVATION_MANIFEST.json', before)
    old = read(index)
    assert old['sentToGpt'] is False and old['pendingFullFeats'] == 327
    d = dict(old)
    d['sentToGpt'] = True
    d['sourceProposalConference'] = {
        'status': 'Submitted to GPT; awaiting actual full verdict. No feat promoted.',
        'threadId': '6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b',
        'requestId': 'bf9d8dbb-22e3-4c31-a046-74608129acb9',
        'submissionReceipt': OUT.relative_to(G).as_posix(),
        'archive': info(archive), 'completeProcedureDrafts': 325, 'deferredGrantOutlines': 2,
        'authoredExamples': 660, 'interfaceQuestions': 15,
        'historicalStatusNote': 'Earlier unsent labels within unchanged cohort files describe their preparation snapshots.',
        'generatorPolicy': 'Historical index builder is one-use and must not overwrite this dispatch metadata.'}
    restored = dict(d)
    restored.pop('sourceProposalConference')
    restored['sentToGpt'] = False
    assert restored == old
    write(index, d)
    text = manuscript.read_text('utf-8')
    old_sentence = 'None of these proposals has been adopted or sent to GPT; this index changes no rules or review status.'
    assert text.count(old_sentence) == 1
    text = text.replace(old_sentence,
        'All 327 pending proposals have now been submitted to Calibration Review Part 2 with their complete sources and 660 examples. The joint verdict is pending; none has been adopted. This index changes no rules or approval status.')
    old_next = 'After the active expedition conference returns, reconcile its actual travel, service, rest, social and transport decisions with the proposed feats. Send the full pending-feat sources, current governing manuscripts and complete proposed procedures to Calibration Review Part 2 together. Preserve any earlier/current disagreements explicitly; a source-authoring verdict is followed by exact review of the completed candidate.'
    assert text.count(old_next) == 1
    text = text.replace(old_next,
        'The expedition conference is fulfilled. The submitted feat packet includes its current reviewed books and fifteen explicit interface questions, including Endurance timing, bonus stacking, mounting, appraisal, foraging and rest repair. Await the actual individual feat dispositions, implement agreed changes while preserving the drafts, then review the assembled exact candidate. Historical unsent labels in the cohort files remain preparation evidence.')
    text += '\n[Current submission and source bindings](../../../../docs/audit/2026-10-08/full-game/FEAT_AUTHORED_V3_SUBMISSION.json) · [Complete review guide](../../../../docs/audit/2026-10-08/full-game/FEAT_AUTHORED_V3_REVIEW_GUIDE.md)\n'
    manuscript.write_text(text, encoding='utf-8', newline='\n')
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
        p = (manuscript.parent / target).resolve()
        assert p.is_file() or p == OUT, target

    nav = nav_builder.read_text('utf-8')
    marker = '    featured = [\n'
    assert nav.count(marker) == 1
    nav = nav.replace(marker, '''    feat_dispatch = read(A / "FEAT_AUTHORED_V3_SUBMISSION.json")
    assert feat_dispatch["sent"] is True and feat_dispatch["requestId"] == "bf9d8dbb-22e3-4c31-a046-74608129acb9"
    for binding in [feat_dispatch["archive"], *feat_dispatch["currentNavigationArtifacts"]]:
        assert digest(G / binding["path"]) == binding["sha256"]
        current_inputs[binding["path"]] = binding["sha256"]
    current_inputs["docs/audit/2026-10-08/full-game/FEAT_AUTHORED_V3_SUBMISSION.json"] = digest(A / "FEAT_AUTHORED_V3_SUBMISSION.json")
    featured = [
        ("327 pending feats — complete procedures submitted to GPT", "docs/audit/2026-10-08/full-game/FEAT_AUTHORED_V3_REVIEW_GUIDE.md"),
        ("Feat conference submission and preserved sources", "docs/audit/2026-10-08/full-game/FEAT_AUTHORED_V3_SUBMISSION.json"),
''')
    old_status = 'Feat index has325 full unadopted procedures and2 deferred grant outlines,660 examples.'
    assert nav.count(old_status) == 1
    nav = nav.replace(old_status,
        'All327 pending feat proposals (325 full drafts and2 deferred grant outlines,660 examples) are now submitted to GPT in request bf9d8dbb-22e3-4c31-a046-74608129acb9 with707 full payloads and15 explicit EX58/cross-cohort issues. Packaging passed5940 preservation/structural checks and707 archive payload checks. Verdict pending; no feat promotion. The71 higher-spell proposals were included only as unadopted comparisons.')
    nav_builder.write_text(nav, encoding='utf-8', newline='\n')
    receipt = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'Complete feat source/procedure conference actually submitted; GPT responding; no verdict yet.',
        'threadTitle': 'Calibration Review Part 2',
        'threadId': '6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b',
        'requestId': 'bf9d8dbb-22e3-4c31-a046-74608129acb9',
        'requestUrl': 'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b',
        'sent': True, 'savedUserMessageId': 'bf9d8dbb-22e3-4c31-a046-74608129acb9',
        'evidence': 'Browser showed submitted text, named attachment and active Stop control. Read-thread independently returned this exact user message and one attached file; a user-only connector turn is not a completed GPT verdict.',
        'archive': info(archive), 'packageReceipt': info(package_path),
        'actualRequest': info(prompt), 'browserProof': info(browser), 'screenshot': info(screenshot),
        'sourceFeats': 335, 'reviewedFeatsUnchanged': 8, 'pendingFullFeats': 327,
        'completeLocalDraftsBeforeCurrentInterfaceReview': 325, 'deferredGrantOutlines': 2,
        'authoredExamples': 660, 'cohorts': 9, 'interfaceQuestions': 15,
        'archivePayloads': 707, 'packagingChecks': 5940, 'archiveRoundtripChecks': 707,
        'navigationPreservation': info(BACKUP / 'PRESERVATION_MANIFEST.json'),
        'currentNavigationArtifacts': [info(index), info(manuscript)],
        'proposalAndGameRulesChanged': 0, 'newRuleAdoptions': 0, 'sourceInformationDeleted': 0,
        'runtimeImplemented': False, 'humanBalanceApproved': False, 'wholeGameFlowApproved': False,
        'pushed': False, 'cosmologyReviewed': False,
        'nextAction': 'Read the actual GPT terminal verdict when ready; verify any delivered artifacts before adoption. Continue independent remaining spell/Director authoring while GPT reviews.'}
    write(OUT, receipt)
    print(json.dumps({k: v for k, v in receipt.items() if k not in ['browserProof', 'screenshot']}, indent=2))


if __name__ == '__main__': main()
