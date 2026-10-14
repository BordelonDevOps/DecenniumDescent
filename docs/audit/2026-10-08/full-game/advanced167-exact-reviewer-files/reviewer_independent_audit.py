"""Read-only independent audit of the frozen advanced-crafting handoff.
Uses only the Python standard library. Does not mutate submitted files or model
an advanced-crafting runtime. Findings are distinguished from passing checks.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from xml.etree import ElementTree as ET
import hashlib, json, math, sys, zipfile

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/mnt/data/advanced_exact_work')
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('/mnt/data/advanced_exact_reviewer/independent_audit.json')
ARCHIVE = Path('/mnt/data/DD_Advanced_Craft_167_Exact_Review_v1.zip')
B = ROOT/'DescentReviewChanges/ReviewBible'
A = ROOT/'docs/audit/2026-10-08/full-game'

def load(path): return json.loads(path.read_text(encoding='utf-8'))
def sha_bytes(x): return hashlib.sha256(x).hexdigest()
def sha(path): return sha_bytes(path.read_bytes())
def canonical(x): return sha_bytes(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
def f(x): return Fraction(x['numerator'], x['denominator'])
checks = []
def check(name, result): checks.append({'name':name, 'pass':bool(result)})

manifest=load(ROOT/'FILE_MANIFEST.json')
with zipfile.ZipFile(ARCHIVE) as z:
    check('archive sha256',sha(ARCHIVE)=='a29420353145c4c91ebb472f2843a3ea14041b38eb49b93420ec99294c03b1a7')
    check('195 payloads plus README and manifest',len(manifest)==195 and len([i for i in z.infolist() if not i.is_dir()])==197)
    for path, m in manifest.items():
        data=z.read(path)
        check('frozen payload '+path,len(data)==m['bytes'] and sha_bytes(data)==m['sha256'])
protected=load(A/'ADVANCED_CRAFT_JOINT_SUBMISSION.json')['currentFileHashes']
check('138 protected source/dependency files',len(protected)==138)
for path,h in protected.items(): check('protected '+path,sha(ROOT/path)==h)
check('final source authority',sha(A/'GPT_ADVANCED_167_SOURCE_AUTHORING_VERDICT.md')=='48f885becd03e4a99ba8d6243ce286c1e1e88cfefc776af9ff89a9182c79c8e0')

D=load(B/'data/director/advanced_craft_recipe_candidate_internal.json')
P=load(B/'data/crafting/advanced_craft_recipe_candidate_public.json')
S=load(B/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')
original={r['id']:r for r in S['recipes']}
internal={c['recipeId']:c for c in D['cards']}
public={c['recipeId']:c for c in P['cards']}
expected={f'recipe-{n}' for n in list(range(121,160))+list(range(636,640))+list(range(396,433))+list(range(664,668))+list(range(471,507))+list(range(672,676))+list(range(585,624))+list(range(684,688))}
check('all167 exact identities',len(D['cards'])==167 and set(internal)==expected)
check('all100 exact public identities',len(P['cards'])==100 and set(public)=={k for k,c in internal.items() if c['visibility']=='public'})
check('trade counts',Counter(c['sourceRecipe']['skill'] for c in D['cards'])=={'Enchanting':43,'Rune Carving':41,'Scribing':40,'Tinkering':43})
check('visibility100/7/60',Counter(c['visibility'] for c in D['cards'])=={'public':100,'restricted':7,'director-only':60})
check('body22/15 and hosts50',len(D['bodyModels'])==22 and len(P['bodyModels'])==15 and len(D['enchantingHostModels'])==50)
check('full public host parity',P['enchantingHostModels']==D['enchantingHostModels'])
check('embedded public guide parity',P['operatingGuideText']==(B/P['guide']).read_text(encoding='utf-8') and P['bodyGuideText']==(B/P['bodyGuide']).read_text(encoding='utf-8'))

eq={x['id']:x for x in load(B/'data/playtest/equipment_acquisition_candidate.json')['items']}
for k,h in D['enchantingHostModels'].items():
    e=eq[k]
    check(k+' full original equipment identity',h['sourceEquipmentRecord']==e)
    check(k+' mass and price',Fraction(str(e['unitPriceCp']))/100==f(h['ordinaryPriceGp']) and e['unitWeightLb']==h['ordinaryWeightLb'])
    hp = 5 if h['bodyKind']=='EN-weapon' else {'Light Armor':10,'Medium Armor':15,'Heavy Armor':20}[e['group']]
    check(k+' ordinary structural base',h['baselineStructuralHP']==hp)

ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with zipfile.ZipFile(ROOT/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx') as z:
    xml=ET.fromstring(z.read('word/document.xml'))
paras=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in xml.findall('.//w:body//w:p',ns)]
trades=['Enchanting','Rune Carving','Scribing','Tinkering']
man_i={t:(B/f"docs/director-only/{t.upper().replace(' ','_')}_INTERNAL_RECIPE_CARDS.md").read_text(encoding='utf-8') for t in trades}
man_p={t:(B/f"docs/mechanics/{t.upper().replace(' ','_')}_CANDIDATE_RECIPE_CARDS.md").read_text(encoding='utf-8') for t in trades}
coverage=[];profiles=Counter();comp=Counter();effect_groups={};body_memberships={k:[] for k in D['bodyModels']}
for c in D['cards']:
    k=c['recipeId'];s=c['sourceRecipe'];o=c['operational'];w=o['work'];q=s['quantity'];profiles[o['profile']]+=1
    check(k+' complete original object and index',s==original[k] and S['recipes'][c['sourceRecipeIndex']]==s and c['sourceObjectSha256']==canonical(s))
    check(k+' complete manuscript',c['manuscriptText'] in man_i[s['skill']] and all(p['text'] in c['manuscriptText'] for p in o['paragraphs']))
    check(k+' source requirements/discovery/progression',w['sourceRequirements']==s['workRequirements'] and w['sourceDiscovery']==s['discovery'] and w['sourceSkillProgression']==s['skillProgression'])
    mins=115200 if k=='recipe-623' else Fraction(str(s['workRequirements']['activeWorkHours']))*60
    dwarf=math.ceil(mins*Fraction(3,4))
    check(k+' time and Forge arithmetic',w['activeMinutes']==mins and w['forgeDwarfActiveMinutes']==dwarf and w['includedFirstPhaseMinutes']==min(15,mins) and w['remainingActiveMinutes']==mins-min(15,mins) and w['dwarfRemainingActiveMinutes']==dwarf-min(15,dwarf))
    check(k+' quantity and maximum body reservation',o['standardQuantity']==q and o['maximumOrderedBodyReserve']==3*q//2)
    creature=o['profile'] in ['TI-automaton','TI-drone']
    bands={'Mishap':0,'Failed':0,'Flawed':(0 if creature and q==1 else (q//2 if q>1 else 1)),'Standard':q,'Exceptional':5*q//4,'Masterwork':3*q//2}
    check(k+' all six manufacturing quantities',o['creation']['sixBands']==bands)
    check(k+' all source occurrences retained',len(o['componentOccurrences'])==len(s['components']))
    for j,x in enumerate(s['components']):
        comp['total']+=1;comp['consumed' if x['consumed'] else 'nonconsumed']+=1
        if x['role']=='tool':comp['consumedTools' if x['consumed'] else 'retainedTools']+=1
        if x['role']=='catalyst':comp['catalysts']+=1
        occ=o['componentOccurrences'][j]
        check(k+f'[{j}] identity/consumption predicates',occ['index']==j and occ['retainedTool']==(x['role']=='tool' and not x['consumed']) and occ['consumedTool']==(x['role']=='tool' and x['consumed']) and occ['masterworkCatalystEligible']==(x['role']=='catalyst' and x['consumed']))
    for v in o['bodyVariants']:
        bid=v['bodyModelId'];body_memberships[bid].append(k)
        base=D['bodyModels'][bid]['sourceAuthoringProfile'];value=Fraction(str(base['priceGp']));hp=o['useBinding']['hitPoints'] if creature else base['HP']
        check(k+' '+bid+' reference and repair',f(v['mundaneBodyReferenceGp'])==value and f(v['functionalRepair']['materialReferenceGp'])==value/4 and f(v['brokenReconstruction']['materialReferenceGp'])==(Fraction(str(s['economy']['recommendedMarketValue']))/q+value)/4 and f(v['functionalRepair']['defaultMaxHPHours'])==max(Fraction(1),Fraction(hp,10)) and f(v['brokenReconstruction']['defaultMaxHPHours'])==max(Fraction(8),Fraction(hp,10)))
    u=o['useBinding']
    if o['profile']=='TI-automaton':
        n=s['mechanics']['charges'];atk=u['attack']
        check(k+' complete added attack lookup',atk['bonus']==2+n and atk['dice']==f'{n}d6' and atk['reachFeet']==5 and atk['abilityDamage']==0 and atk['damageType'] in s['effects'].lower() and u['hitPoints']==s['mechanics']['hitPoints'] and u['armorClass']==s['mechanics']['armorClass'])
    if c['visibility']=='public':
        pc=public[k];check(k+' source binding public parity',pc['publicBookBinding']==c['publicBookBinding'])
        check(k+' public complete manuscript',pc['manuscriptText'] in man_p[s['skill']] and all(p['text'] in pc['manuscriptText'] for p in pc['operational']['paragraphs']))
        for par in c['publicBookBinding']['paragraphs']: check(k+' book paragraph '+str(par['index']),paras[par['index']]==par['text'])
        for field in ['profile','useBinding','bodyModelIds','standardQuantity','maximumOrderedBodyReserve','work','creation','references','creatureOutput','sourceStandardBatchReferenceGp','sourceProcessUnitReferenceGp','bodyVariants']:
            check(k+' public active '+field,pc['operational'][field]==o[field])
    for par in o['paragraphs']:
        if par['label']=='Effect and operation': effect_groups.setdefault(sha_bytes(par['text'].encode()),[]).append(k)
    coverage.append({'recipeId':k,'profile':o['profile'],'visibility':c['visibility'],'completeObjectSha256':canonical(c),'manuscriptSha256':sha_bytes(c['manuscriptText'].encode()),'paragraphCount':len(o['paragraphs']),'bodyModels':o['bodyModelIds']})
check('758/90/668/6/172 occurrence totals',comp=={'total':758,'nonconsumed':90,'consumed':668,'retainedTools':90,'consumedTools':6,'catalysts':172})

# Independent fail-closed reconstruction from visible source material records.
ledger=load(A/'ADVANCED_CRAFT_PUBLIC_PROJECTION_LEDGER.json');lc={(x['recipeId'],x['componentIndex']):x for x in ledger['entries'] if 'componentIndex' in x}
mentions=provided=withheld=0
for k,c in public.items():
    for j,x in enumerate(c['sourceRecipe']['components']):
        src=internal[k]['sourceRecipe']['components'][j];mentions+=1
        expected_mention={key:src[key] for key in ['name','quantity','role','consumed']}
        matches=[(i,m) for i,m in enumerate(S['materials']) if m['name'].casefold()==src['name'].casefold() and all(m.get(key)==src.get(key) for key in ['tier','value','weight'])]
        if len(matches)==1 and matches[0][1].get('visibility')=='public':
            idx,m=matches[0];expected_mention['publicMaterialProfile']={key:m[key] for key in ['name','tier','rarity','category','value','weight','properties'] if key in m};provided+=1
            check(k+f'[{j}] independent public authority',lc[(k,j)]['supplementalAuthority']['materialIndex']==idx)
        else:withheld+=1
        check(k+f'[{j}] complete projected occurrence',x==expected_mention and c['operational']['componentOccurrences'][j]['componentMention']==x)
check('343 mentions/100 authorized/243 withheld', (mentions,provided,withheld)==(343,100,243))
classcards=D['tinkerInterfaceRegister']['cards']; cls=load(B/'data/public/class_playtests/tinker.json')
# Locate cards in the actual class envelope without assuming its grouping shape.
def all_cards(node):
    if isinstance(node,dict):
        if 'id' in node and 'effect' in node: yield node
        for v in node.values():yield from all_cards(v)
    elif isinstance(node,list):
        for v in node:yield from all_cards(v)
clidx={x['id']:x for x in all_cards(cls)}
check('48 exact preserved class-interface cards',len(classcards)==48 and all(c['sourceCard']==clidx[c['id']] for c in classcards))
cases=load(A/'ADVANCED_CRAFT_AUTHORED_SEQUENCE_CASES.json')
check('all37 actual qualitative sequences',len(cases['cases'])==37 and {c['id'] for c in cases['cases']}=={f'W-{n:02}' for n in range(1,20)}|{f'E-{n:02}' for n in range(1,19)})

# Detect submitted textual conflicts. These are findings, NOT passing runtime tests.
def text(c,label):return next(p['text'] for p in c['operational']['paragraphs'] if p['label']==label)
g=P['operatingGuideText']
findings=[
 {'id':'AEX-01','present':all('25% of genuinely remaining consumed' in text(c,'Retention and failure') for c in D['cards']),'kind':'failure entitlement basis differs from AC-04 cap wording'},
 {'id':'AEX-02','present':('genuinely relevant INT tool check' in g and 'moving/suppressing the original plate ends' in g),'kind':'public Rune control credentials/endpoints/disarming incompletely projected'},
 {'id':'AEX-03','present':'Spend one when a genuine encounter starts' in g,'kind':'public automaton initial service debit lacks actual operation'},
 {'id':'AEX-04','present':'stops applicable movement, attacks and device aura functions' in g,'kind':'public routed disable omits triggers and other active uses'},
 {'id':'AEX-05','present':'4x4x2 inches or 2 lb' in P['bodyModels']['TI-device']['model'],'kind':'disjunctive model field conflicts with conjunctive geometry/load limits'},
 {'id':'AEX-06','present':all(c['operational']['useBinding']['trigger']=='attuned bearer is targeted' for c in D['cards'] if c['operational']['profile']=='RC-warding'),'kind':'ward trigger field omits saving-throw events including areas'},
 {'id':'AEX-07','present':any('consultation under SC-04' in text(c,'Effect and operation') for c in D['cards'] if c['operational']['profile']=='SC-script'),'kind':'wrong/missing operational section locators'}
]
report={'scope':'Read-only independent frozen-source, complete-object/manuscript, arithmetic and public-envelope checks; semantic findings separate; no advanced runtime or campaign authentication.',
 'archiveSha256':sha(ARCHIVE),'sourceVerdictSha256':sha(A/'GPT_ADVANCED_167_SOURCE_AUTHORING_VERDICT.md'),
 'internalCandidateSha256':sha(B/'data/director/advanced_craft_recipe_candidate_internal.json'),'publicCandidateSha256':sha(B/'data/crafting/advanced_craft_recipe_candidate_public.json'),
 'checkCount':len(checks),'failedChecks':[x for x in checks if not x['pass']], 'checks':checks,
 'counts':{'recipes':167,'publicRecipes':100,'bodyVariants':22,'publicBodyVariants':15,'hostTemplates':50,'occurrences':dict(comp),'publicComponentMentions':mentions,'publicSupplementalProfiles':provided,'withheldSupplementalProfiles':withheld,'qualitativeSequences':37,'classInterfaceDispositions':48},
 'completeCardCoverage':coverage,'bodyMemberships':body_memberships,'profiles':dict(profiles),'effectTextGroups':effect_groups,'submittedSemanticFindings':findings,
 'runtimeImplementedOrTested':False,'worldFactsAuthenticated':False,'sourcesModifiedByThisAudit':False,'approvalsMadeByScript':0}
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'failed':report['failedChecks'],'findings':findings,'counts':report['counts']},ensure_ascii=False,indent=2))
