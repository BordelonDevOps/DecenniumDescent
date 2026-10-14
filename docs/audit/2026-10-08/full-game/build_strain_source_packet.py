from pathlib import Path
import hashlib
import json
import re
GAME=Path(__file__).resolve().parents[4]
ROOT=GAME/'DescentReviewChanges/ReviewBible'
AUDIT=Path(__file__).resolve().parent
def sha(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
warrior=json.loads((ROOT/'data/public/class_playtests/warrior.json').read_text(encoding='utf-8'))
cards=[c for c in warrior['cards'] if re.search(r'\bStrain\b',c.get('effect',''),re.I)]
guide=(ROOT/'docs/mechanics/GAMEPLAY_LOOP_CANON.md').read_text(encoding='utf-8')
sections=[]
for heading in ['## 5. Opening clock and Watches','### Supply','### Strain']:
    start=guide.find(heading)
    if start<0:
        continue
    level=len(heading.split()[0])
    ending=re.search(r'^#{1,'+str(level)+r'} ',guide[start+len(heading):],re.M)
    end=start+len(heading)+ending.start() if ending else len(guide)
    sections.append({'heading':heading,'exactText':guide[start:end]})
packet={'warriorPath':'data/public/class_playtests/warrior.json',
        'engine':[{'index':i,'text':v,'textSha256':hashlib.sha256(v.encode()).hexdigest()} for i,v in enumerate(warrior['engine']) if re.search(r'\bStrain\b|rest',v,re.I)],
        'cards':[{'card':c,'sourceObjectSha256':sha(c)} for c in cards],
        'gameplayPath':'docs/mechanics/GAMEPLAY_LOOP_CANON.md',
        'gameplaySha256':hashlib.sha256((ROOT/'docs/mechanics/GAMEPLAY_LOOP_CANON.md').read_bytes()).hexdigest(),
        'gameplaySections':sections,
        'core':json.loads((AUDIT/'STRAIN_NAMESPACE_CORE_EVIDENCE.json').read_text(encoding='utf-8'))}
(AUDIT/'STRAIN_SOURCE_BINDINGS.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
base=(AUDIT/'CODEX_STRAIN_NAMESPACE_CONFERENCE.md').read_text(encoding='utf-8')
base+='\nAdditional source gate: the Gameplay reference caps beneficial short rests at2 between Long Rests and beneficial Long Rests at1 per24h. The shared class reference states completed1h/8h durations without repeating those caps. Please explicitly retain those campaign rest limits if compatible; do not let this pass silently waive them. Full HP/RP/RC rest rewards remain their later system review.\n\nEXACT SOURCES\n\n'+json.dumps(packet,ensure_ascii=False,indent=2)
(AUDIT/'CODEX_STRAIN_EXACT_CONFERENCE.md').write_text(base,encoding='utf-8')
print(f'Built Strain conference: {len(cards)} exact Warrior cards, {len(packet["engine"])} engine references, {len(sections)} campaign sections, {len(base)} characters')
