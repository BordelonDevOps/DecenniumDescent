from pathlib import Path
import datetime, hashlib, json, subprocess

root = Path.cwd()
out = root / 'engine/artifacts/tac05-frightened/development'
report = out / 'IMPLEMENTATION_PROGRESS.json'
previous = out / 'IMPLEMENTATION_PROGRESS.090513.json'
if not previous.exists():
    previous.write_bytes(report.read_bytes())
baseline = 'd9ad3db339f0da613690e7de9c497f77b8221c71'
changed = subprocess.check_output(['git', 'diff', baseline, '--name-only', '--', 'engine'], text=True).splitlines()
new = [f'engine/com.decennium.foundation/{name}{suffix}' for name in [
    'Laboratory/Model/FrightenedRules.cs', 'Laboratory/Model/SharedFrightened.cs',
    'Laboratory/Model/SourceQualifiedConditionCure.cs',
    'Runtime/Core/FrightenedRecords.cs', 'Runtime/Persistence/FrightenedCodec.cs',
    'Tests/EditMode/FrightenedLifecycleCases.cs'] for suffix in ['', '.meta']]
files = []
for name in sorted(set(changed + new)):
    data = root.joinpath(name).read_bytes()
    files.append(dict(path=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
old = root.joinpath('docs/unity/evidence/2026-11-15-tac07-cleric-repertoire/regression/inventory.txt').read_text(encoding='utf-8-sig').splitlines()
inventory = out.joinpath('source-integration-inventory.txt').read_text(encoding='utf-8-sig').splitlines()
assert len(old) == 1509 and [x for x in inventory if x in set(old)] == old
headless = 'run-20261115T093650131Z-40129a7c/results.json'
standalone = 'compile-20261115T093927386Z-07dca160/results.json'
for name in [headless, standalone]:
    build = json.loads(out.joinpath(name).read_text(encoding='utf-8-sig'))
    assert build['status'] == 'PASS'
    for source in build['sourceHashes']:
        data = root.joinpath('engine', source['path'].replace('\\', '/')).read_bytes()
        assert hashlib.sha256(data).hexdigest() == source['sha256']
value = dict(
    status='IMPLEMENTATION_IN_PROGRESS_NOT_REVIEW_READY',
    atUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    approvedContractCommit='d9ad3db339f0da613690e7de9c497f77b8221c71',
    actualReviewResponse='226d668a-fd32-51b3-b64c-bbd74b67e64c',
    sourceCommit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(), sourceFiles=files,
    connectedAbilityCheckCase=headless, connectedMainCase='case-20261115T093927408Z/results.json', standaloneCompile=standalone,
    focusedRegression='source-integration-controls.json',
    staticChecks='static/static-20261115T093927415Z-c23a0399/results.json',
    consoleProbe='console-source-probe/results.json', connectedObservations='connected-observations.json',
    inventory='source-integration-inventory.txt', registeredCases=len(inventory), retainedPredecessors=len(old),
    focusedPassed=132, fullRegression='RUNNING_FIXED_DLLS_NOT_A_PASS',
    regressionLaunch='regression/launch.json', regressionRunId='d9620202bba1434aa4885782edb2888d',
    compatibility='compatibility/results.json', authenticCompatibility='PASS_19_WIRE95_THROUGH_106_ROUNDTRIP_AND_CONTINUATION',
    detachedClockControls='clock-components-3/results.json', detachedProjectionControls='projection-controls/results.json',
    detachedForcedMovementControls='forced-movement-controls-2/results.json',
    consumerScope='consumer-scope-progress.json', historicalCausalControls='historical-check-controls/results.json',
    pathReports={name: (json.loads(out.joinpath(name).read_text(encoding='utf-8-sig'))['status']
        if out.joinpath(name).exists() else 'RUNNING') for name in [
        'paths-main-20261115T093859999Z/results.json', 'paths-ability-check/results.json', 'paths-sight-loss/results.json']},
    sourceAuditVerifier='Historical source-only verifier asserts unchanged engine; do not rerun it after engine implementation.',
    implementedSoFar=[
        'Versioned v2 shared relationship journal/codec; unchanged v1 admission and serialization. Independent presence, immunity, suppression, expiry and raw named-cure component controls.',
        'Internal source-qualified cure invocation/settlement with explicit detached test authority; all present eligible records, including suppressed, end while protected and unrelated records remain. No public cure command or Radiance producer.',
        'Wire107/base90 Frightened profile retains Cleric RP/repertoire and adds exact revision0 defender fixture entitlement and STR choice, source-bound histories, endpoint/recharge records and strict codec validation.',
        'Actual reinforced-encounter target-only activation with directional sight both ways, range/line of effect, preflight, Action, shared normal WIS saves and source-specific applications. Defender authored first-use tactic and trusted typed later-use path.',
        'Target-owned captured repeat/final endpoints and real shared-clock repeat saves before expiry; named recharge integrates actual local/global regular-start cadence while preserving old Soldier serialization.',
        'Exact rational simultaneous-motion boundary calculation integrated into world advancement and reconciliation. Detached shared-clock controls pass whole/split18-second repeat/final/recharge progression, three source-motion attribution cases, and exact pending-edge suspension at temporary immunity expiry with retained paid distance.',
        'Fear consumers wired for club/unarmed, ranged, Hide/Search, cache, formula, manufacture, mining, retreat and tactical/ordinary movement; full consumer and historical-validation audit remains.',
        'Current connected case executes first two successful uses, two lawful recharges, third use with both failed saves, active restore, paid affected attack (11/16 selects11), both repeat successes, actual later defeat/normal closure/paid exploration, and alternate farther-position unchanged approach denial.',
        'Additional genuine branch pays tool retrieval and tactical cache pick: 11/16 selects11, +2 total13 fails DC15, Action spent. Actual WIS repeat3 fails and final expiry occurs exactly6 seconds later without a third save or RNG draw.',
        'Genuine sight-loss branch uses paid steps and actual opportunity response to reach2,0 behind the authored blocker. Fear persists; an otherwise walkable closer diagonal rejects unchanged; paid Hide consumes one die with the source unseen and restores exactly.',
        'Detached source controls reject target/user sight, invalid later target, missing ownership/choice, spent Action and recharge without any stored-field change. Named immunity still pays and rolls canonical targets then prevents admission. Suppressed repeat matches the unsuppressed normal save.',
        'Historical cache natural and fear-save modifier forgeries pass structural encoding but fail strict causal restoration after fear has expired, leaving the live session byte-identical.',
        'Detached consumer controls pass independent sources, ordinary advantage cancellation, unseen/dead-source geometry and existing authoritative Push versus willing movement. These do not claim connected optional acquisition or a new public forced switch.',
        'Main216-command route matches8 reference checkpoints on uninterrupted/restored console, independent typed dispatch, restored typed and independent receipt replay. Ability/expiry186-command branch matches6 checkpoints and sight-loss181-command branch matches5 across the same five paths:95 byte comparisons total.',
        'All19 authentic wire95-106 saves pass exact roundtrip and actual remaining-command continuation, including genuine wire106 Cleric repertoire state. All19 reject unchanged when restored into the incompatible Frightened profile.',
        'New console profile and typed target input/trusted defender operation. Development console probe uses standalone DLLs and retains four identical snapshots across restore, wrong player authority, spent Action denial and exact retry.',
        'Current eight new registered cases plus124 legacy condition controls pass (132 total). Headless and separate standalone C#9 builds and static checks pass. All1509 predecessor names remain in order among1517. Actual party stance ordinal1 is Aggressive despite the legacy helper name ClericGuard.'
    ],
    requiredRemaining=[
        'Complete remaining capacity/source/class/DC/relationship forgery and per-consumer causal validation/audit details; finish final traceability and reproducibility retention.',
        'Finish per-consumer causal validation and scope audit. Partial matrix records17 families and21 actual unavailable profile fields; it is not blanket certification.',
        'Resolve genuine still-present relationship across normal closure reachability. Fourth lawful use creates fear on hero; actual next hit leaves defender at0HP but alive, so normal closure correctly rejects. This study is retained and is not a claimed closure-with-fear witness.',
        'Extend meaningful conflict/parser controls and retain complete final scripts/inputs/checkpoints.',
        'Finish the exact1517-case full regression already running under d9620202bba1434aa4885782edb2888d. Never restart or replace those six workers silently; retain every journal and completed identity.',
        'Bind and retain final evidence to the committed implementation, push Engine, send actual final evidence to Unity Rules Engine Development Part2 and resolve review blockers before successor. The implementation checkpoint is not final acceptance.'
    ]
)
report.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(status=value['status'], sourceFiles=len(files), registeredCases=len(inventory), focusedPassed=value['focusedPassed'])))
