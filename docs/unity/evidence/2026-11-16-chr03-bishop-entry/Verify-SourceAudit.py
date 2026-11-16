"""Read-only source/API audit for the Bishop-entry dependency proposal; no engine execution."""
import hashlib
import json
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
BASELINE = '70e697de4890ed292485804957dd03b34b643158'
ENGINE = 'e0994929b444b15fc38957eb80cc34ab19d56db6'
SOURCE = '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
AUTHORITY = [
    'CANON_MANIFEST.md', 'docs/canon/CANON_MANIFEST.json', 'docs/canon/REPOSITORY_PROMOTION.md',
    'docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md', 'docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json',
    'docs/unity/evidence/2026-11-15-mgt03-cleric-long-rest/GPT_FINAL_REVIEW.json',
    'docs/unity/evidence/2026-11-15-mgt03-cleric-long-rest/SOURCE_API_CONTRACT.md',
    'docs/unity/evidence/2026-11-15-mgt03-cleric-long-rest/implementation/RESULTS.json',
    'docs/unity/evidence/2026-11-15-chr05-cleric-conviction/SOURCE_API_FINDINGS.md',
    'docs/unity/evidence/2026-11-15-chr03-cleric-settlement/SETTLEMENT_CONTRACT.md',
    'docs/unity/evidence/2026-11-15-chr03-cleric-settlement/GPT_FINAL_REVIEW.md',
    'docs/unity/evidence/2026-11-15-tac08-cleric-casting/APPROVED_CASTING_CONTRACT.md',
    'docs/unity/evidence/2026-11-15-tac07-cleric-repertoire/SOURCE_API_CONTRACT.md',
]
GAMEPLAY = [
    'DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json',
    'DescentReviewChanges/ReviewBible/data/playtest/class_sources/cleric.json',
    'DescentReviewChanges/ReviewBible/data/playtest/character_foundation.json',
    'DescentReviewChanges/ReviewBible/docs/mechanics/classes/cleric.md',
    'DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md',
    'DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',
    'DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_BUILD_EXAMPLES.md',
    'DescentReviewChanges/ReviewBible/docs/mechanics/XP_ADVANCEMENT_CANON.md',
    'DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md',
    'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json',
    'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json',
    'docs/reference/Player_Rulebook_v6_source_text.txt',
    'src/data/spells.js', 'src/data/class-spell-progression.js',
    'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json',
]
CODE = [
    'Laboratory/Model/SharedClericSettlement.cs', 'Laboratory/Model/SharedClericLongRest.cs',
    'Laboratory/Model/SharedWorldCombatPolicy.cs', 'Laboratory/Model/SharedLaterEncounter.cs',
    'Laboratory/Model/SharedRetreat.cs', 'Laboratory/Model/SharedReengagement.cs',
    'Laboratory/Model/SharedFrightened.cs', 'Laboratory/Model/SharedSpellCasting.cs',
    'Laboratory/Model/SharedSpellEffects.cs', 'Laboratory/Model/SharedSpellRepertoire.cs',
    'Laboratory/Model/ConnectedExpeditionSession.cs', 'Laboratory/Model/ClassAdvancementScheduleCatalog.cs',
    'Laboratory/Model/ClassAdvancementOptionCatalog.cs', 'Runtime/Core/ClericSettlementRecords.cs',
    'Runtime/Core/ClericSettlementValidation.cs', 'Runtime/Core/ClericLongRestValidation.cs',
    'Runtime/Core/FrightenedRecords.cs', 'Runtime/Core/SpellCastingProfile.cs',
    'Runtime/Core/CharacterAdvancementRecords.cs', 'Runtime/Core/ResonanceRecords.cs',
    'Runtime/Persistence/ClericSettlementCodec.cs', 'Runtime/Persistence/ClericLongRestCodec.cs',
]


def write(name, value):
    (PACKET/name).write_bytes((json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode())


def main():
    requests = [(BASELINE, p, 'authority-or-accepted-boundary') for p in AUTHORITY]
    requests += [(SOURCE, p, 'selected-provisional-source') for p in GAMEPLAY]
    requests += [(ENGINE, 'engine/com.decennium.foundation/'+p, 'accepted-engine-api') for p in CODE]
    payload = ''.join(rev+':'+path+'\n' for rev,path,_ in requests).encode()
    result = subprocess.run(['git','cat-file','--batch'], cwd=ROOT, input=payload,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    position, bindings, blobs = 0, [], {}
    for revision,path,role in requests:
        end = result.stdout.index(b'\n',position)
        header = result.stdout[position:end].decode().split()
        assert len(header)==3 and header[1]=='blob', (path,header)
        length = int(header[2]); position=end+1
        raw = result.stdout[position:position+length]; position+=length+1
        local = (ROOT/path).read_bytes()
        assert local==raw or local.replace(b'\r\n',b'\n')==raw, 'Source checkout differs: '+path
        blobs[path]=raw
        bindings.append({'path':path,'revision':revision,'role':role,'gitBlob':header[0],
                         'bytes':length,'sha256':hashlib.sha256(raw).hexdigest(),
                         'checkoutRelation':'exact' if local==raw else 'CRLF-only; preserved'})
    assert position==len(result.stdout) and not result.stderr.strip()
    assert not subprocess.check_output(['git','diff',ENGINE,'--','engine'],cwd=ROOT).strip()
    checks=[]

    def check(name, condition):
        assert condition, name
        checks.append(name)

    cleric=json.loads(blobs[GAMEPLAY[0]])
    check('Cleric draft authority retained',cleric['status']=='provisional-card-draft-not-balance-approved')
    check('Exact level3 schedule',cleric['schedule'][2]=={'classLevel':3,'choose':2,'bands':['Arch'],'minimumActives':1,'asiOrFeat':False})
    check('RP4to7 and rank1to2',cleric['rpByClassLevel'][1:3]==[4,7] and cleric['maxSpellRankByClassLevel'][1:3]==[1,2])
    check('Candidate cards have legal distinct slots',[(cleric['cards'][i]['id'],cleric['cards'][i]['minimumClassLevel'],cleric['cards'][i]['sourceKind']) for i in [16,23]]==[('cleric.arch.aura-of-faith',3,'passive'),('cleric.arch.divine-invocation',3,'active')])
    check('Legal example preserves proposed pair',b'| 3 | Divine Invocation; Aura of Faith |' in blobs[GAMEPLAY[6]])
    check('Self ally is explicitly sourced',b'\xe2\x80\x9cAlly\xe2\x80\x9d includes self unless it says OTHER.' in blobs[GAMEPLAY[4]])
    check('Milestones must be announced before opening',b'other milestones announced before the Opening begins' in blobs[GAMEPLAY[7]])
    check('No advancement recovery',b'Keep current HP and spent resources unchanged' in blobs[GAMEPLAY[5]])
    catalog=json.loads(blobs[GAMEPLAY[9]]); spell=catalog['spells'][33]
    check('Candidate Dispel exact identity and class placement',spell['id']=='dispel-magic-lesser' and spell['classAccess']['Cleric']=={'rank':2,'minimumClassLevel':3,'school':'Abjuration','baseRpCost':3} and spell['additionalRpCost']==0)
    authored=json.loads(blobs[GAMEPLAY[10]]); entry=next(x for x in authored['entries'] if x['id']==spell['id'])
    check('Dispel authored review binds same whole card',entry['authoredStatus']=='reviewed-authored-operational-playtest' and entry['wholeCardPointer']=='/spells/33' and entry['procedurePointer']=='/spells/33/operational')
    check('Dispel preserves actual generating rank', 'actual recorded rank 0, 1 or 2' in spell['operational']['targets'])
    mapping={x['id']:x for x in json.loads(blobs[AUTHORITY[4]])['workItems']}
    check('CHR03 mapped dependency unchanged',mapping['CHR-03']['dependencies']==['CHR-02'])
    check('EXP07 proposed prerequisite uses existing map',mapping['EXP-07']['dependencies']==['TAC-01','TAC-02','EXP-01','MGT-01'])
    check('CHR05 mapped dependency unchanged',mapping['CHR-05']['dependencies']==['CHR-03','TAC-02','TAC-05','TAC-08'])
    prefix='engine/com.decennium.foundation/'
    for file,needle,name in [
        ('Laboratory/Model/SharedWorldCombatPolicy.cs','return s.Lives.Single(x => x.ActorId == opponent).Dead;','Resolved closure needs actual dead opponent'),
        ('Laboratory/Model/SharedLaterEncounter.cs','if (command.Kind == CommandKind.EndFixedEncounter) RecordClericObjectiveCompletion(state, closed);','Retreat cannot earn earlier Cleric2 objective'),
        ('Laboratory/Model/SharedReengagement.cs','CapableWorker(s, x) && TestOnlyClubAttackPolicy.Aware(s, x)','Reengagement needs same living capable defender'),
        ('Laboratory/Model/SharedFrightened.cs','state.Encounter?.Id != state.Reinforcement.Definition.EncounterId','Fear source remains encounter-restricted'),
        ('Runtime/Core/SpellCastingProfile.cs','if(c.Kind==CommandKind.StartIntake)return "UnsafeConsumableIntakeUnsupported";','Contamination is not an existing poisoning producer'),
        ('Laboratory/Model/SharedClericSettlement.cs','character.Levels.Count != 1','Current advancement is one fixed earned2 transaction'),
    ]:
        check(name,needle.encode() in blobs[prefix+file])
    accepted=json.loads(blobs[AUTHORITY[5]])
    check('Actual predecessor acceptance and source',accepted['responseId']=='0361603a-8572-5112-896a-d04663473407' and accepted['sourceCommit']==ENGINE)
    check('Accepted1553 baseline retained',json.loads(blobs[AUTHORITY[7]])['fullRegression']['passed']==1553)
    write('SOURCE_BINDINGS.json',{'baseline':BASELINE,'acceptedEngine':ENGINE,'sourceRevision':SOURCE,'scope':'Source/API dependency review only; no runtime approval','sources':bindings})
    write('SOURCE_AUDIT.json',{'status':'PASS_SOURCE_ONLY_DEPENDENCY_AUDIT','baseline':BASELINE,'acceptedEngine':ENGINE,
        'sourceRevision':SOURCE,'pinnedBlobs':len(bindings),'checks':checks,'engineChanged':False,
        'runtimeExecuted':False,'compilationExecuted':False,'proposalRuntimeApproval':'NOT_GRANTED',
        'remaining':'Actual source/API and dependency review; complete operational and connected-context contract before runtime.'})
    print(f'SOURCE-ONLY PASS: {len(bindings)} pinned blobs; {len(checks)} source/API checks; engine unchanged; no C# run.')


if __name__=='__main__':
    main()
