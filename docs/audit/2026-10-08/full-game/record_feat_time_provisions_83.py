from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import hashlib, json, zipfile

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
OLD = A / 'ACTIVE_AUTHORING_CHECKPOINT_FULL_GAME_FRONTIER_82.json'
OUT = A / 'ACTIVE_AUTHORING_CHECKPOINT_FEAT_TIME_PROVISIONS_83.json'
CHECK = A / 'ACTIVE_AUTHORING_CHECKPOINT_FEAT_TIME_PROVISIONS_83_CHECK.json'
BACKUP = A / 'navigation-before-feat-time-provisions-83'
SAVED = A / Path(__file__).name
for p in (OUT, CHECK, BACKUP, SAVED):
    assert not p.exists(), str(p)

def j(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def enc(x):
    return (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

def info(p):
    b = p.read_bytes()
    return {'path': p.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

checks = []
def ck(name, truth):
    checks.append({'check': name, 'pass': bool(truth)})
    if not truth:
        raise AssertionError(name)

cp = j(OLD)
ck('Exact previous checkpoint 82', info(OLD)['sha256'] == '8d232518b1b00bad2dd5b3776e3514b28ed59ffd638e69e59843d2ddfba042e3')
casefile = A / 'FEAT335_TIME_PROVISIONS_CASES_83.json'
checkfile = A / 'FEAT335_TIME_PROVISIONS_CHECK_83.json'
archive = A / 'DD_Feat335_Time_Provisions_Cases_83.zip'
report, validation = j(casefile), j(checkfile)
ck('Exact 83 report and archive are the validated artifacts', info(casefile) == validation['report'] and info(archive) == validation['archive'])
ck('88 isolated checks passed', validation['checkCount'] == 88 and validation['failures'] == 0 and all(x['pass'] for x in validation['checks']))
ck('20 case groups and 28 variants', len(report['topLevelCaseIds']) == 20 and report['caseCount'] == 28 and len(report['cases']) == 28)
ck('FXC06 is explicitly partial and does not claim runtime or full feat approval', len(report['remainingFXC06']) == 3 and not any(report['approvalBoundaries'].values()) and validation['runtimeTestsExecuted'] == 0)
for row in report['sourceBindings']:
    ck('Full source remains exact: ' + row['path'], info(G / row['path']) == row)
with zipfile.ZipFile(archive) as z:
    ck('Archived report preserves every byte', z.read('REPORT.json') == casefile.read_bytes())
    manifest = json.loads(z.read('MANIFEST.json'))
    ck('Archive manifest accounts for every retained member', set(z.namelist()) == set(manifest) | {'MANIFEST.json'})
    ck('Archive CRC', z.testzip() is None)
    for name, binding in manifest.items():
        b = z.read(name)
        ck('Archived exact member: ' + name, len(b) == binding['bytes'] and hashlib.sha256(b).hexdigest() == binding['sha256'])

protected = [cp['currentAuthoredIndex'], cp['currentAcceptedInterfaceRegistry'], cp['currentWorkQueue'], *cp['canonicalHelperBaselinesUnchanged']]
for row in protected:
    ck('Protected current authority: ' + row['path'], info(G / row['path']) == row)
ck('Accepted but unapplied count remains 50', cp['acceptedButUnapplied'] == 50 and not cp['implementationApplied'])
ck('Complete 75-domain map remains exact', info(G / cp['currentFullGameReviewMap']['path']) == cp['currentFullGameReviewMap'] and info(G / cp['currentFullGameEvidenceFrontier']['path']) == cp['currentFullGameEvidenceFrontier'])
observation = A / 'GPT_PART5_RESONANCE_FIELDS3_HANDOFF_83.txt'
text = observation.read_text(encoding='utf-8')
ck('Same actual GPT review remains active at latest saved observation', 'Working for 54m 32s' in text and 'button "Stop"' in text and 'DD_Rank9_Resonance_Fields3_Current_Context_80.zip' in text)

navs = [G / 'START_HERE.md', R / 'docs/DEVELOPMENT_DIRECTION.md', G / 'REVIEW_MAP.html']
for row in cp['navigation']:
    ck('Exact previous navigation: ' + row['path'], info(G / row['path']) == row)
originals = {p: p.read_bytes() for p in navs}
BACKUP.mkdir()
for p, b in originals.items():
    (BACKUP / p.name).write_bytes(b)
base = 'docs/audit/2026-10-08/full-game/'
for p, prefix in [(navs[0], ''), (navs[1], '../../../')]:
    b = originals[p]
    pos = b.index(b'\n') + 1
    notice = ('\n**Current checkpoint — 20 October 2026:** [Checkpoint 83](' + prefix + base + OUT.name + ') preserves 20 Forager/Endurance case groups (28 variants, 88 passing isolated checks) against the current feat candidate and exact EX58 rules. This is partial FXC-06 evidence; full feat review and engine testing remain open. [The 75-domain map](' + prefix + base + 'FULL_GAME_CURRENT_REVIEW_MAP_82.md) remains the current overall map. GPT is still reviewing Resonance Fields3; applied 525/323/249, 173 interfaces and 50 accepted but unapplied remain unchanged.\n').encode('utf-8')
    p.write_bytes(b[:pos] + notice + b[pos:])
    ck('All original navigation bytes preserved: ' + p.name, p.read_bytes().replace(notice, b'', 1) == b)
p = navs[2]
b = originals[p]
pos = b.index(b'</h1>') + 5
notice = ('<section class="sequence" aria-label="Current feat diagnostic checkpoint"><p><strong>Checkpoint 83: Forager and Endurance specification cases.</strong> 20 case groups, 28 variants and 88 passing checks preserve actual stocks, rest debt and independent deprivation counters. Partial feat evidence; no engine or full-game approval. <a href="' + base + OUT.name + '">Current checkpoint</a> · <a href="' + base + 'FULL_GAME_CURRENT_REVIEW_MAP_82.md">75-domain review map</a></p></section>').encode('utf-8')
p.write_bytes(b[:pos] + notice + b[pos:])
ck('All original review-map bytes preserved', p.read_bytes().replace(notice, b'', 1) == b)

cp['previousGptObservationBefore83'] = deepcopy(cp['activeGptReviewAtLastVerifiedObservation'])
cp['activeGptReviewAtLastVerifiedObservation'].update(browserObservation=info(observation), activeGenerationVerified=True, completedResponseReceived=False, latestObservedStatus='Same actual Resonance Fields3 review working at 54m32s; Stop and additional thinking notice visible. No restart, resend or interruption.')
cp.update(
    id='ACTIVE-AUTHORING-FEAT-TIME-PROVISIONS-83', recordedAtUtc=datetime.now(timezone.utc).isoformat(), previousCheckpoint=info(OLD),
    status='Partial FXC-06 Forager/Endurance specification diagnostics complete: 20 groups, 28 variants, 88 checks. Exact EX58 and current candidate source bytes retained. Same actual GPT Resonance Fields3 review continues.',
    featTimeProvisionsDiagnostics={'report': info(casefile), 'archive': info(archive), 'validation': info(checkfile), 'topLevelCases': 20, 'caseVariants': 28, 'checkCount': 88, 'failures': 0, 'sourceFileCount': len(report['sourceBindings']), 'fullFeatAcceptance': False, 'runtimeTestsExecuted': 0, 'sentToGpt': False, 'remainingScope': report['remainingFXC06']},
    navigation=[info(p) for p in navs], preservedNavigation=[info(BACKUP / p.name) for p in navs],
    lastUsageObservation={'usedPercent': 42, 'remainingPercent': 58, 'stopAtRemainingPercent': 20, 'resetsAt': 1793110625},
    previousGoalTurnClassification='82 made concrete progress reconciling 75 domains and 1135 explicit evidence paths, verifying current EX58/LAX approvals and preparing the complete EX58 bestiary supplement. 83 adds 20 partial FXC-06 specification case groups with all original source and full state retained. No canonical rules are changed.',
    laterLocalWork='All 73–83 work remains local after the verified GitHub backup through 72.',
    nextAction='Receive and independently review the same active Resonance Fields3 return. Then confer on bestiary V3 with the current EX58 supplement. Complete outstanding feat time-discount and repair cases and later parent review without repeating already fulfilled scopes. Retain owner implementation reservation and all 75-domain gates.'
)
OUT.write_bytes(enc(cp))
for row in protected:
    ck('Protected authority unchanged at completion: ' + row['path'], info(G / row['path']) == row)
for row in report['sourceBindings']:
    ck('Original diagnostic source unchanged at completion: ' + row['path'], info(G / row['path']) == row)
SAVED.write_bytes(Path(__file__).read_bytes())
CHECK.write_bytes(enc({'checkpoint': info(OUT), 'checks': checks, 'checkCount': len(checks), 'failures': 0, 'newRuleAdoptions': 0, 'newDomainClosures': 0, 'runtimeTestsExecuted': 0, 'sourceInformationDeleted': 0, 'scope': 'Preservation and navigation for isolated specification evidence; no full parent feat or engine validation claim.'}))
print(json.dumps({'checkpoint': info(OUT), 'report': info(CHECK), 'checks': len(checks), 'failures': 0}))
