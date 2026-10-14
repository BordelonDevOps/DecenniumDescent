"""Apply the three authorized TEX-ADD operations and append immutable provenance."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
from urllib.parse import unquote
import copy,json,re,shutil
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
D=A/'teaching-tex-controlling-addendum-files';B=A/'teaching-before-tex-controlling-addendum'
def load(p):return json.loads(p.read_text('utf-8-sig'))
def h(p):return sha256(p.read_bytes()).hexdigest()
def rec(p):return {'path':p.relative_to(G).as_posix(),'bytes':p.stat().st_size,'sha256':h(p)}
def save(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def enc(b,t):return (b'\xef\xbb\xbf' if b.startswith(b'\xef\xbb\xbf') else b'')+(t.replace('\n','\r\n') if b'\r\n' in b else t).encode('utf-8')
assert not B.exists(), 'One-use application already started'
spec=load(D/'TEX_ADD_EXACT_OPERATIONS.json');prior=load(A/'TEACHING_TEX_EXACT_FULFILLMENT.json')
assert h(A/'TEACHING_TEX_EXACT_FULFILLMENT.json')=='a3e447ce732c86818ca46468505ef8eb4fbea41a7b04340c4e5708576d9840d6'
for rel,v in {**prior['finalArtifacts'],**prior['correctedCurrentCraftArtifacts']}.items():assert h(G/rel)==v['sha256'],rel
ops=spec['operations'];assert len(ops)==3
targets={op['path'] for op in ops};sp=G/spec['statusAppend']['path'];tp=R/'docs/playtest/TEACHING_REVIEW_STATUS.json'
tracked=set(load(A/'TEACHING_TEX_LOCAL_PREPARATION.json')['liveDiskPayloadsUnchanged'])|targets|{tp.relative_to(G).as_posix()}
before={p:rec(G/p) for p in tracked}
originals={}
for rel in targets|{sp.relative_to(G).as_posix(),tp.relative_to(G).as_posix()}:
    p=G/rel;q=B/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);originals[rel]=rec(p)
newguide=A/'TEX_CONTROLLING_ADDENDUM_2026_10_11.md';assert not newguide.exists();shutil.copy2(D/newguide.name,newguide)
assert h(newguide)==spec['provenanceAppend']['value']['addendumSha256']
expected={}
for op in ops:
    p=G/op['path'];b=p.read_bytes()
    if op['op']=='replace_text':
        old=p.read_text('utf-8-sig');assert old.count(op['old'])==1
        new=old.replace(op['old'],op['replacement'],1);expected[op['path']]=new;p.write_bytes(enc(b,new))
        assert enc(b,new.replace(op['replacement'],op['old'],1))==b
    else:
        old=load(p);new=copy.deepcopy(old);assert new['procedureSections']['TD-13']['text']==op['old'];new['procedureSections']['TD-13']['text']=op['replacement'];expected[op['path']]=new
        app=spec['provenanceAppend'];arr=new.get('controllingCorrections',[]);assert isinstance(arr,list)
        assert not any(isinstance(x,dict) and x.get('id')==app['value']['id'] for x in arr)
        new.setdefault('controllingCorrections',[]).append(copy.deepcopy(app['value']))
        p.write_bytes(enc(b,json.dumps(new,ensure_ascii=False,indent=2)+'\n'))
checks=[]
def ck(name,condition):
    checks.append({'name':name,'passed':bool(condition)});assert condition,name
for rel,value in expected.items():ck('Exact complete amended object/text '+rel,(load(G/rel) if rel.endswith('.json') else (G/rel).read_text('utf-8-sig'))==value)
ip=G/ops[1]['path'];internal=load(ip);oldinternal=load(B/ops[1]['path']);ig=(G/ops[0]['path']).read_text('utf-8-sig')
paragraph=re.search(r'^## TD-13[^\n]*\n\n(.*?)(?=\n\n## )',ig,re.M|re.S).group(1)
ck('Whole current internal TD-13 paragraph equals JSON',paragraph==internal['procedureSections']['TD-13']['text'])
for key in ['cards','bodyModels','enchantingHostModels','tinkerInterfaceRegister','sourceVerdictSha256']:
    ck('Preserved complete internal '+key,internal[key]==oldinternal[key])
ck('Retained exact cb2 Tinker disposition',internal['tinkerInterfaceRegister']['cards'][31]['authoringDisposition']==spec['preservation']['cb2CurrentTinkerDisposition'])
undo=copy.deepcopy(internal);ck('Exact provenance append',undo['controllingCorrections'].pop()==spec['provenanceAppend']['value']);undo['procedureSections']['TD-13']['text']=ops[1]['old']
if 'controllingCorrections' not in oldinternal:del undo['controllingCorrections']
ck('Undo two permitted JSON changes restores whole old object',undo==oldinternal)
pub=load(R/'data/crafting/advanced_craft_recipe_candidate_public.json');ck('Unchanged complete public guide parity',pub['operatingGuideText']==(R/'docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md').read_text('utf-8-sig'))
cross=load(D/'TEX_ADD_ACCEPTANCE_CROSSWALK.json');ck('Sixteen TB cases retained exactly',cross['retainedCases']==load(A/'teaching-nine-exact-reviewer-files/TEX_FINITE_ACCEPTANCE_CASES.json')['cases']);ck('All twenty alternate cases mapped',len(cross['alternateCrosswalk'])==20)
timing=R/'docs/mechanics/CLASS_PLAYTEST_RULES.md';text=timing.read_text('utf-8-sig');source=next(x for x in text.splitlines() if x.startswith('Recharge N sets a counter'))
assessments=[
 {'id':'TA-01','adjudication':'Recharge2 after use on regular turn1 remains2 at its end, after an extra Action and throughout an extra turn. Starts2/3 produce1/0. Readiness grants no activation.','trace':[{'event':'use on regular1','counter':2},{'event':'regular1 end','counter':2},{'event':'extra Action','counter':2},{'event':'extra turn','counter':2},{'event':'regular2 start','counter':1},{'event':'regular3 start','counter':0}],'sourcePhrases':['Extra turns/Actions do not tick it.','Recharge 2 used on turn 1 is ready on turn 3.'],'runtimeExecuted':False},
 {'id':'TA-02','adjudication':'An unable-to-act owner still ticks at the real regular start. That counted boundary is retained on mode transition; switching to elapsed tracking does not repeat it. A later distinct six-second boundary can tick under the existing rule.','sourcePhrases':['whether able to act or not.','Outside combat tick once per 6 elapsed seconds, without double counting.'],'runtimeExecuted':False},
 {'id':'TA-03','adjudication':'Each native start/end/elapsed deadline remains unchanged. Zero counter rejects reset without spending a reset use. An acquired legal reset/shortening of a positive named counter spends its single numbered-round opportunity; a second one that round is unavailable. It adds neither RP/per-rest stock nor activation.','sourcePhrases':['A positive counter can be reset/shortened at most once per ability per round.','Zero counters are not legal reset targets and expend no reset use.','Resets never restore RP or per-rest uses or grant an immediate activation.'],'runtimeExecuted':False}]
for case in assessments:
    ck(case['id']+' exact current source supports adjudication',all(x in source for x in case['sourcePhrases']))
for rel,v in before.items():
    if rel not in targets:ck('Unchanged tracked input before status append '+rel,h(G/rel)==v['sha256'])
coverage=load(R/'data/playtest/game_development_coverage.json');ck('Exactly five retained resolved TC issues',sum(x.get('id')=='TC-RECYCLING-01' for a in coverage['aspects'] for x in a.get('resolvedInterfaceIssues',[]))==5)
def anchors(t):return {''.join(c for c in re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',x).lower() if c.isalnum() or c in '_- ').replace(' ','-') for x in re.findall(r'^#{1,6}\s+(.+)$',t,re.M)}
links=[]
for rel in prior['finalArtifacts']:
    if not rel.endswith('.md'):continue
    p=G/rel
    for raw in re.findall(r'\]\(([^)]+)\)',p.read_text('utf-8-sig')):
        if re.match(r'\w+://|mailto:',raw):continue
        file,_,anchor=unquote(raw.strip('<>')).partition('#');dest=(p.parent/file).resolve() if file else p
        ck('Teaching link '+p.name+' '+raw,dest.is_file() and (not anchor or anchor in anchors(dest.read_text('utf-8-sig'))));links.append({'from':rel,'link':raw})
ck('All162 original corrected links retained',len(links)==162)
evidence={'scope':'Exact text/object, byte preservation and link checks; three authored source-based semantic adjudications. No new runtime tests.','checks':checks,'checkCount':len(checks),'failed':[],'semanticAdjudications':assessments,'semanticSource':rec(timing),'completeSourceRechargeParagraph':source,'acceptanceCrosswalk':rec(D/'TEX_ADD_ACCEPTANCE_CROSSWALK.json'),'beforeTrackedFiles':before,'links':links}
save(A/'TEACHING_TEX_ADDENDUM_LOCAL_CHECKS.json',evidence)
receipt={'addendumId':spec['addendumId'],'status':'FULFILLED — three exact current-text replacements and append-only provenance','completedAt':datetime.now(timezone.utc).isoformat(),'requestId':'bcfce0be-6718-4e51-8921-17dea64f9839','replyId':'1220c55b-f3b9-4e3d-abd4-91dbbff9bd4b','addendum':rec(newguide),'package':rec(A/'DD_TEX_Controlling_Addendum_2026_10_11.zip'),'predecessorFulfillment':rec(A/'TEACHING_TEX_EXACT_FULFILLMENT.json'),'operations':ops,'provenanceAppend':spec['provenanceAppend'],'beforeArtifacts':originals,'finalArtifacts':{rel:rec(G/rel) for rel in sorted(targets)},'localEvidence':rec(A/'TEACHING_TEX_ADDENDUM_LOCAL_CHECKS.json'),'checks':len(checks),'failures':0,'semanticCases':3,'retainedCases':16,'runtimeCasesExecuted':0,'originalAexHashMapRetained':True,'coverageChanged':False,'navigationChanged':False,'pdfChanged':False,'labelsChanged':False,'newCardApprovals':0,'newGameplayRules':0,'sourceInformationDeleted':0,'wholeGameApproved':False,'githubPushed':False,'cosmologyReviewed':False}
rp=A/'TEACHING_TEX_ADDENDUM_FULFILLMENT.json';save(rp,receipt)
status=load(sp);oldstatus=copy.deepcopy(status);entry={'id':spec['addendumId'],'addendumFile':newguide.relative_to(G).as_posix(),'addendumSha256':h(newguide),'fulfillmentReceiptFile':rp.relative_to(G).as_posix(),'fulfillmentReceiptSha256':h(rp),'currentArtifactHashes':{rel:h(G/rel) for rel in sorted(targets)}}
assert isinstance(status['subsequentInterfaceErrata'],list);status['subsequentInterfaceErrata'].append(entry);save(sp,status)
undo=copy.deepcopy(status);assert undo['subsequentInterfaceErrata'].pop()==entry and undo==oldstatus
# Retain earlier teaching-status hashes as a version; append the current descendant.
tstatus=load(tp);oldteach=copy.deepcopy(tstatus);tstatus.setdefault('subsequentAddenda',[]).append(entry);save(tp,tstatus)
undo=copy.deepcopy(tstatus);assert undo['subsequentAddenda'].pop()==entry
if 'subsequentAddenda' not in oldteach:del undo['subsequentAddenda']
assert undo==oldteach
save(A/'TEACHING_TEX_ADDENDUM_STATUS_PROOF.json',{'scope':'Downstream append-only status proof; no receipt/status hash cycle','advancedStatus':rec(sp),'teachingStatus':rec(tp),'entry':entry,'earlierAdvancedStatusObjectPreserved':True,'earlierTeachingStatusObjectPreserved':True,'originalAexArtifactHashMapUnchanged':status['artifactHashes']==oldstatus['artifactHashes']})
print(json.dumps({'exactOperations':3,'checks':len(checks),'failed':0,'semanticCases':3,'links':len(links),'pdfNavigationCoverageUnchanged':True,'receipt':rec(rp)}))
