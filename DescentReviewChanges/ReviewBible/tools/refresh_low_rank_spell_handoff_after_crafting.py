"""Preserve the frozen 137-spell source set and add completed crafting authority."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import zipfile

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path):
    return path.relative_to(G).as_posix()

def main():
    out = A / 'LOW_RANK_SPELL_FILE_HANDOFF_V2_PREPARATION.json'
    archive = A / 'DD_Low_Rank_Spells_137_Source_Prepared_v2.zip'
    notes = A / 'LOW_RANK_SPELL_FILE_HANDOFF_V2_SCOPE.md'
    assert not any(p.exists() for p in [out, archive, notes]), 'Preserve prior revisions'
    old = read(A / 'LOW_RANK_SPELL_FILE_HANDOFF_PREPARATION.json')
    assert sha(A / old['bundleFile']) == old['bundleSha256']
    assert len(old['currentFileHashes']) == 163
    assert all(sha(G / p) == h for p, h in old['currentFileHashes'].items())
    with zipfile.ZipFile(A / old['bundleFile']) as z:
        assert z.testzip() is None
        assert all(hashlib.sha256(z.read(p)).hexdigest() == h
                   for p, h in old['currentFileHashes'].items())
    status_path = R / 'docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json'
    status = read(status_path)
    assert status['status'].startswith('REVIEWED')
    assert len(status['artifactHashes']) == 14
    assert all(sha(G / p) == h for p, h in status['artifactHashes'].items())
    catalog = read(R / 'data/public/spell_playtests/catalog.json')
    pending = {s['id'] for s in catalog['spells'] if s['operational'] is None
               and min(a['rank'] for a in s['classAccess'].values()) <= 3}
    assert pending == {s['spellId'] for s in old['selectedMembership']}
    assert len(pending) == 137
    assert sum(s['operational'] is not None for s in catalog['spells']) == 276
    verdict = A / 'advanced167-exact-reviewer-files/AEX_167_Exact_Review_Verdict.md'
    assert sha(verdict) == '87db8f8b373d497444bbd3b6b43e4dfd0b4eedf4f4239312af7bf513ace3f250'
    notes.write_text('''# Low-rank spell source conference — refreshed complete evidence

Prepared and UNSENT. This revision retains all 163 payload files from v1 byte for byte, including all six source preparations, individual questions, original spell and class objects, 141 book bindings and complete governing sources. No spell rule or source grant has changed. The v1 archive remains intact.

The advanced-crafting prerequisite is fulfilled. All 167 advanced recipes, including 100 public formulas, completed their authored-operational review under AEX-01–07. All recipe totals are now 687/687 and public 433/433. The final 14 artifacts, exact verdict, review manifest, completion validation and promotion/navigation receipts are included in full. Earlier preparation labels describing this review as pending are historical.

Use the six original SOURCE_PREPARATION.json files for the 137 exact spell identities and individual question IDs. Resolve the 136 pre-push mechanical questions. Blink remains an unchanged receipt for post-push review; do not interpret its cosmology here. The complete source check remains valid because every original dependency and selected catalog object is unchanged.

For interactions with scrolls, runes, wards, crafted spell storage, references and devices, read the complete reviewed advanced guides and exact source/card records. Keep their caster eligibility, acquisition, physical host, activation, targeting, visibility, suppression, expiry, use and repair procedures. A shared name does not merge an ordinary spell with a class feature or recipe output. A crafted carrier supplies only its reviewed permissions; it does not settle an unfinished ordinary spell's effect. The existing crafting verdict does not approve any of these pending spells.

Return finite source-authoring directions mapped to each affected spell and original question: casting time and components; class rank/access and cost; targets, range and geometry; duration and concentration; attacks/saves and all outcomes; each source clause and scaling; recast/identity, suppression and ending. Label newly supplied operating details NEW. Explain actual source conflicts and give worked boundary cases for contested procedures. Do not reopen settled crafting directions without naming a concrete conflicting source.

This packet is queued behind the current six-manuscript onboarding/charter verdict and the prepared language conference. Before dispatch, compare these hashes with the current files and include any intervening language decisions relevant to its spells. No exact-card approval is requested until complete candidate cards exist. Preserve originals and keep human balance, runtime and whole-game completion separate. Final joint whole-game flow precedes the authorized GitHub push; verified remote commit precedes careful cosmology review.
''', encoding='utf-8')
    files = {G / p for p in old['currentFileHashes']}
    files.update(G / p for p in status['artifactHashes'])
    files.update([status_path, verdict, notes, Path(__file__).resolve(),
                  A / 'ADVANCED_167_EXACT_COMPLETION_VALIDATION.json',
                  A / 'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json',
                  A / 'ADVANCED_PROMOTION_NAVIGATION_RECEIPT.json'])
    manifest = {rel(p): {'bytes': p.stat().st_size, 'sha256': sha(p)}
                for p in sorted(files, key=rel)}
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr('README_SOURCE_REVIEW.md', 'Read docs/audit/2026-10-08/full-game/LOW_RANK_SPELL_FILE_HANDOFF_V2_SCOPE.md first. All original spell evidence and completed crafting authority are included. Prepared and UNSENT. No new approvals.\n')
        z.writestr('FILE_MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        for p in sorted(files, key=rel):
            z.write(p, rel(p))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(set(z.namelist())) == len(manifest) + 2
        assert all(len(z.read(n)) == m['bytes'] and
                   hashlib.sha256(z.read(n)).hexdigest() == m['sha256']
                   for n, m in manifest.items())
    report = {'status': 'PASS complete source refresh; UNSENT',
              'preparedAtUtc': datetime.now(timezone.utc).isoformat(),
              'originalBundle': old['bundleFile'], 'originalBundleSha256': old['bundleSha256'],
              'unchangedOriginalPayloadFiles': 163, 'selectedIdentities': 137,
              'prePushMechanicalQuestions': 136, 'postPushReceiptOnlyIds': ['blink'],
              'currentBookBindings': 141, 'completedAdvancedArtifactsAdded': 14,
              'ordinarySpellsOperational': 276, 'ordinarySpellsPending': 572,
              'bundleFile': archive.name, 'bundleBytes': archive.stat().st_size,
              'bundleSha256': sha(archive), 'payloadFiles': len(manifest),
              'currentFileHashes': {n: m['sha256'] for n, m in manifest.items()},
              'sent': False, 'newApprovals': 0, 'sourceInformationDeleted': 0,
              'runtimeChanged': False, 'cosmologyReviewed': False,
              'nextAction': 'After active onboarding and queued language decisions, check dependencies and dispatch finite source conference.'}
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'currentFileHashes'}, indent=2))

if __name__ == '__main__':
    main()
