from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
original=json.loads((HERE/'REMAINING_LIFECYCLE_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
rows=list(original['classRecords'])
additions={'cleric':{'engines':[10],'cards':[]},'oracle':{'engines':[19,29],'cards':[]},
           'soldier':{'engines':[3],'cards':['soldier.arch.fortify-zone','soldier.hero.champion.wall-of-aegis']}}
for owner,select in additions.items():
    path=f'data/public/class_playtests/{owner}.json'
    data=json.loads((ROOT/path).read_text(encoding='utf-8'))
    for i in select['engines']:
        text=data['engine'][i]
        rows.append({'kind':'class-engine','owner':owner,'path':path,'engineIndex':i,'text':text,
                     'textSha256':hashlib.sha256(text.encode()).hexdigest(),
                     'candidateOrigin':'Semantic supplement: exact acquisition, agency, copy or TierII object boundary.'})
    for ident in select['cards']:
        card=next(c for c in data['cards'] if c['id']==ident)
        rows.append({'kind':'class-card','owner':owner,'path':path,'card':card,'sourceObjectSha256':digest(card),
                     'candidateOrigin':'Semantic supplement: distinguish named protection effect from physical object.'})
def ident(r):return r['card']['id'] if r['kind']=='class-card' else f"{r['owner']}.engine[{r['engineIndex']}]"
assert len(rows)==len({ident(r) for r in rows})==80
data={**original,'scope':'80 exact passages:74 remaining original lexical candidates plus6 semantic supplements. Unreviewed lifecycle/guard/tempHP classification; full effects not certified.',
      'originalInventoryCandidates':74,'semanticSupplements':6,'classRecords':rows}
(HERE/'REMAINING_LIFECYCLE_CONFERENCE_SOURCES.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Preserved80 exact next-conference passages:74 original+6 semantic supplements.')
