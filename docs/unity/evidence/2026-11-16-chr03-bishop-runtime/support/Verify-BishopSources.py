"""Reconcile pinned authority, exact projections, and current save consumers.

This source audit is not runtime execution, balance approval, or module acceptance.
Historical packet generators/reports are read only.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
CONTRACT = HERE.parent.parent / '2026-11-16-chr03-bishop-contract'
ENGINE = ROOT / 'engine/com.decennium.foundation'
sha = lambda raw: hashlib.sha256(raw).hexdigest()
canonical = lambda value: json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def main():
    output = Path(sys.argv[1]).resolve()
    assert not output.exists(), 'Preserve earlier audit evidence.'
    output.mkdir(parents=True)
    bindings = json.loads((CONTRACT / 'SOURCE_BINDINGS.json').read_text())
    rows = bindings['sources']
    specs = [r['revision'] + ':' + r['path'] for r in rows]
    raw = subprocess.check_output(['git', 'cat-file', '--batch'], input=('\n'.join(specs)+'\n').encode(), cwd=ROOT)
    cursor = 0
    checked = []
    payloads = {}
    for row in rows:
        end = raw.index(b'\n', cursor)
        blob, kind, size = raw[cursor:end].decode().split()
        start = end + 1
        data = raw[start:start + int(size)]
        cursor = start + int(size) + 1
        assert kind == 'blob' and blob == row['gitBlob'] and len(data) == row['bytes'] and sha(data) == row['sha256'], row['path']
        payloads[row['path']] = data
        current = (ROOT / row['path']).read_bytes()
        if row['role'] == 'selected-provisional-source':
            assert current == data, 'Selected source changed: ' + row['path']
        checked.append(dict(row, currentSha256=sha(current), currentMatchesPin=current == data))
    assert cursor == len(raw)
    rb = 'DescentReviewChanges/ReviewBible/'
    catalog = json.loads(payloads[rb+'data/public/spell_playtests/catalog.json'])['spells']
    review = json.loads(payloads[rb+'data/public/spell_playtests/authored_review_index.json'])['entries']
    card = catalog[33]
    reviewed = next(x for x in review if x['id'] == card['id'])
    assert card['id'] == 'dispel-magic-lesser' and card['status'] == 'operational-playtest-draft'
    assert reviewed['authoredStatus'] == 'reviewed-authored-operational-playtest'
    assert reviewed['wholeCardPointer'] == '/spells/33'
    source = (ENGINE/'Runtime/Core/BishopSpellSource.cs').read_text()
    projections = {'wholeCard': sha(canonical(card)), 'procedure': sha(canonical(card['operational'])),
                   'originalCatalogRecord': sha(canonical(card['source']['original'])), 'authoredReviewEntry': sha(canonical(reviewed))}
    for digest in projections.values():
        assert '"'+digest+'"' in source, 'Dispel exact source projection differs.'
    access = []
    for name, value in sorted(card['classAccess'].items()):
        expected = 'new SpellClassAccess("%s", "%s", %d, %d, %d)' % (name, value['school'], value['rank'], value['minimumClassLevel'], value['baseRpCost'])
        assert expected in source
        access.append(expected)
    assert source.count('new SpellClassAccess(') == len(access) == 7
    placements = card['source']['original']['placements']
    for item in placements:
        assert 'new SpellSourcePlacement("%s", %d, "%s")' % (item['school'],item['level'],item['summary']) in source
    assert source.count('new SpellSourcePlacement(') == len(placements) == 1
    assert card['classAccess']['Cleric'] == dict(school='Abjuration',rank=2,minimumClassLevel=3,baseRpCost=3)
    assert card['additionalRpCost'] == 0 and card['operational']['rangeFeet'] == 30
    legacy_path = 'engine/com.decennium.foundation/Runtime/Core/SpellSourceCatalog.cs'
    legacy = subprocess.check_output(['git','show',bindings['acceptedEngine']+':'+legacy_path],cwd=ROOT).decode()
    expected = legacy.replace('Definitions.SingleOrDefault(x => x.Id == id);',
        'Definitions.SingleOrDefault(x => x.Id == id) ?? (id == BishopProfile.Dispel ? BishopProfile.DispelSource : null);')
    assert expected.replace('\r\n','\n') == (ROOT/legacy_path).read_text(), 'Predecessor six-definition source projection changed.'
    cleric = json.loads(payloads[rb+'data/public/class_playtests/cleric.json'])
    entry = (ENGINE/'Runtime/Core/BishopEntryRecords.cs').read_text()
    selected = []
    for index, identifier in [(16,'cleric.arch.aura-of-faith'),(23,'cleric.arch.divine-invocation')]:
        item = cleric['cards'][index]
        assert item['id'] == identifier and sha(canonical(item)) in entry
        selected.append(dict(pointer='/cards/'+str(index),id=identifier,sha256=sha(canonical(item))))
    lab = ENGINE/'Laboratory/Model'
    direct_damage = []
    consumers = []
    for file in sorted(lab.glob('*.cs')):
        text = file.read_text()
        for number, line in enumerate(text.splitlines(),1):
            if 'PlaytestDamageDice.Resolve(' in line:
                direct_damage.append(dict(path=str(file.relative_to(ROOT)).replace('\\','/'),line=number,text=line.strip()))
            if re.search(r'AuraOfFaithRules\.(Qualify|Modifier|RecordSave|Damage|HealAfterRite)\(',line):
                consumers.append(dict(path=str(file.relative_to(ROOT)).replace('\\','/'),line=number,text=line.strip()))
    assert len(direct_damage) == 1 and direct_damage[0]['path'].endswith('/SharedAuraOfFaith.cs')
    covered = {Path(x['path']).name for x in consumers}
    required = {'SharedFrightened.cs','SharedSanctuary.cs','SharedSpellEffects.cs','SharedOverwatchExecution.cs',
                'SharedWorldRangedCombat.cs','SharedHuntingTrap.cs','SharedCraftingConsequences.cs','SharedHarvest.cs',
                'SharedMining.cs','SharedPeriodicRider.cs','TestOnlyClubAttackPolicy.cs','SharedResonance.cs'}
    assert required <= covered
    death = 'engine/com.decennium.foundation/Laboratory/Model/ActorLifeRules.cs'
    assert (ROOT/death).read_bytes() == payloads[death], 'Death-save code changed.'
    report = dict(status='PASS_SOURCE_ONLY',scope=__doc__.strip(),pinnedBlobs=len(rows),pins=checked,
                  selectedCards=selected,dispelProjections=projections,allDispelClassAccess=card['classAccess'],
                  allDispelPlacements=placements,legacySixDefinitions='UNCHANGED',directDamageConsumers=direct_damage,
                  auraCallSites=consumers,deathSaveCode='UNCHANGED; no Aura contribution for unconscious recipients',
                  limitations=['Text reconciliation requires semantic review and actual runtime evidence.',
                               'The third-ally control does not establish acquisition.',
                               'No production or balance promotion.'])
    (output/'SOURCE_AUDIT.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print('PASS_SOURCE_ONLY:',len(rows),'pins;',len(consumers),'Aura call sites; exact Dispel metadata and old six definitions.')


if __name__ == '__main__':
    main()
