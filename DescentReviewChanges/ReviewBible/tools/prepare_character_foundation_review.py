"""Preserve the mechanical evidence for the character-foundation conference."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def segment(path, first, last):
    lines = path.read_text(encoding='utf-8-sig').splitlines()
    return {'path': str(path.relative_to(GAME)).replace('\\', '/'),
            'sha256': sha(path), 'firstLine': first, 'lastLine': last,
            'lines': [{'line': i + 1, 'text': lines[i]} for i in range(first-1, last)]}

player = GAME / 'docs/reference/Player_Rulebook_v6_source_text.txt'
assert sha(player) == 'a346670f4244efe3641cfb06814819d83ffb8512153858205f0621bd8ab8a04b'
spans = [(56,86), (130,196), (1656,1747), (6470,6550), (7156,7250), (7772,7818)]
evidence = {'status': 'source-evidence-not-a-new-canon-promotion',
            'scope': 'Mechanical character foundation only. Cosmology review is deferred until after the verified GitHub push.',
            'playerSegments': [segment(player,a,b) for a,b in spans], 'classes': []}
details = (ROOT/'src/data/class-details.js').read_text(encoding='utf-8')
for p in sorted((ROOT/'data/playtest/class_sources').glob('*.json')):
    d = json.loads(p.read_text(encoding='utf-8'))
    if 'bookLines' not in d:
        continue
    name = d['class']
    slug = p.stem
    # Capture only the actual chassis lines, including the joined Druid paragraph.
    chassis = [x for x in d['bookLines'] if re.search(r'^(Hit Points|Hit Dice|Armor Proficiency|Weapon Proficiency|Tool Proficiency|Armor:|Saving Throws:|Skills:)',x['text'])]
    m = re.search(r'^  (?:"'+re.escape(name)+r'"|'+re.escape(name)+r'): \{\n(.*?)    combat:',details,re.M|re.S)
    assert m, name
    fields = {}
    for field in ['armor','weapons','tools','skills']:
        found = re.search(r'\b'+field+r': (\[.*?\])',m.group(1))
        assert found, (name,field)
        fields[field] = json.loads(found.group(1))
    active = (ROOT/'data/public/Decennium_Descent_Bard_Playtest_v0_1.json' if name=='Bard'
              else ROOT/f'data/public/class_playtests/{slug}.json')
    draft = json.loads(active.read_text(encoding='utf-8'))
    relevant = [s for s in draft.get('engine',[]) if re.search(r'Hit Die|HIT DIE|armor|proficien|class ability|governs|govern ',s,re.I)]
    evidence['classes'].append({'class':name,'slug':slug,'detailedBookChassis':chassis,
        'companionFields':fields,'companionPath':'DescentReviewChanges/ReviewBible/src/data/class-details.js',
        'companionSha256':sha(ROOT/'src/data/class-details.js'),
        'activeCandidatePath':str(active.relative_to(GAME)).replace('\\','/'),
        'activeCandidateSha256':sha(active), 'activeChassisAndAbilityRules':relevant,
        'rpByClassLevel':draft['rpByClassLevel'],
        'asiClassLevels':draft.get('asiClassLevels',[4,8,12,16,19])})
assert len(evidence['classes'])==17
evidence['builderPointBuy'] = segment(ROOT/'src/components/CharacterBuilder.tsx',116,174)
evidence['builderSkillLabels'] = segment(ROOT/'src/components/CharacterBuilder.tsx',382,401)
economy = ROOT/'src/data/resonance-economy.js'
elines = economy.read_text(encoding='utf-8').splitlines()
first = next(i+1 for i,x in enumerate(elines) if x.startswith('function casterTierRank'))
last = next(i+1 for i,x in enumerate(elines) if x.startswith('export function multiclassRpBreakdown'))-5
evidence['legacyMulticlassHelper'] = segment(economy,first,last)
evidence['sharedRules'] = {'path':'DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md',
                         'sha256':sha(ROOT/'docs/mechanics/CLASS_PLAYTEST_RULES.md')}
out = AUDIT/'CHARACTER_FOUNDATION_SOURCE_EVIDENCE.json'
out.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
parts=['CODEX — CHARACTER FOUNDATION CONFERENCE. Please reconcile this complete mechanical evidence batch and the proposal at the end. This is not final game-flow or push approval. Cosmology is deferred until after a verified GitHub push.\n']
parts.append('Preserved evidence SHA256: '+sha(out)+'\n')
for s in evidence['playerSegments']:
    parts.append(f"\nPLAYER SOURCE {s['path']} SHA256 {s['sha256']} lines {s['firstLine']}–{s['lastLine']}\n")
    parts.extend(f"{x['line']}: {x['text']}\n" for x in s['lines'])
parts.append('\nALL 17 CLASS COMPARISONS (exact source text, existing candidate excerpts, existing pools)\n')
parts.append(json.dumps(evidence['classes'],ensure_ascii=False,separators=(',',':'))+'\n')
for key in ['builderPointBuy','builderSkillLabels','legacyMulticlassHelper']:
    s=evidence[key]
    parts.append(f"\n{key} {s['path']} SHA256 {s['sha256']}\n")
    parts.extend(f"{x['line']}: {x['text']}\n" for x in s['lines'] if x['text'].strip())
parts.append('\nCURRENT SHARED CANDIDATE RULES (already reviewed; retain)\n')
shared=(ROOT/'docs/mechanics/CLASS_PLAYTEST_RULES.md').read_text(encoding='utf-8')
parts.append(shared[shared.index('## Ordinary spells:'):shared.index('## Source and review status')])
parts.append('\nPROPOSED DECISIONS\n'+(AUDIT/'CHARACTER_FOUNDATION_PROPOSAL.txt').read_text(encoding='utf-8'))
packet = AUDIT/'CODEX_CHARACTER_FOUNDATION_CONFERENCE.txt'
packet.write_text(''.join(parts),encoding='utf-8')
print(json.dumps({'evidence':str(out),'packet':str(packet),'characters':len(''.join(parts)),'packetSha256':sha(packet)},indent=2))
