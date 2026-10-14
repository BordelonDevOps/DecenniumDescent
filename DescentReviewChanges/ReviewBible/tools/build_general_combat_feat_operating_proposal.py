"""Preserve 58 general combat sources and author complete, unadopted procedures."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import json,re
G=Path(r'C:\Github\DecenniumDescent'); R=G/'DescentReviewChanges/ReviewBible'; A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def info(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pointer(x,p):
 for key in p.strip('/').split('/'):x=x[int(key)] if isinstance(x,list) else x[key.replace('~1','/').replace('~0','~')]
 return x
draft_path=A/'GENERAL_COMBAT_58_OPERATING_PROPOSALS.json'
out=R/'data/director/general_combat_feat_operating_proposal_internal.json'
doc=R/'docs/feats/GENERAL_COMBAT_FEAT_OPERATING_PROPOSAL.md'
receipt=A/'GENERAL_COMBAT_58_OPERATING_PROPOSAL_CHECK.json'
backup=A/'general-combat-before-lifecycle-clarifications'
assert all((backup/p.name).is_file() and info(backup/p.name)==info(p) for p in [draft_path,out,doc,receipt]),'Preserve outputs before this one-use clarification'
prep_file=A/'GENERAL_COMBAT_FEAT_SOURCE_PREPARATION.json';prep=read(prep_file);sources={x['featId']:x for x in prep['selectedFeats']}
combat_file=R/'data/director/combat_feat_operating_proposal_internal.json';combat=read(combat_file)
magic_file=R/'data/director/magic_core_feat_operating_proposal_internal.json';magic=read(magic_file)
shared={
 'Authority and acquisition':'All58 GC entries remain UNADOPTED and UNSENT. The full original335-feat registries, historical effects and eight reviewed full feats remain unchanged. These proposals supplement current reviewed Core, action, condition, healing, equipment, ancestry and creature-lifecycle interfaces without silently promoting them. Total character level and permanent printed ability prerequisites govern feat acquisition. NEW all58 feats are nonrepeatable except Weapon Focus, which explicitly proposes repetition for a distinct actual weapon type. Ability increases use the existing cap20 composite-grant rule; a capped increase becomes0 while other benefits remain. Missing half-elf/half-orc receipts are not created by name. Actual spellcasting means a personally acquired casting route, not item ownership alone.',
 'Costs and cadence':'Carry the proposed combat-cohort turn, causal and damage conventions reproduced in the structured dependency below. Once per turn means one allowance for each actual regular creature turn; extra turns share the associated original turn identity. Once on your turn shares the owner regular-turn interval. Outside initiative preserve a single equivalent6second owner interval and no transition refresh. Per-rest uses recover only on actual eligible completed rests; LR also refreshes SR uses. The global one-extra-full-Action cap, no invented BA, regular-start Reaction clock, source restrictions and once-character/target/encounter hard-denial guard apply. A spell or class exception must be acquired and legal. A failed legal committed attempt spends its printed cost; an illegal activation is rejected before payment.',
 'Feat modifiers':'NEW distinct flat feat bonuses to the same roll/stat add unless their own family or an already reviewed source expressly says otherwise; repeated copies of the same feat never add. Thus Alert+Alertness+Danger Sense can add5+2+2 to a real new initiative roll, but the bonuses never reorder established initiative. Actual initiative-only restrictions still apply. Active Perception modifiers enter passive10+WIS+applicable skill modifiers when relevant; advantage/disadvantage alone creates no invented passive±5. Advantage and disadvantage cancel to one ordinary d20 regardless of counts. Source-specific same-stat spell/class bonus families remain controlling; a feat does not convert those into freely additive bonuses.',
 'Attacks and movement':'Weapon classification, actual attack mode, hands, anatomy, Heavy/Two-Handed/Loading/Ammunition and equipment condition remain separate requirements. An actual melee-class weapon thrown is a ranged attack but not automatically a ranged-class weapon. Natural attacks count as weapon attacks only if their real profile says so; unarmed remains distinct. No feat grants a hand, item, extra weapon interaction, spell component exemption or proficiency unless expressly supplied. Separate movement budgets pay terrain/crawl/squeeze costs and require nonzero usable Speed; ordinary movement stays spent. No voluntary endpoint in occupied space or solid matter. Forced displacement and teleport do not provoke ordinary opportunity attacks. Specific entry triggers below retain those exclusions; Disengage applies to their opportunity attacks.',
 'Senses and information':'Keep seeing, perceiving, knowing location and having line of effect distinct. A new sense has only its explicit range and blockage, never hidden anatomy/type/HP knowledge. Total cover blocks the senses proposed here. A successful source-authorized information feature can reveal its exact permitted fact, but no missing data or absent record is invented. Advantages for real evidence do not guarantee detection. Companion noses, hearing and item optics belong to their actual bodies; ownership never grants personal sensory omniscience.',
 'Source and trigger integrity':'Use actual independent meaningful hostiles for kill/critical reward generation; never farm allies, compliant captives, harmless creatures, owned summons, copies or reused bodies. A weapon attack hit and a positive-to-zero crossing are different predicates. Damage floors/replacements are resolved before drop rewards. Copies, reflection, transfer and ongoing ticks cannot masquerade as new attacks or personal kills. NEW all feat-granted extra attacks share the combat proposal\'s causal no-recursion rule across Cleave, Frenzied Rage, Riposte, Great Weapon Master and analogous bonus-attack grants; one derived attack cannot mint another derived attack entitlement in the same root. Ordinary independent finite riders retain their actual limits.',
 'Companion and expedition interfaces':'Animal Companion below has its own explicit NEW animal chassis and acquisition; it does not acquire Ranger class features. All own companions and devices keep one BA command and one offensive companion action per numbered round, with attached phases after the owner\'s regular turn and no extra-turn refresh. Companion Training\'s two-recipient command changes recipient count, not the shared offensive allowance, unless GPT selects an explicit priced exception. Actual animals eat, occupy space, require passage/custody and can die. They do not supply a new expedition roster entitlement or bypass the owner-locked12-character cap; reconcile exact participant accounting with the pending58-question verdict. Literal moonlight/transformation facts are usable without deciding cosmology.',
 'New missing-content completion':'The six maneuver definitions below are explicitly NEW feat-only procedures; the current class-card search found no Battle Master archetype or superiority-die menu. No outside game rules are imported and no Soldier card/resource is renamed. Generic Magic Initiate uses actual low-rank rows from the14 current ordinary spellcasting classes, plus the separately NEW finite Sorcerer/Warlock curricula already proposed in Core Magic. Oracle, Soldier and Warrior provide no ordinary rank0+rank1 list in current data. The16 curriculum options do not establish19 classes or a new class feature.'
}
P=[]
def add(fid,procedure,new,c1,c2,deps='Current Core/combat/conditions; actual equipment and feat acquisition; shared proposed feat conventions'):
 s=sources[fid];P.append({'featId':fid,'questionId':s['questionId'],'procedure':procedure,'newChoices':new,'workedCases':[c1,c2],'dependencies':deps.split('; '),'procedureScope':'complete-proposed-feat'})

add('alert',
 'Add+5 to actual new initiative rolls. While conscious, surprise imposes none of its action/movement/reaction restrictions on you; retain any underlying first-turn schedule and all unrelated incapacity, without granting lost actions. Creatures do not gain attack advantage against you solely because their position is Hidden from you. NEW this prevents the unseen-attacker advantage when its sole cause is that specific Hidden state, but does not remove independent darkness/Blinded/Invisible or another source of advantage. It does not locate them, reveal a suspected square, grant sight or end their Hidden record for others. Other feat initiative bonuses may add by the proposed distinct-family rule. No initiative reroll, extra Reaction, or current-combat order change.',
 'Exact Hidden-versus-independent-unseen distinction and conscious surprise suppression.',
 'A hidden sniper gains no advantage from being Hidden from Alert; the victim still does not know the sniper\'s square before the shot reveals it normally.',
 'Alert+Alertness adds7 to a new initiative roll. Becoming conscious later restores surprise protection but supplies no retroactive turn.')
add('alertness',
 'Add+2 to your WIS Perception checks and to new initiative rolls. The Perception contribution also enters your actual passive Perception formula when that task uses Perception; do not add it a second time as a generic awareness modifier. Different eligible initiative feats may add, but duplicate Alertness never does. No Surprise immunity, attack advantage denial, new sense or automatic trap discovery is granted. Improved Alertness requires this exact alertness identity, not alert.',
 'Passive-formula inclusion and distinct-category arithmetic; exact prerequisite identity.',
 'WIS+2 andPB3 gives passive15; Alertness makes it17, not19.',
 'The same feat adds2 to initiative, but the owner can still be surprised if no other protection applies.')
add('ambidexterity',
 'The current ordinary two-weapon rule has no inherent attack-roll penalty for either hand; retain that absence. NEW completion of without penalty: when you make the ordinary two-weapon Bonus Action attack, add your usual positive ability modifier to its damage instead of omitting it. A negative modifier still applies normally. This specific grant can also restore the positive modifier to Double Tap\'s BA attack only if that attack is actually the ordinary two-weapon attack under both sources; a lone-crossbow Double Tap is not. The normal Light one-handed melee weapons, two usable hands, Attack Action trigger and real BA still apply unless Dual Wielder independently expands Light eligibility. It waives no proficiency, Heavy, anatomy, injury or improvised penalty and grants no second BA.',
 'Explicit positive two-weapon damage-modifier restoration as the only newly waived hand penalty.',
 'DEX+3 dual-Light ordinary BA attack adds3 damage with this feat.',
 'Wielding two non-Light weapons still requires Dual Wielder; this feat alone does not authorize that pair.')
add('animal_companion',
 'NEW acquisition: with actual Animal Handling proficiency, select one already real willing/tamed Beast, noncorrupted, INT<7, that fits one of the three finite body templates below. Finding, buying or taming it requires actual campaign access/consent; the feat creates no animal, stocked shop or universal charm. Spend one uninterrupted hour together at touch range; one bond attempt per completedLR, noRP. One feat bond at a time. Use the template corresponding to the real animal\'s body/native movement; do not turn a dog into a bird or grant a new breathing mode. AC12+floor(ownerPB/2), maximumHP5+total owner level; template attack/ability/movement values are explicit NEW. At initial bond convert existing HP proportionally max(1,floor(newMax×oldHP/oldMax)); preserve actual conditions/injuries. Later maximum growth never heals, decreases clamp without damage. Ordinary legal healing works, but no Hit Dice/rest-refill is invented. Use one shared BA command within60ft while the animal can perceive you: in its attached phase after your regular turn, move and make its one attack or Dash/Disengage/Help/Dodge. No independent turn/Reaction; uncommanded move defensively and Dodge. The animal\'s HP-only chassis dies at0, producing its one actual corpse and ending the bond, with no Wound/death-save sequence; this is a feat-specific NEW rule, not generic animal law. Death/release never creates replacement: after a new completedLR, a new real animal and full hour are required. Voluntary release takes one uninterrupted hour and ends the bond without healing; preserve the same physical animal and restore its prior ordinary profile with the same current-HP fraction, not a fresh full animal. A creature cannot have this and a Ranger bond simultaneously; transferring requires actual release and new paid acquisition, not additive statistics. Owner death ends the bond and, if the animal remains alive, restores its saved ordinary profile using the same positive-HP ratio conversion as release; a dead animal remains its actual corpse. Temporary owner incapacity prevents new commands but does not cancel a previously committed legal command; after that command, uncommanded phases remain defensive. This never supplies autonomous attacks.',
 'Complete real-animal bond, three body templates, finite statistics, proportional conversion, command/HP-only death and no-free-replacement procedure.',
 'A ground companion bonded by level5 has max10HP. A real animal at half of its oldHP converts to5HP, not full10.',
 'At0HP it dies and leaves its actual body. Taking a rest alone neither revives it nor creates another beast.',
 'NEW animal templates below; reviewed creature lifecycle and maximumHP conversion; pending expedition roster and transport decisions')
add('battle_awareness',
 'At total level5, opponents receive no attack advantage against you merely because they flank you. Current reviewed combat supplies no universal flanking advantage, and the proposed Tactical Flanker geometry grants only its explicit damage rider; this protection creates no penalty for other defenders and does not erase that separate damage rider. Any independently sourced flanking-advantage rule is suppressed only as an advantage source against you; other advantage still works and ordinary cancellation applies. Gain+1AC only against an actual opportunity attack while that one attack resolves, including a legal feat-specific entry opportunity attack. No lasting AC, immunity or protection from a Reaction attack that is not actually an opportunity attack.',
 'Compatibility protection for absent universal flanking advantage; attack-specific AC window.',
 'A normal attack from a flanking foe has no new benefit to remove; Tactical Flanker\'s lawful1d6 remains separate.',
 'An entry-trigger polearm opportunity attack compares against+1AC. Mage Slayer\'s non-opportunity Reaction attack does not.')
add('bladedancer',
 'NEW once per turn, immediately after your direct attack with an actual Finesse weapon hits a meaningful hostile, you may move using a separate5ft movement-cost budget, with no Action/BA/Reaction. The attack may be melee or a legal thrown Finesse weapon. Resolve its damage and immediate source riders first; if still capable, perform the move before any later attack. This movement provokes no opportunity attacks from anyone but retains terrain, hazards, usable Speed and legal endpoints. One hit cannot bank a move for later; multiple hits that turn do not each create5ft. A copied/periodic hit or harmless training target cannot create movement. No teleport or restoration of ordinary movement.',
 'Once-per-turn meaningful-hostile cap, separate5-point budget and post-hit sequencing.',
 'After a dagger hit, move5ft on normal ground without opportunity attacks.',
 'A second hit in the same turn grants no additional move. A difficult5ft tile costs10 and is beyond this5-point budget.')
add('blind_fight',
 'Ignore only attack disadvantage directly imposed by your Blinded condition. Other independent unseen-target, darkness, long-range or condition disadvantages remain. NEW pinpointing is a nonvisual spatial sense: while conscious, automatically know the occupied location of an actual creature within30ft with line of effect, unless it is behind total cover or protected by an explicit anti-detection effect. It needs no hearing or sight and so works while Deafened/Blinded; those bodily consequences otherwise remain. This specific sense defeats a Hidden location within range for you but does not supply visual sight, colors, text, identity/type or perceive objects as creatures. An invisible creature\'s located position follows the current Invisible known-position exception; separate darkness can still impose unseen penalties. A creature you can see spell still needs actual qualifying sight, not this pinpoint. Leaving range loses live localization; remembered last position is not a new exact current one.',
 'Explicit nonvisual30ft location sense, line/cover/blockers and no true sight grant.',
 'A Blinded owner pinpoints a creature20ft away through open air; it still cannot satisfy a spell\'s can-see requirement using this sense alone.',
 'A creature behind a closed solid wall is not pinpointed, even within10ft; known location outside30 does not remain automatically tracked.')
add('blindFighting',
 'NEW interpret the literal10ft effectively-see clause as a nonvisual blindsight sense while conscious. Within10ft and line of effect, you can effectively see actual creatures/objects regardless of ordinary darkness, fog, Blinded or invisibility; total cover and explicit blindsight/anti-detection blockers still prevent it. Hearing is not required. It meets an ordinary can-see targeting requirement within that range but cannot read colors, printed text or visual illusion details that require actual eyes; it perceives physical shapes/presence, not a secret true identity or magical aura. Hidden creatures with an exposed physical body in this range are seen by you and therefore not Hidden from you. A purely visual illusion without a physical body is not a real body to this sense; this does not grant other observers automatic disbelief. Beyond10ft use normal senses. Blind Fight\'s30ft pinpoint range does not extend this10ft effective sight.',
 'Nonvisual10ft physical blindsight, can-see permission and explicit limits versus30ft location-only feat.',
 'A creature5ft away in opaque fog can be effectively seen for a can-see spell if line of effect remains.',
 'Owning both feats locates an enemy20ft away but does not extend blindsight or can-see permission to20ft.')
add('brawler',
 'Your ordinary unarmed strike base becomes1d4+STR bludgeoning, minimum0. NEW it is a replacement profile, not an added die; choose a separately legal stronger unarmed profile when available without stacking their base dice. It does not replace a form\'s natural weapon or grant hands/anatomy. You may spend BA for one ordinary Grapple without needing a prior hit or Attack Action. Use actual usable free grasping hand/appendage, reach, target at most one size larger, STR Athletics versus target STR Athletics/DEX Acrobatics, tie preserves state. Normal hold/escape/drag rules remain. This supplies no extra BA or damage with the grapple.',
 'Replacement unarmed base and unconditional BA Grapple under actual ordinary contests.',
 'An unarmed hit atSTR+2 deals1d4+2; a Monk\'s larger legal base can be used instead, not added.',
 'Before attacking, a free-handed owner can BA grapple. A weapon in every usable hand still prevents that ordinary grapple.')
add('cavalry',
 'While legally riding a real mount under actual mounted/control/custody rules, your attacks have advantage against actual unmounted creatures. Retain the broad source: melee/ranged weapon, unarmed/natural and spell attacks qualify, with no target-size restriction. Save-only effects do not. Other disadvantage still cancels. The ridden mount\'s existing Speed modes each gain10ft while you remain its actual rider; NEW derive any mode explicitly equal to another Speed from that modified value rather than adding10 twice. No new mode is created, and Speed0 restrictions override the increase. Multiple Cavalry riders give one+10 family bonus, not one per passenger. The feat creates no mount, control permission, mount attack, shared Action pool or extra turn. Mounted Combatant remains a separate narrower feat with no double advantage. Exact mounting, load and shared-space procedures must follow the actual expedition/transport verdict when returned.',
 'Literal broad attack advantage, current real mount, existing-mode+10 and no passenger stacking.',
 'A mounted archer attacks an unmounted giant: Cavalry advantage applies despite its size, subject to other disadvantage.',
 'Two Cavalry passengers do not give a horse+20Speed; no flying Speed appears on a walking-only mount.',
 'Pending full transport verdict; actual mount body and custody; source Mounted Combatant comparison')
add('charger',
 'After taking Dash as an Action on your own turn, you may use your available BA that turn for either one melee weapon attack or one ordinary Shove. NEW a BA Dash, Reaction movement or merely moving far does not trigger this feat. There is no required approach distance/straight path in its printed source, and no extra damage or push distance is added. The attack needs legal reach/weapon/target; Shove uses ordinary reach, one-size-larger cap and Athletics opposed by Athletics/Acrobatics, with success choosing5ft away or Prone. Actual Speed0 can prevent Dash movement but does not create an attack permission if Dash itself is illegal under your condition; a legal Dash with no movement still meets the Action trigger. No second BA.',
 'Action Dash only and no imported approach/damage bonus.',
 'A legal Action Dash followed by BA spear attack pays both actions; moving10ft is not required by this feat.',
 'A Thief\'s BA Dash does not trigger Charger and has already spent the ordinary BA anyway.')
add('cleave',
 'NEW once on your own turn, after your direct melee attack reduces a meaningful hostile from positiveHP to0, you may make one immediate additional melee weapon, natural or unarmed attack against a different creature within the actual reach of the selected legal attack. It costs no separate Action/BA but is exactly one attack, not Attack Action/Extra Attack. No melee spell may be cast through this grant. Death is unnecessary; an actually prevented drop gives no trigger. A different second target need not be hostile, but no staged friendly drop can generate the first trigger. Use current weapon/hands and normal attack/damage; no free draw. Mark the attack as derived under the shared causal cap so it cannot spawn Cleave, Frenzied Rage, Great Weapon Master or analogous further attack grants. If multiple extra-attack sources trigger on the same drop, NEW choose one grant for that event, pay its actual cost, and do not bank the others.',
 'One own-turn free attack, meaningful drop, nonspell melee modes and one selected derived-attack grant per drop.',
 'A melee hit downs a hostile: make one immediate unarmed or weapon attack against another legal target.',
 'That derived attack downs the next foe; it cannot spawn another Cleave or a Great Weapon Master entitlement.')
add('combatCasting',
 'Gain advantage on CON saves specifically to maintain actual spell concentration, including concentration holding a readied spell. Other CON saves, nonspell concentration and generic Strain/Wounds gain nothing. War Caster\'s same advantage does not add another die; actual disadvantage cancels normally. When an actual opportunity-attack trigger would let you spend Reaction against one creature, you may instead cast one legally available Action-time spell whose actual target selection is exactly that creature. NEW any accessible rank is permitted, with no other creature/object target, area, self-only effect, long casting time, BA or Reaction spell. Recheck spell range/line/perception at the opportunity window; original movement-trigger timing remains before exit. The spell retains its own attack/save, actual casting route/rank/RP or charge, components/hands/focus, concentration, Dissonance/Refrain and cast interruption. The spell resolves instead of the weapon attack and spends the same Reaction; no spell knowledge or cost waiver. For Sentinel and Battle Awareness it is a spell substitution, not an actual opportunity attack hit, so those weapon-attack event benefits do not automatically transfer.',
 'Spell-only concentration, full paid Action-spell substitution, exactly one target and event-type boundary.',
 'A foe begins leaving reach. A legal single-target Action cantrip can replace the opportunity attack, provided its own range/line and components are legal.',
 'An area burst or Self spell cannot qualify merely because only one enemy would be affected; neither can a1minute ritual.')
add('combatExpertise',
 'NEW once during your regular own turn, before your first attack roll that turn, declare the−1attack/+1AC trade. You must actually commit a legal attack at that declaration; merely announcing Expertise while making no attack grants no defense. All your attack rolls from that commitment through your next original regular start take−1, including spell, off-turn and linked extra-turn attacks. Gain+1AC for exactly that same interval, including if the first attack misses. No repeated toggling, mid-interval opt-out, scalable penalty or retroactive defense. It is not a stance, so a separately chosen stance remains subject to its rules; duplicate Expertise never stacks.',
 'Committed pre-first-attack activation, all-attack penalty and fixed interval.',
 'The owner declares before a sword attack; even a miss leaves−1 on later attacks and+1AC until next regular start.',
 'After already making an unpenalized attack, the owner cannot turn Expertise on to obtain defense for that interval.')
add('combat_reflexes',
 'NEW grant one additional general-purpose Reaction token per numbered encounter round, separate from the ordinary regular-start Reaction. It begins available on actual encounter entry unless prohibited, refreshes at the next global numbered-round start, and never carries over as a second extra token. The ordinary token still refreshes at owner regular start. Leaving/reentering initiative retains the same encounter/round ledger; an extra turn refreshes neither extra token nor numbered round. Outside initiative one extra token per actual6second global interval, with no duplicated boundary on transition. You may choose which eligible token to spend, but NEW at most one Reaction from you on the same triggering event; the extra token cannot respond twice to one spell/attack or produce a self-recursive Reaction chain. A later distinct event may use the same named ability if its own cadence allows. Surprise, Incapacitated, Focused and source Reaction prohibitions affect both tokens. No free action or ability knowledge.',
 'Separate numbered-round token matching the printed per-round phrase, canonical entry/boundary state and one-reaction-per-event cap.',
 'Before a late initiative slot, spend the ordinary token; after own start it refreshes. The independent extra token remains at most one for that numbered round.',
 'Two different foes leave reach on distinct events: ordinary and extra tokens may fund one attack each. One foe leaving once cannot be attacked twice from that one trigger.')
add('coordinator',
 'BA: choose one other willing ally within30ft that can perceive and understand your brief audible or visible direction. NEW gain advantage on its next attack roll before your next original regular start; the first attack consumes it whether hit or miss, with no replacement if disadvantage cancels it. One recipient per activation, no extra attack or forced action. Reapplication from the same feat family preserves one advantage entitlement per recipient and the latest expiry, not a stack of future attacks. Multiple applicable next-attack advantage grants consume on that same next attack according to their own rules; they do not queue by name. Actual communication can fail through silence/obstruction, though a mutually understood visible signal is sufficient. You cannot target yourself.',
 'Perception/understanding, other-ally scope, next-start deadline and no queued duplicate advantages.',
 'An ally receives the signal and misses its next attack; the advantage is spent.',
 'If independent disadvantage cancels the benefit, that first attack still consumes the Coordinator entitlement.')
add('crossbowExpert',
 'Ignore the actual Loading property\'s limit of one ammunition attack per Action/BA/Reaction when using a crossbow; Extra Attack can then make its legal number with real bolts. This does not waive Ammunition\'s free loading hand, Two-Handed support, magazine contents or the separate Repeating5 reload Action. NEW you may spend your BA on your own turn for one attack with an actually wielded usable hand crossbow, without a prior Attack Action requirement. Use its ordinary attack and damage modifiers. A preloaded bolt permits that shot under actual inventory; further loading needs a genuine available hand unless a separate sourced exception applies. No second BA, extra bolt, proficiency or nearby-hostile disadvantage immunity. A shield/buckler does not become a free loading hand.',
 'Unconditional legal BA hand-crossbow attack and exact Loading-only waiver.',
 'An Attack Action with Extra Attack can fire an ordinary crossbow twice if hands and two bolts are available.',
 'An empty repeating-crossbow magazine still needs its real reload Action; Crossbow Expert does not refill it or erase Repeating5.')
add('crusher',
 'NEW once per turn, after your direct attack with a weapon whose native damage includes bludgeoning hits, you may move the target5ft to a legal unoccupied destination, subject to a target size no more than one category larger than you. Choose direction; this is forced displacement along a real unobstructed path, not teleport. No save is added. It cannot lift into unsupported air or through a wall; ordinary falling applies if moved over a real edge. Resolve hit damage before movement; an actual hit with0resolved damage can still qualify. Separately, a critical hit with that bludgeoning weapon imposes disadvantage on all the target\'s attack rolls through your next original regular start, no size limit. Repeated critical records retain independent deadlines but disadvantage is applied once. This source is weapon-qualified, not any bludgeoning spell or added rider on a nonbludgeoning weapon. A real natural weapon qualifies only if its profile is a bludgeoning weapon; ordinary unarmed is not one without an express rule.',
 'Once-turn movement, one-size cap, no save, legal horizontal direction and exact critical-disadvantage endpoint.',
 'A mace hit can move a similarly sized foe5ft sideways into an open square; it cannot phase through an occupied wall.',
 'A critical with that mace gives disadvantage through next owner start even if the target is too large to move.')
add('danger_sense',
 'At total character level3, add the current effect\'s+2 to new initiative rolls; preserve legacy+4 only as historical text. Gain advantage on actual Perception checks to notice traps or signs of an immediate ambush when real relevant evidence is perceivable by your working senses. It does not invent evidence, auto-detect danger, reveal a hidden identity or grant surprise immunity/DEX-save advantage. Ordinary passive Perception has no invented±5 advantage adjustment; an explicitly called active Perception roll uses advantage. Distinct Alert/Alertness initiative bonuses may add, but no reroll or retroactive initiative change.',
 'Explicit current+2 versus preserved legacy+4 and evidence-bound active Perception.',
 'Hearing suspicious movement immediately around a corner can qualify for an advantaged actual Perception roll.',
 'A completely undetectable trap with no available cue is not automatically found; initiative remains+2 from this source, not+4.')
add('deadlyAim',
 'Before any actual ranged attack roll, optionally accept−1 on that one roll to add+2flat damage if it hits. NEW the source says ranged attacks, so this includes ranged weapon, thrown, natural and spell attacks, but not save-only effects. The+2 joins one native damage component of that attack, chosen if multiple types, and is not doubled by a critical. It does not create damage for an attack with no native damage. Each attack makes its own pre-roll choice, no persistent stance or rest limit. Duplicate same feat cannot scale the trade; no retroactive selection after the die. Independently eligible feat modifiers may add unless their actual family forbids it.',
 'Broad ranged-attack scope, per-attack declaration and one flat native component.',
 'A ranged spell attack accepts−1 before rolling and adds2 to native fire damage on a hit.',
 'A critical doubles the attack\'s dice as usual but keeps Deadly Aim at+2, not+4.')
add('defender',
 'When another allied creature within5ft of you is targeted by an attack, spend Reaction before its attack roll to impose disadvantage on that one roll. NEW you must perceive the ally and the attacker\'s actual attack; no can-see requirement, shield or free hand is added, but you must be capable of a deliberate physical distraction/intervention with line of effect to the ally. It does not require reaching the attacker, so a visible incoming ranged shot can qualify. Range is checked at declaration and no movement is granted. Advantage cancels normally; later attacks in a multiattack need their own actual triggers/resources. This grants no damage transfer, interception, AC bonus or reroll after the result.',
 'Pre-roll Reaction, actual perceived attack/ally and interposition line without unprinted equipment tax.',
 'An adjacent ally faces a visible archer\'s shot: spend Reaction before the roll for disadvantage.',
 'A second attack in the same multiattack is unaffected unless a separate legal Reaction is available on that distinct event.')
add('disarm',
 'Replace one attack of your Attack Action with this attempt against a held reachable object of a creature in your current melee reach. NEW choose either an actually wielded melee weapon or a usable free grasping hand as the implement; use that weapon\'s actual attack ability orSTR for an unarmed attempt. Target choosesSTR orDEX save DC8+PB+that actual ability modifier. No attack roll, damage, critical or on-hit trigger. Failure drops one declared object to a legal adjacent unoccupied space you choose, otherwise its own space; success keeps it. No size limit is added by the source, but physical reach, graspability and real non-droppable bonds remain. Implanted body parts, worn armor and strapped shields are not freely held droppable objects. You do not gain custody automatically; retrieving costs normal interaction/time. No special proficiency requirement grants missing weapon PB on other attacks.',
 'Actual Attack Action replacement, melee implement/ability, target choice and no damage/custody grant.',
 'ADEX+3 proficient dagger implement atPB3 setsDC14; target chooses itsSTR orDEX save.',
 'A failed save can drop a held wand, but cannot sever an implanted claw or instantly transfer ownership to the attacker.')
add('dualWielder',
 'For ordinary two-weapon fighting, each weapon may be a non-Light one-handed melee weapon that you can actually wield in its own usable hand. NEW Versatile works using its one-hand profile; Two-Handed cannot occupy one hand, and Heavy/size penalties still apply even if an unusual legal one-hand profile has Heavy. Do not dual-wield a weapon requiring two hands with another weapon absent an actual specific hand exception. Gain+1AC while actually wielding two such usable melee weapons, one in each of two hands; a Broken, stowed, dropped or anatomy-incompatible weapon cannot supply the bonus. No extra draw/stow, BA or positive offhand damage modifier: Ambidexterity or another explicit grant supplies that separately. The ordinary Attack Action and two-weapon BA trigger remain.',
 'Actual one-handed melee pairing, Versatile one-hand profile and AC dependency.',
 'Two usable longswords can form a legal pair, each using1d8 rather than its two-hand1d10.',
 'Dropping one sword immediately ends+1AC. A greatsword held with one hand does not become a legal paired weapon.')
add('elvenAccuracy',
 'Require an actual Elf ancestry receipt or a genuine independently sourced half-elf receipt; do not create or alias an absent half-elf base. On an attack actually made with advantage usingDEX,INT,WIS orCHA, after seeing the two original d20s and before final hit/outcome declaration, you may reroll one chosen die once and must use its new face in that position. Then keep the higher of the two resulting dice. NEW at most one Elven Accuracy reroll per attack; it cannot reroll the same die again through this feature or create a third independent kept die. If any disadvantage cancels advantage, there is one ordinary die and this feature is ineligible. STR/CON attacks, saves and checks do not qualify. Keep actual natural-face provenance for criticals. Lucky\'s separate die replacement may affect this attack only under its own one-event procedure; no Elven reroll of that additional Lucky die.',
 'Actual ancestry receipt, replace-one-die procedure, before-outcome timing and no reroll loop.',
 'An advantagedDEX attack rolls4 and12. Reroll4 to9, then keep12; rerolling does not guarantee improvement.',
 'Advantage canceled by disadvantage yields one d20, so Elven Accuracy cannot trigger.')
add('fast_talker',
 'NEW complete combat procedure: Action, once per SR, choose one hostile creature within30ft that can hear your rapid speech and understands the language you actually speak. Spend the use at declaration; it makesWIS save DC8+PB+CHA. Failure prevents it taking an Action during its next future regular turn; movement, BA and Reaction are not otherwise removed, and an extra-Action grant cannot bypass that turn\'s denial. The source-character/target/encounter hard-denial guard applies jointly with class/spell/companion/other feat denial; a target already affected by your hard denial in this encounter cannot suffer this rider again. NEW hearing/language comprehension and a capacity to process speech are required; explicit immunity to this mental action-denial effect blocks it, but the feat does not automatically impose Charmed, Frightened or Stunned. It neither forces beliefs nor commands a particular act. Outside combat it can support an ordinary social attempt but does not automatically win agreement or impose a recurring lost-time penalty.',
 'Action/SR/30ft/language/WIS-save procedure, next-regular-turn Action denial and shared hard-control guard.',
 'A hearing language-sharing foe failsDC14: it can move and use a legalBA on its next regular turn, but cannot take an Action.',
 'A foe unable to understand the speech is ineligible, and a previously denied target is protected by the shared encounter guard.')
add('fencer',
 'While actually wielding a usable Finesse melee weapon, gain+1AC as one feat modifier. NEW a second empty hand is not required and a lawful shield may coexist; the weapon must remain wielded with actual anatomy and cannot be Broken/stowed. When a seen hostile creature voluntarily crosses from outside to inside that weapon\'s ordinary current melee reach, you may spend Reaction for one opportunity attack with that same weapon immediately after entry and before further movement. It must be a legal melee target in reach then. Forced displacement, teleport, newly appearing, your movement/reach expansion and the target merely starting within reach do not trigger. Disengage/opportunity immunity suppresses it. Lunge\'s single-attack extension creates no persistent entry boundary. No additional Reaction or perpetual threatened range.',
 'Usable Finesse melee-weapon AC and voluntary entry opportunity trigger with actual immunity rules.',
 'A seen enemy walks from10ft to5ft from a rapier wielder: the entry attack may spendReaction.',
 'Pushing an enemy into5ft or extending reach around it does not trigger this feat.')
add('fighter',
 'Gain proficiency with all actual Simple and Martial weapon profiles; no armor, shield, class level or item is granted. NEW after making at least one personal weapon, natural or unarmed attack on your own turn through a legal source, you may spendBA for one additional personal weapon, natural or unarmed attack. It is not a spell cast and cannot substitute a spell attack that needs casting. No Attack Action is specifically required, but a save-only technique is not a prior attack. Actual weapon/ammunition/hands/reach and physical capability remain. One availableBA, no Extra Attack multiplier. The additional attack is derived and cannot create another feat-granted extra-attack entitlement in its causal root. The feat\'s name is not a Fighter class or permission to take an external class\'s features.',
 'Any lawful personal physical-attack trigger, oneBA nonspell attack and no class alias.',
 'After one unarmed attack, the owner canBA attack with a legally wielded martial weapon using its newly granted proficiency.',
 'A fireball-like save-only spell supplies no prior physical attack, and the feat cannot cast a second spell as its BA attack.')
add('fleet_of_foot',
 'NEW interpret this feat\'s legacy Agility14 as permanentDEX14, without adding a seventh ability. Increase current walkingSpeed by10ft; preserve its older+10% wording only as historical source. No direct addition to independent flying/swimming/climbing modes. A mode explicitly defined as equal to walkingSpeed derives from the increased walking value once; if another rule independently increases both, do not count the same derivation twice. Actual conditions settingSpeed0 and other lawful reductions still apply, and changingSpeed never refunds spent movement. Distinct fixed Speed feat bonuses may add once each; duplicate Fleet does not.',
 'Explicit Agility→DEX and current+10ft versus legacypercent, walking-only derivation.',
 'Walk30 becomes40; an independentFly30 remains30.',
 'A climbingSpeed expressly equal to walking becomes40 too, but not50 from adding Fleet a second time.')
add('greatWeaponMaster',
 'Preserve the two-handed mastery description as a qualification to the broad effect: NEW while using a melee weapon actually wielded in two hands, after your direct attack critically hits a meaningful hostile or reduces it from positiveHP to0, you may spend your availableBA before the same own turn ends for one attack with a melee weapon wielded in two hands. A Versatile two-hand use qualifies; no separate Heavy property is required. A legal ranged/thrown hit cannot qualify after releasing the weapon because it was not a melee two-handed attack. No−5/+10 is printed or added. If the attack both crits and drops, it still creates one entitlement; no extraBA. If Cleave/Frenzied Rage/Cleaving Momentum also trigger on that same event, use the proposed choose-one-derived-grant rule and pay the chosen cost. The derived attack cannot spawn further attack grants in its root. Off-turn criticals cannot bank a futureBA.',
 'Explicit two-handed melee completion from description, same-own-turnBA and no imported damage trade.',
 'A two-handed quarterstaff critical can fund oneBA melee attack with a lawful two-hand weapon.',
 'A one-handed sword critical does not qualify under this proposed description-bound scope; a crit-and-drop never grants twoBAs.')
add('hunter',
 'Gain Survival proficiency, not expertise if already proficient. You may attempt tracking across any terrain when a real trail exists; NEW difficult medium, bare stone, water or air does not automatically make an actual passage untrackable, but no trail is created across teleportation or a source explicitly leaving none. Spend1minute at a real last-known trail location, WIS Survival DC15 for a trail within24hours, +5 if older than12hours and +5 if genuinely mixed/obscured; an explicitly sourced trail DC replaces this default. Success finds the next local direction/evidence, not the target\'s present location, identity or whole route. No unchanged free retry; changed evidence, new route segment or actual aid can support a new attempt. Add+2flat once per own direct damage event against an actual Beast or Monstrosity, of one native damage type before defenses; not per die, critical doubling, periodic/copy/transfer/reflection or companion-owned event. Actual target typing is decided from source facts without automatically disclosing it. This is distinct from Tracker/Wilderness features and grants no terrain movement immunity.',
 'Finite tracking method across real terrain, actual evidence/no-teleport rule and native-event damage scope.',
 'A real mixed trail16hours old usesDC25 under the default; success yields the next local direction, not a live target beacon.',
 'A critical against a Beast adds2flat once. A summoned companion\'s own hit does not acquire its owner\'s Hunter damage.')
add('alertness_improved',
 'Requires the exact Alertness feat. NEW blindsense10ft is nonvisual location awareness: while conscious you pinpoint actual creature locations within10ft and line of effect, excluding total cover and explicit anti-detection blockers. It is not blindsight and does not meet can-see requirements, read objects/text, reveal type or identify illusions without an actual body. Hearing is not required under this explicit feat-only sense proposal. Actual Hidden location ends for you within that range, with Invisible\'s current known-position exception but unrelated darkness/unseen modifiers retained. While conscious, surprise restrictions are suppressed as in Alert; no extra actions or previous-turn recovery. Blind Fight may supply a broader30ft location sense independently, but no addition of their ranges and no promotion to sight.',
 'Exact prerequisite,10ft location-only sense and conscious surprise suppression.',
 'Alert without Alertness cannot acquire this feat merely because their names resemble each other.',
 'An invisible body5ft away is located, but a can-see spell remains unavailable without another qualifying sense.')
add('inspiring_presence',
 'After your direct attack critically hits a meaningful hostile, other allied creatures within30ft that can actually see or hear you at that instant gain+1 to their attack rolls through your next original regular start. NEW recipients are fixed at the trigger, with no continuing range/hearing tether; allies entering later do not gain the old inspiration. No common language is required. You are not your own recipient. Any genuine critical-if-hit result qualifies, not just natural20; automatic-hit wording without a critical does not. Same-feat overlapping records never add beyond+1, and independent expiry records remain. Another legitimate critical can renew eligible allies but cannot duplicate the number. Preserve older+5%damage/10seconds as history; current effect is+1attack, not damage.',
 'Meaningful critical, fixed other-ally snapshot and same-family overlap handling.',
 'An adjacent ally who hears an off-turn critical keeps+1 until the owner\'s next regular start even after moving40ft away.',
 'Two inspiring owners grant one+1family layer to an ally; a later expiry can preserve that layer without making it+2.')
add('intimidating',
 'Gain Intimidation proficiency, not expertise if already proficient. NEW in combat spendBA to demoralize one hostile within30ft who perceives your audible or visible credible threat. Oppose your normal CHA Intimidation (STR only if an independently legal actual source permits that substitution) with targetWIS Insight. Higher wins, ties preserve state; no natural task shift. Success imposes disadvantage on its next attack roll before your next original regular start, consumed by that attack even if canceled or missed. One attempt per target per owner regular-turn interval; new successful applications refresh one family record, not a queue. No SR cap beyond realBA/cadence. Shared language is unnecessary for a plainly understood physical threat; an unperceivable or incomprehensible threat is ineligible. This is a distinct demoralization rider, not Frightened, forced loyalty, Charmed or whole-turn denial; immunity to fear alone does not automatically block it unless it expressly covers demoralization/intimidation.',
 'BA/30ft/contest, credible perceived threat, next-attack endpoint and no invented Frightened.',
 'Intimidation18 defeats Insight14: the foe\'s next attack has disadvantage, then the rider ends.',
 'A creature behind opaque total cover with no audible/visible threat cannot be demoralized through this feature.')
add('lucky',
 'NEW gain3luck points, initially full and restored to3 only on a completedLR; no overcap or conversion. On your own attack, ability/skill/tool check or save, after the initial d20 die/dice are visible but before the outcome and consequences are declared, spend at most1point to roll one additionald20. Choose either to keep the original dice unchanged or to replace one original die with the new face; then apply the roll\'s original normal/advantage/disadvantage selection over its original one/two positions. The added die is not a third freely best-kept die under disadvantage. Actual natural face is the final kept face; no source allows inventing an automatic result. It may affect an opposed check or death save because those are your checks/saves; it cannot reroll an enemy, a damage die, a flat result or a no-roll automatic failure. NEW one Lucky intervention per underlying roll event even if another rule later rerolls it. Resolve Elven Accuracy on initial eligible dice first, then Lucky; Elven Accuracy cannot reroll the added Lucky die. Other mandatory whole-roll replacements preserve their own order and consume the same event entitlement.',
 'LR recovery, before-outcome window, optional one-position replacement with original selection rule and finite interaction ordering.',
 'Disadvantage rolls3 and17; Lucky rolls12 and replaces3. Final disadvantage keeps12, not17.',
 'An ordinary death save shows1 before its consequences. Lucky may replace it with the added die; it cannot be invoked after the failure/death has already resolved.')
add('mage_slayer',
 'When a creature within5ft actually casts a spell and you can perceive the casting event, you may spendReaction for one legal melee weapon attack against it. NEW this reaction occurs after that spell fully resolves or is negated, not in its interruption window. Range/reach/line/perception and your capability must still hold at reaction resolution. A caster that teleports away, becomes untargetable, incapacitates you, or kills you can leave no legal attack. V/S or another actually perceptible magical cue can reveal casting; no automatic detection of fully imperceptible casting is granted. Reaction spells qualify as real casts, but the attack does not itself repeat casting or grant a newReaction. Readied spells trigger at actual preparation/casting, not a second time on held release. A damaging hit can cause ordinary concentration consequences afterward but does not retroactively negate the completed spell. No generic spell-save advantage or concentration disadvantage.',
 'Post-spell timing, actual perception and legal target recheck; no unprinted counterspell.',
 'A nearby caster completes a self-buff and remains in reach: an availableReaction can attack afterward.',
 'A nearby teleport resolves to30ft away. The caster is no longer in melee reach, so Mage Slayer cannot deliver the attack or cancel the teleport.')
add('magicInitiate',
 'NEW expand the original six-name curriculum choice to the finite16-option table below; this expansion requires explicit joint approval. At acquisition choose permanently one curriculum:14 actual current class-rank0/rank1 lists or the explicitly NEW Sorcerer/Warlock feat-only lists retained from Core Magic. Choose two distinct rank0 identities and one rank1 identity from that curriculum, preserving exact class placement/school/mode. Source1st-level means rank1 here, not another game\'s spell slot. Use the table\'s explicit casting ability, normal totalPB, spell attackPB+ability andDC8+PB+ability. The feat supplies these named grant ranks independently of class level but no class features, ordinary repertoire/prepared slot, RPpool, class level or RC. Rank0 uses actual action/cadence with no generic scaling; rank1 gets one charge per completedLR. Retain Core Magic\'s entire proposed classless casting contract: normal rankRPprice waived, independent effect/material costs retained, real components/focus/hands, concentration/interruption, shared Dissonance/Refrain and rankedLimit+6block, and total character level only for an explicitly numeric spell-payload class-level variable. Unfinished chosen spell payloads stay inactive pending their actual review. NEW one copy of each curriculum across generic and named Magic Initiate identities; acquiring genericBard when namedBard is owned is invalid, rather than a second daily charge. Generic feat itself is nonrepeatable; separately named other curricula may be selected with actual separate feat choices. No class alias is created by the two legacy labels.',
 'Finite16-option curriculum table,14 real lists plus2 separately NEW lists, explicit abilities, same-curriculum duplicate guard and complete shared casting route.',
 'GenericMage selects two actual Mage rank0 rows and one Mage rank1 row, usingINT without acquiring Mage class levels orRP.',
 'A namedWizard initiate cannot add genericWizard for a duplicate rank1charge; genericCleric is a different curriculum if legally selected instead.',
 'Exact current spell choice pools and authored review index; Core Magic MF16–21 and full feat-casting shared proposal; current class engines')
add('martialAdept',
 'The literal Battle Master archetype/superiority-die source has no matching current class-card menu. NEW use the six feat-only maneuver definitions below, each fully specified from existing ordinary actions with a finite die spend. At acquisition permanently choose two different maneuverIDs; gain a separate pool of one superiorityd6, initially available and recovered on completedSR orLR. One die can fund only one declared maneuver on one event; noRP/RC/class-resource exchange or conversion. All maneuvers pay their own actual Action/BA/Reaction or attack-replacement timing, with ordinary target/body legality. A committed attempt spends its die even on miss/failure/countering; illegal attempts spend nothing. The rolled result is used only as the selected maneuver states, not free damage on every maneuver. It grants no Soldier Coordinated Maneuver, class levels or Battle Master subclass. Choices cannot be changed for free at rest.',
 'Explicit NEW six-maneuver feat menu, two permanent choices and oneSRd6 pool.',
 'Choose Measured Strike and Guarding Deflection; spending the one die on either leaves none for the other before a legal rest.',
 'A Soldier\'s independent resource cannot be spent as this superiority die, nor does the feat acquire Coordinated Maneuver.')
add('martial_adept_advanced',
 'Require exact martialAdept. Choose two additional distinct entries from that same six-maneuver menu, excluding the two already known; permanent choices. Increase the common feat superiority pool capacity by one die of the same sized6, for two total; NEW the newly granted die begins available on actual acquisition, not each rest or retarget. CompletedSR/LR restores the shared pool to its current capacity once. Known maneuver count becomes four, not four copies of one option. No larger die, additional class resource, extraAction, simultaneous multiple-die payment or free retraining. Same underlying event may still use at most one superiority maneuver unless a future expressly priced source overrides it.',
 'Exact dependency, four distinct choices, common2d6 capacity and one-maneuver-per-event.',
 'Adept knew two maneuvers; Advanced chooses two others and now has four with a two-die shared pool.',
 'It cannot spend two dice to double Measured Strike\'s bonus on one attack or recharge each feat as independent extra pools.')
add('mobile',
 'NEW add10ft to each existing Speed mode, except a mode expressly derived as equal to another uses that already-modified value and gets no second addition. Grant no new movement mode. Each creature you personally attack on your own turn cannot make opportunity attacks provoked by your voluntary movement for the rest of that actual turn, whether your attack hit or missed. Retain the source\'s broad attack wording: weapon/natural/unarmed/spell and melee/ranged attacks qualify; a save-only effect does not. Source attack must actually be directed at that creature, not an arbitrary empty-square guess proven empty, copied hit or companion attack. No action cost beyond the actual attack/movement; maintain a set of actual attacked identities, not only one. It suppresses only those creatures\' opportunity attacks, not other Reactions or later-turn attacks. No Dash terrain immunity or teleport.',
 'Existing-mode Speed completion, broad actual-attack scope and per-target current-turn immunity.',
 'A missed thrown dagger attack still protects this turn\'s movement from that actual target\'s opportunity attacks.',
 'A fireball-like save effect is not an attack, so it creates no Mobile target immunity; difficult terrain still costs extra.')
add('mounted_combatant',
 'While you are actually legally mounted, gain advantage on your melee attack rolls against creatures that are unmounted and smaller than the actual ridden mount at resolution. Include melee weapon, natural, unarmed and actual melee spell attacks; no ranged or save-only effect. Use real mount/target sizes, not rider size, names or desired posture. Other disadvantage cancels normally. This grants no mount, proficiency/control, target redirection, mount save evasion, immunity, extra action or shared turn. Cavalry\'s broader advantage is separate, but two sources still roll only two dice. Pending full transport rules govern mounting, movement, custody and actual eligibility.',
 'Literal melee/smaller-unmounted scope and actual size snapshot; no external mount-protection clauses.',
 'On a Large mount, melee attacks against an unmountedMedium foe have advantage.',
 'An unmountedLarge foe is not smaller than that mount; this feat gives no advantage, even though Cavalry might independently do so.')
add('natural_leader',
 'While conscious and capable of audible direction, other allied creatures within10ft who can actually hear you gain+1 on real morale saves and saves against effects that actually impose fear/Frightened. NEW no common language is required for this rallying presence, but silence, Deafened and sound-blocking barriers can prevent hearing. Check current radius/hearing when each save occurs; leaving ends the benefit without an expiry timer. It applies only to saves the actual source calls for: do not invent a morale save, turn an ordinary persuasion check into one, compel loyalty or prevent voluntary withdrawal. Same-feat multiple leaders give at most+1; a separately sourced actual bonus follows its own family. You are not your own ally for this feature.',
 'Continuous other-ally audible aura and source-qualified save predicate.',
 'An ally8ft away hearing the leader adds1 to a genuine fear save.',
 'An ally decides to retreat voluntarily: the aura does not force a morale check or take away that decision.')
add('night_hunter',
 'At acquisition record whether the character has an actual independent darkvision source. NEW if none, this feat grants60ft ordinary darkvision. If one exists, instead record a permanent+30ft extension to the current strongest operative independent darkvision range; that mode adds no vision when every underlying source is suppressed/absent. Preserve the acquisition mode when forms/sources later change; no repeated+30 from toggling forms, reacquisition or multiple base ranges. A60ft-grant mode and later independent120ft darkvision use the strongest base120, not180; extension mode on120 becomes150. Ordinary darkvision sees dim light as bright and darkness as dim within range, without color in darkness; eyes/anatomy and Blinded still matter. Magical darkness, total cover and explicit blockers remain unless a separate source defeats them. It is not blindsight or general invisibility detection.',
 'Fixed acquisition mode, dynamic underlying-range extension and ordinary visual limits.',
 'A character already possessing60ft darkvision acquires extension mode and reaches90ft.',
 'Changing to a form with no usable underlying darkvision does not manufacture30ft in extension mode or bank another+30 on returning.')
add('orcish_fury',
 'Require actual Orc or independently sourced half-orc ancestry; no missing half-orc alias is invented. NEW once perSR, after your personal attack with a Simple or Martial weapon hits and before rolling damage, spend the use to add one die of that actual weapon\'s base damage expression. A2d6 weapon adds1d6; use the actual one/two-handed Versatile die selected for the hit. Critical doubles this added attack die with other noncritical-only weapon dice. No ability modifier is added again, and fixed/no-die profiles cannot provide a die. Thrown use qualifies if the weapon is actually Simple/Martial. Natural/unarmed attacks qualify only if independently classified as a Simple/Martial weapon. Source immunity or0damage does not refund the committed use; no additional ancestry endurance or attack is granted.',
 'OneSR charge, on-hit pre-damage commitment, base-die selection and critical treatment.',
 'A2d6 greatsword ordinary hit gains1d6, totaling3d6 before modifiers.',
 'On a critical with that weapon, the added die doubles too for6d6 total; the STR modifier is still added only once.')
add('piercer',
 'NEW once per turn, after rolling damage for a personal hit with a weapon whose native type includes piercing, you may reroll one actual piercing base-weapon die and must keep its new face. Choose from native weapon dice including critical copies and expressly additional weapon dice, not poison/Smite/spell rider dice. One Piercer reroll per event/turn; no repeated loop. Separately, every critical hit with that piercing weapon adds one additional die of its actual base weapon expression after ordinary critical doubling; this critical-specific die is not doubled again. For a2d6 weapon choose one d6. A natural weapon requires an actual piercing weapon profile; save-only spells and a nonpiercing weapon with an attached piercing rider do not qualify. NEW if Savage Attacker also applies, resolve its whole-pool choice first, then Piercer on one die of the kept pool; no return to a discarded pool. All source-specific reroll limits remain.',
 'Once-turn mandatory-result reroll, actual weapon pool and one post-critical additional die.',
 'A rapier critical normally rolls2d8; Piercer adds one mored8 for3d8, not4d8.',
 'A rerolled1 that becomes1 must remain1; the feat cannot reroll again until another qualifying turn allowance.')
add('polearm_master',
 'While actually wielding a usable glaive, halberd, pike or quarterstaff with its required hands, when a seen hostile creature voluntarily crosses from outside to inside that weapon\'s ordinary current melee reach, you may spendReaction for one opportunity attack with that weapon immediately after entry. Retain pike explicitly. No creature appears/teleports/is forced into reach trigger, no trigger from your own movement or reach growth, and no trigger for merely beginning inside. Disengage and other actual opportunity immunity apply. Use the chosen weapon\'s real reach, not a universal10ft; quarterstaff ordinarily remains5ft. It grants no butt-end BA attack, damage die, new proficiency or additionalReaction. Multiple entry-trigger feats offer one eligible attack on the same event under the proposed extra-Reaction event guard.',
 'Exact four-weapon list and voluntary seen-hostile entry timing, without external BA attack.',
 'A seen hostile walks into a pike\'s real10ft reach; an availableReaction can attack.',
 'A quarterstaff wielder does not gain10ft reach merely from this feat, and a forced push into5ft does not trigger.')
add('savage_attacker',
 'Once per turn when you roll damage for your actual melee weapon attack, after seeing that roll but before consequences, reroll the entire eligible native weapon-dice pool once and choose either the complete original total or complete new total. NEW eligible pool includes base weapon dice, their critical copies and expressly additional weapon dice from feats such as Draw Cut, Orcish Fury or Piercer; exclude separate spell/Smite/poison/elemental rider dice and flat modifiers. Preserve each die\'s native type and apply the chosen corresponding per-type totals, not a pooled total reassigned to a preferred type. Never mix the best die from each pool or reroll only unfavorable dice through this feature. Roll once for each original die identity in the chosen pool, not new attacks or damage events. Maximized/fixed numeric damage has no rolled pool to reroll. Resolve Savage Attacker before Piercer\'s one-die adjustment if both are used; after selecting a pool you cannot return to a discarded pool to optimize a later modifier. Own and off-turn regular-turn allowances follow the shared cadence.',
 'Explicit weapon-only full-pool scope, whole-result choice, per-type provenance and reroll ordering.',
 'A2d6 pool rolls2+6=8 and rerolls5+1=6. Choose8 or6, never6+5=11.',
 'A separate poison2d6 rider remains its original roll; Savage Attacker does not reroll it just because it accompanied the melee hit.')
add('sentinel',
 'When your actual opportunity attack hits a creature, set all its current Speed modes to0 for the rest of the actual turn containing that event. NEW the endpoint is that enclosing turn\'s end, including an actual extra-turn end, not the target\'s next future turn; outside initiative use the remainder of the current6second interval. The hit qualifies even if damage is0. This overrides ordinary positive Speed additions during the interval and preserves spent movement cost; ending it restores otherwise-current Speed without refunding cost. It stops subsequent voluntary Speed expenditure, but not independently legal forced movement or teleport. A flying creature withSpeed0 follows existing Falling/hover/support rules, not immediate invented fall damage. Disengage still prevents the opportunity trigger. A Reaction attack that is not an opportunity attack, or Combat Casting\'s replacement spell, does not qualify. No ally-attack trigger, extraReaction or bypass of condition defenses is granted.',
 'All-mode0 and current-enclosing-turn endpoint; ordinary opportunity-hit identity.',
 'An opportunity hit during an enemy\'s movement setsSpeed0 through that enemy turn\'s end, preventing later ordinary movement.',
 'An independently legal teleport can still move the target; Sentinel does not turn0Speed into a teleport prohibition.')
add('sharpshooter',
 'Your attacks made with actual ranged-class weapons ignore the target\'s half and three-quarters cover for the attack comparison and ignore disadvantage solely from being beyond normal range but within that weapon\'s actual long range. Total cover, sight/perception, line of effect, ammunition, maximum range and all independent disadvantage remain. A thrown melee-class weapon is not automatically a ranged-class weapon; spell attacks do not qualify. A magical barrier that supplies only half/three-quarters cover is ignored for that cover term because the source makes no mundane restriction; a barrier\'s independent untargetability or damage prevention remains. No−5/+10, nearby-hostile disadvantage immunity, extra range or ability-score increase.',
 'Actual ranged-weapon classification and cover-term-only scope including magic cover without defeating barriers themselves.',
 'A longbow shot inside its long maximum ignores long-range disadvantage and three-quarters cover.',
 'A fully enclosing wall still prevents targeting, and an adjacent hostile can still impose proximity disadvantage.')
add('shield_master',
 'While actually wielding a usable shield, spendBA for one ordinary Shove against a creature within5ft. No prior Attack Action/hit is required. UseSTR Athletics opposed by defenderSTR Athletics/DEX Acrobatics, target at most one size larger, tie preserves state; on success choose5ft directly away or Prone. NEW the shield itself supplies the physical contact, so no separate empty grasping hand is required beyond actually wielding it. Shield proficiency is not a new acquisition requirement, but actual nonproficient-shield disadvantage applies to theSTR check and is not waived. A Broken shield cannot supply this maneuver. Buckler qualifies only while its actual body can be deliberately used to shove under current anatomy; no free extra hand is created. No damage, save bonus, evasion or extraBA.',
 'Usable shield as contact implement, ordinary contest and retained nonproficiency effects.',
 'A proficient shield user mayBA shove before any Attack Action; a successful contest can chooseProne.',
 'A nonproficient shield user still makes theSTR Athletics contest with the actual shield disadvantage.')
add('skulker',
 'You may attempt Hide when only lightly obscured, provided an actual source of light obscuration affects that observer\'s view; use the normal observer-specific Stealth/passive procedure. This is an express permission to try, not automatic Hidden, invisibility or an ability to hide in plainly unobscured sight. When your ranged-class weapon attack misses, suppress the ordinary attack-rule automatic position reveal caused by that missed shot for observers from whom you were Hidden. Do not end your Hidden record merely for the shot\'s normal firing noise/trajectory. NEW independent clear observation, a successful Search, movement into unobscured sight, communication revealing your position or another actual disclosure can still locate you; they are not negated by missing. A hit reveals normally. Spell misses and thrown melee-class weapons are outside this ranged-weapon clause. It neither improves vision in darkness nor suppresses all evidence permanently.',
 'Light-obscuration Hide permission and narrowly preserved position after a ranged-weapon miss.',
 'A hidden archer misses from light foliage; the miss alone does not reveal the archer\'s position.',
 'Stepping into a plainly visible lit doorway afterward still ends Hidden, regardless of the prior miss.')
add('slasher',
 'NEW once per turn, after your personal attack with a weapon whose native damage includes slashing hits, reduce each of the target\'s Speed modes by10ft, minimum0, through your next original regular start. A hit with0damage still qualifies. Same feat identity across owners applies one−10layer with independent expiries; distinct Crippling Strike can add a separate−10 under the proposed feat-family rule, before applicable halving/Speed0 overrides. Separately, any critical hit with that slashing weapon imposes disadvantage on all target attack rolls through your next original regular start. Same-name disadvantage never stacks extra dice. Reapplication can preserve later deadlines but grants no new condition beyond these explicit riders. No ability-score increase or trigger from a slashing spell/rider on a non-slashing weapon. Actual natural-weapon qualification requires its real profile.',
 'Once-turn speed rider, all modes, exact endpoint and separate critical rider/families.',
 'One Slasher hit changesSpeed30 to20; another owner\'s Slasher does not lower it again.',
 'If independently proposed Crippling Strike also applies, the two distinct−10layers yield10 before a separate halving; both proposals still need joint approval.')
add('tactical_insight',
 'BA: observe one actual perceived living creature within60ft and line of effect. Choose currentHP band, highest ordinary save modifier or lowest ordinary save modifier before rollingINT Investigation orWIS Insight againstDC10+ceil(actualCR); NEW useDC15 if the source supplies noCR. Apply ordinary fixed-DC task degrees/natural shifts; Success/Critical Success returns only the selected fact, failure none. NEW one attempt per actual target identity per completedLR, spent on the legal attempt even on failure; changing form/name or leaving initiative does not reset it. HP bands are Full, Positive-above-half, Positive-at-or-below-half, and Zero; effective maximum and normalHP govern, tempHP excluded. Highest/lowest uses actual six ordinary save modifiers including current unconditional proficiency/stat/item modifiers, not situational advantage or a specific opponent\'s conditional bonus; report all tied abilities. If complete actual data is unavailable or explicit information protection blocks it, return Indeterminate without fabricating a stat/type or diagnosing the protection. It is a specific information permission, not a general creature identification or exactHP read. MissingCR uses the fixed default without proving a hidden classification.',
 '60ft/perception, roundedDC/default, preselected information, precise bands/ties and per-targetLR attempt ledger.',
 'CR1/2 givesDC11. HP10/max20 reports Positive-at-or-below-half rather than an exactHP number.',
 'A failed attempt spends that target\'s allowance until a completedLR; a disguised version of the same individual is not a fresh target.')
add('tavern_brawler',
 'Gain actual improvised-weapon and unarmed-strike proficiency. Use the reviewed improvised object profile: an actually similar existing weapon can use its agreed full profile, otherwise1d4 appropriate physical type and20/60 throwing range. Ordinary unarmed damage is unchanged by this feat unless another actual source, such as Brawler, changes it. After your unarmed strike hits a creature on your own turn, you may spendBA that same turn for one ordinary Grapple of that same creature. NEW target must still be within actual reach and no more than one size larger, with a usable free grasping hand; use ordinary Athletics opposed by Athletics/Acrobatics. No damage or automatic success from the grapple. An improvised-weapon hit is not an unarmed hit for this trigger. Brawler\'s independently unconditionalBAgrapple remains broader; neither grants a secondBA or unprinted ability increase.',
 'Same-turn/same-target unarmed-hit gate and actual existing object/unarmed profiles.',
 'An unarmed hit can enableBAgrapple of that same nearby foe if a free hand remains.',
 'Hitting with a chair uses improvised proficiency but does not enable this feat\'s unarmed-hit grapple trigger.')
add('versatile_grip',
 'NEW explicit completion of the unresolved80%: when making an otherwise legal weapon attack with a weapon in which you lack proficiency, add floor(0.8×your currentPB) to that attack roll as a feat-specific training allowance instead of the ordinary zero proficiency contribution. Use exact4×PB//5 arithmetic. Damage remains normal; do not multiply the weapon\'s damage or whole attack total by80%, and do not claim this is the original source\'s recovered definition. If genuinely proficient, use normalPB and no extra allowance. This is not proficiency for acquisition/prerequisite, tool, save, maneuver or class gates. Actual Simple/Martial/Special profile, hands, anatomy, Heavy/size, ammunition and property restrictions remain. The allowance replaces rather than adds to another partial-proficiency contribution for that attack. No repeat stacking or new weapon item.',
 'Explicit NEW80%-of-PB attack allowance rather than undefined effectiveness; no proficiency credential.',
 'AtPB3 the allowance isfloor2.4=2, added to the actual attack ability; damage is unchanged.',
 'AtPB2 it is1. The owner still cannot choose that unproficient weapon as Weapon Focus\'s prerequisite.')
add('weaponFocus',
 'Choose one exact current weapon type/profile for which you have actual proficiency. NEW this feat may be selected again only for a different type, spending a real feat choice each time. Gain+1 on attack rolls actually using that chosen profile while that proficiency remains operative; no damage bonus. Melee/thrown use of that actual weapon qualifies if it retains the chosen profile; improvised use that changes it to a generic object does not. A specific natural-weapon profile or unarmed-strike profile can be chosen only with an actual proficiency receipt for that profile; do not select all weapons, all natural attacks or a damage type as one choice. Losing the usable profile/proficiency suppresses the bonus without erasing the record. Distinct eligible Precision Throw can add+1, while duplicate Focus on the same type cannot.',
 'Repeatable distinct types, current proficiency condition and exact profile versus family.',
 'Focus dagger adds1 to its legal melee or Thrown attack, not to every piercing weapon.',
 'Two paid Focus selections can cover rapier and longbow; selecting rapier twice does not create+2.')
add('weapon_master',
 'At acquisition choose four distinct actual weapon types/profiles from the current equipment catalog and gain proficiency with them; an already-proficient choice gives no additionalPB/expertise and is not replaceable for free later. NEW catalog Special weapons may be selected if their complete real profile exists, but proficiency does not waive actual attunement, anatomy, size, Two-Handed, loading or source-specific use permissions. Natural/unarmed attacks are not catalog weapon choices here. Increase permanentSTR orDEX by1, cap20 under the existing composite-grant rule. Choose the ability once; if already capped, the increase is0 but the four training choices remain. This grants no four items, blanket Simple/Martial proficiency, free retraining or extra class level. Actual feat-acquisition time/cost is governed by advancement, not an invented additional lesson requirement here.',
 'Four distinct catalog profiles, permitted existing special profiles, capped composite ability and no invented acquisition tax.',
 'Choose four actual weapon types andDEX19→20; no physical weapons appear in inventory.',
 'Choosing a weapon already proficient does not make it expertise. STR20 remains20 while the other training grants still apply.')
add('companion_training',
 'Require the exact Animal Companion feat OR actual Animal Handling proficiency. Your genuinely bound/tamed Beast companions under your lawful current command gain+2 to their attack rolls and+2flat once per native attack damage roll, not per die/type or critical doubling. NEW no benefit to an ordinary allied Beast, non-Beast construct/undead/familiar, or a body you have no actual companion/control relation with. Original source-owner stats remain; add this feat layer once across overlapping trainers. For real tracking checks, if you are proficient in Survival, the companion uses its ownWIS plus your currentPB as the inherited proficiency contribution; expertise is not inherited, and a better real own contribution can replace it, not add twice. If you lack Survival proficiency, nothing is inherited. During your regular turn spend the sharedBAcommand within60ft to one companion that can hear you, selecting attack, Dash, Disengage or Help. At total level10+, the same command can name two audible owned companions taking that same action in their attached phases. This changes command recipient count only: one shared offensive companion action per owner numbered round remains. For attack, designate at most one to spend that offense; the other may move defensively and Dodge, not bank an attack. Two pure support actions can both resolve if legal. Command fails without refund if eligibility is lost; no extra independent turns/Reactions. When one of your actually commanded Beast companions reduces a meaningful hostile from positiveHP to0, you gain one advantage entitlement for your next attack against a creature within30ft of you before your next future regular end. NEW only an attack meeting30ft consumes it; a farther attack does not. Same-family reapplication refreshes one entitlement/deadline, never queues multiple. Death is not required, source floors/copy/no-reward restrictions apply.',
 'Actual Beast companion relation, additive single layer, inherited proficiency arithmetic, two-recipient command within unchanged shared offense and bounded owner reward.',
 'At level10, two companions can each perform a legal Help from the one shared command; an Attack command still permits only one shared offensive action.',
 'A commanded Beast downs a hostile: the owner\'s next attack within30ft gains advantage before the deadline; no extra attack is granted.')
add('primal_instinct',
 'Gain advantage on actualWIS Perception checks relying on working hearing or smell, without a passive±5 adjustment. While conscious, surprise restrictions are suppressed as in Alert, with no retroactive actions. When actually tracking a real trail, ignore penalties caused solely by difficult terrain; preserve absent evidence, concealment, age, weather and source-specific no-trace restrictions. NEW the moonlight/transformed clause qualifies both the+2initiative and howl: at the actual initiative roll, if physically illuminated by real existing moonlight or in an actual body-transforming form, add2. It does not establish an astronomical calendar, count a moon-themed spell as moonlight, or treat an illusion/disguise as body transformation. Once perSR while that predicate holds, on your own regular turn without an Action cost, audibly howl/roar and choose one actual creature you are currently tracking through a legal source or personally damaged during this encounter. Other allies within30ft who hear at the moment gain advantage on their next attack against that chosen creature before your next future regular end. NEW recipient list and target are fixed, no continuing range tether and no extra attack; one family entitlement per ally, consumed by its first eligible attack hit/miss/cancellation. The body must actually be able to howl or roar; articulated speech or a shared language is not required. Silence or an anatomy unable to make that sound prevents it. Conditions otherwise permit this brief free communication but do not grantActions. Tracking alone does not reveal a target\'s present location for an attack.',
 'Actual hearing/smell, terrain-only tracking relief, literal moonlight/body-change predicate and complete free-own-turnSR howl contract.',
 'A transformed owner howls on its turn for a foe it actually damaged; hearing allies receive one next-attack advantage through the owner\'s next regular end.',
 'A moon-painted lantern is not actual moonlight. The feat creates neither transformation access nor current location knowledge from an old trail.')

animal_templates=[
 {'id':'feat-animal.ground','name':'Ground companion','status':'NEW feat-only profile, not a recovered monster record',
  'eligibleBody':'An actual positive-HP living Small or Medium terrestrial Beast with ordinary biting anatomy; preserve its actual size. Dog/fox-like examples are illustrative, not free supplied animals.',
  'abilities':{'STR':12,'DEX':12,'CON':12,'INT':3,'WIS':12,'CHA':6},
  'movement':{'walkFeet':30},'attack':'One melee bite, reach5ft, attack=ownerPB+owner actualWIS modifier, damage1d6piercing; no addedWIS damage and no automatic level scaling.',
  'sense':'Choose its actually sourced keen hearing OR smell, if present, for advantage on that sense\'s actual Perception checks. No new keen sense if absent.',
  'limits':'No Pack Tactics, knockdown, grapple, multiattack, burrow or extraordinary source powers. Carrying uses this actual body/STR and ordinary Load/pounds limits, real harness/hands. A mount must separately meet real riding eligibility.'},
 {'id':'feat-animal.flyer','name':'Flying companion','status':'NEW feat-only profile, not a recovered monster record',
  'eligibleBody':'An actual positive-HP living Tiny winged Beast that already possesses natural flight and a pecking/biting attack. No Hover.',
  'abilities':{'STR':3,'DEX':14,'CON':10,'INT':3,'WIS':14,'CHA':6},
  'movement':{'walkFeet':10,'flyFeet':30},'attack':'One melee peck/bite, reach5ft, attack=ownerPB+owner actualWIS modifier, damage1d4piercing; no addedWIS damage and no level scaling.',
  'sense':'Retain actual sourced keen sight, if present, as advantage on that sense\'s Perception checks; no automatic darkvision/blindsight.',
  'limits':'No free Flyby, invisibility, aerial carrying exception, Hover, multiattack or ability to carry a Medium ally. Ordinary falling, weather, carrying and support apply.'},
 {'id':'feat-animal.swimmer','name':'Swimming companion','status':'NEW feat-only profile, not a recovered monster record',
  'eligibleBody':'An actual positive-HP living Small Beast with native swimming and biting anatomy. Keep its real breathing requirements; a fish gains no lungs and an air breather gains no gills.',
  'abilities':{'STR':10,'DEX':12,'CON':12,'INT':3,'WIS':12,'CHA':6},
  'movement':{'walkFeet':5,'swimFeet':30},'attack':'One melee bite, reach5ft, attack=ownerPB+owner actualWIS modifier, damage1d6piercing; no addedWIS damage and no level scaling.',
  'sense':'Retain one actually sourced keen hearing OR smell, if present, for that sense\'s Perception advantage only.',
  'limits':'The5ft ground movement is crawling/flopping for a body without legs, paying ordinary crawl cost and suffocation/exposure; no new hands, amphibiousness, Water Breathing, multiattack or sonar.'}
]
animal_common={
 'profile':'AC12+floor(current ownerPB/2); dynamic maximumHP5+current total owner level; all ordinary saves use current ownerPB alone; other ability checks use template ability modifiers, no PB unless a real source grants it. Template INT3 is a feat-profile value, not proof that a real source beast meets the INT<7 admission gate.',
 'nativeBody':'Preserve actual original source profile, body identity, current health ratio, size, breathing, conditions, disease, hunger, custody and age. Templates replace only their stated combat/ability/speed values for this bond. Any actual anatomy incapacity/sensory blocker remains. No template creates a supernatural sense, trait, hand or extra body.',
 'actions':'One command and offensive allowance across owner companions/devices per numbered round. Commanded body has one attached phase after whole owner regular turn, move plus chosen legal attack or standard Dash/Disengage/Help/Dodge; Dash adds one currentSpeed to its phase cap, Disengage suppresses opportunities for that phase, Help follows actual5ft/physically possible aid and expires at the next original companion-start marker. No independent BA/Reaction/turn/death save; no extra-turn phase. Uncommanded only defensive movement/Dodge.',
 'conversion':'Admission requires a real living animal with positiveHP and positive maximumHP and an actual eligible willing/tamed receipt. Initial and release conversion preserves health ratio using max(1,floor(newMax*oldHP/oldMax)), not a heal/damage event. At0 the feat animal is dead, never eligible for conversion. Save the prior source profile rather than deriving a new one on release.',
 'recovery':'No resummon, free rest healing, unprinted Hit Dice or new original animal from a saved profile. External legal healing/resurrection retains its actual costs and rules; resurrection returns the same body unbonded, and new bonding still requires the post-death completedLR plus full procedure. Capacity change never repairs injury, replenishes resources or creates death/HP-loss triggers.'
}
maneuvers=[
 {'id':'feat-maneuver.measured-strike','name':'Measured Strike','activation':'Within one actual weapon attack, before its attack roll','cost':'One superiorityd6',
  'procedure':'Roll the spentd6 and add it to that one attack roll. Choose before seeing the d20/outcome; natural1 still misses and no extra critical range is created. It adds no damage and supplies no attack, target permission or extra Action.',
  'basis':'NEW attack-check enhancement; not an imported Battle Master maneuver.'},
 {'id':'feat-maneuver.driving-shove','name':'Driving Shove','activation':'Replace one Attack Action attack with ordinary Shove','cost':'One superiorityd6 plus the replaced attack',
  'procedure':'Before both opposed rolls, spend/roll thed6 and add it to yourSTR Athletics total for that one ordinary Shove. Target choosesAthletics/Acrobatics; tie preserves state. Actual reach/one-size-larger cap applies; success still pushes5ft away OR Prone, never both solely from this maneuver. It adds no damage.',
  'basis':'NEW finite bonus on reviewed ordinary Shove; printed feat/class save-based Shoves are not this maneuver.'},
 {'id':'feat-maneuver.disarming-feint','name':'Disarming Feint','activation':'Replace one Attack Action attack with ordinary opposed Disarm','cost':'One superiorityd6 plus replaced attack',
  'procedure':'Choose a reachable actually held droppable item and an ordinary legal Athletics or weapon-check Disarm. Before rolls, spend/roll thed6 and add it to your one opposed total; defender usesAthletics/Acrobatics, tie preserves state. Success uses the existing adjacent/own-space drop placement, not automatic custody. No damage, severed bond or proficiency grant. The save-based Disarm feat and Whip Control are separate procedures and do not acquire this bonus.',
  'basis':'NEW finite die on reviewed ordinary Disarm only.'},
 {'id':'feat-maneuver.guarding-deflection','name':'Guarding Deflection','activation':'Reaction when one direct damage event would damage you','cost':'One superiorityd6 and the actual Reaction',
  'procedure':'After passive defenses but before tempHP, spend/roll1d6 to reduce that whole resolved event by its face, minimum0. Allocate across stable native component order. Attached conditions remain. No re-mitigation of transfer packets that forbid recipient mitigation, HP sacrifice, state assignment or direct death. It neither changes a hit to a miss nor qualifies as Riposte\'s successful Parry.',
  'basis':'NEW finite physical defense using current whole-event/damage-provenance interface.'},
 {'id':'feat-maneuver.measured-advance','name':'Measured Advance','activation':'Bonus Action on your own regular turn','cost':'One superiorityd6 and the actual BA',
  'procedure':'Spend/roll1d6, gaining a separate movement-cost budget of5×face feet resolved immediately. Use one already available movement mode with nonzeroSpeed, pay normal terrain/crawl/squeeze costs, respect legal endpoints and provoke ordinary opportunity attacks. No teleport, new movement mode, free Disengage, replenished ordinary movement or banked distance. Interrupted unspent distance is lost.',
  'basis':'NEW bounded movement procedure; no copied Soldier grant.'},
 {'id':'feat-maneuver.rallying-signal','name':'Rallying Signal','activation':'Action under the ordinary Rally procedure','cost':'One superiorityd6 and the actual Action',
  'procedure':'Choose one actual ally within30ft able to perceive the rally and one active source-qualifiedFrightened record. Before rolling the ordinaryCHA task check at its sourceDC (otherwise10), spend/roll thed6 and add its face to the total. Apply actual task degrees/natural shift; success ends only that selected record. NoHP/tempHP, loyalty, extra save, new ally turn or automatic cure of other fear records.',
  'basis':'NEW finite die on current reviewed Rally.'}
]

# Compile against actual sources. No output has been written above this point.
checks=[]
def check(name,value):
 checks.append({'name':name,'pass':bool(value)})
 assert value,name
registry=R/'src/data/feats.js'; manifest=R/'data/public/feat_playtests/manifest.json'
feats=json.JSONDecoder().raw_decode(registry.read_text('utf-8').split('export const feats = ',1)[1])[0]
by={f['id']:f for f in feats}; approved=set(read(manifest)['operationalIds'])
check('335 unique original feats and eight reviewed full feats',len(feats)==len(by)==335 and len(approved)==8)
check('58 exact source identities and questions',len(P)==len(sources)==58 and {x['featId'] for x in P}==set(sources) and {x['questionId'] for x in P}=={f'GC-{n:02d}' for n in range(1,59)})
check('Both original feat registries remain byte-identical',registry.read_bytes()==(G/'src/data/feats.js').read_bytes())
prior_index=R/'data/director/feat_operating_proposal_index.json';previous=read(prior_index)
prior_ids={x['featId'] for x in previous['records'] if x['proposalManuscript']}
check('Prior index has189 treatments,187 complete and two deferred',len(prior_ids)==189 and previous['completeProposedProcedures']==187 and previous['deferredPayloadGrantInterfaces']==2)
check('58 general combat proposals are disjoint from prior189',prior_ids.isdisjoint(sources))
inputs={registry,G/'src/data/feats.js',manifest,prep_file,A/'GENERAL_COMBAT_FEAT_SOURCE_AUDIT.md',combat_file,magic_file,prior_index}
for path in prep['protectedFiles']:inputs.add(G/path)
records=[]
for p in P:
 s=sources[p['featId']];f=by[p['featId']]
 check(p['questionId']+' preserves complete original object',s['sourceObject']==f)
 check(p['questionId']+' retains original question',bool(s['fullClauseQuestion']))
 check(p['questionId']+' remains pending full review',p['featId'] not in approved)
 check(p['questionId']+' complete nonempty proposal with two authored cases',len(p['procedure'])>150 and len(p['workedCases'])==2 and p['procedureScope']=='complete-proposed-feat')
 records.append({**p,'sourceObject':f,'sourceObjectSha256':s['sourceObjectSha256'],'originalQuestion':s['fullClauseQuestion'],
                 'status':'unadopted-complete-feat-proposal','authoredCasesAreRuntimeTests':False})
for row in prep['counterpartSources']:
 check('Counterpart source preserved: '+row['sourceObject']['id'],row['sourceObject']==by[row['sourceObject']['id']])

spellroot=R/'data/public/spell_playtests';catalog_file=spellroot/'catalog.json';spell_index_file=spellroot/'authored_review_index.json'
catalog=read(catalog_file);spell_index=read(spell_index_file);spell_by={x['id']:x for x in catalog['spells']};si={x['id']:x for x in spell_index['entries']}
inputs.update([catalog_file,spell_index_file])
check('Current ordinary spell authored counts preserved',spell_index['authoredCounts']=={'reviewed':412,'pending':436})
ability_map={'Bard':'CHA','Cleric':'WIS','Crimson Agent':'INT','Dragoon':'STR','Druid':'WIS','Mage':'INT','Monk':'DEX','Mirrorsage':'INT','Paladin':'CHA','Ranger':'WIS','Shaman':'WIS','Thief':'DEX','Tinker':'INT','Wizard':'INT','Sorcerer':'CHA','Warlock':'CHA'}
expected_counts={'Bard':(47,46),'Cleric':(63,59),'Crimson Agent':(62,61),'Dragoon':(48,48),'Druid':(64,64),'Mage':(80,79),'Monk':(48,48),'Mirrorsage':(63,59),'Paladin':(64,59),'Ranger':(48,48),'Shaman':(64,64),'Thief':(64,62),'Tinker':(64,63),'Wizard':(140,135),'Sorcerer':(6,6),'Warlock':(6,6)}
curricula={};dependencies={};filecache={}
for name,ability in ability_map.items():
 legacy=name in ('Sorcerer','Warlock')
 if legacy:
  choices=magic['currentChoicePools'][name]['choices']
 else:
  choices=[]
  for spell in catalog['spells']:
   access=spell['classAccess'].get(name)
   if access is None or access['rank'] not in (0,1):continue
   entry=si[spell['id']]
   choices.append({'id':spell['id'],'name':spell['name'],'rank':access['rank'],'school':access['school'],'sourceClass':name,
    'fullOriginalClassAccessRow':access,'authoredStatus':entry['authoredStatus'],'currentProcedureFile':entry['procedureFile'],
    'currentWholeCardPointer':entry['wholeCardPointer'],'sourceStatusUnchanged':spell.get('status')})
 check(name+' exact finite rank0/rank1 counts',tuple(sum(x['rank']==r for x in choices) for r in (0,1))==expected_counts[name])
 check(name+' no repeated spell identity in curriculum',len(choices)==len({x['id'] for x in choices}))
 for choice in choices:
  fid=choice['id'];entry=si[fid];access=spell_by[fid]['classAccess'][choice['sourceClass']]
  check(name+' source access and current procedure: '+fid,access==choice['fullOriginalClassAccessRow'] and entry['authoredStatus']==choice['authoredStatus'] and entry['procedureFile']==choice['currentProcedureFile'] and entry['wholeCardPointer']==choice['currentWholeCardPointer'])
  if fid not in dependencies:
   path=spellroot/entry['procedureFile'];inputs.add(path)
   if path not in filecache:filecache[path]=read(path)
   whole=pointer(filecache[path],entry['wholeCardPointer'])
   check('Exact current whole spell payload: '+fid,whole['id']==fid)
   dependencies[fid]={'currentAuthoredIndexEntry':entry,'completeOriginalCatalogObject':spell_by[fid],
                       'completeCurrentProcedureCard':whole,'currentProcedureFile':path.relative_to(G).as_posix(),
                       'purpose':'Source dependency only. A pending payload stays pending; this feat does not authorize it.'}
 curricula[name]={'status':'NEW finite legacy feat curriculum; not a current class or class alias' if legacy else 'NEW feat grant and ability assignment over unchanged actual classAccess rows',
                  'featCastingAbility':ability,'rank0Choices':expected_counts[name][0],'rank1Choices':expected_counts[name][1],
                  'selection':'Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.',
                  'ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax':True,'choices':choices}
for name in ['Oracle','Soldier','Warrior']:
 check(name+' has no rank0+rank1 ordinary curriculum',not any(s['classAccess'].get(name,{}).get('rank') in (0,1) for s in catalog['spells']))
class_manifest_file=R/'data/public/class_playtests/manifest.json';class_manifest=read(class_manifest_file);inputs.add(class_manifest_file)
class_comparisons=[]
for entry in class_manifest['classes']:
 path=(R/'docs/mechanics'/entry['data']).resolve();data=read(path);inputs.add(path)
 class_comparisons.append({'class':entry['class'],'file':path.relative_to(G).as_posix(),'currentFile':info(path),
                          'completeCurrentEngine':data.get('engine'),'specialBardFullClassSource':data if entry['class']=='Bard' else None,
                          'purpose':'Actual class comparison; Bard uses its separate source schema. Feat assignments neither acquire nor rewrite these engines.'})
check('All17 current class comparisons retained, including separate Bard schema',len(class_comparisons)==17 and all(x['completeCurrentEngine'] or x['specialBardFullClassSource'] for x in class_comparisons))
actual_cards=[]
for entry in prep['classComparisonSources']:
 path=G/entry['file'];data=read(path);inputs.add(path);card=next(x for x in data['cards'] if x['id']==entry['card']['id'])
 check('Exact current companion/maneuver comparison: '+card['id'],card==entry['card'])
 actual_cards.append({'file':entry['file'],'currentFile':info(path),'actualCard':card,'completeCurrentEngine':data['engine']})
for excerpt in prep['currentGoverningExcerpts']:
 path=G/excerpt['file'];inputs.add(path)
 check('Governing excerpt still literal: '+excerpt['heading'],excerpt['exactText'] in path.read_text('utf-8-sig'))
input_info={p.relative_to(G).as_posix():info(p) for p in sorted(inputs)}
arithmetic=[
 ('Alertness passive10 WIS2 PB3 bonus2',10+2+3+2,17),
 ('Distinct initiative feat bonuses',5+2+2,9),
 ('Animal AC PB3',12+3//2,13),
 ('Animal maxHP level5',5+5,10),
 ('Animal admission preserves halfHP',max(1,(10*4)//8),5),
 ('Animal release preserves positive wounded body',max(1,(8*3)//10),2),
 ('Animal maxHP capacity growth does not heal current3',min(3,5+6),3),
 ('Versatile Grip PB2',4*2//5,1),
 ('Versatile Grip PB3',4*3//5,2),
 ('Versatile Grip PB6',4*6//5,4),
 ('Orcish Fury critical2d6 weapon plus1base die',2*(2+1),6),
 ('Piercer critical rapier plus postcritical one die',2*1+1,3),
 ('Tactical Insight fractional CR default rounding',10+1,11),
 ('Tactical Insight exact halfHP belongs lower band',2*10<=20,True),
 ('Distinct Slasher and Cripple then halving',max(0,30-10-10)//2,5),
 ('Measured Advance die3 budget',5*3,15),
 ('Measured Advance15 budget difficult5ft tiles',15//10,1),
 ('Companion Training native1d6critical flat2',2*1,2),
 ('Companion Training Survival WIS1 ownerPB3',1+3,4),
 ('Weapon Master capped ability',min(20,20+1),20),
]
for name,actual,expected in arithmetic:check(name,actual==expected)
for path,expected in read(A/'EXPEDITION_INTEGRATED_V3_PREPARATION.json')['manifest'].items():
 if path!='README_EXPEDITION_INTEGRATED_V3.md':check('Submitted current payload unchanged: '+path,info(G/path)==expected)
status='UNADOPTED, UNSENT. All58 general combat feats remain pending joint source conference and exact review. Complete original objects and wording are retained; no public registry, current governing rule or class/spell card is changed.'
created=datetime.now(timezone.utc).isoformat()
shared_casting={k:magic['sharedProposal'][k] for k in ['featCastingRoute','castingCostsAndStrain','focusAndHands']}
save(draft_path,{'status':status,'createdAtUtc':created,'sharedProposal':shared,'proposals':P,'authoredExamples':116,'runtimeImplemented':False})
save(out,{'status':status,'createdAtUtc':created,'sharedProposal':shared,'records':records,
 'proposedCombatConventionDependency':combat['sharedProposal'],'proposedMagicCastingDependency':shared_casting,
 'newAnimalCompanionCommonRules':animal_common,'newAnimalCompanionProfiles':animal_templates,'newFeatOnlyManeuvers':maneuvers,
 'magicInitiateCurricula':curricula,'completeCurrentSpellDependencies':dependencies,'currentClassEngineComparisons':class_comparisons,
 'currentCompanionAndManeuverCardComparisons':actual_cards,'originalCounterpartFeatSources':prep['counterpartSources'],
 'originalAncestryComparisons':prep['exactAncestryMatches'],'scopedOriginalManeuverSearch':prep['namedManeuverSearch'],
 'currentGoverningExcerpts':prep['currentGoverningExcerpts'],'sourceFiles':input_info,
 'sourceFeats':335,'reviewedFullFeatsUnchanged':8,'pendingFullFeatsUnchanged':327,'completeProposedFeatsInThisCohort':58,
 'sourceInformationDeleted':0,'runtimeImplemented':False,'cosmologyReviewed':False})
lines=['# General combat feats: complete operating proposal','',
 '**UNADOPTED — all58 original general combat feats remain pending full review.** This manuscript supplies one complete proposed procedure and two authored adjudications for each GC-01–58 source question. Every NEW interpretation is for joint discussion; original source wording and records are preserved.','',
 '[Complete structured proposal and sources](../../data/director/general_combat_feat_operating_proposal_internal.json) · [Original source audit](../../../../docs/audit/2026-10-08/full-game/GENERAL_COMBAT_FEAT_SOURCE_AUDIT.md) · [Preservation and arithmetic receipt](../../../../docs/audit/2026-10-08/full-game/GENERAL_COMBAT_58_OPERATING_PROPOSAL_CHECK.json)','',
 'The116 worked examples are authored expectations, not runtime tests or human play. No current feat, spell, class or companion is activated by this document.','',
 '## Shared proposed rules','']
for title,body in shared.items():lines+=['### '+title,'',body,'']
lines+=['## Carried proposal dependencies','', 'These are earlier UNADOPTED proposals, reproduced to make the cross-feat contract reviewable. They remain subject to the same joint review.','']
for title,body in combat['sharedProposal'].items():lines+=['### Combat — '+title,'',body,'']
for title,body in shared_casting.items():lines+=['### Magic — '+title,'',body,'']
lines+=['## All58 original feat questions','']
for x in records:
 f=x['sourceObject'];lines+=['### '+x['questionId']+' — '+f['name'],'',f"Source identity: `{f['id']}`. Original prerequisite: **{f['prerequisite']}**.",'',
 '**Original effect, unchanged**','',f['effect'],'','**Proposed complete procedure**','',x['procedure'],'','**Explicit NEW choices:** '+x['newChoices'],'','**Worked adjudications**','']
 for case in x['workedCases']:lines+=['- '+case,'']
 lines+=['**Dependencies:** '+'; '.join(x['dependencies'])+'.','','<details><summary>Complete original source and conference question</summary>','','```json',json.dumps(f,ensure_ascii=False,indent=2),'```','',x['originalQuestion'],'','</details>','']
lines+=['## NEW animal companion profiles','', 'These three finite feat-only profiles require an actual eligible animal. They do not import monster traits, supply a free animal or replace Ranger class cards.','']
for title,body in animal_common.items():lines+=['### '+title,'',body,'']
for profile in animal_templates:
 lines+=['### '+profile['name'],'']
 for key,value in profile.items():
  if key=='name':continue
  lines+=['**'+key+':** '+(json.dumps(value,ensure_ascii=False) if isinstance(value,dict) else value),'']
lines+=['## NEW feat-only maneuver menu','', 'Martial Adept chooses two of these six; its exact Advanced feat adds two different choices. One shared superiority-die pool and one maneuver per event apply. No current class called Battle Master or its absent menu is presumed.','']
for m in maneuvers:
 lines+=['### '+m['name'],'','**Activation:** '+m['activation']+'. **Cost:** '+m['cost']+'.','',m['procedure'],'',m['basis'],'']
lines+=['## Generic Magic Initiate: exact finite curricula','',
 'Choose one curriculum, two distinct rank0 spells and one rank1 spell permanently. The rank1 grant has its own1/LR charge under the reproduced casting rules. The abilities below are explicit NEW feat assignments, not changes to ordinary class engines. Fourteen curricula use actual current class rows; Sorcerer and Warlock are finite NEW legacy feat curricula, not new classes. Oracle, Soldier and Warrior have no ordinary low-rank curriculum in the current catalog.','',
 'Each choice below preserves its complete original classAccess row and full current procedure card in the structured companion. The authored review index controls current spell status; an older catalog status is retained as history. A pending spell cannot be used through this feat until its own exact payload approval. Generic and named Magic Initiate in the same curriculum belong to one nonduplicating family.','']
for name,pool in curricula.items():
 lines+=['### '+name+' — '+pool['featCastingAbility'],'',pool['status']+'.','',
 '| Spell identity | Name | Rank | School | Actual source class | Current authored status |','|---|---|---:|---|---|---|']
 for choice in pool['choices']:
  lines.append(f"| `{choice['id']}` | {choice['name']} | {choice['rank']} | {choice['school']} | {choice['sourceClass']} | {choice['authoredStatus']} |")
 lines.append('')
lines+=['## Joint decisions still required','',
 'Review every GC source question and proposed completion, especially stacked initiative, exact surprise and sensing permissions, full companion acquisition/death/custody, feat reaction cadence, same-event attack recursion, spell-for-opportunity substitution, Tactical Insight information limits, extra weapon dice and rerolls, generic Magic Initiate curricula/ability assignments, finite new maneuvers, Versatile Grip\'s explicit80%-of-PB interpretation and Companion Training\'s two-recipient command within the shared one-offense allowance.','',
 'Reconcile the actual expedition verdict before dispatching the complete feat package. Literal moonlight or body-transformation predicates do not authorize cosmology interpretation. These58 entries remain source-authoring proposals, not reviewer agreement or runtime/balance approval. Final joint whole-game flow agreement precedes the authorized GitHub push; verified remote commit precedes careful cosmology review.','']
doc.write_text('\n'.join(lines),encoding='utf-8',newline='\n')
for path,expected in input_info.items():check('Input unchanged during authoring: '+path,info(G/path)==expected)
for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',doc.read_text('utf-8')):
 path=(doc.parent/target).resolve();check('Document link: '+target,path.exists() or path==receipt)
summary={'status':status,'createdAtUtc':created,'sourceRecords':58,'originalQuestions':58,'completeProposedFeatProcedures':58,
 'authoredExamples':116,'checks':len(checks),'failures':0,'plainArithmeticChecks':len(arithmetic),'existingReviewedComponentQueries':0,'fullFeatRuntimeCases':0,
 'sourceFeats':335,'reviewedUnchanged':8,'pendingUnchanged':327,'combinedSourceFeatsWithProposedTreatment':247,
 'combinedCompleteProposedFeats':245,'combinedDeferredGrantInterfaces':2,'combinedSourceQuestionOnlyFeats':80,'combinedAuthoredExamples':500,
 'newSupplementalFeatProposalsOutsideOriginalRegistry':1,'finiteCurricula':16,'currentRealClassCurricula':14,'newLegacyFeatCurricula':2,
 'completeCurrentSpellDependencies':len(dependencies),'newAnimalProfiles':3,'newFeatManeuvers':6,'submittedCurrentPayloadsUnchanged':303,
 'artifacts':{p.relative_to(G).as_posix():info(p) for p in [draft_path,out,doc]},'details':checks,
 'sourceInformationDeleted':0,'cosmologyReviewed':False,'pushed':False}
save(receipt,summary)
print(json.dumps({k:v for k,v in summary.items() if k!='details'},ensure_ascii=False))
