"""Preserve a focused semantic audit and a small unadopted successor proposal."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as ET
import hashlib, json, re, shutil
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())
def sha(b): return hashlib.sha256(b).hexdigest()
def get(d, pointer):
    for segment in pointer.strip('/').split('/') if pointer else []:
        segment=segment.replace('~1','/').replace('~0','~')
        d=d[int(segment)] if isinstance(d,list) else d[segment]
    return d
def files(root):
    return [{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(root.rglob('*')) if p.is_file() and p!=root/'MANIFEST.json']

def main():
    now=datetime.now(timezone.utc).isoformat()
    local=A/'cosmology-epilogue-campaign-arcs-local-draft-01'
    oldpacket=A/'cosmology-epilogue-campaign-arcs-01'
    history=local/'history/before-semantic-review-03'
    report=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_SEMANTIC_REVIEW_03.json'
    validation=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_LOCAL_DRAFT_01_VALIDATION_03.json'
    packet=A/'cosmology-epilogue-campaign-arcs-02'
    archive=A/'DD_Cosmology_Epilogue_Campaign_Arcs_02.zip'
    preparation=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_02_PREPARATION.json'
    assert all(not p.exists() for p in [history,report,validation,packet,archive,preparation])
    modelpath=local/'ARCS_MODEL.json';casepath=local/'CASEBOOK.json'
    model=read(modelpath);casebook=read(casepath)
    before=deepcopy(model);beforecases=deepcopy(casebook)
    assert casebook['count']==len(casebook['cases'])==19
    bindings=read(oldpacket/'SOURCE_BINDINGS.json')
    assert len(bindings)==41
    checks=[]
    for row in bindings:
        p=oldpacket/'sources'/row['path'];b=p.read_bytes()
        checks.append({'name':'frozen source '+row['path'],'pass':len(b)==row['bytes'] and sha(b)==row['sha256'] and (G/row['path']).read_bytes()==b})
    assert all(c['pass'] for c in checks)
    history.mkdir(parents=True)
    for name in ['ARCS_MODEL.json','CASEBOOK.json','MANIFEST.json']:
        (history/name).write_bytes((local/name).read_bytes())
    model_evidence=info(history/'ARCS_MODEL.json');case_evidence=info(history/'CASEBOOK.json')
    source_path=oldpacket/'sources/The Cosmology of Decennium Descent.docx'
    with ZipFile(source_path) as z: doc=ET.fromstring(z.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paragraphs=[''.join(x.text or '' for x in p.findall('.//w:t',ns)) for p in doc.findall('.//w:p',ns)]
    source_evidence=[{'path':'The Cosmology of Decennium Descent.docx','part':'word/document.xml','paragraphIndexZeroBased':n,'excerpt':paragraphs[n],'textSha256':sha(paragraphs[n].encode())} for n in range(319,323)]
    assert 'errant equation' in paragraphs[321] and 'Mephistopheles envoy' in paragraphs[322]
    issues=[]
    def issue(n,title,kind,pointers,finding,required,case_requirements,status='open-for-joint-review'):
        issues.append({'id':f'ARC03-{n:02d}','title':title,'kind':kind,'status':status,
          'evidence':[{'file':model_evidence,'jsonPointer':p,'value':get(before,p)} for p in pointers],
          'finding':finding,'requiredResolution':required,'requiredWorkedCases':case_requirements})
    issue(1,'Mooring cannot support the stated empty craft','numerical contradiction',
      ['/arcs/1/vessel/body','/arcs/1/strandScene/geometry','/arcs/1/route/requiredPlan'],
      'The platform rating is 2000 lb including tether force; the empty craft is 3000 lb before crew, passengers and cargo. The offered engine-off mooring plan therefore lacks a supporting structure under the printed load rule.',
      'Local successor proposes a 6000 lb combined deck-and-mooring rating. Count actual hull, supported equipment, bodies and tethered load once. This fixes the simple rating contradiction but still needs the full stock/load envelope and overload/transfer procedure in ARC03-02/03/06.',
      ['Empty and fully loaded craft supported at the mooring; same person moves from craft to deck without double-counting; combined support exactly at rating and above rating.'],
      'locally-corrected-proposal-awaiting-joint-review')
    issue(2,'Payload and inventory omit real equipment quantities','incomplete operating envelope',
      ['/arcs/1/vessel/body','/arcs/1/vessel/payload','/arcs/1/vessel/hoods','/arcs/1/vessel/repair','/arcs/1/strandScene/props','/arcs/1/strandScene/risk'],
      'The draft supplies a pound capacity but no vessel Load capacity. Hoods are called part of empty load; clamps, tongs, lined case, harnesses, repair material and some consumables have no complete mass/Load placement. A mass total cannot yet be checked without assumptions. The current body rules require pounds and Load separately, with container contents counted once.',
      'Provide one inventory ledger with documented mass, Load, quantity, initial location and whether included in hull mass or payload; define the craft Load capacity as NEW. Use the actual body/casualty Load rules, melded-gear mass and footprint rules. Make removal/consumption/installation transfers explicit. Do not turn assumed mass into historical source fact.',
      ['Four actual characters plus two crew, all personal gear and mission kit; full/empty refill containers; Large and no-breath passengers; a petrified or transformed body; a load that passes pounds but fails Load.'])
    issue(3,'Support after power loss and missing crew is undefined','missing state transition',
      ['/arcs/1/vessel/movement','/arcs/1/vessel/fuel','/arcs/1/vessel/emergency','/arcs/1/strandScene/geometry'],
      'Fuel at zero stops powered motion, but the draft does not say whether unsupported hover remains possible. It also does not define support when a necessary operator cannot contribute, or how engine, mooring and canopy modes exchange support. The text cannot establish when an actual fall begins.',
      'Write a finite support/movement state procedure. Distinguish supported dock, active flight/hover, moored support, controlled canopy descent and ordinary Falling. State crew reservations, actual support-loss timestamps, legal restart/unmoor conditions and the existing fall-marker interaction. Do not infer stopped generation or automatic pause from user-interface delay in any example.',
      ['Fuel reaches zero while unmoored; pilot or engineer becomes Incapacitated; canopy deployed before/after a real fall marker; safe restart at mooring; extra controller Actions do not add movement.'])
    issue(4,'Opening the hatch has no pressure or air transition','missing state transition',
      ['/arcs/1/vessel/air','/arcs/1/vessel/highAtmosphere','/arcs/1/vessel/breach','/arcs/1/vessel/hoods','/arcs/1/strandScene/procedure'],
      'Workers must reach the exposed lattice, but the draft never states whether opening/closing the ordinary hatch breaks/restores cabin protection, how long that takes, or whether a hull breach still prevents resealing. Work lasts 60 minutes while a hood lasts 60 minutes, so boarding/closure and equality boundaries matter.',
      'Provide an actual entry/exit and hatch procedure, including opening and closing Actions, real positions, any airlock if deliberately authored, damaged-seal behavior, cumulative exposure counters and exact hood-expiry ordering. Do not assume an unprinted airlock or lengthen hoods silently.',
      ['Outward and return hatch cycles with unprotected crew; hood expiry exactly at resealing; damaged hull after closing hatch; a worker delayed beyond the hood interval.'])
    issue(5,'Flight totals omit the deployment Action','incomplete clock claim',
      ['/common/clock','/arcs/1/vessel/emergency','/arcs/1/route/requiredPlan'],
      '480 powered minutes plus 528 descent steps of 6 seconds equals the recorded 31968 seconds, but includes no separate 6-second canopy deployment. ARC16-C03 does include that Action. Without a valid concurrent reservation, deployment adds at least 6 seconds, and powered hovering during it adds 0.1 powered minute. Boarding and unmooring may add more.',
      'Build a complete actor/vehicle event schedule before replacing the final totals. With only an added powered deployment Action, the subtotal would be 31974 seconds, 480.1 powered minutes, 119m54s fuel left and 187m6s cabin air left. Those are not a verified whole-voyage total until ARC03-03/04/06 are resolved. Do not keep the old arithmetic check as evidence of full procedural timing.',
      ['Complete ordinary voyage with crew Actions and hatch cycles; weather detour; final fuel boundary during deployment; powered-idle versus engine-off mooring.'])
    issue(6,'Recovery and departure lack a full actor schedule','incomplete operating envelope',
      ['/arcs/1/vessel/movement','/arcs/1/strandScene/geometry','/arcs/1/strandScene/procedure','/arcs/1/strandScene/risk'],
      'Phase1 explicitly includes mooring/dial Actions in its 20-minute interval. The return does not similarly establish worker positions, clipping/unclipping, moving the actual strand into the craft, hatch closure and unmooring. The full-footprint and required-crew contract cannot be checked from the current prose.',
      'Provide a small exact dock/working-position map and a complete departure sequence. Count necessary movement, harness and hatch Actions; reserve crew Actions once. Retain legal alternative methods using actual character abilities instead of forcing the sample party.',
      ['Two crew and one worker complete all three phases and depart; a Large worker with a real footprint; a stranded or unconscious worker recovered using actual capacity; interrupted departure with no free movement.'])
    issue(7,'Atmosphere classification needs real ancestry/class dispositions','unresolved cross-system interface',
      ['/arcs/1/vessel/highAtmosphere'],
      'Calling the hazard anomalous harmful inhalation does not resolve which current climate, altitude, cold-save, no-breath and adaptive class rules apply. Exact supplied records include Mountain Born, Nomadic Human adaptation, Mycelian/Undead no-breath, Druid cold adaptation, Mage no-breath and several Warrior adaptations. Cold resistance alone does not resolve the Exhaustion component.',
      'Use the supplied exact effect/trait evidence below to state whether each hazard component is cold exposure, altitude/low oxygen, ordinary natural or magical. Honor each real permission and limit; do not label the danger magical solely to negate a printed defense. Define equality when a one-minute adaptation and one-minute exposure save occur together. Keep any new interpretation explicit and jointly reviewed.',
      ['No-breath character; Mountain Dwarf or Mountain Ogre; Frost Drakari; Nomadic Human; the actual Druid cold card; Warrior one-minute and three-round adaptations; cold resistance with a failed Exhaustion save; advantage and disadvantage cancellation.'])
    issue(8,'Current annual record has no unique meaning at departure','ambiguous contract state',
      ['/arcs/2/contractHandout'],
      'Bond return requires the current annual record to be accepted, but no rule identifies that record after the first due date or at an exact boundary. One reading requires an undued second record immediately after year one; another requires only records already due. Early submission and early retirement are also not fully ordered.',
      'Define record numbering, when a record opens, which records must be satisfied for bond return and how early fulfillment works. Preserve the annual obligation and meaningful source benefit. Publish the exact choice in the player handout; do not resolve it through an unannounced penalty.',
      ['Exit immediately after acceptance with no statement; exit after early accepted year-one fulfillment; exit one day after first due date; exit at the exact next annual boundary.'])
    issue(9,'Due, review, grace and issuer absence need one event order','incomplete deadline composition',
      ['/arcs/2/contractHandout','/arcs/2/knowledgeReward/absence'],
      'The separate clauses define due dates, a 24-hour review, 10-day correction and issuer absence, but do not provide a single state table for timely pending submissions, no submission, late first submission, paper theft, delayed review or an absence spanning several annual records.',
      'Provide a per-record state machine and exact simultaneous-event order. A timely pending submission must not default while its allowed review is pending. Decide the no-submission default boundary and actual notice/delivery conditions explicitly. Future annual due dates must remain fixed to T0, with no clock rebasing.',
      ['Timely paper at due instant; rejection at review boundary and correction exactly at grace boundary; no paper; late first paper; two annual records during issuer absence; issuer returns and claimant submits at the exact availability deadline.'])
    issue(10,'The original envoy relationship is absent','source-fidelity omission',
      ['/profiles/2/type','/arcs/2/scene','/arcs/2/contractHandout/0'],
      'Original paragraph322 specifically calls the visitor Mephistopheles envoy. The draft makes Veyr an engine-office courier but does not state that relationship.',
      'Local successor identifies Veyr as Mephistopheles envoy for this Canian offer, with only the printed local office authority. This does not expand Mephistopheles beyond the owner-corrected Cania scope or identify any unrelated being.',
      ['Player-facing refusal scene preserves the named envoy relationship without granting blanket authority.'],
      'locally-corrected-proposal-awaiting-joint-review')
    issue(11,'The errant equation is missing from the causal hook','source-fidelity omission',
      ['/arcs/1/hook','/arcs/1/strandScene/returnEffect'],
      'Original paragraph321 says an errant equation echoes from Broken Ladder strands. The draft attributes interference to the strand without retaining that explicit cause. Retaining this local errant equation does not mean recovering the lost cosmic Equation.',
      'Local successor restores the local errant-equation cause and explicitly separates it from the unresolved original cosmic formula.',
      ['Director explanation and recovery handout distinguish the local disturbance from a research qualification or recovered cosmic Equation.'],
      'locally-corrected-proposal-awaiting-joint-review')
    issue(12,'Payments lack complete custody and transaction timing','incomplete finite resource procedure',
      ['/profiles/1/property','/arcs/1/access','/arcs/1/reward'],
      'Spindle scrap has a buyer offer but no actual named buyer or finite cash stock. Crew escrow has 40gp and a 20gp sortie wage, but its custodian, payee shares and payment timing are unspecified. These are small finite transactions, not permission to generate money.',
      'Give actual custody and timing for the scrap offer and crew wages, including abort, crew replacement and exhausted cash. Separate mission reward, wages and salvage stocks without double-counting the same chest.',
      ['First aborted sortie then second sortie; third sortie with no wage stock; all three spindle bodies sold once; stolen reward or wage chest.'])
    issue(13,'The second annual rejection case has zero elapsed time','incorrect worked-case duration',
      ['/arcs/2/contractHandout/4'],
      'ARC17-C06 includes Veyr reviewing and rejecting the second annual submission but records elapsedSeconds=0 without an explicit immediate-review assumption.',
      'Local successor sets an actual 24-hour review: submission at T0+800days, rejection/notice 86400seconds later; correction grace begins at that actual notice and later due dates do not move.',
      ['The preserved ARC17-C06 ID now distinguishes submission timestamp, review duration and the new grace start.'],
      'locally-corrected-proposal-awaiting-joint-review')
    issue(14,'Transition changes work length but prose hardcodes 30 minutes','cross-field contradiction',
      ['/arcs/1/strandScene/procedure','/arcs/1/strandScene/returnEffect'],
      'The proposed procedure allows a reviewed Transition extension for Phase3, while returnEffect requires completing the actual30minute Phase3. The same release cannot require both an unmodified 30 minutes and an authorized reduced interval.',
      'Local successor ties termination to actual completion of Phase3 using its authorized clock, without adopting the proposed Transition extension. GPT must still define work-order, beneficiaries, qualifications, interruptions and rounding against the current character module.',
      ['Ordinary release; release with the expressly reviewed extension if approved; interruption before and after retained blocks; event equality with scheduled melody loss.'],
      'locally-corrected-proposal-awaiting-joint-review')
    issue(15,'Knowledge and free-will scenes need a substantive design review','design concern, not proven source contradiction',
      ['/arcs/2/knowledgeReward','/arcs/2/refusalExercise'],
      'The draft makes three local demonstrations the entire patent knowledge benefit and offers an uncomplicated paid choice as the free-will test. These are explicit NEW choices, but source fidelity and a fully developed campaign arc require examining whether they supply meaningful knowledge, stakes and decisions. Numeric closure alone cannot establish that.',
      'Ask GPT to develop the actual patent knowledge and choice consequences sufficiently to run a satisfying arc, while retaining informed choice and the original annual-contradiction premise. Do not substitute arbitrary soul penalties, involuntary character changes or generic machine omnipotence for substantive design.',
      ['Use of each patent insight in an actual problem; two meaningfully different freely chosen responses and their finite consequences; refusal of both contract and test remains available.'])

    # Capture actual supplied effects without importing external game rules.
    environments=[]
    pattern=re.compile(r'breathe|breathing|high altitude|extreme cold|cold climates|environmental|suffocat',re.I)
    def walk(value,pointer,path):
        if isinstance(value,dict):
            if isinstance(value.get('effect'),str) and pattern.search(value['effect']):
                environments.append({'path':path,'jsonPointer':pointer+'/effect','id':value.get('id'),'name':value.get('name'),'value':value['effect']})
            for k,v in value.items(): walk(v,pointer+'/'+k.replace('~','~0').replace('/','~1'),path)
        elif isinstance(value,list):
            for i,v in enumerate(value):walk(v,pointer+'/'+str(i),path)
    for binding in bindings:
        path=binding['path']
        if 'class_playtests/' in path or path.endswith('Decennium_Descent_Bard_Playtest_v0_1.json'):
            walk(read(oldpacket/'sources'/path),'',path)
    ancestry_path='DescentReviewChanges/ReviewBible/docs/mechanics/ANCESTRY_BACKGROUND_SOURCE_BINDINGS.md'
    ancestry_lines=(oldpacket/'sources'/ancestry_path).read_text(encoding='utf-8-sig').splitlines()
    ancestry=[{'path':ancestry_path,'lineOneBased':i+1,'excerpt':line} for i,line in enumerate(ancestry_lines) if pattern.search(line) and any(term in line for term in ['Amphibious','Cold Endurance','Mountain Born','Environmental Adaptation','Fungal Nature','Undead Nature'])]
    body_path='DescentReviewChanges/ReviewBible/docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md'
    body_lines=(oldpacket/'sources'/body_path).read_text(encoding='utf-8-sig').splitlines()
    body={'path':body_path,'firstLineOneBased':86,'lastLineOneBased':111,'excerpt':'\n'.join(body_lines[85:111])}
    changes=[]
    def replace(pointer,value):
        parent_pointer,key=pointer.rsplit('/',1);parent=get(model,parent_pointer)
        old=parent[int(key)] if isinstance(parent,list) else parent[key]
        changes.append({'jsonPointer':pointer,'before':old,'after':value})
        if isinstance(parent,list):parent[int(key)]=value
        else:parent[key]=value
    b=model['arcs'][1]
    replace('/arcs/1/hook',b['hook'].replace('A Broken Ladder strand in the upper atmosphere produces the interference.','An errant equation echoes from a Broken Ladder strand in the upper atmosphere and produces the interference, preserving the original cause. This local errant equation is not the lost original cosmic Equation or a granted research qualification.'))
    replace('/arcs/1/strandScene/geometry',b['strandScene']['geometry'].replace('Lattice supports2000lb including tether force, NEW and announced; no permanent travel network.','NEW proposed combined lattice-and-mooring rating is6000lb of actual supported load, including the complete craft and tethered load. Count a body or item only once as it transfers between craft and lattice. The earlier2000lb rating could not support the3000lb empty craft and is superseded only in this local proposal. The full inventory/Load and support-transfer procedures still require ARC03-02/03/06 review. No permanent travel network.'))
    replace('/arcs/1/strandScene/returnEffect',b['strandScene']['returnEffect'].replace('Completing the actual30minute Phase3 release','Completing Phase3 release under its actual authorized work clock (printed30minutes before any expressly approved modifier)'))
    replace('/profiles/2/type','living Devil, NEW named local envoy of Mephistopheles for this Canian offer')
    replace('/arcs/2/contractHandout/0','Issuer: Veyr of the Second Margin, Mephistopheles’ envoy for this Canian offer and licensed courier for the Canian engine patent office. This local license grants only the powers written here. It does not speak for every devil or mortal court and grants no authority beyond the owner-corrected Cania scope.')
    replace('/arcs/2/scene',model['arcs'][2]['scene'].replace('Veyrarrives byordinarypublicroute andcanbequestioned.','Veyr, Mephistopheles’ envoy for this Canian offer, arrives byordinarypublicroute andcanbequestioned.'))
    replace('/knownProposalSeams',model['knownProposalSeams']+['Semantic review03 records15 concrete issues/design questions. Five have narrow local proposal corrections; ten remain open for joint review. In particular the voyage is not yet a complete timed/load/support envelope and the annual contract needs a single explicit state procedure. Do not adopt or describe the candidate as operationally complete.'])
    cases_by_id={c['id']:c for c in casebook['cases']}
    oldcase=deepcopy(cases_by_id['ARC17-C06'])
    cases_by_id['ARC17-C06'].update(events='Claimant submits the identical pair atT0+800days. Veyr completes review24elapsed hours later, identifies duplicate evidence and gives actual notice then.',elapsedSeconds=86400,end='Year2 remains unsatisfied. Its10day correction grace starts at the actual rejection notice atT0+801days. A materially changed conflict may qualify; future annual due dates remain fixed toT0. No arbitrary secret moral test.')
    modelpath.write_bytes(encoded(model));casepath.write_bytes(encoded(casebook))
    (local/'MANIFEST.json').write_bytes(encoded({'files':files(local)}))
    report.write_bytes(encoded({'recordedAtUtc':now,'status':'Independent local semantic audit; no joint approval or adoption.','reviewedModel':model_evidence,'reviewedCasebook':case_evidence,'currentLocalModel':info(modelpath),'currentLocalCasebook':info(casepath),'originalSourceEvidence':source_evidence,'sourceBindings':bindings,'issues':issues,'issueCount':len(issues),'locallyCorrectedProposalIssues':sum(x['status'].startswith('locally-corrected') for x in issues),'openJointReviewIssues':sum(x['status']=='open-for-joint-review' for x in issues),'environmentClassEvidence':environments,'environmentAncestryEvidence':ancestry,'bodyCapacityEvidence':body,'modelChanges':changes,'caseChanges':[{'id':'ARC17-C06','before':oldcase,'after':cases_by_id['ARC17-C06']}],'sourceInformationDeleted':0,'newRulesAdopted':False,'jointReviewComplete':False,'campaignEpochChosen':False,'runtimeTestsExecuted':0,'humanPlaytested':False,'wholeGameComplete':False}))
    checks += [
      {'name':'all19 earlier case IDs retained','pass':{x['id'] for x in beforecases['cases']}=={x['id'] for x in casebook['cases']} and len(casebook['cases'])==19},
      {'name':'prior local bytes preserved','pass':read(history/'ARCS_MODEL.json')==before and read(history/'CASEBOOK.json')==beforecases},
      {'name':'all approval gates remain false','pass':not any(model['common']['approvalGates'].values())},
      {'name':'source equation and envoy words verified against original paragraphs','pass':'errant equation' in paragraphs[321] and 'Mephistopheles envoy' in paragraphs[322]},
      {'name':'24hour rejection case has real elapsed duration','pass':cases_by_id['ARC17-C06']['elapsedSeconds']==24*3600},
      {'name':'prior arithmetic did omit a distinct deployment Action','pass':480*60+528*6==31968 and 6+480*60+528*6==31974},
      {'name':'prior mooring rating fails even empty hull','pass':2000<3000 and 3000+1600<=6000},
      {'name':'five narrow proposal corrections and ten open issues are distinguished','pass':sum(x['status'].startswith('locally-corrected') for x in issues)==5 and sum(x['status']=='open-for-joint-review' for x in issues)==10}
    ]
    failures=[x for x in checks if not x['pass']]
    assert not failures,failures
    validation.write_bytes(encoded({'recordedAtUtc':now,'model':info(modelpath),'casebook':info(casepath),'semanticReview':info(report),'checks':checks,'checkCount':len(checks),'failureCount':0,'scope':'Frozen-source preservation, prior draft/case retention, source wording and selected audit arithmetic. Ten semantic issues remain open. These checks do not certify a complete voyage, contract, balance or playtest.','newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False}))
    shutil.copytree(oldpacket,packet)
    for name in ['ARCS_MODEL.json','CASEBOOK.json']:(packet/name).write_bytes((local/name).read_bytes())
    (packet/'SEMANTIC_REVIEW_03.json').write_bytes(report.read_bytes())
    (packet/'LOCAL_VALIDATION.json').write_bytes(validation.read_bytes())
    context=read(packet/'CURRENT_REVIEW_CONTEXT.json')
    context.update(recordedAtUtc=now,packetRevision='02',relicNullReview='Actual EPI08–14 completion reply recovered through native read_thread, reporting47cases and archive SHA25624eeecec44d1ed248e96adf1d58b80b5c7f8434a3fdb487bdf7443c272de4699. Exact archive not locally retrieved or reviewed. Native export request is visible as user turn fb930b64-06e3-4a33-9f72-60037b465c97 but has no assistant reply and status systemError. Do not reauthor EPI08–14.',currentLocalModel=info(modelpath),currentLocalCases=info(casepath),currentValidation=info(validation),semanticReview=info(report),openJointReviewIssues=10,sourceFidelityCorrections='Errant equation and Mephistopheles envoy retained; no recovered cosmic Equation or expanded realm authority.')
    (packet/'CURRENT_REVIEW_CONTEXT.json').write_bytes(encoded(context))
    request=(packet/'REQUEST.txt').read_text(encoding='utf-8')
    request='REVISION02: Read SEMANTIC_REVIEW_03.json before review. It records15 findings: five narrow local proposal corrections and ten unresolved interfaces/design questions. Preserve all19 case IDs, including the now-explicit24hour review inARC17-C06. The old31968second voyage arithmetic is incomplete: an independent canopy deployment alone adds6seconds and may cost0.1powered minute; hatch, return and unmooring actions must be fully scheduled before claiming any total. The proposed6000lb mooring only fixes its obvious rating contradiction. Resolve full mass/Load, support, hatch/exposure, actual trait/card defenses and annual record/deadline composition. The package is still unsubmitted and unadopted.\n\n'+request
    (packet/'REQUEST.txt').write_text(request,encoding='utf-8',newline='\n')
    entries=[{'path':p.relative_to(packet).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(packet.rglob('*')) if p.is_file() and p!=packet/'PACKAGE_MANIFEST.json']
    (packet/'PACKAGE_MANIFEST.json').write_bytes(encoded({'files':entries}))
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for p in sorted(packet.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(packet).as_posix())
    with ZipFile(archive) as z:
        assert set(z.namelist())=={x['path'] for x in entries}|{'PACKAGE_MANIFEST.json'}
        for e in entries:
            content=z.read(e['path']);assert len(content)==e['bytes'] and sha(content)==e['sha256']
    preparation.write_bytes(encoded({'recordedAtUtc':now,'status':'prepared-not-submitted','supersedesForSubmission':info(A/'DD_Cosmology_Epilogue_Campaign_Arcs_01.zip'),'archive':info(archive),'sourceCount':41,'arcs':3,'authoredCases':19,'semanticReview':info(report),'openJointReviewIssues':10,'localValidation':info(validation),'newRulesAdopted':False,'sourceInformationDeleted':0,'campaignEpochChosen':False,'runtimeTestsExecuted':0,'humanPlaytested':False,'dependency':'Recover and review the exact EPI08–14 return before cross-module adoption; new conference requires restored GPT communication.'}))
    print(json.dumps({'review':info(report),'model':info(modelpath),'casebook':info(casepath),'issues':15,'locallyCorrectedProposals':5,'openIssues':10,'checks':len(checks),'failures':0,'preparedPacket':info(archive),'preparation':info(preparation),'submitted':False}))

if __name__=='__main__':main()
