"""Bind source/API review evidence. This does not compile or execute resurrection."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SOURCE = '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
BASELINE = '2082003073be9124e7a3e6c15113828cceee56e6'
RB = 'DescentReviewChanges/ReviewBible/'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def bind(path, revision):
    raw = git('show', revision + ':' + path)
    return dict(path=path, revision=revision,
                gitBlob=git('rev-parse', revision + ':' + path).decode().strip(),
                sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw),
                equalsBaseline=raw == git('show', BASELINE + ':' + path))

sources = [RB+p for p in [
    'data/public/class_playtests/cleric.json',
    'docs/mechanics/CLASS_PLAYTEST_RULES.md',
    'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',
    'docs/mechanics/HEALING_DEATH_PLAYTEST.md',
    'docs/mechanics/HEALING_DEATH_SOURCE_BINDINGS.md',
    'data/playtest/healing_death_bindings.json',
    'tools/healing_playtest_rules.py',
]]
baseline_paths = [
    'docs/canon/CANON_MANIFEST.json', 'docs/canon/REPOSITORY_PROMOTION.md',
    'docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json',
    'engine/com.decennium.foundation/Runtime/Core/ActorLifeRecords.cs',
    'engine/com.decennium.foundation/Runtime/Core/CharacterAdvancementRecords.cs',
    'engine/com.decennium.foundation/Runtime/Core/HarvestRecords.cs',
    'engine/com.decennium.foundation/Runtime/Core/Simulation.cs',
    'engine/com.decennium.foundation/Laboratory/Model/SharedCharacterAdvancement.cs',
    'engine/com.decennium.foundation/Laboratory/Model/PlaytestCharacterBuild.cs',
    'engine/com.decennium.foundation/Laboratory/Model/CharacterProfiles.cs',
    'engine/com.decennium.foundation/Laboratory/Model/ClassAdvancementOptionCatalog.cs',
    'engine/com.decennium.foundation/Laboratory/Model/ActorLifeRules.cs',
    'engine/com.decennium.foundation/Laboratory/Model/ConnectedExpeditionSession.cs',
    'engine/com.decennium.foundation/Laboratory/Model/SharedConsumeDecay.cs',
    'engine/com.decennium.foundation/Laboratory/Model/SharedShortRest.cs',
]
records = [bind(p, SOURCE) for p in sources] + [bind(p, BASELINE) for p in baseline_paths]
assert all(r['equalsBaseline'] for r in records), 'Source changed since pinned review revision'
cleric = json.loads(git('show', SOURCE + ':' + sources[0]).decode('utf-8-sig'))
card = cleric['cards'][37]
assert card['id'] == 'cleric.hero.saint.resurrection'
assert card['minimumClassLevel'] == 16 and card['path'] == 'Saint'
assert card['cost'] == '3 Conviction + 10 RP' and card['activation'] == 'Action'
assert card['frequency'] == '1/long rest' and cleric['rpByClassLevel'][15] == 45
assert card['designStatus'] == 'provisional-playtest'
binding_data = json.loads(git('show', SOURCE + ':' + sources[5]).decode('utf-8-sig'))
def find_binding(value):
    if isinstance(value, dict):
        if value.get('bindingId') == 'class-card:cleric:cleric.hero.saint.resurrection':
            return value
        for child in value.values():
            found = find_binding(child)
            if found is not None: return found
    elif isinstance(value, list):
        for child in value:
            found = find_binding(child)
            if found is not None: return found
    return None
binding = find_binding(binding_data)
assert binding is not None
for key, value in binding['sourceProcedure'].items():
    assert card.get(key) == value, 'Classified binding mismatch: '+key
card_hash = hashlib.sha256(json.dumps(card, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
assert card_hash == binding['sourceSha256'], 'Classified source object hash mismatch'
result = dict(status='PROPOSED_CONTRACT_NOT_IMPLEMENTED', sourceRevision=SOURCE,
              engineBaseline=BASELINE, acceptedRuntime='0742794a7c1f8e15dd4e38ff72ae21dd61762b4a',
              acceptedReview='7b1e6b05-b5aa-5853-9cae-0bb428e20edb', sources=records,
              selectedCard=card, classifiedHealingBinding=binding,
              clericEngineSelectors=['/engine/'+str(i) for i in [0,1,2,3,4,7,9,10,11]],
              clericClassLevel16RpCapacity=45,
              engineAuditScope='Runtime/Core and Laboratory/Model; current balances/access not inferred from catalogs or pure capacity helpers')
(HERE/'SOURCE_API_BINDINGS.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
changed = git('diff', '--name-only', BASELINE, '--', 'engine').decode().splitlines()
assert not changed, 'Unexpected engine change during contract gate: '+repr(changed)
packet = []
for path in sorted(HERE.iterdir()):
    if path.is_file() and path.name != 'CONTRACT_VALIDATION.json':
        raw = path.read_bytes()
        packet.append(dict(path=path.relative_to(ROOT).as_posix(), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
report = dict(status='PASS_SOURCE_BINDINGS_ONLY', sourceFileCount=len(sources), baselineAuditFileCount=len(baseline_paths),
              allPinnedSourcesEqualBaseline=True, exactCardSelectorValidated=True, classifiedSourceObjectSha256=card_hash,
              engineChangesFromBaseline=changed, artifacts=packet,
              compilation='NOT_RUN_NO_ENGINE_CHANGE', runtimeTests='NOT_RUN_NO_RESURRECTION_IMPLEMENTATION',
              connectedResurrection='NOT_IMPLEMENTED',
              gptContractReview='50395a8a-f1f7-58ac-81b6-a9e116e35f09' if (HERE/'GPT_CONTRACT_REVIEW.md').exists() else 'PENDING')
(HERE/'CONTRACT_VALIDATION.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='artifacts'}))
