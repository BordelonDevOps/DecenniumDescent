"""One-shot receipt of the completed GPT availability report; no rules promotion."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import hashlib, json

G = Path(r'C:\Github\DecenniumDescent')
A = G / 'docs/audit/2026-10-08/full-game'
PRE = A / 'ACTIVE_AUTHORING_CHECKPOINT_MAGIC_CORE_CASEBOOK_100.json'
OUT = A / 'ACTIVE_AUTHORING_CHECKPOINT_NOTEBOOK_RECHECK_101.json'
CHECK = A / 'ACTIVE_AUTHORING_CHECKPOINT_NOTEBOOK_RECHECK_101_CHECK.json'
BACK = A / 'navigation-before-notebook-recheck-101'
SAVED = A / Path(__file__).name
for p in (OUT, CHECK, BACK, SAVED):
    assert not p.exists(), str(p)

def enc(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

def info(p, data=None):
    b = p.read_bytes() if data is None else data
    return {'path': p.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def put(p, b):
    with p.open('xb') as f:
        f.write(b)

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

checks = []
def ck(name, result):
    checks.append({'check': name, 'pass': bool(result)})
    assert result, name

prior = read(PRE)
ck('Exact checkpoint100 retained', info(PRE)['sha256'] == '8408ea2579b4791f3115faa3bf03ebf9b93546763f76e2b596ade61cb9770154')
for row in [prior['currentAuthoredIndex'], prior['currentAcceptedInterfaceRegistry'], prior['currentWorkQueue'], *prior['canonicalHelperBaselinesUnchanged']]:
    ck('Protected baseline unchanged: ' + row['path'], info(G / row['path']) == row)

native = A / 'GPT_BESTIARY_RETURN02_UNAVAILABLE_NATIVE_101.json'
response = A / 'GPT_BESTIARY_RETURN02_UNAVAILABLE_RESPONSE_101.txt'
notebooks = A / 'GPT_NOTEBOOK_PERTINENT_RECHECK_101.json'
browser = A / 'GPT_BESTIARY_RETURN02_VISIBLE_RESPONSE_101.txt'
unity_browser = A / 'GPT_UNITY_VISIBLE_RECHECK_101.txt'
n = read(native)
msg = next(x for x in n['turns'][0]['items'] if x['type'] == 'agentMessage')
ck('Completed exact availability response', n['turns'][0]['status'] == 'completed' and msg['id'] == 'e4f07372-a3f4-4b2b-b26d-b599422cbc33')
ck('Full response retained', response.read_text(encoding='utf-8').rstrip('\n') == msg['text'])
ck('Visible response independently present', 'The interrupted Return02 work was partially written' in browser.read_text(encoding='utf-8'))
nb = read(notebooks)
ck('Unity latest known response identity retained', nb['unityChat']['latestTurn']['items'][1]['id'] == 'b0572b7f-e15c-4d11-8353-86853e0329c6')
ck('Standby routing retained', nb['standbyChat']['latestTurn']['items'][1]['id'] == 'b6d0af60-3b57-434e-99a0-5b3163ba6a22')
brief = A / 'unity-development-directions-75/Decennium_Descent_Unity_Codex_Directions.md'
ck('Previously downloaded Unity brief unchanged', info(brief)['sha256'] == 'cfca586c7351f7ac913523a3b9cde076bc3e92f4301404f1f78b608db6145369')

inputs = [
    ('DD_Bestiary_Complete_Source_Prepared_v3_81.zip', 42404028, 'a07245c72cfbe44079d9addcf1376f3d7f9c8a7ad1b3a6cee442f2964fb1a15b'),
    ('DD_Bestiary_Current_EX58_Context_82.zip', 3510131, '424be66594e6acdea09f640e3e6e64af997cd56805852beb6e451081de0aa334'),
    ('DD_Bestiary_Linked_Recipe_Dependencies_91.zip', 564856, '019ef9001fa948d02c1df0bb60bf7195bcbfa83485b2e9efaa5c85a4b8c6dd58'),
    ('DD_Bestiary_Replacement_Current_Context_96.zip', 834145, 'fa5db7718a341ceca3d65a088ec1c34e1d3cd345362cf5cedd788082c5476f38'),
]
input_receipts = []
for name, size, sha in inputs:
    r = info(A / name)
    ck('Local source archive survives: ' + name, r['bytes'] == size and r['sha256'] == sha)
    input_receipts.append(r)

cp = deepcopy(prior)
cp['id'] = 'ACTIVE-AUTHORING-NOTEBOOK-RECHECK-101'
cp['recordedAtUtc'] = datetime.now(timezone.utc).isoformat()
cp['previousCheckpoint'] = info(PRE)
cp['status'] = 'Notebook reconciliation: full completed Bestiary Return02 availability response preserved; GPT reports staged outputs missing and no final archive. Four exact local input archives survive. Unity brief and standby chat carry no new decision beyond already preserved records. No feat coverage, rules acceptance or canonical application increment.'
cp['previousGptObservationBefore101'] = deepcopy(prior['activeGptReviewAtLastVerifiedObservation'])
cp['activeGptReviewAtLastVerifiedObservation'].update({
    'latestNativeRecord': info(native), 'latestObservation101': info(browser),
    'latestObservedStatus': 'Native conversation reports idle with completed assistant e4f07372-a3f4-4b2b-b26d-b599422cbc33. Browser visibly contains this complete response but still retained a Stop/thinking footer; no interruption, duplicate continuation, or new dispatch was performed. Completed availability report explicitly says no Return02 output bytes exist. The actual full candidate remains unavailable and unaccepted.'
})
cp['bestiaryUnavailableReturn02_101'] = {
    'native': info(native), 'fullResponse': info(response), 'browser': info(browser),
    'continuationUserId': '624e9657-d99d-46fd-a54e-163e25ab96d6',
    'assistantId': msg['id'], 'exactLocalInputs': input_receipts,
    'partialFilesReportedMissing': ['INPUT_CHECKS.json', 'SOURCE_MODEL.json', 'SOURCE_HISTORY.json', 'RULES.json', 'MODEL.json', 'PROCEDURES.json', 'input/'],
    'outputArchiveReceived': False, 'outputHashAvailable': False,
    'newRulesAccepted': False, 'interimTraitAndPressureWaveClaimsAccepted': False,
    'scope': 'Report of remote temporary-output loss; not a loss of local sources or completed local casebooks. Historical Return01 and Return02 claims remain evidence only.'
}
cp['pertinentNotebookRecheck101'] = {
    'completeNativeEvidence': info(notebooks), 'unityBrowser': info(unity_browser), 'verifiedLocalUnityBrief': info(brief),
    'unityLatestUserId': '41d5797f-d115-4cce-90fd-8ccc835b86cb', 'unityLatestAssistantId': 'b0572b7f-e15c-4d11-8353-86853e0329c6',
    'standbyStatus': 'Review continuation part 5 remains standby; its historical525/323/249 and earlier24 acceptance context are not current53 acceptance totals.',
    'otherCodexActivity': {'threadId': '01a14c7c-7b93-74f1-9cd7-0920537dafec', 'title': 'Prepare project for Unity design', 'observed': 'Active Stage0/Stage1 TEST_ONLY foundation work, as reported by that task. No independent code/test review or message to that task in this check.'},
    'userClarification': 'Optional async question asks which GPT discussion the owner means. No answer had arrived when this checkpoint was written.',
    'messagesSentToGptThisCheck': 0
}
cp['nextAction'] = 'Continue full magic_extended58/116 and heritage_mutation22/44 casebooks from unchanged500/660 originals and17/28 boundaries. For bestiary, preserve this loss report and use smaller separately versioned recoverable source-backed deliveries, saved locally after each completion; do not expect vanished Return02 staged files to become available or promote interim trait/PressureWave claims. No reconstruction request was dispatched in101. Honor any clarification about pertinent notebook information. Avoid duplicating the separate active Unity task; canonical rules integration remains owner-reserved. Parent335 final assembly/joint review and all five whole-positive-case holds remain.'
cp['lastUsageObservation'] = {'usedPercent': 64, 'remainingPercent': 36, 'resetsAt': 1793110625, 'stopAtRemainingPercent': 20, 'source': 'Fresh get_usage_limits at notebook recheck101'}
cp['laterLocalWork'] = 'Authored review checkpoints73-101 local after separately verified GitHub backup through72. No push in101. Separate active Unity task may have later work in github-delivery; do not overwrite it.'

nav = [G / row['path'] for row in prior['navigation']]
originals = {}; replacements = {}
for p in nav:
    row = next(x for x in prior['navigation'] if x['path'] == p.relative_to(G).as_posix())
    raw = p.read_bytes(); originals[p] = raw
    ck('Navigation unchanged before insertion: ' + p.name, info(p, raw) == row)
    if p.suffix == '.html':
        pos = raw.find(b'>', raw.find(b'<body')) + 1
        note = ('<aside><p><strong>Checkpoint101:</strong> Latest GPT report says Bestiary Return02 temporary outputs are unavailable; all four local input archives verified intact. Unity directions match the preserved brief. Feat coverage remains500/660 plus17/28. <a href="docs/audit/2026-10-08/full-game/' + OUT.name + '">Notebook reconciliation</a>.</p></aside>\n').encode()
    else:
        pos = raw.find(b'\n') + 1
        prefix = 'docs/audit/2026-10-08/full-game/' if p.name == 'START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/'
        note = ('\n**Current notebook check:** [Checkpoint101](' + prefix + OUT.name + ') preserves GPT\'s completed report that Bestiary Return02 temporary outputs are unavailable. All four local source archives are intact. The Unity brief matches the saved copy; a separate Codex chat is implementing its TEST_ONLY foundation. Feat coverage remains500/660 original cases and17/28 boundaries; no rules were promoted.\n').encode()
    ck('Valid insertion: ' + p.name, pos > 0)
    replacements[p] = raw[:pos] + note + raw[pos:]
    ck('Older navigation preserved: ' + p.name, replacements[p][:pos] + replacements[p][pos + len(note):] == raw)

cp['navigation'] = [info(p, replacements[p]) for p in nav]
cp['preservedNavigation'] = [info(BACK / p.name, originals[p]) for p in nav]
ck('Coverage and membership unchanged', cp['authoredCounts'] == prior['authoredCounts'] and cp['acceptedButUnapplied'] == 53 and cp['featMagicCoreCasebook100'] == prior['featMagicCoreCasebook100'])
ck('Prior checkpoint fields retained', set(prior).issubset(cp))
payload = enc(cp)
validation = enc({'id': 'CHECKPOINT101-VALIDATION', 'checkpoint': info(OUT, payload), 'checks': checks, 'passed': len(checks), 'failed': 0, 'runtimeTestsExecuted': 0, 'newMessagesSent': 0, 'script': info(SAVED, Path(__file__).read_bytes())})
BACK.mkdir()
for p in nav:
    put(BACK / p.name, originals[p])
    assert p.read_bytes() == originals[p], 'Concurrent navigation change: ' + str(p)
    p.write_bytes(replacements[p])
for p, data in [(SAVED, Path(__file__).read_bytes()), (OUT, payload), (CHECK, validation)]:
    put(p, data)
print(json.dumps({'checkpoint': info(OUT), 'check': info(CHECK), 'passed': len(checks), 'failed': 0}, indent=2))
