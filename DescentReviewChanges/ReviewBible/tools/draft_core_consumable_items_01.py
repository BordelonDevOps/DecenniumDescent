"""Draft individual item procedures; retain unresolved source choices without promotion."""
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
import hashlib,json,zipfile
import xml.etree.ElementTree as ET
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())
def digest(b):return hashlib.sha256(b).hexdigest()

def main():
    root=A/'core-consumable-items-local-draft-01';receipt=A/'CORE_CONSUMABLE_ITEMS_DRAFT_01_PREPARATION.json'
    assert not root.exists() and not receipt.exists()
    sharedpath=A/'core-consumable-use-local-draft-01/USE_MODEL.json';shared=read(sharedpath)
    assert len(shared['itemRegister'])==24 and not shared['newRulesAdopted']
    sourcepaths=[G/x['path'] for x in shared['sources']]
    sourcepaths.extend([sharedpath,
        R/'data/public/Decennium_Descent_Bard_Playtest_v0_1.json',R/'docs/mechanics/BARD_PLAYTEST_v0_1.md',
        R/'docs/mechanics/DAMAGE_SHARING_PLAYTEST.md',R/'docs/mechanics/SPELL_PLAYTEST_STARTER.md',
        R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',R/'docs/mechanics/ANCESTRY_BACKGROUND_PLAYTEST.md',
        A/'ENVIRONMENT_HAZARD_SOURCE_RECONNAISSANCE.json',
        G/'books/player/Decennium_Descent_Player_Rulebook_v6.docx',
        G/'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx',
        G/'docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx'])
    sourcepaths=list(dict.fromkeys(sourcepaths));bindings=[info(p) for p in sourcepaths]
    assert all(info(G/x['path'])==x for x in shared['sources'])
    bardpath=R/'data/public/Decennium_Descent_Bard_Playtest_v0_1.json';bard=read(bardpath)
    chants=[{'pointer':'/cards/'+str(i),'completeCard':c} for i,c in enumerate(bard['cards']) if 'chant' in c.get('tags',[])]
    assert {x['completeCard']['id'] for x in chants}=={'bard.base.chant-of-renewal','bard.arch.resonant-chant','bard.discord.chant-of-fear'}
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};searches=[]
    for p in sourcepaths[-3:]:
        with zipfile.ZipFile(p) as z:xml=z.read('word/document.xml')
        t=ET.fromstring(xml);ps=[''.join(n.text or '' for n in q.findall('.//w:t',ns)) for q in t.findall('.//w:p',ns)]
        hits=[{'paragraphIndexZeroBased':i,'exactText':s} for i,s in enumerate(ps) if 'mutat' in s.lower() and any(w in s.lower() for w in ['table','complication','overdose'])]
        searches.append({'source':info(p),'xmlSha256':digest(xml),'paragraphCount':len(ps),'indexConvention':'all descendant w:p, zero-based','predicate':'contains mutat and one of table/complication/overdose, case-insensitive','hits':hits})
    ingredients={x['id']:x for x in shared['itemRegister']}
    profiles=[]
    common={
        'status':'All new procedures below are LOCAL PROPOSALS for actual GPT review. No source item, global rule or recipe is promoted.',
        'authority':'Original item text, price, tier, description, legal label and dependence DC remain copied verbatim. Printed facts and new completions are distinct. The four held items have no usable full profile in this draft.',
        'administration':'Use shared CU-01-01–14 as proposed, not adopted law. Unless a profile says otherwise, a brew is one pint/1 lb liquid in an actual separately counted container, consumed over one uninterrupted active minute. A substance uses one ready oral dose, one Action, actual hand/access and an eligible recipient able to swallow. No forced dosing of an unwilling active creature is granted. Completion is T0; all stated minute/hour clocks are exact elapsed clocks from the named event, preserved across initiative and sessions.',
        'packaging':'NEW substance packaging: a liquid/sap/resin/suspension dose has 0.1 lb gross mass: 0.08 lb content and a retained 0.02 lb vial, ampoule or pot. Quickglass uses that prepared draught. Null Salt and Choir Dust use 0.02 lb paper packets, comprising 0.01 lb content and 0.01 lb retained wrapper. Spiral Ink is one consumed 0.02 lb marked wafer. Wyrmspice is one 0.02 lb packet with the same 0.01/0.01 split. Prices purchase the source unit, not free bulk ingredients. No unit has an inferred crafting recipe. Carry all remaining actual containers and contents once.',
        'doubling':'NEW preparation: with two actual substance units, an actual suitable empty vessel, one free hand and one Action, combine their complete contents into one ready doubled portion; original containers remain. This preparation is not consumption. The combined ready portion may then be administered with one Action. It counts as two doses in one event under the shared proposal and grants only normal potency/duration. No preparation resurrects spilled/partial material. Different named substances cannot be combined into an invented compound profile.',
        'magic':'NEW classification proposal: special effects of these brews/substances, their item-specific damage and listed adverse effects are magical nonspell item effects unless expressly described as ordinary hydration or physical bookkeeping. They do not have spell ranks, casting components, RP costs or class-cast triggers. Dependence/tolerance/consumption records follow the existing recovery system and are not erased by spell-only dispelling. An actual suppressor/cure must match its printed scope. Suppression never pauses clocks or produces a delayed duplicate damage event; an ongoing timed adverse record can operate again only during its original remaining duration when suppression ends.',
        'repetition':'Same-item numerical bonuses/penalties use the strongest rather than adding; advantage/resistance do not stack. Each actual dose retains its own benefit end and crash. Different actual damage, Intoxication, Unity or Strain gain events remain distinct. Shared one-use entitlement policy is proposed CU-01-10. Each substance overdose also applies the shared proposed dependence advancement; its item-specific severe complication below is additional to the ordinary later crash.',
        'life':'Apply ordinary immunity, life state, damage/Wound/death and condition-source rules. A dose is no resurrection or extra body. No effect compels a player’s beliefs, behavior or real disclosure. Physical consumption is never refunded by later death, transformation or redundant benefits. If a recipient is Dead at a due event, apply only effects that can actually affect that target; no living-target save, corpse farming or postponed damage packet is invented. Existing timed records retain original timestamps through any genuine restoration unless that restoration explicitly ends them.',
        'rest':'The shared proposed beneficial-Long-Rest boundary remains an unresolved joint choice. It controls the individual references to a qualifying Long Rest below. No currently approved rest or maintenance chapter is overwritten.',
        'damageReduction':'NEW item-integration choice: Embermark’s 1 and Null Salt’s PB belong to one eligible pre-resistance flat-prevention group with the existing strongest class flat reduction; choose its highest applicable value, not their sum. Resolve save half, then this flat group, then actual resistance/immunity and later finite prevention. Post-defense transferred damage skips a second defense/reduction stage. This explicitly extends a scoped class rule to these items and needs independent review.'
    }
    def item(i,benefit,ending,repeat,limits,overdose=None,unit=None,notes=None):
        s=ingredients[i]
        profiles.append({'id':i,'name':s['name'],'family':s['family'],'sourcePointer':s['sourcePointer'],'original':deepcopy(s['original']),'originalBookBinding':deepcopy(s['originalBookBinding']),
            'reviewReadiness':'individual-procedure-proposal','unitOverride':unit,'benefit':benefit,'endingOrCrash':ending,'repetitionAndTolerance':repeat,'limitsAndInterfaces':limits,
            'overdose':overdose if s['family']=='magical_substances' else 'Not part of the substance-dependence catalog. No unsourced generic overdose rule added; actual printed Intoxication and individual risks remain.',
            'newDesignNotes':notes or 'All missing quantities, triggers, limits and endpoints above are explicit NEW local choices. Original source record remains authoritative evidence, not silently replaced.',
            'approved':False,'activeOperational':False})
    def hold(i,reason,options,nextEvidence):
        s=ingredients[i];profiles.append({'id':i,'name':s['name'],'family':s['family'],'sourcePointer':s['sourcePointer'],'original':deepcopy(s['original']),'originalBookBinding':deepcopy(s['originalBookBinding']),
            'reviewReadiness':'specific-source-decision-required','reason':reason,'concreteAlternativesForJointDiscussion':options,'requiredEvidenceOrDecision':nextEvidence,'fullProcedure':None,'approved':False,'activeOperational':False})

    item('CB-01','One complete serving grants no Intoxication. NEW hydration credit: each actual pint swallowed counts as one pint toward this recipient’s ordinary water need. Incomplete but actually swallowed clean liquid can credit its known volume without granting a completed serving effect. It does not purify another liquid.',
        'No timed buff or later crash. No food credit is assigned: a reference to brewing calories does not quantify edible ration mass.',
        'NEW repeated-serving proposal: every actual serving retains its no-Intoxication property; no additional intoxication is inferred for an arbitrary second pint. Repeated hydration consumes real volume and never creates a Supply basket.',
        'Ordinary hydration is nonmagical. Food, oil, sundries, contamination and anatomy remain real. This explicit extension of the one-serving source to repeated servings must be reviewed, not treated as recovered text.')
    item('CB-02','For eight elapsed hours, the next saving throw actually imposed by ingesting spoiled food has advantage. Apply automatically before that eligible roll and spend the entitlement even on success. A spoiled-food source can cause poison or disease, but unrelated venom, a poisoned weapon or an already progressing illness does not qualify merely by its condition name.',
        'Entitlement ends on the first eligible save or at T0+28800 seconds. No cure and no later crash.',
        'One overlapping same-item entitlement; consuming it spends every overlapping copy under CU-01-10. A later actual serving can grant one new use, with its own deadline.',
        'No save is created if the food/hazard procedure calls for none. Immunity preventing an otherwise required save leaves this entitlement unspent; original expiry still occurs.')
    hold('CB-03','The source specifies the first level of cold-weather exposure without supplying that level’s mechanics. Current global Exhaustion is a different named track; the bounded source audit has not established a matching cold-exposure scale.',
        ['Preserve the wording literally and bind it to the first actual stage of a separately completed cold-weather hazard. That requires the hazard’s full threshold/cadence/recovery table; no invisible placeholder stage suffices.',
         'Explicitly replace the ambiguous clause with a reviewed new rule about one named cold-caused Exhaustion penalty. This changes the mechanical meaning and must state whether points, cumulative thresholds and death still count. It cannot be described as the original effect.'],
        'Confer on HZ-03 with the actual environment sources, then supply the exact chosen protection and four-hour timing. Do not import the later sky-voyage cold-inhalation proposal as global weather law.')
    item('CB-04','For eight elapsed hours, gain advantage on actual ability checks to resist or recover from seasickness. NEW bounded motion procedure: on rough waterborne travel, after ten continuous minutes of actual rough motion, make a CON ability check DC 12. Failure causes the local Seasick penalty: disadvantage on STR/DEX ability checks, no automatic attacks/saves/damage penalty. While rough motion continues, repeat once at each subsequent completed hour from that first check; success ends Seasick, failure applies/retains it. Do not create additional checks for changing seats, headings, initiative or sessions.',
        'The advantage expires at T0+28800; it does not itself cure an existing Seasick record. Ten uninterrupted minutes without rough motion ends this local Seasick penalty and resets the exposure clock. Returning to rough motion before those ten minutes complete retains the original clock and penalty.',
        'Overlapping grog doses do not stack advantage and retain individual endpoints. No invented drug dependence or generic Intoxication gain.',
        'This optional local motion hazard is NEW and must be reconciled with the environment chapter. Declare actual rough motion before its timer starts; ordinary calm transport creates no check. Poisoned immunity does not itself prevent this separately named motion penalty. No drowning, pressure, shiphandling or general balance benefit.')
    item('CB-05','For one elapsed hour, reduce each eligible environmental-heat fire-damage packet by 1, minimum zero, through the proposed shared pre-resistance flat group. Eligible: an actual ambient hot-air/sustained environmental heat hazard whose damage is explicitly fire. The Director identifies the hazard and packet before resolution.',
        'Ends at T0+3600. No later crash; no reversal of earlier damage.',
        'Same-item reductions do not add. Another actual dose has its own hour; no universal resistance multiplier is granted.',
        'Does not halve fire damage, prevent heat Exhaustion, stop suffocation or protect against direct attacks, weapon flames, Burning, a fire spell or touching a damaging hot object merely because its damage is fire. This interprets the source numeral 1 as flat reduction and needs explicit GPT confirmation.')
    item('CB-06','Designate the actual meal being eaten when consumption completes. Before one actual Nature or Performance ability check directly undertaken during that meal, choose to spend this entitlement for +1. NEW meal window: it remains eligible while that real meal continues, for at most one elapsed hour from T0; leaving/completing the meal ends it. A pause shorter than ten minutes does not by itself end the meal, but ten continuous minutes of unrelated activity does.',
        'Ends on the chosen check, the end of that meal or T0+3600, whichever comes first. No later crash.',
        'One same-item entitlement across overlapping servings, not several queued +1 bonuses. It supplies no entire research-project reward and cannot affect a roll after the meal has ended.',
        'There must be an actual task and check. Talking about a plant or singing does not force a roll, grant proficiency or invent a completed research finding.')
    item('CB-07','During the next actual sleep episode beginning within 24 hours of T0, after one uninterrupted hour of sleep, experience one symbolic dream. The player selects a true emotional fact about their own character, or an agreed neutral surrogate, and chooses how to express it. It reveals no other person’s mind, hidden world fact, soul identity or mandatory character trait. At that completed dream, make WIS save DC 13.',
        'Failure produces vivid fictional nightmares and a NEW one-hour disadvantage on WIS (Perception) checks after actual waking. Success produces no penalty. The dream does not automatically interrupt the sleep or invalidate an otherwise legal rest. If the qualifying one-hour dream never completes by T0+24 hours, this dose expires unused with no penalty.',
        'Overlapping doses yield one dream event for that sleep episode; all eligible overlapping dream entitlements are spent. One save resolves the overlapping same-item nightmare risk; no repeated compelled confessions. Later distinct doses can affect a later actual sleep.',
        'This NEW sleep threshold, DC and waking penalty complete missing mechanics. A creature that cannot sleep receives no dream by asserting a rest. The player may summarize without acting out a nightmare or exposing private information.')
    item('CB-08','Increase walking Speed by 5 ft for ten elapsed minutes. Use current ordering: sum legal flat changes, then applicable multipliers and flooring; an effect setting Speed 0 still controls. Derived movement modes use their own actual rules.',
        'At this serving’s actual benefit end, gain one dose-driven Intoxication point through the existing track. An actual early-ending effect triggers that point under shared CU-01-09; suppression retains the original timer. It is not a two-hour generic Intoxicated floor.',
        'No stacking +5 from multiple servings. Each completed serving has a real end and one later Intoxication gain, even while another still supplies Speed. No crash is removed by changing sessions or ending combat.',
        'Intoxication recovery and thresholds remain current. A drinker who cannot gain Intoxication uses that actual qualified protection; no immunity is inferred from being a Warrior or using a serum.')
    item('CB-09','Gain one fear-save advantage entitlement for NEW eight elapsed hours. Choose to spend it before a real save to prevent or end Frightened or another effect explicitly identified as fear. It is separate from the Intoxication track’s episode entitlement, while advantage still does not stack.',
        'Safe consumption takes one uninterrupted minute. Choosing the NEW rapid option consumes the full ready serving with an Action and deals 1 fire damage immediately after completion, through actual defenses/life rules. The entitlement is still granted if the recipient survives; fire resistance can round that 1 to 0. No other later crash.',
        'One overlapping same-item fear entitlement under CU-01-10, expiring no later than its actual eight-hour endpoint. Every actual rapid serving has its own 1-fire event; no duplicated bonus from several unspent servings.',
        'No extra Action, automatic fear immunity or forced drinking. The eight-hour expiry and fast/safe timing are NEW proposed completions.',unit='NEW exception: one 2-fluid-ounce serving, 1/8 pint, 0.125 lb liquid plus actual container. Printed 10 gp is per such proposed serving.')
    item('CB-10','For 24 elapsed hours suppress the sensation of hunger and apply a local −1 flat modifier to each actual healing-received event, minimum zero. This does not consume or satisfy food/water/Supply requirements. Apply the modifier once at the compatible flat-reduction stage after applicable fractional multipliers, before caps.',
        'At T0+86400, or actual early end, hunger sensation and ordinary healing handling resume. Suppression of the item removes only its currently operative modifiers while timers continue. No refund of missed food and no retroactive HP restoration.',
        'Same-item −1 applies once while any copy is active. Do not subtract twice from one event or numeric add-on. A genuinely separate child healing event uses its own actual recipient and source rules. Under Blight Totem compare allowed local-reduction plans rather than compounding Totem with this local reducer.',
        'State recovery from natural-20 death save or Stable recovery is not a healing effect and keeps its guaranteed 1 HP. Temporary HP are not healing. This item does not lower maximum HP or remove Wounds.')
    item('CB-11','For one elapsed hour, the drinker does not receive whispered sound or inbound telepathic messages. NEW acoustic boundary: a deliberate whisper is a voice intentionally kept below ordinary conversational volume at its source; lowering volume after speech was heard does not undo it. The effect does not make the drinker generally Deafened, block ordinary speech/instrument sound or erase language knowledge. An independently legal outgoing mental channel can still send, but this item grants no channel or translation. A dialogue requiring an incoming reply cannot succeed without it.',
        'While active the drinker cannot receive a beneficial effect whose applying Bard card is actually tagged chant. Current exact cards: Chant of Renewal, Resonant Chant and Chant of Fear; the last is normally harmful, so ordinary audible hostile fear is not made harmless by the no-benefit clause. Block ongoing beneficial Chant modifiers while this dose operates, and new eligible healing/tempHP/condition-removal grants. Do not remove HP already healed before the dose. Ends at T0+3600.',
        'Overlap extends actual coverage only through real individual deadlines. NEW tag-based choice: an independent Echo card is not automatically a Chant merely because its legal stored number came from a Chant. Its actual hearing/cost/source rules still apply; a blocked Chant that healed nothing does not fabricate an Echo source. A named residual/passive card needs its own actual applying identity, not an invented inherited tag.',
        'The drinker may still perform a legal audible Chant for other recipients; their own benefit is blocked. Incoming whispers/telepathy cannot bypass audible V or Bard hearing gates. No immunity to ordinary psychic damage or all mental magic is granted. The tag-based Echo/residual boundary requires explicit GPT review.')
    hold('CB-12','Final spoken sentence, unique vintage and records every drinker do not identify a terminal event, recording medium, retrieval method, duration or protected-information boundary. The current soul/death review is not a specific item verdict.',
        ['A drinking-occasion interpretation would record the last complete audible sentence of each actual serving scene. It requires an explicit scene endpoint, physical recorder/custody, access and persistence rules and changes the implied death-related reading.',
         'A final-life interpretation would record the last sentence before actual true death. It requires explicit rulings for distance, silence, resurrection, Hunt death, memory/identity, destroying the vessel, access and whether it knows unwitnessed speech. None is inferred from the name.'],
        'Discuss the two readings with actual GPT against original sources and owner corrections. Preserve State-controlled as the exact price field; no invented gp value or availability. No operative terminal recorder is selected here.')

    item('CS-01','For ten elapsed minutes, gain +10 ft walking Speed and advantage on an actual new initiative roll. Apply flat Speed before multipliers/zero overrides. Entering or changing initiative does not create a gratuitous reroll or restart the clock.',
        'At each actual benefit end add +1 expedition Strain and impose disadvantage on DEX ability checks for one elapsed hour. The Strain gain uses its actual potentially lethal track; the check penalty includes initiative when it is actually a DEX check but never reorders established combat. These consequences have independent recovery/endings.',
        'Tolerance halves the 600-second benefit to 300 seconds, not the 3600-second crash. Two doses at different times retain both crashes; Speed/advantage do not add. A doubled event restores normal benefit duration with two real units.',
        'No Warrior serum Strain, extra turn, extra Action or unqualified Exhaustion substitution.',
        overdose='NEW severe complication at each overdose event: take 1d6 lightning damage and become Stunned for six elapsed seconds. Apply actual defenses, life and Stunned immunity; the later normal crash remains. This is an item-specific proposal, not an existing drug table.')
    hold('CS-02','The crash says the first failed Wisdom save is made with disadvantage, which requires a failure to determine how its own dice were rolled. Sleep, directed vision, Divination checks and next-rest anchors also need explicit definitions.',
        ['Explicit editorial replacement: after waking, the next actual WIS save before the next qualifying rest has disadvantage. It is simple and finite but changes first failed to next and must be approved as a NEW replacement, not paraphrased source.',
         'Literal conditional-pool model: predesignate two dice for each prospective WIS save; compare ordinary and additional-disadvantage interpretations from that same pool, applying the latter only if the ordinary result fails. This preserves the failure-gated wording but needs exact advantage, reroll, replacement and save-margin windows before use. No second retroactive save is assumed.'],
        'Choose the crash interpretation with actual GPT. Then define one real sleep/vision, knowledge and player-agency boundary, eligible existing skill checks (Divination is not a new free proficiency), next-rest endpoint, tolerance handling and an item-specific overdose. No full effect is active from this draft.')
    item('CS-03','On a legal dose grant temporary HP equal to 2×current actual PB, through existing nonstacking tempHP choice rules, for at most ten elapsed minutes. Choose one actual Wound record when consuming: ignore only that record’s −1 to CON saves during the same interval. No Wound is removed, no Hit-Dice recovery penalty is ignored, and the actual count, Critical Speed/healing ceiling, linked Injury and fatal subsequent Wound save remain.',
        'At the ten-minute or actual early benefit end, end this dose’s unspent temporary HP and CON-penalty exception, then take 1d6 NEW necrotic crash damage. The recipient cannot gain this item’s benefit again until an actual qualifying Long Rest after the dose. The lock begins at dose completion so repeated overlap cannot avoid it; a rest before the running dose ends does not release that current lock until its end.',
        'Tolerance halves the timed benefits to five minutes; the instant numeric offer remains 2×PB, not twice again for a doubled dose. A deliberately consumed dose while benefit-locked still consumes stock, enters dose history and schedules its own crash at the normal/tolerant endpoint, but grants no prohibited benefit.',
        'Choosing a Wound for its CON penalty is independent of tempHP. With no Wound, grant only the otherwise legal tempHP. A chosen record later removed cannot be replaced by a newly gained Wound without a new eligible dose. Crash damage uses ordinary Wounds/death and is not an HP cost.',
        overdose='NEW: immediately take 1d6 necrotic damage and gain Poisoned for one elapsed hour, subject to actual immunity. This is separate from the scheduled ordinary 1d6 crash; it does not erase the benefit lock.')
    item('CS-04','For one elapsed hour gain darkvision out to 120 ft, using the current ordinary darkvision rules; use the greater actual range, never add ranges. NEW movement sense: with functioning sight, immediately learn the current occupied space(s) of an actually Invisible creature when it makes nonzero physical displacement within 10 ft and has a clear unobstructed sight path. Its stationary presence, teleport disappearance/arrival without a traversed local path, sounds or vague nearby magic do not trigger this movement-only sense. The known position is information for this observer, not visible anatomy.',
        'At benefit end the granted darkvision/movement sense cease. For the next elapsed hour, bright light gives disadvantage on sight-based ability checks. Darkness/dim light does not trigger that crash penalty. It is not Blinded and gives no generic attack/save penalty.',
        'Tolerance halves only the 3600-second benefit. Repeated sensing is permitted for actual separate movement while active; it does not refresh the dose. Overlapping crashes use one same-type disadvantage but retain individual expiry.',
        'Ordinary known-position/Hidden/Invisible rules apply; do not impose Invisible’s own modifiers after knowledge merely because it is still Invisible. Independent darkness, smoke or blindness can still matter. No sight-required spell target or attack through a wall is granted.',
        overdose='NEW: Blinded for ten elapsed minutes, subject to actual immunity. This prevents the proposed eye-dependent movement sense while it operates; it does not pause the original benefit/crash clocks.')
    hold('CS-05','The source’s ethereal creatures, spiritual residue and nearest spirit/corpse are not an operational target taxonomy. No item-specific definition was found in the reviewed souls/planes JSONs; generic perception is not a license to identify souls or bypass protected information.',
        ['A strictly source-qualified local sense could reveal only entities/residue whose actual established profile explicitly qualifies, with a printed finite range, line-of-effect rule and no soul identity/truth revelation. Compile those real eligible profiles before claiming usable coverage.',
         'A broader new spiritual sense would need an explicit new taxonomy and owner/GPT source reconciliation, including residue creation/persistence, corpse versus active Undead, invisibility/planes and protected records. Do not substitute generic omniscience.'],
        'Actual joint decision must define eligible real source profiles, ten-minute sense, fear-source selection/ties/range, WIS DC, one-minute fear ending, tolerance and specific overdose. Preserve dependence DC15 and75gp. No spirit/corpse identity or new realm is invented here.')
    item('CS-06','For one elapsed minute gain advantage on saving throws directly imposed by actual spells, and reduce each direct incoming spell-damage packet by actual PB through the proposed pre-resistance flat group. Periodic damage from that actual spell qualifies; an independent weapon attack by a summoned creature, a magical class technique, an item, a nonspell Echo or a hazard merely near a spell does not. A post-defense transfer is not defended again.',
        'At benefit end the recipient cannot spend Resonance Points for ten elapsed minutes. This blocks RP spending on ordinary spells and actual class techniques alike; a truly zero-RP legal effect remains governed by its own costs and restrictions. RP recovery is not prohibited, but recovered RP still cannot be spent until this record ends.',
        'Tolerance halves benefit from60 to30seconds, never the600second RP lock. Independent locks overlap without adding a second counter; the restriction remains while any is active. Same-item PB reductions do not add.',
        'No Oracle RC prohibition, spell immunity, class-cast permission, free costly material or canceled concentration merely from this effect. Limiting the source’s advantage against spells to actual saves and joining the flat group are NEW choices requiring review.',
        overdose='NEW: immediately create a separate one-hour prohibition on spending RP. It does not alter RC or remove existing RP, and the later ordinary ten-minute lock retains its own endpoint.')
    item('CS-07','For ten elapsed minutes gain advantage on actual CHA ability checks and resistance to psychic damage. This does not improve CHA saves, dictate another character’s response or identify true resonance.',
        'At benefit end gain +1 Unity Exposure through the currently reviewed public provisional track. The gain is a new item-source authorization proposed here; all track caps, interruption of Anchor Projects and player agency remain current. Repeated use’s false-resonance/identity-loss language is represented only by those accumulating public track effects and voluntary fictional portrayal in this proposal, not forced beliefs or new cosmic truth.',
        'Tolerance halves only the benefit. Each actual dose supplies its own eventual +1 Exposure; no numerical stacking of resistance/advantage. Being at the cap still records a positive unprevented gain event under the actual track.',
        'This finite mechanical interpretation of repeated-use risk requires explicit joint review. No research taint, Hunt mark, class feature, recovered Equation fragment or general soul penalty is added.',
        overdose='NEW: immediately gain one additional Unity Exposure through the same track. The ordinary later +1 still occurs. No independent mind-control, alignment or identity-removal result is invented.')
    item('CS-08','At consumption identify one actual research project and its question, a lawful existing Arcana/History/Religion/Nature/Engineering task and the real available evidence/work method. For eight elapsed hours add +2 to the recipient’s relevant ability checks directly advancing that identified project, when their actual required work/check completes during the window. No proficiency, subject access, Equation qualification, free progress or additional skill called Research is granted.',
        'When the benefit ends, NEW finite crash: for up to eight elapsed hours, disadvantage on CON concentration-maintenance saves until the recipient completes ten uninterrupted active minutes of feasible work on that same question, or the question is actually answered by the legitimate project. A statement of intent is not work. The person may choose another activity and bear the finite penalty; no forced conduct. Legitimate already completed answers prevent an impossible obligation. Actual evidence access and qualifications remain required; ten minutes is not automatically a complete finding.',
        'Tolerance halves the eight-hour benefit to four hours, not the eight-hour maximum crash. Same-project +2 does not add; different projects keep separate eligibility. Concurrent identical crashes may be satisfied by the same ten minutes of actual work on that one question, but different projects require their own compatible real work, not duplicate time.',
        'The source’s concentration checks is NEW interpreted as actual concentration-maintenance saves, not all checks while concentrating. A first failed save ends concentration normally; later crash time still remains. No automatic spell or research promotion.',
        overdose='NEW: Incapacitated for one elapsed minute, which ends concentration under current rules. It does not force voluntary movement, speech loss or pursuit of a question, and ordinary later crash remains.')
    item('CS-09','For one elapsed hour breathe water as well as retain any ordinary air-breathing ability, and gain swim Speed equal to current effective walking Speed. Recompute when that walking Speed changes. Do not apply a shared flat penalty/Exhaustion multiplier twice to an already derived swim value. Actual Speed 0 gives0; no movement Action, pressure immunity, water speech/V component or hands are granted.',
        'At benefit end ordinary breathing abilities remain and this dose’s swim grant ends. For the next eight elapsed hours double actual water requirement only. NEW accounting: at each canonical daily settlement, extra pints equal the integral of the recipient’s otherwise applicable daily water rate during the union of active Deep Blue crash intervals, divided by86400. For a constant normal Small/Medium8-pint day, eight hours of crash adds8/3pints. Split intervals at day boundaries and actual requirement changes; no rounding away fractions.',
        'Tolerance halves the one-hour benefit, not eight-hour thirst. Overlapping same-item thirst records double the underlying rate once during their union, not4×/8×. Actual water consumed credits the same daily ledger once. A genuine0water requirement doubles to0; no new requirement is invented for that anatomy.',
        'If expiry leaves a submerged creature unable to breathe, use its actually established breathing/drowning procedure; the item grants no free surfacing. The water formula is a NEW integration proposal, not recovered physiology, and does not double food, oil or sundries.',
        overdose='NEW: gain one global Exhaustion level at the overdose event, through its actual six-level track and life rules. This does not replace or satisfy the normal thirst crash.')
    item('CS-10','For ten elapsed minutes gain fire resistance and add +1 to one damage component of each actual melee attack that hits and would otherwise have a positive rolled/base damage amount before defenses. Choose an existing component at declaration, using its type; no new type is invented. It includes legal melee weapon, unarmed, natural or melee spell attacks; it excludes a melee-range save effect, miss, damaging aura or a new secondary damage trigger. Add once per attack, not once per die or component.',
        'For one elapsed hour after benefit end, disadvantage on ability checks whose declared purpose is to de-escalate an actual conflict. Declare that purpose before rolling. Other social checks, CHA saves and the player’s ability to choose peaceful behavior remain unchanged.',
        'Same-item resistance and +1 do not stack; distinct actually legal melee attacks can each receive the +1 while active. Tolerance halves benefit to five minutes, not the crash hour. Independent crash sources retain real expiries.',
        'The added point follows the attack’s ordinary defenses and damage-root rules; it is not an additional hit/packet or an extra critical die. No automatic ignition or compulsory aggression.',
        overdose='NEW: immediately take1d6fire damage, then suffer disadvantage on WIS saves for ten elapsed minutes. Apply any actually operative fire resistance, including this dose’s already active benefit, without deleting the later normal social crash.')
    item('CS-11','Before voluntary activation choose one actual unspent Hit Die from the recipient’s real pool. On completion spend it immediately and maximize its die face for one ordinary healing event, adding the recipient’s actual CON modifier under this NEW healing interpretation, minimum base0 before other lawful modifiers. It is a die-based heal for existing modifiers; no Short Rest or free die is created. Also suppress the Poisoned condition for one elapsed hour: existing and later actually applied Poisoned source records remain, but their condition penalties are inactive during suppression.',
        'At hour end only still-present, unexpired and uncured Poisoned sources operate again. Do not reapply an ended poison or pause its timers. Independent poison damage, disease, dependence and non-Poisoned penalties were never removed. NEW accelerated-dependence completion: make this item’s CON dependence save on every actual use, including the first, at most once per event.',
        'The instant maximized die is not halved by tolerance; its one-hour Poisoned suppression is. Every benefiting use spends a separate available die. With no die, a voluntary benefit attempt is rejected before payment; deliberately consuming anyway still spends the dose/history and resolves dependence/overdose but grants no healing or suppression. Existing HD recovery limits/Wounds remain.',
        'The recipient must be a legal ordinary-healing target with that actual die; no corpse revival. Wounds reduce actual HD recovery, not each maximized die’s result. Actual healing reductions/caps and TempHP distinctions still apply. Requiring the die for both benefits and the first-use save need joint review.',
        overdose='NEW: gain one global Exhaustion level immediately under the current track. The normal accelerated dependence save and future Poisoned-source reappearance remain independent.')
    item('CS-12','At consumption choose acid, cold, fire, lightning or thunder (NEW finite elemental list). Gain one breath entitlement lasting NEW one elapsed minute. Using it requires a later actual Action, a mouth/airway capable of exhaling, and an actual chosen direction; it does not require audible speech or a V component. Every creature, including allies, in the15ft cone with line of effect makes DEX save against NEW DC8+actualPB+actualCON modifier. Roll3d6 once; each failure takes full, success half rounded down, then actual defenses.',
        'At completion of the breath, or expiry/actual early loss of an unused entitlement, take1d6damage of the chosen type once for that dose. Actual resistance/immunity applies. NEW geometry follows the stated15ft cone construction in Burst of Flamewind as a proposed reusable template: origin at edge of user space, excluded; length15, diameter equal to forward distance. Include a creature once when the center of at least one occupied square is within/on its footprint; use matching actual height/volume and total cover. This copies geometry only, never Flamewind’s targeting, automatic damage or push.',
        'Tolerance halves the entitlement window to30seconds, not damage dice or recoil. A doubled dose never gives two breaths or6d6. Multiple overlapping same-item entitlements obey CU-01-10: one breath spends all overlapping entitlements, with each consumed dose’s own recoil resolved once. A later actual dose can grant a new opportunity subject to its real dependence/overdose rules.',
        'No separate object damage, lingering area, ignition, forced movement, roar/hearing gate or class breath-weapon use is granted. The chosen type cannot be changed after seeing targets/save results. This new activation/DC/window/template and the proposed replacement Mutation table all require explicit review.',
        overdose='Roll one d6 on the NEW six-row Wyrmspice complication proposal at the overdose event; apply that one result and the shared proposed dependence advancement. Ordinary breath/expiry recoil remains separate. The original referenced Mutation complication table has not been recovered in the bounded inspected primary-book search.')

    mutations=[
        {'roll':1,'name':'Trembling hands','effect':'Disadvantage on DEX ability checks for one elapsed hour. No extra attack/save penalty or lost anatomy.'},
        {'roll':2,'name':'Muscular contraction','effect':'Disadvantage on STR ability checks for one elapsed hour. No automatic Grappled, lost equipment or forced movement.'},
        {'roll':3,'name':'Vocal distortion','effect':'Cannot provide audible V components, command words or an audible Bard performance for one elapsed hour. Ordinary communication remains possible in a strained voice; this is not the complete Silenced condition and grants no immunity to sound.'},
        {'roll':4,'name':'Light sensitivity','effect':'Disadvantage on sight-based WIS (Perception) checks in bright light for one elapsed hour. No blindness, general attack penalty or new sense.'},
        {'roll':5,'name':'Rigid limbs','effect':'Walking Speed −10ft, minimum0, for one elapsed hour. Apply before actual multipliers; an existing zero-Speed rule still controls. Derived modes use their own rules.'},
        {'roll':6,'name':'Elemental feedback','effect':'Immediately take1d6damage of this dose’s already chosen type and gain one global Exhaustion level, resolving actual damage/life before a later living-target gain. This is additional to that dose’s later ordinary recoil, not a recurring pulse.'}
    ]
    mutation_scope='Entire table is NEW local temporary-complication authorship, not recovered Core canon. Results1–5 retain separate source/end records; duplicate same-row modifiers do not add but remain until all copies end. Different lawful results can coexist. A genuine effect explicitly ending that named source can act; a generic Poisoned cure does not remove non-Poisoned mutations. These results grant no Warrior mutation slot, ability, ancestry, permanent cosmetic identity or cosmic revelation.'
    profiles.sort(key=lambda p:p['id']);assert len(profiles)==24
    held=[p['id'] for p in profiles if p['reviewReadiness']=='specific-source-decision-required'];assert held==['CB-03','CB-12','CS-02','CS-05']
    byid={p['id']:p for p in profiles}
    scenarios={
        'CB-01':[
            ('One real pint','Normal8-pint water day, no water yet; consume one proposed serving.','Credit1pint water and0food/Supply baskets; no Intoxication. Actual pint is gone and container remains.'),
            ('Repeated serving choice','Consume a second actual serving.','Under the explicitly NEW repeat proposal, total2pints hydration and no Intoxication. This extension of the source’s one-serving clause still requires GPT approval.')],
        'CB-02':[
            ('Spoiled food','Entitlement active; actual spoiled-food hazard requires aCONsave.','Advantage applies and the one entitlement is spent before result; no illness cure afterward.'),
            ('Different poison','Same entitlement active; bitten by an unrelated venomous creature.','No advantage from this brew; its entitlement/expiry remain. Poisoned as a shared condition label does not establish spoiled-food origin.')],
        'CB-03':[
            ('Undefined stage','A referee proposes that first cold exposure means global Exhaustion1.','No adopted conversion exists. Keep the item held until the exact cold stage/meaning is jointly chosen.'),
            ('Sky-voyage shortcut','A draft upper-atmosphere inhalation event deals cold damage and thin-air Exhaustion.','Do not treat that local draft as the missing global cold-weather level table or grant general cold resistance.')],
        'CB-04':[
            ('First motion check','Rough water motion beginsT0; grog active. At600seconds CONcheck rolls4and16, modifier0.','Advantage gives16, meetingDC12; no Seasick. Next continuous-motion check4200, not another check on seat change.'),
            ('Actual recovery','Already Seasick; motion stops, then restarts after9minutes.','No ten-minute recovery completed, so penalty/original clock remain. Ten uninterrupted steady minutes would end it; brew expiry alone would not.')],
        'CB-05':[
            ('Environmental flat reduction','Eligible heat hazard deals5fire; no save/classDR; actual fire resistance also active.','Proposed flat1 gives4, resistance halves to2. Porter alone would give4, not2.'),
            ('Combat fire','A fire spell deals5fire to the same drinker.','Porter gives no reduction because this is direct spell damage. Any independently real fire resistance still applies.')],
        'CB-06':[
            ('One meal check','During the actual meal, a real eligible Nature check is declared; base total14 against15.','Choose entitlement before roll; +1 gives15 before the actual natural-die degree shift. It is one real task, not automatic research completion.'),
            ('Late project','The meal ended; a four-hour research finding later completes.','No wine bonus from the ended meal window. An earlier conversation does not extend the meal or grant project credit.')],
        'CB-07':[
            ('Player-owned truth','DoseT0; sleep1h actually completes beforeT0+24h; WISsave total12.','Player chooses an emotional fact/surrogate; DC13fails. On waking, one-hour Perception-check disadvantage; no automatic lost rest or imposed private belief.'),
            ('No sleep','A creature completes a source-defined rest without sleeping, or wakes before one continuous hour.','No completed dream, no invented sleep requirement or truth. If none completes by24hours, entitlement expires unused.')],
        'CB-08':[
            ('Speed ordering','Base walking30; Ale+5; actual Exhaustion2half; no other modifiers.','Effective walking Speed floor(35/2)=17. At its own benefit end gain the one printed Intoxication point.'),
            ('Overlapping ends','Servings completedT0 andT0+300; no ending suppression.','Speed bonus stays+5, not+10. Gain Intoxication at600 and900 separately; the second dose does not defer the first crash.')],
        'CB-09':[
            ('Rapid resistant drink','Consume the0.125lb serving with the rapidAction; actual fire resistance.','One-fire packet halves to0; a lawful fear entitlement still exists. No extra Action or universal fear immunity.'),
            ('Two fear sources','Brandy entitlement and Intoxication episode entitlement both available.','They cannot create double advantage. Spending Brandy does not automatically spend the independent episode use unless its own actual choice is made.')],
        'CB-10':[
            ('Healing and Totem','Baseheal8, systemicCorruptedhalf, both BlightTotem andCask.','Compare Totem plan2 with Cask plan3, choose2. Do not compound to1 or subtract twice from the same event.'),
            ('No nutrition','Hunger is suppressed, but actual food requirement goes unmet at daily settlement.','Use the actual one-Strain-per-unsupported-day procedure; sensation is not food and no water/oil/sundries appear.')],
        'CB-11':[
            ('Chant pulse and harmful fear','Drinker hears ordinary-volume Chant of Renewal and later Chant of Fear.','No Renewal healing/beneficialrider. Fear still uses its actual save because no-benefit does not grant harmful-Chant immunity.'),
            ('Echo identity','A legal non-Chant Echo stores a real prior Chant heal on a different eligible ally; its actual target/hearing rules are met.','Under this explicit tag-based proposal, the Echo is not automatically banned as a Chant. No blocked zero-heal event may be fabricated as its source; joint review must confirm this boundary.')],
        'CB-12':[
            ('Resurrection ambiguity','A former drinker dies, is genuinely restored, and later speaks/dies again.','No choice between first terminal sentence and eventual last sentence is made here. Preserve both source and unresolved terminal-record question.'),
            ('Unwitnessed speech','A drinker speaks privately far from the unique vintage.','No omniscient recording/retrieval, soul identity or hidden information is granted by the uncompleted source row.')],
        'CS-01':[
            ('Tolerant normal crash','One tolerated single dose completesT0; benefit duration300.','At300 gain1expeditionStrain and DEX-check disadvantage until3900. No serumStrain or half-hour crash substitution.'),
            ('Third-dose complication','Third dose since proposed qualifyingrest, no applicabledefenses; overdoseroll4.','Immediate4lightning and6secondsStunned plus shared proposed dependence advancement; actual later normalcrash remains. Apply real life rules if damage is fatal.')],
        'CS-02':[
            ('Failure-gated dice','First ordinary WISsave succeeds.','Literal first-failed wording should not be silently spent here; the simpler next-save replacement would differ and requires an explicit decision.'),
            ('Advantage and margin','An advantaged normal save would fail by1; a different conditional die pool could fail by5.','The crash can affect a source-defined failure margin; do not declare it meaningless or retroactively roll an unapproved second save. Hold full procedure until the dice window is chosen.')],
        'CS-03':[
            ('Actual Wound count','PB3, two real Wounds; choose one record, accept6tempHP.','CONsave penalty becomes−1 during the selectedexception, not0; actualtwo Wounds, HDrecovery andlinkedInjuries remain. Third/fatalWound rules use actual count.'),
            ('Benefit lock','A second serving is deliberately swallowed before the required qualifyingrest.','No new tempHP orWoundexception; actualdosehistory/cost and its eventualcrash still occur. No overlap loophole by dosing before the first10minutes end.')],
        'CS-04':[
            ('Invisible movement','Invisible creature moves inside10ft behind no barrier; drinker has functioning sight.','Learn its actualposition under the proposed sense; do not grant true sight. Apply current Invisible-known-position exception and any independent obscurity separately.'),
            ('Wall or stationary target','Invisible creature stays still or moves behind totalopaqueobstruction.','No movement-sense acquisition through the wall or from stationarypresence. No magical target eligibility is invented.')],
        'CS-05':[
            ('Nearest untyped object','An ordinary corpse and an alleged spirit are near the drinker.','Do not invent spiritual/ethereal eligibility, range/tie selection or a WISDC from the name. The entire operational profile remains held.'),
            ('Protected knowledge','A general souls model exists but no Ghostwine-specific perception verdict.','The item does not automatically reveal ownership, identities, Hunt records or absolute cosmic truth.')],
        'CS-06':[
            ('Save then flat then resistance','Spell rolls13damage; save succeeds; PB3 reduction and actual matching resistance; no strongerflatDR.','13/2floor=6, subtract3=3, resistancefloor=1. A redirectedpost-defense portion does not run this reduction again.'),
            ('RP and RC','Normal benefit ends;600secondRPspendlock begins. OracleRC and actualRP both present.','RPspending blocked; RC unaffected by name. A zeroRP legal effect still needs its actualcomponents/othercosts and cannot relabel paidRP asfree.')],
        'CS-07':[
            ('Dose and laterExposure','First ordinary dose benefit expires while AnchorProject isactive.','Apply proposedactual+1Unitygain; realtrack interrupts project evenatcap ifgainunprevented. NoHuntmark/Equationknowledge/forcedbelief follows.'),
            ('Overdose and normalcrash','An overdose event occurs; normalbenefitwillendlater.','OneadditionalUnitygainnow and oneordinarygainlater, through actualtrack. No separate identity-deletion mechanic is invented.')],
        'CS-08':[
            ('Finite researchbonus','A validchosenfour-hourfinding completesinside the8hwindow.','+2toits actualeligiblecheck only. No autoqualification, extra finding, borrowed proficiency or clock halving.'),
            ('Choosing not to pursue','Atbenefitend thequestionisnotanswered andnoactualworkcanbedone.','Concentration-maintenance savedisadvantage lasts atmost8h. Playercanleaveorchooseotherwork; no indefinitecompulsion or invented10minuteanswer.')],
        'CS-09':[
            ('Split-day water','Baseline8pints/day; crashactivefourhoursbeforedayend andfourafter.','Eachday gains8×4/24=4/3extra pints. Totalextra8/3. Actualconsumptioncreditsonce; overlappingcrashescountuniontime.'),
            ('Derived swim speed','EffectivewalkingSpeed15afterrealmodifiers; DeepBlueactive.','Granted swim15, not7 fromhalvingagain. If actualwalking becomes0, thisderivedswim becomes0; nofreebreathingafterexpiry.')],
        'CS-10':[
            ('Mixed melee damage','One legalmeleeattackhaspiercing+firecomponents; choosepiercingfor+1beforetheroll.','Addonepointtopiercing,notonepercomponent/die. It isnotanotherhit orcriticaldie; actualdefensesapply.'),
            ('Peaceful choice','Crashactive; actornegotiatesceasefirewithanactualPersuasioncheck, thensellsordinarysupplies.','De-escalationcheckhasdisadvantage. Ordinarysalescheckdoesnotunlessitactuallyservesthatconflictpurpose. Characterisnotforcedtoattack.')],
        'CS-11':[
            ('Maximized die remains spent','Availableactuald8, CON+2, ordinaryhealingeligible, noneothermodifiers.','Spendd8; base10healingbeforeactualcaps. Itisonehealingdie,notflat10forper-dieclassification. OnfirstusemakeproposedDC16dependencesave.'),
            ('Suppressed poison expires','Poisonedsourcehas20minutesleft; Ashsuppressesconditionfor1hour.','Sourceexpiresatitsoriginal20minuteendpoint. Atonehouritdoesnotreturn. Independentongoingpoisondamagewasneverautomaticallycured.')],
        'CS-12':[
            ('One breath and recoil','PB3, CON+2, choosecoldatdosecompletion; legalbreathwithinwindow, damage13, targetDEXsave15.','DC13:targetsuccess takesfloor13/2=6beforedefenses. Userresolvesown1d6coldrecoilonce. Noignition,push,selectivealliesorsecondbreath.'),
            ('Expired overdose entitlement','Tolerantsingledosewindow30seconds; overdosecomplicationroll5; nobodyexhales.','ImmediateNEWrigid-limbs−10walkingfor1hour; at30secondsunusedentitlementexpiresandnormal1d6chosentyperecoiloccurs. MutationdoesnotgrantaWarriorslot.')]
    }
    cases=[]
    for i in sorted(scenarios):
        for n,(title,start,result) in enumerate(scenarios[i],1):
            cases.append({'id':f'{i}-I01-C{n}','itemId':i,'title':title,'given':start,'expected':result,'kind':'unresolved-source-boundary' if i in held else 'proposed-item-adjudication','runtimeExecuted':False})
    assert len(cases)==48
    # Exact line bindings for consequences that depend on current other systems.
    line_evidence=[]
    for p,terms in [
        (R/'docs/mechanics/DAMAGE_SHARING_PLAYTEST.md',['Pure prevention removes damage']),
        (R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',['Attacks against unseen targets']),
        (R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',['Each Wound imposes']),
        (R/'docs/mechanics/HEALING_DEATH_PLAYTEST.md',['Within each permitted reduction plan:','Blight Totem cannot compound']),
        (R/'docs/mechanics/SPELL_PLAYTEST_STARTER.md',['The cone begins at the edge of your space, extends 15 feet']),
        (R/'docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md',['**Supply is a basket of real goods:**','At each canonical 24-hour day endpoint']),
        (R/'docs/mechanics/BARD_PLAYTEST_v0_1.md',['**Tags govern interactions:**'])]:
        ls=p.read_text(encoding='utf-8').splitlines()
        for term in terms:
            hits=[(i+1,s) for i,s in enumerate(ls) if term in s];assert len(hits)==1,(p,term,len(hits))
            line,text=hits[0];line_evidence.append({'path':p.relative_to(G).as_posix(),'lineOneBased':line,'exactText':text,'sha256':info(p)['sha256']})
    model={'id':'CORE-CONSUMABLE-ITEMS-LOCAL-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'20 individual procedure proposals and4 explicit source-decision holds; all24 unadopted/unpromoted.',
        'sharedUseModel':info(sharedpath),'sourceBindings':bindings,'commonProposals':common,'items':profiles,
        'bardChantEvidence':{'source':info(bardpath),'matches':chants,'scope':'Exact current tags and whole cards, not a new tag inferred from name.'},
        'lineEvidence':line_evidence,'mutationTableSearch':{'books':searches,'scope':'Bounded literal matching in three primary books. No full table recovered from these hits; not a claim about every archive. Earlier source JSON and Director JSON references also contain Wyrmspice wording.'},
        'newWyrmspiceComplicationProposal':{'status':mutation_scope,'rows':mutations},
        'reviewGates':['Resolve CU-01 common choices, especially rest epochs and dose/crash ordering','Independently review all20 complete proposed envelopes and all48 authored dispositions','Resolve four held source decisions with actual GPT','Review exact original versus proposed semantics, balance and multi-system interactions','No full-catalog promotion until all24 whole profiles receive exact review'],
        'newRulesAdopted':False,'individualItemsPromoted':0,'sourceInformationDeleted':0,'runtimeImplemented':False,'humanPlaytested':False,'wholeGameApproved':False}
    checks=[]
    def check(name,condition):checks.append({'name':name,'pass':bool(condition)})
    check('all24 original objects and book bindings unchanged',all(p['original']==ingredients[p['id']]['original'] and p['originalBookBinding']==ingredients[p['id']]['originalBookBinding'] for p in profiles))
    check('20proposals and4 explicit holds retained',len(profiles)-len(held)==20 and held==['CB-03','CB-12','CS-02','CS-05'])
    check('ten proposed substances each have actual severe consequence text',sum(p['family']=='magical_substances' and p['reviewReadiness']=='individual-procedure-proposal' and bool(p['overdose']) for p in profiles)==10)
    check('48 unique authored situations, eight unresolved-boundary cases',len({x['id'] for x in cases})==48 and sum(x['kind']=='unresolved-source-boundary' for x in cases)==8)
    check('Bard tags bind exactly three whole current cards',len(chants)==3)
    check('water split day retains exact fractions',Fraction(8*4,24)*2==Fraction(8,3) and Fraction(8*8,24)==Fraction(8,3))
    check('save-flat-resistance example follows declared new order',((13//2)-3)//2==1)
    check('Wyrmspice example uses8+PB+CON and save half',8+3+2==13 and 15>=13 and 13//2==6)
    check('new mutation table covers d6 exactly',sorted(x['roll'] for x in mutations)==list(range(1,7)))
    check('no approval or operational flag changed',not any(p['approved'] or p['activeOperational'] for p in profiles))
    for p,b in zip(sourcepaths,bindings):check('source unchanged '+b['path'],info(p)==b)
    assert all(x['pass'] for x in checks)
    root.mkdir()
    (root/'ITEMS_MODEL.json').write_bytes(encoded(model));(root/'CASEBOOK.json').write_bytes(encoded({'count':48,'proposedItemAdjudications':40,'unresolvedSourceBoundaries':8,'status':'Authored examples, not executed gameplay tests.','cases':cases}))
    text=['# Core brews and substances — individual discussion draft','',
        '**Local, unsubmitted and unadopted.** Twenty items have complete proposed procedure envelopes; four retain specific unresolved source choices. All 24 original records are preserved. Nothing in this file approves a source item or changes the active game rules.','',
        '[Exact source-linked model](ITEMS_MODEL.json) · [48 authored situations](CASEBOOK.json) · [Shared use proposal](../core-consumable-use-local-draft-01/DISCUSSION.md)','',
        '## Common proposals','']
    for k,v in common.items():
        if k!='status':text.extend([f'**{k}:** {v}',''])
    for p in profiles:
        text.extend([f"## {p['id']} — {p['name']}",'',f"**Source:** {p['original']['effect']}"])
        if 'crash' in p['original']:text.append('**Source crash:** '+p['original']['crash'])
        fields={k:v for k,v in p['original'].items() if k not in ['name','effect','crash','description']};text.extend(['','**Preserved source fields:** '+json.dumps(fields,ensure_ascii=False),''])
        if p['reviewReadiness']=='specific-source-decision-required':
            text.extend(['**Specific decision required:** '+p['reason'],''])
            for option in p['concreteAlternativesForJointDiscussion']:text.extend(['- '+option,''])
            text.extend(['**Next:** '+p['requiredEvidenceOrDecision'],''])
        else:
            if p['unitOverride']:text.extend(['**Serving:** '+p['unitOverride'],''])
            for key,label in [('benefit','Proposed benefit'),('endingOrCrash','Ending and crash'),('repetitionAndTolerance','Repeat use'),('limitsAndInterfaces','Limits and interfaces'),('overdose','Overdose')]:text.extend([f'**{label}:** '+p[key],''])
    text.extend(['## Proposed Wyrmspice complication table','',mutation_scope,'','| d6 | Result | Actual consequence |','|---|---|---|'])
    for r in mutations:text.append(f"| {r['roll']} | {r['name']} | {r['effect']} |")
    text.extend(['','No local example count or schema check establishes semantic approval, human balance, runtime support, whole-game completion or publication readiness. The next real GPT review must challenge the original-to-proposal changes explicitly.',''])
    (root/'DIRECTOR_DISCUSSION.md').write_text('\n'.join(text),encoding='utf-8',newline='\n')
    (root/'LOCAL_CHECKS.json').write_bytes(encoded({'count':len(checks),'checks':checks,'failures':0,'scope':'Source equality, actual tag evidence, unique authored coverage and selected arithmetic. No simulation of all proposed item behavior.'}))
    manifest=[{'path':p.name,'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in sorted(root.iterdir()) if p.is_file()]
    (root/'MANIFEST.json').write_bytes(encoded({'files':manifest}))
    receipt.write_bytes(encoded({'recordedAtUtc':model['recordedAtUtc'],'status':model['status'],'model':info(root/'ITEMS_MODEL.json'),'discussion':info(root/'DIRECTOR_DISCUSSION.md'),'casebook':info(root/'CASEBOOK.json'),'checks':info(root/'LOCAL_CHECKS.json'),'sourceCount':len(bindings),'sourceItems':24,'proposedItemEnvelopes':20,'sourceDecisionHolds':held,'authoredSituations':48,'runtimeSituationsExecuted':0,'newRulesAdopted':False,'individualItemsPromoted':0,'sourceInformationDeleted':0,'jointReviewComplete':False,'next':'Actual GPT review of common and individual proposals; resolve four held sources before complete-catalog exact approval.'}))
    print(json.dumps({'preparation':info(receipt),'model':info(root/'ITEMS_MODEL.json'),'sources':len(bindings),'itemProposals':20,'held':held,'cases':48,'checks':len(checks),'failures':0,'adopted':False}))

if __name__=='__main__':main()
