"""Prepare three exact example repairs beside the unchanged corrected AC4 rules."""
from datetime import datetime,timezone
from zipfile import ZipFile,ZIP_DEFLATED
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    source=A/'ac4-corrections-02-return';root=A/'ac4-exact-case-patch-03';archive=A/'DD_AC4_Exact_Case_Patch_03.zip';receipt=A/'AC4_EXACT_CASE_PATCH_03_PREPARATION.json'
    assert not any(p.exists() for p in [root,archive,receipt])
    replacement={
      'AC4-X01':"Exact comparison: Wizard A (class7, PB3, INT+4, spell attack+7, current RP20, current HP8/max30, AC12, no tempHP or acid defense) has ordinary Acid Arrow legally prepared and remains under unsuppressed Null Veil throughout this fixture. B, 20ft away with line of effect, has one active Spell Shield and a Reaction; return range30ft and targeting are legal. A commits rank2 Acid Arrow, pays its base3RP (RP20 to17; no extra price modifiers), and applies its actual casting hooks. After the legal interruption window B spends its Reaction and the shield to redirect the same pending spell. Spell Shield creates no replacement damage root and does not advance the original spell's real root checkpoint. A remains caster/dealer. The returned ranged attack rolls12+7=19 against A's AC12 and hits; initial4d4=10 acid. At the original damage-root creation checkpoint A is Veiled, so that actual root is nullNonlethal. With no defenses/tempHP, A reaches Stable0 rather than damage-caused death/Wounds; establish the ordinary one Stable recovery deadline. The same continuing A identity receives Acid Arrow's finite2d4 delayed rider, due at A's first future regular END excluding the current turn. When that rider deals5 acid at its proper marker, it inherits the original root flag and leaves already-Stable0 A with the same recovery deadline, even if Veil has ended after root creation. No second cast, payment, reflection, target or root is created by Shield. Boundary comparison at the existing root checkpoint: with an un-Veiled original dealer at creation, that root is ordinary; later Veil gain cannot rewrite it. If an independently completed lawful event changes Veil before actual root creation, use the then-current dealer state. This comparison grants no new event window and does not equate cast commitment with root creation.",
      'AC4-X08':"Exact waiver comparison: Wizard20 W has Grand Reservoir available (one/long rest), RP10, and Greater Warding recorded in its spellbook at its legal Wizard rank4/base7RP. W is inside one active Dampening Field at actual legal cast commitment, with final Resonance Influence Ease and no strain surcharge, consumed material or other price modifier. W uses Grand Reservoir for that legal Action cast: its exact source waives only base7RP, leaving ordinary price0; the field adds mandatory2RP; final Ease subtracts1, producing final1RP. W commits its Action, Grand Reservoir use and1RP (10 to9), then applies actual casting/concentration/strain hooks; no prohibited Overcast/Fusion/Dual Cast/refund combination is used. A normal unwaived rank4/base7 cast in the same conditions costs7+2-1=8RP. Ritual comparison: Wizard Ritual Casting only applies to an actually eligible Ritual-tagged spell and keeps its extra at-least10-minute time, no-encounter completion and exact no-normal-Dissonance rule; field eligibility is evaluated at actual legal CAST COMMITMENT, never newly at ritual resolution or an ongoing pulse. A field that begins only after that commitment adds no retroactive price. A genuine charge-only/free spell activation, if independently available under its own source, still acquires the scoped2RP payment plus its real charge/use; this example grants no item or spell access. A no-RP-pool actor cannot pay a positive final price. Actual Cleric Healing Rite is a class technique (Action2RP), not automatically an ordinary/class spell, so merely spending RP does not incur the field surcharge. Master of Winter's current authored bounded weather invocation replaces the undefined historical free high-rank Control Weather permission; it is not used here as evidence that the character casts the ordinary Control Weather spell for free.",
      'AC4-X09':"Exact comparison: Wizard7 owner O previously legally cast Summon Spectral Steed (rank3/base5RP, with no price modifiers; RP20 to15) and maintains its original one-minute concentration, with24seconds remaining. The Large steed carries one willing Medium rider: effective body160lb/6Load plus real noncreature gear20lb/2Load =180lb/8Load, within both350lb/12Load caps. At8Load it is Burdened, so walking Speed60 becomes50ft with the actual burden penalties; this does not add or remove a Planar Crossing use. Mounting and current rider position were already legally established. O starts its regular turn with the steed30ft away and able to perceive O. O spends the one shared Bonus Action command for Planar Crossing to a specific personally known site on another plane. In its attached phase immediately after O's regular turn, the steed spends its Action and its one remaining crossing attempt (1 to0) at attempt start. Unknown to O, another caster's already-active Dimensional Anchor covers the destination footprint. At resolution that endpoint is blocked, so the whole steed+rider+permitted-gear transaction remains at origin; original rider position and real cargo are preserved. Command, Action, crossing use and previous cast price are not refunded; no hidden reason or coordinates are revealed. The original concentration deadline continues. There is no mid-resolution cast, free interrupt or cross-plane perception. Control: an otherwise legal same-plane teleport with both endpoints outside an Anchor is not blocked merely because an imaginary straight line crosses its sphere."
    }
    old=read(source/'CASEBOOK.json');new=read(source/'CASEBOOK.json');changes=[]
    for i,c in enumerate(new['cases']):
        if c['id'] in replacement:
            changes.append({'id':c['id'],'pointer':f'/cases/{i}/currentAdjudication','old':c['currentAdjudication'],'replacement':replacement[c['id']]})
            c['currentAdjudication']=replacement[c['id']]
    assert len(changes)==3 and len(new['cases'])==48
    for b,a in zip(old['cases'],new['cases']):
        assert b['id']==a['id']
        if b['id'] not in replacement:assert b==a
        else:assert {k:v for k,v in b.items() if k!='currentAdjudication'}=={k:v for k,v in a.items() if k!='currentAdjudication'}
    original=read(A/'ac4-current-review-01-input/CURRENT_REVIEW_INPUT.json')
    for b in original['sourceBindings']:assert info(G/b['path'])==b
    root.mkdir();candidate=root/'candidate';candidate.mkdir()
    for p in source.iterdir():(candidate/p.name).write_bytes(p.read_bytes())
    (candidate/'CASEBOOK.json').write_bytes(encoded(new))
    manifest=read(candidate/'EVIDENCE_MANIFEST.json')
    for b in manifest['outputFiles']:
        if b['path']=='CASEBOOK.json':b.update({k:v for k,v in info(candidate/'CASEBOOK.json').items() if k!='path'})
    (candidate/'EVIDENCE_MANIFEST.json').write_bytes(encoded(manifest))
    payloads=[{'name':p.name,**info(p)} for p in sorted(candidate.iterdir())]
    reg={'id':'AC4-EXACT-CASE-PATCH-03','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'UNSUBMITTED exact example-only repair for actual joint approval',
      'priorActualReturn':info(A/'DD_AC4_Corrections_02_Return.zip'),'sourceCheck':info(A/'AC4_CORRECTIONS_02_RETURN_SOURCE_CHECK.json'),
      'independentSemanticAssessment':'All corrected15 procedures/shared interfaces and complete Envoy profile read against prior return and sources. C01..C08 rule changes are coherent as scoped provisional authorship. X08 and X09 contain source-example errors; X01 is restored to a concrete current Acid Arrow example. No model/profile/chapter rule text changes are proposed here.',
      'changes':changes,'unchangedCandidateFiles':[p.name for p in candidate.iterdir() if (source/p.name).read_bytes()==p.read_bytes()],
      'acceptedArtifactsRequested':payloads,'sourceBindings':original['sourceBindings'],'all70CurrentSourcesUnchanged':True,'all48CaseIdsPreserved':True,'all30OriginalTextsPreserved':True,
      'newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False}
    (root/'EXACT_PATCH.json').write_bytes(encoded(reg))
    request='''Please perform the final exact check of this15-spell AC4 candidate. I independently read all corrections,48 cases, both chapters and the complete profile. The revised rules address C01..C08, including the explicitly NEW scoped summon targeting and Beacon checkpoint. Source/prose verification passed248 checks. I found two remaining source-example errors and prepared exact replacements, plus a concrete restoration of X01:

1. X09 assigns a Medium rider+gear5Load, but the actual Summon Spectral Steed source counts a Medium body6Load before gear. The replacement uses body160lb/6Load +gear20lb/2Load =180lb/8Load and actual Burdened Speed50, preserving capacities and the spent crossing attempt.
2. X08 treats current Master of Winter as a free ordinary Control Weather cast. The current Druid card instead authors a bounded winter invocation replacing that undefined permission; its current spellRank is null. Use the unambiguous Wizard20 Grand Reservoir instead: exact base-only waiver, mandatory field+2, final Ease-1=1RP. Keep field eligibility at actual CAST COMMITMENT, not a new resolution-time charge during a ritual.
3. X01 now uses the actual reviewed Acid Arrow rank2/3RP/30ft/4d4 plus finite2d4 rider with explicit rolls, HP outcomes and root identity; it preserves your root-creation correction without inventing a generic interrupt.

EXACT_PATCH.json contains complete old/replacement text and every candidate hash. candidate/ contains the complete eight-file corrected module; only CASEBOOK.json and its manifest changed from your return. All15 procedure records, shared rules, both chapters, profile, register and verdict are byte-identical to your accepted corrected return; their prior verdict remains historical evidence, not a claim you already accepted these new example bytes. All70 frozen sources are included and unchanged. Please verify the exact three replacements against the supplied current sources (especially Wizard cards/62, Druid cards/46, Cleric engine/Healing Rite, and actual Summon Spectral Steed/Acid Arrow). Do not substitute historical source prose for current operative cards.

If coherent, explicitly accept the complete eight candidate payloads by their recorded SHA256 and affirm no operative corrections remain for this bounded authored module; return an exact acceptance JSON with acceptedArtifactBindings/acceptedSpellIds, dispositions for these3 repairs,48 authored-case count, preserved source/access/30original text identities, and no runtime/human/balance/cosmology/whole-game approval. A small downloadable acceptance archive is sufficient; no need to rewrite the unchanged model/chapter files. If any concrete contradiction remains, name it and supply the exact minimal correction instead of accepting. Banishment remains excluded and unadopted.
'''
    (root/'README_REVIEW.txt').write_text(request,encoding='utf8',newline='\n')
    with ZipFile(archive,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
        for b in original['sourceBindings']:z.write(G/b['path'],'sources/'+b['path'])
    requestpath=A/'AC4_EXACT_CASE_PATCH_03_REQUEST.txt';requestpath.write_text(request+'\nAttached: '+archive.name+'\n'+json.dumps(info(archive))+'\n',encoding='utf8',newline='\n')
    receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(archive),'request':info(requestpath),'patch':info(root/'EXACT_PATCH.json'),'changedExamples':3,'unchangedRulePayloads':6,'sourceFiles':70,'cases':48,'newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0}))
    print(json.dumps({'receipt':info(receipt),'archive':info(archive),'changedExamples':3,'unchangedRulePayloads':6}))

if __name__=='__main__':main()
