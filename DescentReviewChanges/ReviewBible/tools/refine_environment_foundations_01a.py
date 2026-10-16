"""Close three explicit authoring gaps before an actual environment conference."""
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p):return json.loads(p.read_bytes())
def main():
    root=A/'environment-foundations-local-draft-01';history=root/'history/before-refinement-01a'
    receipt=A/'ENVIRONMENT_FOUNDATIONS_DRAFT_01A_REFINEMENT.json'
    assert not history.exists() and not receipt.exists()
    m=read(root/'MODEL.json');cb=read(root/'CASEBOOK.json');assert cb['count']==56
    before=[];history.mkdir(parents=True)
    for p in root.iterdir():
        if p.is_file():
            dest=history/p.name;dest.write_bytes(p.read_bytes());before.append({'before':info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    now=datetime.now(timezone.utc).isoformat()
    oracle=R/'data/public/class_playtests/oracle.json';assert oracle.relative_to(G).as_posix() not in [x['path'] for x in m['sourceBindings']]
    m['sourceBindings'].append(info(oracle))
    # The Oracle source was read/frozen at draft creation through the recon card selector;
    # this adds its missing full-file binding without claiming the earlier manifest had it.
    card=next(x for x in m['currentClassCards'] if x['file']==oracle.relative_to(G).as_posix())
    def objs(x):
        if isinstance(x,dict):
            yield x
            for v in x.values():yield from objs(v)
        elif isinstance(x,list):
            for v in x:yield from objs(v)
    actual=[x for x in objs(read(oracle)) if x.get('id')==card['record']['id']]
    assert len(actual)==1 and actual[0]==card['record']
    breath=next(p for p in m['procedures'] if p['id']=='EF-02')
    target='A creature already partway through deprivation keeps its existing unused reserve/grace instead of receiving a new snapshot. Stat changes and form changes alone do not refill either allowance.'
    replacement=target+' If a newly breathing body has no established prior breathing record and has not actually completed six seconds of breathing, initialize zero reserve and the current calculated grace once. Do not infer an inhalation from spawning into the scene, a form change or a character-sheet edit.'
    i=next(i for i,s in enumerate(breath['rules']) if target in s);breath['rules'][i]=breath['rules'][i].replace(target,replacement,1)
    weather=next(p for p in m['procedures'] if p['id']=='EF-07')
    target="The same feature's overlapping adjustments use the strongest single change rather than accumulating five-mph steps. Existing gale can be reduced by five mph; no infinite repeated reduction."
    replacement="For each of wind and rain, the same feature's overlapping adjustments use the largest absolute single change; equal changes with opposing directions use the earlier still-active application. Apply that one adjustment to the actual unmodified local weather, never to the already-adjusted output. A recast by the same creature replaces that creature's earlier Storm Magic adjustment, including its residual adjustment, rather than adding another source; other casters retain their own actual endings. Existing gale can be reduced by five mph; no infinite repeated reduction."
    i=next(i for i,s in enumerate(weather['rules']) if target in s);weather['rules'][i]=weather['rules'][i].replace(target,replacement,1)
    m['climateAcceptanceBindings']=[{'sourceAuditQuestion':i+1,'question':question,'proposedProcedureIds':ids,'status':'proposed-answer; not accepted'} for i,(question,ids) in enumerate(zip(read(A/'ENVIRONMENT_CHAPTER_REFERENCE_AUDIT_01.json')['acceptanceQuestions'],[['EF-03'],['EF-03'],['EF-04'],['EF-04'],['EF-01','EF-04'],['EF-03','EF-04'],['EF-04'],['EF-03'],['EF-03'],['EF-02','EF-03'],['EF-01','EF-03']]))]
    additions=[
      ('EF-C57',['EF-02'],'A still-living suffocating creature legally becomes a truly nonbreathing body while at 0 HP.','Suppress suffocation prohibition and enforcement while that body does not need to breathe, preserving exhausted reserve/grace. No HP or stabilization is granted. An actual eligible healer can now recover HP. Reverting without air reactivates suffocation immediately; a form change does not create breath.'),
      ('EF-C58',['EF-07'],'Two different casters have equal opposing five-mph Storm Magic adjustments; the reduction was applied first to actual 22-mph wind.','Use the earlier active reduction: 17 mph. If it actually ends while the increase remains, use actual baseline 22 plus 5 = 27 mph. Do not add 5 to the formerly adjusted 17. A same-caster recast replaces that caster’s old adjustment rather than stacking residuals.'),
      ('EF-C59',['EF-02'],'A previously nonbreathing creature with no stored breathing record becomes an ordinary CON+2 breathing body where no breathable medium is available.','Initialize reserve 0 and grace 12 once. Without actual respiration it begins suffocating after 12 seconds, not after a fabricated 180-second inhalation. Six continuous actual breathing seconds would establish the full reserve.')
    ]
    for cid,ids,given,result in additions:cb['cases'].append({'id':cid,'procedureIds':ids,'given':given,'proposedAdjudication':result,'status':'authored-example; not runtime-tested or jointly accepted'})
    spacing={'one1d6':'one 1d6','next1d6':'next 1d6','One3d6':'One 3d6','one failure':'one failure','one actual':'one actual','itsWater':'its Water','keepone':'keep one','live0':'live 0','T121':'T121','source remainsout':'source remains out','Retainthin':'Retain thin','useAthletics15':'use Athletics 15','Existing wind22mph':'Existing wind 22 mph','StormMagic':'Storm Magic','belowstrongwind':'below strong-wind','actual residual/concentration':'actual residual/concentration','actual new magical cause later creates severeweather':'actual new magical cause later creates severe weather','newcause':'new cause','actual newcause':'actual new cause','stillgale':'still gale','EyeoftheStorm':'Eye of the Storm','full10minutes':'full 10 minutes','unfinishedcold':'unfinished cold','completed30minutes':'completed 30 minutes','existingcold':'existing cold','levelsremain':'levels remain','Clothingdrying':'Clothing drying','breathrefill':'breath refill','actualconditions':'actual conditions','bridgegustSTR15':'bridge gust STR 15','movedoffedge':'moved off edge','andmadeProne':'and made Prone','actualProne':'actual Prone','explicitProne':'explicit Prone','blocksProne':'blocks Prone','actualpushremains':'actual push remains','after10continuousminutes':'after 10 continuous minutes','localair5°C':'local air 5 °C','wet-coldprofile':'wet-cold profile','precedingdrytenminutes':'preceding dry ten minutes','duehazard':'due hazard','activecoldcause':'active cold cause','genericremovalofthatblocked-sourceExhaustion':'generic removal of that blocked-source Exhaustion','eight-hourrest':'eight-hour rest','orerase':'or erase','newlevel':'new level','scenechange':'scene change','WarriorSurvivalAdaptation':'Warrior Survival Adaptation','choosescold':'chooses cold','while cold2':'while cold 2','partialprogressalreadyexist':'partial progress already exists','suppresscold1/2ordinarypenalties':'suppress cold 1/2 ordinary penalties','foractualfeature':'for actual feature','Preserveprogress/levels':'Preserve progress/levels','future saves andseparateExhaustiongain':'future saves and separate Exhaustion gain','actualadvantage/resistancecomponents':'actual advantage/resistance components','enters dry20°C':'enters dry 20 °C','for90 continuous':'for 90 continuous','fresh30':'fresh 30','airless six seconds':'airless six seconds'}
    for c in cb['cases']:
        for field in ['given','proposedAdjudication']:
            for a,b in spacing.items():c[field]=c[field].replace(a,b)
    cb['count']=len(cb['cases']);assert cb['count']==59
    m['recordedAtUtc']=now;m['refinement']='01A: missing full Oracle file binding; no-history breath initialization; opposed/recast Storm Magic priority; eleven proposed climate acceptance answers; three new authored situations.'
    (root/'MODEL.json').write_bytes(encoded(m));(root/'CASEBOOK.json').write_bytes(encoded(cb))
    intro='# Environmental foundations — discussion draft\n\n**NEW local proposals. Not submitted, agreed or active rules.** This draft supplies concrete procedures for actual GPT discussion. Source books and reviewed rules remain unchanged.\n\n'
    body='\n\n'.join('## '+p['id']+' — '+p['title']+'\n\n'+'\n\n'.join(p['rules']) for p in m['procedures'])
    (root/'PLAYER_DISCUSSION.md').write_text(intro+body+'\n',encoding='utf-8',newline='\n')
    director=intro+'Read [the full proposal](PLAYER_DISCUSSION.md) before the examples. The original five climate references and all earlier draft files remain preserved. These are proposed outcomes, not completed gameplay tests.\n\n'
    director+='## Decisions requiring actual conference\n\n'+'\n'.join('- '+s for s in m['reviewRequired'])+'\n\n'
    director+='## Authored situations\n\n'+'\n\n'.join('### '+c['id']+'\n\n'+c['given']+'\n\nProposed result: '+c['proposedAdjudication'] for c in cb['cases'])+'\n'
    (root/'DIRECTOR_DISCUSSION.md').write_text(director,encoding='utf-8',newline='\n')
    checks=[{'check':'all25 source files match their recorded bindings','passed':all(info(G/r['path'])==r for r in m['sourceBindings'])},{'check':'all13 current class cards have full-file source bindings','passed':all(x['file'] in [r['path'] for r in m['sourceBindings']] for x in m['currentClassCards'])},{'check':'all59 case IDs unique and earlier56 preserved','passed':len({c['id'] for c in cb['cases']})==59 and [c['id'] for c in cb['cases'][:56]]==[c['id'] for c in read(history/'CASEBOOK.json')['cases']]},{'check':'eleven climate questions now have proposed procedure links','passed':len(m['climateAcceptanceBindings'])==11},{'check':'no prior file discarded','passed':all(info(G/r['preservedCopy'])['sha256']==r['before']['sha256'] for r in before)},{'check':'no adoption or submission','passed':not m['newRulesAdopted'] and not m['activeOperational'] and not m['submittedToGpt']}]
    assert all(c['passed'] for c in checks)
    (root/'LOCAL_CHECKS.json').write_bytes(encoded({'refinement':'01A','checks':checks,'count':len(checks),'failureCount':0,'earlierChecks':info(history/'LOCAL_CHECKS.json'),'scope':'Source/selection/preservation checks only, not behavior or balance.'}))
    (root/'MANIFEST.json').write_bytes(encoded({'id':'ENVIRONMENT-FOUNDATIONS-DRAFT-MANIFEST-01A','files':[info(p) for p in sorted(root.iterdir()) if p.is_file() and p.name!='MANIFEST.json'],'sourceBindings':m['sourceBindings'],'history':before,'newRulesAdopted':False}))
    result={'recordedAtUtc':now,'model':info(root/'MODEL.json'),'casebook':info(root/'CASEBOOK.json'),'playerDiscussion':info(root/'PLAYER_DISCUSSION.md'),'directorDiscussion':info(root/'DIRECTOR_DISCUSSION.md'),'manifest':info(root/'MANIFEST.json'),'originalPreparation':info(A/'ENVIRONMENT_FOUNDATIONS_DRAFT_01_PREPARATION.json'),'history':before,'sourceFiles':len(m['sourceBindings']),'actualClassCards':len(m['currentClassCards']),'actualRecipeCards':len(m['currentRecipeCards']),'procedures':7,'authoredSituations':59,'climateAcceptanceAnswersProposed':11,'checks':checks,'failures':0,'submitted':False,'newRulesAdopted':False,'sourceInformationDeleted':0}
    receipt.write_bytes(encoded(result));print(json.dumps({'receipt':info(receipt),'model':result['model'],'casebook':result['casebook'],'sources':25,'cases':59,'failures':0,'newRulesAdopted':False}))
if __name__=='__main__':main()
