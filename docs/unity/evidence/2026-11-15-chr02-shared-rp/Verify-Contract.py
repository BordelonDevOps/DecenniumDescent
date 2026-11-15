"""Validate immutable contract sources, not proposed gameplay execution."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOURCE = '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
BASE = '27a942aa549c78f23d5db300a71590a738b97120'
RB = 'DescentReviewChanges/ReviewBible/'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def raw(path, rev=SOURCE):
    return git('show', rev+':'+path)

def obj(path, rev=SOURCE):
    return json.loads(raw(path,rev).decode('utf-8-sig'))

def bind(path, rev):
    data=raw(path,rev)
    assert data==raw(path,BASE), 'Pinned source changed: '+path
    return dict(path=path,revision=rev,gitBlob=git('rev-parse',rev+':'+path).decode().strip(),
                sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),equalsBaseline=True)

source_paths=[RB+p for p in [
    'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',
    'docs/mechanics/CHARACTER_FOUNDATION_TABLES.md',
    'data/playtest/character_foundation.json',
    'data/public/class_playtests/cleric.json',
    'docs/mechanics/CLASS_PLAYTEST_RULES.md',
    'docs/mechanics/CLASS_PLAYTEST_BUILD_EXAMPLES.md',
    'docs/mechanics/HEALING_DEATH_PLAYTEST.md',
    'docs/mechanics/HEALING_DEATH_SOURCE_BINDINGS.md',
    'data/playtest/healing_death_bindings.json',
    'docs/mechanics/SPELL_INTEGRATION_RULES.md',
]]
audit_paths=[
    'docs/canon/CANON_MANIFEST.json','docs/canon/REPOSITORY_PROMOTION.md',
    'docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json',
    'docs/unity/evidence/2026-11-15-tac06-resurrection/GPT_CONTRACT_REVIEW.md',
    'engine/com.decennium.foundation/Laboratory/Model/PlaytestCharacterBuild.cs',
    'engine/com.decennium.foundation/Laboratory/Model/CharacterProfiles.cs',
    'engine/com.decennium.foundation/Laboratory/Model/CharacterRuleFacts.cs',
    'engine/com.decennium.foundation/Laboratory/Model/SharedCharacterAdvancement.cs',
    'engine/com.decennium.foundation/Laboratory/Model/ConnectedExpeditionSession.cs',
    'engine/com.decennium.foundation/Laboratory/Model/ActorLifeRules.cs',
    'engine/com.decennium.foundation/Runtime/Core/CharacterAdvancementRecords.cs',
]
sources=[bind(p,SOURCE) for p in source_paths]+[bind(p,BASE) for p in audit_paths]
foundation=obj(RB+'data/playtest/character_foundation.json')
cleric=obj(RB+'data/public/class_playtests/cleric.json')
class_row=next(c for c in foundation['classes'] if c['class']=='Cleric')
card=cleric['cards'][12]
assert card['id']=='cleric.base.healing-rite' and card['minimumClassLevel']==1
assert card['acquisition']=='selection' and card['activation']=='Action' and card['cost']=='2 RP'
assert class_row['hitDie']==8 and class_row['rpByClassLevel'][0]==3
assert class_row['rpByClassLevel']==cleric['rpByClassLevel']
assert class_row['multiclassPrerequisites']=={'WIS':13}
assert class_row['savingThrowProficiencies']==['WIS','CHA']
assert all(x in class_row['skillOptions'] for x in ['Medicine','Religion']) and class_row['skillChoices']==2
selections=[cleric['cards'][i] for i in [1,3,12,14]]
assert all(c['minimumClassLevel']==1 and c['band']=='Base' and c['acquisition']=='selection' for c in selections)
assert sum(c['sourceKind']=='active' for c in selections)==2
assert len(set(c['id'] for c in selections))==4
assert not any(c['name']=='Divine Favor' for c in cleric['cards'])
card_hash=hashlib.sha256(json.dumps(card,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
assert card_hash=='20a27516ae922475d5979c529d88a5f83d4a29cff8e8ce063b46f1009be73e2f'
def walk(value):
    if isinstance(value,dict):
        yield value
        for v in value.values():yield from walk(v)
    elif isinstance(value,list):
        for v in value:yield from walk(v)
healing=next(x for x in walk(obj(RB+'data/playtest/healing_death_bindings.json'))
             if x.get('bindingId')=='class-card:cleric:cleric.base.healing-rite')
assert healing['sourceSha256']==card_hash
assert all(card.get(k)==v for k,v in healing['sourceProcedure'].items())
rulemap=obj('docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json',BASE)
ids=['CHR-02','CHR-03','CHR-05','TAC-06','TAC-07','TAC-08']
edges={x['id']:x['dependencies'] for x in walk(rulemap) if x.get('id') in ids and 'dependencies' in x}
assert edges['CHR-02']==['CHR-01','FND-05']
assert 'CHR-02' in edges['CHR-03'] and 'CHR-02' in edges['TAC-07']
assert 'TAC-07' in edges['TAC-08'] and 'TAC-08' in edges['CHR-05']
assert 'CHR-03' in edges['CHR-05']
costs={int(k):v for k,v in foundation['pointBuy']['costs'].items()}
assert foundation['pointBuy']['budget']==27
scores=[10,10,10,10,14,10]
assert sum(costs[s] for s in scores)==17
data=dict(status='PROPOSED_NOT_IMPLEMENTED',baseline=BASE,sourceRevision=SOURCE,sources=sources,
          selectedClass=class_row,selectedCard=card,classifiedBinding=healing,
          initialCardSelections=[c['id'] for c in selections],mappedDependencies=edges,
          proposedInitialFacts=dict(abilities=scores,pointBuyCost=17,level=1,maximumHp=8,hitDie=8,
                                    rpCapacity=3,currentRp=3,currentRpAuthority='PENDING_EXPLICIT_CONSENSUS_NOT_TABLE_AUTHORITY'),
          pendingDecisions=['A: exact paid witness dependency refinement','B: once-only initial RP funding','C: scoped initial class construction'])
(HERE/'SOURCE_API_BINDINGS.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
changes=git('diff','--name-only',BASE,'--','engine').decode().splitlines()
assert not changes, 'Engine changed before contract approval: '+repr(changes)
artifacts=[]
for p in sorted(HERE.iterdir()):
    if p.is_file() and p.name!='CONTRACT_VALIDATION.json':
        b=p.read_bytes();artifacts.append(dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b)))
report=dict(status='PASS_SOURCE_CHECKS_ONLY',sourceFiles=len(source_paths),baselineFiles=len(audit_paths),
            exactSelectedCardSha256=card_hash,mappedDependencies=edges,engineChanges=changes,
            artifacts=artifacts,compilation='NOT_RUN_NO_ENGINE_CHANGE',runtimeTests='NOT_RUN',
            connectedPaidHealingRite='NOT_IMPLEMENTED',gptReview='PENDING',pendingDecisions=data['pendingDecisions'])
(HERE/'CONTRACT_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['artifacts','mappedDependencies']}))
