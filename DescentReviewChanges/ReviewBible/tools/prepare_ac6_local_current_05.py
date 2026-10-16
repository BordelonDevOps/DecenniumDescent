"""Preserve the actual GPT Repair04 return and prepare a bounded joint-review correction.

This creates an unadopted candidate; it does not change accepted spells or counts.
"""
import copy
import hashlib
import json
import math
import zipfile
from datetime import datetime, timezone
from pathlib import Path

G = Path(r'C:\Github\DecenniumDescent')
A = G / 'docs/audit/2026-10-08/full-game'
R = G / 'DescentReviewChanges/ReviewBible'
P = A / 'ac6-repair-04-return'
P3 = A / 'ac6-full-review-03-return'
I = A / 'ac6-full-current-review-03-input'
O = A / 'ac6-local-current-05'
NAMES = ['REGISTER.json', 'SPELLS_MODEL.json', 'PLAYER_CHAPTER.md', 'DIRECTOR_REVIEW.md',
         'CASEBOOK.json', 'SOURCE_HASHES.json', 'VERDICT.md', 'EVIDENCE_MANIFEST.json']

def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b): return hashlib.sha256(b).hexdigest()
def binding(p, name=None):
    b = p.read_bytes()
    return {'path': name or p.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': sha(b)}
def dump(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
def ref(path, pointer, role):
    return {'path': path, 'pointer': pointer, 'role': role,
            'authority': 'current authored candidate' if path == 'SPELLS_MODEL.json' else 'frozen source'}

assert not O.exists(), 'One-shot preparation: preserve existing output rather than overwrite.'
for path, expected in [(A/'DD_AC6_Repair_04_Return.zip', 'a9a32823acc03843f3aa4f947182d0c4ebeb25312cc26258a964adcb674656fa')]:
    assert sha(path.read_bytes()) == expected
before = {n: binding(P/n, n) for n in NAMES}
old_model = read(P/'SPELLS_MODEL.json'); model = copy.deepcopy(old_model)
old_cases = read(P/'CASEBOOK.json'); cases = copy.deepcopy(old_cases)
reg = read(P/'REGISTER.json')
case_by_id = {c['id']: c for c in cases['cases']}
ac5_path = 'DescentReviewChanges/ReviewBible/data/public/spell_candidates/abjuration_conjuration_rank5_reviewed_05.json'
combat_path = 'DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md'
integration_path = 'DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md'

geometry_rule = {
    'classification': 'NEW source-specific Chain Arc successor geometry; proposed for joint review, not a global range amendment',
    'rule': [
        'Use the actual occupied body volumes in the pre-damage snapshot for every size, including Medium, Large and the caster. A successor is in local range only if one point on the previous body and one point on the candidate body are at most30feet apart AND the straight segment connecting that same pair has actual clear line of effect on the same actual plane. Do not combine the distance of a blocked pair with the line of effect of a different out-of-range pair. Do not mix center measurements for smaller creatures with nearest-body measurements for larger ones.',
        'Include each unvisited qualifying actual creature identity exactly once, including allies, unseen bodies and the caster. Exclude already visited identities, objects, corpses and images. Stable preexisting identity order precedes each fair draw. This is only the successor test: the initial declared target still needs its actual60foot range, caster perception and line of effect.',
        'Bodies have extent. The60foot initial range and five30foot jumps bound their respective targeting gaps, not a universal center-to-center distance to the last body. No arbitrary remote endpoint or unprinted conductive path is added.'
    ],
    'sourceRefs': [ref('SPELLS_MODEL.json', '/spells/8/completeSourceAndAccess', 'unchanged Chain Arc source/access'),
                   ref('SPELLS_MODEL.json', '/sharedRules/AC6-CHAIN-RANDOM-01', 'unchanged fair-draw and information limits')]
}
model['sharedRules']['AC6-CHAIN-GEOMETRY-05'] = geometry_rule
old_chain = model['spells'][8]['procedure']
new_chain = old_chain.replace(
    "within30feet of the immediately previous selected creature's snapshotted position and with line of effect from it.",
    "meeting AC6-CHAIN-GEOMETRY-05 against the immediately previous selected creature's snapshotted occupied body volume.")
new_chain = new_chain.replace(
    'Its longest theoretical six-body straight sequence is initial60plus five30foot jumps, but every actual hop still needs the snapshotted geometry; no arbitrary farthest endpoint is targeted directly.',
    'Each successive targeting gap is at most30feet under AC6-CHAIN-GEOMETRY-05. Body extent prevents treating initial60plus five30foot gaps as a universal center-to-center endpoint limit. No arbitrary farthest endpoint is targeted directly.')
assert new_chain != old_chain
model['spells'][8]['local05PreviousCurrentVersion'] = copy.deepcopy(old_model['spells'][8])
model['spells'][8]['procedure'] = new_chain

supp = model['sharedRules']['AC6-SUMMON-SUPPRESS-01']
model['sharedRules']['AC6-SUMMON-SUPPRESS-01_local05PreviousCurrentVersion'] = copy.deepcopy(supp)
intersection_rule = ('NEW explicit scope for these three AC6 profiles: while any part of the actual occupied body intersects operative Lesser Antimagic, apply this whole-body suppression lifecycle. Use the field\'s actual clipped volume and re-evaluate as the body moves or falls. This extends the accepted AC5 summon-intersection convention only to Greater Air Pet, Greater Planar Ally and each Faction Army soldier; it does not suppress a whole extended wall/field, grant a new effect to another antimagic source, or change accepted AC5 rules.')
supp['rule'].insert(0, intersection_rule)
supp['sourceRefs'].extend([
    ref(ac5_path, '/spells/0/procedure', 'accepted Lesser Antimagic local intersection and same-family exception'),
    ref(ac5_path, '/sharedRules/AC5-ANTIMAGIC-SUMMON-01', 'accepted AC5 scoped body-intersection convention; AC6 extension is new')])

# Restore the exact return03 version omitted from the return04 NX-D02 history.
nx = case_by_id['NX-D02']
nx['local05PreviousCurrentVersion'] = copy.deepcopy(nx)
assert 'repair04PreviousCurrentVersion' not in nx
nx['repair04PreviousCurrentVersion'] = copy.deepcopy(next(c for c in read(P3/'CASEBOOK.json')['cases'] if c['id']=='NX-D02'))

# A bounded fixture with all actual bodies enumerated. Geometry is recomputed below.
chain_case = case_by_id['AC6-N17']
chain_case['local05PreviousCurrentVersion'] = copy.deepcopy(chain_case)
positions = {'W': [-40,0,0], 'A': [0,0,0], 'B': [10,15,0], 'C': [10,-15,0],
             'F': [25,0,0], 'H': [40,30,0], 'U': [50,0,0], 'D': [80,0,0],
             'E': [110,0,0], 'G': [140,0,0]}
bodies = {}
for ident, p in positions.items():
    width = 10 if ident == 'U' else 5
    bodies[ident] = {'bottomCenterFeet': p, 'sizeFeet': [width,width,width],
                     'min': [p[0]-width/2,p[1]-width/2,p[2]],
                     'max': [p[0]+width/2,p[1]+width/2,p[2]+width]}
def gap(a,b):
    return math.sqrt(sum(max(0,a['min'][i]-b['max'][i],b['min'][i]-a['max'][i])**2 for i in range(3)))
order = sorted(bodies)
selected = ['A']; expected_arrays = [['B','C','F'],['B','C','H','U'],['D','H'],['E'],['G']]
choices = ['F','U','D','E','G']; hops=[]
for expected, chosen in zip(expected_arrays, choices):
    previous = selected[-1]
    distances = {k: gap(bodies[previous], bodies[k]) for k in order if k not in selected}
    actual = [k for k,d in distances.items() if d <= 30]
    assert actual == expected, (previous, actual)
    hops.append({'previous':previous, 'unvisitedDistancesFeet':distances,
                 'completeCandidateArray':actual, 'selected':chosen,
                 'lineOfEffect': 'All candidate distance-minimizing point pairs have a clear segment in this unobstructed fixture.'})
    selected.append(chosen)
chain_case.update({
    'title': 'Complete body-volume candidate sets, fair selection and distinct recipient packets',
    'initialState': 'Wizard W level11 INT18/PB4 has acquired Chain Arc, RP40, Dissonance0, no Veil or price modifiers, spell DC16. W at(-40,0,0) perceives initial A at(0,0,0) within60ft with clear LoE. The ten recorded actual bodies are the entire local population; all are on one actual plane with no intervening barriers. Medium bodies are5x5x5; unseen U alone is Large10x10x10. No concealment blocks the actual arc LoE. F is friendly; A is lightning-immune. Every non-A recipient has no applicable damage prevention, resistance, transfer or Null qualification.',
    'actionsAndResolution': [
        'Commit Action/V/S/F and13RP:40->27. Revalidate initial A after the interruption window, then snapshot every recorded body before any damage. Stable identity order is[A,B,C,D,E,F,G,H,U,W].',
        'From A the complete unvisited local array is[B,C,F]. Director-private fair physical d6:1-2=B,3-4=C,5-6=F; roll5 selects F. W is35ft from A body-to-body and cannot enter this array. H is sqrt(35^2+25^2)>30ft away.',
        'From F the complete array is[B,C,H,U]. Director-private fair d4=4 selects U. F-to-H is sqrt(10^2+25^2)<30ft; F-to-U is17.5ft. U remains one identity across its entire Large body.',
        'From U the complete array is[D,H]. B and C are each sqrt(32.5^2+7.5^2)=33.35416016ft away and are correctly excluded. Director-private fair d2=1 selects D. U-to-D is22.5ft and U-to-H is sqrt(2.5^2+22.5^2).',
        'From D the sole eligible unvisited identity is E at25ft; from E it is G at25ft. Singleton selections need no die. Final sequence[A,F,U,D,E,G] is fixed before damage. No observer perceives the Director-private dice; this fixture offers no eligible Fate Coin replacement or hidden roster readout.',
        'Create the six caster-dealt recipient roots together with actual Veil=false and shared cast lineage. Roll3d8 faces[6,7,6]=19. Resolve the six actual DEX saves and recipient packets recorded below. Immunity, success and HP loss do not revise any candidate array or later selection.',
        'No independently sourced immediate removal occurs in this fixture. A future genuine removal follows its own authority and cannot redraw the established chain; it is a conditional rule, not a claimed executed event.'
    ],
    'costLedger': {'rpBefore':40,'rpSpent':13,'rpAfter':27,'dissonanceBefore':0,'baseDissonanceGain':2,'dissonanceAfter':2,'spellSaveDC':16},
    'clockLedger': {'selection':'All candidate arrays/draws and permitted replacements precede every damage packet.','damageRoots':'All six caster/recipient roots allocated together after final selection; no actual damage is implied by allocation.'},
    'geometryLedger': {'initialRangeMaxFeet':60,'successorGapMaxFeet':30,'bodyVolumes':bodies,'stableIdentityOrder':order,'hops':hops,'finalSequence':selected,'bodyMeasurementRule':'AC6-CHAIN-GEOMETRY-05','allBodiesSameActualPlane':True,'noOtherCreaturesInFixture':True},
    'damageLedger': [
        {'id':'A','dexModifier':0,'natural':12,'total':12,'save':'fail','rolledSharedDamage':19,'damageAfterDefenses':0,'hpBefore':30,'hpAfter':30,'defense':'lightning immunity'},
        {'id':'F','dexModifier':0,'natural':8,'total':8,'save':'fail','rolledSharedDamage':19,'damageAfterDefenses':19,'hpBefore':30,'hpAfter':11},
        {'id':'U','dexModifier':2,'natural':12,'total':14,'save':'fail','rolledSharedDamage':19,'damageAfterDefenses':19,'hpBefore':40,'hpAfter':21},
        {'id':'D','dexModifier':0,'natural':18,'total':18,'save':'success','rolledSharedDamage':19,'damageAfterDefenses':9,'hpBefore':30,'hpAfter':21},
        {'id':'E','dexModifier':1,'natural':7,'total':8,'save':'fail','rolledSharedDamage':19,'damageAfterDefenses':19,'hpBefore':30,'hpAfter':11},
        {'id':'G','dexModifier':1,'natural':17,'total':18,'save':'success','rolledSharedDamage':19,'damageAfterDefenses':9,'hpBefore':30,'hpAfter':21}
    ],
    'outcome': 'Each complete successor array follows one body-volume rule across all sizes; all six distinct roots and actual recipient outcomes remain fixed after selection.',
    'sourceRefs': [ref('SPELLS_MODEL.json','/spells/8/procedure','current full Chain Arc procedure'),ref('SPELLS_MODEL.json','/sharedRules/AC6-CHAIN-GEOMETRY-05','proposed source-specific body geometry'),ref('SPELLS_MODEL.json','/sharedRules/AC6-CHAIN-RANDOM-01','fair draw and hidden information limits')]
})

fall_case = case_by_id['AC6-N15']
fall_case['local05PreviousCurrentVersion'] = copy.deepcopy(fall_case)
fall_case.update({
    'title': 'Same-body Null healing, continuously suppressed descent, fixed slot-end marker and expiry',
    'initialState': 'Wizard W11 INT18/PB4 formed the Greater Air Pet at t0, paying13RP from40->27; original concentration deadline60. The later fixture begins with the already-damaged same Pet at6/65HP, bottom20ft above floor z0. Its actual occupied box is x[-2.5,2.5],y[-2.5,2.5],z[20,25]. Earlier damage is an input state, not a claim that a fresh Pet forms at6HP. At t12 an already legally resolved10-point qualifying Null packet from an actual Veiled character reaches this Pet; the source root/dealer qualification is a supplied fixture input, not a newly invented attack. Cleric K1 WIS16(+3), selected Healing Rite, Recharge0, RP6, is at(-5,0,0) with hands/components, actual perception and clear range to the willing Pet. Independent Wizard C9 INT18/PB4, acquired Lesser Antimagic, RP20, Dissonance0 and no price modifiers, stands on a real supported ledge at(8,0,11); the ledge does not cross the Pet fall column. W stays at(-20,0,0), outside the field, preserving Pet concentration. All stated casters have their actual eligible regular turns and resources; no other effect changes this fixture.',
    'actionsAndResolution': [
        'At t12 the supplied qualifying Null10 packet leaves the same Pet NullDisabled0. Speed0 and inability to act do not themselves suppress its active Hover, so it stays at bottom-height20 with original source/deadline intact.',
        'At t18.5 during K regular turn[18,20], Healing Rite Action pays2RP:6->4. Its1d8 face4 plus WIS3 heals7HP through AC6-HEAL-TARGET-02. NullDisabled ends on that same body. The source maximum65, position, command history and t60 deadline do not reset.',
        'At t20.5 during C regular turn[20,22], C uses Action to Ready the Action-time Lesser Antimagic, choosing the perceived fixed point(0,0,11),8ft away with clear LoE. Pay10RP:20->10, hold concentration, and specify the visible W hand signal as trigger. The Ready deadline is C next actual regular START t26. No prior concentration or spent Reaction blocks this action.',
        'At t24.5 during W regular turn[24,26], W gives the agreed visible hand signal. After that trigger resolves, C spends its available Reaction to release the same paid spell before t26. There is no second spell cast, RP charge or Ready Action. The field establishes its fixed10ft-radius sphere centered(0,0,11), with nominal concentration deadline84.5; its own family exception allows it to remain active while C is inside it.',
        'At t24.5 the Pet intersects the operative sphere. The explicit AC6 whole-body intersection rule suppresses fly/Hover, starting ordinary Falling immediately. The enclosing regular slot ends26 and repeats[30,32] in the next numbered round, so the first fixed Fall Marker is t32, not t30 or merely start+6. No voluntary horizontal movement is granted by Falling.',
        'At every intermediate bottom-height h in[0,20], the unchanged5ft-tall body overlaps the sphere: its nearest z-distance to11 is at most9ft, strictly below radius10. No barrier clips that connecting vertical segment. The Pet remains fully suppressed throughout the actual descent, so Hover cannot resume halfway down.',
        'At t32 the still-suppressed body takes its first ordinary Falling Step, descending20ft to floor z0. Total uncontrolled fall20ft gives min(10,floor(20/20))=1d6 bludgeoning; actual roll3 reduces HP7->4. It lands Prone and Falling ends. It still intersects the sphere and remains Speed0/no source actions.',
        'At t38.5 during C regular turn[38,40], C voluntarily ends concentration on Lesser Antimagic. The same Pet resumes source traits at its actual ground position, HP4 and Prone. There is no teleport back to height20, missed-command replay, HP refill or new body.',
        'At original t60 the independent Pet source expires, ending the body with no corpse or replacement. The prematurely ended antimagic field has no remaining future effect at84.5.'
    ],
    'costLedger': {'petRpBefore':40,'petCastRp':13,'petRpAfter':27,'clericRpBefore':6,'healingRp':2,'clericRpAfter':4,'antimagicRpBefore':20,'antimagicRpPaidAtReady':10,'antimagicRpAfter':10,'releaseRp':0,'releaseReaction':1,'petBaseDissonanceGain':2,'antimagicBaseDissonanceGain':1},
    'clockLedger': {'created':0,'nullZero':12,'healing':18.5,'readyCast':20.5,'readyCasterSlot':[20,22],'readyDeadlineNextStart':26,'release':24.5,'enclosingRegularSlot':[24,26],'sameSlotNextNumberedRound':[30,32],'firstFallMarker':32,'suppression':[24.5,38.5],'antimagicNominalExpiry':84.5,'antimagicActuallyEnded':38.5,'petExpiry':60},
    'geometryLedger': {'petHorizontalBounds':[[-2.5,2.5],[-2.5,2.5]],'bodyHeightFeet':5,'initialBottomHeightFeet':20,'floorZ':0,'sphereCenter':[0,0,11],'sphereRadiusFeet':10,'fieldCasterPoint':[8,0,11],'fieldCenterRangeFeet':8,'fieldCasterSupported':True,'ledgeOutsideFallColumn':True,'fallBottomHeightInterval':[0,20],'maximumNearestSphereCenterToBodyDistanceFeet':9,'uncontrolledFallFeet':20,'impactDice':'1d6=3','landingHp':4,'landingCondition':'Prone','noMidfallHoverRestoration':True},
    'outcome': 'NullDisabled retains active Hover; full body-intersection antimagic removes it. A concrete Ready trigger fixes the enclosing slot and t32 fall marker, with real suppression throughout the same-body20ft descent and independent t60 source expiry.',
    'sourceRefs': [ref('SPELLS_MODEL.json','/sharedRules/AC6-SUMMON-SUPPRESS-01','proposed explicit AC6 whole-body suppression'),ref('SPELLS_MODEL.json','/sharedRules/AC6-HEAL-TARGET-02','scoped existing body healing'),ref('SPELLS_MODEL.json','/spells/6/procedure','Greater Air Pet full source lifecycle'),ref(ac5_path,'/spells/0/procedure','accepted Lesser Antimagic'),ref(ac5_path,'/sharedRules/AC5-ANTIMAGIC-SUMMON-01','accepted AC5 intersection convention, proposed AC6 extension'),ref('DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json','/cards/12','actual Healing Rite card'),{'path':combat_path,'section':'Ready / concentration / regular slots / Hover','role':'actual Action and Reaction release with deadline','authority':'frozen source'},{'path':integration_path,'section':'Falling bridge — new provisional procedure','role':'fixed next-round slot-end marker and impact formula','authority':'frozen source'}]
})

corrections = [
    {'id':'AC6-L05-01','type':'preservation repair','change':'NX-D02 now retains the exact superseded return03 case, including old references, in repair04PreviousCurrentVersion. The exact return04 case is also retained. No current NX-D02 adjudication changes.'},
    {'id':'AC6-L05-02','type':'NEW bounded rule plus example correction','change':'AC6-CHAIN-GEOMETRY-05 makes successor measurement consistent for all occupied bodies and same-pair LoE. AC6-N17 enumerates all ten bodies, every complete candidate array, fair draw, six actual saves and HP outcomes. The unsupported universal endpoint-center bound is removed.'},
    {'id':'AC6-L05-03','type':'NEW explicit AC6 suppression scope','change':'AC6-SUMMON-SUPPRESS-01 explicitly applies whole-body suppression when any part intersects operative Lesser Antimagic, matching the accepted AC5 convention only for the three AC6 summon profiles. Other source/extended-area rules remain unchanged.'},
    {'id':'AC6-L05-04','type':'concrete timing and geometry repair','change':'AC6-N15 now uses actual Ready preparation, trigger and Reaction, separate source clocks, enclosing24..26 regular slot and next-round32 fall marker, a field intersecting the Pet throughout descent, and paid legal Healing Rite. Its Null packet and previously damaged HP are explicitly supplied input states, not newly invented attacks.'}
]
provenance = {'priorReturnArchive':binding(A/'DD_AC6_Repair_04_Return.zip'),
              'priorEightFiles':list(before.values()),
              'return03ArchiveForMissingHistory':binding(A/'DD_AC6_Full_Review_03_Return.zip'),
              'independentReturn04Check':binding(A/'AC6_REPAIR_04_INDEPENDENT_STRUCTURAL_CHECK.json')}
model['local05Corrections'] = corrections
model['local05Provenance'] = provenance
model['moduleId'] = 'DD-AC6-LOCAL-CURRENT-05'
model['status'] = 'Complete local correction candidate for joint review; no exact acceptance or adoption claimed'
reg['moduleId'] = model['moduleId']; reg['reviewStatus'] = model['status']
reg['local05Corrections'] = corrections; reg['local05Provenance'] = provenance
reg['newScopedRules'].append({'id':'AC6-CHAIN-GEOMETRY-05','status':geometry_rule['classification']})
reg['preservation']['return04AllEightFilesRetainedUnchanged'] = True
reg['preservation']['return04ChangedCurrentCasesRetainedExactly'] = True
reg['preservation']['missingNXD02Return03HistoryRestored'] = True
cases['moduleId'] = model['moduleId']

O.mkdir()
dump(O/'SPELLS_MODEL.json', model);dump(O/'CASEBOOK.json', cases);dump(O/'REGISTER.json', reg)
(O/'SOURCE_HASHES.json').write_bytes((P/'SOURCE_HASHES.json').read_bytes())
shared_geometry_md = '\n\n### AC6-CHAIN-GEOMETRY-05\n\n' + geometry_rule['classification'] + '\n\n' + '\n\n'.join(geometry_rule['rule']) + '\n'
for name in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:
    text = (P/name).read_text(encoding='utf8')
    assert text.count(old_chain) == 1
    text = text.replace(old_chain,new_chain)
    needle = '- ' + old_model['sharedRules']['AC6-SUMMON-SUPPRESS-01']['rule'][0]
    assert needle in text
    text = text.replace(needle,'- '+intersection_rule+'\n- '+old_model['sharedRules']['AC6-SUMMON-SUPPRESS-01']['rule'][0],1)
    marker = '\n### AC6-COMPANION-01' if name == 'PLAYER_CHAPTER.md' else '\n## AC6-COMPANION-01'
    assert marker in text
    text = text.replace(marker,shared_geometry_md+marker,1)
    text = text.replace('— Repair 04 Player Procedures','— Local Current 05 Player Procedures').replace('— Repair 04 Director Review','— Local Current 05 Director Review')
    if name == 'DIRECTOR_REVIEW.md':
        text += '\n\n# Local Current 05 Corrections\n\nThese corrections remain unadopted pending joint review.\n\n'
        for item in corrections:text += '## '+item['id']+'\n\n'+item['change']+'\n\n'
        for cid in ['AC6-N15','AC6-N17']:
            c=case_by_id[cid]
            text += '## '+cid+' — '+c['title']+'\n\n'+c['initialState']+'\n\n'
            text += '\n\n'.join(str(i)+'. '+v for i,v in enumerate(c['actionsAndResolution'],1))+'\n\n'+c['outcome']+'\n\n'
    (O/name).write_text(text,encoding='utf8')
(O/'VERDICT.md').write_text('# AC6 Local Current 05 — awaiting joint review\n\nThis complete fourteen-identity/sixteen-placement candidate retains the103 frozen sources,22 historical texts,55 ordered current cases and the complete actual GPT Repair04 return. It corrects missing NX-D02 history, proposes consistent Chain Arc body-volume geometry, and makes the Air Pet antimagic/Falling fixture concrete.\n\nAC6-L05-01 through04 require GPT review. No exact acceptance, spell adoption, full semantic closure, runtime execution, human playtesting, balance, cosmology canon, whole-game completion or publication is claimed.\n',encoding='utf8')
manifest = {'schemaVersion':'5.0','moduleId':model['moduleId'],'status':'unadopted local correction candidate',
            'frozenSourceCount':103,'identityCount':14,'placementCount':16,'historicalTextCount':22,'currentCaseCount':55,
            'priorReturnProvenance':provenance,'localCorrections':corrections,
            'runtimeTestsExecuted':False,'humanPlaytested':False,'balanceApproved':False,
            'files':[dict(name=n,**{k:v for k,v in binding(O/n,n).items() if k!='path'}) for n in NAMES if n!='EVIDENCE_MANIFEST.json']}
dump(O/'EVIDENCE_MANIFEST.json',manifest)
assert before == {n: binding(P/n,n) for n in NAMES}, 'Actual GPT return must remain byte-identical.'
print(json.dumps({'output':str(O),'files':[binding(O/n,n) for n in NAMES],'newSpellAdoptions':0},ensure_ascii=False))
