"""Source-only EXP-07 contract audit. Does not execute the engine or validate a future route."""
import hashlib
import json
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
BASELINE = '0f96b0eea5822336f7933d3bc1a2428802611757'
ENGINE = 'e0994929b444b15fc38957eb80cc34ab19d56db6'
SOURCE = '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
EVIDENCE = 'eeb3a803ef736b0827d123d4a88c8620234d1727'
AUTHORITY = [
    'CANON_MANIFEST.md', 'docs/canon/CANON_MANIFEST.json', 'docs/canon/REPOSITORY_PROMOTION.md',
    'docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md', 'engine/AGENTS.md',
    'docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json',
    'docs/unity/evidence/2026-11-16-chr03-bishop-entry/GPT_SOURCE_REVIEW.json',
    'docs/unity/evidence/2026-11-15-mgt03-cleric-long-rest/GPT_FINAL_REVIEW.json',
    'docs/unity/evidence/2026-11-15-mgt03-cleric-long-rest/SOURCE_API_CONTRACT.md',
    'docs/unity/evidence/2026-11-15-mgt03-cleric-long-rest/implementation/RESULTS.json',
    'docs/unity/evidence/2026-11-11-exp07-later-encounter/SOURCE_API_REVIEW.md',
    'docs/unity/evidence/2026-11-11-exp07-companion-reinforcement/SOURCE_API_REVIEW.md',
    'docs/unity/evidence/2026-11-11-exp07-physical-reengagement/APPROVED_CONTRACT.md',
    'docs/unity/evidence/2026-11-15-tac05-frightened/SOURCE_API_CONTRACT.md',
    'docs/unity/evidence/2026-11-15-tac05-frightened/GPT_CONTRACT_REVIEW.md',
    'docs/unity/evidence/2026-11-15-chr03-cleric-settlement/SETTLEMENT_CONTRACT.md',
    'docs/unity/evidence/2026-11-15-tac08-cleric-casting/APPROVED_CASTING_CONTRACT.md',
    'docs/unity/CONDITION_LIFECYCLE_RULE_DECISIONS.md', 'docs/unity/ORDINARY_ATTACK_RULE_DECISIONS.md',
]
GAMEPLAY = [
    'DescentReviewChanges/ReviewBible/data/public/class_playtests/warrior.json',
    'DescentReviewChanges/ReviewBible/docs/mechanics/classes/warrior.md',
    'DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md',
    'DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md',
    'DescentReviewChanges/ReviewBible/docs/mechanics/CONDITIONS_PLAYTEST.md',
    'DescentReviewChanges/ReviewBible/data/playtest/condition_playtests.json',
    'DescentReviewChanges/ReviewBible/docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',
    'DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md',
    'DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json',
    'DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md',
]
CODE = [
    'Laboratory/Model/TestOnlySharedWorldPolicy.cs', 'Laboratory/Model/SharedLaterEncounter.cs',
    'Laboratory/Model/SharedReinforcement.cs', 'Laboratory/Model/SharedWorldCombatPolicy.cs',
    'Laboratory/Model/SharedWorldCommandQueries.cs', 'Laboratory/Model/SharedReengagement.cs',
    'Laboratory/Model/SharedFrightened.cs', 'Laboratory/Model/SharedCharacterAdvancement.cs',
    'Laboratory/Model/SharedResonance.cs', 'Laboratory/Model/SharedRadiance.cs',
    'Laboratory/Model/SharedSpellCasting.cs', 'Laboratory/Model/SharedSpellEffects.cs',
    'Laboratory/Model/SharedClericLongRest.cs', 'Laboratory/Model/SharedDailyProvisioning.cs',
    'Laboratory/Model/SharedRestDebt.cs', 'Laboratory/Model/SharedCharterAttempt.cs',
    'Laboratory/Model/SharedConnectedExplorationObservation.cs', 'Laboratory/Model/TestOnlyPolicy.cs',
    'Laboratory/Model/ActorLifeRules.cs', 'Laboratory/Model/SharedHavenAppraisal.cs',
    'Laboratory/Model/SharedHavenSale.cs', 'Laboratory/Model/LaterDefenderController.cs',
    'Laboratory/Model/ConnectedExpeditionSession.cs', 'Laboratory/Model/FrightenedRules.cs',
    'Runtime/Core/LaterEncounterRecords.cs', 'Runtime/Core/ReinforcementRecords.cs',
    'Runtime/Core/EncounterHistory.cs', 'Runtime/Core/FrightenedRecords.cs',
    'Runtime/Core/CharacterAdvancementRecords.cs', 'Runtime/Core/ClericSettlementValidation.cs',
    'Runtime/Core/ClericLongRestValidation.cs', 'Runtime/Core/SpellCastingProfile.cs',
]
VIEW_ROOT = 'docs/unity/evidence/2026-11-15-mgt03-cleric-long-rest/implementation/qualification/trace-terminal/reference/'
VIEWS = ['initial.ddsave.Player.view.json', 'initial.ddsave.FirstOpponent.view.json',
         'long-rest-first-funded.ddsave.Player.view.json', 'long-rest-paid-continuation.ddsave.Player.view.json']


def write(name, value):
    (PACKET/name).write_bytes((json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))


def main():
    requests = [(BASELINE,p,'authority-or-accepted-boundary') for p in AUTHORITY]
    requests += [(SOURCE,p,'selected-provisional-source') for p in GAMEPLAY]
    requests += [(ENGINE,'engine/com.decennium.foundation/'+p,'accepted-engine-api') for p in CODE]
    requests += [(EVIDENCE,VIEW_ROOT+p,'authentic-retained-view') for p in VIEWS]
    result = subprocess.run(['git','cat-file','--batch'],cwd=ROOT,
        input=''.join(rev+':'+path+'\n' for rev,path,_ in requests).encode('utf-8'),
        stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    position, bindings, blobs = 0, [], {}
    for revision,path,role in requests:
        end=result.stdout.index(b'\n',position)
        header=result.stdout[position:end].decode().split()
        assert len(header)==3 and header[1]=='blob', (path,header)
        length=int(header[2]); position=end+1
        raw=result.stdout[position:position+length];position+=length+1
        local_path=Path('\\\\?\\'+str(ROOT/path)) if len(str(ROOT/path))>=250 else ROOT/path
        local=local_path.read_bytes()
        assert local==raw or local.replace(b'\r\n',b'\n')==raw, 'Checkout differs: '+path
        blobs[path]=raw
        bindings.append({'path':path,'revision':revision,'role':role,'gitBlob':header[0],
            'bytes':length,'sha256':hashlib.sha256(raw).hexdigest(),
            'checkoutRelation':'exact' if local==raw else 'CRLF-only; preserved'})
    assert position==len(result.stdout) and not result.stderr.strip()
    assert not subprocess.check_output(['git','diff',ENGINE,'--','engine'],cwd=ROOT).strip()
    checks=[]
    def check(name,condition):
        assert condition,name
        checks.append(name)
    def contains(file,needle,name):
        check(name,needle.encode('utf-8') in blobs['engine/com.decennium.foundation/'+file])

    review=json.loads(blobs[AUTHORITY[6]])
    check('Actual source/dependency response and Codex agreement',review['responseId']=='a18c0728-47f3-5f33-8051-c89796f2864f'
        and review['status']=='ACTUAL_SOURCE_DEPENDENCY_REVIEW_CODEX_AGREES_EXP07_CONTRACT_ONLY')
    check('Accepted engine and actual Long Rest review',json.loads(blobs[AUTHORITY[7]])['sourceCommit']==ENGINE)
    check('Original1553 qualification retained',json.loads(blobs[AUTHORITY[9]])['fullRegression']['passed']==1553)
    mapping={x['id']:x for x in json.loads(blobs[AUTHORITY[5]])['workItems']}
    check('EXP07 direct dependencies unchanged',mapping['EXP-07']['dependencies']==['TAC-01','TAC-02','EXP-01','MGT-01'])
    check('CHR03/CHR05 map remains unchanged',mapping['CHR-03']['dependencies']==['CHR-02'] and mapping['CHR-05']['dependencies']==['CHR-03','TAC-02','TAC-05','TAC-08'])
    warrior=json.loads(blobs[GAMEPLAY[0]]);card=warrior['cards'][8]
    check('Warrior remains provisional draft',warrior['status']=='provisional-card-draft-not-balance-approved')
    check('Exact fear source acquisition and cost',card['id']=='warrior.base.intimidating-presence' and card['minimumClassLevel']==2
        and card['acquisition']=='selection' and card['activation']=='Action' and card['cost']=='0')
    check('Exact fear range/recharge',card['rangeAndTarget']=='Up to 3 enemies of your choice within 15 feet that can see or hear you'
        and card['frequency']=='Recharge 3 rounds' and card['duration']=='Maximum 2 rounds')
    check('DC uses ordinary ability modifier', 'Warrior technique save DC = 8 + normal character proficiency bonus + chosen modifier.' in warrior['engine'][0])
    combat=blobs[GAMEPLAY[2]].decode('utf-8')
    check('Source has distinct player and NPC ties','Players choose player/player ties; the Director resolves ties involving NPCs.' in combat)
    check('Source initial Reaction is distinct from regular refresh','Begin an encounter with one available Reaction unless surprised or otherwise prohibited.' in combat)
    check('Original virtual effect markers survive schedule changes','Existing effects keep that **virtual marker**' in combat)
    for file,needle,name in [
        ('Laboratory/Model/TestOnlySharedWorldPolicy.cs','InitializeLaterEncounter(s);','Earlier defender is initialized before encounter entry'),
        ('Laboratory/Model/SharedLaterEncounter.cs','state.Actors = state.Actors.Append','Existing world actor creation is explicit'),
        ('Laboratory/Model/SharedLaterEncounter.cs','if (command.Kind == CommandKind.EndFixedEncounter) RecordClericObjectiveCompletion(state, closed);','Earlier objective producer is closure-qualified'),
        ('Laboratory/Model/SharedWorldCombatPolicy.cs','return s.Lives.Single(x => x.ActorId == opponent).Dead;','Current conflict resolves by actual opponent death'),
        ('Laboratory/Model/SharedFrightened.cs','state.AbilityRecharges = new[]','Current fear payment replaces a singleton recharge array; extension required'),
        ('Runtime/Core/FrightenedRecords.cs','state.WarriorAbilityChoices.Length == 1','Current fear validation assumes one owner; extension required'),
        ('Laboratory/Model/SharedCharacterAdvancement.cs','epoch.Id != before.EpochId','Current recharge rejects different owning epoch; preserve explicit transfer semantics'),
        ('Laboratory/Model/SharedResonance.cs','(postClosure ? 2 : 1)','Current Healing Rite class/context gate needs explicit earned2 tactical extension'),
        ('Laboratory/Model/SharedRadiance.cs','s.InventoryCombat || s.Encounter != null','Current Radiance owns only ordinary post-closure context'),
        ('Laboratory/Model/SharedSpellCasting.cs','SpellcastingCalendarUnsupported','Current casting epoch restriction must be extended explicitly'),
        ('Laboratory/Model/SharedDailyProvisioning.cs','actors.Length > 2','Current daily obligations are bounded to two party actors'),
        ('Laboratory/Model/SharedCharterAttempt.cs','attempt.Authority.HeroId != command.Actor || attempt.Returned != null','Completed charter and companion movement do not reopen its departure gate'),
        ('Laboratory/Model/TestOnlyPolicy.cs','x >= 0 && x < 5 && y >= 0 && y < 5 && !(x == 2 && y == 1)','Candidate route uses the actual bounded walkable map'),
        ('Laboratory/Model/SharedConnectedExplorationObservation.cs','new ObservationFixture(5, 5','Existing observation map is5x5'),
        ('Laboratory/Model/ActorLifeRules.cs','new CharacterLevelFact("Warrior",12),new CharacterLevelFact("Warrior",7),new CharacterLevelFact("Warrior",7)','Proposed numerical body reuses exact existing26HP template'),
    ]:
        contains(file,needle,name)
    views=[]
    for name in VIEWS:
        raw=blobs[VIEW_ROOT+name]; view=json.loads(raw)
        views.append({'path':VIEW_ROOT+name,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),
            'revision':view['Revision'],'clock':view['Clock'],'inEncounter':view['InEncounter'],
            'visibleActorFacts':[{'position':a['Position'],'hp':a['Hp'],'maximumHp':a['MaximumHp'],
                'conditions':a['Conditions'],'cleric':a.get('Cleric'),'casting':a.get('Casting')} for a in view['Actors']]})
    paid=json.loads(blobs[VIEW_ROOT+VIEWS[-1]])
    hero=next(a for a in paid['Actors'] if a['Position']['Id']=='TEST_ONLY.actor')
    ally=next(a for a in paid['Actors'] if a['Position']['Id']=='TEST_ONLY.companion')
    check('Authentic paid-care hero is fully healed at0,2',hero['Hp']==26 and hero['Position']['X']==0 and hero['Position']['Y']==2)
    check('Authentic paid-care companion remains13HP at1,3',ally['Hp']==13 and ally['Position']['X']==1 and ally['Position']['Y']==3)
    route={'companion':[(1,3),(2,3),(3,3),(3,4)],'hero':[(0,2),(1,2),(2,2),(3,2),(3,3)]}
    check('Proposed routes have only ordinary cardinal neighbor edges',all(abs(a[0]-b[0])+abs(a[1]-b[1])==1 for path in route.values() for a,b in zip(path,path[1:])))
    check('Proposed route coordinates are within known map and avoid blocked2,1',all(0<=x<5 and 0<=y<5 and (x,y)!=(2,1) for path in route.values() for x,y in path))
    check('Proposed contact has three distinct anchors in fear range',len({(3,3),(3,4),(4,4)})==3 and all(5*max(abs(x-4),abs(y-4))<=15 for x,y in [(3,3),(3,4)]))
    write('SOURCE_BINDINGS.json',{'baseline':BASELINE,'acceptedEngine':ENGINE,'sourceRevision':SOURCE,'sources':bindings})
    write('SELECTED_SOURCE_EXTRACTS.json',{'sourceRevision':SOURCE,'warriorStatus':warrior['status'],
        'enginePointer':'/engine/0','engine':warrior['engine'][0],'cardPointer':'/cards/8','card':card,
        'note':'Exact provisional source; new actor entitlement remains proposed for actual contract review.'})
    write('BASELINE_ROUTE_INSPECTION.json',{'status':'READ_ONLY_RETAINED_VIEWS_AND_MAP_INSPECTION','evidenceCommit':EVIDENCE,'views':views,
        'proposedPaidRoutes':route,'newActorPosition':[4,4],
        'limits':'Filtered views are not a full world trace. Geometry arithmetic is not actual traversal, complete occupancy/authority proof, actor admission or runtime reachability. No new actor/route was executed. Exact new-profile upstream/approach evidence remains required after approval.'})
    write('SOURCE_AUDIT.json',{'status':'PASS_SOURCE_ONLY_CONTRACT_AUDIT','baseline':BASELINE,'acceptedEngine':ENGINE,'sourceRevision':SOURCE,
        'pinnedBlobs':len(bindings),'checks':checks,'engineChanged':False,'compilationExecuted':False,'runtimeExecuted':False,
        'contractApproval':'PENDING_ACTUAL_GPT_REVIEW','limits':'Pins and source/API checks do not prove new profile construction, route reachability, timing correctness or gameplay. Proposed fixture facts are not source authority.'})
    print(f'SOURCE-ONLY PASS: {len(bindings)} pinned blobs; {len(checks)} checks; engine unchanged; no C# or gameplay run.')


if __name__=='__main__':
    main()
