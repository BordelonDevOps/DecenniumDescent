"""Bind the resumed CHR03 proposal to accepted TAC05; no engine or gameplay execution."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
BASELINE = '91ede3a20dc1c2672bf431746ce143eb5d8a1951'
IMPLEMENTATION = 'f5800818bfadb7c51865c96a6058f9af2deb75a3'
EVIDENCE = 'e222a8663f0c74df886b4d927a5ec715e5fe34a5'
SOURCE = '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
RB = 'DescentReviewChanges/ReviewBible/'
ENGINE = 'engine/com.decennium.foundation/'
FEAR = 'docs/unity/evidence/2026-11-15-tac05-frightened/'
SETTLEMENT = 'docs/unity/evidence/2026-11-15-chr03-cleric-settlement/'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def require(value, message):
    if not value:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--create-bindings', action='store_true')
    args = parser.parse_args()
    historical = read(PACKET / 'SOURCE_BINDINGS.json')
    rows = [(row['path'], SOURCE if row['role'] == 'pinned-gameplay-source' else BASELINE, row['role'])
            for row in historical['sources']]
    rows += [(SETTLEMENT + name, BASELINE, 'accepted-context-and-historical-audit') for name in
             ('SOURCE_BINDINGS.json', 'GPT_CONTEXT_GUIDANCE.md', 'GPT_DEPENDENCY_REVIEW.md')]
    rows += [(FEAR + name, BASELINE, 'accepted-frightened-prerequisite') for name in
             ('GPT_FINAL_REVIEW.md', 'GPT_CONTRACT_REVIEW.md', 'GPT_CLOSURE_GUIDANCE.md', 'SOURCE_API_CONTRACT.md')]
    rows += [(FEAR + name, EVIDENCE, 'immutable-completed-regression') for name in
             ('IMPLEMENTATION_BINDINGS.json', 'REGRESSION_PROGRESS.json', 'retained-development/regression/all-names.txt')]
    rows += [(ENGINE + name, BASELINE, 'accepted-runtime-audit') for name in
             ('Runtime/Core/FrightenedRecords.cs', 'Runtime/Persistence/CharacterAdvancementCodec.cs',
              'Laboratory/Model/SourceQualifiedConditionCure.cs', 'Laboratory/Model/SharedFrightened.cs',
              'Laboratory/Model/ClassAdvancementScheduleCatalog.cs', 'Laboratory/Model/ClassAdvancementOptionCatalog.cs')]
    require(len(rows) == len({path for path, _, _ in rows}), 'Duplicate source path')
    requests = ''.join(revision + ':' + path + '\n' for path, revision, _ in rows).encode()
    raw = subprocess.run(['git', 'cat-file', '--batch'], cwd=ROOT, input=requests,
                         stdout=subprocess.PIPE, check=True).stdout
    reader, entries, payloads = io.BytesIO(raw), [], {}
    for path, revision, role in rows:
        header = reader.readline().decode().split()
        require(len(header) == 3 and header[1] == 'blob', 'Missing pinned blob: ' + path)
        data = reader.read(int(header[2]))
        require(reader.read(1) == b'\n', 'Invalid Git batch framing')
        entries.append({'path': path, 'revision': revision, 'role': role, 'gitBlob': header[0],
                        'sha256': sha(data), 'bytes': len(data)})
        payloads[path] = data
    require(not reader.read(), 'Unexpected Git batch remainder')
    require(sha((PACKET / 'SOURCE_BINDINGS.json').read_bytes()) == sha(payloads[SETTLEMENT + 'SOURCE_BINDINGS.json']),
            'Historical source bindings were changed')
    binding = {'baseline': BASELINE, 'implementation': IMPLEMENTATION, 'acceptedEvidence': EVIDENCE,
               'sourceRevision': SOURCE, 'sources': entries,
               'status': 'COMPLETE_CONTRACT_SOURCE_AUDIT_ONLY_NOT_IMPLEMENTATION_APPROVAL'}
    if args.create_bindings:
        write(PACKET / 'COMPLETE_SOURCE_BINDINGS.json', binding)
    require(read(PACKET / 'COMPLETE_SOURCE_BINDINGS.json') == binding, 'Complete source bindings differ')
    require(not subprocess.check_output(['git', 'diff', '--name-only', BASELINE, '--', 'engine'], cwd=ROOT).strip(),
            'Engine changed during complete-contract audit')
    require(not subprocess.check_output(['git', 'diff', '--name-only', IMPLEMENTATION, BASELINE, '--', 'engine'], cwd=ROOT).strip(),
            'Accepted baseline differs from reviewed implementation')
    checks = []

    def check(name, value):
        require(value, name)
        checks.append({'name': name, 'status': 'PASS'})

    def text(path):
        return payloads[path].decode('utf-8-sig')

    cleric = json.loads(payloads[RB + 'data/public/class_playtests/cleric.json'])
    foundation = json.loads(payloads[RB + 'data/playtest/character_foundation.json'])['classes'][1]
    cards = {row['id']: row for row in cleric['cards']}
    selected_ids = ['cleric.base.healing-rite', 'cleric.base.invocation-attunement', 'cleric.base.radiance.radiance',
                    'cleric.base.judging-light', 'cleric.base.conviction-pool']
    check('Cleric chronological d8/base5 and RP3-to4', foundation['class'] == 'Cleric'
          and foundation['hitDie'] == 8 and foundation['fixedLaterLevelHpBase'] == 5
          and foundation['rpByClassLevel'][:2] == cleric['rpByClassLevel'][:2] == [3, 4])
    check('Exactly two Base selections, no active minimum or ASI', cleric['schedule'][1] ==
          {'classLevel': 2, 'choose': 2, 'bands': ['Base'], 'minimumActives': 0, 'asiOrFeat': False})
    check('Automatic Attunement and Radiance at Cleric2', all(cards[key]['acquisition'] == 'automatic'
          and cards[key]['minimumClassLevel'] == 2 for key in selected_ids[1:3]))
    check('Selected Judging Light and Pool are legal distinct Base choices', all(cards[key]['acquisition'] == 'selection'
          and cards[key]['band'] == 'Base' and cards[key]['minimumClassLevel'] <= 2 for key in selected_ids[3:]))
    rite, radiance = cards[selected_ids[0]], cards[selected_ids[2]]
    check('Healing Rite actual Action2RP and living ally30ft', rite['activation'] == 'Action'
          and rite['cost'] == '2 RP' and rite['rangeAndTarget'] == 'One living ally within 30 feet'
          and 'S d8 + M HP' in rite['effect'])
    check('Radiance requires own-turn actual healing and optional named cure', all(value in radiance['effect'] for value in
          ['Once on each of your turns', 'restores HP', 'one creature healed by that Rite',
           'S additional HP', 'may immediately end either Frightened or Poisoned on itself']))
    check('Pool adds capacity without immediate restoration', 'Increase your Conviction maximum by 2' in cards[selected_ids[4]]['effect']
          and 'does not immediately restore' in cards[selected_ids[4]]['effect'])
    check('Advancement is not healing or rest', all(value in text(RB + 'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md')
          for value in ['Keep current HP and spent resources unchanged', 'not healing or a rest']))
    check('Objective must be announced before the Opening', 'other milestones announced before the Opening begins'
          in text(RB + 'docs/mechanics/XP_ADVANCEMENT_CANON.md'))
    old_spells = json.loads(payloads['docs/unity/evidence/2026-11-15-tac07-cleric-repertoire/SELECTED_SPELL_BINDINGS.json'])
    detect = next(row for row in old_spells['selected'] if row['id'] == 'detect-magic')
    catalog = json.loads(payloads[RB + 'data/public/spell_playtests/catalog.json'])['spells']
    spell = catalog[int(detect['wholeCardPointer'].split('/')[-1])]
    check('Earned Detect Magic keeps exact source and Cleric placement', spell['id'] == 'detect-magic'
          and sha(canonical(spell)) == detect['wholeCardSha256']
          and sha(canonical(spell['operational'])) == detect['procedureSha256']
          and spell['classAccess']['Cleric']['rank'] == 1 and spell['classAccess']['Cleric']['school'] == 'Divination')
    check('Earned repertoire component requires genuine staged consumption', all(value in text(ENGINE + 'Laboratory/Model/SharedSpellRepertoire.cs')
          for value in ['SettleClericEarnedRepertoire', 'milestone.ConsumedRevision != advancement.Revision',
                        'staged.CharacterAdvancements.Contains(advancement)']))
    check('Initial automatic grant semantics are revision0 only', 'origin==CharacterFeatureGrantOrigin.AutomaticClassFeature&&(milestoneId!=""||grantedRevision!=0)'
          in text(ENGINE + 'Runtime/Core/CharacterAdvancementRecords.cs'))
    check('Current advancement path is Soldier-only', 'if(!supportedProfile)return "UnsupportedAdvancementPath"'
          in text(ENGINE + 'Laboratory/Model/SharedCharacterAdvancement.cs'))
    check('Current Rite still requires Cleric1 tactical context', all(value in text(ENGINE + 'Laboratory/Model/SharedResonance.cs')
          for value in ['HealingRiteContextUnsupported', 'character.Levels.Count(x => x.ClassName == "Cleric") != 1']))
    check('Current recipient control can use actual Authority.Controls', 'public bool Controls(string actor)'
          in text(ENGINE + 'Runtime/Core/Simulation.cs'))
    timing = text(ENGINE + 'Runtime/Core/LaterEncounterRecords.cs')
    check('Owning actor calendar prioritizes retained reinforcement epoch', 'phase.Epoch.Order.Contains(actor)) return phase.Epoch' in timing)
    check('Closure clears tactical Encounter', 'state.Encounter = null' in text(ENGINE + 'Laboratory/Model/SharedLaterEncounter.cs'))
    check('Interval starts and phase markers require local/global conversion', 'admission.Phase.GlobalTurn(local)' in timing
          and 'global - phase.FirstTurn' in text(ENGINE + 'Laboratory/Model/SharedReinforcement.cs'))
    kinds = [value.strip() for value in re.search(r'enum ConditionKind\s*\{([^}]+)\}',
             text(ENGINE + 'Laboratory/Model/ConditionApplications.cs')).group(1).split(',')]
    check('Accepted lifecycle now includes both named conditions and appended Frightened', len(kinds) == 15
          and kinds[-1] == 'Frightened' and 'Poisoned' in kinds)
    cure = text(ENGINE + 'Laboratory/Model/SourceQualifiedConditionCure.cs')
    check('Qualified cure has only detached invocation factory at baseline', 'private ConditionCureInvocation(' in cure
          and 'internal static ConditionCureInvocation ForDetachedTest(' in cure
          and 'ForClericRadiance' not in cure and 'history.Append(ConditionOperation.Cure(' in cure)
    check('Generic cure uses present eligible records, including suppressed records', all(value in text(ENGINE + 'Laboratory/Model/ConditionLedger.cs')
          for value in ['if (!instance.Present(Now)) return instance;', 'instance.Application.Kind == kind && instance.Application.GenericCureAllowed']))
    check('Runtime repeat already skips applications no longer present', 'if (!ledger.Applications.Any(x => x.Id == timing.ApplicationId && x.Present(ledger.Now))) continue;'
          in text(ENGINE + 'Laboratory/Model/SharedFrightened.cs'))
    fear_validation = text(ENGINE + 'Runtime/Core/FrightenedRecords.cs')
    check('Old profile still requires due repeat and rejects Frightened cure', 'Missing due Frightened repeat save.' in fear_validation
          and 'x.Kind == ConditionOperationKind.Cure && x.Subject == "Frightened"' in fear_validation)
    check('TAC05 acceptance preserves explicit connected closure exception', all(value in text(FEAR + 'GPT_FINAL_REVIEW.md') for value in
          ['4d7b608f-3bcb-5b6c-866f-17235e04d5c6', IMPLEMENTATION, EVIDENCE, 'not demonstrated; reviewed scope exception']))
    check('Post-closure context and both RP branches are actually reviewed', all(value in text(SETTLEMENT + 'GPT_CONTEXT_GUIDANCE.md')
          for value in ['68898ea2-4ba8-52e5-afe9-ac081a2dbd12', 'WorldTiming.ForActor', '1/4', '3/4', 'Codex agrees']))
    found = {}

    def visit(value):
        if isinstance(value, dict):
            if value.get('id') in ('CHR-03', 'TAC-05', 'TAC-07', 'TAC-08', 'CHR-05') and 'dependencies' in value:
                found[value['id']] = sorted(value['dependencies'])
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(json.loads(payloads['docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json']))
    expected = {'CHR-03': ['CHR-02'], 'TAC-05': ['TAC-01', 'RUL-05'], 'TAC-07': ['CHR-02', 'FND-05'],
                'TAC-08': ['TAC-02', 'TAC-05', 'TAC-07'], 'CHR-05': ['CHR-03', 'TAC-02', 'TAC-05', 'TAC-08']}
    check('Approved direct map dependencies remain unchanged', found == {key: sorted(value) for key, value in expected.items()})
    regression = json.loads(payloads[FEAR + 'REGRESSION_PROGRESS.json'])
    names = text(FEAR + 'retained-development/regression/all-names.txt').splitlines()
    check('Accepted original1517 inventory and all six completed workers', regression['status'] == 'PASS'
          and regression['completed'] == regression['discovered'] == len(names) == len(set(names)) == 1517
          and regression['failed'] == 0 and len(regression['finishedWorkers']) == 6
          and [row['Name'] for row in regression['cases']] == names)
    selections = [{'id': key, 'pointer': '/cards/' + str(next(i for i, row in enumerate(cleric['cards']) if row['id'] == key)),
                   'sha256': sha(canonical(cards[key])), 'source': cards[key]['source']} for key in selected_ids]
    selected = {'sourceRevision': SOURCE, 'clericFile': RB + 'data/public/class_playtests/cleric.json',
                'cards': selections, 'engine': [{'pointer': '/engine/' + str(index), 'sha256': sha(canonical(cleric['engine'][index]))}
                                              for index in (0, 1, 3, 7, 8, 9, 10, 11)],
                'schedule': {'pointer': '/schedule/1', 'sha256': sha(canonical(cleric['schedule'][1]))},
                'earnedSpell': detect}
    write(PACKET / 'SELECTED_SETTLEMENT_BINDINGS.json', selected)
    artifacts = {path.name: {'bytes': path.stat().st_size, 'sha256': sha(path.read_bytes())}
                 for path in sorted(PACKET.iterdir()) if path.is_file() and path.name != 'COMPLETE_CONTRACT_AUDIT.json'}
    report = {'status': 'PASS', 'scope': 'Pinned source and current capability findings; no runtime implementation or execution',
              'baseline': BASELINE, 'implementation': IMPLEMENTATION, 'acceptedEvidence': EVIDENCE,
              'sourceEntriesVerified': len(entries), 'checks': checks, 'engineChanged': False,
              'compilation': 'NOT_RUN_SOURCE_ONLY', 'runtimeTests': 'NOT_RUN_SOURCE_ONLY',
              'implementationAuthorized': False, 'completeContractReview': 'PENDING',
              'openReviewDecision': 'Condition-present connected cure intersection versus explicit detached Radiance producer controls',
              'artifacts': artifacts}
    write(PACKET / 'COMPLETE_CONTRACT_AUDIT.json', report)
    print(json.dumps({'status': 'PASS', 'sources': len(entries), 'checks': len(checks), 'engineChanged': False,
                      'runtimeTests': 'NOT_RUN_SOURCE_ONLY', 'completeContractReview': 'PENDING'}))


if __name__ == '__main__':
    main()
