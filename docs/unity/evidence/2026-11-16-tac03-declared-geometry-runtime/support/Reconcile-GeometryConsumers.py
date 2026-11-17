"""Retain a source disposition for every row of the approved lexical inventory."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[5]
PACKET = Path(__file__).resolve().parents[1]
BASE = 'fd422433bb83b72bed88e6e62c98fe2c901c659b'
SOURCE = '7261052ae4dec908f8c0ac38e0a2c5f4b831065b'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def main():
    inventory = PACKET.parent / '2026-11-16-tac03-declared-geometry/API_CONSUMERS.json'
    raw = inventory.read_bytes()
    data = json.loads(raw)
    changed = set(git('diff', '--name-only', BASE, SOURCE, '--', 'engine').decode().splitlines())
    sources = {}
    for group in data['searches'].values():
        for row in group['rows']:
            path = row['path']
            if path not in sources:
                before = git('show', BASE + ':' + path)
                current = git('show', SOURCE + ':' + path)
                assert current == (ROOT / path).read_bytes(), path
                sources[path] = dict(before=before.decode('utf-8-sig').splitlines(),
                    currentBytes=len(current), currentSha256=hashlib.sha256(current).hexdigest(),
                    currentGitBlob=git('rev-parse', SOURCE + ':' + path).decode().strip())
            for hit in row['hits']:
                # The approved inventory stores line.strip(), not source indentation.
                assert sources[path]['before'][hit['line'] - 1].strip() == hit['text'], (path, hit['line'])

    notes = {
        'SharedConnectedExplorationObservation.cs': 'Existing parent configuration runs before EnableDeclaredGeometry replaces the observation fixture and wraps the final fingerprint. Its inherited (2,1) occlusion and search/hide identities remain deliberate bootstrap requirements.',
        'SharedWorldDefinitions.cs': 'Fixed actor/worksite constructor restrictions remain for the old worldConfiguration factory, which is not selected by declared geometry. WorldSpatialQueries itself takes positions, map predicates and corner policy as arguments and remains shared.',
        'TacticalCombatFixture.cs': 'Legacy third-actor and terrain constructors retain their original fixed-map bounds. The selected Bishop composition has no additional actor declaration and an empty legacy terrain table; declared terrain resides in the appended trusted declaration.',
        'FoundationLab.cs': 'The original fixed-grid Unity demonstration is deferred and is not a host of the declared-geometry C# composition.',
        'TestOnlyPolicy.cs': 'The original synthetic fixed floor remains the explicit legacy branch of SharedDeclaredGeometry.SupportsAnchorAt. Selected declared geometry never falls back to it.',
        'ObservationGeometry.cs': 'ObservationFixture initialization/validation uses its instance Width, Height and Cells; EnableDeclaredGeometry supplies the new immutable fixture before genesis. Runtime support, rays, exact positions and breakpoints use canonical snapshot fields.',
        'ObservationRecords.cs': 'Existing bounded map/actor/cell validation and exact spatial queries already use the canonical observation dimensions and cells. The stricter selected layout is checked separately by DeclaredGeometryProfile.',
        'ObservationCodec.cs': 'The inherited observation map encoding remains authoritative and unchanged. The new envelope appends its trusted binding instead of storing a competing map.',
        'SharedMining.cs': 'Assistant placement now uses the common support adapter, removing its separate hardcoded <5 bounds. Existing cardinal worksite metrics and mining profile admission remain unchanged; this does not claim new connected mining gameplay.',
        'SharedLaterDefenderDecision.cs': 'Known static-floor support now uses the common adapter. Existing observed-occupancy checks, neighbor/corner rules, deterministic ranking and legal fallback remain; no full-state hidden-occupancy pathfinding is added.',
        'SharedWorldCommandQueries.cs': 'Ordinary support uses the shared adapter; existing position/occupancy and five-foot metrics remain. Declared-profile tactical discovery emits absolute destinations and run/begin/resume queries use the same read-only Dash admission as payment.',
        'TacticalMovementPolicy.cs': 'Tactical support and destination terrain use the shared adapter; actual movement expenditure, corner policy, occupancy, OA/Press and parent continuation retain their existing procedures.',
        'TestOnlySharedWorldPolicy.cs': 'Ordinary CostPerFoot uses shared destination terrain and existing crawl costs. Run payment and query assessment share admission while preserving paid-interval reuse and actual Strain lock expiry.',
        'ConnectedExplorationObservation.cs': 'Selected declared layouts use exact DeclaredGeometryProfile.HasExpectedLayout; all old layouts retain their original 5x5 validation. Existing selection continues through the inherited profile chain.',
        'ConnectedExpeditionSession.cs': 'A fresh explicit declared-geometry factory composes Bishop before initialization. The public host admits only its bounded existing movement commands with actor/payload checks; inherited spell, advancement and stage gates remain.',
        'VerifiedSharedWorldCheckpoint.cs': 'Verified replay selects envelope113 only for the declared composition and retains all predecessor schema selections and command-history verification.',
        'BishopEntryRecords.cs': 'SelectedFingerprint explicitly recognizes the declared profile while preserving the Bishop prefix. Grants, earned advancement and source ability records retain their existing validation and authority.',
        'SharedBishopEntry.cs': 'The existing Bishop declaration and parent fingerprint are installed before declared geometry. Runtime grants, advancement and abilities continue to require actual inherited Bishop records; geometry supplies no additional grants.',
        'Simulation.cs': 'Adds explicit113 selection, copies the immutable declaration and validates it. Canonical observation map cloning and existing inherited validators remain.',
        'SnapshotCodec.cs': 'Explicit113 preserves the accepted base90 and all112 inherited components, then appends marker18 and the declaration. Previous wire branches remain exact; no implicit migration is introduced.',
        'TestOnlyFillingPolicy.cs': 'The matched prefix check belongs to the separate legacy inventory filling policy, not the selected shared-world declared-geometry policy.',
        'FleshWardenRecords.cs': 'The matched selector remains exclusive to its old Flesh Warden fingerprint and requires its old mutation/Warrior qualification; declared geometry does not select this profile.',
        'ShortRestRecord.cs': 'This old Short Rest selector admits only its own fingerprint or Flesh Warden. Its validator continues rejecting records under other profiles; it is not promoted by geometry.',
        'ConsumeDecayRecord.cs': 'The matched old consumption/decay selector retains its own fingerprint and Short Rest chain. Declared geometry does not broaden it.',
        'WoundTreatmentRecord.cs': 'The matched legacy treatment selector retains its own fingerprint and consumption/decay chain. Shared treatment APIs elsewhere are not evidence that this old envelope is selected.',
    }
    exclusions = {
        'SharedExpeditionCampUse.cs': 'camp-site',
        'SharedExpeditionRouteTravel.cs': 'general-route',
        'SharedHuntingTrap.cs': 'hunting-trap',
        'SharedOverwatchExecution.cs': 'Overwatch-execution',
    }
    bootstrap = {'SharedConnectedBloodSpecimen.cs', 'SharedConnectedFormulaResearch.cs',
                 'SharedConnectedRecipe4Batch.cs', 'SharedConnectedVial.cs'}
    results = {}
    for name, group in data['searches'].items():
        rows = []
        for original in group['rows']:
            path = original['path']; file = Path(path).name
            disposition = 'changed_shared' if path in changed else 'existing_shared'
            if file in exclusions:
                reason = ('Fixed-floor calls now use the common adapter with the old observation behavior preserved. '
                    + exclusions[file] + ' configuration/grants/records and internal dispatch remain unavailable in this selected composition, '
                    'as checked at genuine genesis and r327 by Audit-GeometryBoundaries. Legacy full-command coverage remains required; no newly played procedure is claimed.')
            elif file in notes:
                reason = notes[file]
            elif name == 'spatial-consumers':
                reason = ('The listed calls already take actual snapshot positions, supplied cells, support predicates, '
                    'distances or canonical observation queries. They retain their existing metric, actor authority and profile admission. '
                    'This shared-call disposition does not claim every procedure was newly played beyond x4.')
            elif name == 'explicit-map-bounds':
                reason = ('The listed validation/query/record code already reads canonical observation dimensions or supplied positions. '
                    'Its source and existing admission remain unchanged; the selected trusted layout is validated centrally.')
            elif name == 'profile-save-gates' and file in bootstrap:
                reason = ('Matched configuration-prefix checks run while assembling the inherited parent before declared-geometry wrapping. '
                    'Runtime connected selection/stage checks keep their shared selector chain; no old factory accepts arbitrary new fingerprints.')
            elif name == 'profile-save-gates':
                reason = ('Existing source IDs, grants, advancement records, selection chains and validators remain unchanged. '
                    'BishopProfile.SelectedFingerprint centralizes recognition of113; connected layout and wire recognition change only in their explicit shared gates. '
                    'This disposition preserves each original predicate and does not declare all old profiles selected.')
            else:
                raise AssertionError(('Missing reviewed disposition', name, path))
            if file in {'FoundationLab.cs', 'TestOnlyPolicy.cs', 'TestOnlyFillingPolicy.cs', 'FleshWardenRecords.cs',
                        'ShortRestRecord.cs', 'ConsumeDecayRecord.cs', 'WoundTreatmentRecord.cs', 'TacticalCombatFixture.cs'}:
                disposition = 'legacy_profile_or_host_only'
            row = dict(path=path, disposition=disposition, explanation=reason, originalHits=original['hits'])
            row.update({k:v for k,v in sources[path].items() if k != 'before'})
            rows.append(row)
        results[name] = dict(files=len(rows), matchedLines=sum(len(r['originalHits']) for r in rows), rows=rows)
    report = dict(status='PASS_SOURCE_INVENTORY_RECONCILIATION', sourceCommit=SOURCE, inventorySourceCommit=BASE,
        inventorySha256=hashlib.sha256(raw).hexdigest(), uniqueFiles=len(sources),
        scope='Source trace for every approved lexical row, with semantic boundary notes. Does not replace execution, prove complete call-graph coverage, qualify all procedures beyond x4 or accept the module.',
        semanticBoundaryEvidence='qualification-checkpoint/RETENTION.json: exclusions/genesis, exclusions/continued and retained execution source bytes',
        supplementalSource='SharedDeclaredGeometry.cs, DeclaredGeometryRecords.cs, DeclaredGeometryCodec.cs and the public PowerShell host are additionally bound by compiled-source and execution-source records.',
        searches=results)
    output = PACKET / 'CONSUMER_RECONCILIATION.json'
    output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k != 'searches'}))
    print(json.dumps({k:{'files':v['files'],'matchedLines':v['matchedLines']} for k,v in results.items()}))


if __name__ == '__main__':
    main()
