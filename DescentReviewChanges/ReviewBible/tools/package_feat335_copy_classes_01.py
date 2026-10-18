"""Seal the agreed class-copy integration with full source/code/test evidence."""
from datetime import datetime, timezone
from pathlib import Path
import json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded


def main():
    root = A/'feat335-copy-classes-01'
    progress = A/'FEAT335_COPY_CLASSES_01_PROGRESS.json'
    prep = A/'FEAT335_COPY_CLASSES_01_PREPARATION.json'
    request = A/'FEAT335_COPY_CLASSES_01_GPT_UPDATE.txt'
    zp = A/'DD_Feat335_Copy_Classes_01.zip'
    assert not any(p.exists() for p in [root, progress, prep, request, zp])
    report_path = A/'FEAT335_COPY_CLASSES_01_CHECK.json'
    report = json.loads(report_path.read_bytes())
    assert report['status'] == 'pass' and report['checks'] == 205 and not report['failures']
    bindings = {b['path']: b for b in report['sourceBindings']}
    def bind(p):
        b = info(p); bindings[b['path']] = b; return b
    for p in [report_path, Path(__file__), A/'FEAT335_COPY_PAYLOADS_01_PROGRESS.json',
              A/'FEAT335_COPY_RELEASE_01_PROGRESS.json']: bind(p)
    record = {'id': 'FEAT335-COPY-CLASSES-01', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'AGREED_RULE_IMPLEMENTATION; ACTUAL_GPT_PROGRESS_UPDATE_UNSENT',
        'previousIntegration': info(A/'FEAT335_COPY_PAYLOADS_01_PROGRESS.json'),
        'sourceAuthority': info(A/'feat335-copy-release-source-addendum-01/FEAT335_COPY_RELEASE_SOURCE_ADDENDUM_01.json'),
        'validation': info(report_path),
        'implementations': [info(R/'tools'/n) for n in ['feat335_copy_class_providers.py', 'feat335_copy_class_release.py']],
        'counts': {'checks': 205, 'conditionalHistories': 22, 'classes': 2, 'profiles': 7},
        'scope': 'Actual source-qualified Shaman/Mirrorsage known-repertoire and level credentials, paid ASI feats, direct copy commitments and all seven existing recipient adapters. Existing Shaman paid-totem/ordinary-vent and Mirrorsage shared-release boundaries are connected within explicit conditional fixtures.',
        'coverage': report['coverage'],
        'completedAtThisBoundary': [
            'Actual native class/ability/rank ceilings and source bindings; no Wizard impersonation, feat-only alias or automatic original-spell grant.',
            'Both classes use their existing RP capacities and FS-09 copy quote; suppressed/lost providers, forged Action counts, missing RP and actual Fractured thresholds reject before mutation.',
            'Shaman uses WIS. Paid own totem and copy share RP/cadence/actions and one adopted concentration burden. Immediate copy preserves the aura and ordinary positive vent; sustained copy ends the totem before the counter window.',
            'Bloodcaller retains its real pool/totem but loses ranked ordinary-Shaman qualification. An independently acquired retained feat-only Blast route remains CHA/q0 within its own scope.',
            'Mirrorsage uses INT with no class first-release Refrain waiver. Its exact same EchoLedger blocks existing paid Beast-origin class releases and feat copies in both directions; countering does not refund either cap.',
            'Changing to a feat-only CHA provider does not bypass an owned Mirrorsage round cap; extra turns do not reset that cap.',
            'Existing Wizard/feat-only commitment tests136 and recipient tests115 pass unchanged; historical reports remain frozen.'
        ],
        'remainingWork': report['limits'],
        'queuedReadyQuestionUnchanged': {'id': 'COPY-READY-ALLOWANCE-01', 'source': info(A/'FEAT335_COPY_RELEASE_01_PROGRESS.json'), 'newDecisionSelected': False},
        'newRuleAdoptions': 0, 'sourceInformationDeleted': 0, 'runtimeApproved': False,
        'fullFeatExactApproved': False, 'humanBalanceApproved': False, 'wholeGameComplete': False}
    progress.write_bytes(encoded(record)); bind(progress)
    request.write_text(
        'Actual GPT progress update — prepared UNSENT. Accepted CRS-03B/C now have bounded class integrations: actual Shaman WIS and Mirrorsage INT credentials, exact level/rank/RP tables, source-qualified known spell subsets and paid class ASIs. '
        '205 checks in22 conditional histories pass; the existing136 commitment and115 payload checks also pass unchanged. All7 existing recipient profiles execute under each native provider. '
        'The Shaman case uses an actual selected2RP totem: the copy shares its canonical RP/cadence/Action state and adopted concentration, receives/consumes no vent, and a subsequent actual ordinary Fate Coin receives the positive vent. Sustained copies end the totem before countering; no restoration. '
        'The Mirrorsage case shares its actual EchoLedger and wallet with the existing paid Beast-origin command boundary, proving mutual cap exclusion. Class Mirrorbind capture and class Echo strain/payload are still upstream/unimplemented; this is not whole-class approval. '
        'Bloodcaller cannot use retained RP as ordinary Shaman rank permission; a separately acquired Blast-only route stays CHA/q0. No rule was added and no authored spell membership or whole-game gate changed. '
        'The archive contains all full source files, implementation, test operands, outcomes and limitations. COPY-READY-ALLOWANCE-01 remains unanswered. '
        'Part4 hit the actual conversation-length limit; Part5 creation is awaiting the owner. Continue the prepared full Illusion14 conference first when available. This progress package is not a substitute for reading that conference or a claim that GPT has reviewed the new code.\n',
        encoding='utf8', newline='\n')
    bind(request); root.mkdir()
    for b in bindings.values():
        p = G/b['path']; assert info(p) == b
        dst = root/'sources'/b['path']; dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(p.read_bytes())
        assert dst.read_bytes() == p.read_bytes()
    (root/'MANIFEST.json').write_bytes(encoded({'progress': info(progress), 'sources': list(bindings.values()),
        'sourceCount': len(bindings), 'allBytesVerified': True, 'newRuleAdoptions': 0}))
    with zipfile.ZipFile(zp, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.write(progress, 'PROGRESS.json')
        for p in root.rglob('*'):
            if p.is_file(): z.write(p, p.relative_to(root).as_posix())
    with zipfile.ZipFile(zp) as z:
        assert z.testzip() is None
        for b in bindings.values(): assert z.read('sources/'+b['path']) == (G/b['path']).read_bytes()
    prep.write_bytes(encoded({'archive': info(zp), 'progress': info(progress), 'request': info(request),
        'manifest': info(root/'MANIFEST.json'), 'sourceCount': len(bindings), 'allArchivedBytesVerified': True,
        'status': 'Prepared UNSENT; no new rule or broader approval.'}))
    print(json.dumps({'archive': info(zp), 'sources': len(bindings), 'checks': 205, 'histories': 22}))


if __name__ == '__main__': main()
