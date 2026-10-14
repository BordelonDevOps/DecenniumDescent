"""Verify Strain source identities before interpreting the colliding names."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]


def main():
    packet=json.loads((GAME/'docs/audit/2026-10-08/full-game/STRAIN_SOURCE_BINDINGS.json').read_text(encoding='utf-8'))
    warrior=json.loads((ROOT/packet['warriorPath']).read_text(encoding='utf-8'))
    cards={c['id']:c for c in warrior['cards']}
    issues=[]
    for row in packet['engine']:
        text=warrior['engine'][row['index']]
        if text!=row['text'] or hashlib.sha256(text.encode()).hexdigest()!=row['textSha256']:
            issues.append('Warrior engine mismatch:'+str(row['index']))
    for row in packet['cards']:
        card=cards.get(row['card']['id'])
        digest=hashlib.sha256(json.dumps(card,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
        if card!=row['card'] or digest!=row['sourceObjectSha256']:
            issues.append('Warrior card mismatch:'+row['card']['id'])
    path=ROOT/packet['gameplayPath']
    if hashlib.sha256(path.read_bytes()).hexdigest()!=packet['gameplaySha256']:
        issues.append('Gameplay reference hash changed')
    guide=path.read_text(encoding='utf-8')
    for row in packet['gameplaySections']:
        if row['exactText'] not in guide:
            issues.append('Gameplay section mismatch:'+row['heading'])
    core=packet['core']
    path=GAME/core['path']
    if hashlib.sha256(path.read_bytes()).hexdigest()!=core['sha256']:
        issues.append('Core book hash changed')
    with ZipFile(path) as z:
        tree=ElementTree.fromstring(z.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paragraphs=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in tree.findall('.//w:p',ns)]
    for row in core['paragraphs']:
        if paragraphs[row['paragraph']]!=row['text']:
            issues.append('Core paragraph mismatch:'+str(row['paragraph']))
    report={'status':'FAIL' if issues else 'PASS','scope':'Exact Strain source integrity only; operational review status and limits are recorded in STRAIN_PLAYTEST.md.',
            'warriorEngines':len(packet['engine']),'warriorCards':len(packet['cards']),
            'gameplaySections':len(packet['gameplaySections']),'coreParagraphs':len(core['paragraphs']),
            'issues':issues}
    (ROOT/'docs/mechanics/STRAIN_SOURCE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(report)
    if issues:
        raise SystemExit(1)


if __name__=='__main__':
    main()
