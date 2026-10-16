"""Author a shared use/recovery discussion candidate; preserve all 24 source items."""
from datetime import datetime, timezone
from copy import deepcopy
import hashlib, json, zipfile
import xml.etree.ElementTree as ET
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())
def digest(raw): return hashlib.sha256(raw).hexdigest()

def main():
    root=A/'core-consumable-use-local-draft-01'
    receipt=A/'CORE_CONSUMABLE_USE_DRAFT_01_PREPARATION.json'
    assert not root.exists() and not receipt.exists()
    oldpath=A/'CORE_CONSUMABLE_24_SOURCE_PREPARATION.json'; old=read(oldpath)
    core=G/old['sourceJsonFile']; original=read(core)
    book=G/old['bookFile']; ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with zipfile.ZipFile(book) as z: xml=z.read('word/document.xml')
    tree=ET.fromstring(xml)
    paragraphs=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in tree.findall('.//w:p',ns)]
    assert len(old['records'])==24
    for row in old['records']:
        assert original[row['family']][row['sourceArrayIndex']]==row['completeCoreJsonRecord']
    for p in old['completeBookSections37And38']:
        assert paragraphs[p['paragraphIndex']]==p['exactText']
    sourcepaths=[oldpath,core,book,
        R/'docs/mechanics/CONDITION_RECOVERY_PLAYTEST.md',R/'docs/mechanics/CONDITIONS_PLAYTEST.md',
        R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',
        R/'docs/mechanics/STRAIN_PLAYTEST.md',R/'docs/mechanics/HEALING_DEATH_PLAYTEST.md',
        R/'docs/mechanics/EQUIPMENT_ITEM_PROCEDURES.md',R/'docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md',
        R/'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md',R/'docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md',
        R/'docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md',
        R/'data/director/cosmology/souls_research_reviewed_01.json',R/'data/director/cosmology/planes_reviewed_01.json']
    bindings=[info(p) for p in sourcepaths]
    evidence=[]
    def quote(rel, term):
        p=R/rel; ls=p.read_text(encoding='utf-8').splitlines(); hits=[(i+1,s) for i,s in enumerate(ls) if term in s]
        assert len(hits)==1,(rel,term,len(hits))
        i,s=hits[0]; key='E'+str(len(evidence)+1).zfill(2)
        evidence.append({'id':key,'path':p.relative_to(G).as_posix(),'sha256':info(p)['sha256'],'lineOneBased':i,'exactText':s})
        return key
    e={
        'use':quote('docs/mechanics/EQUIPMENT_ITEM_PROCEDURES.md','Unless stated otherwise, using a consumable'),
        'dose':quote('docs/mechanics/CONDITION_RECOVERY_PLAYTEST.md',"Preserve Core's existing substance procedures"),
        'tolerance':quote('docs/mechanics/CONDITION_RECOVERY_PLAYTEST.md','**Tolerance:**'),
        'maintenance':quote('docs/mechanics/CONDITION_RECOVERY_PLAYTEST.md','**Maintenance:**'),
        'project':quote('docs/mechanics/CONDITION_RECOVERY_PLAYTEST.md','**NEW dependence recovery project:**'),
        'withdrawal':quote('docs/mechanics/CONDITION_RECOVERY_PLAYTEST.md','Withdrawal imposes disadvantage on ability checks.'),
        'intox':quote('docs/mechanics/CONDITION_RECOVERY_PLAYTEST.md','Use one dose-driven score from 0 to 5.'),
        'quickglass':quote('docs/mechanics/STRAIN_PLAYTEST.md',"Quickglass's crash adds1 expedition point"),
        'rest':quote('docs/mechanics/STRAIN_PLAYTEST.md','**Rest Debt order.**'),
        'supply':quote('docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md','**Supply is a basket of real goods:**'),
        'day':quote('docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md','At each canonical 24-hour day endpoint'),
        'healing':quote('docs/mechanics/HEALING_DEATH_PLAYTEST.md','Within each permitted reduction plan:'),
        'totem':quote('docs/mechanics/HEALING_DEATH_PLAYTEST.md','Blight Totem cannot compound'),
        'smallMass':quote('docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md','**New small-weight completion.**'),
        'vision':quote('docs/mechanics/COMBAT_ACTION_PLAYTEST.md','Attacks against unseen targets have disadvantage;'),
        'language':quote('docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md','| Silenced |'),
        'pendingLanguage':quote('docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md','Pending effects remain unavailable through this chapter.')
    }
    decisions=[]
    def decision(i,title,source,proposal,question):
        decisions.append({'id':f'CU-01-{i:02d}','title':title,'sourceEvidence':source,'classification':'NEW local proposed completion or integration; actual GPT disposition pending','proposal':proposal,'jointReviewQuestion':question,'adopted':False})
    decision(1,'Separate the two catalogs',[e['dose'],e['intox']],
        'The twelve magical substances use their printed dependence DC and the Core repeat-dose, tolerance, overdose and crash rules. The twelve brews have no printed dependence DC and do not silently inherit that subsystem. A brew adds Intoxication only when its own proposed operational profile explicitly does so. Preserve Gatehouse Small Beer’s one-serving exemption and Thunder-Vein Ale’s printed delayed +1. Neither an alcohol-like name nor a price creates a generic poisoning, dependence or Intoxication gain. Individual brew proposals must disclose any NEW repeated-serving rule rather than hiding it in this framework.',
        'Confirm the catalog boundary and whether a separate source-directed ordinary brewing rule should give other brews Intoxication; no such increase is adopted here.')
    decision(2,'Real portions and administration',[e['use'],e['smallMass']],
        'NEW unit proposal: an ordinary brew serving is one actual pint of liquid, provisionally 1 lb plus its real container, drunk over one uninterrupted active minute. A named profile can expressly use a different amount/time. Each magical substance uses one measured ready dose and the existing Action/available-hand/actual-access procedure; oral administration requires actual swallowing and an eligible willing or Incapacitated recipient within 5 ft. Inability to eat as a requirement is not automatically inability to swallow, but no effect supplies missing anatomy. An unwilling active creature receives no generic forced-dose permission. All 24 profiles must specify their actual packaging/mass rather than treating a menu entry as stock. These proposed portions do not replace printed crafting recipe units or transform powders into free inhaled attacks.',
        'Accept or replace the pint/minute brew convention and classify the individual substance units against their actual descriptions. Do not equate the brew serving with a universal meal duration.')
    decision(3,'Consumption and interruption',[e['use'],e['supply']],
        'Reserve actual units when administering. A completed full serving/dose creates one consumption event at its completion timestamp. Fluid/material actually swallowed, spilled or destroyed before an interruption is physically gone; no game benefit is granted for an incomplete dose and no whole unit is refunded. Ordinary consumed water/food counts only when its own source permits that actual amount. Do not combine arbitrary fractional remains into a stronger dose: a named whole-unit preparation procedure must establish usable potency. This is an explicit NEW rule for unfinished administration, not a statement about real chemistry.',
        'Confirm completion timing and distinguish physically lost quantities from completed-dose counters. Individual instant benefits still use their actual completed consumption event.')
    decision(4,'Dose history belongs to the recipient and named substance',[e['dose'],e['tolerance']],
        'Maintain a stable recipient ID and exact substance identity, with completed dose events (eventId, completedAt, units=1 or 2, actual stock IDs), beneficial-long-rest boundaries, dependence status, maintenance interval, tolerance latch, benefit records and crash records. Another supplier, brand, session, controller or inventory transfer does not erase a recipient’s history. Different named substances have separate histories unless an explicit later reviewed equivalence says otherwise. No broad label such as drug, wine, Null or Strain establishes identity.',
        'Confirm the identity and recipient boundaries, including a real later restoration using the same character record; source-specific transformation/restoration exceptions remain controlling.')
    decision(5,'Rest boundary is an explicit unresolved integration choice',[e['maintenance'],e['rest']],
        'NEW proposed resolution: only a genuinely beneficial completed Long Rest resets the doses-since-rest counter and opens the next named-dependence maintenance interval. An extra safe eight-hour Rest Watch inside the reward cap can clear Rest Debt as printed but cannot be used to erase repeat-dose/overdose accounting. Resetting the counter does not clear dependence, tolerance, already scheduled crashes or running effects. This narrows the condition chapter’s unqualified completed-long-rest wording and therefore needs an explicit joint disposition before use; the currently reviewed chapter is not changed by this draft.',
        'Should substance epochs require a beneficial Long Rest, or any actual completed Long Rest? Resolve this against the current safe-Rest-Watch distinction and record an explicit supersession if needed.')
    decision(6,'Repeat-dose and overdose ordering',[e['dose'],e['tolerance'],e['maintenance']],
        'At a legal completed event, read the recipient’s pre-event tolerance and rest-counter state. One ordinary dose counts as one; a doubled dose counts as two. If this event contains any second-or-later dose since the rest boundary, require one CON save at that named substance’s printed dependence DC, at most one save for the whole event. NEW failure interpretation: become Addicted to that named substance; success never cures existing dependence. If the new rest count exceeds two, also execute that item’s explicit severe complication once for the event and apply the NEW dependence-advancement interpretation: acquire named dependence automatically if absent, otherwise retain it and record the overdose without inventing a second severity scale. The save cannot cancel the separate automatic overdose consequence. Every further event above two triggers its actual complication once, not once per conceptual dose inside a doubled event. A missing complication blocks an item’s operational completion; this draft supplies no generic substitute.',
        'Review the save trigger for a doubled first use, once-per-event overdose, and automatic named dependence as the meaning of advances dependence. Approve each item’s actual severe complication separately.')
    decision(7,'Tolerance is a latch with exact rolling history',[e['tolerance']],
        'Use seven elapsed days = 604800 seconds. The completed-dose counting window is (now−604800, now], so an event exactly seven days old is outside it. At seven full days without a dose, clear the tolerance latch immediately before processing a new dose at that timestamp. If tolerance was inactive before the event, its current ordinary benefit duration is not shortened even when that event reaches three doses in the rolling window. Set tolerance active after that completion if the new rolling count is at least three. Once active it remains active until a full seven-day no-dose interval, even if the rolling count later falls below three while some more recent use remains. A Long Rest does not clear it.',
        'Confirm the exact equality boundary and its order against a simultaneous new dose; the third-use and seven-day abstinence rules come from the reviewed recovery chapter.')
    decision(8,'What doubling and half duration actually do',[e['tolerance']],
        'A doubled event needs two real complete doses already prepared for one actual administration. It uses two units for inventory, rolling tolerance and doses-since-rest, but never doubles potency, temporary HP, damage, number of targets or entitlements. When tolerance was already active, it restores the printed normal benefit duration; without tolerance it gives only that normal duration. One actual Action is permitted only where the individual dose profile allows both ready units to be consumed in that Action; otherwise they are separate completed events, not an after-the-fact doubled declaration. Half duration uses exact elapsed seconds, with no rounding to a larger minute or round. Only duration-based benefits are halved. Crashes, recovery requirements, overdose complications and the duration of an adverse effect are not shortened by generic tolerance. Instant benefits and undefined until-next-rest/one-use endpoints require a named item interpretation; do not invent a half-rest.',
        'Review per-item administration, Dreammilk/Spiral Ink endpoint semantics and Wyrmspice’s missing entitlement duration. No doubling can waive the printed Redwake benefit lock.')
    decision(9,'Every dose keeps its own ending and crash',[e['dose'],e['quickglass']],
        'Create one dose-benefit record with a fixed original endpoint and one pending crash record. Same-name bonuses, advantage and resistance do not stack numerically. A later dose does not erase or postpone an earlier dose’s endpoint or crash. At each dose’s real end, apply its printed crash once even if another dose still supplies a benefit; the two can coexist. NEW proposal: an actual effect-ending cure that removes the benefit early triggers that dose’s crash at the actual ending timestamp unless it explicitly also prevents/removes the crash. Mere suppression pauses neither the original duration nor the crash clock. A spent benefit use ends that entitlement but triggers an immediate crash only where the individual item explicitly binds the crash to that expenditure. Temporary HP follows its actual source record and existing selection rules; there is no pooled duplicate award.',
        'Confirm early ending versus suppression and the intended crash trigger for each consumable. A spell-only dispel does not automatically target a nonspell dose.')
    decision(10,'One-use rewards cannot become hidden stockpiles',[e['dose']],
        'NEW proposed policy for a brew or dose saying next/one check or save: overlapping applications of that same item provide at most one available entitlement. A new completed use may refresh that one available opportunity through its own stated expiry, but cannot queue several. Committing the permitted roll marks every currently overlapping same-item entitlement consumed, so an older covered dose does not reappear as another use. Independent named items remain governed by their own scope; advantage sources still do not stack. A future actually paid dose after expenditure can grant a new opportunity, subject to its actual repeat-use costs and risks. Eligibility and commitment occur before the roll, not after seeing failure.',
        'Confirm for Delver’s Bitter, Dragonblood Brandy and Verdant Leaf Wine, or provide explicit alternative bounded entitlements. No use is gained if the item’s timing/eligibility remains undefined.')
    decision(11,'Condition suppression is not cure or a free maintenance dose',[e['maintenance'],e['project'],e['withdrawal']],
        'Only actual completed consumption satisfies a due maintenance dose. Suppressing Withdrawal symptoms does not remove named dependence, erase the due interval or count as taking a dose. For the proposed beneficial-rest boundary, evaluate actual completed rest, open the new interval, then credit only a completed dose at/after that boundary; a dose from before completion cannot prepay it. A dose legally taken after the boundary may end that substance’s Withdrawal while still causing its own crash, dependence save, tolerance accounting and overdose. The seven-day abstinence recovery project and tolerance clearance can run on the same real calendar, but neither one automatically proves completion of the other’s work/supplies/check. A new dose breaks the abstinence project, even if its benefit was suppressed or redundant.',
        'Review simultaneous completion ordering and whether a completed doubled event can satisfy only the current maintenance requirement, without stockpiling future intervals.')
    decision(12,'No cross-system cure or resource conversion',[e['quickglass'],e['withdrawal'],e['intox'],e['healing'],e['totem']],
        'Keep expedition Strain, Warrior serum Strain, global Exhaustion, dose-driven Intoxication, Unity Exposure, named dependence/Withdrawal, Wounds and HP separate. Quickglass keeps +1 expedition Strain plus its separate one-hour DEX-check disadvantage; neither rest nor suppression silently removes both. A Poisoned immunity does not imply immunity to every substance effect or dependence. Hollow Cask’s eventual −1 healing proposal belongs to the compatible flat-reduction stage and must be compared through Blight Totem’s actual alternate plans, never subtracted twice from one event. A named prohibition on spending RP does not prohibit Oracle RC by name similarity, erase material costs or grant free casts.',
        'Confirm each named interface against its item’s complete profile. The shared chapter must not promote the item solely because a track or healing pipeline already exists.')
    decision(13,'Physical provisions and economics remain real',[e['supply'],e['day'],e['smallMass']],
        'Keep printed prices and legal labels as source fields, not guaranteed sellers, permission or stock. A bought brew/dose must come from an actual lot and container. Small/Medium normal daily demand is the current two pounds of food and eight pints of water, Large twice, with actual exceptions. Gatehouse Small Beer’s hydration-safe wording supports proposing actual liquid hydration credit, but one serving never creates a whole Supply basket or food ration. Hollow Cask’s hunger suppression does not remove food/water requirements. Deep Blue’s doubled-water crash needs a defined time-weighted or day-end procedure before it becomes operational; no food/oil/camp-sundry doubling is implied. Committing one real basket to an activity does not leave a second inventory basket.',
        'Approve each actual serving’s water/food credit and the Deep Blue partial-day formula. Do not let a purchase price or recipe name decide unreviewed ingredient availability.')
    decision(14,'Preserve protected-information and source-specific meanings',[e['vision'],e['language'],e['pendingLanguage']],
        'Current souls/research and planes companions do not mention Ghostwine, Sovereign Reserve or their exact effect phrases in their JSON string values. That bounded finding does not decide those items’ taxonomy, target predicates, observation range, protected facts or terminal recording. Keep their whole source records pending individual conference. Choir Dust’s repeated-use identity-loss phrase and Choirless Absinthe’s named auditory scope likewise cannot be converted into compulsory beliefs, automatic Equation knowledge or a new soul/realm identity. Moonsap’s movement detection must be reconciled with the current known-position Invisible exception; detecting position is not automatically true sight or permission to target through a wall.',
        'Resolve these specific item interfaces with actual GPT using the reviewed cosmology sources; do not assume the general cosmology review was also a consumable verdict.')

    cases=[]
    def case(i,title,start,events,expected,seconds=None):
        cases.append({'id':f'CU01-C{i:02d}','title':title,'start':start,'events':events,'elapsedSeconds':seconds,'expected':expected,'status':'Authored adjudication of proposed rules; not a runtime or human test.'})
    case(1,'First ordinary use','Substance X: no doses, no tolerance or dependence; actual unit available.','Complete one legal dose.','One unit consumed; rest count 1; no repeat-dose save or overdose. Benefit and its one crash use the individual profile.',6)
    case(2,'Second use','Same substance: one completed dose since the rest boundary.','Complete another ordinary dose and fail its printed dependence CON save.','Rest count 2; named dependence begins under CU-01-06. No overdose yet. Actual second benefit and crash still apply.',6)
    case(3,'Third use is not retroactively shortened','Two ordinary uses in the current seven-day window; tolerance inactive.','Complete a third single dose before the next qualifying rest; succeed on dependence save.','Current dose has normal duration. Tolerance becomes active afterward. Rest count 3 separately triggers this item’s real severe complication and proposed automatic named dependence despite the successful save.',6)
    case(4,'Fourth use under tolerance','Tolerance active; printed benefit 600 seconds.','Take a single dose.','Benefit lasts 300 seconds from actual completion. Crash duration stays its printed duration; repeat-dose/overdose follows the separate rest counter.',6)
    case(5,'Doubled first event','No doses in this rest epoch/window; two ready actual units with a profile permitting one doubled administration.','Consume both in one event.','Rest/rolling count 2, one dependence save because the event contains the second dose, no overdose. Potency and normal duration are not doubled.',6)
    case(6,'Doubled event crossing three','One previous dose; tolerance inactive; two units ready.','Complete a doubled event.','Rest/rolling count 3; at most one dependence save and one item-specific overdose event. Current duration is normal; tolerance becomes active only afterward.',6)
    case(7,'Doubled tolerant use','Tolerance active; printed duration 600 seconds, two real units prepared.','Complete a permitted doubled event.','Duration 600 seconds, never 1200. Count two actual doses and resolve each threshold once per event as proposed.',6)
    case(8,'No retrospective doubling','Tolerance active; one unit consumed at T0 and another at T0+6 through separate administrations.','Later call them one doubled dose.','Two separate events remain, each with its own tolerance-adjusted duration/crash and threshold evaluation. No retroactive restoration of the first duration.',6)
    case(9,'Tolerance latch outlives the rolling third use','Tolerance active; old doses age out but a dose was taken six days ago.','Rolling seven-day count falls from three to one.','Tolerance remains active; fewer than three current doses does not substitute for seven full days of abstinence.')
    case(10,'Exact seven-day boundary','Last actual dose completed at T0; no later dose.','Reach T0+604800 and consume a new dose at that timestamp.','Clear tolerance first, exclude the old boundary event from the rolling window, then count the new dose. Its duration is normal unless another source explicitly changes it.',604800)
    case(11,'New supplier is the same substance','Quickglass history has two doses since a qualifying rest.','Buy Quickglass from another seller and consume it.','It is the third Quickglass dose, not first use of a new brand. Actual stock changes, recipient history persists.',6)
    case(12,'Different substance is a separate history','Quickglass rest count 2, Moonsap rest count 0.','Consume one Moonsap.','Moonsap count becomes 1; Quickglass stays 2. Effects may coexist only within their actual rules; no automatic pooled drug counter.',6)
    case(13,'Rest does not cancel a scheduled crash','A 600-second dose begins 300 seconds before an actual qualifying Long Rest completion.','Rest completes before the dose’s fixed endpoint.','Proposed rest counter reset and maintenance opening occur, but the remaining 300 seconds of benefit and its crash remain scheduled. The earlier dose cannot satisfy the new maintenance interval.',300)
    case(14,'Unrewarded rest is an unresolved decision','The character already received a beneficial Long Rest within the current 24-hour cap.','Complete another safe eight-hour Rest Watch.','Under this NEW proposal, eligible Rest Debt may clear but substance epoch/maintenance does not reset. This case cannot be called an adopted rule until GPT resolves CU-01-05.',28800)
    case(15,'Maintenance at the boundary','Named dependence; next qualifying rest completes at T0.','A completed legal dose has timestamp T0 exactly, after the ordered rest event.','Open the interval then credit that actual dose once; no prepaid next interval. Dose/crash/tolerance consequences still occur.',0)
    case(16,'Suppressed Withdrawal during recovery','Named dependence and Withdrawal, symptom suppression active.','Patient completes the actual seven-day no-dose project with real daily work/Supply and a successful recovery check.','Suppression did not count as a dose or break abstinence. Named dependence/Withdrawal removed by the actual project, and seven-day abstinence also clears tolerance; no free supplies or project success.',604800)
    case(17,'Redundant dose still breaks abstinence','An abstinence project is running; another effect would suppress this dose’s benefit.','Actually complete a dose anyway.','Physical dose and history count, project fails, and its item-specific crash/thresholds still resolve. A redundant or suppressed benefit does not make consumption nonexistent.',6)
    case(18,'Independent Quickglass endpoints','Two valid Quickglass doses, each actually lasting 600 seconds, completed at T0 and T0+300.','Reach T0+600, then T0+900.','First crash at 600 adds one expedition Strain and DEX-check disadvantage until 4200, even while the second benefit lasts until 900. Second crash at 900 adds its own point and disadvantage until 4500. One advantage/Speed bonus at a time, two real crashes. Actual Strain endpoints/life rules still apply.',900)
    case(19,'Tolerant Quickglass crash is not halved','Tolerance active, one valid single Quickglass dose completed T0.','Reach its 300-second benefit endpoint.','Crash at 300; the independent one-hour DEX-check penalty lasts through 3900, not 2100. Apply expedition gain through its actual track.',300)
    case(20,'Early ending and suppression differ','One dose has a fixed T0+600 endpoint.','At T0+100 one legal effect ends its benefit; in an alternative history it merely suppresses it.','NEW proposal: actual ending triggers the one crash at 100, with no duplicate at 600. Mere suppression retains the original endpoint and crash at 600. The effect must actually target this nonspell benefit.',100)
    case(21,'No fear-advantage stockpile','Two unspent overlapping Dragonblood Brandy entitlements, assuming a later approved complete profile.','Commit one eligible fear save before rolling.','One advantage state applies and both overlapping same-item entitlements become spent under the proposal. They do not provide a second save afterward. Their actual other consequences remain.')
    case(22,'Brew is not silently a dependence drug','A real serving of Thunder-Vein Ale; no item-specific added brewing rule approved.','Its actual proposed ten-minute benefit ends.','Apply the printed +1 Intoxication once when the individual profile is approved; do not invent a magical-substance dependence DC, serum Strain or second intoxication from its name.',600)
    case(23,'One pint is not a basket','One actual proposed pint of hydration-safe Small Beer consumed by a normal Small/Medium creature.','If the proposed hydration credit is approved, record that pint once.','One of eight daily water pints credited, not two pounds of food, lamp oil, sundries or an entire Supply. Container/remaining liquid remain actual inventory.')
    case(24,'Hunger is distinct from provisions','Hollow Cask suppression active; character consumes no required food today.','Reach the canonical provisioning endpoint.','No invented food credit. Apply the actual unmet-day procedure; do not treat the suppressed sensation as satisfaction of the food requirement.')
    case(25,'Healing arithmetic respects the existing stage','Hollow Cask proposed −1 local flat reduction, base healing 8, systemic Corrupted half, no other modifier.','Resolve one actual healing event.','8 × 1/2 = 4, then −1 = 3 before ordinary caps. Do not subtract once from the root and again from the same numeric add-on.')
    case(26,'Blight Totem comparison','Same systemic half and base 8; both Blight Totem and Hollow Cask local reductions apply.','Compare the two permitted local-reduction plans.','Systemic half plus Totem half yields 2. Systemic half plus Hollow Cask −1 yields 3. Select 2; do not combine Totem and Cask into 1.')
    case(27,'Missing overdose is a real blocker','A substance has a complete first-dose benefit but no defined severe complication.','Attempt to classify the whole item as operational.','Fail that completion claim. Keep the source row, dose proposal and missing individual complication visible; no generic placeholder or avoidance of third-dose cases closes the item.')
    case(28,'Cosmology review is not item approval','Reviewed souls/planes documents exist; Ghostwine’s exact targeting/fear procedure remains unreviewed.','Attempt to use the general review as approval of Ghostwine or Sovereign Reserve.','Keep both whole item records pending specific review. No spirit identity, terminal recorder, protected information or new realm is inferred.')

    dependency_map={
        'CB-01':['CU-01-01','CU-01-02','CU-01-03','CU-01-13'],
        'CB-02':['CU-01-09','CU-01-10'], 'CB-03':['Actual cold-exposure scale/HZ-03; no universal Exhaustion or cold-resistance substitution'],
        'CB-04':['Actual seasickness checks/hazard cadence'], 'CB-05':['Meaning and ordering of fire resistance 1 against environmental heat'],
        'CB-06':['CU-01-10','Actual meal interval and check eligibility'], 'CB-07':['Actual sleep/vision/nightmare/save endpoint and player agency'],
        'CB-08':['CU-01-09','CU-01-12','Actual repeated brew serving policy'],
        'CB-09':['CU-01-02','CU-01-10','Actual fast-drinking threshold and fear entitlement expiry'],
        'CB-10':['CU-01-09','CU-01-12','CU-01-13'], 'CB-11':['CU-01-14','Actual receiving versus sending telepathy and named Bard Chant scopes'],
        'CB-12':['CU-01-14','Final sentence/record custody/protected information; specific actual GPT decision required'],
        'CS-01':['CU-01-04','CU-01-05','CU-01-06','CU-01-07','CU-01-08','CU-01-09','CU-01-12','Individual severe complication'],
        'CS-02':['CU-01-08','Actual qualifying sleep/rest anchors and nonretroactive first-failed-save rule','Individual severe complication'],
        'CS-03':['Selected real Wound penalty; temporary HP source and expiry; crash damage type','Actual benefit lock','Individual severe complication'],
        'CS-04':['CU-01-09','CU-01-14','Actual movement-detection predicate and known-position interface','Individual severe complication'],
        'CS-05':['CU-01-14','Ethereal/residue eligibility, range, barriers, actual spirit/corpse fear source and save DC','Individual severe complication'],
        'CS-06':['CU-01-09','CU-01-12','Spell-source damage root and reduction order','Individual severe complication'],
        'CS-07':['CU-01-09','CU-01-12','CU-01-14','Specific Unity-gain authorization and repeated-use meaning','Individual severe complication'],
        'CS-08':['Actual selected research work/check eligibility; finite concentration-penalty ending','Individual severe complication'],
        'CS-09':['CU-01-09','CU-01-13','Actual partial-day doubled-water accounting','Individual severe complication'],
        'CS-10':['Actual eligible melee damage packets, de-escalation checks and noncoercive scope','Individual severe complication'],
        'CS-11':['Actual available Hit Die/maximization/healing; Poisoned source suppression; accelerated dependence interpretation','Individual severe complication'],
        'CS-12':['CU-01-08','Actual ingestion/Action/entitlement and cone/DC/type/recoil','Locate or explicitly author the referenced Mutation complication table']
    }
    records=[]
    for r in old['records']:
        records.append({'id':r['questionId'],'name':r['name'],'family':r['family'],
            'sourcePointer':f"/{r['family']}/{r['sourceArrayIndex']}",
            'original':deepcopy(r['completeCoreJsonRecord']),'originalBookBinding':deepcopy(r['currentBookBinding']),
            'priorQuestion':r['question'],'currentDependencies':dependency_map[r['questionId']],
            'status':'original preserved; common-use proposal drafted; individual full operational profile and actual joint review still required',
            'individualOperational':False,'approved':False})
    # Bounded current-source discovery: retain every hit, not an assertion of global absence.
    terms=['mutation complication','seasick','cold-weather exposure','fire resistance 1','divination checks']
    search={'book':info(book),'xmlSha256':digest(xml),'indexConvention':'all descendant w:p in document order, zero-based','terms':terms,
        'hits':[{'paragraphIndexZeroBased':i,'exactText':s} for i,s in enumerate(paragraphs) if any(t in s.lower() for t in terms)],
        'scope':'This one current Core book only. These matches do not establish a full Mutation table or numerical environment scale; no universal absence claim.'}
    cosmic=[]
    def strings(value):
        if isinstance(value,dict):
            for x in value.values():yield from strings(x)
        elif isinstance(value,list):
            for x in value:yield from strings(x)
        elif isinstance(value,str):yield value
    for p in sourcepaths[-2:]:
        hits=[s for s in strings(read(p)) if any(q in s.lower() for q in ['ghostwine','sovereign reserve','ethereal creatures','spiritual residue','final spoken sentence'])]
        cosmic.append({'source':info(p),'terms':['ghostwine','sovereign reserve','ethereal creatures','spiritual residue','final spoken sentence'],'matchingStringValues':hits,'scope':'Bounded literal search of this current reviewed JSON, not proof of absent world concepts or absent other source evidence.'})
    assert not any(x['matchingStringValues'] for x in cosmic)
    model={'id':'CORE-CONSUMABLE-USE-DRAFT-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'LOCAL NEW discussion proposal. Unsubmitted, unadopted, not a completed consumable catalog.',
        'scope':'A shared actual-use/dose/tolerance/crash/maintenance proposal for finishing all24 source items. It explicitly preserves per-item unknowns instead of claiming that common rules finish their effects.',
        'sources':bindings,'exactGuideEvidence':evidence,'decisions':decisions,'itemRegister':records,
        'requiredDoseRecord':['recipientId','substanceId','eventId','completedAt','actualStockIds','doseUnits','toleranceBeforeEvent','restEpochId','restCountBeforeAndAfter','rollingDoseCount','dependenceSaveOrNot','overdoseConsequenceIdOrMissing','benefitRecordsAndFixedEndpoints','crashRecordsAndAppliedFlags'],
        'requiredIndividualProfile':['Original complete source record','actual dose/serving/container/mass','activation/target/ingestion legality','benefit including all printed clauses','eligibility and full duration/end conditions','stacking/repeated-use policy','crash timing/type/duration/removal','dependence/overdose severe complication for substances','physical source/price/availability','source-specific information boundaries','finite worked situations'],
        'sourceSearch':search,'currentCosmologyItemSearch':cosmic,
        'sourceInformationDeleted':0,'newRulesAdopted':False,'individualItemsPromoted':0,'runtimeImplemented':False,'humanPlaytested':False,'wholeGameApproved':False}
    # Validate exact original correspondence and authored example arithmetic, not gameplay behavior.
    checks=[]
    def check(name, value):checks.append({'name':name,'pass':bool(value)})
    check('all24 original complete objects preserved',all(x['original']==original[x['family']][next(y['sourceArrayIndex'] for y in old['records'] if y['questionId']==x['id'])] for x in records))
    check('all164 original section paragraphs remain exact',len(old['completeBookSections37And38'])==164 and all(paragraphs[x['paragraphIndex']]==x['exactText'] for x in old['completeBookSections37And38']))
    check('14 explicit unadopted decisions and28 unique authored situations',len(decisions)==14 and len(cases)==28 and len({c['id'] for c in cases})==28 and not any(x['adopted'] for x in decisions))
    check('seven-day boundary arithmetic',7*24*60*60==604800)
    check('tolerant duration and crash endpoints',600/2==300 and 300+3600==3900 and 600+3600==4200 and 900+3600==4500)
    check('healing examples use current stage/order',8//2-1==3 and min(8//4,8//2-1)==2)
    check('zero individual approvals or operational promotions',not any(x['individualOperational'] or x['approved'] for x in records))
    for p,binding in zip(sourcepaths,bindings):check('source unchanged '+binding['path'],info(p)==binding)
    assert all(x['pass'] for x in checks)
    root.mkdir()
    (root/'USE_MODEL.json').write_bytes(encoded(model)); (root/'CASEBOOK.json').write_bytes(encoded({'status':'Authored proposed adjudications, not runtime/human tests','count':28,'cases':cases}))
    lines=['# Core consumables — common-use discussion draft','',
        '**Local proposal, not jointly reviewed or adopted.** The 24 source brews/substances remain unchanged and individually unpromoted. This draft gives the next conference one concrete shared procedure to challenge, with explicit per-item dependencies. It is not permission to use incomplete item effects.','',
        '[Model and exact source evidence](USE_MODEL.json) · [28 authored situations](CASEBOOK.json)','',
        'The central source distinction is twelve magical substances with dependence DCs versus twelve brews without those DCs. The source supplies repeat-dose, tolerance and overdose concepts, but not a complete operational profile for every item.','']
    for d in decisions:
        lines.extend([f"## {d['id']} — {d['title']}",'',d['proposal'],'',f"**For actual GPT review:** {d['jointReviewQuestion']}",'',f"Evidence: {', '.join(d['sourceEvidence'])} in USE_MODEL.json.",''])
    lines.extend(['## Individual completion register','','Every item below still requires its complete individual effect and exact review; none is promoted by this shared proposal.','','| ID | Source name | Remaining individual/interface work |','|---|---|---|'])
    for r in records:lines.append('| '+r['id']+' | '+r['name']+' | '+'; '.join(r['currentDependencies'])+' |')
    lines.extend(['','The current Core search found the item references to Mutation complications, cold-weather exposure and seasickness, but did not establish their full procedures in that bounded matching set. The reviewed souls/planes JSONs contain no literal item-specific Ghostwine or Sovereign Reserve clause; that is not a general claim that spirit or death sources are absent. Actual item-specific conference remains necessary.','',
        'Nothing here changes the completed 687 crafting recipes, 419 reviewed ordinary spells, original books, approved condition recovery, cosmological identities or owner campaign era. Runtime, human playtesting, balance and whole-game approval remain open.',''])
    (root/'DISCUSSION.md').write_text('\n'.join(lines),encoding='utf-8',newline='\n')
    (root/'LOCAL_CHECKS.json').write_bytes(encoded({'checks':checks,'count':len(checks),'failures':0,'scope':'Original-source equality, stable authored IDs and selected arithmetic only; not execution of the proposed dosing rules.'}))
    manifest=[{'path':p.name,'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in sorted(root.iterdir()) if p.is_file()]
    (root/'MANIFEST.json').write_bytes(encoded({'files':manifest}))
    receipt.write_bytes(encoded({'recordedAtUtc':model['recordedAtUtc'],'status':'Local shared-use discussion proposal; not sent or adopted','model':info(root/'USE_MODEL.json'),'discussion':info(root/'DISCUSSION.md'),'cases':info(root/'CASEBOOK.json'),'checks':info(root/'LOCAL_CHECKS.json'),'sourceCount':len(bindings),'sourceItemCount':24,'sharedProposedDecisions':14,'authoredSituations':28,'individualItemsPromoted':0,'newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeImplemented':False,'humanPlaytested':False,'wholeGameApproved':False,'next':'Review the explicit rest-boundary/overdose/stacking choices with actual GPT; finish every item profile, including its real severe complication, before exact catalog review.'}))
    print(json.dumps({'preparation':info(receipt),'model':info(root/'USE_MODEL.json'),'sources':len(bindings),'items':24,'decisions':14,'situations':28,'checks':len(checks),'failures':0,'adopted':False}))

if __name__=='__main__':main()
