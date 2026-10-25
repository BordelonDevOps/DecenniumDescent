from pathlib import Path
import json, hashlib

R=Path(r'C:\Github\DecenniumDescent'); A=R/'docs/audit/2026-10-08/full-game'; O=A/'spell-review-resume-116'
P=R/'DescentReviewChanges/ReviewBible/data/director/spell_review/rank7_mechanics_16_source_conference_01.json'
C=json.loads(P.read_text())
hazards={
'lightning-grave':['Later move/act trigger must cause the printed10d8; no initial unconditional damage.','Commit/interrupt order must not allow an already invalid action or produce repeated discharge.','Forced displacement, voluntary teleport, ordinary physiology, saved/immune trigger, death and expiry need distinct outcomes.'],
'pyroclasm':['Preserve cast-point20ft range and distinguish burst size; caster and allies may be exposed.','Burning ground must have actual persistent behavior despite Instantaneous source label; its parameters require explicit new authorship.','Ground contact cannot be inferred from horizontal overlap of flying bodies; initial blast and later ground ticks are distinct damage roots.'],
'frost-reaver':['Preserve8d8cold and until-healed endpoint, rather than importing full Slow or adding a timeout.','Healing at fullHP, blocked healing, temporaryHP and suppression must be distinguished.','Rider establishment and damage immunity/save outcomes need explicit independently consistent rules.'],
'arcbolt-singularity':['At most6 distinct eligible enemies and5d6each; no recursive chains or extra damage for fewer targets.','Core/arc geometry, target selection and shared versus per-target RNG must be explicit.','No persistent power resource, pull or gravity from the name singularity.'],
'delayed-blast-fireball':['12d6is a ceiling and damage must increase over a legal delay.','Original finite clock, elapsed-time/turn distinction, early release and suppression must not create infinite growth or banked casts.','Finite anchor and casting/expression loci; no assumed external transferable bead rules.'],
'prismatic-spray':['Exactly7distinct native effects and60ftcone; every table entry has complete save/success/lifetime rules.','Each selection draw must be separate from damage/save draws; no new Fate visibility permission.','Cone/body intersection and cover, plus independent hard-control admission where relevant, need actual cases for all7effects.'],
'whirlwind':['Preserve10d6bludgeoning plus a concrete pull; blocked pull does not erase damage.','Whole-body path must stop before obstruction/occupied geometry and handle anchors/support.','Movement/damage order must not grant creature-only movement to an already dead ordinary corpse.'],
'crown-of-stars':['Exactly7finite motes, each4d12radiant; explicit cadence and action costs without free actions.','Committed missed/immune discharges spend motes, and successful/failed recasts have separate replacement behavior.','No salvageable inventory gems or rest/suppression refills; define original clock and concentration.'],
'mass-confusion':['Preserve enemy-only30ftradius and30ftcenter range.','Native d4behavior, d8direction and1dNvictim draws must be separate; absent budget/target/path gives no reroll.','Initial hard admission and future regular START/END timing must distinguish extra turns and attached companion opportunities.'],
'dominate-greater-beast':['Actual magical-beast classification andCR<=12are both required; no type or CR by analogy.','Preserve120ftrange and concentration1minute; positive fixture may remain explicitly conditional.','Command scope, harm/repeat-save, replacement, mental delivery and actual owner-attached budgets need complete local rules.'],
'mindfog-field':['Preserve all6 INT/WIS/CHAcheck-and-save categories at-2; no inferred attack/DC/ability-score changes.','First exposure save must not be penalized before establishment; zone entry/exit and cover return need stable history.','Overlap/suppression cannot duplicate penalties, delete losing records or reveal hidden sources.'],
'lasting-control':['Preserve ALL qualifying current Enchantment spells and+600seconds while reconciling its own concentration<=60seconds.','Commitment/concentration replacement occurs before eligible-target snapshot; ended own spells cannot be resurrected.','Define school/owner/range/LoE scope, typed versus elapsed endpoints and dependent rider clocks.','No renewed hard admission, restored charges, completed orders or recursive unlimited extension; any new cap must be declared as new authorship.'],
'power-word-pain':['Printed100HPthreshold is current normalHP, not temporaryHP or hidden free UI information.','Preserve V/S/F; spell title alone gives neither no-save nor verbal-only casting.','Define actual pain effects, threshold application versus ongoing condition, repeat saves and ending without imported external rule lists.'],
'project-image':['Preserve both school profiles: Enchantment120ftremote sightANDhearing; IllusionSelfduplicate.','Actual class access maps to Enchantment; alternate profile existence is not acquisition permission.','Define sensory selection/control costs, image travel/tether/LoE, physical interactions and observer-specific disbelief.','No invented creature body/HP/turn/inventory/spell origin or voice authentication; suppression resumes no past information.'],
'reverse-gravity':['Both schools retain50ftradius,50ftcast range,creaturesANDobjects,concentration1minute,V/S/M-or-F.','Explicit finite3Dfield, body eligibility, anchoring, carried objects and top boundary prevent unlimited oscillation.','Grasp must use real reach/support; collision/fall path and suppression transitions need ordered state with no duplicated distance.','No inferred structural break force/objectHP or silently dropping the object benefit.'],
'symbol-of-stunning':['Actual rune with complete finite arming,trigger,radius and discharge rules; no external ritual/material cost.','Stunned requires native hard admission; independent saves and guard rejection have no invented fallback.','One consumed discharge remains spent when all targets save; source-rune and established-rider lifecycles are distinct.']}
rows=[]
for i,r in enumerate(C['records']):
 s=r['completeCurrentCatalogSourceAndAccess']
 rows.append({'spellId':r['spellId'],'sourcePointer':f'/records/{i}/completeCurrentCatalogSourceAndAccess',
 'sourceAccess':s['classAccess'],'sourceCoreProfiles':s['source']['coreEntries'],
 'sourceBookProfiles':r['completeCurrentBookBindings'],
 'questionIds':[q['id'] for q in C['questions'] if r['spellId'] in q['spellIds']],
 'independentReturnReviewObligations':hazards[r['spellId']],
 'returnedProcedureReviewed':False})
assert len(rows)==16 and sum(len(x['sourceBookProfiles']) for x in rows)==18
assert sum(len(x['questionIds']) for x in rows)==33
out={'id':'RANK7-MECHANICS16-INDEPENDENT-REVIEW-OBLIGATIONS-116',
 'basis':{'path':str(P),'sha256':hashlib.sha256(P.read_bytes()).hexdigest()},
 'scope':'Independent source reading and acceptance obligations prepared before reviewer return. No procedure selected or semantic acceptance claimed. These checks are not runtime tests.',
 'records':rows,
 'crossCuttingChecks':['Exact actual class/rank/access and17baseRP preserved; no hardcoded17minimum classlevel.','Full original question dispositions and declared new parameter selections must agree with all procedure/case mirrors.','Actual inputs, intermediate snapshots, payment, RNG, damage arithmetic, target eligibility, geometry and endings must agree in each complete case.','Missing world/content qualifications must not be hidden behind positive execution claims.','Retained current accepted53spell identities and feat335acceptance are not reopened by older packet status strings.']}
(O/'INDEPENDENT_SOURCE_OBLIGATIONS.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Independent obligations saved for16spells/18source profiles/33questions.')
