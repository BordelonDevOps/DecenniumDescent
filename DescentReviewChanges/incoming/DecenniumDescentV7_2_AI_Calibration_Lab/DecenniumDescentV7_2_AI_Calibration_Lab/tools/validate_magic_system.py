from __future__ import annotations
import json, re, csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CANON=["Bard","Cleric","Crimson Agent","Dragoon","Druid","Mage","Monk","Mirrorsage","Oracle","Ranger","Shaman","Soldier","Thief","Tinker","Warrior","Wizard","Paladin"]
NON_WEAVE={"Oracle","Soldier","Warrior"}


def load_spells():
    s=(ROOT/'src/data/spells.js').read_text(encoding='utf-8')
    m=re.search(r'export const SPELLS = (\{.*?\});\n\nexport const SPELL_SCHOOLS',s,re.S)
    if not m: raise AssertionError('Could not parse SPELLS payload')
    return json.loads(m.group(1))

spells=load_spells()
placements=json.loads((ROOT/'src/data/spell-placements.json').read_text())
assert len(spells)==848, len(spells)
assert len(placements)==936, len(placements)
all_tags={c for sp in spells.values() for c in sp.get('classes',[])}
assert all_tags <= set(CANON), sorted(all_tags-set(CANON))
assert not (all_tags & NON_WEAVE), all_tags & NON_WEAVE
assert len(all_tags)==14, sorted(all_tags)

varied=[]
for sp in spells.values():
    levels=set(sp.get('classLearnLevels',{}).values())
    if len(levels)>1: varied.append(sp['name'])
assert len(varied)>=500, len(varied)

# All 17 protected class-mechanic entries.
core=(ROOT/'src/data/class-core-mechanics.js').read_text()
for cls in CANON:
    key=f'  "{cls}":' if ' ' in cls else f'  {cls}:'
    assert key in core, f'missing core mechanic: {cls}'
assert 'Crescendo' in core and 'Conviction' in core and 'Blood Gauge' in core
assert 'Momentum' in core and 'Shapeshifting' in core and 'Nuke Chains' in core
assert 'Ki Flow' in core and 'Echo Slots' in core and 'Revelation Charges' in core
assert 'Track Target' in core and 'Totem System' in core and 'Palisade' in core
assert 'Sneak Attack' in core and 'Anacite Drone' in core and 'Mutation Slots' in core
assert 'Spell Matrix' in core and 'The Oath' in core
assert 'DARK_RESONANCE_PATHS' in core and 'Lich' in core and 'Necromancer' in core

paths=(ROOT/'src/data/class-paths.js').read_text()
for path in ['Lich','Necromancer']:
    idx=paths.index(f'name: "{path}"')
    window=paths[idx:idx+2800]
    assert 'Evil / Transgressive' in window, f'{path}: explicit evil ethos missing'
    assert 'Traumatic Casting' in window, f'{path}: Traumatic Casting missing'
assert 'Soul Reservoir' in paths and 'Grave Conductor' in paths

res=(ROOT/'src/data/resonance-economy.js').read_text()
for token in ['dissonanceLimit','dissonanceState','dissonanceGain','castingPermissionsAtDissonance','traumaticCastingBacklash']:
    assert f'function {token}' in res, token

# Class school map and progression cover all 17 classes.
with (ROOT/'class_spell_school_mapping.csv').open(newline='',encoding='utf-8') as f:
    rows=list(csv.reader(f))
map_classes={r[0] for r in rows[1:] if r}
assert map_classes==set(CANON), sorted(set(CANON)-map_classes)
with (ROOT/'class_spell_progression.csv').open(newline='',encoding='utf-8') as f:
    rows=list(csv.DictReader(f))
prog_classes={r['Class'] for r in rows}
assert prog_classes==set(CANON), sorted(set(CANON)-prog_classes)

# No retired base-class tags in spell records.
spell_blob=(ROOT/'src/data/spells.js').read_text()
assert '"Sorcerer"' not in spell_blob
assert '"Warlock"' not in spell_blob
assert '"Fighter"' not in spell_blob

# Player-facing rulebook magic terms.
rule=(ROOT/'rulebook_output.txt').read_text(encoding='utf-8',errors='ignore')
assert 'Mana Surge' not in rule
assert 'Mana Shield' not in rule
assert 'Mana Tether' not in rule
assert 'Mana Furnace' not in rule
assert 'Mana Kindle' not in rule
assert '## Alignment and Magic' not in rule
assert '## Resonance Rank, Class Access, and Dissonance' in rule
assert 'Traumatic Casting' in rule
for retired_phrase in [
    'Apply Arcane Guilds reputation to the merged total once',
    'Standing with magical factions can enhance or diminish capacity',
    'alignment affinity',
    'Affinity Discount',
    'Opposition Penalty',
    'Alignment and reputation affect regeneration rates',
]:
    assert retired_phrase.lower() not in rule.lower(), retired_phrase
assert 'reputation and alignment do not alter intrinsic RP capacity' in rule


# Current UI/source must not describe reputation/alignment as spell physics.
ui_blob="\n".join((ROOT/x).read_text(encoding='utf-8',errors='ignore') for x in [
    'src/components/ReputationPanel.tsx',
    'src/components/CharacterBuilder.tsx',
    'src/components/CharacterSheet.tsx',
    'src/components/SessionTracker.tsx',
])
for retired_ui in [
    'Resonance RP modifiers (Arcane Guilds max',
    'spell-cost preview',
    'Spend to push smites, crescendos, or Weave echoes',
    'Resonance max RP and spell costs update from Arcane Guilds',
    '+ rep ${resonanceMax.multiclass.repModifier',
]:
    assert retired_ui not in ui_blob, retired_ui
assert 'standing itself never adds RP' in rule
assert 'reputation score itself' in rule
assert 'Alignment does not make a Shapeshifting form stronger or cheaper' in rule
assert 'Shapeshifting activation has no RP cost' in rule

# Compatibility APIs are hard no-ops: even numeric legacy arguments cannot alter spell physics.
assert 'function resolveRepModifier(_repModifierOrScores)' in res
resolve_window=res[res.index('function resolveRepModifier(_repModifierOrScores)'):res.index('function singleClassPoolBase') ]
assert 'return 0;' in resolve_window
assert 'Arcane Guilds rep:' not in res

# Current magic-physics invariants.
econ=(ROOT/'src/data/resonance-economy.js').read_text(encoding='utf-8')
assert 'export function spellCostRepModifier(_className, _reputation)' in econ
assert 'export function maxRpRepModifier(_reputation)' in econ
assert 'return { affinity: false, opposition: false }' in econ
assert 'Burnout' not in rule
assert 'Low Resonance' in rule

report=ROOT/'docs/mechanics/MAGIC_SYSTEM_VALIDATION_2026-07-31.md'
report.write_text(f'''# Magic System Validation — 2026-07-31\n\n**Result: PASS**\n\n- Canon base classes: **{len(CANON)} / 17**\n- Protected class-mechanic contracts: **17 / 17**\n- General Weave casters: **{len(all_tags)} / 14**\n- Oracle: Revelation Charges only\n- Soldier / Warrior: no general Weave list\n- Spell school/rank placements: **{len(placements)} / 936**\n- Unique named spells: **{len(spells)} / 848**\n- Spells with different acquisition levels across classes: **{len(varied)}**\n- Retired spell-class tags (Sorcerer/Warlock/Fighter): **0**\n- Dissonance/Refrain anti-spam functions: **present**\n- Lich Traumatic Casting exception: **present**\n- Necromancer Traumatic Casting exception: **present**\n- Rulebook alignment-based magic-cost section: **removed**
- Automatic reputation-to-spell-cost / reputation-to-capacity physics: **disabled**
- Retired Burnout subsystem in Player Rulebook: **removed; Low Resonance is informational**\n\n## Protected design conclusion\n\nSpell overlap is intentional. The spell is a shared pattern in the Weave; the class determines how and when the character learns to sound it. Resonance Points limit total magical output, while Dissonance and Refrain prevent repetitive spam. Lich and Necromancer are the only current Hero Paths allowed to force ranked casting through Fractured Dissonance, and they pay direct magical trauma for doing so.\n''',encoding='utf-8')
print(f'PASS spells={len(spells)} placements={len(placements)} varied_acquisition={len(varied)} classes={len(CANON)}')
