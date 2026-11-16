"""Source/API contract audit only. No C# execution and no runtime approval.

Writes only this packet's derived JSON reports; reads exact Git blobs in one batch.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
BASELINE = '64e93efd1349998fb266096b1178f3cffebf2849'
ENGINE = '6d840c4dfce268115904ea0dda6b475450f7be6f'
SOURCE = '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
PREFIX = 'engine/com.decennium.foundation/'
OLD = PACKET.parent/'2026-11-16-chr03-bishop-entry'


def write(name, value):
    (PACKET/name).write_bytes((json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode())


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def main():
    old = json.loads((OLD/'SOURCE_BINDINGS.json').read_text(encoding='utf-8'))
    requests = {}
    for item in old['sources']:
        path = item['path']
        revision = ENGINE if path.startswith('engine/') else SOURCE if item['role']=='selected-provisional-source' else BASELINE
        requests[path] = (revision, item['role'])
    extra = [
        'docs/unity/evidence/2026-11-16-chr03-bishop-entry/GPT_SOURCE_REVIEW.md',
        'docs/unity/evidence/2026-11-16-exp07-post-recovery/APPROVED_CONTRACT.md',
        'docs/unity/evidence/2026-11-16-exp07-post-recovery/GPT_FINAL_REVIEW.md',
        'docs/unity/evidence/2026-11-16-exp07-post-recovery/implementation/RESULTS.json',
    ]
    for path in extra:
        requests[path] = (BASELINE, 'accepted-boundary')
    code = [
        'Laboratory/Model/SharedPostRecoveryEncounter.cs', 'Laboratory/Model/SharedRadiance.cs',
        'Laboratory/Model/SharedResonance.cs', 'Laboratory/Model/SharedSanctuary.cs',
        'Laboratory/Model/SharedShortRest.cs', 'Laboratory/Model/ActorLifeRules.cs',
        'Laboratory/Model/PlaytestDamageDice.cs', 'Laboratory/Model/PlaytestLife.cs',
        'Runtime/Core/SpellCastingValidation.cs', 'Runtime/Core/SpellCastingHistory.cs',
        'Runtime/Core/SpellCastingRecords.cs', 'Runtime/Core/SpellRepertoireRecords.cs',
        'Runtime/Core/ClericLongRestRecords.cs', 'Runtime/Core/PostRecoveryEncounterRecords.cs',
        'Runtime/Core/PostRecoveryEncounterValidation.cs',
        'Tests/EditMode/PostRecoveryEncounterCases.cs', 'Tests/EditMode/ConnectedClericLongRestCases.cs',
        'Runtime/Persistence/SpellCastingCodec.cs', 'Runtime/Persistence/SnapshotCodec.cs',
    ]
    for path in code:
        requests[PREFIX+path] = (ENGINE, 'accepted-engine-api')
    # Search all tracked laboratory C# for save-producing interfaces. This is a
    # candidate inventory, not a claim that string matching proves completeness.
    all_code = git('ls-tree', '-r', '--name-only', ENGINE, '--', PREFIX+'Laboratory/Model').decode().splitlines()
    candidates = []
    for path in all_code:
        if not path.endswith('.cs'):
            continue
        raw = (ROOT/path).read_bytes()
        lines = raw.decode('utf-8-sig').splitlines()
        hits = [{'line': i+1, 'text': line.strip()} for i,line in enumerate(lines)
                if re.search(r'SaveProficiencyBonus|SavingThrowModifier|PlaytestRolls\.SavingThrow|SaveAtMarker|ConstitutionSaveModifier', line)]
        if hits:
            candidates.append({'path': path, 'hits': hits})
            requests[path] = (ENGINE, 'save-consumer-audit')
    ordered = sorted(requests.items())
    payload = ''.join(revision+':'+path+'\n' for path,(revision,_) in ordered).encode()
    result = subprocess.run(['git','cat-file','--batch'], cwd=ROOT, input=payload,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    position, bindings, blobs = 0, [], {}
    for path,(revision,role) in ordered:
        end = result.stdout.index(b'\n', position)
        header = result.stdout[position:end].decode().split()
        assert len(header)==3 and header[1]=='blob', (path,header)
        length = int(header[2]); position = end+1
        raw = result.stdout[position:position+length]; position += length+1
        local = (ROOT/path).read_bytes()
        assert local==raw or local.replace(b'\r\n',b'\n')==raw, 'Checkout differs: '+path
        blobs[path] = raw
        bindings.append({'path':path,'revision':revision,'role':role,'gitBlob':header[0],
                         'bytes':length,'sha256':hashlib.sha256(raw).hexdigest(),
                         'checkoutRelation':'exact' if local==raw else 'CRLF-only; preserved'})
    assert position==len(result.stdout) and not result.stderr.strip()
    assert not git('diff', ENGINE, '--', 'engine').strip(), 'Engine must remain unchanged at this contract gate'
    checks = []

    def check(name, value):
        assert value, name
        checks.append(name)

    def contains(path, needle):
        return needle.encode() in blobs[PREFIX+path]

    rules = 'DescentReviewChanges/ReviewBible/'
    cleric = json.loads(blobs[rules+'data/public/class_playtests/cleric.json'])
    spells = json.loads(blobs[rules+'data/public/spell_playtests/catalog.json'])['spells']
    by_id = {s['id']:s for s in spells}
    check('Cleric remains provisional', cleric['status']=='provisional-card-draft-not-balance-approved')
    check('Exactly two Arch selections and one Active at3', cleric['schedule'][2]=={'classLevel':3,'choose':2,'bands':['Arch'],'minimumActives':1,'asiOrFeat':False})
    check('RP4to7 rank1to2', cleric['rpByClassLevel'][1:3]==[4,7] and cleric['maxSpellRankByClassLevel'][1:3]==[1,2])
    check('Selected exact cards', [cleric['cards'][i]['id'] for i in [16,23]]==['cleric.arch.aura-of-faith','cleric.arch.divine-invocation'])
    check('Actual Dispel source rank and cost', by_id['dispel-magic-lesser']['classAccess']['Cleric']=={'rank':2,'minimumClassLevel':3,'school':'Abjuration','baseRpCost':3})
    check('Guidance is persistent without concentration', by_id['guidance']['operational']['concentration'] is False and '1 minute' in by_id['guidance']['operational']['duration'])
    check('Detect supplies visible outlines, not exact ranks', 'visible outline' in by_id['detect-magic']['operational']['effect'] and 'ranks' in by_id['detect-magic']['operational']['limitations'])
    check('Dispel itself does not replace concentration', by_id['dispel-magic-lesser']['operational']['concentration'] is False)
    check('Arcane Ward expires at next caster Start', by_id['arcane-ward']['operational']['duration']=='Until the start of your next regular turn')
    mapping = {x['id']:x for x in json.loads(blobs['docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json'])['workItems']}
    for name, deps in [('CHR-03',['CHR-02']),('EXP-07',['TAC-01','TAC-02','EXP-01','MGT-01']),('CHR-05',['CHR-03','TAC-02','TAC-05','TAC-08'])]:
        check(name+' dependencies unchanged', mapping[name]['dependencies']==deps)
    api_checks = [
        ('Laboratory/Model/SharedClericSettlement.cs','character.Levels.Count != 1','Existing settlement admits only earned2'),
        ('Runtime/Core/ClericSettlementValidation.cs','advances.Length > 1','Existing validator requires versioned second advancement admission'),
        ('Laboratory/Model/SharedResonance.cs','? 2 : 1)','Rite requires explicit level3 integration'),
        ('Runtime/Core/SpellRepertoireRecords.cs','if (spell == "dispel-magic-lesser") return "SpellClassLevelDenied";','Dispel acquisition remains explicitly denied'),
        ('Runtime/Core/SpellCastingHistory.cs','classLevel > 2','Casting history requires versioned level3 admission'),
        ('Runtime/Core/ClericLongRestValidation.cs','conviction != 5','Conviction spending requires a causal ordered history'),
        ('Runtime/Core/ClericLongRestValidation.cs','s.HealingRites.Select','RP history must add Invocation alongside actual old debits'),
        ('Laboratory/Model/SharedSpellCasting.cs','AuraObservationId','Opaque individual outlines already exist'),
        ('Laboratory/Model/SharedSpellCasting.cs','ConcentratingSpell(spell)','Concentration replacement is source-specific'),
        ('Laboratory/Model/SharedSpellCasting.cs','activities.Any(x=>x.IsMagical)','Magical activity excludes idle decay'),
        ('Laboratory/Model/SharedSpellEffects.cs','SpellSaveKind.ConcentrationConstitution','Concentration is a required real save consumer'),
        ('Tests/EditMode/ConnectedClericLongRestCases.cs','bool eligible=endpoint>=172800','Existing genuine second beneficial rest boundary'),
        ('Tests/EditMode/PostRecoveryEncounterCases.cs','PostRecoveryStep(session,companion,1,0);','Existing paid eastward berth departure'),
    ]
    for file, needle, name in api_checks:
        check(name, contains(file, needle))
    check('Actual final EXP07 acceptance retained', b'7ed650ba-0d52-5376-9188-7ee179d7d397' in blobs[extra[2]])
    check('All1566 accepted predecessors retained', json.loads(blobs[extra[3]])['passed']==1566)
    extracts = {'sourceRevision':SOURCE,'authority':'provisional operational drafts; no production promotion',
                'cards':[{'pointer':'/cards/'+str(i),'card':cleric['cards'][i]} for i in [16,23]],
                'spells':[{'pointer':'/spells/'+str(spells.index(by_id[i])),'card':by_id[i]} for i in ['dispel-magic-lesser','guidance','detect-magic','arcane-ward','sanctuary']]}
    write('SOURCE_BINDINGS.json',{'baseline':BASELINE,'acceptedEngine':ENGINE,'sourceRevision':SOURCE,'sources':bindings})
    write('SOURCE_EXTRACTS.json', extracts)
    write('SAVE_CONSUMER_INVENTORY.json',{'scope':'Candidate audit from all tracked Laboratory/Model C#; requires semantic review at implementation',
           'acceptedEngine':ENGINE,'files':candidates,'fileCount':len(candidates),
           'mandatoryConsumers':['initial/repeat fear','Sanctuary','concentration','Wound saves for all admitted damage producers',
                                 'Overwatch Push','Suppression Fire','trap DEX/CON','unconscious death saves: no perception, no Aura bonus'],
           'notSaves':['attacks','Guidance ability checks','initiative unless explicitly a check','ordinary skills']})
    write('SOURCE_AUDIT.json',{'status':'PASS_SOURCE_ONLY','baseline':BASELINE,'acceptedEngine':ENGINE,
          'pinnedBlobs':len(bindings),'checks':checks,'engineChanged':False,'compilationExecuted':False,'runtimeExecuted':False,
          'runtimeApproval':'NOT_GRANTED','limitations':'Source/API findings are not executed Bishop gameplay or reachability proof.'})
    print(f'SOURCE-ONLY PASS: {len(bindings)} pinned blobs; {len(checks)} checks; {len(candidates)} save-candidate files; engine unchanged.')


if __name__=='__main__':
    main()
