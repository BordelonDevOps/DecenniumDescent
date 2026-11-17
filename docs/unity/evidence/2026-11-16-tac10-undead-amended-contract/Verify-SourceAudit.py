"""Source-only TAC-10 amendment audit. No C# execution or runtime authorization."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
BASELINE = 'e7f7ac179170e491f2e628f46de4441165551f12'
ENGINE = '7261052ae4dec908f8c0ac38e0a2c5f4b831065b'
SOURCE = '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
CODE = 'engine/com.decennium.foundation/'
OLD = 'docs/unity/evidence/2026-11-16-tac10-undead-contract/'
GEO = 'docs/unity/evidence/2026-11-16-tac03-declared-geometry-runtime/'
RB = 'DescentReviewChanges/ReviewBible/'
FERRY = 'docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack/Monster_Manual_of_the_Known_Descent_Source/entries/ferry-wraith-of-the-hush.md'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def write(name, value):
    (PACKET / name).write_bytes((json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode())

def main():
    assert not git('diff', ENGINE, '--', 'engine').strip(), 'Frozen engine changed before review'
    old = json.loads((ROOT/OLD/'SOURCE_BINDINGS.json').read_text(encoding='utf-8-sig'))
    sources = {x['path']: (ENGINE if x['path'].startswith(CODE) else SOURCE if x['revision']==SOURCE else BASELINE) for x in old['sources']}
    for name in ['SOURCE_API_CONTRACT.md','SOURCE_API_DECISIONS.md','GPT_SOURCE_API_REVIEW.json','Verify-SourceAudit.py']:
        sources[OLD+name] = BASELINE
    for name in ['GPT_FINAL_REVIEW.json','final/FINAL_RECONCILIATION.json','final/QUALIFICATION_MEMBERS.json','SOURCE_TRACE.md','CONSUMER_RECONCILIATION.json']:
        sources[GEO+name] = BASELINE
    cs = [p for p in git('ls-tree','-r','--name-only',ENGINE,'--',CODE).decode().splitlines() if p.endswith('.cs')]
    sources.update({p:ENGINE for p in cs})
    batch = subprocess.run(['git','cat-file','--batch'], cwd=ROOT, input=''.join(rev+':'+p+'\n' for p,rev in sorted(sources.items())).encode(), stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    pos,blobs,bindings=0,{},[]
    for p,rev in sorted(sources.items()):
        end=batch.stdout.index(b'\n',pos); head=batch.stdout[pos:end].decode().split()
        assert len(head)==3 and head[1]=='blob', (p,head)
        size=int(head[2]); pos=end+1; raw=batch.stdout[pos:pos+size]; pos+=size+1
        local=(ROOT/p).read_bytes()
        assert local==raw or local.replace(b'\r\n',b'\n')==raw,p
        blobs[p]=raw
        bindings.append(dict(path=p,revision=rev,gitBlob=head[0],bytes=size,sha256=hashlib.sha256(raw).hexdigest(),checkoutRelation='exact' if raw==local else 'CRLF-only'))
    assert pos==len(batch.stdout) and not batch.stderr
    text=lambda p:blobs[p].decode('utf-8-sig')
    parsed=lambda p:json.loads(text(p))
    patterns={
        'numeric':r'CharacterRuleFacts|CharacterStateFacts|\.Characters\b|PrototypeArmor|UnarmoredBaseAc',
        'proficiency':r'ProficiencyBonus|proficiencyBonus|\bPB\b',
        'damage-defense':r'Resistan|Immunit|DamageType|DamageFlavor|ReduceIncomingDamage|PetrifiedDamage',
        'life':r'UsesDeathSaves|ActorLifeValidation|LivingRecipient',
        'attack-continuation':r'OrdinaryUnarmed|OpportunityAttackCommand|SanctuaryAttackSource|PendingSanctuary|SanctuaryTargetProhibited',
        'epoch':r'PostRecoveryProfile|PostRecoveryEncounter\??\.Admission|Reinforcement\??\.Admission|WorldTiming\.',
        'object-perception':r'AvailableHands|GeometricSight|DirectSightAt|ClearLineSight|LineOfEffect',
        'physical-seal-commands':r'\bDisarm\b|\bSunder\b|\bImprovise\b|DestroySeal|InvalidateSeal',
    }
    searches={}
    for label,pattern in patterns.items():
        rows=[]
        for p in cs:
            if '/Tests/' in p: continue
            hits=[dict(line=i+1,text=line.strip()) for i,line in enumerate(text(p).splitlines()) if re.search(pattern,line)]
            if hits: rows.append(dict(path=p,hits=hits))
        searches[label]=dict(pattern=pattern,excludesTests=True,matchedFiles=len(rows),matchedLines=sum(len(r['hits']) for r in rows),rows=rows)
    checks=[]
    def check(name,value):
        assert value,name
        checks.append(dict(name=name,passed=True))
    review=parsed(GEO+'GPT_FINAL_REVIEW.json')
    check('Actual geometry acceptance and Codex agreement',review['responseId']=='9e7360a4-f81d-5f06-8884-49e8ef8eda0a' and review['codexAgreement']['accepted'])
    check('Frozen engine and exact final evidence',review['sourceCommit']==ENGINE and review['evidenceCommit']=='cd60eacd075b8ed4b4738fd9effed19ecf6c1237')
    prior=parsed(OLD+'GPT_SOURCE_API_REVIEW.json')
    check('Actual earlier Undead review retained',prior['responseId']=='2d01541e-6b9d-54c0-88a7-0db0f65bc6af')
    decisions=text(OLD+'SOURCE_API_DECISIONS.md')
    check('Settled decisions and mandatory corrections retained',all(x in decisions for x in ['U-NUM-01','U-LIFE-01','U-DEF-01','U-ATK-01','U-SEAL-01','U-SEAL-02','U-EVID-01','affected creature','current post-recovery']))
    mapping=parsed('docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json')
    item=lambda name:next(x for x in mapping['workItems'] if x['id']==name)
    check('Approved dependencies unchanged',item('TAC-03')['dependencies']==['CHR-01','TAC-01'] and item('TAC-10')['dependencies']==['TAC-03','TAC-04','TAC-05','TAC-02'] and item('CHR-05')['dependencies']==['CHR-03','TAC-02','TAC-05','TAC-08'])
    raw=text(FERRY); candidate=parsed(RB+'data/playtest/bestiary_public_source_candidate.json')
    ferry=next(x for x in candidate['records'] if x['id']=='ferry-wraith-of-the-hush')
    check('Parsed candidate remains uninstalled',not candidate['runtimeInstalled'] and ferry['reviewStatus']=='SOURCE_BOUND_NOT_OPERATIONALLY_REVIEWED')
    check('Canonical Ferry source exact modulo CRLF',ferry['source']['originalUtf8Text'].replace('\r\n','\n')==raw.replace('\r\n','\n'))
    check('Printed identity and numeric facts',all(x in raw for x in ['Medium Undead','Armor** 10','Hit Points** 9','Speed** 40 ft.','12 (+1) | 14 (+2) | 14 (+2) | 9 (-1) | 11 (+0) | 16 (+3)']))
    check('Separate defenses and DC',all(x in raw for x in ['**Resistances** necrotic','**Immunities** poison','**Condition Immunities** poisoned','**Save DC** 13']))
    check('Printed attack, trait, knowledge and harvest',all(x in raw for x in ['+3 to hit','1d4 fire','until the end of the next round','DC 19','45%, 10 gp base']))
    check('No printed senses/darkvision',not re.search(r'darkvision|\*\*Senses',raw,re.I))
    check('Generic Bleeding requires affected creature PB','affected creature\'s regular turn, take damage equal to its current PB' in text(RB+'docs/mechanics/CONDITIONS_PLAYTEST.md'))
    check('Character-origin invariant requires versioned union','!actors.SequenceEqual(s.Characters.Select' in text(CODE+'Runtime/Core/ActorLifeRecords.cs'))
    check('Old opportunity fallback assumption exists','Every reactor has a usable ordinary unarmed attack' in text(CODE+'Laboratory/Model/TacticalMovementPolicy.cs'))
    check('Current opportunity dispatch needs source generalization','unarmed ? CommandKind.AttackUnarmed : CommandKind.AttackClub' in text(CODE+'Laboratory/Model/TacticalMovementPolicy.cs'))
    check('Sanctuary cached interval prohibition exists','SanctuaryTargetProhibitedThisInterval' in text(CODE+'Laboratory/Model/SharedSanctuary.cs'))
    check('Old calendar registration explicitly bounded','PostRecoveryProfile.IsEpoch' in text(CODE+'Runtime/Core/SpellCastingValidation.cs'))
    check('Actual shared declared geometry adapter exists','DeclaredGeometryProfile.SupportsAnchorAt' in text(CODE+'Laboratory/Model/SharedDeclaredGeometry.cs'))
    check('No existing named physical seal command',searches['physical-seal-commands']['matchedLines']==0)
    check('Old cross-roster combat restriction explicit','TargetOutsideEncounter' in text(CODE+'Laboratory/Model/SharedWorldCombatPolicy.cs'))
    check('Source audit covers full frozen Csharp tree including deferred Unity files',len(cs)==461)
    archive=ROOT/GEO/'final/qualification-final.zip'
    archive_sha=hashlib.sha256(archive.read_bytes()).hexdigest()
    check('Accepted archive SHA matches actual final retention',archive_sha=='45ebff77c7fb1c39517f76c64ca5f60e1f4040c9155fa57be0bb59d24a707b72')
    member='qualification/connected-paths/ConsoleUninterrupted/geometry-continued.ddsave.Player.view.json'
    other='qualification/connected-paths/ConsoleUninterrupted/geometry-continued.ddsave.RecoveryOpponent.view.json'
    with zipfile.ZipFile(archive) as z:
        pb=z.read(member); ob=z.read(other)
    view=json.loads(pb); ov=json.loads(ob)
    hero=next(x for x in view['Actors'] if x['Position']['Id']=='TEST_ONLY.actor')
    cleric=next(x for x in view['Actors'] if x['Position']['Id']=='TEST_ONLY.companion')
    check('Retained paid route terminal source facts',view['Revision']==327 and not view['InEncounter'] and hero['Position']==dict(Id='TEST_ONLY.actor',X=7,Y=2) and hero['Hp']==17 and cleric['Cleric']['CurrentRp']==7 and cleric['Hp']==18)
    check('Prior opponent remains dead body at5,3',ov['Actors'][0]['Dead'] and ov['Actors'][0]['Position']==dict(Id='TEST_ONLY.recovery-defender',X=5,Y=3))
    write('ROUTE_BASELINE.json',dict(scope='Read-only extract of accepted geometry113 evidence; no new profile or proposed route executed',archivePath=GEO+'final/qualification-final.zip',archiveSha256=archive_sha,members=[dict(path=member,sha256=hashlib.sha256(pb).hexdigest()),dict(path=other,sha256=hashlib.sha256(ob).hexdigest())],revision=view['Revision'],clock=view['Clock'],hero={k:hero[k] for k in ['Position','Hp','MaximumHp']},companion={k:cleric[k] for k in ['Position','Hp','MaximumHp','Cleric']},priorOpponent={k:ov['Actors'][0][k] for k in ['Position','Hp','Dead']}))
    check('No engine modification',not git('diff',ENGINE,'--','engine').strip())
    write('SOURCE_BINDINGS.json',dict(baseline=BASELINE,acceptedEngine=ENGINE,sourceRevision=SOURCE,sources=bindings))
    write('API_CONSUMERS.json',dict(searchedTrackedCsharpFiles=len(cs),searches=searches,limits='Lexical inventory. Required dispositions are proposals until implementation and execution prove admission gates and indirect paths. No claim of semantic completeness.'))
    write('SOURCE_EXTRACTS.json',dict(canonicalPath=FERRY,canonicalText=raw,candidate=ferry,selectedSourceRules={p:text(p) for p in sources if p.startswith(RB+'docs/mechanics/')},scope='Source evidence; operational consensus is separately bound to actual reviews.'))
    report=dict(status='PASS_SOURCE_AUDIT_AWAITING_ACTUAL_AMENDED_CONTRACT_REVIEW',baseline=BASELINE,acceptedEngine=ENGINE,sourceRevision=SOURCE,auditToolSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),pinnedBlobs=len(bindings),searchedTrackedCsharpFiles=len(cs),searchCounts={k:dict(files=v['matchedFiles'],lines=v['matchedLines']) for k,v in searches.items()},checks=checks,engineUnchanged=True,newCompilation=False,newGameplay=False,runtimeAuthorized=False)
    write('SOURCE_AUDIT.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='checks'}|dict(checks=len(checks))))

if __name__=='__main__':
    main()
