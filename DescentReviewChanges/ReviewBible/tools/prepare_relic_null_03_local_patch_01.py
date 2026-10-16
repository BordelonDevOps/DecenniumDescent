"""Preserve revision03 and prepare a finite, unapplied correction for actual GPT review."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib,json,re
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())
def digest(b):return hashlib.sha256(b).hexdigest()

def main():
    src=A/'cosmology-epilogue-relic-null-03-return'
    root=A/'relic-null-03-local-patch-01'
    archive=A/'DD_Relic_Null_03_Local_Patch_01.zip'
    review=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_03_SEMANTIC_REVIEW_01.json'
    assert all(not p.exists() for p in [root,archive,review])
    files={p.name:p.read_bytes() for p in src.iterdir() if p.is_file()}
    assert len(files)==8
    original_files=dict(files)
    m=json.loads(files['RELIC_NULL_MODEL.json']);c=json.loads(files['CASEBOOK.json'])
    reg=json.loads(files['REGISTER.json']);sources=json.loads(files['SOURCE_HASHES.json'])
    prose={k:files[k].decode() for k in ['PLAYER_CHAPTER.md','DIRECTOR_CHAPTER.md']}
    operations=[];findings=[]
    def finding(i,title,evidence,proposal):
        findings.append({'id':i,'title':title,'evidence':evidence,'proposedResolution':proposal,'gptReviewed':False})
    def model(pointer,new,issue):
        node=m;parts=pointer.strip('/').split('/')
        for part in parts[:-1]:node=node[int(part)] if isinstance(node,list) else node[part]
        key=int(parts[-1]) if isinstance(node,list) else parts[-1]
        old=deepcopy(node[key]) if key in node or isinstance(node,list) else None
        operations.append({'issue':issue,'file':'RELIC_NULL_MODEL.json','jsonPointer':pointer,'old':old,'replacement':deepcopy(new)})
        node[key]=new
    def replace(name,old,new,issue,count=1):
        assert prose[name].count(old)==count,(name,old,prose[name].count(old),count)
        prose[name]=prose[name].replace(old,new)
        operations.append({'issue':issue,'file':name,'old':old,'replacement':new,'expectedOccurrences':count})
    def both(old,new,issue):
        for name in prose:replace(name,old,new,issue)
    def mirrored(pointer,new,issue):
        node=m
        for part in pointer.strip('/').split('/'):node=node[int(part)] if isinstance(node,list) else node[part]
        old=deepcopy(node);model(pointer,new,issue);both(old,new,issue)
    def case(cid,field,new,issue):
        index=next(i for i,x in enumerate(c['cases']) if x['id']==cid)
        old=deepcopy(c['cases'][index].get(field));c['cases'][index][field]=new
        operations.append({'issue':issue,'file':'CASEBOOK.json','caseId':cid,'jsonPointer':f'/cases/{index}/{field}','old':old,'replacement':deepcopy(new)})
    byid={x['id']:x for x in c['cases']}
    finding('RN3-01','Initial failed exposure save is absent from the operative rule',
      ['null.field.exposure requires WIS DC15 but never states the first failure applies Veil; RN-N01 and RNX-14-A do apply it. Both chapters repeat the omission.'],
      'State the first failure creates one Veil; success creates none; existing Veil follows the no-stack/no-refresh rule. Dead exception remains.')
    old=m['null']['field']['exposure'];new=old+' On a failed hourly save, a creature without Null Veil gains one Null Veil immediately; on success it gains none. A creature already bearing Veil uses the no-stack/no-refresh rule below. Dead targets remain ineligible.'
    mirrored('/null/field/exposure',new,'RN3-01')
    finding('RN3-02','Both chapters omit the recipient lifecycle branches they reference',
      ['Ordered damage step6 refers to recipientLifecycle branches below; neither chapter prints the model table. Undying Spellform, Ranger Beast, finite summons, undead and local projections cannot be adjudicated from the advertised complete prose.'],
      'Render every existing recipientLifecycle branch in both chapters, unchanged, and print the existing eight local actor bindings. Remove double numbering only.')
    labels={'ordinaryLiving':'Ordinary living recipient','rangerBeast':'Ranger Beast','finiteSummonFamiliarMirrorBeast':'Finite summon, Familiar or Mirror Beast','mageLichElite':'Mage Lich elite','wizardStandardUndead':'Wizard standard undead','localProjection':'Authored local projection','undyingSpellform':'Undying Spellform','wouldDieProtections':'Would-die protections','ordinaryNonlivingConstruct':'Actual nonliving Construct','localSpirit':'Silence Wraith only'}
    dn=m['null']['veil']['damageNonlethal']
    table='### Recipient lifecycles for qualifying Null damage\n\n'+''.join('**'+labels[k]+'.** '+v+'\n\n' for k,v in dn['recipientLifecycle'].items())
    table+='**Local actor bindings.** '+ '; '.join(k+': '+v for k,v in dn['localActorBindings'].items())+'.\n\n'
    both('**What Null Veil does not erase.**',table+'**What Null Veil does not erase.**','RN3-02')
    for name in prose:
        for n in range(1,9):replace(name,f'{n}. {n}. ',f'{n}. ','RN3-02')
    finding('RN3-03','Actor placement contradicts counts and arena distance',
      ['All four Toy Sentinels use the single center (20,20) despite one-per-plinth count. Devil(25,20) and Demon(20,20) are5ft apart; CH10 requires30ft.'],
      'Use four distinct Toy/plinth identities at (10,10),(30,10),(10,30),(30,30). Keep CH10 stated30ft separation by Devil(10,25),Demon(40,25), circlecenter(25,25). New scene geometry only.')
    new='NEW fixed scene map: 40×40-ft square, southwest origin, floor z=0, ceiling20. West arch x=0,y17.5–22.5; east arch x=40,y17.5–22.5 is initially sealed. Central 10×10 forge dais occupies x15–25,y15–25 at floor level. Four 5×5 plinth spaces are centered at (10,10),(30,10),(10,30),(30,30); Toy1..Toy4 start respectively on those spaces. Each is a separate ACT-TOY-SENTINEL creature with its own24HP and resolution record. No starting spaces overlap.'
    mirrored('/chambers/0/geometry',new,'RN3-03')
    old=m['actorProfiles']['ACT-TOY-SENTINEL']['initialPlacement'];new='CH01: Toy1(10,10), Toy2(30,10), Toy3(10,30), Toy4(30,30), all floor z=0, one independent creature per printed plinth.'
    model('/actorProfiles/ACT-TOY-SENTINEL/initialPlacement',new,'RN3-03');replace('DIRECTOR_CHAPTER.md',old,new,'RN3-03')
    mirrored('/chambers/9/geometry','NEW fixed scene map: 50-ft-diameter arena centered (25,25), floor z=0, ceiling20. West entry at (0,25), east exit at (50,25); central accord circle has diameter10 and center (25,25). Devil starts (10,25), Demon (40,25), exactly30ft apart; each occupies its own Medium footprint.','RN3-03')
    for key,pos in [('ACT-ACCORD-DEVIL','(10,25)'),('ACT-ACCORD-DEMON','(40,25)')]:
        old=m['actorProfiles'][key]['initialPlacement'];new=f'CH10: {pos}, floor z=0.'
        model('/actorProfiles/'+key+'/initialPlacement',new,'RN3-03');replace('DIRECTOR_CHAPTER.md',old,new,'RN3-03')
    old=m['chambers'][9]['procedures'][0]
    mirrored('/chambers/9/procedures/0',old.replace('Devil at west inner edge, Demon at east inner edge','Devil at (10,25), Demon at (40,25)'),'RN3-03')
    case('RN-C01','initialState','Party enters CH01; Toy1..4 each have24HP on distinct plinths at (10,10),(30,10),(10,30),(30,30). Each approach uses real legal movement.','RN3-03')
    case('RN-C10','initialState','Devil starts(10,25), Demon(40,25),30ft apart, both above0HP. Each broker pays actual movement to enter the central10-ft accord circle before its Action; this example assumes both projections remain above0 until the second success.','RN3-03')
    finding('RN3-04','Player chapter discloses hidden puzzle answers',
      ['PLAYER_CHAPTER CH04 geometry prints Row1=B,Row2=A,Row3=C despite its Director-only-answer promise. CH08 fallback prints sequence2-5-1-6.'],
      'Keep exact answers in model/Director only; player text states successful read/check reveals the fixed answer.')
    replace('PLAYER_CHAPTER.md',' Fixed safe lanes remain Row1=B, Row2=A, Row3=C.',' The Director records one fixed safe lane per row; successful observation reveals it.','RN3-04')
    replace('PLAYER_CHAPTER.md','success derives mechanical tab sequence 2-5-1-6 and opens exit','success reveals the fixed mechanical tab sequence and opens exit','RN3-04')
    finding('RN3-05','Retained examples contain obsolete fields and incomplete ledgers',
      ['RN-R10-04 still says north backstage; RN-C09 unused tokens stay in bowl; RNX-08-B still spends3/5HP and rolls1d6 although clipped catches now do no impact. RNX-09-A mentions Hold; RNX-09-B lists backpack/tray/A absent from its setup. RNX-14-B unspecified rest conflicts with beneficial-LR reset. RNX-07-A has3 reads but2 results and an unexplained10m+.'],
      'Repair exact stale fields; retain all75 IDs/order. Add explicit DC14/+5 natural1 arithmetic to RNX-01-B. Cases remain authored examples, not tests.')
    x=deepcopy(byid['RN-R10-04']['steps']);x[0]=x[0].replace('north backstage','east-stage');case('RN-R10-04','steps',x,'RN3-05')
    case('RN-C09','initialState',byid['RN-C09']['initialState'].replace('remaining8 tokens stay bowl','remaining8 tokens stay at their numbered neutral stations'),'RN3-05')
    case('RNX-08-B','consumedStock','No HP damage from either clipped catch; each failed attempt spends Action+30 movement, each recovery Action+10 movement. No cable stock consumed.','RN3-05')
    case('RNX-08-B','rollsAndDCs',['Climb DC14 totals10/12 fail; no impact damage roll for either supported catch.'],'RN3-05')
    case('RNX-09-A','consumedStock','Card consumed once at t0; no extra stock is granted by the recovery extension.','RN3-05')
    case('RNX-09-B','consumedStock','One card consumed at activation; no backpack, tray or additional traveler is introduced by this example.','RN3-05')
    case('RNX-14-B','initialState','Character enters CH07 field for25m, leaves for a beneficial Short Rest only (no beneficial Long Rest), later reenters35m; separately uses CH11 Veiled Expanse card for10m.','RN3-05')
    x=deepcopy(byid['RNX-14-B']['steps']);x[0]='First CH07 stay accumulates25m; leaving pauses the field accumulator. The specified beneficial Short Rest outside does not clear it. A beneficial Long Rest wholly outside this field would clear its partial accumulator under the actual exposure rule; that event does not occur in this branch.';case('RNX-14-B','steps',x,'RN3-05')
    case('RNX-14-B','elapsedTime','25m exposure + one beneficial Short Rest outside +35m exposure + separate10m card visit. No beneficial Long Rest occurs.','RN3-05')
    case('RNX-07-A','elapsedTime','Three successful read Actions plus actual paid travel along the fixed lanes; no10-minute retry study is needed.','RN3-05')
    case('RNX-07-A','rollsAndDCs',['Row1 read DC14 total15 success','Row2 read DC14 total14 success','Row3 read DC14 total16 success'],'RN3-05')
    x=deepcopy(byid['RNX-01-B']['steps']);x[3]='BT-4 harvest uses modifier+5, natural1: total6 vsDC14 is ordinary Failure, shifted one degree by natural1 to Critical Failure. Yield0; the node has spent its single attempt and the tool requires10-minute cleaning before another flora harvest.';case('RNX-01-B','steps',x,'RN3-05')
    finding('RN3-06','Frightened climb example does not locate its fear source',
      ['CONDITIONS_PLAYTEST lines311–325: visible fear source imposes check disadvantage; moving closer is forbidden. RNX-08-A assumes advantage without specifying fear visibility or movement direction.'],
      'Keep self-steady rule; state source is below and out of sight so climbing away is legal and no fear disadvantage applies; explicitly explain visible-source cancellation alternative.')
    x=byid['RNX-08-A']['initialState'];case('RNX-08-A','initialState',x+' In Subcase2 the recorded fear source is below the starting platform, out of line of sight; climbing upward moves farther away. No other disadvantage applies.','RN3-06')
    x=deepcopy(byid['RNX-08-A']['steps']);x[-1]+=' If the fear source were visible, Frightened disadvantage would cancel this advantage; self-steady never permits willingly moving closer to the fear source.';case('RNX-08-A','steps',x,'RN3-06')
    finding('RN3-07','Twelve-character cap is real but absent from the84-source handoff',
      ['Current GAMEPLAY_LOOP_CANON.md line91 states no more than12 characters per Expedition. None of the84 SOURCE_HASHES paths is this guide; prior cap claim therefore lacked supplied source evidence.'],
      'Freeze and supply that current file as source85; retain original84 entries unchanged. Bind the exact line91 excerpt. No new roster cap is created.')
    cap=R/'docs/mechanics/GAMEPLAY_LOOP_CANON.md';cap_binding=info(cap)
    assert cap.read_text(encoding='utf-8').splitlines()[90]=='An Expedition contains no more than twelve characters. Larger forces are multiple Expeditions coordinating.'
    assert all(x['path']!=cap_binding['path'] for x in sources['sources'])
    sources['sources'].append(cap_binding);sources['sourceCount']=85
    model('/chambers/8/voting/expeditionCapSource',{'path':cap_binding['path'],'firstLineOneBased':91,'lastLineOneBased':91,'excerpt':cap.read_text(encoding='utf-8').splitlines()[90]},'RN3-07')
    finding('RN3-08','Shardpool activation, emergency-space and voluntary-release boundaries need explicit text',
      ['Action by willing group does not identify who spends it or what adjacent means. Nearest legal chamber floor can include the supposedly+20-only emergency pad. Return Waiting forbids all voluntary agency but discusses only outside-caster concentration release. Geometry omits the promised north bypass exit.'],
      'One initiator spends Action, included among1–6 willing travelers with current footprints within5ft of pool. Exclude pad from ordinary return/origin before+20. Permit only actual no-action end-concentration during Waiting. Print north door/lever. These are NEW scoped completions for GPT review.')
    old=m['chambers'][10]['procedures'][0]
    new=old.replace('Action by willing group up to six adjacent creatures activates drawn card.','One willing initiator spends one Action to activate the drawn card for itself and up to five other willing creatures. Each traveler must have its current footprint within5ft of the pool boundary and fit a legal supported, nonoverlapping origin footprint outside the emergency pad. Consent costs no extra Action; no traveler gains an Action from activation.')
    mirrored('/chambers/10/procedures/0',new,'RN3-08')
    old=m['chambers'][10]['procedures'][2]
    mirrored('/chambers/10/procedures/2',old+' For all ordinary placement attempts, exclude the reserved emergency pad; it is unlocked only by the explicit +20:00 emergency step and remains eligible on later rechecks.','RN3-08')
    old=m['chambers'][10]['procedures'][6]
    mirrored('/chambers/10/procedures/6',old+' Narrow release exception: an unresolved traveler may end its own existing concentration without an Action if its actual source permits that release. This permits no new activation, movement, harvest or other voluntary activity; a resulting eligibility change triggers the same immediate return check.','RN3-08')
    old=m['chambers'][10]['geometry']
    mirrored('/chambers/10/geometry',old+' The north bypass exit is x22.5–27.5,y40, with its lever adjacent at (27.5,37.5), outside the emergency pad. Ordinary legal floor connects the west entrance to that lever/exit.','RN3-08')
    case('RNX-09-A','initialState',byid['RNX-09-A']['initialState']+' B has a legal Medium origin footprint but adjacent actual obstacles prevent its current Large body fitting there; all other ordinary free spaces are likewise too small for B. The reserved pad is excluded before+20:00. A and B current bodies fit nonoverlapping spaces in the destination cell.','RN3-08')
    x=deepcopy(byid['RNX-09-B']['steps']);x.append('Separate release check: a waiting traveler whose own existing concentration is the source of an obstructing form may end that concentration without an Action only if the actual source allows it. Process the source end and immediate placement recheck; no other voluntary activity becomes available.');case('RNX-09-B','steps',x,'RN3-08')
    finding('RN3-09','Void arrival fear lacks a source and transition-safe expiry',
      ['CH11 Boundless Void arrival says Frightened until end of next turn from vertigo, without a recorded fear-source location or regular/outside-initiative clock.'],
      'Use cell-local center(10,10,z0) as the NEW fixed vertigo source; end at next regular target-turn end or outside+6s absolute, preserving markers. Ordinary immunity and fear rules still apply.')
    old=m['chambers'][10]['destinations']['Boundless Void']
    new='20×20×20 force-lattice cell, local southwest origin, floor z=0, with no air loss/gravity hazard in this bounded staging bubble. On arrival WIS save DC14 or Frightened of the fixed vertigo source at cell center(10,10,z0) until the end of the target’s next regular turn; outside initiative,6 elapsed seconds absolute. Preserve the recorded virtual/absolute deadline through initiative changes; ordinary fear immunity and movement restrictions apply. No outer travel.'
    model('/chambers/10/destinations/Boundless Void',new,'RN3-09');replace('DIRECTOR_CHAPTER.md',old,new,'RN3-09')
    now=datetime.now(timezone.utc).isoformat()
    meta={'id':'RELIC-NULL-03-LOCAL-PATCH-01','status':'PROPOSED only; actual GPT review pending; no adoption','recordedAtUtc':now,'basedOn':info(A/'DD_Cosmology_Epilogue_Relic_Null_03_Return_01.zip'),'findingIds':[v['id'] for v in findings]}
    m['localCorrectionProposal']=meta;reg['localCorrectionProposal']=meta;c['localCorrectionProposal']=meta
    for name in prose:
        prose[name]=prose[name].replace('the same 84 frozen/current source bindings are used.','the original84 frozen/current source bindings are retained; current GAMEPLAY_LOOP_CANON.md is additionally supplied as source85 for the existing12-character cap.')
        prose[name]='> Local correction proposal01 to the preserved revision03. GPT review is pending; this is not adopted.\n\n'+prose[name]
    files.update({'RELIC_NULL_MODEL.json':encoded(m),'REGISTER.json':encoded(reg),'CASEBOOK.json':encoded(c),'SOURCE_HASHES.json':encoded(sources)})
    files.update({k:v.encode() for k,v in prose.items()})
    files['VERDICT.md']=('Local correction proposal01: actual GPT review PENDING. No adoption.\n\nThe original revision03 verdict below is preserved as historical GPT text, not a claim that these newly identified gaps were resolved. See PATCH_MANIFEST.json outside this candidate directory for exact operations.\n\n'+files['VERDICT.md'].decode()).encode()
    manifest={'moduleId':m['moduleId'],'localCorrectionProposal':meta,'files':[{'path':k,'bytes':len(v),'sha256':digest(v)} for k,v in files.items() if k!='EVIDENCE_MANIFEST.json']}
    files['EVIDENCE_MANIFEST.json']=encoded(manifest)
    original_ids=[x['id'] for x in json.loads((src/'CASEBOOK.json').read_bytes())['cases']]
    assert [x['id'] for x in c['cases']]==original_ids and len(original_ids)==75
    assert sources['sources'][:84]==read(src/'SOURCE_HASHES.json')['sources']
    assert 'Row1=B' not in prose['PLAYER_CHAPTER.md'] and '2-5-1-6' not in prose['PLAYER_CHAPTER.md']
    for k,v in dn['recipientLifecycle'].items():assert all(v in s for s in prose.values())
    assert all((src/n).read_bytes()==b for n,b in original_files.items())
    checks={'original75CaseIdsSameOrder':True,'original84SourceEntriesUnchanged':True,'source85ActualBytes':cap_binding,'all10LifecycleBranchesPrintedInBothChapters':True,'playerFixedPuzzleAnswersRemoved':True,'originalReturnedEightFilesUnchanged':True,'runtimeTestsExecuted':0}
    packet={'proposal':meta,'findings':findings,'operations':operations,'sourceEntryAppend':cap_binding,'checks':checks,'newRulesAdopted':False,'sourceInformationDeleted':0,'semanticReviewScope':'Both full prose chapters, all75 authored examples, current Null model and revision03 actor/maps/procedures reviewed; reference/source checks are distinct from execution and numerical balance.'}
    (root/'candidate').mkdir(parents=True)
    for name,b in files.items():(root/'candidate'/name).write_bytes(b)
    (root/'PATCH_MANIFEST.json').write_bytes(encoded(packet))
    capout=root/'additional_sources'/cap_binding['path'];capout.parent.mkdir(parents=True);capout.write_bytes(cap.read_bytes())
    (root/'README.txt').write_text('Review this finite Codex correction proposal against the preserved revision03 archive. PATCH_MANIFEST.json lists exact before/after operations and nine findings. candidate/ contains the complete proposed eight-file result. additional_sources/ contains source85 GAMEPLAY_LOOP_CANON.md; original84 entries remain unchanged. Do not regenerate the whole module. Return a text verdict for RN3-01..09: AGREE, REVISE with exact replacement, or DISAGREE with source reason. Independently inspect changed values and their interactions, especially new scene coordinates, activation budget, pad timing, concentration release and fear source. Approval is only authored provisional playtest scope, never canon, owner rulings, runtime, human balance, whole-game or later-draft approval. If approved, identify this patch archive by exact SHA and authorize only these exact changes. Preserve all original sources and returns.\n',encoding='utf-8')
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    packet['proposedArchive']=info(archive);packet['patchManifest']=info(root/'PATCH_MANIFEST.json')
    review.write_bytes(encoded(packet))
    request=A/'RELIC_NULL_03_LOCAL_PATCH_01_REVIEW_REQUEST.txt'
    request.write_text('Codex independently reviewed your preserved118128-byte revision03 (SHA88df4e8a928ac2e2407ba9872801c52e791ab6fa066ca22124c9b93a1e029764). All247 source/identity checks passed. The remaining nine bounded findings and a complete proposed correction are attached as DD_Relic_Null_03_Local_Patch_01.zip. Its exact SHA256 is '+info(archive)['sha256']+'. Please read README.txt and PATCH_MANIFEST.json, inspect the proposed changed values in candidate/, and confer on RN3-01 through RN3-09. Original84 sources and75 case IDs/order remain; source85 supplies the actual existing twelve-character cap. No original returned file was changed. Please return a text-only exact verdict (AGREE/REVISE/DISAGREE with source reason) for each finding; do not regenerate the entire archive. If the exact proposed patch is acceptable, explicitly approve only its bounded authored provisional-playtest scope by archive hash. Otherwise supply exact replacement text for remaining corrections so we can converge without losing existing fixes. No owner identities/epoch, runtime, balance, whole-game or unseen later content is approved.\n\n'+ '\n'.join(v['id']+' — '+v['title']+': '+v['proposedResolution'] for v in findings),encoding='utf-8')
    print(json.dumps({'review':info(review),'patchArchive':info(archive),'request':info(request),'findings':len(findings),'operations':len(operations),'newRulesAdopted':False}))

if __name__=='__main__':main()
