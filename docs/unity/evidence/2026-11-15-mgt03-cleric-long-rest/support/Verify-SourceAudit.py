"""Reproduce the Long Rest source/API audit. This runs no gameplay or C# tests."""
from pathlib import Path
import hashlib
import io
import json
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[3]
BASELINE = 'e3c6b7083d2d9393053d59fa02d5159103e2c7d3'
ENGINE = '0e5928bddd5abce47c16ff86172f5613423a2460'
SOURCE = '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
MODEL = 'engine/com.decennium.foundation/Laboratory/Model/'
CORE = 'engine/com.decennium.foundation/Runtime/Core/'
REVIEW = 'DescentReviewChanges/ReviewBible/'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write(name, value):
    (PACKET / name).write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

def main():
    authority = ['CANON_MANIFEST.md', 'docs/canon/CANON_MANIFEST.json', 'docs/canon/REPOSITORY_PROMOTION.md',
        'docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md', 'docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json',
        'docs/unity/evidence/2026-11-15-chr05-cleric-conviction/GPT_DEPENDENCY_REVIEW.json',
        'docs/unity/evidence/2026-11-15-chr05-cleric-conviction/SOURCE_API_FINDINGS.md',
        'docs/unity/evidence/2026-11-15-tac08-cleric-casting/GPT_FINAL_REVIEW.json',
        'docs/unity/evidence/2026-11-15-tac08-cleric-casting/APPROVED_CASTING_CONTRACT.md',
        'docs/unity/evidence/2026-11-15-chr03-cleric-settlement/SETTLEMENT_CONTRACT.md',
        'docs/unity/evidence/2026-11-14-mgt03-short-rest/SOURCE_API_CONTRACT.md',
        'docs/unity/evidence/2026-11-14-mgt03-rest-calendar/GPT_FINAL_REVIEW.md',
        'docs/unity/DAILY_PROVISIONING_RULE_DECISIONS.md',
        'docs/unity/evidence/2026-11-08-rest-debt/GPT_REVIEW.md',
        'docs/unity/evidence/2026-11-08-strain-recovery/GPT_REVIEW.md']
    sources = [REVIEW + x for x in ['data/public/class_playtests/cleric.json',
        'data/playtest/strain_bindings.json', 'docs/mechanics/CLASS_PLAYTEST_RULES.md',
        'docs/mechanics/GAMEPLAY_LOOP_CANON.md', 'docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md',
        'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md', 'docs/mechanics/STRAIN_PLAYTEST.md']]
    sources += ['docs/reference/Player_Rulebook_v6_source_text.txt']
    books = ['books/player/Decennium_Descent_Player_Rulebook_v6.docx',
        'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx',
        'books/director/Decennium_Descent_Core_Systems_Bible_v1_Full_Director.docx']
    engine = [MODEL + x for x in ['ConnectedExpeditionSession.cs', 'ConnectedExpeditionView.cs',
        'TestOnlySharedWorldPolicy.cs', 'SharedDailyProvisioning.cs', 'SharedRestDebt.cs',
        'SharedStrainRecovery.cs', 'SharedShortRest.cs', 'SharedResonance.cs', 'SharedClericSettlement.cs',
        'SharedSpellCasting.cs', 'SharedCharterAttempt.cs', 'SharedWorldCommandQueries.cs', 'ActorLifeRules.cs']]
    engine += [CORE + x for x in ['ShortRestRecord.cs', 'ActorLifeRecords.cs',
        'ClericSettlementRecords.cs', 'ClericSettlementValidation.cs', 'ResonanceRecords.cs',
        'ExpeditionProvisioningRecords.cs', 'ExpeditionStrainRecoveryRecords.cs', 'SpellCastingProfile.cs',
        'Simulation.cs']]
    engine += ['engine/com.decennium.foundation/Runtime/Persistence/' + x for x in
        ['SnapshotCodec.cs', 'ClericSettlementCodec.cs', 'ShortRestCodec.cs', 'ExpeditionProvisioningCodec.cs']]
    engine += ['engine/com.decennium.foundation/Tests/EditMode/' + x for x in
        ['ConnectedClericSettlementCases.cs', 'ConnectedShortRestCases.cs', 'SpellCastingCases.cs']]
    bindings = []
    blobs = {}
    for paths, revision, role in [(authority, BASELINE, 'authority-or-accepted-boundary'),
            (sources + books, SOURCE, 'historical-source-not-release-promotion'),
            (engine, ENGINE, 'accepted-engine-inspection')]:
        for path in paths:
            data = git('show', revision + ':' + path)
            checkout = (ROOT / path).read_bytes()
            exact = data == checkout
            assert exact or data.replace(b'\r\n', b'\n') == checkout.replace(b'\r\n', b'\n'), path
            blobs[path] = data
            bindings.append({'path': path, 'revision': revision, 'role': role,
                'gitBlob': git('rev-parse', revision + ':' + path).decode().strip(),
                'bytes': len(data), 'sha256': sha(data), 'checkoutBytes': len(checkout),
                'checkoutSha256': sha(checkout), 'checkoutRelation': 'exact' if exact else 'CRLF-only; preserved'})
    assert len(bindings) == len(set(x['path'] for x in bindings))
    def read(path):
        return blobs[path].decode('utf-8-sig')
    checks = []
    def require(condition, name):
        assert condition, name
        checks.append(name)
    session = read(MODEL + 'ConnectedExpeditionSession.cs')
    require(all(x not in session for x in ['.EnableDailyProvisioning(', '.EnableRestDebt(', '.EnableExpeditionStrainRecovery(']),
        'Selected public session does not compose daily provisioning, Rest Debt or secure-rest recovery')
    daily = read(MODEL + 'SharedDailyProvisioning.cs')
    require('CanonicalDayOrigin => default;' in daily and 'new RuleQuantity(2)' in daily and 'new RuleQuantity(8)' in daily,
        'Older fixed provisioning profile binds origin0, two food pounds and eight water pints')
    require('DailyProvisioningRequiresCanonicalInitialProfile' in daily and 'DailyProvisioningProfileMissing' in daily,
        'Existing profile/schema gates prohibit simply attaching provisioning history to a public save')
    rest = read(MODEL + 'SharedRestDebt.cs')
    require('RestWatchSeconds = 8 * 60 * 60' in rest and 'default-slot=evening' in rest,
        'Older Rest Debt profile binds eight hours and default Evening Watch')
    require('RestSiteNotQualified' in rest and 'ActorNotAtRestSite' in rest and 'RestConflictsWithAssignedActivity' in rest,
        'Older Rest commands require qualified physical site and reject incompatible activity')
    recovery = read(MODEL + 'SharedStrainRecovery.cs')
    require('last.Value.AddSeconds(24 * 60 * 60)' in recovery and 'ExpeditionBeneficialRestRecord' in recovery,
        'Beneficial-rest cadence is recorded separately from actual Strain removal')
    require('ProvisioningBlockActive' in recovery and 'RestDebtOwedAt' in recovery and 'PointIds.Contains(c.Target' in recovery,
        'Secure recovery requires supply/debt gates and patient selection of an exact eligible point')
    short = read(CORE + 'ShortRestRecord.cs')
    require('HitDiceSpent => 0' in short and 'InitialBenefits = 2' in short and 'BenefitsUsed(Snapshot state)' in short,
        'Existing hero Short Rest is a zero-dice two-initial-benefit profile without a Long Rest reset')
    require('ClassRecoveryUnsupported' in read(MODEL + 'SharedWorldCommandQueries.cs'),
        'Selected Cleric Short Rest remains explicitly unsupported')
    capacity = read(CORE + 'ClericSettlementRecords.cs')
    require('Current => null' in capacity and 'CurrentAvailable => false' in capacity,
        'Accepted current Conviction is unavailable and must retain its historical meaning')
    require('CharacterHitDieRecord(c.Actor,2,"Cleric",8,false)' in read(MODEL + 'SharedClericSettlement.cs'),
        'Earned Cleric2 adds an unspent d8, not an expended die or recovery transaction')
    cleric = json.loads(read(REVIEW + 'data/public/class_playtests/cleric.json'))
    require(cleric['status'] == 'provisional-card-draft-not-balance-approved', 'Class source remains provisional')
    require('after a long rest you begin at your current maximum' in cleric['engine'][1], 'Actual Long Rest establishes maximum Conviction')
    require('It never fills gained capacity immediately' in cleric['engine'][11], 'Capacity acquisition is not funding')
    owned_ids = ['cleric.base.consecrate', 'cleric.base.consecrated-ground', 'cleric.base.fervent-ritualist',
        'cleric.base.healing-rite', 'cleric.base.conviction-pool', 'cleric.base.judging-light',
        'cleric.base.invocation-attunement', 'cleric.base.radiance.radiance']
    owned = [next(c for c in cleric['cards'] if c['id'] == i) for i in owned_ids]
    require(all('rest' not in c['frequency'].lower() for c in owned), 'Selected cards contain no per-rest use counter to fabricate')
    require('A long rest restores RP and clears Dissonance.' in read(REVIEW + 'docs/mechanics/CLASS_PLAYTEST_RULES.md'),
        'Long Rest RP restoration and Dissonance clearing are explicit')
    require('Refrain survives idle/weapon turns unless a class explicitly clears it.' in read(REVIEW + 'docs/mechanics/CLASS_PLAYTEST_RULES.md'),
        'There is no generic idle/weapon Refrain clear; rest contract must preserve sourced history')
    gameplay = read(REVIEW + 'docs/mechanics/GAMEPLAY_LOOP_CANON.md')
    require('Restore HP according to the Player Rulebook.' in gameplay and 'Recover half expended Hit Dice, rounded up.' in gameplay,
        'Gameplay delegates HP amount and explicitly uses half expended Hit Dice rounded up')
    core = read(REVIEW + 'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md')
    require('reduces the normal maximum number of Hit Dice recovered per long rest by one' in core
        and 'maximum HP - 1' in core, 'Core Wounds overlay owns Hit Dice restriction and Critical healing ceiling')
    require('An additional safe RestWatch inside the24h reward cap can discharge debt' in read(REVIEW + 'docs/mechanics/STRAIN_PLAYTEST.md'),
        'Safe debt clearance and benefit-ineligible rest remain distinct')
    prior = json.loads(read('docs/unity/evidence/2026-11-15-chr05-cleric-conviction/GPT_DEPENDENCY_REVIEW.json'))
    require(prior['responseId'] == '04e19c85-6b86-5529-9b34-edeb306fb1eb', 'Actual prerequisite review is bound, not inferred from a request')
    rule_map = json.loads(read('docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json'))
    nodes = {x['id']: x for x in rule_map['workItems']}
    require(nodes['MGT-03']['dependencies'] == ['MGT-02', 'TAC-05']
        and nodes['CHR-05']['dependencies'] == ['CHR-03', 'TAC-02', 'TAC-05', 'TAC-08'], 'Approved dependency edges unchanged')
    require(not git('diff', '--name-only', ENGINE, '--', 'engine').strip(), 'Accepted engine unchanged')

    # Every body paragraph includes those inside tables. Table rows are separately retained
    # to show adjacent cells; they intentionally duplicate their component paragraphs.
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    pattern = r'long[\s-]*rest|(?:rest.{0,110}(?:hit points?|\bhp\b|heal|recover)|(?:hit points?|\bhp\b|heal|recover).{0,110}rest)'
    rx = re.compile(pattern, re.I)
    book_search = []
    for path in books:
        with zipfile.ZipFile(io.BytesIO(blobs[path])) as z:
            document = ET.fromstring(z.read('word/document.xml'))
        paragraphs = [''.join(t.text or '' for t in p.findall('.//w:t', ns))
            for p in document.findall('.//w:body//w:p', ns)]
        rows = [' | '.join(''.join(t.text or '' for t in cell.findall('.//w:t', ns))
            for cell in row.findall('w:tc', ns)) for row in document.findall('.//w:body//w:tr', ns)]
        hits = [{'paragraph': i + 1, 'text': t} for i, t in enumerate(paragraphs) if rx.search(t)]
        row_hits = [{'tableRow': i + 1, 'text': t} for i, t in enumerate(rows) if rx.search(t)]
        book_search.append({'path': path, 'sha256': sha(blobs[path]), 'paragraphsSearched': len(paragraphs),
            'tableRowsSearched': len(rows), 'paragraphHits': hits, 'tableRowHits': row_hits})
    excerpts = []
    for path, start, end in [(REVIEW + 'docs/mechanics/GAMEPLAY_LOOP_CANON.md', 130, 157),
            (REVIEW + 'docs/mechanics/CLASS_PLAYTEST_RULES.md', 17, 49),
            (REVIEW + 'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md', 50, 68),
            (REVIEW + 'docs/mechanics/STRAIN_PLAYTEST.md', 82, 94),
            (REVIEW + 'docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md', 55, 81),
            ('docs/reference/Player_Rulebook_v6_source_text.txt', 8245, 8254),
            ('docs/reference/Player_Rulebook_v6_source_text.txt', 8283, 8289)]:
        lines = read(path).splitlines()
        excerpts.append({'path': path, 'firstLine': start, 'lastLine': end, 'lines': lines[start-1:end]})
    write('SOURCE_BINDINGS.json', {'baseline': BASELINE, 'acceptedEngine': ENGINE, 'sourceRevision': SOURCE, 'sources': bindings})
    write('SOURCE_EXTRACTS.json', {'excerpts': excerpts, 'clericEngine': cleric['engine'], 'ownedCards': owned,
        'dependencyNodes': [nodes[x] for x in ['MGT-03', 'CHR-03', 'CHR-05']]})
    write('HP_SOURCE_SEARCH.json', {'meaning': 'Bounded source search; manual interpretation is in the contract; no proof about every archive',
        'sourceRevision': SOURCE, 'pattern': pattern, 'bodyIncludesTableParagraphs': True, 'books': book_search})
    write('SOURCE_AUDIT.json', {'status': 'PASS', 'meaning': 'SOURCE_AND_API_INSPECTION_ONLY', 'sourceFiles': len(bindings),
        'checks': checks, 'acceptedEngine': ENGINE, 'engineChanged': False,
        'sourceBindingsSha256': sha((PACKET/'SOURCE_BINDINGS.json').read_bytes()),
        'sourceExtractsSha256': sha((PACKET/'SOURCE_EXTRACTS.json').read_bytes()),
        'hpSearchSha256': sha((PACKET/'HP_SOURCE_SEARCH.json').read_bytes()),
        'compilation': 'NOT RUN; unchanged engine', 'runtimeTests': 'NOT RUN; unchanged engine',
        'latestAcceptedRegression': {'passed': 1551, 'failed': 0, 'evidenceCommit': '9d578350f1de1285ea2133b0e8a334191de4cb46'},
        'contractApproval': 'PENDING', 'runtimeImplementation': 'NOT AUTHORIZED', 'unityIntegration': 'DEFERRED'})
    print(f'PASS: {len(bindings)} pinned files, {len(checks)} source/API checks, three complete DOCX body/table searches; engine unchanged.')

if __name__ == '__main__':
    main()
