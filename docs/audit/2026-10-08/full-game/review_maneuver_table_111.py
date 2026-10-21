from pathlib import Path
import datetime,hashlib,json
A=Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game')
def bind(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
sp=A/'feat335-assembly-106/after/data/director/feat_candidates/exact_01/supplements.json';cp=A/'feat335-planar-reference-108/after/data/director/feat_candidates/exact_01/candidate.json'
s=json.loads(sp.read_bytes());c=json.loads(cp.read_bytes());g=next(x for x in s['groups'] if x['id']=='SUP-03')
feats=[x for x in c['records'] if x['id'] in ['martialAdept','martial_adept_advanced']]
assert len(feats)==2 and len(g['completeAuthoringValue'])==6
meaning=[
 {'activationAndPayment':'Before one independently legal weapon attack roll; spend1superiorityd6, add its face to that attack only. Attack Action/BA/Reaction still comes from the underlying source.',
  'targetAndResolution':'Actual weapon range, attack target, body and attack permissions apply. Natural1 misses; no changed critical range, automatic damage or added damage die.',
  'lifecycle':'One committed event spends the die even on miss/failure/counter; invalid declaration spends none. No ongoing effect or new attack.'},
 {'activationAndPayment':'Replace one actual Attack Action attack with ordinary Shove; spend1d6 before both opposed rolls.',
  'targetAndResolution':'Actual ordinary reach/one-size-larger cap; STR Athletics plus die opposes chosen Athletics/Acrobatics. Equal totals preserve state. Success chooses5ftpush OR Prone, no damage.',
  'lifecycle':'Immediate ordinary Shove result. Does not change save-based feat/class Shoves or provide another attack.'},
 {'activationAndPayment':'Replace one actual Attack Action attack with ordinary opposed Disarm; spend1d6 before rolls.',
  'targetAndResolution':'Reachable actually held droppable item, ordinary legal Athletics/weapon-check route vs Athletics/Acrobatics. Tie preserves state. Success drops to ordinary adjacent/own-space placement; no automatic custody, damage or severed bond.',
  'lifecycle':'Immediate ordinary disarm only. No general proficiency and no imported die for separate save-based Disarm/Whip Control.'},
 {'activationAndPayment':'Actual available Reaction plus1d6 after passive defenses and before temporary HP on one direct damage event against self.',
  'targetAndResolution':'Reduce the whole resolved event by the die face, minimum0, using stable native component order. Conditions remain. Not a hit-to-miss or successful Parry for Riposte.',
  'lifecycle':'One event, no repeat reduction per typed component. Excludes transfer packets forbidding mitigation, HP sacrifice, state assignment and direct death; adds no healing/reserve/resource.'},
 {'activationAndPayment':'Actual Bonus Action on own regular turn plus1d6; immediately spend separate5times-face movement-cost budget.',
  'targetAndResolution':'Self using one already available nonzero-Speed mode; pay actual terrain/crawl/squeeze, obey route/endpoints and ordinary opportunity attacks.',
  'lifecycle':'No teleport, new mode, Disengage, normal movement refill or stored movement. Interrupted remainder is lost.'},
 {'activationAndPayment':'Actual ordinary Rally Action plus1d6, declared before its task roll.',
  'targetAndResolution':'One actual ally within30ft able to perceive rally; choose one actual source-qualified Frightened record. CHA task at its source DC, otherwise10; actual task degrees/natural shifts apply.',
  'lifecycle':'Success ends selected fear record only. No HP/tempHP, loyalty, new save, extra turn or removal of other records.'}
]
review=[]
for row,assessment in zip(g['completeAuthoringValue'],meaning):
 review.append({'id':row['id'],'completeCurrentRow':row,'fieldByFieldAssessment':assessment,'bodyStockProviderAuthority':'No independent body, tool, weapon, target, proficiency, resource pool other than the expressly purchased feat superiority pool, or class feature is created. Underlying action carries actual body/equipment/stock requirements.','status':'AUTHORED_SOURCE_REVIEW_NOT_RUNTIME'})
out={'id':'FXC04-MANEUVER-SUBTABLE-REVIEW-111','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sourceBindings':[bind(sp),bind(cp)],'completeCurrentFeatures':feats,'completeCurrentSupplementGroup':g,'rowReviews':review,
 'commonAcquisitionAndLifecycle':'martialAdept permanently selects2distinct IDs from6 and grants one separate initially available d6; actual beneficial SR/LR restores it. Advanced requires the exact base feat, selects2additional distinct unknown IDs, increases same pool capacity to2 and explicitly initializes the newly granted die on real acquisition. That source-specific initial die is not a general capacity-refill rule. Rest does not retrain; one event uses at most one maneuver/die. Actual action/target/body legality remains required and a committed failed attempt spends its die. No RP/RC/class conversion or Battle Master subclass is supplied.',
 'remaining':['Exact GPT review pending.','FXC04 other tables and full assembled parent evidence remain open.','Actual action, body, stock, movement, damage and condition engines are not executed by this review.'],
 'newMechanicsAuthored':False,'historicalProgramsRerun':False,'runtimeExecuted':False,'canonicalApplied':False,'FXC04Accepted':False,'parent335Accepted':False,'actuallySentToGpt':False,'sourceInformationDeleted':False}
p=A/'FEAT335_FXC04_MANEUVER_SUBTABLE_REVIEW_111.json'
with p.open('x',encoding='utf8') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
with (A/Path(__file__).name).open('xb') as f:f.write(Path(__file__).read_bytes())
print(json.dumps({'report':bind(p),'fullRows':6,'fullParentFeats':2,'parentAccepted':False}))
