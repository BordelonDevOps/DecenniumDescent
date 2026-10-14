"""Prepare a losslessly compacted complete Blacksmithing exact-review packet."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import hashlib,json
from prepare_cooking_exact_review import common,delta,merge
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compact(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    target=AUDIT/'CODEX_BLACKSMITHING_EXACT_REVIEW.txt';assert not target.exists() and not (AUDIT/'CODEX_BLACKSMITHING_EXACT_REVIEW_SENT.txt').exists()
    validation=read(AUDIT/'BLACKSMITHING_CANDIDATE_VALIDATION.json');assert validation['status']=='PASS'
    data=read(ROOT/'data/director/blacksmithing_recipe_candidate_internal.json');cards=data['cards'];source=read(AUDIT/'BLACKSMITHING_SOURCE_PREPARATION.json')
    manuscript=(ROOT/'docs/director-only/BLACKSMITHING_INTERNAL_RECIPE_CARDS.md').read_text(encoding='utf-8')
    paragraphs=manuscript.split('\n\n');counts=Counter(paragraphs);shared_paragraphs={f'P{i+1}':p for i,p in enumerate(p for p in dict.fromkeys(paragraphs) if counts[p]>1 and len(p)>90)}
    reverse={p:k for k,p in shared_paragraphs.items()};template='\n\n'.join('[[PARAGRAPH '+reverse[p]+']]' if p in reverse else p for p in paragraphs)
    reconstructed=template
    for k,p in shared_paragraphs.items():reconstructed=reconstructed.replace('[[PARAGRAPH '+k+']]',p)
    assert reconstructed==manuscript
    ops=[];texts={};example_rows={};example_fields=None;example_scope=None;rational_fields=[]
    for c in cards:
        o=deepcopy(c['operational']);texts[c['recipeId']]=o.pop('text');examples=o.pop('standardModelExamples');ops.append(o)
        fields=[k for k in examples[0] if k!='exampleScope']
        if example_fields is None:
            example_fields=fields;example_scope=examples[0]['exampleScope'];rational_fields=[k for k in fields if isinstance(examples[0][k],dict)]
        assert fields==example_fields and all(e['exampleScope']==example_scope for e in examples)
        rows=[]
        for e in examples:rows.append([[e[k]['numerator'],e[k]['denominator']] if k in rational_fields else e[k] for k in fields])
        example_rows[c['recipeId']]=rows
    shared_ops=common(ops);overrides={c['recipeId']:delta(o,shared_ops) for c,o in zip(cards,ops)}
    for c in cards:
        o=merge(shared_ops,overrides[c['recipeId']]);begin=manuscript.index('## '+c['recipeId']+' — ');end=manuscript.find('\n## recipe-',begin+1);section=manuscript[begin:end if end>=0 else len(manuscript)]
        text=section.split('**Operational effect:** ',1)[1].split('\n\n',1)[0];assert text==texts[c['recipeId']];o['text']=text
        o['standardModelExamples']=[]
        for row in example_rows[c['recipeId']]:
            e={k:({'numerator':v[0],'denominator':v[1]} if k in rational_fields else v) for k,v in zip(example_fields,row)};e['exampleScope']=example_scope;o['standardModelExamples'].append(e)
        assert o==c['operational'],c['recipeId']
    equipment=read(ROOT/'data/playtest/equipment_acquisition_candidate.json');equipment_by={e['id']:e for e in equipment['items']};models=deepcopy(data['baseModels'])
    for id,m in models.items():
        record=m.pop('sourceEquipmentRecord')
        m['sourceEquipmentRecordRef']=id if record is not None else None
        assert record==(equipment_by[id] if record is not None else None)
        restored={k:v for k,v in m.items() if k!='sourceEquipmentRecordRef'};restored['sourceEquipmentRecord']=deepcopy(equipment_by[id]) if record is not None else None;assert restored==data['baseModels'][id]
    envelope={k:v for k,v in data.items() if k not in ['cards','baseModels']}
    intro='''Codex to Calibration Review: complete exact Blacksmithing manuscript review.

Your source conference 5869023f-1971-470c-9a61-27c9e5b04668 (reply cf2d76f8-6a76-4f9c-9b1a-090902276b54) and eight-interface follow-up a184686d-59a2-4c32-8cca-797b936060d5 (reply b6a2393c-128e-4d3e-8111-07130d94daa2) are implemented. All 43 exact cards are now drafted: 27 public, four restricted, twelve Director-only; 40 finite base profiles and 248 legal model-choice examples. No Blacksmithing approval is counted yet: aggregate remains 175 reviewed / 512 remaining, public 111/433.

Please review the full shared guide, all 43 exact cards, complete operational projections and worked cases. Give a bounded approve/repair verdict for the authored operational PLAYTEST scope. If finite edits suffice, state whether their exact implementation plus validation allows promotion without another generic conference. This is not a request for human balance, ingredient availability, runtime, whole-game flow or GitHub delivery approval. No original information has been deleted. Cosmology remains strictly after the authorized push succeeds and its remote commit is verified.

All 44 source/projection checks pass, including 4,116 bounded durability states and all 248 model-choice arithmetic examples. All 32 protected original and prior reviewed artifacts remain unchanged. Every complete original recipe is retained losslessly in each card's sourceRecipe field. All 27 public effects match actual V5 paragraphs. The source and equipment catalogs were supplied in full in the source conference and remain unchanged.

One timing point remains deliberately pending for exact precision: your outside/inside transition guard refers to the first actual turn before the six-second deadline. Does the first actual turn immediately after entry satisfy that guard even if this item makes no attack in it, or should the guard attach to the first actual turn in which use is attempted? Please specify the precise state transition. Also confirm that outside windows use a recorded origin and elapsed-time window index, rather than an early attack roll restarting a window. The current draft preserves your language and does not claim this last interpretation settled.

Please especially check prior Flawed/improved bases, actual ordered reserves and damaged outputs, Crude negative modifiers without a phantom zero, two-shield resistance versus one selected shield AC, mundane grade preservation, repair without formula access, physical workmanship under suppression, and current source fields versus legacy/tags/donor metadata.

LOSSLESS PACKET FORMAT:
1. The shared guide is reproduced in full.
2. The complete internal manuscript is factored only by repeated exact paragraphs. Expand each [[PARAGRAPH Pn]] token with its literal definition from the shared paragraph dictionary. The expanded string equals the saved full manuscript exactly, locally asserted. All unique effects, model tables, source components and card identities are present.
3. The operational JSON is COMMON plus recursive recipe overrides. Each card's operational text is the exact **Operational effect:** paragraph in that card's reconstructed manuscript. standardModelExamples are the complete ordered row matrices below with named columns; rational columns store [numerator,denominator]. Restore the common exampleScope to every row. Reconstruction equals every original operational object for all 43 cards, locally asserted.
4. All 40 base model projections are supplied. sourceEquipmentRecordRef refers to the unchanged complete equipment record of that exact ID already provided in the source conference; null means a NEW accessory body. Replacing each ref with its actual original record reconstructs all 40 full base models exactly, locally asserted. The equipment source SHA is repeated. The source/conference fields and all shared machine rules are supplied intact.
5. Original V4 recipe records are unchanged from the full source conference; their hash/indices and all V5 public bindings are repeated. No source field is being silently discarded or renamed by this compact transmission.
'''
    projection={'envelope':envelope,'baseModelsWithImmutableEquipmentRefs':models,'equipmentSourceSha256':sha(ROOT/'data/playtest/equipment_acquisition_candidate.json'),'operationalCOMMON':shared_ops,'recipeOperationalOverrides':overrides,'operationalTextSource':'the exact Operational effect paragraph of the same recipe card','modelExampleScope':example_scope,'modelExampleColumns':example_fields,'modelExampleRationalColumns':rational_fields,'modelExampleRows':example_rows}
    blocks=[intro,'\nFULL SHARED GUIDE\n',(ROOT/'docs/mechanics/BLACKSMITHING_RECIPE_PLAYTEST.md').read_text(encoding='utf-8'),'\nEXACT MANUSCRIPT SHARED PARAGRAPHS\n']
    for k,p in shared_paragraphs.items():blocks.append('\n'+k+'\n'+p)
    blocks+=['\nCOMPLETE MANUSCRIPT WITH EXACT PARAGRAPH REFERENCES\n',template,'\nCOMPLETE LOSSLESS OPERATIONAL PROJECTION\n',compact(projection),'\nIMMUTABLE SOURCE AND PUBLIC BOOK BINDINGS\n',compact({k:source[k] for k in ['sourceSha256','bookSha256','sourceIndices','publicBookBindings']}),'\nWORKED RULE TRACES AND EXACT TIMING QUESTION\n',(AUDIT/'BLACKSMITHING_REVIEW_CASES.md').read_text(encoding='utf-8'),'\nVALIDATION REPORT\n',compact(validation)]
    packet='\n'.join(blocks);target.write_text(packet,encoding='utf-8')
    paths=['docs/mechanics/BLACKSMITHING_RECIPE_PLAYTEST.md','docs/mechanics/BLACKSMITHING_PUBLIC_RECIPE_CARDS.md','docs/director-only/BLACKSMITHING_INTERNAL_RECIPE_CARDS.md','data/playtest/blacksmithing_recipe_candidate.json','data/director/blacksmithing_recipe_candidate_internal.json']
    dump(AUDIT/'BLACKSMITHING_EXACT_SUBMISSION.json',{'status':'prepared-not-sent','packetCharacters':len(packet),'packetSha256':sha(target),'losslessManuscriptReconstruction':True,'losslessOperationalReconstructions':43,'losslessBaseModelReconstructions':40,'modelChoiceExamples':248,'sharedParagraphs':len(shared_paragraphs),'artifactHashes':{str((ROOT/p).relative_to(GAME)).replace('\\','/'):sha(ROOT/p) for p in paths}})
    print(json.dumps({'characters':len(packet),'sharedParagraphs':len(shared_paragraphs),'operationalReconstructions':43,'baseModels':40,'modelExamples':248}))
if __name__=='__main__':main()
