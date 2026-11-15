"""Source/API proposal evidence only. Never reports runtime qualification or approval."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import re
import subprocess

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[3]
BASELINE = '3ca48580c6f2dfeb602d6e83b2ca7dd369d9d5fd'
ENGINE = '34229ec6f19c9569dd35fd7b6013b99f37759c85'
SOURCE = '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
MODEL = 'engine/com.decennium.foundation/Laboratory/Model/'
CORE = 'engine/com.decennium.foundation/Runtime/Core/'
EXTRA_MODEL = (
    'TestOnlySharedWorldPolicy.cs', 'SharedWorldCombatPolicy.cs',
    'SharedPortableEquipment.cs', 'SharedObservationActions.cs',
    'SharedConnectedExplorationObservation.cs', 'SharedExplorationSearch.cs',
    'SharedExplorationHide.cs', 'ObservationRules.cs', 'ObservationGeometry.cs',
    'SharedCompanionStabilization.cs', 'PlaytestLife.cs', 'PlaytestDamageDice.cs',
    'ActorLifeRules.cs', 'TestOnlyClubAttackPolicy.cs', 'SharedWorldRangedCombat.cs',
    'SharedOverwatchExecution.cs', 'SharedReadyAction.cs', 'SharedPeriodicRider.cs',
    'SharedHuntingTrap.cs', 'SharedHarvest.cs', 'SharedMining.cs',
    'SharedCraftingConsequences.cs', 'SharedFrightened.cs', 'WaterFilling.cs',
    'TestOnlyFillingPolicy.cs', 'SharedNextCharterPlan.cs', 'SharedReinforcement.cs', 'CharacterRuleFacts.cs',
)
EXTRA_CORE = ('LaterEncounterRecords.cs', 'NextCharterPlanRecords.cs')
EXTRA_DECISIONS = ('INVENTORY_RULE_DECISIONS.md', 'VESSEL_FILLING_RULE_DECISIONS.md',
                   'CONDITION_LIFECYCLE_RULE_DECISIONS.md', 'CONDITION_COMBAT_RULE_DECISIONS.md',
                   'SHARED_WORLD_RULE_DECISIONS.md', 'CONNECTED_COMBAT_RULE_DECISIONS.md')

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical(value):
    return sha(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8'))

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def require(value, message):
    if not value:
        raise ValueError(message)

def bind():
    destination = PACKET / 'CONTRACT_BINDINGS.json'
    require(not destination.exists(), 'Do not overwrite frozen proposal source bindings')
    paths = [(MODEL + x, ENGINE, 'accepted-runtime-integration-point') for x in EXTRA_MODEL]
    paths += [(CORE + x, ENGINE, 'accepted-runtime-integration-point') for x in EXTRA_CORE]
    paths += [('docs/unity/' + x, BASELINE, 'accepted-policy-preserve-own-scope') for x in EXTRA_DECISIONS]
    paths += [('DescentReviewChanges/ReviewBible/docs/mechanics/CORE_RESOLUTION_PLAYTEST.md', SOURCE,
               'pinned-provisional-life-and-check-source')]
    initial = load(PACKET / 'SOURCE_BINDINGS.json')
    require(not set(x[0] for x in paths) & {x['path'] for x in initial['sources']}, 'Duplicate initial binding')
    rows = []
    for path, revision, role in paths:
        ref = revision + ':' + path
        data = git('show', ref)
        working = (ROOT / path).read_bytes()
        require(data == working, 'Additional inspected checkout differs: ' + path)
        rows.append(dict(path=path, revision=revision, role=role,
                         gitBlob=git('rev-parse', ref).decode().strip(), bytes=len(data), sha256=sha(data),
                         workingBytes=len(working), workingSha256=sha(working), workingTreeComparison='EXACT'))
    value = dict(status='PROPOSED_FOR_ACTUAL_REVIEW_NOT_IMPLEMENTATION_APPROVAL', baseline=BASELINE,
                 engineSource=ENGINE, sourceRevision=SOURCE, initialBindings='SOURCE_BINDINGS.json',
                 initialBindingsSha256=sha((PACKET / 'SOURCE_BINDINGS.json').read_bytes()), sources=rows)
    destination.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')

def verify():
    initial = load(PACKET / 'SOURCE_BINDINGS.json')
    supplement = load(PACKET / 'CONTRACT_BINDINGS.json')
    require(supplement['initialBindingsSha256'] == sha((PACKET / 'SOURCE_BINDINGS.json').read_bytes()),
            'Historical initial binding changed')
    rows = initial['sources'] + supplement['sources']
    require(len(rows) == len({x['path'] for x in rows}), 'Duplicate source binding')
    data_by_path = {}
    for row in rows:
        ref = row['revision'] + ':' + row['path']
        data = git('show', ref)
        require(len(data) == row['bytes'] and sha(data) == row['sha256']
                and git('rev-parse', ref).decode().strip() == row['gitBlob'], 'Pinned blob differs: ' + ref)
        working = (ROOT / row['path']).read_bytes()
        require(len(working) == row['workingBytes'] and sha(working) == row['workingSha256'],
                'Inspected checkout differs: ' + row['path'])
        require(data == working or row['workingTreeComparison'] == 'CRLF_ONLY'
                and row['path'] == 'docs/canon/CANON_MANIFEST.json'
                and data.replace(b'\r\n', b'\n') == working.replace(b'\r\n', b'\n'),
                'Unrecorded working-tree difference')
        data_by_path[row['path']] = data
    selected = load(PACKET / 'SPELL_CANDIDATES.json')
    catalog = json.loads(data_by_path[selected['catalogPath']].decode('utf-8-sig'))
    authored = json.loads(data_by_path['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'].decode('utf-8-sig'))
    authored_by_id = {x['id']: x for x in authored['entries']}
    require(len(selected['candidates']) == 6, 'Selected source inventory changed')
    for row in selected['candidates']:
        card = catalog['spells'][int(row['wholeCardPointer'].split('/')[-1])]
        require(card['id'] == row['id'] and canonical(card) == row['wholeCardSha256']
                and canonical(card['operational']) == row['procedureSha256']
                and card['operational'] == row['operationalEvidence']
                and card['classAccess']['Cleric'] == row['clericAccess']
                and canonical(authored_by_id[row['id']]) == row['authoredReviewEntrySha256'],
                'Exact operational procedure differs: ' + row['id'])
    anchors = {
        CORE + 'SpellRepertoireRecords.cs': [b'public bool CastingSupported => false;', b'OrdinarySpellcastingUnsupported'],
        CORE + 'LaterEncounterRecords.cs': [b'public static class WorldTiming', b'ForActor(Snapshot state, string actor)'],
        MODEL + 'ConditionCombatPolicy.cs': [b'This explicitly selected fixture admits no concentration.'],
        MODEL + 'TestOnlySharedWorldPolicy.cs': [b'private static int AvailableHands', b'private string AdvanceTo'],
        MODEL + 'TestOnlyClubAttackPolicy.cs': [b'internal static void ApplyLife'],
        MODEL + 'SharedCompanionStabilization.cs': [b'PlaytestLife.StabilizeAt', b'DiceStream.Draw(randomAfter, 4)'],
        MODEL + 'WaterFilling.cs': [b'WaterVesselProfile.OrdinaryFlask?new RuleQuantity(1)'],
        MODEL + 'TestOnlyFillingPolicy.cs': [b'Hazards, contamination and tactical filling remain unsupported.'],
    }
    for path, required in anchors.items():
        require(all(x in data_by_path[path] for x in required), 'Claimed baseline API differs: ' + path)
    rule_map = json.loads(data_by_path['docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json'].decode('utf-8-sig'))
    dependencies = {x['id']: x['dependencies'] for x in rule_map['workItems'] if x['id'] in ('TAC-08', 'CHR-05')}
    require(set(dependencies['TAC-08']) == {'TAC-02', 'TAC-05', 'TAC-07'}
            and set(dependencies['CHR-05']) == {'CHR-03', 'TAC-02', 'TAC-05', 'TAC-08'}, 'Historical dependency order differs')
    require(not git('diff', BASELINE, '--', 'engine'), 'Engine changed before actual contract approval')
    contract = (PACKET / 'CASTING_CONTRACT.md').read_bytes()
    policies = re.findall(rb'\*\*P([0-9]+)', contract)
    require(set(policies) == {str(x).encode() for x in range(1, 11)} and len(policies) == 10,
            'Explicit proposal decision inventory differs')
    retained = ['CASTING_CONTRACT.md', 'CONTRACT_BINDINGS.json', 'SOURCE_BINDINGS.json', 'SPELL_CANDIDATES.json',
                'SOURCE_AUDIT.json', 'support/Verify-SourceAudit.py', 'support/Verify-Contract.py']
    result = dict(status='PASS_SOURCE_API_PROPOSAL_BINDINGS_ONLY', atUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  baseline=BASELINE, engineSource=ENGINE, sourceFiles=len(rows), initialSourceFiles=len(initial['sources']),
                  additionalSourceFiles=len(supplement['sources']), exactProcedures=6, explicitPoliciesRequiringActualReview=10,
                  dependencies=dependencies, baselineApiAssertions=sum(map(len, anchors.values())), engineUnchanged=True,
                  contractApproval='NOT_YET_REVIEWED', compilation='NOT_RUN_DOCUMENTATION_ONLY',
                  runtimeTests='NOT_RUN_DOCUMENTATION_ONLY', connectedCasting='NOT_IMPLEMENTED',
                  unity='DEFERRED', wholeEngine='NOT_COMPLETE',
                  artifacts=[dict(path=x, bytes=len((PACKET/x).read_bytes()), sha256=sha((PACKET/x).read_bytes())) for x in retained])
    (PACKET / 'CONTRACT_AUDIT.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('PASS SOURCE/API PROPOSAL BINDINGS ONLY: %d pinned files, six procedures, ten explicit unapproved policies; engine unchanged.' % len(rows))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', action='store_true', help='Create the additional immutable proposal bindings once')
    args = parser.parse_args()
    if args.bind:
        bind()
    verify()
