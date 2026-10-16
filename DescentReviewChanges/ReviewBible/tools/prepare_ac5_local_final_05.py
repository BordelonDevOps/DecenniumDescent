"""Make concrete, reversible local geometry corrections for exact GPT review."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import hashlib,json,math,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at

def read(p):return json.loads(p.read_bytes())

def main():
    oldroot=A/'ac5-repair-04-return'; root=A/'ac5-local-final-05-candidate'; packet=A/'ac5-local-final-05-input'
    archive=A/'DD_AC5_Local_Final_05.zip'; report=A/'AC5_LOCAL_FINAL_05_CORRECTIONS.json';request=A/'AC5_LOCAL_FINAL_05_REQUEST.txt'
    assert not any(p.exists() for p in [root,packet,archive,report,request])
    model=read(oldroot/'SPELLS_MODEL.json');reg=read(oldroot/'REGISTER.json');cb=read(oldroot/'CASEBOOK.json')
    originalmodel=deepcopy(model); originalcases=deepcopy(cb)
    byid={x['id']:x for x in cb['cases']}
    old25=deepcopy(byid['AC5-X25']);old12=deepcopy(byid['AC5-X12']);old27=deepcopy(byid['AC5-X27'])
    changes=[]
    def change_case(ident,fields):
        c=byid[ident];before=deepcopy(c)
        for k,v in fields.items():c[k]=v
        c['local05PreviousCurrentVersion']=before
        changes.append({'file':'CASEBOOK.json','pointer':'/cases/'+str(cb['cases'].index(c)),'old':before,'replacement':deepcopy(c)})
    change_case('AC5-X25',{
      'currentInitialState':'Two independent fixtures, not simultaneous overlays. A: only F1 is active, center(0,0),radius10, establishedt0/deadline60. W1 Wizard9 INT4/PB4/DC16 stands(20,0),RP30,Dissonance0, ordinary body footprint5x5. A is Medium centered(15,0),footprint x[12.5,17.5],y[-2.5,2.5],HP40/40,no tempHP/defense; B is Medium centered(7.5,0),footprint x[5,10],y[-2.5,2.5],HP20/20, with a live rank5 Spell Resistance whose deadline is3590. W2 Wizard9 at(20,10),RP30,Dissonance0, can perceive/address the field and the eligible effect set. No other relevant ongoing applications are present. B: independent scene has F1 center(0,0),deadline60 and F2 center(8,0),deadline66, both radius10 and separate owners; B at(7.5,0) has its own Spell Resistance. W2 at(20,20),RP30, is outside both fields. All relevant center/near-face lines of effect are clear.',
      'actionsAndResolution':[
       'Fixture A t6: W1 casts actual Burning Hands west,15ft cone,Action/V/S/F,2RP. RP30->28; ranked Dissonance0->1 with no repeated-name extra. A and B are both legally in the cone and failDEX againstDC16. Shared3d6=10. A is wholly outside the sole field F1 and takes10fire: HP40->30,no Wound threshold. B intersects F1 and its local instantaneous manifestation is suppressed: HP20 unchanged,no damage packet/root. F2 does not exist in this fixture.',
       'Fixture A t12: on W1\'s next real available Action, Dimensional Door costs7RP,RP28->21,Dissonance1->2,another named cast so no repeated-name extra. Destination insideF1 makes the paid relocation fail atomically at the original outside body position; no delayed release.',
       'Fixture A t18: W2 casts Greater Dispel for10RP,RP30->20,Dissonance0->1,center(0,0) within30ft,area radius30. Immutable capture includes F1 and B\'s Spell Resistance. Snapshot each termination operation before removal: F1\'s operation ignores only F1\'s own suppression and is otherwise legal, so rank5 automatic termination succeeds; Spell Resistance\'s operation is suppressed byF1 at the snapshot and stays suppressed for this cast. F1 ends, B\'s retained Spell Resistance resumes with its original deadline3590, and no rescan retroactively removes it.',
       'Fixture B t12: W2 separately casts Greater Dispel for10RP,RP30->20,center(4,0),distance sqrt656 fromW2 (<30),radius30. Both field anchors and B\'s existing buff are captured before removal. F1 and F2 centers are8ft apart: F2 covers F1\'s anchor and F1 covers F2\'s anchor. Their same-family exemption keeps the two fields themselves operative.',
       'Fixture B operation snapshot: F1 termination ignores F1 only and is suppressed byF2; F2 termination ignores F2 only and is suppressed byF1; B\'s buff termination is also suppressed. No captured termination executes. F1/F2/buff retain their own clocks and no second scan, oscillation or cost refund occurs. This branch supplies the genuine different-field counterexample without altering Fixture A.'
      ],
      'costLedger':{'fixtureA_W1_start':30,'burningHands':2,'W1_afterBurningHands':28,'dimensionalDoor':7,'W1_end':21,'fixtureA_W2_start':30,'greaterDispel':10,'fixtureA_W2_end':20,'fixtureB_W2_start':30,'fixtureB_greaterDispel':10,'fixtureB_W2_end':20},
      'clockLedger':{'fixtureA_F1_established':0,'fixtureA_burningHands':6,'fixtureA_door':12,'fixtureA_F1_endedByDispel':18,'fixtureA_buffOriginalDeadline':3590,'fixtureB_dispel':12,'fixtureB_F1_deadline':60,'fixtureB_F2_deadline':66,'noClockRestart':True},
      'geometryLedger':{'fixtureA':{'F1':{'center':[0,0],'radius':10},'noF2':True,'W1':[20,0],'A':[15,0],'B':[7.5,0],'W2':[20,10],'cone':'15ft west-facing'},'fixtureB':{'F1':[0,0],'F2':[8,0],'radii':[10,10],'anchorSeparation':8,'W2':[20,20],'dispelCenter':[4,0],'dispelRadius':30}},
      'currentAdjudication':'Legal actual cone and whole-body eligibility are shown separately from a two-field dispel fixture. A single field can be terminated while another captured buff survives its snapshotted suppression; two genuinely mutually covering fields suppress each other\'s termination operations without becoming immune to independent source-ending rules.'})
    change_case('AC5-X12',{
      'currentInitialState':'Wall plane x=0 with1inch thickness,y[-10,10],z[0,10],fixed2.5ft panel grid anchoredy=-10,z=0. Fromt12 an actual radius10 Lesser Antimagic sphere centered(-1,0,5) overlaps the wall; its caster can place this center legally within10ft and has clear line of effect to the wall\'s affected near face. Use the actual sphere intersection, not a rectangular six-panel Antimagic volume. The sphere wholly covers the six central panels y[-2.5,2.5],z[0,7.5] and also suppresses other wall portions. All other affected portions remain unoccupied. A standing Medium body x[-2.5,2.5],y[-2.5,2.5],z[0,6] lawfully enters the opening and intersects those six central panel volumes att18.',
      'actionsAndResolution':[
       'At12, record each actual suppressed portion as its fixed1inch panel volume intersected with sphere (x+1)^2+y^2+(z-5)^2<=100 and operative centerLoE. Portions outside that actual intersection remain solid. Do not assert that only six panels were suppressed.',
       'The six central2.5x2.5 panels are wholly inside the sphere: even their farthest relevant corner has squared distance less than33. This gives at least a5ft-wide,7.5ft-high legal opening for the stated6ft-tall body. The creature enters before suppression ends.',
       'At18 the suppressor ends. Each stored portion not occupied resumes normally. The six complete central portions intersect the body and remain wholly absent under AC5-WALL-PANELS-04. No new body-shaped cutout or additional deactivation occurs. Exactly six pending whole panels remain; they were not the only portions originally suppressed.',
       'At24 the creature has moved to a whole footprint x[2.5,7.5], clear of the1inch wall. The six stored pending portions resume at their original coordinates. No push,cut,crush,free squeeze or new source clock is supplied.'
      ],
      'geometryLedger':{'wallPlane':'x=0','wallThicknessFt':1/12,'panelSizeFt':2.5,'sphereCenter':[-1,0,5],'sphereRadiusFt':10,'sphereIntersection':'(x+1)^2+y^2+(z-5)^2<=100 with actual operative LoE','pendingCentralY':[-2.5,2.5],'pendingCentralZ':[0,7.5],'pendingWholePanelCount':6,'bodyHeightFt':6,'centralClearanceHeightFt':7.5,'otherSuppressedPortions':'actual sphere intersections, clear and resumed at18'},
      'currentAdjudication':'A real spherical suppressor provides the legal opening. Six occupied central panels remain pending when the larger actual suppressed area resumes; exact previous geometry is retained.'})
    # Express the accepted additive movement accounting without a vague multiplier.
    oldrule=model['sharedRules']['AC5-PORTAL-GEOMETRY-04']['rule'][3]
    newrule=oldrule.replace('Apply real difficult-terrain/crawling/squeezing multipliers.', 'Use the accepted additive per-foot cost: terrain rate1 normal,2 difficult or3 severe (strongest terrain only), then add1 for crawling and1 for squeezing. A5ft traversal therefore costs5 times that sum; difficult+squeeze costs15ft, not20ft.')
    assert newrule!=oldrule
    model['sharedRules']['AC5-PORTAL-GEOMETRY-04']['rule'][3]=newrule
    changes.append({'file':'SPELLS_MODEL.json','pointer':'/sharedRules/AC5-PORTAL-GEOMETRY-04/rule/3','old':oldrule,'replacement':newrule})
    fields={k:deepcopy(old27[k]) for k in ['actionsAndResolution','geometryLedger']}
    fields['actionsAndResolution'].insert(3,'In an independent difficult-terrain version of that same voluntary squeezed5ft crossing, cost is5*(2 terrain+1 squeeze)=15ft. With additional crawling it is5*(2+1+1)=20ft. These are accepted per-foot additions, not multiplying difficult2 by squeeze2. No extra terrain cost is imposed on a forced displacement unless its own source says so.')
    fields['geometryLedger']['largeDifficultSqueezeCostFt']=15;fields['geometryLedger']['largeDifficultCrawlSqueezeCostFt']=20
    change_case('AC5-X27',fields)
    corrections=[
      {'id':'AC5-L05-01','status':'Proposed exact local correction, awaiting GPT acceptance','finding':'Repair04 X25 erroneously places A and W1 inside its added F2, then calls A outside all Antimagic. It also says a radius10 field centered15 covers point0 despite distance15.','correction':'Use independent single-field incoming/self-dispel fixture and a separate mutually covering pair with8ft anchor separation. All coordinates, costs, clocks and termination outcomes are explicit in revised X25.'},
      {'id':'AC5-L05-02','status':'Proposed exact local correction, awaiting GPT acceptance','finding':'Repair04 X12 calls an actual sphere an exactly rectangular six-panel suppressed region. No actual sphere geometry is provided.','correction':'Use radius10 center(-1,0,5), retain actual sphere/panel intersections, and distinguish the six occupied pending full panels from the additional clear suppressed portions that resume.'},
      {'id':'AC5-L05-03','status':'Accepted-source precision, awaiting GPT confirmation of these exact files','finding':'Portal shared rule says movement multipliers even though COMBAT_ACTION_PLAYTEST specifies terrain rate plus crawl/squeeze additions.','correction':'Write exact additive formula and show difficult+squeeze15ft/crawl+difficult+squeeze20ft for a5ft crossing in X27.'}]
    model['local05Corrections']=deepcopy(corrections)
    model['priorDispositionAuthority']='Repair03/04 dispositions remain preserved as historical GPT responses. Local05 corrections supersede their erroneous scene-geometry descriptions only; they are not new GPT acceptance statements.'
    reg['local05Corrections']=deepcopy(corrections);reg['reviewStatus']='Local exact candidate derived from Repair04; awaiting actual GPT exact-file acceptance. No adoption.'
    reg['priorDispositionAuthority']=model['priorDispositionAuthority']
    root.mkdir()
    for name,obj in [('SPELLS_MODEL.json',model),('REGISTER.json',reg),('CASEBOOK.json',cb)]: (root/name).write_bytes(encoded(obj))
    (root/'SOURCE_HASHES.json').write_bytes((oldroot/'SOURCE_HASHES.json').read_bytes())
    note='## Local05 corrections awaiting exact GPT acceptance\n\nThe preceding returned Repair04 material is preserved in the audit archive. The current files correct three precisely identified issues below. Prior GPT disposition text is retained as historical evidence and does not constitute acceptance of these local edits. The original sixteen procedures, seventeen placements and source/access objects remain exact; only the shared portal cost wording is clarified against the accepted additive movement rule. Full current case data and previous versions remain in CASEBOOK.json.\n\n'+'\n\n'.join('**'+x['id']+'** '+x['finding']+' '+x['correction'] for x in corrections)+'\n\n'
    for name in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:
        text=(oldroot/name).read_text(encoding='utf8');assert oldrule in text
        text=text.replace(oldrule,newrule)
        pos=text.index('\n\n')+2;text=text[:pos]+note+text[pos:]
        if name=='DIRECTOR_REVIEW.md':
            text+='\n\n## Exact current Local05 case replacements\n\n'
            for ident in ['AC5-X12','AC5-X25','AC5-X27']:
                cur={k:byid[ident][k] for k in ['id','title','currentInitialState','actionsAndResolution','costLedger','clockLedger','geometryLedger','currentAdjudication']}
                text+='### '+ident+'\n\n```json\n'+json.dumps(cur,ensure_ascii=False,indent=2)+'\n```\n\n'
        (root/name).write_text(text,encoding='utf8',newline='\n')
    (root/'VERDICT.md').write_text('# Local05 exact candidate — acceptance pending\n\nThis is Codex\'s concrete correction candidate derived from the exact Repair04 return. It is not a GPT acceptance receipt. Three local corrections are listed in REGISTER.json and SPELLS_MODEL.json. All92 frozen sources,16 source/access objects,17 placements,61 current case IDs and22 original historical case texts are preserved. All prior versions remain in their original archives and marked case history. No new spell adoption, runtime execution, human playtest, balance, cosmology canon, whole-game or publication approval is claimed.\n',encoding='utf8')
    checks=[]
    def ck(label,ok,**kw):checks.append({'check':label,'pass':bool(ok),**kw});assert ok,(label,kw)
    ck('Same16 full source/access records',[(x['id'],x['completeSourceAndAccess']) for x in model['spells']]==[(x['id'],x['completeSourceAndAccess']) for x in originalmodel['spells']])
    ck('Same16 procedure strings', [x['procedure'] for x in model['spells']]==[x['procedure'] for x in originalmodel['spells']])
    ck('Same61 case IDs and22 original texts',len(cb['cases'])==61 and [(x['id'],x.get('historicalOriginalText')) for x in cb['cases']]==[(x['id'],x.get('historicalOriginalText')) for x in originalcases['cases']])
    for s in model['spells']:
        for fn in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:ck('Complete procedure in chapter',s['procedure'] in (root/fn).read_text(encoding='utf8'),spellId=s['id'],chapter=fn)
    ck('Single-field caster and outside target clear',20-2.5>10 and 15-2.5>10)
    ck('Inside recipient and cone legal',7.5<10 and 20-7.5<15 and 20-15<15)
    ck('Second scene mutual suppression symmetric',8<10)
    ck('Second scene caster outside both fields',math.dist((20,20),(0,0))>10 and math.dist((20,20),(8,0))>10)
    ck('Second scene GreaterDispel center within30',math.dist((20,20),(4,0))<30)
    corners=[(x,y,z) for x in [-1/24,1/24] for y in [-2.5,2.5] for z in [0,7.5]]
    ck('Six central full panel volumes inside sphere',max((x+1)**2+y*y+(z-5)**2 for x,y,z in corners)<33)
    ck('Six actual occupied central panels',sum(1 for y in [-2.5,0] for z in [0,2.5,5] if y<2.5 and y+2.5>-2.5 and z<6 and z+2.5>0)==6)
    ck('Additive movement arithmetic',5*(2+1)==15 and 5*(2+1+1)==20)
    current_refs=[];descriptive=[]
    def walk(v,loc):
        if isinstance(v,dict):
            if isinstance(v.get('path'),str) and 'pointer' in v:current_refs.append((loc,v))
            for k,x in v.items():
                if k not in ['previousCurrentVersion','historicalProposalEvidence','historicalPriorCurrentVersion','local05PreviousCurrentVersion']:walk(x,loc+'/'+k)
        elif isinstance(v,list):
            for i,x in enumerate(v):walk(x,loc+'/'+str(i))
    for name,obj in [('SPELLS_MODEL.json',model),('REGISTER.json',reg),('CASEBOOK.json',cb)]:walk(obj,name)
    sourceRoot=A/'ac5-repair-04-input/sources'
    for loc,ref in current_refs:
        p=root/ref['path'] if (root/ref['path']).is_file() else sourceRoot/ref['path']
        ck('Reference file exists',p.is_file(),location=loc,path=ref['path'])
        if str(ref['pointer']).startswith('/'):ck('Current JSON pointer resolves',at(read(p),ref['pointer']) is not None,location=loc,path=ref['path'],pointer=ref['pointer'])
        else:descriptive.append({'location':loc,**ref})
    bindings=read(root/'SOURCE_HASHES.json')['bindings'];ck('Same92 source bindings',len(bindings)==92)
    for b in bindings:ck('Frozen and current source exact',info(G/b['path'])==b and (sourceRoot/b['path']).read_bytes()==(G/b['path']).read_bytes(),path=b['path'])
    names=['REGISTER.json','SPELLS_MODEL.json','PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md','CASEBOOK.json','SOURCE_HASHES.json','VERDICT.md']
    manifest={'schemaVersion':1,'id':'AC5-LOCAL-FINAL-05-MANIFEST','status':'Exact proposed files, pending GPT acceptance','files':[{'name':n,'bytes':(root/n).stat().st_size,'sha256':hashlib.sha256((root/n).read_bytes()).hexdigest()} for n in names],'currentReferenceObjects':len(current_refs),'descriptiveReferences':len(descriptive),'sourceBindings':92,'spellIdentities':16,'placements':17,'caseCount':61,'historicalOriginalTexts':22,'localCheckCount':len(checks),'localFailures':0,'runtimeTestsExecuted':False,'humanPlaytested':False}
    (root/'EVIDENCE_MANIFEST.json').write_bytes(encoded(manifest))
    review={'id':'AC5-LOCAL-FINAL-05-CORRECTIONS','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Concrete local corrections; source-preserved and independently checked; actual GPT acceptance required.','priorReturn':info(A/'DD_AC5_Repair_04_Return.zip'),'priorStructuralCheck':info(A/'AC5_REPAIR_RETURN_04_STRUCTURAL_CHECK.json'),'corrections':corrections,'operations':changes,'checks':checks,'checkCount':len(checks),'failureCount':0,'files':[info(root/n) for n in names+['EVIDENCE_MANIFEST.json']],'newSpellAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
    report.write_bytes(encoded(review));packet.mkdir()
    for b in bindings:
        p=packet/'sources'/b['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((sourceRoot/b['path']).read_bytes())
    (packet/'candidate').mkdir()
    for n in names+['EVIDENCE_MANIFEST.json']:(packet/'candidate'/n).write_bytes((root/n).read_bytes())
    (packet/'CORRECTIONS.json').write_bytes(report.read_bytes());(packet/'SOURCE_MANIFEST.json').write_bytes((A/'ac5-repair-04-input/SOURCE_MANIFEST.json').read_bytes())
    (packet/'PREVIOUS_RETURN.zip').write_bytes((A/'DD_AC5_Repair_04_Return.zip').read_bytes())
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(packet.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(packet).as_posix())
    prompt=f'''Please review the exact local final candidate in attached DD_AC5_Local_Final_05.zip ({archive.stat().st_size} bytes,SHA256{info(archive)['sha256']}) for source-consistent authored-playtest acceptance of the16 AC5 spells. Your complete Repair04 return is preserved exactly; independent structural verification passed858 checks. I made three concrete local corrections, with reversible before/after operations and checks in CORRECTIONS.json. All92 complete frozen sources, the full previous return and the eight exact candidate files are included. No scripts need execution.

L05-01: Repair04 X25 introduced F2 center(15,0),radius10 while calling A at(15,0) outside all fields; W1 at(20,0) is also inside F2. It also claimed F2 covers F1 anchor0 despite15ft separation. Candidate X25 separates a legal single-field BurningHands/self-dispel fixture from an independent mutually covering two-field fixture with centers0 and8. Costs, clocks, all operation-snapshot outcomes and actual body/cone geometry are explicit.
L05-02: Repair04 X12 asserted a spherical Antimagic volume suppresses exactly a rectangular six-panel region. Candidate uses an actual radius10 sphere at(-1,0,5), preserves its real intersections, and distinguishes the six occupied central panels that remain pending from other suppressed portions that resume.
L05-03: Portal costs now explicitly use accepted terrain rate plus crawl/squeeze additions, with5ft difficult+squeeze=15ft and crawl+difficult+squeeze=20ft. Original16 procedure strings and all source/access records remain exact; only this shared-rule precision and the three case corrections/new local notes differ. Prior GPT dispositions remain clearly historical, not forged acceptance of these edits.

Inspect the exact candidate files and sources critically. Confirm or reject each L05 correction with evidence. If no substantive contradiction remains, return DD_AC5_Exact_Acceptance_05.zip containing ACCEPTANCE.json and VERDICT.md. ACCEPTANCE.json must identify all eight candidate filenames, exact byte lengths and SHA256s from your own verification, all92 source verification results,16 spell IDs/17 placements/61 case IDs/22 historical texts, and explicit bounded verdict ACCEPT_FOR_AUTHORED_CAMPAIGN_PLAYTEST_INTEGRATION with zero unresolved blocking findings. Do not silently regenerate the candidate: acceptance must name these exact bytes. If you disagree or find a concrete blocker, return a precise source-linked finding and proposed correction instead of acceptance. This is not runtime, human-playtest, balance, cosmology-canon, whole-game or publication approval. We will apply only after both of us agree. Then the complete14-identity AC6 draft can be refreshed against the accepted AC5 interfaces.'''
    request.write_text(prompt,encoding='utf8',newline='\n')
    prep={'id':'AC5-LOCAL-FINAL-05-PREPARATION','archive':info(archive),'request':info(request),'corrections':info(report),'checkCount':len(checks),'failureCount':0,'candidateManifest':info(root/'EVIDENCE_MANIFEST.json'),'sourceCount':92,'spellIdentities':16,'caseCount':61,'status':'Prepared for exact acceptance; not yet submitted or adopted.'}
    (A/'AC5_LOCAL_FINAL_05_PREPARATION.json').write_bytes(encoded(prep));print(json.dumps(prep))

if __name__=='__main__':main()
