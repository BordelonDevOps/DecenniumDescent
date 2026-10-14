"""Attach the existing source-preservation workflow to the new AC6 authoring."""
from pathlib import Path

R = Path(r'C:\Github\DecenniumDescent\DescentReviewChanges\ReviewBible')
target = R / 'tools/build_abjuration_conjuration_rank6_operating_proposal.py'
head = target.read_text('utf-8')
assert 'def main():' not in head, 'One-use builder completion'
old = (R / 'tools/build_illusion_necromancy_rank6_operating_proposal.py').read_text('utf-8')
m = old[old.index('def main():'):]

def once(before, after):
    global m
    assert m.count(before) == 1, before
    m = m.replace(before, after)

m = m.replace('illusion_necromancy_rank6', 'abjuration_conjuration_rank6').replace('ILLUSION_NECROMANCY_RANK6', 'ABJURATION_CONJURATION_RANK6')
once("check('All thirteen prepared mechanical identities and no deferred procedures', len(P) == len(selected) == 13 and {p['spellId'] for p in P} == set(selected) and not deferred)",
     "check('Eleven mechanical procedures and three literal post-push receipts', len(P) == len(selected) == 11 and {p['spellId'] for p in P} == set(selected) and len(deferred) == 3)")
once("        if sid == 'create-undead': record['explicitNewCreatureProfiles'] = UNDEAD_PROFILES\n", '')
start = m.index("    check('Fourteen exact Core entries preserved'")
end = m.index('    cids = sorted(', start)
m = m[:start] + '''    check('Twelve exact mechanical Core entries preserved', sum(len(catalog[p['spellId']]['source']['coreEntries']) for p in P) == 12)
    check('Guards and Wards both actual school placements preserved', {e['original']['school'] for e in catalog['guards-and-wards']['source']['coreEntries']} == {'Abjuration', 'Universal'})
    check('Globe printed Tier5 terminology remains intact', 'Tier 5' in catalog['globe-of-invulnerability']['source']['coreEntries'][0]['original']['effect'])
    check('Warp Field retains range10feet', catalog['elemental-warp-field']['source']['coreEntries'][0]['original']['range'] == '10 feet')
    for d in deferred:
        sid = d['spellId']; f = catalog[sid]
        check(sid + ' literal deferred source unchanged', f == d['fullSourceAndCurrentAccessRecord'] and f['operational'] is None and sid not in {r['spellId'] for r in records})
        for e in f['source']['coreEntries']:
            check(sid + ' full literal Core receipt at ' + str(e['index']), core['spells'][e['index']] == e['original'])
    check('Alignment Nexus distinct rank6 and rank8 preserved', {e['original']['level'] for e in catalog['alignment-nexus']['source']['coreEntries']} == {6, 8})
''' + m[end:]
once("{'major-image', 'fear', 'antimagic-field-lesser'}", "{'greater-dispel', 'antimagic-field-lesser', 'fabricate', 'resonance-anchor', 'arcane-lock'}")
once("check('Fifteen whole current counterparts: seven reviewed/eight pending', len(counterparts) == 15 and len(pending) == 8)",
     "check('Sixteen whole current counterparts: eight reviewed/eight pending', len(counterparts) == 16 and len(pending) == 8)")
once("['divination_enchantment_rank4', 'enchantment_illusion_rank5', 'necromancy_transmutation_rank5', 'enchantment_rank6', 'abjuration_conjuration_rank5']",
     "['abjuration_conjuration_rank5', 'divination_universal_rank5', 'evocation_rank6', 'transmutation_universal_rank4']")
once("'expedition/EXPEDITION_PLAYER_BOOK.md', 'expedition/EXPEDITION_DIRECTOR_BOOK.md']:",
     "'expedition/EXPEDITION_PLAYER_BOOK.md', 'expedition/EXPEDITION_DIRECTOR_BOOK.md', 'CRAFTING_TRADE_REFERENCE.md', 'ADVANCED_CRAFT_CANDIDATE_GUIDE.md', 'ADVANCED_CRAFT_REVIEW_STATUS.json']:")
once("['bard', 'crimson-agent', 'mirrorsage', 'wizard', 'cleric', 'shaman', 'druid']", "['bard', 'mirrorsage', 'wizard', 'cleric', 'shaman', 'druid', 'mage', 'tinker']")
start = m.index('    bestiary_path = ')
end = m.index('    status_path = ', start)
m = m[:start] + m[end:]
start = m.index('    arithmetic = [')
end = m.index('    for label, actual, expected in arithmetic:', start)
m = m[:start] + '''    arithmetic = [('Wizard11 RP remainder',40-13,27), ('Mage11 RP remainder',32-13,19), ('Actual saveDC',8+4+4,16), ('Actual spell attack',4+4,8),
                  ('Minute deadline',60,60), ('Seven-day Seal deadline',7*24*60*60,604800), ('Eight-hour forge lifetime',8*60*60,28800),
                  ('Globe diameter',2*10,20), ('Ward/Forbiddance diameter',2*20,40), ('Alignment complete pairs',3*3,9),
                  ('Forbiddance example save-half',17//2,8), ('Elemental example resistance',17//2,8),
                  ('One of two equally likely defense outcomes',1/2,0.5), ('Chain example save-half',19//2,9),
                  ('Maximum chain targets',1+5,6), ('Maximum straight chain reach',60+5*30,210),
                  ('Skybrand movement budget remainder',30-20,10), ('Skybrand separate attacks',1+1,2),
                  ('Forge two cycles protected RP',2*5,10), ('Forge two cycles elapsed work',2*10,20),
                  ('Forge two cycles credited work',2*60,120), ('Forge example caster total cost',13+10,23),
                  ('Forge Wizard example remaining RP',40-13-10,17), ('Forge interrupted-cycle credit',0,0),
                  ('Forge final partial credit',min(60,15),15), ('No banked final remainder',60-15,45),
                  ('Army minimum count',3*1,3), ('Army maximum count',3*6,18), ('Army actual formed count',min(12,9),9),
                  ('Army missing arrivals',12-9,3), ('Uncommanded formed bodies',9-1,8)]
''' + m[end:]
once(", 'explicitNewCreatureProfiles': UNDEAD_PROFILES, 'explicitJointIssues': ISSUES", ", 'explicitJointIssues': ISSUES")
once("            'explicitNewCreatureProfiles': UNDEAD_PROFILES, 'completeCurrentBestiaryComparison': bestiary,\n", '')
once("'# Rank-six Illusion and Necromancy operating proposals'", "'# Rank-six Abjuration and Conjuration operating proposals'")
start = m.index("        if rec['spellId'] == 'create-undead':")
end = m.index("        lines += ['### Authored examples'", start)
m = m[:start] + m[end:]
once("    doc.parent.mkdir(parents=True, exist_ok=True)\n", "    lines += ['## Literal post-push receipts', '']\n    for d in deferred:\n        lines += [d['questionId'] + ' — ' + d['fullSourceAndCurrentAccessRecord']['name'], '', d['individualQuestion'], '', '```json', json.dumps(d['fullSourceAndCurrentAccessRecord'], ensure_ascii=False, indent=2), '```', '']\n    doc.parent.mkdir(parents=True, exist_ok=True)\n")
once("    for profile in UNDEAD_PROFILES: check(profile['name'] + ' complete new profile rendered', json.dumps(profile, ensure_ascii=False, indent=2) in rendered)\n", "    for d in deferred: check(d['spellId'] + ' full literal receipt rendered', json.dumps(d['fullSourceAndCurrentAccessRecord'], ensure_ascii=False, indent=2) in rendered)\n")
once("check('Saved whole proposed records and all four explicit profiles', read(out)['records'] == records and read(out)['explicitNewCreatureProfiles'] == UNDEAD_PROFILES)",
     "check('Saved whole proposed records and all literal deferred receipts', read(out)['records'] == records and read(out)['completeUntouchedDeferredReceipts'] == deferred)")
once("'untouchedPostPushReceipts': 0,", "'untouchedPostPushReceipts': len(deferred),")
once(", 'explicitNewCreatureProfiles': len(UNDEAD_PROFILES)", '')
once('current rules/classes/bestiary, reviewed EX58 bindings', 'current rules/classes/crafting, reviewed EX58 bindings')
assert 'UNDEAD_PROFILES' not in m and 'bestiary' not in m and 'illusion_necromancy_rank6' not in m
compile(head + '\n\n' + m, str(target), 'exec')
target.write_text(head + '\n\n' + m, encoding='utf-8', newline='\n')
print('Attached AC6 preservation, full-context rendering and arithmetic workflow; no output generation yet.')
