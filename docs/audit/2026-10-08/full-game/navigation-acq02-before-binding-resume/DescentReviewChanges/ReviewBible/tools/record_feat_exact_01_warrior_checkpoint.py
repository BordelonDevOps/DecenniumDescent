"""Record the twelve Warrior acquisitions and fulfilled actual GPT ACQ-02."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G/'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def info(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')


previous = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_NUMERIC_PREREQUISITES.json'
target = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_WARRIOR_ACQUISITIONS.json'
preservation = A/'navigation-and-coverage-before-feat-exact-01-warrior-acquisitions'
assert not target.exists() and not preservation.exists(), 'One-use checkpoint already recorded'
fixture_path = A/'FEAT_EXACT_01_WARRIOR_ACQUISITION_FIXTURES.json'
check_path = A/'FEAT_EXACT_01_WARRIOR_ACQUISITION_CHECK.json'
notes_path = A/'FEAT_EXACT_01_WARRIOR_ACQUISITION_NOTES.md'
fulfillment_path = A/'FEAT327_ACQ_02_INDEPENDENT_FULFILLMENT.json'
fulfillment = read(fulfillment_path)
warrior_check = read(check_path)
assert not warrior_check['failures'] and warrior_check['mutationFeatCount'] == 12
assert fulfillment['failureCount'] == 0 and fulfillment['onlyNamedIssueClosed']
for binding in fulfillment['measuredCurrentDescendants']:
    assert info(G/binding['path']) == binding

ledger_path = R/'data/playtest/game_development_coverage.json'
original_ledger = read(ledger_path)
ledger = deepcopy(original_ledger)
now = datetime.now(timezone.utc).isoformat()
prefix = 'docs/audit/2026-10-08/full-game/'
review_refs = [prefix+'feat327-source-verdict/FEAT327_FINAL_SOURCE_VERDICT.md',
               prefix+'FEAT327_ACQ_01_GPT_ADDENDUM.md',
               prefix+'feat327-acq02-source/FEAT327_ACQ_02_ADDENDUM.md']
validation_refs = [prefix+'FEAT_EXACT_01_NUMERIC_PREREQUISITE_CHECK.json',
                   prefix+'FEAT_EXACT_01_WARRIOR_ACQUISITION_CHECK.json',
                   prefix+'FEAT327_ACQ_02_INDEPENDENT_FULFILLMENT.json']
for ref in review_refs+validation_refs:
    assert (G/ref).exists(), ref
for row in ledger['aspects']:
    if row['id'] not in {'DD-06', 'DD-09', 'DD-14', 'DD-69'}:
        continue
    for field, refs in [('reviewEvidence', review_refs), ('validationEvidence', validation_refs)]:
        for ref in refs:
            if ref not in row[field]:
                row[field].append(ref)
    row.setdefault('completedScopes', []).append(
        'FEAT327-ACQ-02 narrow source correction fulfilled: Advanced equipment is capped at two per actual tree, '
        'Apex at one total across all trees, within unlocked Warrior slots. Seven prior files preserved; '
        '164 independent source/whole-descendant/bounded checks pass. All126 Warrior cards and12 feat procedures '
        'unchanged. Twelve source-qualified synthetic acquisition witnesses and bounded activation sequences '
        'passed683 checks before the correction; current independent checks confirm all12 remain eligible. '
        'Full feat runtime, human balance, class/game-wide closure and exact candidate approval remain open.')
    row.setdefault('currentEvidenceAddenda', []).append({
        'id': 'FEAT327-ACQ-02', 'recordedAtUtc': now, 'status': 'fulfilled-named-correction-only',
        'authority': review_refs[-1], 'fulfillment': validation_refs[-1],
        'historicalBindingPolicy': 'The measured seven descendants override prior hashes for current evaluation. '
                                  'Earlier reports remain evidence of their earlier input bytes; do not rewrite '
                                  'old manifests or treat stale equality checks as new failures.',
    })
    if row['id'] == 'DD-14':
        row.setdefault('historicalOpenIssueSnapshots', []).append({
            'recordedAtUtc': now, 'reason': 'Retain prior preparation/unsent status statements as history; '
                                        'actual source verdict and assembled candidate now supersede those stages.',
            'status': row['status'], 'openIssues': deepcopy(row['openIssues']),
        })
        row['status'] = 'source-directions-complete-exact-candidate-validation-in-progress'
        row['openIssues'] = [
            'All327 source-authoring decisions are delivered; the assembled candidate preserves335 originals, '
            'eight reviewed envelopes,325 full new procedures andtwo deferred null payloads. Separate exact '
            'review and promotion remain outstanding.',
            'FXC-05:209 numeric/level/None identities have1678 boundary projections;12 Warrior identities have '
            'source-qualified paid-acquisition witnesses.114 other credential-dependent identities still '
            'need actual training, spell, lineage, owned-feat, trade or context receipts. These disjoint '
            'predicate scopes do not claim all335 complete acquisitions.',
            'Complete remaining FXC-04–10 finite supplements, selection choices, repeatability, finite '
            'initialization, clocks, damage/resources, actual physical/social premises, casting/Ready and '
            'all660 original authored case premises. Existing checks have stated limited scopes.',
            'Package the complete exact candidate and obtain actual GPT exact review when the required '
            'acceptance evidence is complete. Full game flow agreement precedes authorized GitHub push; '
            'verify the remote commit before cosmology review. No source deletion or runtime/balance approval.',
        ]
        row['completedScopes'].append(
            'FEAT327 source-authoring conference completed and independently reproduced; full exact candidate '
            'assembled with original objects/questions/examples retained. ACQ-01 weapon prerequisites and '
            'ACQ-02 Warrior tier scope are fulfilled named corrections. Source-authoring completion does not '
            'promote the unfinished exact candidate.')

nav = R/'tools/build_review_map.py'
text = nav.read_text(encoding='utf-8')
anchor = '        ("Feat numeric prerequisites — independent printed-string checks", "FEAT_EXACT_01_NUMERIC_PREREQUISITE_CHECK.json"),'
assert text.count(anchor) == 1
text = text.replace(anchor, anchor+'\n'
    '        ("Warrior feats — twelve acquisition examples", "FEAT_EXACT_01_WARRIOR_ACQUISITION_NOTES.md"),\n'
    '        ("Warrior feats — full source-bound acquisition fixtures", "FEAT_EXACT_01_WARRIOR_ACQUISITION_FIXTURES.json"),\n'
    '        ("Warrior feats — acquisition and activation checks", "FEAT_EXACT_01_WARRIOR_ACQUISITION_CHECK.json"),\n'
    '        ("Warrior tier limits — actual GPT ACQ-02 addendum", "feat327-acq02-source/FEAT327_ACQ_02_ADDENDUM.md"),\n'
    '        ("Warrior tier limits — exact applied operations", "FEAT327_ACQ_02_DERIVED_OPERATIONS.json"),\n'
    '        ("Warrior tier limits — independent fulfillment", "FEAT327_ACQ_02_INDEPENDENT_FULFILLMENT.json"),')
anchor = 'The remaining finite acceptance evidence, full package and actual exact review remain outstanding.'
assert text.count(anchor) == 1
text = text.replace(anchor,
    'Twelve Warrior mutation feats now have source-qualified synthetic acquisitions with complete20-level '
    'class-choice history, actual slots/tiers, one paid identity through either representation and bounded '
    'serum/Apex sequences:683 checks pass. Actual GPT ACQ-02 revised the proposed global Advanced cap to '
    'two Advanced per actual tree, while retaining one Apex globally. Seven derived files were corrected '
    'with prior bytes preserved;164 independent whole-file/source/bounded checks pass, including mixed-tree '
    'equipment and a recorded conditional Transcendent threshold/expiry trace. Only this named issue is '
    'closed.114 other credential-dependent identities and broader feat acquisition/use work remain. '
    'The old numeric/history/Warrior reports retain their original input bindings; use the ACQ-02 '
    'fulfillment receipt for the current seven descendants. '+anchor)
compile(text, str(nav), 'exec')

saved = []
for path in [ledger_path, nav, G/'REVIEW_MAP.html', A/'REVIEW_MAP_BUILD.json']:
    binding = info(path)
    copy = preservation/binding['path']
    copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, copy)
    assert copy.read_bytes() == path.read_bytes()
    saved.append({**binding, 'preservedCopy': copy.relative_to(G).as_posix()})
manifest = preservation/'PRESERVATION_MANIFEST.json'
write(manifest, saved)
write(ledger_path, ledger)
nav.write_text(text, encoding='utf-8', newline='\n')
build = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True,
                       text=True, encoding='utf-8')
if build.returncode:
    print(build.stderr)
    raise SystemExit(build.returncode)
navigation = read(A/'REVIEW_MAP_BUILD.json')
assert not navigation['missingLinks']
assert navigation['sha256'] == info(G/'REVIEW_MAP.html')['sha256']
# Every unrelated aspect and every closure/human-evidence field remains intact.
for old, current in zip(original_ledger['aspects'], ledger['aspects']):
    assert old['closure'] == current['closure'] and old['humanEvidence'] == current['humanEvidence']
    if old['id'] not in {'DD-06', 'DD-09', 'DD-14', 'DD-69'}:
        assert old == current

state = read(previous)
previous_gpt = deepcopy(state['activeGptReview'])
state.update({
    'recordedAtUtc': now, 'goalTurnClassification': 'progress',
    'previousGoalTurnClassification': 'progress:209 numeric prerequisite trees/1678 boundary cases; no complete335 acquisition claim.',
    'previousCheckpoint': info(previous),
    'status': 'Twelve source-qualified Warrior acquisition witnesses validated. Actual GPT ACQ-02 tier-cap '
              'ambiguity resolved and fulfilled through seven preserved derived corrections and164 '
              'independent checks.114 other credential-dependent identities and broader exact acceptance '
              'work remain. Whole-game delivery and post-push cosmology remain open.',
    'featWarriorAcquisitionPass': {'fixtures': info(fixture_path), 'notes': info(notes_path),
                                  'checks': info(check_path), 'checkCount': warrior_check['checks'],
                                  'scope': warrior_check['scope'], 'identities': 12,
                                  'remainingCredentialDependentIdentities': 114,
                                  'sourceHashStatus': 'Historical before ACQ-02; all33 normal mutation cards, '
                                                      'all126 class cards, class schedule and12 acquisition '
                                                      'requirements/procedures remain unchanged under the '
                                                      'independently reconstructed narrow correction.'},
    'featWarriorTierAddendum': {'id': 'FEAT327-ACQ-02',
                               'question': info(A/'FEAT327_ACQ_02_WARRIOR_TIER_QUESTION.txt'),
                               'response': info(A/'FEAT327_ACQ_02_GPT_RESPONSE.md'),
                               'sourcePackage': info(A/'DD_FEAT327_ACQ_02_Warrior_Tier_Addendum.zip'),
                               'addendum': info(A/'feat327-acq02-source/FEAT327_ACQ_02_ADDENDUM.md'),
                               'operations': info(A/'FEAT327_ACQ_02_DERIVED_OPERATIONS.json'),
                               'fulfillment': info(fulfillment_path), 'checks': fulfillment['checks'],
                               'onlyNamedIssueClosed': True,
                               'measuredCurrentDescendants': fulfillment['measuredCurrentDescendants']},
    'newRuleAdoptions': 1,
    'newRuleAdoptionScope': 'One explicitly NEW narrow reconciliation: Advanced cap2 per tree/Apex cap1 global; '
                            'no whole class/feat promotion or complete exact-candidate approval.',
    'coverageLedger': info(ledger_path),
    'navigation': {'map': info(G/'REVIEW_MAP.html'), 'receipt': info(A/'REVIEW_MAP_BUILD.json'),
                   'links': navigation['existingDistinctLinks'], 'missingLinks': []},
})
state.setdefault('priorCompletedGptObservations', []).append(previous_gpt)
state['activeGptReview'].update({
    'requestId': None, 'replyId': None, 'requestStatus': 'completed',
    'currentAuthoritativeObservation': 'Actual GPT response complete in Calibration Review Part2; full response '
                                     'copied through visible UI and four-payload package independently hash-verified. '
                                     'Named seven-file correction and all eight finite case groups fulfilled locally.',
    'finalVerdictReceived': True, 'awaitingGptResponse': False,
    'liveObservation': info(A/'FEAT327_ACQ_02_GPT_RESPONSE.md'),
    'terminalReport': info(fulfillment_path),
    'finalVerdictScope': 'FEAT327-ACQ-02 only; full exact feat and whole-game review remain pending.',
    'browserScreenshot': info(A/'FEAT327_ACQ_02_SUBMITTED.png'),
    'browserRecoveryNote': 'Download observer timed out and reset cua session after the complete response '
                           'was saved. The completed20196-byte download existed and matched its declared SHA; '
                           'no resubmission or repeated download. getTab125745656 then reported Debugger '
                           'unattached. Reuse selected Chrome browser3 for future work and recover a tab '
                           'through documented APIs if needed; original user tab125745612 was never closed.',
    'messageIdentifierStatus': 'Current request/reply IDs were not captured; nulls are intentional.',
})
state['safeNextActions'] = [
    'Continue FXC-05 with the114 other credential-dependent identities. Start from the126 /remaining records '
    'in the numeric report and exclude the12 sharedPaidIdentity Warrior records. The12 current acquisition '
    'predicates, actual source loadouts, class choices and paired purchase identities are now exercised; '
    'their complete damage/target/use-time procedures remain separate.',
    'Actual GPT FEAT327-ACQ-02 is complete and locally fulfilled, not awaiting a reply. The approved scope '
    'is two equipped Advanced per actual tree, one Apex globally, actual total slots. Do not use the rejected '
    'global-two-Advanced proposal. Seven current files are bound by FEAT327_ACQ_02_INDEPENDENT_FULFILLMENT.json. '
    'Apply that receipt after ACQ-01 when resolving current hashes; never rewrite historical snapshots.',
    'The683 Warrior acquisition checks predate the narrow source correction;164 independent current checks '
    'prove exact seven-file differences, unchanged126 cards/12 procedures, all12 positive acquisitions '
    'under the corrected cap, and eight case groups with bounded event/accounting scope. Numeric/history '
    'reports also preserve earlier source hashes. Do not rerun old validators blindly after legitimate '
    'foundation/shared-rule hash changes or overwrite prior receipts.',
    'No full660-case or all335-complete-acquisition claim is established. Complete numeric-cohort named '
    'choices/repeatability/initialization;114 credential-dependent trees; finite supplements; physical, '
    'social, spell/copy/Ready, clocks, damage and causal budgets before exact-package submission.',
    'The development coverage ledger now records the actual final327 source verdict and both fulfilled '
    'narrow addenda. Prior unsent/source-preparation open-issue wording is preserved under the Feats '
    'historicalOpenIssueSnapshots and in the pre-change ledger; broader domain closures remain open.',
] + [action for action in state['safeNextActions'][3:] if not action.startswith('When finite acceptance evidence')]
state['safeNextActions'].append(
    'When acceptance evidence is complete, submit the complete exact candidate to the actual Calibration '
    'Review Part2 chat. Current ACQ-02 request is already terminal. Recover browser access using selected '
    'Chrome3 and the documented same-browser tab workflow; do not resend the completed question. Final '
    'whole-game agreement still precedes authorized GitHub push, verified remote commit, then cosmology.')
for path in [A/'feat-exact-01-before-acq02/PRESERVATION_MANIFEST.json', manifest]:
    state.setdefault('preservationManifests', []).append(info(path))
with target.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(state, stream, ensure_ascii=False, indent=2)
    stream.write('\n')
print(json.dumps({'checkpoint': info(target), 'navigationLinks': navigation['existingDistinctLinks'],
                  'coverageLedger': info(ledger_path), 'narrowGptIssueFulfilled': True,
                  'remainingCredentialDependentIdentities': 114,
                  'candidateReadyForSubmission': False, 'wholeGameComplete': False}, indent=2))
