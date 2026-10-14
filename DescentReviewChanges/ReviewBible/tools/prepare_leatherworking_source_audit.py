"""Preserve Leatherworking originals and exact public-book bindings without approval."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import json,hashlib,zipfile,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    target=AUDIT/'LEATHERWORKING_SOURCE_PREPARATION.json'
    if target.exists():raise SystemExit('Leatherworking preparation already exists; inspect before replacing.')
    source=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json';s=json.loads(source.read_text(encoding='utf-8-sig'));rs=[r for r in s['recipes'] if r['skill']=='Leatherworking'];assert len(rs)==44
    book=GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx';w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    with zipfile.ZipFile(book) as z:tree=E.fromstring(z.read('word/document.xml'))
    ps=[''.join(t.text or '' for t in p.iter(w+'t')) for p in tree.iter(w+'p')];bindings=[];struct=[]
    for r in rs:
        hits=[i for i,t in enumerate(ps) if t.startswith('Formula ID: '+r['id']+' ')]
        if r['visibility']=='public':
            assert len(hits)==1,(r['id'],hits)
            i=hits[0];assert ps[i-4]=='Effect. '+r['effects'];bindings.append({'recipeId':r['id'],'effectMatches':True,'paragraphs':[{'index':j,'text':ps[j]} for j in range(i-5,i+1)]})
        else:assert not hits
        struct.append({'recipeId':r['id'],'quantity':r['quantity'],'maximumYield':3*r['quantity']//2,'sourceConsumedMassLb':float(sum(Fraction(str(c['weight']))*c['quantity'] for c in r['components'] if c['consumed'])),'sourceNonToolMassLb':float(sum(Fraction(str(c['weight']))*c['quantity'] for c in r['components'] if c['consumed'] and c['role']!='tool')),'componentRoles':dict(Counter(c['role'] for c in r['components'])),'nonconsumedRows':[{'componentIndex':i,**c} for i,c in enumerate(r['components']) if not c['consumed']],'sourceWorkHours':r['workRequirements']['activeWorkHours'],'effectType':r['mechanics']['type']})
    out={'status':'source preparation only; no authoring or exact-review approval','sourceSha256':sha(source),'bookSha256':sha(book),'sourceIndices':{r['id']:s['recipes'].index(r) for r in rs},'counts':dict(Counter(r['visibility'] for r in rs)),'effectTypes':dict(Counter(r['mechanics']['type'] for r in rs)),'recipes':rs,'publicBookBindings':bindings,'structuralAudit':struct}
    target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'recipes':len(rs),'publicBookMatches':len(bindings),'visibility':out['counts'],'effectTypes':out['effectTypes'],'recipesApproved':0}))
if __name__=='__main__':main()
