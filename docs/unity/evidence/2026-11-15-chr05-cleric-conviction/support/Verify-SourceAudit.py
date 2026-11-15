"""Pin CHR05 Conviction sources and audit selected-build prerequisite boundaries.

This is source inspection only; it runs no engine, compilation or gameplay tests.
"""
from pathlib import Path
import hashlib
import json
import subprocess

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[3]
BASELINE = '9288439878476b8d130894d3af28302d7d535e86'
ENGINE = '0e5928bddd5abce47c16ff86172f5613423a2460'
SOURCE = '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
CORE = 'engine/com.decennium.foundation/Runtime/Core/'
MODEL = 'engine/com.decennium.foundation/Laboratory/Model/'
REVIEW = 'DescentReviewChanges/ReviewBible/'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def read(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def save(name, value):
    (PACKET / name).write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8'))

def main():
    authority = ['CANON_MANIFEST.md', 'docs/canon/CANON_MANIFEST.json', 'docs/canon/REPOSITORY_PROMOTION.md',
        'docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md', 'docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json',
        'docs/unity/evidence/2026-11-15-tac08-cleric-casting/GPT_FINAL_REVIEW.json',
        'docs/unity/evidence/2026-11-15-tac08-cleric-casting/APPROVED_CASTING_CONTRACT.md',
        'docs/unity/evidence/2026-11-15-chr03-cleric-settlement/SETTLEMENT_CONTRACT.md',
        'docs/unity/evidence/2026-11-15-chr03-cleric-settlement/GPT_FINAL_REVIEW.md',
        'docs/unity/evidence/2026-11-14-mgt03-short-rest/SOURCE_API_CONTRACT.md',
        'docs/unity/evidence/2026-11-14-mgt03-short-rest/GPT_FINAL_REVIEW.md',
        'docs/unity/evidence/2026-11-14-mgt03-rest-calendar/GPT_FINAL_REVIEW.md']
    sources = [REVIEW + x for x in ['data/public/class_playtests/cleric.json',
        'data/playtest/class_sources/cleric.json', 'data/playtest/class_sources/supplements.json',
        'docs/mechanics/classes/cleric.md', 'docs/mechanics/CLASS_PLAYTEST_RULES.md',
        'docs/mechanics/GAMEPLAY_LOOP_CANON.md', 'docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md',
        'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md']]
    sources += ['docs/reference/Player_Rulebook_v6_source_text.txt', 'src/data/class-core-mechanics.js']
    engine = [CORE + x for x in ['ResonanceRecords.cs', 'ClericSettlementRecords.cs', 'ClericSettlementValidation.cs',
        'ExpeditionProvisioningRecords.cs', 'ExpeditionStrainRecoveryRecords.cs', 'SpellCastingProfile.cs']]
    engine += [MODEL + x for x in ['SharedResonance.cs', 'SharedClericSettlement.cs', 'SharedSpellCasting.cs',
        'SharedRestDebt.cs', 'SharedStrainRecovery.cs', 'SharedShortRest.cs', 'SharedWorldCommandQueries.cs',
        'TestOnlySharedWorldPolicy.cs', 'ConnectedExpeditionSession.cs', 'ConnectedExpeditionView.cs',
        'ClassAdvancementOptionCatalog.cs', 'ClassAdvancementScheduleCatalog.cs']]
    engine += ['engine/com.decennium.foundation/Runtime/Persistence/ClericSettlementCodec.cs',
        'engine/com.decennium.foundation/Tests/EditMode/ConnectedClericSettlementCases.cs',
        'engine/com.decennium.foundation/Tests/EditMode/ConnectedClericRpCases.cs']
    bindings = []
    for paths, revision, role in [(authority, BASELINE, 'authority-or-accepted-boundary'),
                                  (sources, SOURCE, 'historical-source-not-release-promotion'),
                                  (engine, ENGINE, 'accepted-engine-source-inspection')]:
        for path in paths:
            blob = git('show', revision + ':' + path)
            checkout = (ROOT / path).read_bytes()
            exact = blob == checkout
            assert exact or blob.replace(b'\r\n', b'\n') == checkout.replace(b'\r\n', b'\n'), path
            bindings.append({'path': path, 'revision': revision, 'role': role,
                'gitBlob': git('rev-parse', revision + ':' + path).decode().strip(),
                'bytes': len(blob), 'sha256': sha(blob), 'checkoutBytes': len(checkout),
                'checkoutSha256': sha(checkout), 'checkoutRelation': 'exact' if exact else 'CRLF-only; preserved'})
    assert len(bindings) == len({r['path'] for r in bindings})
    checks = []
    def require(value, name):
        assert value, name
        checks.append(name)
    cleric = json.loads(read(REVIEW + 'data/public/class_playtests/cleric.json'))
    cards = {c['id']: c for c in cleric['cards']}
    initial = ['cleric.base.consecrate', 'cleric.base.consecrated-ground', 'cleric.base.fervent-ritualist', 'cleric.base.healing-rite']
    selected = ['cleric.base.conviction-pool', 'cleric.base.judging-light']
    automatic = ['cleric.base.invocation-attunement', 'cleric.base.radiance.radiance']
    owned = initial + selected + automatic
    require(all(x in cards for x in owned), 'All eight selected/automatic cards bind to actual source records')
    require(cleric['status'] == 'provisional-card-draft-not-balance-approved', 'Operational class cards retain provisional status')
    require(cleric['sourceExtractSha256'] == sha((ROOT / 'docs/reference/Player_Rulebook_v6_source_text.txt').read_bytes()), 'Original rulebook extract hash agrees')
    require(all('Conviction' not in cards[x]['cost'] for x in owned), 'Preserved selected build has no printed Conviction spender')
    generators = ['cleric.base.sacred-chant', 'cleric.arch.sermon-of-purpose', 'cleric.hero.priest.doctrine-shield',
        'cleric.hero.cultist.dark-conviction', 'cleric.hero.cultist.blood-sacrifice']
    require(all(x in cards and x not in owned for x in generators), 'Named generator cards remain unowned; Sermon only modifies unowned Chant')
    require(cards['cleric.base.healing-rite']['cost'] == '2 RP', 'Healing Rite is an RP-only spender')
    require(cards['cleric.arch.divine-invocation']['minimumClassLevel'] == 3
        and cards['cleric.arch.divine-invocation']['acquisition'] == 'selection'
        and cards['cleric.arch.divine-invocation']['cost'] == '2 Conviction + 3 RP', 'Divine Invocation requires a selected Cleric3 Arch grant and finite dual payment')
    schedule = next(x for x in cleric['schedule'] if x['classLevel'] == 3)
    require(schedule['choose'] == 2 and schedule['bands'] == ['Arch'] and schedule['minimumActives'] == 1,
        'Cleric3 requires two Arch choices, at least one active; it cannot silently select Base Chant/Smite')
    capacity = read(CORE + 'ClericSettlementRecords.cs')
    require('public int? Current => null;' in capacity and 'public bool CurrentAvailable => false;' in capacity,
        'Accepted capacity record has unavailable current, not numerical zero or full')
    require('public int Maximum => PoolAcquiredRevision == 0 ? 3 : 5;' in capacity,
        'Current selected capacity3 to5 is grant-derived and does not fund a balance')
    codec = read('engine/com.decennium.foundation/Runtime/Persistence/ClericSettlementCodec.cs')
    require('r.ReadInt32() != s.ConvictionCapacity.Maximum || SnapshotCodec.ReadBool(r)' in codec
        and 'fabricated balance' in codec, 'Existing settlement codec rejects fabricated numeric availability')
    settlement = read(MODEL + 'SharedClericSettlement.cs')
    require('ClassAdvancementScheduleCatalog.Get("Cleric",2)' in settlement
        and 's.CharacterAdvancements.Any(x => x.ActorId == c.Actor)' in settlement,
        'Selected advancement is one earned level1 to2 transaction, not an available level3 path')
    session = read(MODEL + 'ConnectedExpeditionSession.cs')
    require('CommandKind.BeginRest' not in session and 'CommandKind.ScheduleRestWatch' not in session
        and '.EnableRestDebt(' not in session and '.EnableExpeditionStrainRecovery(' not in session,
        'Current public session does not expose or compose the older full Rest Watch/beneficial Long Rest path')
    require('s.ConnectedClericRp && ShortRestBerth.IsCommand(c.Kind)' in read(MODEL + 'SharedWorldCommandQueries.cs')
        and 'ClassRecoveryUnsupported' in read(MODEL + 'SharedWorldCommandQueries.cs')
        and 'ClassRecoveryUnsupported' in read(MODEL + 'TestOnlySharedWorldPolicy.cs'),
        'Cleric Short Rest recovery is explicitly rejected at query and execution')
    require('private const long RestWatchSeconds = 8 * 60 * 60;' in read(MODEL + 'SharedRestDebt.cs')
        and 'last.Value.AddSeconds(24 * 60 * 60)' in read(MODEL + 'SharedStrainRecovery.cs'),
        'Reusable older Rest Watch and beneficial-rest timing primitives exist without selected-session recovery authority')
    require('A completed short rest restores 1 spent Conviction' in cleric['engine'][1]
        and 'A completed long rest restores all Conviction' in cleric['engine'][1],
        'Source distinguishes spent-Conviction recovery and authoritative full Long Rest restoration')
    require('Only explicit features generate Conviction' in cleric['engine'][2]
        and 'The expenditure must actually occur' in cleric['engine'][4],
        'Explicit producers and actual regular-turn spending are necessary for Conviction generation/venting')
    rules = json.loads(read('docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json'))
    items = {x['id']: x for x in rules['workItems']}
    require(items['CHR-05']['dependencies'] == ['CHR-03', 'TAC-02', 'TAC-05', 'TAC-08'], 'Approved CHR05 dependency edges preserved')
    require(items['CHR-03']['dependencies'] == ['CHR-02'] and items['MGT-03']['dependencies'] == ['MGT-02', 'TAC-05'],
        'Candidate prerequisite work remains within existing mapped CHR03/MGT03 edges')
    require(not git('diff', '--name-only', ENGINE, '--', 'engine').strip(), 'Accepted engine source remains unchanged')
    acceptance = json.loads(read('docs/unity/evidence/2026-11-15-tac08-cleric-casting/GPT_FINAL_REVIEW.json'))
    require(acceptance['responseId'] == '4380847f-3bdc-5003-b5a1-1803a4fed501', 'Actual TAC08 acceptance authorizes only next bounded contract review')
    binding_doc = {'baseline': BASELINE, 'acceptedEngine': ENGINE, 'sourceRevision': SOURCE,
        'scope': 'Source/API prerequisite findings only; no runtime implementation or contract approval.', 'sources': bindings}
    extracts = {'classSource': REVIEW + 'data/public/class_playtests/cleric.json', 'sourceRevision': SOURCE,
        'sourceStatus': cleric['status'], 'engine': cleric['engine'], 'initialSelectedCards': initial,
        'earnedSelectedCards': selected, 'earnedAutomaticCards': automatic,
        'selectedBuildRecords': [cards[x] for x in owned],
        'unownedRelevantRecords': [cards[x] for x in generators + ['cleric.base.divine-smite', 'cleric.arch.divine-invocation', 'cleric.arch.sacrament']],
        'nextClassSchedule': schedule, 'dependencyNodes': [items[x] for x in ['CHR-03', 'CHR-05', 'MGT-03']]}
    save('SOURCE_BINDINGS.json', binding_doc)
    save('SOURCE_EXTRACTS.json', extracts)
    save('SOURCE_AUDIT.json', {'status': 'PASS', 'meaning': 'SOURCE_BINDINGS_AND_PREREQUISITE_AUDIT_ONLY',
        'baseline': BASELINE, 'acceptedEngine': ENGINE, 'sourceFiles': len(bindings), 'checks': checks,
        'sourceBindingsSha256': sha((PACKET / 'SOURCE_BINDINGS.json').read_bytes()),
        'sourceExtractsSha256': sha((PACKET / 'SOURCE_EXTRACTS.json').read_bytes()),
        'engineChanged': False, 'compilation': 'NOT RUN; no engine changes', 'runtimeTests': 'NOT RUN; source-only audit',
        'latestAcceptedRegression': {'passed': 1551, 'failed': 0, 'evidenceCommit': '9d578350f1de1285ea2133b0e8a334191de4cb46'},
        'contractApproval': 'PENDING', 'runtimeImplementation': 'NOT AUTHORIZED', 'unityIntegration': 'DEFERRED'})
    print(f'PASS: {len(bindings)} pinned sources; {len(checks)} source/API checks; engine unchanged; no compilation/runtime execution claimed.')

if __name__ == '__main__':
    main()
