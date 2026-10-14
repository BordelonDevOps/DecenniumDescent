"""Complete the one-use DI6 source-preserving authoring builder."""
from pathlib import Path
R = Path(r'C:\Github\DecenniumDescent\DescentReviewChanges\ReviewBible')
target = R / 'tools/build_divination_rank6_operating_proposal.py'
head = target.read_text('utf-8')
assert 'def main():' not in head
old = (R / 'tools/build_abjuration_conjuration_rank6_operating_proposal.py').read_text('utf-8')
m = old[old.index('def main():'):]
def once(before, after):
    global m
    assert m.count(before) == 1, before
    m = m.replace(before, after)
m = m.replace('abjuration_conjuration_rank6', 'divination_rank6').replace('ABJURATION_CONJURATION_RANK6', 'DIVINATION_RANK6')
once("check('Eleven mechanical procedures and three literal post-push receipts', len(P) == len(selected) == 11 and {p['spellId'] for p in P} == set(selected) and len(deferred) == 3)", "check('Five mechanical procedures and one literal post-push receipt', len(P) == len(selected) == 5 and {p['spellId'] for p in P} == set(selected) and len(deferred) == 1)")
start = m.index("    check('Twelve exact mechanical Core entries preserved'")
end = m.index('    cids =', start)
m = m[:start] + '''    check('Six exact mechanical Core entries preserved', sum(len(catalog[p['spellId']]['source']['coreEntries']) for p in P) == 6)
    check('Chrono Lock preserves both actual school placements', {e['original']['school'] for e in catalog['chrono-lock']['source']['coreEntries']} == {'Divination', 'Universal'})
    check('Chrono original no-save and no-damage clauses retained', any('no save' in e['original']['effect'] for e in catalog['chrono-lock']['source']['coreEntries']) and any('no actions or damage' in e['original']['effect'] for e in catalog['chrono-lock']['source']['coreEntries']))
    check('Eye retains its material-or-focus source', catalog['eye-of-judgement']['source']['coreEntries'][0]['original']['components'] == 'V, S, M/F')
    check('Resonance Prophecy original Instantaneous remains intact', catalog['resonance-prophecy']['source']['coreEntries'][0]['original']['duration'] == 'Instantaneous')
    for d in deferred:
        sid = d['spellId']; f = catalog[sid]
        check(sid + ' literal deferred source unchanged', f == d['fullSourceAndCurrentAccessRecord'] and f['operational'] is None and sid not in {r['spellId'] for r in records})
        for e in f['source']['coreEntries']:
            check(sid + ' full literal Core receipt at ' + str(e['index']), core['spells'][e['index']] == e['original'])
    check('Planar Binding Minor retains printed CR8', deferred[0]['spellId'] == 'planar-binding-minor' and 'CR 8' in catalog['planar-binding-minor']['source']['coreEntries'][0]['original']['effect'])
''' + m[end:]
once("{'greater-dispel', 'antimagic-field-lesser', 'fabricate', 'resonance-anchor', 'arcane-lock'}", "{'counterspell', 'greater-dispel', 'resonance-sight-greater'}")
once("check('Sixteen whole current counterparts: eight reviewed/eight pending', len(counterparts) == 16 and len(pending) == 8)", "check('Thirteen whole current counterparts: seven reviewed/six pending', len(counterparts) == 13 and len(pending) == 6)")
once("['abjuration_conjuration_rank5', 'divination_universal_rank5', 'evocation_rank6', 'transmutation_universal_rank4']", "['divination_universal_rank5', 'evocation_rank6', 'abjuration_conjuration_rank5']")
once("check('All eight pending comparisons retain their complete prior proposals', len(earlier) == 8", "check('All six pending comparisons retain their complete prior proposals', len(earlier) == 6")
once("'CRAFTING_TRADE_REFERENCE.md', 'ADVANCED_CRAFT_CANDIDATE_GUIDE.md', 'ADVANCED_CRAFT_REVIEW_STATUS.json'", "'TEMPORAL_CONTROL_PLAYTEST.md', 'TEMPORAL_PARENT_PLAYTEST.md', 'TEMPORAL_KERNEL_PLAYTEST.md', 'BODY_EQUIPMENT_PLAYTEST.md', 'TRANSFORMATION_SPELL_PLAYTEST.md', 'HEALING_DEATH_PLAYTEST.md'")
once("['bard', 'mirrorsage', 'wizard', 'cleric', 'shaman', 'druid', 'mage', 'tinker']", "['bard', 'cleric', 'crimson-agent', 'dragoon', 'druid', 'mage', 'mirrorsage', 'monk', 'oracle', 'paladin', 'ranger', 'shaman', 'soldier', 'thief', 'tinker', 'warrior', 'wizard']")
once("    check('Prepared textual class comparisons remain empty', prep['classComparisonRecords'] == [])", "    check('Complete envelopes for all17 actual classes retained', len(classes) == 17)\n    check('Prepared textual class comparisons remain empty', prep['classComparisonRecords'] == [])")
start = m.index('    arithmetic =')
end = m.index('    for label, actual, expected in arithmetic:', start)
m = m[:start] + '''    arithmetic = [('Wizard11 cast remainder', 40-13,27), ('Mage11 cast remainder',32-13,19),
                  ('Actual saveDC',8+4+4,16), ('Actual spell attack',4+4,8),
                  ('Outside one-round endpoint',1*6,6), ('One-minute field',60,60),
                  ('Thirty-day forecast',30*24*60*60,2592000), ('Earlier seven-day horizon',7*24*60*60,604800),
                  ('Maximum forecast milestones',3*3,9), ('Field diameter',2*20,40),
                  ('Suppression capacity maximum',80-20,60), ('HP clamp',min(75,60),60),
                  ('Capacity return is not healing',min(60,80),60), ('One conserved initial resource balance',10+2,12),
                  ('Independent legal resource spend',10-3,7), ('Resource return after spend',7+2,9),
                  ('Gain room accounts for reserve',max(0,10-(7+2)),1), ('Conserved balance after gain',7+2+1,10),
                  ('Shorter route remains shortest distance',min(80,120),80), ('Route distance difference',120-80,40),
                  ('No banked notices in ten-second suppression',0,0), ('Unelapsed field after ten seconds',60-10,50)]
''' + m[end:]
once('# Rank-six Abjuration and Conjuration operating proposals', '# Rank-six Divination operating proposals')
once('current rules/classes/crafting, reviewed EX58 bindings', 'current rules/all17 classes/temporal boundaries, reviewed EX58 bindings')
compile(head + '\n\n' + m, str(target), 'exec')
target.write_text(head + '\n\n' + m, encoding='utf-8', newline='\n')
print('Completed DI6 one-use builder without modifying any source or prior proposal.')
