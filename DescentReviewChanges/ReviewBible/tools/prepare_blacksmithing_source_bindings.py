"""Derive source-only Blacksmithing bindings, without choosing output mechanics."""
from pathlib import Path
from collections import Counter
import json,re
ROOT=Path(__file__).resolve().parents[1];AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
def main():
    out=AUDIT/'BLACKSMITHING_EFFECT_CLASSIFICATION.json';assert not out.exists()
    x=json.loads((AUDIT/'BLACKSMITHING_SOURCE_PREPARATION.json').read_text(encoding='utf-8'));records=[]
    bindings={b['recipeId']:b for b in x['publicBookBindings']}
    lines=['# Blacksmithing preserved source bindings','','Source-only reference for the pending Blacksmithing conference. No base model, mass, structural profile, enhancement stacking or exact-card approval is implied. Full original records remain in BLACKSMITHING_SOURCE_PREPARATION.json. Cosmology remains post-push.','','| Recipe | Family | Visibility | Standard quantity | Current complete effect |','|---|---|---|---:|---|']
    for r in x['recipes']:
        m=re.fullmatch(r'Creates a durable (\w+) with \+(\d+) to attack and damage rolls(?: and (\d+d\d+) additional (\w+) damage once per turn)?\.',r['effects'])
        if m:
            v={'recipeId':r['id'],'family':r['recipeFamily'],'type':'weapon','attackBonus':int(m[2]),'damageBonus':int(m[2]),'bonusDamageDice':m[3],'bonusDamageType':m[4],'bonusDamageFrequencySource':'once per turn' if m[3] else None}
            assert m[1].lower()==r['recipeFamily'].lower() and int(m[2])==r['mechanics']['attackBonus']==r['mechanics']['damageBonus']
            assert r['mechanics']['bonusDamage']==(m[3]+' '+m[4] if m[3] else None)
        else:
            m=re.fullmatch(r'Creates reinforced (\w+) granting \+(\d+) AC(?: and resistance to (\w+) damage while worn)?\.',r['effects']);assert m,r['id']
            v={'recipeId':r['id'],'family':r['recipeFamily'],'type':'armor','armorBonus':int(m[2]),'resistance':m[3]}
            assert m[1].lower()==r['recipeFamily'].lower() and int(m[2])==r['mechanics']['armorBonus'] and m[3]==r['mechanics']['resistance']
        v.update(operativeTag=r['mechanics']['tag'],visibility=r['visibility'],standardQuantity=r['quantity'],currentEffect=r['effects'],legacyEffectPresent='legacyEffect' in r,legacyEffect=r.get('legacyEffect'),legacyEffectMatchesCurrent=r.get('legacyEffect')==r['effects'],sourceWorkHours=r['workRequirements']['activeWorkHours'])
        records.append(v)
        lines.append(f"| {r['id']} — {r['name']} | {r['recipeFamily']} | {r['visibility']} | {r['quantity']} | {r['effects']} |")
    lines+=['','## Exact source differences and public-book anchors','']
    for r in x['recipes']:
        lines += ['### '+r['id']+' — '+r['name'],'','**Current:** '+r['effects'],'','**Legacy effect:** '+(r['legacyEffect'] if 'legacyEffect' in r else 'No legacyEffect field in this source record.'),'','**Original tags:** '+', '.join(r['tags'])+'. **Current operative tag:** '+r['mechanics']['tag']+'.','',f"**Work:** {r['craftingTime']}; {r['workRequirements']['activeWorkHours']} active hours; fieldCraftable={r['workRequirements']['fieldCraftable']}; source time mode={r['workRequirements']['timeMode']}; maximum assistants={r['workRequirements']['maximumAssistants']}.",'']
        if r['id'] in bindings:
            lines+=['**V5 public binding:**']+[f"- Paragraph {p['index'] if 'index' in p else p.get('paragraphIndex',p.get('paragraph'))}: {p['text']}" for p in bindings[r['id']]['paragraphs']]+['']
        else:lines+=['**Public book:** no public binding; retain the source visibility gate.','']
    assert len(records)==43 and Counter(v['type'] for v in records)=={'weapon':27,'armor':16}
    report={'status':'source effects parsed and reconciled; no authored output approval','sourceSha256':x['sourceSha256'],'recipes':records,'familyCounts':dict(Counter(v['family'] for v in records)),'weaponElementalRiders':sum(v.get('bonusDamageDice') is not None for v in records),'sourceRecordsPreserved':43,'outputRulesApproved':False}
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (AUDIT/'BLACKSMITHING_SOURCE_BINDINGS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'sourceEffectsParsed':43,'weaponEffects':27,'armorEffects':16,'elementalRiders':report['weaponElementalRiders']}))
if __name__=='__main__':main()
