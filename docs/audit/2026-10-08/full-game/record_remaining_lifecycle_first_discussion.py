from pathlib import Path
import json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/remaining_lifecycle_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
ids={r['bindingId'] for r in data['bindings']}
reply=(HERE/'GPT_REMAINING_LIFECYCLE_FIRST_REVIEW.md').read_text(encoding='utf-8')
roles={};expansions=[]
def common(a,b):
    n=0
    for x,y in zip(a,b):
        if x!=y:break
        n+=1
    return n
for line in reply.splitlines():
    cells=line.split('\t')
    if len(cells)!=3 or cells[0]=='Family':continue
    family,listed,classification=cells;previous=None
    for token in (x.strip() for x in listed.split(';')):
        if token.startswith('...'):
            suffix=token[3:]
            candidates=[i for i in ids if i.startswith(family.lower().replace(' ','-')+'.') and i.endswith(suffix)]
            assert candidates,(token,candidates)
            if len(candidates)>1:
                assert previous,(token,candidates)
                scores={i:common(i,previous) for i in candidates};best=max(scores.values())
                candidates=[i for i in candidates if scores[i]==best]
            assert len(candidates)==1,(token,candidates)
            ident=candidates[0];expansions.append({'printed':token,'context':previous,'resolvedId':ident})
        else:ident=token
        assert ident in ids and ident not in roles,(ident,classification)
        roles[ident]=classification;previous=ident
assert set(roles)==ids,{'missing':sorted(ids-set(roles)),'extra':sorted(set(roles)-ids)}
data['status']='SOURCE-AUDITED / DRAFTABLE:80+5 source conference discussed; boundary reconciliation and implementation pending'
for r in data['bindings']:
    r['classification']=roles[r['bindingId']]
    r['status']='DISCUSSED; supplied role only, implementation pending'
    r['reviewEvidence']=['GPT_REMAINING_LIFECYCLE_FIRST_REVIEW.md']
    r['operationalOverrides']=['First notebook conference classifies this exact role; pending reconciliation controls before implementation. No complete-card/family closure.']
    r['openIssues']=['Resolve named source gaps and cross-system edge cases; implement/validate only supplied lifecycle/object/guard roles. Incidental tempHP/TimeLoop/full effects stay deferred.']
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'REMAINING_LIFECYCLE_CLASSIFICATION_EXPANSIONS.json').write_text(json.dumps({'scope':'Exact abbreviated notebook table resolved against80 supplied unique IDs; longest explicit same-row prefix breaks suffix ambiguity.','resolvedCount':80,'abbreviations':expansions},indent=2)+'\n',encoding='utf-8')
print('All80 IDs individually classified once; preserved abbreviation expansions; no closure.')
