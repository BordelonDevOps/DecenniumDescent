"""Deliver saved work after the gods/pantheons submission without changing sources."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, sys

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('snapshot_helpers', HERE/'deliver_progress_2026_10_15_cosmology.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
p.W = HERE.parent/'audit_work/github-snapshot-2026-10-15-pantheons'
p.REPORT = 'docs/audit/2026-10-15/github-snapshot-pantheons'
p.BASE = 'dff2089b873a22d21b192f7c2d4a40e11f83c059'
p.STATUS = 'SNAPSHOT_STATUS_2026-10-15_PANTHEONS.md'
G, D, W, REPORT, A, BASE, STATUS = p.G, p.D, p.W, p.REPORT, p.A, p.BASE, p.STATUS
lp, git, digest, write_new, jsraw = p.lp, p.git, p.digest, p.write_new, p.jsraw
previous_tree_reader = p.tree
p.tree = lambda ref=BASE: previous_tree_reader(ref)


def assemble():
    plan = json.loads((W/'plan.json').read_bytes())
    assert not plan['credentialPatternAlerts']
    assert git('status', '--porcelain=v1', '-z') == b''
    assert git('rev-parse', 'HEAD').decode().strip() == BASE
    expected, paths = {}, []
    for row in plan['included']:
        raw = lp(G/row['path']).read_bytes()
        assert digest(raw) == row['sha256'], row['path']
        expected[row['path']] = row['gitBlob']
        if row['changedFromBaseline']:
            dest = lp(D/row['path'])
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(raw)
            assert digest(dest.read_bytes()) == row['sha256'], row['path']
            paths.append(row['path'])

    index = p.read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')
    assert index['authoredCounts'] == {'reviewed': 419, 'pending': 429}
    submission = p.read(f'{A}/COSMOLOGY_GODS_PANTHEONS_01_SUBMISSION.json')
    assert submission['sourceFiles'] == 71 and submission['status'] == 'sent-once-response-observed-running'
    followup = p.read(f'{A}/COSMOLOGY_GODS_PANTHEONS_01_LOCAL_FOLLOWUP_READING.json')
    assert followup['sourceFilesStillUnchanged'] == 71 and followup['ruleChanges'] == 0
    for source in p.read(f'{A}/cosmology-gods-pantheons-01/SOURCE_BINDINGS.json'):
        assert p.binding(source['path']) == source, source['path']
    formula = p.read(f'{A}/COSMOLOGY_MATRIX_FORMULA_SOURCE_CHECK_01.json')
    assert formula['paragraphsChecked'] == 23 and formula['originalSourceModified'] is False
    inventory = p.read(f'{A}/ORIGINAL_COSMOLOGY_EPILOGUE_RULE_INVENTORY_01.json')
    assert inventory['count'] == 17 and inventory['runtimeApproved'] is False
    evidence = [
        'ACTIVE_AUTHORING_CHECKPOINT_AFTER_GODS_PANTHEONS_SUBMISSION.json',
        'COSMOLOGY_GODS_PANTHEONS_01_PREPARATION.json',
        'COSMOLOGY_GODS_PANTHEONS_01_SUBMISSION.json',
        'COSMOLOGY_GODS_PANTHEONS_01_LOCAL_FOLLOWUP_READING.json',
        'ORIGINAL_COSMOLOGY_EPILOGUE_RULE_INVENTORY_01.json',
        'COSMOLOGY_MATRIX_FORMULA_SOURCE_CHECK_01.json',
    ]
    checkpoint = {
        'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'ownerInstruction': 'Push what we have done to github.',
        'scope': 'Saved development backup; no new game rules adopted by this delivery.',
        'authoredSpellCounts': index['authoredCounts'],
        'cosmology': {
            'completedScopedReviews': ['COSMOLOGY-SOURCE-AUTHORITY-01', 'COSMOLOGY-CREATION-ORIGIN-01'],
            'submittedReview': 'COSMOLOGY-GODS-PANTHEONS-01',
            'submittedSourceFilesReverified': 71,
            'savedReviewState': 'Submitted; no returned verdict preserved in this snapshot. Live browser state was not rechecked for this delivery.',
            'localFollowupFindings': 8,
            'epilogueSourceInventoryUnits': 17,
            'matrixFormulaSourceParagraphsChecked': 23,
            'originalSourcesModifiedByDelivery': False,
            'fullCosmologyApproved': False,
        },
        'wholeGameAcceptanceClaimed': False,
        'sourceInformationDeleted': 0,
        'usageInstruction': 'Owner revoked the prior 50% stop limit during this delivery: dont worry about the limit. I am watching it.',
        'evidence': [p.binding(f'{A}/{name}') for name in evidence],
    }
    notice = f'> **Latest progress backup — 15 October 2026:** See [the current snapshot status]({STATUS}). Includes the gods/pantheons submission, local source comparisons, epilogue inventory and Matrix formula source check. The saved GPT verdict is still pending. **419 spells reviewed / 429 pending.** Full cosmology and whole-game approval remain open. Earlier status text below is retained history.\n\n'
    overlays = []
    for name in ['README.md', 'START_HERE.md']:
        raw = lp(G/name).read_bytes()
        preserved = f'{REPORT}/source-before/{name}'
        write_new(D/preserved, raw)
        delivered = notice.encode() + raw
        lp(D/name).write_bytes(delivered)
        overlays.append({'path': name, 'sourceSha256': digest(raw), 'deliveredSha256': digest(delivered), 'preservedSource': preserved, 'change': 'Current delivery notice prepended; source content retained byte-for-byte.'})
        paths += [name, preserved]

    status = f'''# Decennium Descent progress backup — 15 October 2026, gods and pantheons

This saves the current local work at the owner's request, continuing from `{BASE}`. The game remains in development.

- The gods/pantheons review packet and submission record include 71 bound source files, nine proposed issue rows and four proposed summaries. No returned GPT verdict is preserved in this snapshot; this push does not adopt those proposals. The live browser was not rechecked for this delivery.
- The local follow-up records complete prose reading of the three original cosmology documents and current Player Appendix B, with eight source issues for comparison against GPT's eventual verdict. This is reading coverage, not full rules or cosmology approval.
- The original cosmology epilogue has a preserved inventory of seventeen rules/toolbox groups. Domain reconciliation and behavior review remain pending.
- The Matrix formula source check covers 23 paragraphs. Their incomplete-looking fragments are present in the supplied Word document; no hidden equation objects or media were found to repair them. No formulas were reconstructed.
- Earlier source/authority and creation/origin reviews remain preserved. Ordinary spells remain **419 reviewed / 429 pending**; the thirteen copy-release behavioral examples and other development gates remain open.

Resume from the [saved authoring checkpoint]({A}/ACTIVE_AUTHORING_CHECKPOINT_AFTER_GODS_PANTHEONS_SUBMISSION.json), the [later formula source check]({A}/COSMOLOGY_MATRIX_FORMULA_SOURCE_CHECK_01.json), and this [delivery checkpoint]({REPORT}/DELIVERY_CHECKPOINT.json). Retrieve the existing GPT gods/pantheons response and compare it against the local follow-up before adopting any new decisions.

The [manifest]({REPORT}/manifest.json) and [staged verification]({REPORT}/STAGED_VERIFICATION.json) record exact preservation and delivery checks. No source information or tracked Git entries were deleted. Original cosmology documents and successful historical receipts remain unchanged. Existing exclusions continue to retain private configuration, raw browser captures, third-party reference books, dependencies and generated work directories locally. This is a development backup containing Director material, not a player-only publication.

The owner withdrew the previous 50% usage stop instruction and is monitoring usage directly. Historical checkpoints retain their original instructions as dated records. This push does not certify full cosmology, whole-game flow, runtime completion, balance or human playtesting.
'''
    extras = {STATUS: status.encode(), f'{REPORT}/DELIVERY_CHECKPOINT.json': jsraw(checkpoint), f'{REPORT}/delivery-script.py': Path(__file__).read_bytes()}
    manifest = dict(plan)
    manifest.update({
        'scope': 'Saved development backup through gods/pantheons submission and local source checks; no whole-game acceptance claimed.',
        'assembledAtUtc': datetime.now(timezone.utc).isoformat(),
        'deliveryOverlays': overlays,
        'allSelectedSourcesReverified': True,
        'wholeGameAcceptanceClaimed': False,
        'sourceInformationDeleted': 0,
        'originalCosmologyDocumentsModified': False,
    })
    extras[f'{REPORT}/manifest.json'] = jsraw(manifest)
    for name, raw in extras.items():
        write_new(D/name, raw)
        paths.append(name)
    for name in set(paths):
        expected[name] = p.blob(lp(D/name).read_bytes())
    write_new(W/'expected-staged-blobs.json', jsraw(expected))
    write_new(W/'stage-paths.nul', b'\0'.join(name.encode() for name in sorted(set(paths)))+b'\0')
    print(json.dumps({'sourceFilesReverified': len(plan['included']), 'pathsToStage': len(set(paths)), 'sourceInformationDeleted': 0}))


if __name__ == '__main__':
    {'scan': p.scan, 'assemble': assemble, 'verify': p.verify}[sys.argv[1]]()
