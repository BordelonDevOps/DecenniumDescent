from pathlib import Path
import json,hashlib,zipfile,datetime
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=A/'director-spell-review-128'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
index=read(R/'data/public/spell_playtests/authored_review_index.json');e=next(e for e in index['entries'] if e['id']=='protection-from-energy');assert e['authoredStatus']=='reviewed-authored-operational-playtest'
catalog=read(R/'data/public/spell_playtests/catalog.json');card=catalog['spells'][34];assert card['id']==e['id']
w=read(R/'data/public/class_playtests/warrior.json');wc=w['cards'][23];assert wc['id']=='warrior.hero.wardborn.protective-mutations'
notes={'id':'MAGIC7-ACTUAL-DEFENSE-SOURCES-128','status':'PREPARED_UNSENT_SOURCE_SUPPLEMENT_NOT_ACCEPTANCE','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Continue current7spell review; preserve all drafted procedures/23questions and closed cohorts. New actual source evidence resolves the claimed missing Rebind defense-provider prerequisites. Do not run any supplied or historical program.',
 'currentCounts':{'reviewedApplied':616,'pending':232,'acceptedUnapplied':0},
 'actualAvailableSources':[
  {'identity':'protection-from-energy','indexEntry':e,'completeCurrentCard':card,'sourcePointer':'current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json#/spells/34','purpose':'Actually reviewed rank2/base3RP nonconcentration spell grants immunity, not merely resistance, to one of8types including fire. Wizard minimum3. Native caster tenth future regular START expiry, or60seconds outside. Use a genuinely acquired/prepared caster.'},
  {'identity':wc['id'],'completeCurrentCard':wc,'sourcePointer':'current/DescentReviewChanges/ReviewBible/data/public/class_playtests/warrior.json#/cards/23','purpose':'Warrior11 Wardborn has S=3. With actual selected Protective Mutations and at least one actually equipped/activated mutation, adjacent ally reduces first damage each numbered round by3. This can protect a Wizard target who already has real fire resistance and an actual ProtectionFromEnergy fire-immunity application. Full class engine/schedule/acquisition/serum source is included.'}],
 'requestedCaseCompletions':[
  'Complete a genuine original combined-defense Rebind case: actual W11 target with its native fire Ward, paid acquired ProtectionFromEnergy granting fire immunity, and actual Warrior11 Wardborn ProtectiveMutations aura granting3flat reduction. Supply full actual Warrior character/acquisition/mutation/serum Action/BA/Strain/round history and exact5ft body geometry; no free trait. Rebind failedCON strips covered fire immunity+resistance, leaving actual first-eventDR3; original5d10 total28 becomes25damage if all source predicates remain valid. Preserve proper mitigation, Wound/concentration and phase results.',
  'Complete an independent immunity-expiry-before-Rebind-end case using actual ProtectionFromEnergy. For example, paid application at0.1 with caster next ten STARTs6..60 expires60, then a genuinely phase-qualified Rebind commitment58.1 and target next futureEND64. Show every needed actual turn/payment/lifecycle event. At60 the immunity source truly ends while covered; at64 Rebind ending cannot recreate it. This is a proposed fixture schedule, not selected state or a waiver of full actor evidence.',
  'Retain original conditional illustrations as history, but do not label these positive defense cases missing-content when the included current native sources suffice. Any residual independent transfer/special absolute-protection case still needs its own actual source or explicitly retained narrow hold.'
 ],
 'draftCaseCorrectionsToCheck':[
  {'case':'TU6-09-B','issue':'Earlier draft used LesserAntimagic radius20; current accepted source is fixed10-foot radius. Correct all final plan/source/before-after/ledger/mirrors if still wrong, preserving exact prior draft in history.'},
  {'case':'TU6-09-B','issue':'Earlier A body foot[30,15,0],extent[5,5,6] did not contain cast sourcePoint[30,12.5,3]. Use an actual current body-surface origin and center within native10ft; verify all other bodies/interference as well. A point[30,15,3] to center[30,5,3] has distance10 if the recorded positions are unchanged. Do not change selected spell rules to repair geometry.'}
 ],
 'sourceProgramsExecuted':False,'canonicalChanged':False,'acceptanceGranted':False}
paths=[R/'data/public/spell_playtests/catalog.json',R/'data/public/spell_playtests/authored_review_index.json',R/'data/public/class_playtests/warrior.json',R/'data/public/class_playtests/wizard.json',R/'data/public/spell_candidates/abjuration_conjuration_rank5_reviewed_05.json',R/'docs/mechanics/CLASS_PLAYTEST_RULES.md',R/'docs/mechanics/SPELL_INTEGRATION_RULES.md',G/'docs/reference/Player_Rulebook_v6_source_text.txt']
files={'current/'+p.relative_to(G).as_posix():p.read_bytes() for p in paths};files['SOURCE_FINDINGS_AND_REQUESTS_128.json']=enc(notes)
files['README.md']=b'MagicModifiers7 current native source supplement128. Complete current immunity+resistance+DR3 and immunity-expiry Rebind cases instead of leaving actually available provider facts unresolved. Preserve historical conditional examples. Check earlier Clone Antimagic radius/origin issues. All substantive choices remain GPT-directed and pending exact independent review; no canonical changes or acceptance from this file.\n'
manifest={'id':'MAGIC7-SOURCE-SUPPLEMENT-128-MANIFEST','files':[{'path':n,'bytes':len(v),'sha256':sha(v)} for n,v in files.items()]};files['MANIFEST.json']=enc(manifest)
out=D/'DD_Magic7_Native_Defense_Sources_128.zip';assert not out.exists()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,v in files.items():z.writestr(n,v)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for b in manifest['files']:v=z.read(b['path']);assert len(v)==b['bytes'] and sha(v)==b['sha256']
(D/'MAGIC7_NATIVE_DEFENSE_FINDINGS_128.json').write_bytes(enc(notes))
receipt={'id':'MAGIC7-NATIVE-DEFENSE-SUPPLEMENT-128','status':'PREPARED_UNSENT','archive':{'path':str(out),'bytes':out.stat().st_size,'sha256':sha(out.read_bytes())},'members':len(files),'bindings':len(manifest['files']),'sourceProgramsExecuted':False,'canonicalChanged':False}
(D/'MAGIC7_NATIVE_DEFENSE_PACKET_128.json').write_bytes(enc(receipt));print(json.dumps(receipt,indent=2))
