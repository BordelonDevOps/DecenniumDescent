"""Integrate actual GPT Ready finding and independent full-current-text findings.

Preserves every Current05 byte and each changed case/procedure. No adoption.
"""
import copy,hashlib,json,math
from pathlib import Path
from datetime import datetime,timezone
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';R=G/'DescentReviewChanges/ReviewBible'
P=A/'ac6-local-current-05';O=A/'ac6-semantic-current-06';I=A/'ac6-full-current-review-03-input'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p,name=None):
 b=p.read_bytes();return {'path':name or p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def ref(path,pointer,role):return {'path':path,'pointer':pointer,'role':role,'authority':'current authored candidate' if path=='SPELLS_MODEL.json' else 'frozen source'}
def section(path,heading,role):return {'path':path,'section':heading,'role':role,'authority':'frozen source'}
assert not O.exists()
report_path=A/'AC6_LOCAL_CURRENT_05_SEMANTIC_REVIEW_06.json';assert not report_path.exists()
review=read(A/'ac6-local-current-05-review/REVIEW.json')
assert sha((A/'DD_AC6_Local_Current_05_Review.zip').read_bytes())=='9a2f6dee676af1597dbfb2afecbae8ed15e54a441c353f4118beb6e157049bc2'
for b in review['reviewedCurrentArtifactBindings']:
 raw=(P/b['name']).read_bytes();assert len(raw)==b['bytes'] and sha(raw)==b['sha256']
m=read(P/'SPELLS_MODEL.json');oldm=copy.deepcopy(m);c=read(P/'CASEBOOK.json');oldc=copy.deepcopy(c);r=read(P/'REGISTER.json')
cases={v['id']:v for v in c['cases']};orig=read(I/'CURRENT_REVIEW_INPUT.json');originals={v['id']:v for v in orig['currentExamples']}
ac5='DescentReviewChanges/ReviewBible/data/public/spell_candidates/abjuration_conjuration_rank5_reviewed_05.json'
ac4='DescentReviewChanges/ReviewBible/data/public/spell_candidates/abjuration_conjuration_rank4_reviewed_03.json'
conditions='DescentReviewChanges/ReviewBible/docs/mechanics/CONDITIONS_PLAYTEST.md'
core='DescentReviewChanges/ReviewBible/docs/mechanics/CORE_RESOLUTION_PLAYTEST.md'
combat='DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md'
null='DescentReviewChanges/ReviewBible/docs/mechanics/COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md'
changed=[]
def edit(cid):
 v=cases[cid]
 if cid not in changed:v['local06PreviousCurrentVersion']=copy.deepcopy(v);changed.append(cid)
 return v
def append_original(cid,text=None):
 v=edit(cid)
 t=text if text is not None else originals[cid]['proposedAdjudication']
 v['actionsAndResolution'].append('RESTORED CURRENT SCENARIO: '+t)
 v.setdefault('originalScenarioRestoration',{})['inputExampleId']=cid

# GPT's substantive Ready correction is correct. Its JSON pointer1 has only the
# release replacement string, so use the separately explicit numbered items.
ready=review['requiredMinimalCorrection']['directorReview']
v=edit('AC6-N15')
v['actionsAndResolution'][2]=ready['replacementItem3'].removeprefix('3. ')
v['actionsAndResolution'][3]=ready['replacementItem4'].removeprefix('4. ')
assert v['actionsAndResolution'][2].startswith('At t20.5') and v['actionsAndResolution'][3].startswith('At t24.5')

sky_rule={
 'classification':'Explicit AC6 Skybrand spatial-attack clarification proposed for joint review; no change to damage-root ownership or global condition rules',
 'rule':[
  'Skybrand remains a caster-dealt noncreature effect. For its actual melee spell attack, use the blade current attack-origin point for reach, attack line of effect and distance-based attack predicates, including Prone and the within5feet Unconscious/Paralyzed critical-hit rule. This does not relocate the caster body, grant remote senses, create a creature attacker or change the caster-dealer root checkpoint.',
  'Apply current conditions at each separate attack. Against an ordinarily Unconscious target within5feet of the blade, the attack has ordinary advantage and any hit is critical. Multiple advantage sources do not stack. Double only damage dice; ordinary damage at already0HP applies two death failures for a critical when the target uses death saves. Actual Null qualification still uses the caster state at that attack root.'
 ],
 'sourceRefs':[section(conditions,'Unconscious / Prone / Paralyzed','accepted attack-distance and condition predicates'),section(core,'Attack / Ordered damage / Zero HP and recovery','accepted dice and death-failure rules'),ref('SPELLS_MODEL.json','/spells/9/procedure','actual Skybrand attack origin and root mapping')]
}
m['sharedRules']['AC6-SKYBRAND-ORIGIN-06']=sky_rule
m['spells'][9]['local06PreviousCurrentVersion']=copy.deepcopy(oldm['spells'][9])
m['spells'][9]['procedure']+='\n\nCURRENT SPATIAL ATTACK CLARIFICATION: use AC6-SKYBRAND-ORIGIN-06. The actual blade point supplies attack distance for Prone and adjacent Unconscious/Paralyzed critical hits; damage dealer/root owner remains the caster. Re-evaluate conditions at each of the two attacks.'
v=edit('AC6-N19')
v['initialState']+=' T has no independent immunity or source-specific conscious-at0 exception. There is no intervening event removing Unconscious/Prone before the second attack.'
v['actionsAndResolution'][1]+=' Ordinary0HP rules also make T Unconscious and Prone; Null does not grant a conscious-at0 exception.'
v['actionsAndResolution'][3]='Second attack uses advantage from actual Unconscious/adjacent Prone, rolling d20 faces[7,11], taking11+8=19 againstAC15. It hits from the blade point within5feet, so the accepted Unconscious rule makes it critical even without natural20. Roll doubled2d12 faces[2,3]=5 lightning. This new caster-dealt root is created after the real Veil purge, so nullNonlethal=false. At already0HP, positive ordinary critical damage cancels Stable recovery and records TWO failed death saves; T remains Dying with failures2/successes0. Five is below the20HP instant-death threshold and2*5<20 triggers no massive-damage Wound check. The earlier qualifying Null root and its outcome are not rewritten.'
v['clockLedger']['stableRecovery']='First root event time+7200, canceled by second ordinary critical hit.'
v['damageLedger']={'firstRoot':{'nullNonlethal':True,'damage':8,'hpBefore':8,'hpAfter':0,'state':'Stable, Unconscious, Prone','deathFailures':0,'deathSuccesses':0},'secondRoot':{'nullNonlethal':False,'attackFaces':[7,11],'attackModifier':8,'attackTotal':19,'automaticAdjacentCritical':True,'damageDice':'2d12','damageFaces':[2,3],'damage':5,'state':'Dying, Unconscious, Prone','deathFailures':2,'deathSuccesses':0}}
v['sourceRefs'] += sky_rule['sourceRefs'][:2]+[ref('SPELLS_MODEL.json','/sharedRules/AC6-SKYBRAND-ORIGIN-06','proposed explicit spatial attack bridge')]

v=edit('AC6-N01')
v['initialState']+=' A and B each occupy an ordinary Medium5ft footprint. The Blast caster actually perceives both and affirmatively regards both as enemies; center LoE is clear. B has DEX+0 and no other save modifier against the Blast DC16.'
v['actionsAndResolution'][1]='Massive Elemental Blast is actual rank5 and its authorized origin is outside the Globe. Both recorded enemy bodies satisfy the actual Blast target predicate. A receives no new local spell application because Globe blocks it. B rolls DEX natural8+0=8 againstDC16 and fails, so the shared5d8=22 fire applies in full to B before its own defenses. A receives no deferred damage when Globe ends.'
v['costLedger']['blastBaseRp']=10
v=edit('AC6-N02')
v['actionsAndResolution'][1]+=' In this outside branch, legal commitment still spends3RP(20->17) and starts Recharge2 before the incoming rank3 payload is blocked; no task roll or refund follows.'

v=edit('AC6-N10')
v['initialState']='Seal protects eligible parent P at one locus. Independent accepted Lesser Antimagic F1 begins t18 and would remain through t24 absent removal. F1 is rank5; no other suppressor, nondispel protection or blocker applies to its termination operation. At t20 an eligible Wizard outside F1 casts Greater Dispel for10RP with a legal center/LoE capturing immutable operations for F1, Seal and P.'
v['actionsAndResolution'][0]='At the immutable snapshot, the termination operation targeting F1 ignores only F1 itself under AC5-ANTIMAGIC-IO-04. F1 is rank5, so accepted Greater Dispel ends it AUTOMATICALLY at t20. No ability check is rolled for F1.'
v['actionsAndResolution'][2]='After F1 ends at20, still-live Seal protection resumes at the current parent origin, but the captured Seal/P termination operations are not rescanned or replayed. In an independent branch where F1 remains active, Wizard class Dispel/cards/19 into that suppressed locus is also a rank3 spell application and cannot execute there after its legal paid commitment.'
v['costLedger']['greaterDispelRp']=10
v['clockLedger']={'antimagicStart':18,'antimagicPlannedEndAbsentRemoval':24,'antimagicActualEnd':20,'greaterDispelAt':20,'sealDeadline':'unchanged'}
v=edit('AC6-RX03')
v['actionsAndResolution'][0]+=' This independently captured Lesser Antimagic is rank5 and has no other blocker, so its own termination is automatic, not a rank6+ task.'
v['actionsAndResolution'][1]='In a separate branch where the field is still active, inside Wizard class Dispel is a rank3 spell application and is suppressed before its task; its legally committed3RP/Recharge2 are spent. Do not place this branch after the field already ended.'

# Preserve actual one-foot wall volume, not only its middle-plane cross-section.
v=edit('PB-D03')
v['initialState']='Planar Barrier occupies x[-15,15],y[-0.5,0.5],z[0,15], a one-foot-thick vertical wall divided into eighteen fixed5x5x1 panel volumes. Lesser Antimagic is the actual radius10 sphere centered(0,0,5) fromt12..18, with no center-LoE clipping inside this wall region. A qualifying Large body occupies x[-5,5],y[-5,5],z[0,10] while suppression is active.'
v['actionsAndResolution'][0]='At12 the exact suppressed volume is the intersection of the wall with x^2+y^2+(z-5)^2<=100. On the middle plane y=0 only, the cross-section is x^2+(z-5)^2<=100. The omitted y^2 term must not be used for the whole one-foot thickness.'
v['actionsAndResolution'][1]='The body has positive-volume interior overlap with exactly four fixed panels: x[-5,0]/[0,5] crossed with z[0,5]/[5,10], each across y[-0.5,0.5]. The farthest corner of each of those panels from the sphere center has squared distance25+0.25+25=50.25<100, so each of those complete four panel volumes was suppressed. Mere face/edge contact with neighboring panels does not count as occupying their interiors.'
v['actionsAndResolution'][2]='At18, the four recorded central suppressed panel volumes still overlap the qualifying body and remain absent until clear. Other clear suppressed portions return with their exact curved3D clipping boundaries; portions outside the sphere were always operative. Pending portions retain their recorded geometry rather than shrinking into a newly chosen tactical hole.'
v['geometryLedger'].update(wall='x[-15,15],y[-0.5,0.5],z[0,15]',panelVolumeFeet=[5,1,5],sphereEquation='x^2+y^2+(z-5)^2<=100',centralPanelMaximumSquaredRadius=50.25,occupancy='positive-volume interior overlap; mere boundary contact is not occupation')

bar=m['spells'][4]['procedure'];m['spells'][4]['local06PreviousCurrentVersion']=copy.deepcopy(oldm['spells'][4])
bar['physicalCrossing']+=' CURRENT EXPLICIT VERTICAL-FALL EXCEPTION: apply fallingAndPlacement below when gravity carries a body down through a top/bottom edge; the wall supplies no horizontal supporting face. This exception does not authorize lateral passage through an otherwise operative broad vertical face.'
bar['fallingAndPlacement']+=' NEW explicit completion for the existing no-platform promise: downward Falling through a top/bottom edge is not stopped by this selective wall. If that lawful vertical entry creates actual interior body overlap with a fixed panel, mark the whole intersected panel pending until qualifying bodies clear, exactly as for qualification-change occupancy. Other operative panels still block lateral crossing. A lateral forced movement component toward an operative face stops at its boundary while the independent unsupported vertical fall keeps its original marker/distance history. No support, extra save, impact damage or new Fall Marker is supplied by the wall itself.'
bar['currentPanelPrecision']+=' For pending-panel occupancy use actual positive-volume interior overlap. Merely touching a neighboring panel face/edge does not occupy that panel. The one-foot wall thickness participates in spherical clipping; y=0 diagrams are cross-sections only.'
v=edit('PB-D06')
v['actionsAndResolution'][0]='An unsupported qualifying body falls vertically down through the top edge of the one-foot wall volume. The explicit vertical-Falling exception supplies no horizontal support and cannot suspend its original Fall Marker. Actual interior-overlapped panels become pending until clear; this is a recorded consequence of body occupancy, not a selected hole.'
v['actionsAndResolution'][1]='A separately legal lateral push toward another operative vertical panel stops that lateral component at its boundary. Unsupported vertical Falling continues along its actual trajectory using the same fall-distance history; the wall supplies no additional save or damage.'
v['sourceRefs'].append(ref('SPELLS_MODEL.json','/spells/4/procedure/fallingAndPlacement','proposed explicit no-platform vertical-entry completion'))

# Restore materially omitted original obligations under their existing identities.
append_original('GA-D02')
append_original('GA-D03')
cases['GA-D03']['clockLedger']={'nullZero':100,'heal':110,'expiry':3600}
cases['GA-D03']['costLedger'].update(clericRpBefore=3,healingRiteRp=2,clericRpAfter=1)
cases['GA-D03']['geometryLedger']={'healingDistanceFeet':20,'actualPerceptionAndLoE':True}
append_original('GA-D04')
append_original('GA-D06')
append_original('GA-D05')
append_original('NX-D01')
cases['NX-D01']['costLedger'].update(wizardRpBefore=30,wizardDivination6RpAfter=17,druidRpBefore=30,druidConjuration8RpAfter=9)
append_original('NX-D02')
append_original('NX-D05')
v=edit('NX-D06')
v['initialState']='Conjuration8 Nexus formed at0 with600-second deadline. An actual inseparable carrier/passenger group fits the live10x15 mouth and its whole receiving footprint; it has5ft available movement. A hidden accepted Dimensional Anchor covers one destination body footprint at the transition checkpoint after valid commitment. The actual Anchor is an endpoint blocker, not a portal-formation prohibition.'
v['actionsAndResolution']=[
 'The legally committed crossing spends the real5ft movement. At endpoint revalidation, one transported creature is blocked by the hidden Anchor. The inseparable group transaction remains entirely at origin: no carrier, passenger, pack or partial body arrives.',
 'The spent5ft is not refunded; Anchor supplies no new substitute receiving space. Both live mouths and the original600-second source deadline remain.',
 'Later actual removal of Anchor permits only a future independently legal transit with its own available movement. It does not replay the failed crossing for free.'
]
v['costLedger']['failedCrossingMovementFeet']=5;v['originalScenarioRestoration']={'inputExampleId':'NX-D06'}
append_original('NX-D07')
cases['NX-D07']['clockLedger'].update(firstCompletedTransitSecond=599,expiryBeforeSecondAttempt=600)
append_original('NX-D08')
cases['NX-D08']['geometryLedger'].update(physicalRouteToEntranceFeet=20,physicalRouteAfterExitFeet=30,totalActualAttackRangeFeet=50)
append_original('NX-D10')
cases['NX-D10']['initialState']='Conjuration8 parent N1 and an independently eligible other caster Nexus N2 are live. Lesser Antimagic covers N1 origin mouth only. A matching creature elsewhere on the real destination plane creates a roll with its local benefit unsuppressed. In the separate termination step, Wizard11 INT18/PB4 stands on that destination plane and casts Greater Dispel from an unsuppressed location with a perceived legal center within30ft and a30ft-radius capture reaching N1 remote mouth with center LoE; N2 has no captured manifestation in that snapshot.'
append_original('NX-D11')
append_original('PB-D05')

v=edit('AC6-N20')
v['initialState']='Wizard11 W INT18/PB4, CON+2, AC15, HP50/50, no Veil, Wounds, damage mitigation or other concentration modifier, maintains Skybrand createdt0 with originaldeadline60. W is at(0,0), the blade starts(10,0), perceived ally-of-Soldier target A is at(35,0), and perceived target B at(45,0); all attack/command paths are clear and targets have no interfering conditions. A has AC18. No round1 command was issued. Round2 W has BA/offense available and declares blade movement20ft to(30,0), attackA, then remaining10ft to(40,0), attackB. Hostile Medium Soldier10 Artillerist on its preceding regular turn spent Action to Ready its actually selected Net Bolt after Skybrand first attack against ally A fully resolves, whether hit or miss. Soldier has real cartridge, unused encounter use, available Reaction and+7 attack, with W perceived within30ft/LoE before its next regular START.'
v['actionsAndResolution']=[
 'Round1 without a command the noncreature blade stays at(10,0); it receives no autonomous defensive movement, Dodge or attack.',
 'Round2 W spends one BA and the one shared offensive allowance. In the attached phase the blade spends20ft of its30ft route to(30,0), within5ft of A. First attack natural7+8=15 missesAC18 and deals0. The miss still completes the declared attack and refunds no offensive allowance.',
 'That perceivable completed attack triggers Soldier Ready. Soldier spends the actual Reaction, one cartridge and1/encounter Net Bolt use; natural12+7=19 hits W AC15. S2 damage2d4 faces[2,3]=5 bludgeoning reduces W50->45; W becomes Restrained under the real Medium-target rider.',
 'W makes concentration save DCmax(10,floor(5/2))=10; natural4+CON2=6 fails. No Wound modifier applies: W remains above0 and2*5<50. Skybrand ends immediately before its remaining10ft movement or attackB.',
 'Unused movement and the absent second attack are lost; no command/offense is transferred to another companion and no saleable sword remains. A later new cast must pay real Action/RP and retains already-spent numbered-round owner allowances.'
]
v['geometryLedger']={'W':[0,0],'bladeInitial':[10,0],'A':[35,0],'B':[45,0],'declaredMovement':[20,10],'firstAttackOrigin':[30,0],'unusedPlannedSecondOrigin':[40,0],'actualMovementSpent':20,'unusedMovementLost':10,'soldierToW':'<=30ft, clear real LoE'}
v['originalScenarioRestoration']={'inputExampleId':'AC6-N20','retainedRepair04Addition':'Actual readied Net Bolt supplies the originally unspecified lawful interruption; first attack restored to the original miss.'}

v=edit('AC6-RX01')
v['initialState']+=' All three actual bodies are already supported on the ground, with no cargo capacity/hand conflict or intervening displacement; Air Pet is not airborne in this distinct fixture. The source-owner concentration predicates remain satisfied.'
v=edit('AC6-N04')
v['initialState']=v['initialState'].replace('Conditional AC5 comparison:','Accepted AC5 interface fixture:')

issues=[
 {'id':'AC6-L06-01','origin':'actual GPT Current05 review','cases':['AC6-N15'],'finding':'Readied spell area selection belongs at release, not preparation.','resolution':'Use exact separately numbered GPT Director replacements for preparation/release. The REVIEW.json pointer1 replacementText accidentally contains the release text; do not apply that ambiguous field blindly.'},
 {'id':'AC6-L06-02','origin':'independent current/source review','cases':['AC6-N19'],'finding':'First Null hit leaves the ordinary target Unconscious/Prone at0. Adjacent second melee spell hit cannot be declared noncritical; it uses advantage and adds two death failures.','resolution':'Explicit Skybrand origin bridge; advantage[7,11], critical2d12[2,3]=5, failures2/successes0. Caster remains dealer; Veil purge still separates the two roots.'},
 {'id':'AC6-L06-03','origin':'independent original/current comparison','cases':['AC6-N01','AC6-N02'],'finding':'Blast full22 damage lost its required failed DEX result; outside class Dispel lost explicit paid-failure accounting.','resolution':'Restore enemy/perception predicate and failed save; outside class Dispel spends3RP/Recharge2 without task or refund.'},
 {'id':'AC6-L06-04','origin':'independent accepted AC5 comparison','cases':['AC6-N10','AC6-RX03'],'finding':'Rank5 Lesser Antimagic is automatically removed by accepted Greater Dispel; no higher-rank task is required. Current interval also needs actual early termination distinguished from planned end.','resolution':'Automatic F1 termination at20; immutable suppressed Seal/P operations do not replay. Distinguish separate still-suppressed class-Dispel branch.'},
 {'id':'AC6-L06-05','origin':'independent geometry review','cases':['PB-D03'],'finding':'A y=0 circle alone omits the one-foot wall thickness; contact versus occupied adjacent panels was implicit.','resolution':'Use full x^2+y^2+(z-5)^2 sphere intersection with y[-0.5,0.5]; four interior-overlapped central panels entirely suppressed, farthest squared radius50.25. Explicit panel-occupancy clarification remains proposed.'},
 {'id':'AC6-L06-06','origin':'independent procedure/case comparison','cases':['PB-D06'],'finding':'General physical-crossing language could stop a fall at the top edge and contradict the explicit no-platform example.','resolution':'Proposed explicit vertical-Falling exception and occupied-panel pending treatment; other operative vertical faces still stop lateral crossing. Requires joint agreement.'},
 {'id':'AC6-L06-07','origin':'all51 original scenario comparison','cases':['GA-D02','GA-D03','GA-D04','GA-D05','GA-D06','NX-D01','NX-D02','NX-D05','NX-D06','NX-D07','NX-D08','NX-D10','NX-D11','PB-D05','AC6-N20'],'finding':'Several current IDs retained titles but lost material original scenarios: actual Load rejection/healing quantities, Null expiry and used-command preservation, locked alignment changes, destination residents/origin exclusion, atomic group paid failure,599/600 closure,20+30 range, remote-mouth removal/other Nexus, and Large receiving depth. N20 lost the original no-command/miss/movement setup.','resolution':'Restore those exact source-compatible original obligations in current cases while retaining newer legal-source work. Original archives/histories are intact; this is a current coverage repair, not recovery of deleted data.'},
 {'id':'AC6-L06-08','origin':'independent fixture clarification','cases':['AC6-RX01','AC6-N04'],'finding':'Three-summon pause example did not state support, and current AC5 comparison still had obsolete conditional label.','resolution':'State grounded body fixture to avoid implied airborne Hover persistence; relabel accepted AC5 comparison without changing rules.'}
]
newid='DD-AC6-SEMANTIC-CURRENT-06';m['moduleId']=newid;c['moduleId']=newid;r['moduleId']=newid
m['status']='Complete semantic correction candidate, unadopted pending joint review';r['reviewStatus']=m['status']
m['local06Corrections']=issues;r['local06Corrections']=issues
provenance={'priorCurrentFiles':[info(p,p.name) for p in sorted(P.iterdir())],'actualGptReview':info(A/'DD_AC6_Local_Current_05_Review.zip'),'actualReviewJson':info(A/'ac6-local-current-05-review/REVIEW.json')}
m['local06Provenance']=provenance;r['local06Provenance']=provenance
r['newScopedRules'].append({'id':'AC6-SKYBRAND-ORIGIN-06','status':sky_rule['classification']})
r['caseScenarioCoverage']=[{'caseId':v['id'],'originalInputPointer':'/currentExamples/'+str(i),'currentCasePointer':'/cases/'+str(next(j for j,x in enumerate(c['cases']) if x['id']==v['id'])),'reviewStatus':'Current scenario read against preserved original; known corrections included in Current06, awaiting joint review.','local06Changed':v['id'] in changed} for i,v in enumerate(orig['currentExamples'])]
O.mkdir()
dump(O/'SPELLS_MODEL.json',m);dump(O/'CASEBOOK.json',c);dump(O/'REGISTER.json',r)
(O/'SOURCE_HASHES.json').write_bytes((P/'SOURCE_HASHES.json').read_bytes())
for name in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:
 t=(P/name).read_text(encoding='utf8')
 for i in [4,9]:
  old=oldm['spells'][i]['procedure'];new=m['spells'][i]['procedure']
  pairs=list(zip(old.values(),new.values())) if isinstance(old,dict) else [(old,new)]
  for before,after in pairs:
   if before!=after:assert t.count(before)==1;(None)
   if before!=after:t=t.replace(before,after,1)
 marker='\n### AC6-COMPANION-01' if name=='PLAYER_CHAPTER.md' else '\n## AC6-COMPANION-01'
 assert marker in t
 t=t.replace(marker,'\n\n### AC6-SKYBRAND-ORIGIN-06\n\n'+sky_rule['classification']+'\n\n'+'\n\n'.join(sky_rule['rule'])+'\n'+marker,1)
 t=t.replace('— Local Current 05 Player Procedures','— Semantic Current 06 Player Procedures').replace('— Local Current 05 Director Review','— Semantic Current 06 Director Review')
 if name=='DIRECTOR_REVIEW.md':
  # Replace old rendered N15 text in place, preserving the whole prior chapter separately.
  old15=next(x for x in oldc['cases'] if x['id']=='AC6-N15')
  for idx in [2,3]:assert old15['actionsAndResolution'][idx] in t;t=t.replace(old15['actionsAndResolution'][idx],cases['AC6-N15']['actionsAndResolution'][idx],1)
  t+='\n\n# Semantic Current06 corrections\n\nThese current corrections remain unadopted pending joint review. Prior chapter bytes are preserved unchanged.\n\n'
  for item in issues:t+='## '+item['id']+'\n\n'+item['finding']+'\n\n'+item['resolution']+'\n\n'
  for cid in changed:
   if cid=='AC6-N15':continue
   v=cases[cid];t+='## '+cid+' — current corrected example\n\n'+v['initialState']+'\n\n'
   t+='\n\n'.join(str(i)+'. '+a for i,a in enumerate(v['actionsAndResolution'],1))+'\n\n'+v['outcome']+'\n\n'
 (O/name).write_text(t,encoding='utf8')
(O/'VERDICT.md').write_text('# AC6 Semantic Current06 — awaiting joint review\n\nIntegrates the actual Current05 GPT Ready correction plus independent condition, save, dispel, volumetric geometry and original-scenario coverage findings. The14 spell identities/16 placements,103 frozen sources,22 original texts and55 ordered cases remain. Every changed current case/procedure and the full Current05 files are preserved.\n\nSkybrand spatial-attack clarification and the explicit Planar Barrier vertical-Falling/occupancy completion require joint agreement. No exact acceptance, spell adoption, runtime execution, human playtesting, balance, cosmology canon, full-game closure or publication is claimed.\n',encoding='utf8')
manifest={'schemaVersion':'6.0','moduleId':newid,'status':'unadopted current semantic correction candidate','frozenSourceCount':103,'identityCount':14,'placementCount':16,'historicalTextCount':22,'currentCaseCount':55,'changedCaseIds':changed,'priorProvenance':provenance,'runtimeTestsExecuted':False,'humanPlaytested':False,'balanceApproved':False,'files':[]}
for p in sorted(O.iterdir()):b=info(p,p.name);manifest['files'].append({'name':b.pop('path'),**b})
dump(O/'EVIDENCE_MANIFEST.json',manifest)
sourcepaths=[ac5,ac4,conditions,core,combat,null,'DescentReviewChanges/ReviewBible/data/playtest/blacksmithing_recipe_candidate.json','DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json','DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json','DescentReviewChanges/ReviewBible/data/public/class_playtests/soldier.json']
frozen={b['path']:b for b in read(I/'SOURCE_MANIFEST.json')['bindings']};bindings=[]
for path in sourcepaths:
 b=info(G/path);assert b['bytes']==frozen[path]['bytes'] and b['sha256']==frozen[path]['sha256'];bindings.append(b)
report={'id':'AC6-CURRENT05-SUBSTANTIVE-REVIEW-06','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'priorCandidateBindings':provenance['priorCurrentFiles'],'actualGptReview':provenance['actualGptReview'],'reviewedCurrentProcedures':[s['id'] for s in oldm['spells']],'reviewedCurrentCaseIds':[v['id'] for v in oldc['cases']],'comparedOriginal51Ids':[v['id'] for v in orig['currentExamples']],'sourceBindingsCheckedAgainstFrozenCopies':bindings,'findings':issues,'newCandidateDirectory':O.relative_to(G).as_posix(),'changedCaseIds':changed,'scope':'All14 current procedures (both Nexus modes), all55 current case texts and all51 original scenario texts read and compared. Source-specific checks focused on the cited rules and repaired examples. This is substantive authored review, not runtime execution or a claim that every possible interaction has been tested. Known findings are repaired provisionally in Current06 and still require independent checks and joint review.','sourceInformationDeleted':0,'newSpellAdoptions':0,'fullSemanticClosure':False,'runtimeTestsExecuted':False,'humanPlaytested':False,'balanceApproved':False}
dump(report_path,report)
print(json.dumps({'candidate':str(O),'changedCases':len(changed),'findings':len(issues),'report':info(report_path),'newSpellAdoptions':0}))
