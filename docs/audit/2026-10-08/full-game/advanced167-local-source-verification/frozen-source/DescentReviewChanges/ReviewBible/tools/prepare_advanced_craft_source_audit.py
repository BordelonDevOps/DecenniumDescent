"""Preserve final four trade sources and identify operational gaps without deciding them."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,hashlib,re,zipfile,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
TRADES=('Enchanting','Rune Carving','Scribing','Tinkering')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ratio(x):return {'numerator':x.numerator,'denominator':x.denominator}
def leafdiff(a,b,path=''):
    if type(a)!=type(b):return [{'path':path,'current':a,'other':b}]
    if isinstance(a,dict):return [v for k in a.keys()|b.keys() for v in leafdiff(a.get(k),b.get(k),path+'/'+k)]
    if isinstance(a,list):return [{'path':path,'current':a,'other':b}] if len(a)!=len(b) else [v for i,(x,y) in enumerate(zip(a,b)) for v in leafdiff(x,y,path+'/'+str(i))]
    return [] if a==b else [{'path':path,'current':a,'other':b}]
def create(p,s):
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    target=AUDIT/'ADVANCED_CRAFT_SOURCE_PREPARATION.json';notes=AUDIT/'ADVANCED_CRAFT_SOURCE_AUDIT.md'
    assert not target.exists() and not notes.exists()
    paths={'mechanicalV4':ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json','internalV4':GAME/'data/director/Decennium_Descent_Crafting_Bible_v4_Full_Internal.json','v2':GAME/'DescentReviewChanges/crafting-bible/Decennium_Descent_Crafting_Bible_v2.json','publicRuntime':GAME/'src/data/crafting-recipes.json'}
    hashes={k:sha(p) for k,p in paths.items()};source=read(paths['mechanicalV4']);rs=[r for r in source['recipes'] if r['skill'] in TRADES];by={r['id']:r for r in rs}
    checks=[]
    def check(name,ok):checks.append({'name':name,'pass':bool(ok)})
    check('167 unique sources:43Enchanting41Rune40Scribing43Tinkering',len(rs)==len(by)==167 and Counter(r['skill'] for r in rs)=={'Enchanting':43,'Rune Carving':41,'Scribing':40,'Tinkering':43})
    check('100public7restricted60Director-only boundary',Counter(r['visibility'] for r in rs)=={'public':100,'restricted':7,'director-only':60})
    book=GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx'
    with zipfile.ZipFile(book) as z:tree=E.fromstring(z.read('word/document.xml'))
    w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}';ps=[''.join(t.text or '' for t in p.iter(w+'t')) for p in tree.iter(w+'p')]
    bindings=[];gated_absent=True;struct=[]
    for r in rs:
        hits=[i for i,p in enumerate(ps) if p.startswith('Formula ID: '+r['id']+' ')]
        if r['visibility']=='public':
            assert len(hits)==1,(r['id'],hits)
            i=hits[0];bindings.append({'recipeId':r['id'],'effectMatches':ps[i-4]=='Effect. '+r['effects'],'paragraphs':[{'index':j,'text':ps[j]} for j in range(i-5,i+1)]})
        else:gated_absent &= not hits
        consumed=[c for c in r['components'] if c['consumed']]
        struct.append({'recipeId':r['id'],'trade':r['skill'],'family':r['recipeFamily'],'quantity':r['quantity'],'maximumYield':3*r['quantity']//2,'sourceConsumedMassLb':ratio(sum((F(str(c['weight']))*c['quantity'] for c in consumed),F(0))),'sourceConsumedValueGp':ratio(sum((F(str(c['value']))*c['quantity'] for c in consumed),F(0))),'sourceUnitReferenceGp':ratio(F(str(r['economy']['recommendedMarketValue']))/r['quantity']),'sourceWorkRequirements':r['workRequirements'],'abilityOptions':r['craftingCheck']['abilityOptions'],'trivialAtSkillLevel':r['skillProgression']['trivialAtSkillLevel'],'mechanics':r['mechanics']})
    check('All100 public effects exactly match actual V5 paragraphs',len(bindings)==100 and all(b['effectMatches'] for b in bindings))
    check('All67 gated formulas absent from public V5',gated_absent)
    check('All167 resultItem mechanics match main source',all(r['resultItem']['mechanics']==r['mechanics'] for r in rs))
    check('All four trades preserve INT crafting and false field flags',all(r['craftingCheck']['abilityOptions']==['Intelligence'] and r['workRequirements']['fieldCraftable'] is False for r in rs))
    nulls=[{'recipeId':r['id'],'craftingTime':r['craftingTime'],'activeWorkHours':r['workRequirements']['activeWorkHours'],'laborValue':r['economy']['laborValue']} for r in rs if r['workRequirements']['activeWorkHours'] is None]
    check('Only recipe623 retains null work-hours,one-year text and zero labor',len(nulls)==1 and nulls[0]=={'recipeId':'recipe-623','craftingTime':'1 year','activeWorkHours':None,'laborValue':0})
    enchant=[r for r in rs if r['skill']=='Enchanting'];runes=[r for r in rs if r['skill']=='Rune Carving'];scripts=[r for r in rs if r['skill']=='Scribing' and r['mechanics']['type']=='script'];tinkers=[r for r in rs if r['skill']=='Tinkering']
    check('43Enchanting bonus and charge numbers match printed prose',all(f"+{r['mechanics']['bonus']} enhancement and {r['mechanics']['charges']} charge" in r['effects'] for r in enchant))
    check('All43 Enchanting sources explicitly recharge at dawn',all('charges return at dawn' in r['effects'] for r in enchant))
    ordinary_runes=[r for r in runes if 'charges' in r['mechanics']]
    check('40 Rune charge counts printed;667 retains distinct no-charge schema',len(ordinary_runes)==40 and all(f"{r['mechanics']['charges']} charge" in r['effects'] for r in ordinary_runes) and 'charges' not in by['recipe-667']['mechanics'])
    check('No Rune source effect supplies a recharge instruction',all(not any(t in r['effects'].lower() for t in ['recharge','return at dawn','long rest','short rest']) for r in runes))
    field_path=AUDIT/'CRAFTING_EFFECT_FIELD_AUDIT.json';field=read(field_path);selected=[r for r in field['recipes'] if r['recipeId'] in by]
    uses=[{'recipeId':r['recipeId'],'visibility':r['visibility'],'sourceEffect':r['sourceEffect'],'finding':v} for r in selected for v in r['selectedNumericFields'] if v['field']=='uses']
    check('22 preserved Scribing use-count ambiguities,19one-use and3two-use fields',len(scripts)==len(uses)==22 and Counter(r['mechanics']['uses'] for r in scripts)=={1:19,2:3} and all(v['finding']['status']=='use-count-not-expressed-in-prose' for v in uses))
    check('Numeric audit evidence still equals all167 current effects',len(selected)==167 and all(r['sourceEffect']==by[r['recipeId']]['effects'] for r in selected))
    autos=[r for r in tinkers if r['mechanics'].get('deviceKind')=='automaton'];traps=[r for r in tinkers if r['mechanics'].get('deviceKind')=='trap'];utility=[r for r in tinkers if r['mechanics'].get('deviceKind')=='utility']
    check('Tinkering preserves11traps18automata12utility1drone1siege',Counter(r['mechanics']['deviceKind'] for r in tinkers)=={'trap':11,'automaton':18,'utility':12,'drone':1,'siege':1})
    check('All18 automata AC/HP/encounter counts match printed effect',all(f"AC {r['mechanics']['armorClass']}, {r['mechanics']['hitPoints']} HP" in r['effects'] and f"{r['mechanics']['charges']} encounter" in r['effects'] for r in autos))
    check('All18 automata omit attack bonus,damage andSpeed mechanics',all(all(k not in r['mechanics'] for k in ['attackBonus','damage','speed','speedFeet']) for r in autos))
    check('11 traps and12utility devices print their charge counts',all(f"{r['mechanics']['charges']} charge" in r['effects'] for r in traps+utility))
    custom_ids=['recipe-667','recipe-674','recipe-675','recipe-686','recipe-687']
    custom=[{'recipeId':id,'name':by[id]['name'],'visibility':by[id]['visibility'],'effects':by[id]['effects'],'mechanics':by[id]['mechanics'],'scope':'Literal source evidence only. No missing field is borrowed from another recipe schema; no cosmological interpretation.'} for id in custom_ids]
    check('Five distinct custom records retained without synthesized common fields',len(custom)==5 and all(r['effects']==by[r['recipeId']]['resultItem']['properties'][0] for r in custom))
    components=[{'recipeId':r['id'],'trade':r['skill'],'componentIndex':i,'sourceComponent':c} for r in rs for i,c in enumerate(r['components'])]
    reusable=[x for x in components if x['sourceComponent']['role']=='tool' and not x['sourceComponent']['consumed']];consumed=[x for x in components if x['sourceComponent']['role']=='tool' and x['sourceComponent']['consumed']];catalysts=[x for x in components if x['sourceComponent']['role']=='catalyst']
    check('758 component occurrences preserve90 reusable and6consumed tool rows',len(components)==758 and len(reusable)==90 and len(consumed)==6)
    check('All172 catalyst occurrences are consumed in source',len(catalysts)==172 and all(x['sourceComponent']['consumed'] for x in catalysts))
    engine_path=ROOT/'data/playtest/crafting_engine_candidate.json';engine=read(engine_path);trades=[r for r in engine['trades'] if r['name'] in TRADES]
    check('Four existing artisan credentials and tool bindings retained',len(trades)==4 and all(t['artisanTool'] for t in trades) and next(t for t in trades if t['name']=='Scribing')['primaryTool']=="Calligrapher's supplies")
    versions={}
    for version,p in paths.items():
        d=read(p);versions[version]={r['id']:r for r in (d if isinstance(d,list) else d['recipes'])}
    fields=['name','effects','mechanics','quantity','components','workRequirements','craftingCheck','economy','visibility','discovery'];comparisons=[];diff=[]
    for r in rs:
      for version,rows in versions.items():
        if version=='mechanicalV4' or r['id'] not in rows:continue
        other=rows[r['id']]
        for key in fields:
            same=(key in r)==(key in other) and r.get(key)==other.get(key);comparisons.append({'recipeId':r['id'],'version':version,'field':key,'equal':same})
            if not same:diff.append({'recipeId':r['id'],'version':version,'field':key,'currentFieldPresent':key in r,'currentValue':r.get(key),'otherFieldPresent':key in other,'otherValue':other.get(key)})
    check('All167 source identities in internalV4 andV2',all(all(r['id'] in versions[v] for r in rs) for v in ['internalV4','v2']))
    check('Public runtime contains exactly100 public formula identities',{r['id'] for r in versions['publicRuntime'].values() if r['skill'] in TRADES}=={r['id'] for r in rs if r['visibility']=='public'})
    visibility_diff=[d for d in diff if d['field']=='visibility'];name_records=[d for d in diff if d['field']!='visibility']
    name_leaves=[{'recipeId':d['recipeId'],'version':d['version'],**leaf} for d in name_records for leaf in leafdiff(d['currentValue'],d['otherValue'],'/'+d['field'])]
    check('4340 compared fields retain167 missingV2 visibility and58 named-tool/component differences',len(comparisons)==4340 and len(diff)==225 and len(visibility_diff)==167 and all(d['version']=='v2' and not d['otherFieldPresent'] for d in visibility_diff) and len(name_records)==58)
    check('All58 other differences are exact preserved Focusing-to-Resonance name correspondences',len(name_leaves)==58 and Counter((d['version'],d['field']) for d in name_records)=={('internalV4','workRequirements'):21,('v2','workRequirements'):21,('internalV4','components'):8,('v2','components'):8} and all((d['current'],d['other']) in [('Resonance lens','Focusing crystal'),('Resonance Lens','Focusing Crystal')] and by[d['recipeId']]['skill']=='Rune Carving' for d in name_leaves))
    history_path=AUDIT/'CRAFTING_HISTORY_RECONCILIATION.md';history_paras=history_path.read_text(encoding='utf-8').split('\n\n');history_quote=next(p for p in history_paras if p.startswith('The full internal V4 file has the same 687 identities'))
    protected=read(AUDIT/'TAILORING_PART2_REVIEW_BASELINE.json')['files'];check('All53 protected original and reviewed inputs unchanged',len(protected)==53 and all(sha(GAME/p)==h for p,h in protected.items()))
    check('All compared source files unchanged',all(sha(paths[k])==h for k,h in hashes.items()))
    assert all(c['pass'] for c in checks),[c['name'] for c in checks if not c['pass']]
    out={'status':'PASS — complete internal source audit; not sent; no operational decisions','trades':list(TRADES),'sourceSha256':hashes['mechanicalV4'],'bookSha256':sha(book),'sourceIndices':{r['id']:source['recipes'].index(r) for r in rs},'counts':dict(Counter(r['visibility'] for r in rs)),'tradeSummaries':{trade:{'recipes':sum(r['skill']==trade for r in rs),'families':dict(Counter(r['recipeFamily'] for r in rs if r['skill']==trade)),'visibility':dict(Counter(r['visibility'] for r in rs if r['skill']==trade)),'components':sum(len(r['components']) for r in rs if r['skill']==trade)} for trade in TRADES},'recipes':rs,'publicBookBindings':bindings,'structuralAudit':struct,'componentOccurrences':len(components),'reusableToolOccurrences':reusable,'consumedToolOccurrences':consumed,'catalystOccurrences':catalysts,'sourceHourNulls':nulls,'scribingUseQuestions':uses,'customSourceEffects':custom,'automatonMissingAttackFields':[{'recipeId':r['id'],'sourceMechanics':r['mechanics'],'printedEffect':r['effects'],'missingOperationalDecisions':['attack accuracy and damage','speed andmovement','task andcommand actions','encounter service boundary','ownership control and resource accounting']} for r in autos],'numericAuditReference':{'file':field_path.relative_to(GAME).as_posix(),'sha256':sha(field_path),'records':selected,'scope':'Historical field comparison; matching numbers are not complete operational-card approval.'},'reviewedTradeBindings':{'file':engine_path.relative_to(GAME).as_posix(),'sha256':sha(engine_path),'trades':trades},'versionAudit':{'sourcePaths':{k:p.relative_to(GAME).as_posix() for k,p in paths.items()},'sourceHashes':hashes,'fields':fields,'comparisons':comparisons,'differences':diff,'fieldComparisons':len(comparisons),'matchingFields':sum(c['equal'] for c in comparisons)},'checks':checks,'protectedFilesUnchanged':53,'recipesApproved':0,'sourceInformationDeleted':0,'cosmology':'No interpretation reviewed; literal named restrictions retained; cosmology remains post-push.'}
    out['sourceNameCorrespondences']={'leafDifferences':name_leaves,'uniqueAffectedRecipes':sorted({d['recipeId'] for d in name_leaves}),'historyFile':history_path.relative_to(GAME).as_posix(),'historySha256':sha(history_path),'exactHistoricalParagraph':history_quote,'interpretation':'Observed textual correspondence only. No new material substitution permission or cosmology ruling; both names,stableIDs,quantities,values,roles andconsumption remain preserved.'}
    create(target,json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    text=f'''# Final four crafting trades — source audit

Internal preparation only; no new source/interface or exact-card approval. **167 full sources** are preserved: Enchanting43,Rune Carving41,Scribing40,Tinkering43; **100 public / seven restricted / sixty Director-only**. All100 public effects match their actual V5 paragraphs. **{len(checks)} checks pass**, including4,340 source-field comparisons:4,115 equal and225 differences. These comprise167 absent V2 visibility fields plus58 Focusing crystal/Crystal versus Resonance lens/Lens differences across the internalV4 andV2 comparisons. Each version differs in21 tool lists andeight component-name records,all within21 Rune recipes; every other field in those records matches. This reproduces the earlier history audit and grants no material substitution.53 protected files remain unchanged.

## Enchanting

Nine families share the instruction to imbue one compatible item with a+1/+2/+3 enhancement and1–6 charges, restored at dawn. Every printed bonus/charge number matches the source. This is not yet a complete effect: compatible base, enhancement target/family, charge action,target,range,power,duration and resolution remain unspecified. Damage-type fields do not by themselves establish damage dice or authorize deriving healing, flight, sentience or command from a title. Complete bodies, existing imprints, supplemental reserves and cross-trade arbitration require decisions. All199 component occurrences remain, including80 consumed catalysts,12 reusable tools andtwo consumed Focusing lenses.

## Rune Carving

Six families contain40 ordinary charged runes and one distinct Seal. Ordinary runes cover binding,explosion,warding andhealing;19 warding profiles mention an attuned bearer as a data trigger. Charges1–6 are printed, but no Rune effect supplies a recharge instruction. Do not inherit Enchanting's dawn reset. Trigger boundaries,arming,action costs,target selection,same-event multiple triggers,escape/repeat saves,successful explosion saves,healing eligibility and bearer attunement must be explicit. The unique recipe667 has radius20feet,duration1hour,DC28 Charisma and printed movement restrictions, but no charge field; missing values are not zero and cannot be synthesized from adjacent records. Its exact Matrical-adjacent wording is retained without cosmological interpretation. All188 components,41 catalysts and17 reusable tools remain. The21 public Rune recipes use Resonance lens in their current required tools, while their older versions and the generic trade reference say Focusing crystal; eight consumed component names differ correspondingly. Preserve both representations and resolve the exact kit/ingredient binding in conference rather than silently renaming a source or making a consumed ingredient reusable.

## Scribing

Nine families contain22 spell-storage scripts and18 references. Every script's prose says one stored spell or ritual; data separately contains uses1 for19 scripts and uses2 for3. Those22 unresolved use counts are retained verbatim with the previous numeric audit. Capacity does not establish casting,consumption,copying or recharge. Spell level,formula access,material/component costs,casting permission,activation and research assistance all need rules. Eleven maps/diagrams have once-per-expedition rerolls requiring an actual expedition boundary. Recipe674 supplies3 Language Insight and cross-disciplinary research;recipe675's willing bargain,6d10 psychic breach,30-day mark and hidden annotation need a finite procedure. No inference about souls,cosmology or universal contract enforcement is made. All177 components,42 catalysts,28 reusable tools andone consumed Protective case remain.

## Tinkering

Seven families contain11 traps,18 ordinary automata,12 utility devices,one command Drone andone siege device. All18 ordinary automata preserve their printed AC,HP and encounter counts, but have no attack bonus,damage orSpeed fields despite promising a basic attack. Complete stat/action/control/service procedures are needed. Creature/object classification,actual carrying,mundane body construction,repair and charge servicing cannot be decided from the Clockwork name. Recipe686 explicitly excludes Silent Ones andHeartcell systems from command; that prohibition is preserved without inspecting their cosmology. Recipe687's12d10 force siege and once-per-long-rest magical breach need target resolution,operating budget and recharge ownership. Recipe623 retains its source one-year,null hours andzero labor; no time overlay is adopted here. All194 components,9 catalysts,33 reusable tools andthree consumed tool rows remain.

## Common source preservation and next step

All167 formulas use INT and fieldCraftable:false. Their four reviewed credentials are artisan tools, including Scribing bound to Calligrapher's supplies. That credential evidence does not determine use permissions for the finished objects. The758 component occurrences include90 reusable tools,six explicitly consumed tool rows and172 consumed catalysts. Preserve every original quantity,tier,value,role,consumption flag,status,needsReview field,legacy effect and source null. Existing structural-quality rules do not automatically increase charges,spell level,command count,damage or item powers.

The [complete source evidence](ADVANCED_CRAFT_SOURCE_PREPARATION.json) includes all originals,100 book bindings,31 family counts,exact version differences,selected numeric-audit records,five distinct custom profiles and18 incomplete automaton interfaces. This is unsent evidence. Consequential mechanics must be discussed with GPT and exact authored cards reviewed afterward. Runtime parity,human balance,material availability and final whole-game flow remain separate. The user-directed cosmology review remains after the successful authorized GitHub push and verification of its remote commit.
'''
    create(notes,text)
    print(json.dumps({'status':'PASS','recipes':len(rs),'publicBookBindings':len(bindings),'checks':len(checks),'sourceFieldComparisons':len(comparisons),'components':len(components),'reusableToolRows':len(reusable),'consumedToolRows':len(consumed),'catalysts':len(catalysts),'scribingUseQuestions':len(uses),'incompleteAutomata':len(autos),'recipesApproved':0}))
if __name__=='__main__':main()
