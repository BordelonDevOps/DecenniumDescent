from pathlib import Path
import datetime,hashlib,json
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
def j(p):return json.loads(p.read_bytes())
def bind(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,d):
 with p.open('x',encoding='utf8') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
sp=A/'feat335-assembly-106/after/data/director/feat_candidates/exact_01/supplements.json'
cp=A/'feat335-planar-reference-108/after/data/director/feat_candidates/exact_01/candidate.json'
hp=A/'FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json'
supp=j(sp);cand=j(cp);hist=j(hp)
gi=next(i for i,x in enumerate(supp['groups']) if x['id']=='SUP-08');g=supp['groups'][gi]
fi=next(i for i,x in enumerate(cand['records']) if x['id']=='contraption_crafter');feat=cand['records'][fi]
rows=g['completeAuthoringValue'];assert [r['die'] for r in rows]==[1,2,3,4]
analyses=[
 {'action':'One actual Action lights or extinguishes the integral enclosed wick; gadget supplies no Action.',
  'rangeAndTarget':'Its own wick; bright10ft/dim additional10ft while lit. Activation/holding obey common actual-reach/hands/object rules.',
  'resolution':'No attack/check/save or damage. Ordinary light, no magical-darkness penetration.',
  'costAndFuel':'The constructed body/integral wick belongs to the one5gp parts product. The row grants light for remaining gadget life, never a separate replenishable fuel inventory or ignition of other objects.',
  'durationAndLifecycle':'Lit status lasts only within the original one-hour-from-completion lifetime and ends on extinguishing, destruction or source expiry; toggle/transfer creates no new lifetime.',
  'movementAndCommand':'Inert mundane object, no self movement/creature phase. Actual person must handle/use it.'},
 {'action':'One actual Action fixes gadget and attached thread across a reachable ground passage.',
  'rangeAndTarget':'Thread5ft, non-load-bearing; actual body must cross and physically touch taut thread. Bell ordinarily audible30ft.',
  'resolution':'One physical trigger rings; no attack/save/damage, identity detection, restraint, trip or automatic hidden DC.',
  'costAndFuel':'Same constructed body and attached finite thread. No new thread stock, ammunition or portable resource pool.',
  'durationAndLifecycle':'First actual trigger releases thread and leaves device inert. Original expiry/destruction still controls; transfer does not reset spent trigger.',
  'movementAndCommand':'No independent creature Action or detector. Incorporeal/noncontact passage is not a trigger. Ordinary senses can notice visible thread.'},
 {'action':'One actual Action attaches or removes the clamp.',
  'rangeAndTarget':'Reachable mundane edge at most2inches thick, holding one unattended or willingly presented object at most5lb.',
  'resolution':'No attack/save/check bonus or creature restraint; no secured door, climber support or extra hand.',
  'costAndFuel':'Same physical clamp/product; actual suitable edge and real eligible object required.',
  'durationAndLifecycle':'Held object falls normally upon expiry/destruction; no invented fall outcome/damage. Original one-hour lifetime persists through movement/custody/reattachment.',
  'movementAndCommand':'Physical fastening only. Clamp is not a motor, carrier, creature or independent action source.'},
 {'action':'One actual Action cranks while held; sustaining airflow needs another Action.',
  'rangeAndTarget':'Ordinary airflow through5ftcone; comfort cooling limited to touched/hands-reach surface.',
  'resolution':'May stir paper/dust and show ordinary airflow. No attack/save/damage, creature displacement, substance identification, suffocation relief, weather/hazard immunity or rules-defined gas/cloud removal.',
  'costAndFuel':'Actual hand and Action operate the existing product. No independent power supply, motor or fuel/resource grant.',
  'durationAndLifecycle':'One activation ends at operator next regular-turn start, and cannot survive object expiry/destruction. Another legal Action is required for continued use.',
  'movementAndCommand':'Held manually; no creature phase, autonomous continuation, free command or source body.'}
]
review=[]
for i,(r,n) in enumerate(zip(rows,analyses)):
 assert r['procedure'].startswith('Action ')
 review.append({'id':r['id'],'die':r['die'],'sourcePointer':'/groups/'+str(gi)+'/completeAuthoringValue/'+str(i),'completeCurrentRow':r,'fieldByFieldAssessment':n,'assessment':'COHERENT_AUTHORED_PROCEDURE_AT_EXPLICIT_PHYSICAL_PREMISES_NOT_ENGINE_VERIFICATION'})
ordinary=[r for r in hist['originalCaseReviews'] if r.get('featId')=='contraption_crafter']
calcs=[r for r in hist['numericAndStateCalculations'] if r['id'] in ['HM105-N07','HM105-N08']]
report={'id':'FXC04-GADGET-SUBTABLE-REVIEW-111','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'sourceBindings':[bind(sp),bind(cp),bind(hp)],'completeCurrentFeat':feat,'completeCurrentSupplementGroup':g,
 'sharedLifecycleAssessment':{'authority':'Explicitly NEW Contraption Crafter feat product; no Tinker Gnome/class device import. Actual Gnome lineage, usable tools and suitable owned mundane parts remain required.',
 'construction':'Commit once-per24-elapsed-hours use and5gp parts at start;10uninterrupted minutes or accepted personally-led Craftsman5minutes. Starting new lawful job ends old gadget. Interruption spends parts/use, produces nothing and rolls no d4.',
 'selection':'One actual open d4 at completion chooses exactly one of four rows; no selected profile, refund, duplicate product or automatic retry.',
 'body':'Tiny mundane1lb AC10/HP1 object with no creature turn/actions. Place in actual reachable legal space; handling/moving uses actual object/hands rules.',
 'expiry':'Completion plus1hour, earlier destruction, or beginning next legal construction. Custody transfers remaining life/state unchanged. Spent parts have no reusable credited crafting value or purchased-item replenishment.'},
 'rowReviews':review,'completeRetainedConstructionCalculations':calcs,'completeRetainedOriginalCaseReviews':ordinary,
 'finding':'The four complete activation profiles are present in SUP-08 of the current106 assembly. Earlier time/work packets did not supply this table: their missing-table qualification is preserved as a limit of those packets, not proof that the current full candidate has no table. This focused review now exposes all four full rows with their common construction/body/lifecycle.',
 'remaining':['GPT has not reviewed this new exact field-by-field subtable join.','Remaining finite supplement tables still need their own complete lifecycle/source mapping for FXC04.','Actual world body, stock, tool, action, custody, expiry and physics behavior requires future implementation; no actual gadget was created.'],
 'newMechanicsAuthored':False,'historicalProgramsRerun':False,'runtimeExecuted':False,'canonicalApplied':False,'FXC04Accepted':False,'parent335Accepted':False,'actuallySentToGpt':False,'sourceInformationDeleted':False}
out=A/'FEAT335_FXC04_GADGET_SUBTABLE_REVIEW_111.json';write(out,report)
with (A/Path(__file__).name).open('xb') as f:f.write(Path(__file__).read_bytes())
print(json.dumps({'report':bind(out),'fullRows':len(review),'constructionCalculations':len(calcs),'parentAccepted':False}))
