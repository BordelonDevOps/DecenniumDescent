"""Build a complete source-bound candidate; this does not approve or enable rules."""
import copy
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'
ABILITIES = ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']

def slug(text):
    return re.sub('[^a-z0-9]+','-',text.lower()).strip('-')

def asi(traits):
    text = next((t['text'] for t in traits if t['name']=='Ability Score Increase'), '')
    if 'ability scores each increase by 1' in text:
        return {a[:3].upper():1 for a in ABILITIES}
    return {a[:3].upper():int(n) for a,n in re.findall(r'(Strength|Dexterity|Constitution|Intelligence|Wisdom|Charisma) score increases by (\d+)',text)}

def main():
    if (ROOT/'docs/mechanics/ANCESTRY_BACKGROUND_REVIEW_STATUS.json').exists():
        raise SystemExit('Reviewed reference already exists. Preserve it and prepare a separately versioned revision instead of overwriting approved data.')
    evidence=json.loads((AUDIT/'ANCESTRY_BACKGROUND_SOURCE_EVIDENCE.json').read_text(encoding='utf-8'))
    original=(GAME/evidence['sourcePath']).read_text(encoding='utf-8-sig').splitlines()
    checks=[]
    def check(name,condition):
        checks.append({'check':name,'pass':bool(condition)})
    result={'schemaVersion':1,'status':'source-bound-candidate-pending-notebook-review',
            'cosmology':'Deferred until after successful GitHub push and verified remote commit. Original lore unchanged.',
            'source':{'path':evidence['sourcePath'],'sha256':evidence['sourceSha256']},
            'sourcePolicy':'Full book mechanics proposed over preserved builder alternatives; no duplicate racialFeat grants. Proposal is not yet active authority.',
            'ancestries':[],'backgrounds':[]}
    document=['# Ancestry and background source bindings', '', '**SOURCE REFERENCE — not operational approval.** This gathers all 14 base ancestries, 45 variants and 20 backgrounds without replacing original files. The notebook review and authored integration rules must resolve conflicts before these become active playtest rules.', '', 'Original source: `'+evidence['sourcePath']+'`; SHA-256 `'+evidence['sourceSha256']+'`.', '', 'Origin lore, age/alignment narratives and cosmological claims remain in the unchanged original. Their exclusion from this mechanical index is not deletion or a judgment about correctness. Cosmology review occurs only after verified GitHub delivery.', '', '[Conference proposal](../../../../docs/audit/2026-10-08/full-game/ANCESTRY_BACKGROUND_PROPOSAL.md) · [Spell dependency proposals](../../../../docs/audit/2026-10-08/full-game/ANCESTRY_SPELL_SUPPLEMENT_PROPOSAL.md)', '', '## Base and variant increases', '', '| Ancestry | Base increases | Variant additions |', '|---|---|---|']
    for a in evidence['ancestries']:
        base=asi(a['traits'])
        document.append('| '+a['name']+' | '+', '.join(k+' +'+str(v) for k,v in base.items())+' | '+'; '.join(v['name']+': '+(', '.join(k+' +'+str(n) for k,n in asi(v['traits']).items()) or 'none') for v in a['variants'])+' |')
    for a in evidence['ancestries']:
        row={'id':slug(a['name']),'name':a['name'],'abilityBonuses':asi(a['traits']),
             'traits':copy.deepcopy(a['traits']),'variants':[]}
        size_text=next(t['text'] for t in a['traits'] if t['name']=='Size')
        row['size']=re.search(r'your size is (Small|Medium|Large)',size_text,re.IGNORECASE).group(1).capitalize()
        speed_text=next(t['text'] for t in a['traits'] if t['name']=='Speed')
        row['baseWalkFeet']=int(re.search(r'(\d+) feet',speed_text).group(1))
        for v in a['variants']:
            adds=asi(v['traits']);total=dict(row['abilityBonuses'])
            for k,n in adds.items():total[k]=total.get(k,0)+n
            row['variants'].append({'id':slug(v['name']),'name':v['name'],'abilityBonuses':adds,'combinedAbilityBonuses':total,'traits':copy.deepcopy(v['traits'])})
        document.extend(['','## '+a['name'], ''])
        for owner in [row]+row['variants']:
            if owner is not row:document.extend(['','### '+owner['name'],''])
            for trait in owner['traits']:
                trait['id']=owner['id']+'--'+slug(trait['name'])
                trait['status']='source-bound-pending-operational-review'
                source_lines=[trait['sourceLine']]+trait.get('continuationLines',[])
                expected='\n'.join(original[n-1].strip() for n in source_lines)
                actual=trait['name']+'. '+trait['text']
                check('exact trait '+trait['id'],actual==expected)
                document.extend(['**'+trait['name']+'** (source line '+str(trait['sourceLine'])+'). '+trait['text'],''])
        result['ancestries'].append(row)
    for b in evidence['backgrounds']:
        row={'id':slug(b['name']),'name':b['name'],'status':'source-bound-pending-operational-review','source':copy.deepcopy(b['source'])}
        document.extend(['','## '+b['name'],''])
        for s in b['source']:
            check('exact background '+row['id']+' L'+str(s['line']),original[s['line']-1]==s['text'])
            field,value=s['text'].split(':',1)
            row[{'Skill Proficiencies':'skillsSource','Tool Proficiencies':'toolsSource','Languages':'languagesSource','Equipment':'equipmentSource','Feature':'featureSource'}[field]]=value.strip()
            document.extend(['Source line '+str(s['line'])+': '+s['text'],''])
        result['backgrounds'].append(row)
    check('all 14 ancestries',len(result['ancestries'])==14)
    check('all 45 variants',sum(len(a['variants']) for a in result['ancestries'])==45)
    check('all 20 backgrounds',len(result['backgrounds'])==20)
    by_name={a['name']:a for a in result['ancestries']}
    check('Troll Medium; Ogre Large',by_name['Troll']['size']=='Medium' and by_name['Ogre']['size']=='Large')
    check('Feykin book increases',by_name['Feykin']['abilityBonuses']=={'CHA':2,'DEX':1})
    check('Mycelian book increases',by_name['Mycelian']['abilityBonuses']=={'WIS':2})
    check('Human all six +1',by_name['Human']['abilityBonuses']=={a[:3].upper():1 for a in ABILITIES})
    check('Drakari no variant increases',all(not v['abilityBonuses'] for v in by_name['Drakari']['variants']))
    check('Nomadic total CON and WIS +2',next(v for v in by_name['Human']['variants'] if v['name']=='Nomadic Human')['combinedAbilityBonuses']=={'STR':1,'DEX':1,'CON':2,'INT':1,'WIS':2,'CHA':1})
    backgrounds={b['name']:b for b in result['backgrounds']}
    check('Guild artisan full correct skills',backgrounds['Guild Artisan Dropout']['skillsSource']=='Insight, Persuasion')
    check('Guild artisan restored language','languagesSource' in backgrounds['Guild Artisan Dropout'])
    for path,sha in evidence['protectedSources'].items():
        check('source preserved '+path,hashlib.sha256((GAME/path).read_bytes()).hexdigest()==sha)
    assert all(c['pass'] for c in checks),[c for c in checks if not c['pass']]
    (ROOT/'data/playtest/ancestry_background_candidate.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'docs/mechanics/ANCESTRY_BACKGROUND_SOURCE_BINDINGS.md').write_text('\n'.join(document)+'\n',encoding='utf-8')
    report={'status':'PASS — source coverage and integrity only; not mechanical approval','checks':len(checks),'ancestryTraitParagraphs':284,'backgroundSourceFields':sum(len(b['source']) for b in result['backgrounds']),'results':checks}
    (AUDIT/'ANCESTRY_BACKGROUND_SOURCE_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='results'}))

if __name__=='__main__':main()
