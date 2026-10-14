"""Project exact source equipment tables without approving proposed mechanics."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'

def number(s):
    s=s.strip().replace(',','').replace('½',' 1/2')
    try: return float(sum(Fraction(x) for x in s.split()))
    except (ValueError,ZeroDivisionError): return None

def slug(s):
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

def main():
    ev=json.loads((AUDIT/'EQUIPMENT_SOURCE_EVIDENCE.json').read_text(encoding='utf-8'))
    # Stable labels do not copy long explanatory paragraphs as headings.
    labels=['Starting wealth','Currency','Trade goods','Armor and shields','Donning and doffing',
      'Simple melee weapons','Simple ranged weapons','Martial melee weapons','Martial ranged weapons',
      'Ammunition','Arcane focuses','Druidic focuses','Holy symbols','Alchemical containers',
      'Adventuring gear','Tools','Mounts vehicles and services']
    records=[]; out=['# Equipment source tables','',
      '**SOURCE REFERENCE — not a standalone operational guide.** These are the complete Player V6 equipment tables. New equipment procedures and conflicts require their separately reviewed guide. The original source, including blank values and alternate procedures, is preserved. A blank source weight is unknown, not zero.','',
      f"Source: `{ev['player']['path']}`; SHA-256 `{ev['player']['sha256']}`.",'']
    for label,t in zip(labels,ev['tables'],strict=True):
        out += ['## '+label,'',f"Player source table begins at line {t['startLine']}.",'',
          '| '+' | '.join(t['headers'])+' | Source line |',
          '| '+' | '.join(['---']*(len(t['headers'])+1))+' |']
        group=None
        for x in t['rows']:
            f=x['fields'];name=next(iter(f.values()))
            if x['group']!=group:
                group=x['group']
                if group:out+=['| **'+group+'** | '+' | '.join(['']*len(t['headers']))+' |']
            price=f.get('Cost'); weight=f.get('Weight'); nominal=None; source_weight=None
            if price:
                m=re.fullmatch(r'([\d,./ ]+)\s+(cp|sp|gp|pp)',price)
                if m:nominal=number(m[1])*{'cp':1,'sp':10,'gp':100,'pp':1000}[m[2]]
            if weight:
                m=re.match(r'([\d,./½ ]+)\s*lb',weight)
                if m:source_weight=number(m[1])
            rec={'id':slug(label)+'.'+slug(name),'name':name,'category':label,'group':group,
                 'status':'source-projection-only','sourceLine':x['line'],'sourceFields':f,
                 'sourcePriceCp':nominal,'sourceWeightLb':source_weight,
                 'sourceWeightIncludesContents':bool(weight and '(full)' in weight)}
            records.append(rec)
            out+=['| '+' | '.join(f.values())+' | '+str(x['line'])+' |']
        out+=['']
    src=GAME/ev['player']['path']; lines=src.read_text(encoding='utf-8-sig').splitlines()
    packs=[{'sourceLine':i,'text':lines[i-1]} for i in range(6920,6927)]
    out+=['## Seven equipment packs','']
    out += [f"**Source line {x['sourceLine']}.** {x['text']}\n" for x in packs]
    data={'schemaVersion':'1.0','status':'source-projection-only; equipment manuscript pending review',
          'source':{'path':ev['player']['path'],'sha256':ev['player']['sha256']},
          'numericPolicy':'Null means absent or nonnumeric in the source. Price is for the printed bundle, not necessarily one unit. No operation or quality approval is implied.',
          'records':records,'packs':packs}
    (ROOT/'data/playtest/equipment_source_catalog.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'docs/mechanics/EQUIPMENT_SOURCE_BINDINGS.md').write_text('\n'.join(out)+'\n',encoding='utf-8')
    checks={'status':'PASS','records':len(records),'uniqueIds':len({x['id'] for x in records}),
            'tables':len(labels),'packs':len(packs),'allRowsBound':sum(len(t['rows']) for t in ev['tables'])==len(records),
            'sourceHashMatches':hashlib.sha256(src.read_bytes()).hexdigest()==ev['player']['sha256']}
    assert checks['records']==checks['uniqueIds'] and checks['allRowsBound'] and checks['sourceHashMatches']
    (AUDIT/'EQUIPMENT_CATALOG_SOURCE_VALIDATION.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(checks))
    print('unparsed weights',[(x['name'],x['sourceFields']['Weight']) for x in records if x['sourceWeightLb'] is None and 'Weight' in x['sourceFields'] and x['sourceFields']['Weight'] not in [',','-','—','']])

if __name__=='__main__':main()
