"""Complete the TU6 one-use preserving builder from the verified DI6 pattern."""
from pathlib import Path
R=Path(r'C:\Github\DecenniumDescent\DescentReviewChanges\ReviewBible')
target=R/'tools/build_transmutation_universal_rank6_operating_proposal.py'
head=target.read_text('utf-8')
assert 'def main():' not in head
old=(R/'tools/build_divination_rank6_operating_proposal.py').read_text('utf-8')
m=old[old.index('def main():'):]
def once(before,after):
    global m
    assert m.count(before)==1,before
    m=m.replace(before,after)
m=m.replace('divination_rank6','transmutation_universal_rank6').replace('DIVINATION_RANK6','TRANSMUTATION_UNIVERSAL_RANK6')
once("check('Five mechanical procedures and one literal post-push receipt', len(P) == len(selected) == 5 and {p['spellId'] for p in P} == set(selected) and len(deferred) == 1)","check('Thirteen mechanical procedures and no deferred identities in this source group', len(P) == len(selected) == 13 and {p['spellId'] for p in P} == set(selected) and len(deferred) == 0)")
start=m.index("    check('Six exact mechanical Core entries preserved'")
end=m.index('    cids =',start)
m=m[:start]+'''    check('Thirteen exact Core entries preserved', sum(len(catalog[p['spellId']]['source']['coreEntries']) for p in P) == 13)
    check('Displace Structure retains actual range30feet', catalog['displace-structure']['source']['coreEntries'][0]['original']['range'] == '30 feet')
    check('Flesh to Stone retains Until dispelled', catalog['flesh-to-stone']['source']['coreEntries'][0]['original']['duration'] == 'Until dispelled')
    check('Wind Walk preserves caster plus ten', 'up to 10' in catalog['wind-walk']['source']['coreEntries'][0]['original']['effect'])
    check('Instant Summons retains concentration minute', catalog['instant-summons']['source']['coreEntries'][0]['original']['duration'] == 'Concentration, up to 1 minute')
    check('Arcane Clone retains actual three-round source', catalog['arcane-clone']['source']['coreEntries'][0]['original']['duration'] == '3 rounds')
''' + m[end:]
once("{'counterspell', 'greater-dispel', 'resonance-sight-greater'}","{'conjure-elemental-lance', 'eye-of-judgement', 'teleport-object', 'counterspell', 'true-seeing', 'quicken-cast', 'greater-dispel'}")
once("check('Thirteen whole current counterparts: seven reviewed/six pending', len(counterparts) == 13 and len(pending) == 6)","check('Twenty-one whole current counterparts: nine reviewed/twelve pending', len(counterparts) == 21 and len(pending) == 12)")
once("['divination_universal_rank5', 'evocation_rank6', 'abjuration_conjuration_rank5']","['abjuration_conjuration_rank4', 'necromancy_transmutation_rank5', 'transmutation_universal_rank4', 'divination_rank6', 'illusion_necromancy_rank6', 'divination_universal_rank5', 'abjuration_conjuration_rank5']")
once("check('All six pending comparisons retain their complete prior proposals', len(earlier) == 6 and {e['completeProposalRecord']['spellId'] for e in earlier} == pending)","check('Ten pending comparisons retain complete prior proposals; two lower-rank sources remain unfinished', len(earlier) == 10 and {e['completeProposalRecord']['spellId'] for e in earlier} == pending - {'gaseous-form', 'glyph-of-warding'})")
once("'TEMPORAL_CONTROL_PLAYTEST.md', 'TEMPORAL_PARENT_PLAYTEST.md', 'TEMPORAL_KERNEL_PLAYTEST.md', 'BODY_EQUIPMENT_PLAYTEST.md', 'TRANSFORMATION_SPELL_PLAYTEST.md', 'HEALING_DEATH_PLAYTEST.md'","'BODY_EQUIPMENT_PLAYTEST.md', 'TRANSFORMATION_SPELL_PLAYTEST.md', 'HEALING_DEATH_PLAYTEST.md', 'CREATURE_LIFECYCLE_PLAYTEST.md', 'CHARACTER_CREATION_PLAYTEST.md', 'CONDITIONS_PLAYTEST.md', 'CRAFTING_TRADE_REFERENCE.md'")
start=m.index('    arithmetic =')
end=m.index('    for label, actual, expected in arithmetic:',start)
m=m[:start]+'''    arithmetic = [('Wizard11 cast remainder',40-13,27), ('Mage11 cast remainder',32-13,19),
                  ('SaveDC',8+4+4,16), ('Attack modifier',4+4,8),
                  ('Rebind flat reduction after failed save',28-3,25), ('Rebind success half',29//2,14),
                  ('Rebind success resistance',14//2,7), ('Earthstep movement allowance',20+10,30),
                  ('One minute',1*60,60), ('One hour',60*60,3600), ('Metaburst STR18score',18+4,22),
                  ('STR22modifier',(22-10)//2,6), ('Metaburst capped23',23+min(4,max(0,24-23)),24),
                  ('Metaburst does not lower26',26+min(4,max(0,24-26)),26),
                  ('Original negativeCON floors',max(1,6-2)+max(1,1-2),5),
                  ('Temporary CON floors',max(1,6)+max(1,1),7), ('Capacity clamp',min(7,5),5),
                  ('Structure example mass fits',80000<=250000,True), ('Rotation actual arc',round(20*math.pi/2,3),31.416),
                  ('Rotation arc exceeds30',20*math.pi/2>30,True), ('Petrified body pounds',180*10,1800),
                  ('Petrified slashing resistance',14//2,7), ('Earth example cubic volume',10*10*10,1000),
                  ('Earth missing receiver volume',1000-200,800), ('Maximum selected earth volume',20*20*20,8000),
                  ('Wind Walk recipients',1+10,11), ('Rift save half',23//2,11),
                  ('Arcane Clone outside clock',3*6,18), ('Combined visual candidates',1+3+1,5),
                  ('Caster selected fraction',1/(1+3+1),0.2), ('Wrapper plus rank3payload cost',13+5,18),
                  ('Wrapper plus rank3payload RP remaining',40-13-5,22), ('Frame maximum lifetime',24*60*60,86400),
                  ('Tiny STR6physical capacity',6*7.5,45), ('Tiny STR6Load',6/2,3),
                  ('Homunculus paid repair',min(20,7+8),15), ('Object recall one mile',5280,5280),
                  ('Prepared case fits50lb',30<=50,True), ('No restored absent payload',0,0)]
''' + m[end:]
once("'completeUntouchedDeferredReceipts': deferred, 'originalBookBindings'", "'completeUntouchedDeferredReceipts': deferred, 'pendingCounterpartsWithoutPriorProposal': ['gaseous-form', 'glyph-of-warding'], 'originalBookBindings'")
once('# Rank-six Divination operating proposals','# Rank-six Transmutation and Universal operating proposals')
once("'earlierFullUnadoptedCounterpartProposals': len(earlier), 'completeComparisonClasses'","'earlierFullUnadoptedCounterpartProposals': len(earlier), 'pendingCounterpartsWithoutPriorProposal': ['gaseous-form', 'glyph-of-warding'], 'completeComparisonClasses'")
once('current rules/all17 classes/temporal boundaries, reviewed EX58 bindings','current rules/all17 classes/body and resource boundaries, reviewed EX58 bindings')
compile(head+'\n\n'+m,str(target),'exec')
target.write_text(head+'\n\n'+m,encoding='utf-8',newline='\n')
print('Completed TU6 one-use builder with explicit unfinished lower-rank comparison sources.')
