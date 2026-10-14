"""Apply the actual GPT ACQ-02 correction once, preserving every prior file."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G/'docs/audit/2026-10-08/full-game'
V = A/'feat327-acq02-source'
P = A/'feat-exact-01-before-acq02'
receipt = A/'FEAT327_ACQ_02_DERIVED_OPERATIONS.json'
assert not P.exists() and not receipt.exists(), 'One-use application; do not overwrite history'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def info(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf-8')


archive = A/'DD_FEAT327_ACQ_02_Warrior_Tier_Addendum.zip'
assert archive.stat().st_size == 20196
assert info(archive)['sha256'] == '7e69bc1839aa96f5119d345520b0f1f9791cd6317e9f02aa92a6b30c7303f726'
manifest = read(V/'FILE_MANIFEST.json')
for item in manifest['payloads']:
    actual = info(V/item['path'])
    assert actual['bytes'] == item['bytes'] and actual['sha256'] == item['sha256']
ops = read(V/'OPERATIONS.json')
o1, o2, o3 = ops['operations']
assert ops['disposition'] == 'REVISE_GLOBAL_GLOBAL_PROPOSAL_TO_PER_TREE_ADVANCED_GLOBAL_APEX'
assert o1['replacement'] == o2['replacement']

planned = []
public = G/o1['path']
public_before = read(public)
assert info(public)['sha256'] == o1['sourceSha256']
assert public_before['engine'][17] == o1['old']
public_after = deepcopy(public_before)
public_after['engine'][17] = o1['replacement']
public_bytes = json_bytes(public_after)
planned.append((public, public_bytes, 'ACQ02-O1', '/engine/17'))

draft = R/'data/playtest/class_drafts/warrior.json'
draft_after = read(draft)
assert draft_after['engine'][17] == o1['old']
draft_after['engine'][17] = o1['replacement']
planned.append((draft, json_bytes(draft_after), 'ACQ02-O1-operative-authoring-mirror', '/engine/17'))

guide = G/o2['path']
guide_before = guide.read_text(encoding='utf-8')
assert info(guide)['sha256'] == o2['sourceSha256']
assert guide_before.count(o2['old']) == 1
planned.append((guide, guide_before.replace(o2['old'], o2['replacement']).encode('utf-8'), 'ACQ02-O2', 'Engine/MUTATION TIERS'))

shared_paths = [R/'data/director/feat_candidates/exact_01/shared_rules.json',
                R/'data/public/feat_candidates/exact_01/shared_rules.json']
old_wording = None
for path in shared_paths:
    data = read(path)
    rule = next(row for row in data['rules'] if row['id'] == 'FS-01')
    assert o3['paragraph'] not in rule['wording']
    if old_wording is None:
        old_wording = rule['wording']
    else:
        assert old_wording == rule['wording']
    rule['wording'] += '\n\n'+o3['paragraph']
    planned.append((path, json_bytes(data), 'ACQ02-O3', '/rules[id=FS-01]/wording'))

shared_guide = R/'docs/feats/exact-candidate-01/SHARED_RULES.md'
shared_before = shared_guide.read_text(encoding='utf-8')
assert shared_before.count(old_wording) == 1
planned.append((shared_guide, shared_before.replace(old_wording, old_wording+'\n\n'+o3['paragraph']).encode('utf-8'),
                'ACQ02-O3-manuscript', 'End of FS-01 wording, before FS-02; this reader projection has no Basis section'))

# This is the current source pointer, not a historical claim about old bytes.
foundation = R/'data/playtest/character_foundation.json'
foundation_after = read(foundation)
row = next(row for row in foundation_after['classes'] if row['class'] == 'Warrior')
assert row['classCandidatePath'] == public.relative_to(G).as_posix()
assert row['classCandidateSha256'] == o1['sourceSha256']
row['classCandidateSha256'] = sha256(public_bytes).hexdigest()
planned.append((foundation, json_bytes(foundation_after), 'mechanical-current-binding-update', '/classes[class=Warrior]/classCandidateSha256'))

# Preserve comparison engines and original packages; no broad regeneration.
protected_paths = [
    G/'docs/reference/Player_Rulebook_v6_source_text.txt',
    A/'DD_Feats_327_Final_Source_Verdict_and_Evidence.zip',
    A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
    A/'FEAT_EXACT_01_WARRIOR_ACQUISITION_FIXTURES.json',
    R/'data/public/feat_candidates/exact_01/candidate.json',
    R/'data/director/feat_candidates/exact_01/candidate.json',
    R/'data/director/feat_candidates/exact_01/cohorts/heritage_mutation.json',
    R/'data/director/feat_candidates/exact_01/cohorts/general_combat.json',
    R/'data/director/expedition_candidate/part04.json',
    R/'data/director/expedition_candidate/complete_candidate.json',
]
protected = [info(path) for path in protected_paths]
preserved = []
for path, _, operation, pointer in planned:
    binding = info(path)
    copy = P/binding['path']
    copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, copy)
    assert copy.read_bytes() == path.read_bytes()
    preserved.append({**binding, 'preservedCopy': copy.relative_to(G).as_posix(),
                      'operation': operation, 'semanticTarget': pointer})
(P/'PRESERVATION_MANIFEST.json').write_bytes(json_bytes(preserved))

for path, data, _, _ in planned:
    path.write_bytes(data)
    assert path.read_bytes() == data
for path, binding in zip(protected_paths, protected):
    assert info(path) == binding
assert read(public)['cards'] == public_before['cards']
for index, paragraph in enumerate(public_before['engine']):
    if index != 17:
        assert read(public)['engine'][index] == paragraph

result = {
    'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
    'status': 'exact-operations-applied-awaiting-independent-acceptance',
    'addendumId': 'FEAT327-ACQ-02', 'sourcePackage': info(archive),
    'sourceOperations': info(V/'OPERATIONS.json'),
    'sourceAddendum': info(V/'FEAT327_ACQ_02_ADDENDUM.md'),
    'actualGptUiResponse': info(A/'FEAT327_ACQ_02_GPT_RESPONSE.md'),
    'threadUrl': 'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b',
    'reviewStatus': 'Actual GPT response observed complete; copied through its visible Copy control. '
                    'Browser download observation timed out, but the completed local ZIP was independently verified '
                    'at20196bytes and its declared SHA256. No question or download was resent.',
    'requestMessageId': None, 'replyMessageId': None,
    'messageIdCaptureStatus': 'Not exposed by the attempted DOM selector; no identifiers invented.',
    'preservationManifest': info(P/'PRESERVATION_MANIFEST.json'),
    'changes': [{'before': before, 'after': info(path), 'operation': operation, 'semanticTarget': pointer}
                for (path, _, operation, pointer), before in zip(planned, preserved)],
    'measuredCurrentDescendants': [info(path) for path, _, _, _ in planned],
    'unchangedProtectedBindings': protected,
    'historicalSnapshotsNotRewritten': True,
    'unaffectedWarriorEngineElementsAndAll126CardsUnchanged': True,
    'allTwelveFeatProceduresUnchanged': True,
    'onlyNamedIssueClosed': False,
    'candidateReadyForSubmission': False, 'sourceInformationDeleted': False,
    'runtimeImplemented': False, 'humanBalanceApproved': False,
    'wholeGameFlowConfirmed': False, 'pushed': False, 'cosmologyReviewed': False,
}
with receipt.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(result, stream, ensure_ascii=False, indent=2)
    stream.write('\n')
print(json.dumps({'receipt': info(receipt), 'changedFiles': len(planned),
                  'preservedFiles': len(preserved), 'awaitingIndependentAcceptance': True}, indent=2))
