"""Read-only source/API audit; writes derived evidence in this packet only.

This neither executes C# nor approves a creature, scenario, rule or runtime.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
BASELINE = 'f0e786402214c4caa40b86bb0963aefe762ff301'
ENGINE = '2733b9fd75e2159ad73312b9583311693b925598'
SOURCE = '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
CODE = 'engine/com.decennium.foundation/'
RB = 'DescentReviewChanges/ReviewBible/'
BESTIARY = 'docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack/'
VOLUME = BESTIARY + 'Monster_Manual_of_the_Known_Descent_Source/'
BISHOP = 'docs/unity/evidence/2026-11-16-chr03-bishop-runtime/'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def write(name, value):
    (PACKET / name).write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())


def main():
    requests = {}
    for path in ['CANON_MANIFEST.md', 'docs/canon/CANON_MANIFEST.json', 'docs/canon/REPOSITORY_PROMOTION.md',
                 'docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json', BISHOP + 'GPT_FINAL_REVIEW.json',
                 BISHOP + 'final/FINAL_RECONCILIATION.json', BISHOP + 'final/QUALIFICATION_MEMBERS.json',
                 'docs/unity/evidence/2026-11-16-chr03-bishop-contract/SOURCE_API_CONTRACT.md',
                 'docs/unity/evidence/2026-11-16-exp07-post-recovery/SOURCE_API_CONTRACT.md',
                 'docs/unity/evidence/2026-11-16-exp07-post-recovery/APPROVED_CONTRACT.md',
                 'docs/unity/evidence/2026-11-12-tac10-later-defender-controller/SOURCE_API_PROPOSAL.md']:
        requests[path] = (BASELINE, 'authority-or-accepted-boundary')
    for path in ['data/public/class_playtests/cleric.json', 'data/playtest/class_drafts/cleric.json',
                 'data/playtest/class_sources/cleric.json', 'docs/mechanics/classes/cleric.md',
                 'docs/mechanics/CLASS_PLAYTEST_RULES.md', 'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',
                 'docs/mechanics/SPELL_INTEGRATION_RULES.md', 'data/playtest/bestiary_public_source_candidate.json']:
        requests[RB + path] = (SOURCE, 'selected-draft-or-source-candidate')
    for path in git('ls-tree', '-r', '--name-only', SOURCE, '--', VOLUME).decode().splitlines():
        if path.endswith('.md') or path.endswith('volume-metadata.json'):
            requests[path] = (SOURCE, 'canonical-volume-inventory-not-runtime-approval')
    requests[BESTIARY + 'build-filters.json'] = (SOURCE, 'canonical-publication-filter')
    code_paths = ['Runtime/Core/Simulation.cs', 'Runtime/Core/ActorLifeRecords.cs',
                  'Runtime/Core/ResonanceRecords.cs', 'Runtime/Core/FrightenedRecords.cs',
                  'Runtime/Core/ClericSettlementRecords.cs', 'Runtime/Core/ClericSettlementValidation.cs',
                  'Runtime/Core/BishopEntryRecords.cs', 'Runtime/Core/PostRecoveryEncounterRecords.cs',
                  'Runtime/Core/PostRecoveryEncounterValidation.cs', 'Runtime/Core/LaterEncounterRecords.cs',
                  'Runtime/Core/RuleTime.cs', 'Runtime/Persistence/SnapshotCodec.cs',
                  'Runtime/Persistence/BishopEntryCodec.cs', 'Runtime/Persistence/ClericSettlementCodec.cs',
                  'Laboratory/Model/SharedResonance.cs', 'Laboratory/Model/SharedRadiance.cs',
                  'Laboratory/Model/SharedAuraOfFaith.cs', 'Laboratory/Model/SharedBishopEntry.cs',
                  'Laboratory/Model/SharedPostRecoveryEncounter.cs', 'Laboratory/Model/SharedSpellCasting.cs',
                  'Laboratory/Model/SharedWorldCombatPolicy.cs', 'Laboratory/Model/SharedWorldRangedCombat.cs',
                  'Laboratory/Model/ConnectedExpeditionSession.cs', 'Laboratory/Model/ConnectedExpeditionView.cs',
                  'Laboratory/Model/ObservationGeometry.cs', 'Laboratory/Model/PlanarCombatGeometry.cs',
                  'Laboratory/Model/PlaytestTiming.cs', 'Laboratory/Model/PlaytestLife.cs',
                  'Laboratory/Model/CharacterRuleFacts.cs', 'Laboratory/Model/TestOnlyClubAttackPolicy.cs',
                  'Laboratory/Model/ClassAdvancementOptionCatalog.cs', 'Tests/EditMode/BishopEntryCases.cs']
    for path in code_paths:
        requests[CODE + path] = (ENGINE, 'accepted-engine-api')

    all_cs = [p for p in git('ls-tree', '-r', '--name-only', ENGINE, '--', CODE).decode().splitlines() if p.endswith('.cs')]
    patterns = {
        'creature-type-candidates': r'\bUndead\b|CreatureType|CreatureKind|CreatureClassification',
        'consecration-candidates': r'Consecrate|ConsecratedGround|consecrated-ground',
        'recharge-consumers': r'CharacterAbilityRechargeRecord|TickAbilityRecharge',
    }
    searches = {}
    for key, pattern in patterns.items():
        hits = []
        for path in all_cs:
            text = (ROOT / path).read_text(encoding='utf-8-sig')
            found = [{'line': i + 1, 'text': line.strip()} for i, line in enumerate(text.splitlines())
                     if re.search(pattern, line, re.IGNORECASE)]
            if found:
                hits.append({'path': path, 'hits': found})
                requests[path] = (ENGINE, 'accepted-engine-search-candidate')
        searches[key] = {'pattern': pattern, 'searchedFiles': len(all_cs), 'hits': hits,
                         'limit': 'Lexical candidates, combined with direct ActorState/profile/API inspection; not a semantic completeness proof.'}

    ordered = sorted(requests.items())
    payload = ''.join(rev + ':' + path + '\n' for path, (rev, _) in ordered).encode()
    result = subprocess.run(['git', 'cat-file', '--batch'], cwd=ROOT, input=payload,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    pos, bindings, blobs = 0, [], {}
    for path, (revision, role) in ordered:
        end = result.stdout.index(b'\n', pos)
        header = result.stdout[pos:end].decode().split()
        assert len(header) == 3 and header[1] == 'blob', (path, header)
        length = int(header[2]); pos = end + 1
        raw = result.stdout[pos:pos + length]; pos += length + 1
        local = (ROOT / path).read_bytes()
        assert local == raw or local.replace(b'\r\n', b'\n') == raw, 'Checkout differs: ' + path
        blobs[path] = raw
        bindings.append(dict(path=path, revision=revision, role=role, gitBlob=header[0], bytes=length,
                             sha256=hashlib.sha256(raw).hexdigest(), checkoutRelation='exact' if local == raw else 'CRLF-only; preserved'))
    assert pos == len(result.stdout) and not result.stderr.strip()
    assert not git('diff', ENGINE, '--', 'engine').strip(), 'Accepted engine must remain unchanged'
    decode = lambda path: blobs[path].decode('utf-8-sig')
    parse = lambda path: json.loads(decode(path))
    checks = []

    def check(name, value):
        assert value, name
        checks.append(dict(name=name, passed=True))

    cleric = parse(RB + 'data/public/class_playtests/cleric.json')
    ground, consecrate = cleric['cards'][1], cleric['cards'][14]
    check('Exact owned card identities and selected Base level1 access',
          ground['id'] == 'cleric.base.consecrated-ground' and consecrate['id'] == 'cleric.base.consecrate'
          and all(c['minimumClassLevel'] == 1 and c['acquisition'] == 'selection' for c in [ground, consecrate]))
    check('Consecrate printed Action/2RP/radius/range/duration/recharge',
          [consecrate[k] for k in ['activation', 'cost', 'rangeAndTarget', 'duration', 'frequency']] ==
          ['Action', '2 RP', '15-foot-radius fixed zone centered at a point within 30 feet', '3 rounds', 'Recharge 3 rounds'])
    check('Consecrate has immediate exit loss and one zone per creator',
          'Undead creatures in the zone have -1 on attack rolls.' in consecrate['effect']
          and 'leaving the zone loses that penalty immediately' in consecrate['effect']
          and 'creating another ends the first' in consecrate['effect'])
    check('Ground is positive-Rite, creator-owned terrain and nonrecursive flat S healing',
          'restores HP to a living creature standing in terrain created by your Consecrate feature' in ground['effect']
          and 'S additional HP' in ground['effect'] and 'once per creature per Rite pulse' in ground['effect']
          and 'not itself another healing trigger' in ground['effect'])
    mapping = parse('docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json')
    check('CHR05 dependencies unchanged', next(x for x in mapping['workItems'] if x['id'] == 'CHR-05')['dependencies']
          == ['CHR-03', 'TAC-02', 'TAC-05', 'TAC-08'])
    review = parse(BISHOP + 'GPT_FINAL_REVIEW.json')
    check('Actual successor gate is contract only', review['response']['id'] == '07ffc865-b1db-5bb0-9204-3e883bc9c559'
          and 'Consecrate / Consecrated Ground' in review['response']['text'] and 'contract preparation and review only' in review['response']['text'])
    check('Accepted1570 remains evidence, not a new run', parse(BISHOP + 'final/FINAL_RECONCILIATION.json')['passed'] == 1570)
    check('Existing recovery actor explicitly living humanoid', 'ordinary living humanoid' in decode('docs/unity/evidence/2026-11-16-exp07-post-recovery/SOURCE_API_CONTRACT.md'))
    core = decode(CODE + 'Runtime/Core/Simulation.cs')
    actor = core[core.index('public sealed class ActorState'):core.index('public sealed class ObjectState')]
    check('ActorState has no creature-type classification', 'public int X, Y, Tokens;' in actor and not re.search(r'Type|Kind|Undead', actor))
    check('Current character numeric record requires attained class levels',
          'gained.Length<1' in decode(CODE + 'Runtime/Core/ActorLifeRecords.cs'))
    check('Future source type membership can be mixed without granting that card',
          'counts as both humanoid and undead' in cleric['cards'][57]['effect'])
    command_enum = core[core.index('public enum CommandKind'):core.index('public enum Outcome')]
    check('No current Consecrate command', not re.search('Consecrat', command_enum, re.I))
    check('Undead search reaches catalog-only entry', {x['path'] for x in searches['creature-type-candidates']['hits']}
          == {CODE + 'Laboratory/Model/ClassAdvancementOptionCatalog.cs'})
    check('Current Rite ordering is base then Radiance then Aura',
          decode(CODE + 'Laboratory/Model/SharedResonance.cs').index('SettleRadiance(state,command,rite)')
          < decode(CODE + 'Laboratory/Model/SharedResonance.cs').index('AuraOfFaithRules.HealAfterRite'))
    check('Exact fractional world position and point effect ray are available',
          'WorldPositionResolver.Position(s, actorId)' in decode(CODE + 'Laboratory/Model/ObservationGeometry.cs')
          and 'LineOfEffectClearToCell' in decode(CODE + 'Laboratory/Model/ObservationGeometry.cs'))
    check('Virtual marker versus absolute duration helpers exist', all(x in decode(CODE + 'Laboratory/Model/PlaytestTiming.cs')
          for x in ['MarkerDeadline', 'AbsoluteDuration', 'ApplicationSequence']))
    check('Actor and ability scoped recharge exists', all(x in decode(CODE + 'Runtime/Core/FrightenedRecords.cs')
          for x in ['CharacterAbilityRechargeRecord', 'ActorId', 'AbilityId', 'EpochId', 'LastLocalStart']))

    inventory = []
    for path in sorted(p for p in blobs if p.startswith(VOLUME + 'entries/') and p.endswith('.md')):
        text = decode(path)
        block = text.split('## Stat Block', 1)[1] if '## Stat Block' in text else ''
        typed = re.search(r'^\*\*(\w+) ([^,\n*]+), ([^*\n]+)\*\*', block, re.M)
        publication = re.search(r'^\*\*Publication classification:\*\* (.+)$', text, re.M)
        inventory.append(dict(path=path, slug=Path(path).stem, publication=publication.group(1).strip() if publication else None,
                              size=typed.group(1) if typed else None, creatureType=typed.group(2) if typed else None,
                              alignment=typed.group(3) if typed else None, sha256=hashlib.sha256(blobs[path]).hexdigest()))
    undead = [x for x in inventory if x['creatureType'] == 'Undead']
    check('Canonical volume Undead census is four exact entries', {x['slug'] for x in undead} ==
          {'angry-grief-bound', 'hungry-grief-bound', 'lonely-grief-bound', 'ferry-wraith-of-the-hush'})
    check('Only Ferry-Wraith among Undead is marked Public', [x['slug'] for x in undead if x['publication'] == 'Public'] == ['ferry-wraith-of-the-hush'])
    filters = parse(BESTIARY + 'build-filters.json')
    check('Ferry-Wraith public filter is explicit', next(x for x in filters['entries'] if x['slug'] == 'ferry-wraith-of-the-hush')['buildBucket'] == 'public')
    candidate = parse(RB + 'data/playtest/bestiary_public_source_candidate.json')
    ferry = next(x for x in candidate['records'] if x['id'] == 'ferry-wraith-of-the-hush')
    ferry_path = VOLUME + 'entries/ferry-wraith-of-the-hush.md'
    check('Source candidate is not operational approval', candidate['runtimeInstalled'] is False
          and ferry['reviewStatus'] == 'SOURCE_BOUND_NOT_OPERATIONALLY_REVIEWED')
    check('Candidate Ferry source text matches canonical source', ferry['source']['originalUtf8Text'].replace('\r\n', '\n') == decode(ferry_path).replace('\r\n', '\n'))
    check('Ferry printed type and finite attack retained', ferry['statBlock']['printedCoreFields']['type'] == 'Undead'
          and ferry['statBlock']['actions'] == [{'name': 'Hellfire Claw', 'sourceText': '*Attack:* +3 to hit, one target. *Hit:* 1d4 fire damage (average 2).'}])
    check('Ferry Contract-Bound trait cannot be silently omitted', len(ferry['statBlock']['traits']) == 1
          and ferry['statBlock']['traits'][0]['name'] == 'Contract-Bound')
    check('Printed attack alone does not supply reach or action kind', not re.search(r'\breach\b|\bmelee\b|\branged\b|\bAction\b', ferry['statBlock']['actions'][0]['sourceText'], re.I))

    index = parse(BISHOP + 'final/QUALIFICATION_MEMBERS.json')
    archive = ROOT / BISHOP / 'final' / index['archive']
    check('Accepted source-view archive binding', archive.stat().st_size == index['bytes'] and hashlib.sha256(archive.read_bytes()).hexdigest() == index['sha256'])
    witnesses = []
    with zipfile.ZipFile(archive) as z:
        for stem, expected_rp in [('second-rest', 7), ('rite-radiance-aura', 0)]:
            path = 'qualification/reference/' + stem + '.ddsave.Player.view.json'
            raw = z.read(path); row = next(x for x in index['members'] if x['path'] == path)
            check(stem + ' exact retained view', len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'])
            view = json.loads(raw.decode('utf-8-sig'))
            actor_view = next(x for x in view['Actors'] if x.get('Cleric'))
            facts = actor_view['Cleric']
            check(stem + ' actual ownership and finite RP', facts['CurrentRp'] == expected_rp and facts['MaximumRp'] == 7
                  and all(c['id'] in facts['OwnedCards'] for c in [ground, consecrate]))
            witnesses.append(dict(path=path, sha256=row['sha256'], revision=view['Revision'], clock=view['Clock'], actor=actor_view,
                                  scope='Read of accepted archived execution evidence, not a new runtime probe or a Consecrate witness.'))

    excerpts = dict(cards=[dict(pointer='/cards/' + str(i), value=x,
                               role='future type-interface constraint only; unowned and not authorized' if i == 57 else 'selected rule or interaction')
                          for i, x in enumerate(cleric['cards']) if i in [1, 12, 14, 16, 57] or 'radiance' in x['name'].lower()],
                    classStatus=cleric['status'], ferry=dict(path=ferry_path, statBlock=ferry['statBlock'], reviewStatus=ferry['reviewStatus']),
                    acceptedWitnesses=witnesses)
    write('SOURCE_BINDINGS.json', dict(baseline=BASELINE, acceptedEngine=ENGINE, sourceRevision=SOURCE, sources=bindings))
    write('SOURCE_EXTRACTS.json', excerpts)
    write('API_INVENTORY.json', dict(searches=searches, actorStateDeclaration=actor,
          caveat='Direct source inspection is summarized in SOURCE_API_CONTRACT.md. Search hits alone do not certify completeness.'))
    write('UNDEAD_SOURCE_SCAN.json', dict(scope=VOLUME, inventory=inventory, undead=undead,
          selectedCandidate='ferry-wraith-of-the-hush', candidateRuntimeInstalled=False,
          unresolved=['Creature type/provenance record and actor composition', 'Printed action operational binding and Contract-Bound trait',
                      'Actual persistent actor, lawful encounter/context and connected penalty witness'],
          caveat='Canonical publication status does not make a parsed source record an operational runtime profile. No creature or encounter is installed.'))
    report = dict(status='PASS_SOURCE_ONLY_WITH_RUNTIME_PREREQUISITE', baseline=BASELINE, acceptedEngine=ENGINE,
                  sourceRevision=SOURCE, pinnedBlobs=len(bindings), searchedCsharpFiles=len(all_cs),
                  canonicalVolumeEntries=len(inventory), canonicalUndead=len(undead), checks=checks,
                  engineUnchanged=True, newCsharpCompilation=False, newRuntimeExecution=False, runtimeAuthorized=False,
                  reviewRequired=['Consecrate timing/geometry/passive-trigger order contract',
                                  'Lawful Undead classification, operational source/actor/context and actual attack witness prerequisite',
                                  'Actual revised finite-funding route and full qualification design'],
                  limits='Source/API findings only. Existing1570 acceptance remains unchanged; no new module or whole-engine completion.')
    write('SOURCE_AUDIT.json', report)
    print(json.dumps({k: v for k, v in report.items() if k != 'checks'} | {'checks': len(checks)}))


if __name__ == '__main__':
    main()
