"""Bind all agreed transport profiles into a complete, reversible candidate view."""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import json
import re

G = Path(r'C:\Github\DecenniumDescent')
R = G/'DescentReviewChanges/ReviewBible'
A = G/'docs/audit/2026-10-08/full-game'
P = A/'ex58-final-gpt-verdict'

def read(p): return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def save(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def label(s):
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])',' ',s).replace('NEW','New ').strip().capitalize()
def value(v):
    if v is None:return 'Unspecified (null preserved)'
    if isinstance(v,bool):return 'Yes' if v else 'No'
    if isinstance(v,(int,float)):return format(v,'g')
    return str(v)
def fields(d,depth=3):
    out=[]
    for k,v in d.items():
        if isinstance(v,dict):
            out += ['#'*min(depth,6)+' '+label(k),'']+fields(v,depth+1)
        elif isinstance(v,list):
            if not v:out += ['**'+label(k)+':** None listed.','']
            elif all(not isinstance(x,(dict,list)) for x in v):out += ['**'+label(k)+':** '+', '.join(value(x) for x in v)+'.','']
            else:out += ['**'+label(k)+'**','', '```json',json.dumps(v,ensure_ascii=False,indent=2),'```','']
        else:out += ['**'+label(k)+':** '+value(v),'']
    return out

def render(public):
    out=['# Transport catalogue — complete provisional profiles','',public['notice'],'',
         'These are game profiles. A listed type and price do not establish that a particular animal, crew, berth or vehicle is available, healthy, trained, willing, staffed or supplied. Record the actual individual/body and its current state before using it. Size, mass, defenses, attacks, training, provisions and new vehicle statistics are explicit provisional design choices wherever the source supplied none. They are not real-world animal or vessel specifications.','',
         'The nine mounts retain their source purchase prices, walking Speeds and carrying pounds. The other original rows retain their printed prices or variable-price rule. Original blank/comma/null fields remain preserved in the internal source envelope; the new operating values do not overwrite them.','',
         'Use these profiles with the forthcoming complete transport procedure chapter. The catalogue alone does not enable selection, approve pending mounted feats or replace exact living-creature, object, command, travel, loading and repair procedures.','',
         '## Catalogue index','','| Entry | Type | Price |','|---|---|---|']
    for p in public['profiles']:
        o=p['operational'];price=(value(o['priceCp']/100)+' gp') if 'priceCp' in o else o['priceRule']
        out += ['| '+p['name']+' | '+p['kind'].replace('-',' ')+' | '+price.replace('|','\\|')+' |']
    out += ['','## Mount comparison','','Body mass is separate from its carried burden. Draw rating is for an actually trained, harnessed animal on the specified feasible route; it is not additional back capacity.','',
            '| Mount | Size | Body lb | Speed ft | Carry lb / Load | Draw lb | AC / HP | Feed lb / day | Water pints / day |',
            '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for p in public['profiles']:
        if p['kind']=='living-mount':
            o=p['operational'];out += [f"| {p['name']} | {o['size']} | {value(o['baseBodyMassLb'])} | {o['walkingSpeedFt']} | {value(o['carryPounds'])} / {value(o['cargoLoadCapacity'])} | {o['grossDrawLimitLb']} | {o['naturalAC']} / {o['maximumHP']} | {o['dailyFeed']['feedMassLb']} | {o['dailyWaterPints']} |"]
    out += ['','## Vessel crew comparison','','Crew counts include helm. Only the Rowboat combines helm and oar work in one person’s Action. Purchase includes no crew.','',
            '| Vessel | Oar crew | Sail crew | Oar ft / mph | Sail ft / mph | Occupants including crew |',
            '|---|---:|---:|---:|---:|---:|']
    for p in public['profiles']:
        if p['kind']=='watercraft':
            o=p['operational'];c=o['requiredActiveCrewByModeIncludingHelm'];speed=o['tacticalSpeedFtByMode'];mph=o['travelMphByMode']
            rates=lambda m: f"{speed[m]} / {value(mph[m])}" if m in speed else 'No mode'
            out += [f"| {p['name']} | {c.get('oar','No mode')} | {c.get('sail','No mode')} | {rates('oar')} | {rates('sail')} | {o['maximumOccupantsIncludingCrew']} |"]
    for p in public['profiles']:
        out += ['', '## '+p['name'],'','Profile reference: '+p['id']+'.','']+fields(p['operational'])
    out += ['','## Auxiliary equipment and Core transport bodies','','These four entries are separate from the 29 Player source rows.','']
    for p in public['auxiliaryProfiles']:
        out += ['### '+p['id'],'']+fields({k:v for k,v in p.items() if k!='id'},4)
    return '\n'.join(out)

def main():
    paths={'public':R/'data/public/expedition_candidate/transport_profiles.json',
           'internal':R/'data/director/expedition_candidate/transport_profiles.json',
           'catalogue':R/'docs/mechanics/expedition/TRANSPORT_CATALOGUE_CANDIDATE.md',
           'receipt':A/'EX58_TRANSPORT_CATALOGUE_CANDIDATE_CHECK.json'}
    assert not any(p.exists() for p in paths.values()),'Preserve previous catalogue outputs before revision'
    checks=[]
    def ck(n,v):
        checks.append({'name':n,'pass':bool(v)})
        assert v,n
    source=read(P/'EX58_TRANSPORT_PROFILES.json')
    manifest=read(P/'FILE_MANIFEST.json')
    expected=next(x for x in manifest['files'] if x['path']=='EX58_TRANSPORT_PROFILES.json')
    ck('Profile source exact delivered hash',info(P/expected['path'])=={k:expected[k] for k in ['bytes','sha256']})
    ck('Exactly 29 distinct original entries',len(source['profiles'])==len({p['id'] for p in source['profiles']})==29)
    ck('Exactly four distinct auxiliary entries',len(source['auxiliaryProfiles'])==len({p['id'] for p in source['auxiliaryProfiles']})==4)
    ck('Nine mounts, five drawn vehicles, six watercraft', [sum(p['kind']==k for p in source['profiles']) for k in ['living-mount','drawn-vehicle','watercraft']]==[9,5,6])
    public={'schemaVersion':1,'moduleId':'EX58-TRANSPORT-CATALOGUE','status':'authored-profile-candidate-awaiting-complete-chapter-and-exact-review',
            'notice':'Complete candidate catalogue derived from GPT’s agreed source profiles. The transport procedure chapter, integrated worked records and exact candidate review remain ahead.',
            'selectionEnabled':False,'newPromotions':0,
            'profiles':[{'id':p['id'],'name':p['name'],'kind':p['kind'],'operationalStatus':p['operationalStatus'],'operational':p['operational']} for p in source['profiles']],
            'auxiliaryProfiles':source['auxiliaryProfiles']}
    dirs=read(R/'data/director/expedition_candidate/source_register_corrected.json')['directions']
    internal={'schemaVersion':1,'moduleId':public['moduleId'],'status':public['status'],
              'publicEnvelope':public,'completeOriginalProfileEnvelope':source,
              'completeTransportDirections':[x for x in dirs if x['id'].startswith('TR-')],
              'profileSource':{'path':(P/'EX58_TRANSPORT_PROFILES.json').relative_to(G).as_posix(),**info(P/'EX58_TRANSPORT_PROFILES.json')},
              'assemblyBoundary':'This catalogue binds all supplied operating profile fields without substitution. It does not count any of the fourteen TR chapters complete; full teaching prose, family boundary cases and integrated records remain to assemble.',
              'runtimeImplemented':False,'humanBalanceConfirmed':False,'newPromotions':0,'sourceInformationDeleted':0}
    for p,q in zip(source['profiles'],public['profiles']):
        ck('Whole operational profile retained '+p['id'],p['operational']==q['operational'])
        ck('Actual source identity retained '+p['id'],p['id']==p['sourceRecord']['id'])
        if 'priceCp' in p['operational']:
            ck('Printed price retained '+p['id'],p['operational']['priceCp']==p['sourceRecord']['sourcePriceCp'])
    ck('Four complete auxiliary profiles retained',public['auxiliaryProfiles']==source['auxiliaryProfiles'])
    ck('All fourteen controlling transport directions bound',len(internal['completeTransportDirections'])==14)
    rendered=render(public)
    save(paths['public'],public);save(paths['internal'],internal)
    paths['catalogue'].parent.mkdir(parents=True,exist_ok=True);paths['catalogue'].write_text(rendered,encoding='utf-8',newline='\n')
    ck('Entire public envelope parity',read(paths['public'])==read(paths['internal'])['publicEnvelope'])
    ck('Complete original source envelope retained',read(paths['internal'])['completeOriginalProfileEnvelope']==source)
    ck('Entire catalogue rendering parity',paths['catalogue'].read_text('utf-8')==render(read(paths['public'])))
    for p in source['profiles']:
        ck('Whole original row, null and placeholders retained '+p['id'],next(x for x in read(paths['internal'])['completeOriginalProfileEnvelope']['profiles'] if x['id']==p['id'])['sourceRecord']==p['sourceRecord'])
    for x in manifest['files']:ck('Original final payload unchanged '+x['path'],info(P/x['path'])=={k:x[k] for k in ['bytes','sha256']})
    receipt={'generatedAtUtc':datetime.now(timezone.utc).isoformat(),'status':public['status'],'profiles':29,'auxiliaryProfiles':4,
             'transportDirectionsBoundButNotCountedAsAuthored':14,'fullChapterCoverageStill':38,
             'checks':len(checks),'failures':[c for c in checks if not c['pass']],
             'outputs':{p.relative_to(G).as_posix():info(p) for k,p in paths.items() if k!='receipt'},
             'builder':{'path':Path(__file__).resolve().relative_to(G).as_posix(),**info(Path(__file__))},
             'scope':'Complete profile/source-envelope equality, prices, distinct identity counts and complete catalogue rendering. No gameplay, admission, action, repair or simulation execution.',
             'runtimeTestsExecuted':0,'newPromotions':0,'sourceInformationDeleted':0,'details':checks}
    save(paths['receipt'],receipt)
    print(json.dumps({k:receipt[k] for k in ['status','profiles','auxiliaryProfiles','checks','failures','outputs']},indent=2))

if __name__=='__main__':main()
