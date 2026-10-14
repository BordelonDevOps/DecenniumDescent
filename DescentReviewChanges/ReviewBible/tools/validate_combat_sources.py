"""Verify the exact Core/V6 combat packet, without claiming operational closure."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
PACKET=GAME/'docs/audit/2026-10-08/full-game/COMBAT_ACTION_VISION_SOURCE_PACKET.json'

def main():
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    packet=json.loads(PACKET.read_text(encoding='utf-8'))
    issues=[]
    results=[]
    for source in packet:
        path=GAME/source['path']
        actual_hash=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash!=source['sha256']:
            issues.append(source['path']+': book hash changed')
        with ZipFile(path) as archive:
            tree=ElementTree.fromstring(archive.read('word/document.xml'))
        paragraphs=[''.join(t.text or '' for t in p.findall('.//w:t',ns))
                    for p in tree.findall('.//w:p',ns)]
        positions=set()
        for row in source['paragraphs']:
            index=row['paragraph']
            if index in positions:
                issues.append(f'{path.name}: duplicate paragraph {index}')
            positions.add(index)
            if index>=len(paragraphs) or paragraphs[index]!=row['text']:
                issues.append(f'{path.name}: source text mismatch at {index}')
        results.append({'path':source['path'],'sha256':actual_hash,'exactParagraphs':len(positions)})
    report={'status':'FAIL' if issues else 'PASS','scope':'Exact source packet integrity only. Operational review status and limits are recorded in COMBAT_ACTION_PLAYTEST.md.',
        'paragraphConvention':'zero-based all w:p descendants','sources':results,
        'exactParagraphs':sum(r['exactParagraphs'] for r in results),'issues':issues}
    (ROOT/'docs/mechanics/COMBAT_SOURCE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f"{report['status']}: {len(results)} unchanged source books, {report['exactParagraphs']} exact combat paragraphs")
    if issues:
        raise SystemExit(1)

if __name__=='__main__':
    main()
