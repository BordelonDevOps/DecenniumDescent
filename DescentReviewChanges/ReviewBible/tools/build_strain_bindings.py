"""Build explicit namespace-reference bindings, never automatic application triggers."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]


def main():
    packet=json.loads((GAME/'docs/audit/2026-10-08/full-game/STRAIN_SOURCE_BINDINGS.json').read_text(encoding='utf-8'))
    bindings=[]
    for record in packet['engine']:
        bindings.append({'sourceId':f"warrior.engine.{record['index']}",
                         'trackId':'warrior.serum-strain','role':'namespace-reference',
                         'source':{'path':packet['warriorPath'],'kind':'engine',**record}})
    for record in packet['cards']:
        bindings.append({'sourceId':record['card']['id'],'trackId':'warrior.serum-strain',
                         'role':'namespace-reference','source':{'path':packet['warriorPath'],'kind':'card',**record}})
    for identity,paragraph in [('core.quickglass.crash',8529),('core.morale-rest',8514)]:
        row=next(r for r in packet['core']['paragraphs'] if r['paragraph']==paragraph)
        bindings.append({'sourceId':identity,'trackId':'expedition.strain','role':'namespace-reference',
                         'source':{'path':packet['core']['path'],'kind':'core-paragraph','bookSha256':packet['core']['sha256'],**row}})
    for identity in ['campaign.rest-debt','campaign.unsupported-supply','recovery.wound-treatment.critical-failure']:
        bindings.append({'sourceId':identity,'trackId':'expedition.strain','role':'namespace-reference',
                         'source':{'path':packet['gameplayPath'],'kind':'campaign-reference','sha256':packet['gameplaySha256']}})
    data={'schemaVersion':'0.1','status':'IN_REVIEW',
          'scope':'Explicit meaning of Strain references in the supplied sources. Binding a reference does not activate a feature, create a point or grant immunity.',
          'tracks':[{'id':'warrior.serum-strain','minimum':0,'maximum':3,'authority':'preserved class engine'},
                    {'id':'expedition.strain','minimum':0,'maximum':6,'authority':'retained provisional campaign overlay; not promoted into Core'}],
          'bindings':bindings,
          'reviewEvidence':['docs/audit/2026-10-08/full-game/GPT_STRAIN_FIRST_REVIEW.md',
                            'docs/audit/2026-10-08/full-game/GPT_STRAIN_COUNTEREXAMPLE_REVIEW.md'],
          'unboundPolicy':'Reject unknown or ambiguous source; never infer track from display name alone.',
          'openIssues':['Exact implementation review; broader rest, travel and class semantic dependencies remain separate.']}
    out=ROOT/'data/playtest/strain_bindings.json'
    if out.exists():
        previous=json.loads(out.read_text(encoding='utf-8'))
        if previous.get('bindings')==bindings and previous.get('status','').startswith('REVIEWED'):
            for key in ('status','reviewEvidence','openIssues'):
                data[key]=previous[key]
    out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Built {len(bindings)} source-qualified Strain namespace bindings; status {data["status"]}')


if __name__=='__main__':
    main()
