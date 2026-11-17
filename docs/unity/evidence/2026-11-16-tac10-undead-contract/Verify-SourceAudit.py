"""Reproducible source/API evidence only; does not execute or qualify C#."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
BASELINE = '1d208c6b863ebd7ef0de5e502818678d73c4038b'
ENGINE = '2733b9fd75e2159ad73312b9583311693b925598'
SOURCE = '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
CODE = 'engine/com.decennium.foundation/'
RB = 'DescentReviewChanges/ReviewBible/'
PRIOR = 'docs/unity/evidence/2026-11-16-chr05-consecration-contract/'
BESTIARY = 'docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack/'
FERRY = BESTIARY + 'Monster_Manual_of_the_Known_Descent_Source/entries/ferry-wraith-of-the-hush.md'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def write(name, value):
    (PACKET / name).write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())

def main():
    assert not git('diff', ENGINE, '--', 'engine').strip(), 'Engine changed before contract approval'
    cs = [p for p in git('ls-tree', '-r', '--name-only', ENGINE, '--', CODE).decode().splitlines() if p.endswith('.cs')]
    sources = {
        'CANON_MANIFEST.md': BASELINE,
        'docs/canon/CANON_MANIFEST.json': BASELINE,
        'docs/canon/REPOSITORY_PROMOTION.md': BASELINE,
        'docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json': BASELINE,
        PRIOR + 'GPT_SOURCE_API_REVIEW.json': BASELINE,
        PRIOR + 'SOURCE_API_DECISIONS.md': BASELINE,
        PRIOR + 'UNDEAD_SOURCE_SCAN.json': BASELINE,
        'docs/unity/evidence/2026-11-16-exp07-post-recovery/SOURCE_API_CONTRACT.md': BASELINE,
        'docs/unity/evidence/2026-11-16-exp07-post-recovery/APPROVED_CONTRACT.md': BASELINE,
        'docs/unity/evidence/2026-11-12-tac10-later-defender-controller/SOURCE_API_PROPOSAL.md': BASELINE,
        'docs/unity/evidence/2026-11-16-chr03-bishop-runtime/GPT_FINAL_REVIEW.json': BASELINE,
        'docs/unity/evidence/2026-11-16-chr03-bishop-runtime/final/FINAL_RECONCILIATION.json': BASELINE,
        FERRY: SOURCE,
        BESTIARY + 'README.md': SOURCE,
        BESTIARY + 'build-filters.json': SOURCE,
        BESTIARY + 'Monster_Manual_of_the_Known_Descent_Source/ENTRY_TEMPLATE.md': SOURCE,
        RB + 'data/playtest/bestiary_public_source_candidate.json': SOURCE,
        RB + 'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md': SOURCE,
        RB + 'docs/mechanics/COMBAT_ACTION_PLAYTEST.md': SOURCE,
        RB + 'docs/mechanics/CONDITIONS_PLAYTEST.md': SOURCE,
        RB + 'docs/mechanics/CLASS_PLAYTEST_RULES.md': SOURCE,
        RB + 'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md': SOURCE,
        'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json': SOURCE,
    }
    patterns = {
        'numeric': r'CharacterRuleFacts|CharacterStateFacts|\.Characters\b|PrototypeArmor|UnarmoredBaseAc',
        'damage-defense': r'Resistan|Immunit|DamageType|DamageFlavor',
        'life': r'UsesDeathSaves|ActorLifeValidation',
        'physical-seal-commands': r'\bDisarm\b|\bSunder\b|\bImprovise\b|DestroySeal|InvalidateSeal',
    }
    texts, searches = {}, {}
    for p in cs:
        texts[p] = (ROOT / p).read_text(encoding='utf-8-sig')
    for label, pattern in patterns.items():
        rows = []
        for p in cs:
            if '/Tests/' in p:
                continue
            hits = [dict(line=i+1, text=line.strip()) for i, line in enumerate(texts[p].splitlines()) if re.search(pattern, line)]
            if hits:
                rows.append(dict(path=p, hits=hits))
                sources[p] = ENGINE
        searches[label] = dict(pattern=pattern, nonTestOnly=True, matchedFiles=len(rows),
                               matchedLines=sum(len(r['hits']) for r in rows), rows=rows)
    extra = [
        'Runtime/Core/Simulation.cs', 'Runtime/Core/ActorMovementRecord.cs',
        'Runtime/Core/PostRecoveryEncounterRecords.cs', 'Runtime/Core/PostRecoveryEncounterValidation.cs',
        'Runtime/Core/LaterEncounterRecords.cs', 'Runtime/Persistence/SnapshotCodec.cs',
        'Runtime/Persistence/PostRecoveryEncounterCodec.cs', 'Laboratory/Model/SharedPostRecoveryEncounter.cs',
        'Laboratory/Model/SharedLaterDefenderDecision.cs', 'Laboratory/Model/LaterDefenderController.cs',
        'Laboratory/Model/ConnectedExpeditionSession.cs', 'Laboratory/Model/ConnectedExpeditionView.cs',
        'Laboratory/Model/ObservationGeometry.cs', 'Laboratory/Model/ObservationRules.cs',
        'Laboratory/Model/PlanarCombatGeometry.cs', 'Laboratory/Model/PlaytestTiming.cs',
        'Laboratory/Model/SharedWorldCombatPolicy.cs', 'Laboratory/Model/SharedAuraOfFaith.cs',
        'Laboratory/Model/SharedRadiance.cs',
    ]
    for p in extra:
        sources[CODE+p] = ENGINE
    payload = ''.join(rev+':'+p+'\n' for p, rev in sorted(sources.items())).encode()
    batch = subprocess.run(['git','cat-file','--batch'], input=payload, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    pos, blobs, bindings = 0, {}, []
    for p, rev in sorted(sources.items()):
        end = batch.stdout.index(b'\n',pos)
        head = batch.stdout[pos:end].decode().split()
        assert len(head)==3 and head[1]=='blob', (p, head)
        size = int(head[2]); pos = end+1
        raw = batch.stdout[pos:pos+size]; pos += size+1
        local = (ROOT/p).read_bytes()
        assert local==raw or local.replace(b'\r\n',b'\n')==raw, p
        blobs[p]=raw
        bindings.append(dict(path=p, revision=rev, gitBlob=head[0], bytes=size, sha256=hashlib.sha256(raw).hexdigest(),
                             checkoutRelation='exact' if raw==local else 'CRLF-only'))
    assert pos==len(batch.stdout) and not batch.stderr
    text = lambda p: blobs[p].decode('utf-8-sig')
    parsed = lambda p: json.loads(text(p))
    checks=[]
    def check(name,value):
        assert value,name
        checks.append(dict(name=name,passed=True))
    review=parsed(PRIOR+'GPT_SOURCE_API_REVIEW.json')
    check('Actual source/API prerequisite selection and Codex agreement', review['responseId']=='e963e4bc-5f8d-5699-b626-ddf4b46339d7' and not review['runtimeAuthorized'] and 'TAC-10' in review['nextGate'])
    mapping=parsed('docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json')
    item=lambda id: next(x for x in mapping['workItems'] if x['id']==id)
    check('Approved dependency edges preserved', item('TAC-10')['dependencies']==['TAC-03','TAC-04','TAC-05','TAC-02'] and item('CHR-05')['dependencies']==['CHR-03','TAC-02','TAC-05','TAC-08'])
    candidate=parsed(RB+'data/playtest/bestiary_public_source_candidate.json')
    ferry=next(x for x in candidate['records'] if x['id']=='ferry-wraith-of-the-hush')
    check('Candidate remains uninstalled and operationally unreviewed', not candidate['runtimeInstalled'] and ferry['reviewStatus']=='SOURCE_BOUND_NOT_OPERATIONALLY_REVIEWED')
    check('Canonical text retained exactly modulo CRLF', ferry['source']['originalUtf8Text'].replace('\r\n','\n')==text(FERRY).replace('\r\n','\n'))
    raw=text(FERRY)
    check('Printed type and numeric facts', all(x in raw for x in ['Medium Undead','Armor** 10','Hit Points** 9','Speed** 40 ft.','12 (+1) | 14 (+2) | 14 (+2) | 9 (-1) | 11 (+0) | 16 (+3)']))
    check('Printed defenses and separate named immunity', all(x in raw for x in ['**Resistances** necrotic','**Immunities** poison','**Condition Immunities** poisoned','**Save DC** 13']))
    check('Actions heading and exact finite attack', '### Actions' in raw and ferry['statBlock']['actions']==[{'name':'Hellfire Claw','sourceText':'*Attack:* +3 to hit, one target. *Hit:* 1d4 fire damage (average 2).'}])
    check('Attack category/reach absent in selected action line', not re.search(r'\bmelee\b|\branged\b|\breach\b', ferry['statBlock']['actions'][0]['sourceText'], re.I))
    check('Mandatory Contract-Bound finite suppression', 'destroying or invalidating it suppresses that feature until the end of the next round' in raw)
    check('Publication does not supply automatic knowledge', all(x in raw for x in ['Use **Religion**','DC 11','DC 15','DC 19']))
    check('Harvest is a separate chance/time/skill source', all(x in raw for x in ['**Harvest DC:** 12','**Base time:** 20 minutes','45%, 10 gp base']))
    life=text(CODE+'Runtime/Core/ActorLifeRecords.cs')
    check('Existing character levels and actor-character equality require integration', 'gained.Length<1' in life and '!actors.SequenceEqual(s.Characters.Select' in life)
    check('Existing ordinary monster versus significant NPC life distinction', 'an ordinary monster dies' in text(RB+'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md') and 'The Director identifies significant NPCs consistently' in text(RB+'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md'))
    check('No arbitrary immunity from type', 'Immunity to a named condition prevents that condition' in text(RB+'docs/mechanics/CONDITIONS_PLAYTEST.md'))
    check('Typed damage and named condition immunity are distinct APIs', 'Named condition immunity only. Damage defenses' in text(CODE+'Laboratory/Model/ConditionApplications.cs'))
    check('Petrification already halves after flat reductions', 'Input is already after flat reductions/saves' in text(CODE+'Laboratory/Model/PlaytestConditions.cs'))
    check('Current armor derives character baseline', 'PrototypeArmor.UnarmoredBaseAc' in text(CODE+'Laboratory/Model/SharedCharacterAdvancement.cs'))
    check('Source-bound numeric consumers include target and observer paths', all(any(Path(r['path']).name==n for r in searches['numeric']['rows']) for n in ['SharedOverwatchExecution.cs','SharedSanctuary.cs','SharedFrightened.cs','SharedObservationActions.cs','SharedHuntingTrap.cs','SharedWorldRangedCombat.cs']))
    check('No current named Disarm Sunder Improvise or seal command in non-test Csharp scan', searches['physical-seal-commands']['matchedLines']==0)
    check('Generic object durability remains an unresolved source dependency', 'No invented durability' in text(RB+'docs/mechanics/COMBAT_ACTION_PLAYTEST.md'))
    check('Geometry can declare larger bounded maps without changing units', 'width > 64' in text(CODE+'Laboratory/Model/ObservationGeometry.cs') and 'height > 64' in text(CODE+'Laboratory/Model/ObservationGeometry.cs'))
    check('Existing recovery actor remains fixed humanoid-style class body', 'Warrior12,7,7' in text(CODE+'Runtime/Core/PostRecoveryEncounterRecords.cs'))
    check('New actor must be registered from genesis rather than entry', 'Entry never creates its actor' in text(CODE+'Runtime/Core/PostRecoveryEncounterRecords.cs'))
    check('Accepted engine is unchanged', not git('diff',ENGINE,'--','engine').strip())
    write('SOURCE_BINDINGS.json',dict(baseline=BASELINE,acceptedEngine=ENGINE,sourceRevision=SOURCE,sources=bindings))
    write('API_CONSUMERS.json',dict(searchedTrackedCsharpFiles=len(cs),searches=searches,
          limits='Lexical inventory with direct inspection of actor validation, numeric projections, attack/defense targets, life, condition immunity, controller and context APIs. Not a semantic proof that every call site is safe; implementation must reconcile all rows and audit indirect consumers.'))
    write('SOURCE_EXTRACTS.json',dict(canonicalPath=FERRY,canonicalText=raw,candidate=ferry,
          selectedSourceRules={p:text(p) for p in sources if p.startswith(RB+'docs/mechanics/')},
          actionContextCorrection='The Actions heading supplies action context; category and reach/range need binding.',
          scope='Exact source evidence only; no proposed rule is promoted by these extracts.'))
    report=dict(status='PASS_SOURCE_API_AUDIT_RUNTIME_NOT_AUTHORIZED',baseline=BASELINE,acceptedEngine=ENGINE,sourceRevision=SOURCE,
                pinnedBlobs=len(bindings),searchedTrackedCsharpFiles=len(cs),numericCandidateFiles=searches['numeric']['matchedFiles'],
                numericCandidateLines=searches['numeric']['matchedLines'],checks=checks,engineUnchanged=True,
                newCompilation=False,newGameplay=False,runtimeAuthorized=False,
                unresolved=['Attack category/reach operational consensus','Non-class actor consumer integration and life eligibility',
                            'Physical seal destruction/invalidation and suppression clock','Fresh connected context and finite route approval',
                            'Required direct defense/trait/compatibility evidence, without an inherited exception'])
    write('SOURCE_AUDIT.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='checks'}|dict(checks=len(checks))))
if __name__=='__main__':
    main()
