"""One-shot, standard-library review of the full general-combat stated casebook.
No project, supplied verification, downloaded program or game runtime is executed.
"""
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
import json, hashlib, math, zipfile
G=Path(r'C:\Github\DecenniumDescent'); R=G/'DescentReviewChanges/ReviewBible'; A=G/'docs/audit/2026-10-08/full-game'; I=R/'data/director/feat_candidates/exact_01'; D=A/'feat335-ft84-derived-review-92/after/DescentReviewChanges/ReviewBible'
ROOT=A/'feat335-general-combat-casebook-99'; OUT=A/'FEAT335_GENERAL_COMBAT_ORIGINAL_CASEBOOK_REVIEW_99.json'; ZIP=A/'DD_Feat335_General_Combat_Casebook_Review_99.zip'; SAVED=A/Path(__file__).name
for p in [ROOT,OUT,ZIP,SAVED]: assert not p.exists(),str(p)
def j(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v): return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b): return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes(); return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
def put(p,b):
 with p.open('xb') as f: f.write(b)
checks=[]
def ck(n,ok): checks.append({'check':n,'pass':bool(ok)}); assert ok,n
selected=[r for r in j(I/'candidate.json')['records'] if r['cohort']=='general_combat']; records={r['id']:r for r in selected}
cases=[x for x in j(I/'example_dispositions.json')['cases'] if x['featId'] in records]; boundaries=[x for x in j(I/'additional_boundary_expectations.json')['cases'] if x['featId'] in records]
ck('58 complete procedures116 original positions3 boundaries',len(selected)==58 and len(cases)==116 and len(boundaries)==3)
notes={
'GC-01':[
'Alert removes the Hidden-only attack-advantage cause without identifying an unknown square. Independent unseen/darkness/Invisible causes and ordinary disclosure from the actual shot still require their own rules; this is not general vision.',
'Distinct Alert5 and Alertness2 add7 only on an actual new initiative roll. Becoming conscious suppresses the extant surprise restriction without restoring a spent token, missed decision or retroactive turn.'],
'GC-02':[
'The actual passive base is10+WIS2+PB3=15; one flat Alertness2 gives17. The feat does not add proficiency twice or invent a passive advantage adjustment.',
'The distinct plus2 initiative bonus supplies neither surprise immunity nor a fresh initiative roll. Conscious Alert protection, if separately present, remains a different feature.'],
'GC-03':[
'A genuinely legal ordinary two-weapon Bonus Action attack restores positiveDEX3 on its damage. Actual two Light one-hand melee weapons, hands, Attack Action and available Bonus Action remain required; this is not a blanket Double Tap or crossbow exception.',
'Non-Light pairing still requires the independently acquired Dual Wielder. Ambidexterity restores only the ordinary omitted positive ability modifier; it does not change weapon properties, supply a hand or grant the attack.'],
'GC-04':[
'A level5 owner sets the qualified ground template maximum to5+5=10. The real living positiveHP animal at half its ordinary maximum converts proportionally to5, preserving injuries, conditions, custody and actual anatomy; no free animal or full heal is granted.',
'The feat chassis dies at0 and leaves the same real corpse. Rest can restore the owner attempt under its exact limits but cannot resurrect, replace or rebond a dead animal; a later legal bond needs a real eligible animal, post-end beneficial rest, attempt and uninterrupted hour.'],
'GC-05':[
'No universal flanking advantage exists to remove in this candidate. Tactical Flanker supplies its separate lawful die, which this anti-flanking-advantage clause does not suppress.',
'The plus1AC compares only against an actual opportunity attack, including an eligible polearm entry attack. Mage Slayer is a different Reaction attack; a replaced Combat Casting spell is also not an actual opportunity-attack hit.'],
'GC-06':[
'After a qualifying direct Finesse hit on a meaningful hostile and its damage, a separate5-cost immediate movement can cover5ft normal terrain. The step suppresses opportunity attacks from everyone but grants no Action or usable movement while Speed is0.',
'A second same-actual-turn hit cannot claim another step. One difficult5ft tile costs10, exceeding this separate5-cost budget; ordinary movement is not silently pooled into it. Final unqualified once-per-turn follows genuine actual turns, not extra Actions.'],
'GC-07':[
'Conscious nonvisual location sensing reaches30ft through legal line of effect, so the20ft body can be located without hearing. Location does not establish can-see, read text or true visual identity; the named Blinded-cause relief does not erase every independent unseen cause.',
'A closed solid wall defeats the line even within10ft. Leaving the30ft range ends live location updates; previously known position is history, not an automatic tracker through cover or distance.'],
'GC-08':[
'Within10ft, this distinct effective nonvisual sight can meet an ordinary can-see condition through fog if line of effect and conscious capability remain. It does not reveal colors, text, true identity or unsupported illusion details.',
'Blind Fight30 and Blind Fighting10 retain their different operations. At20ft the former can locate but cannot extend the latter can-see permission; ranges do not add to40.'],
'GC-09':[
'The replacement unarmed base is1d4+STR2, not an added die on top of a Monk base. Choose an independently legal larger base instead, retaining its actual ability and proficiency rules.',
'Brawler permits an ordinary Bonus Action grapple before attacking. It still needs an actual free grasping hand, reach, size eligibility and opposed contest; weapons occupying every usable hand prevent it.'],
'GC-10':[
'Cavalry literally applies to actual attacks against an unmounted target while riding, including this ranged attack against a larger giant. Other disadvantage can cancel it; save-only effects are not attacks.',
'Two holders supply one plus10 family to each actual independent mount Speed, with derived modes following their parent once. A walking-only horse acquires no flight, no extra phase and no additional movement wallet from its passengers.'],
'GC-11':[
'A legal own-turn Action Dash permits one legal Bonus Action melee weapon attack or ordinary shove. No10ft approach, added damage or added push requirement is supplied by this feat; both actual action costs remain.',
'A Bonus Action Dash is the wrong trigger and spends the ordinary Bonus Action wallet. Neither the label Dash nor the resulting movement grants another Bonus Action.'],
'GC-12':[
'A genuine meaningful-hostile positive-to-zero transition after floors on the owner regular interval can permit one immediate legal nonspell melee attack against a different target. Dying rather than dead can qualify; reach, implement and causal-root restrictions remain.',
'The derived follow-up cannot recursively create Cleave or Great Weapon Master. A shared source event chooses one eligible derived grant without banking the others; no new Action, Bonus Action or attack chain is created.'],
'GC-13':[
'The actual opportunity trigger and available Reaction can instead fund an accessible Action-time spell targeting exactly that one creature. Resolve at the original pre-leave timing with actual range, line, components, route costs, concentration and Dissonance; the spell is not itself an opportunity-attack hit.',
'An area affecting only one present enemy is still an area spell. Self, longer-time, Bonus Action or Reaction spells do not become eligible Action-time exactly-one-creature spells by convenient occupancy or label.'],
'GC-14':[
'Activation must commit a legal attack before the first attack of the own regular interval. The minus1 applies to that attack and all later attacks while plus1AC lasts through next original regular start, even if the first attack misses.',
'A prior unpenalized attack closes activation for that interval. It is not a freely toggled stance, a scaling trade or a way to purchase only the defensive side after attacking.'],
'GC-15':[
'The ordinary Reaction refreshes on the owner regular start; the independent extra token refreshes once per numbered global round. Spending the ordinary token before a late slot does not alter the extra-token clock or permit an extra-turn refill.',
'Distinct real opportunity events may each spend one available token. The same triggering departure can produce only one Reaction by this owner across both wallets; replayed callbacks or two token names do not create two attacks.'],
'GC-16':[
'The current self-ally replacement is valid when the holder can perform and perceive the coordination. One Bonus Action creates one next-attack entitlement through next owner regular start, consumed even on miss or advantage cancellation, without another attack or recipient identity.',
'Independent disadvantage cancels the roll benefit but still consumes the first-attack entitlement. Repeated family applications retain only the appropriate later expiry, not a queue of future advantaged attacks.'],
'GC-17':[
'Ignoring Loading allows both otherwise-legal Extra Attack shots with two bolts and actual hands. Ammunition, two-handed firing, free-hand loading and distinct available attacks still apply.',
'Repeating5 is an actual magazine and reload rule, not the Loading cap. Empty stock requires the ordinary real reload Action and ammunition; no refill or waived action follows from Crossbow Expert.'],
'GC-18':[
'A native bludgeoning weapon hit can move a size-eligible target5ft horizontally to a legal destination after damage. No save or positive-damage threshold is invented; walls, occupied geometry and real falling at an edge still matter.',
'The critical attack-disadvantage branch is independent of the movement size limit. An oversized target can retain that rider through next owner regular start even though the5ft displacement is illegal.'],
'GC-19':[
'An available suspicious sound can support the actual advantaged active Perception task. The feature requires a real sensory trap/ambush cue and does not replace perception with automatic success.',
'No cue means no automatic discovery, passive plus5 or trap-save benefit. The current initiative increment is2; the historical4 remains evidence rather than an extra operative bonus.'],
'GC-20':[
'The broad actual ranged-attack predicate includes ranged spell attacks. Declare minus1 before the roll, then add flat2 to one native damage component on a hit; a save-only or nondamaging effect gets no invented damage.',
'A critical doubles eligible dice but leaves the feat flat2 unchanged. It is not added per die, per native component or to an independent copied/periodic effect.'],
'GC-21':[
'The current self-recipient case is allowed: spend the holder own Reaction before the attack roll for a real perceived intervention. The feat adds no shield, free-hand, can-see or second-body requirement, and does not permit a post-roll reroll.',
'A second constituent attack is a distinct event, so a separately available legal Reaction may defend against it. The first expenditure grants no blanket Multiattack protection or additional token.'],
'GC-22':[
'A legal dagger implement usingDEX3 andPB3 givesDC8+3+3=14, and the target chooses its actualSTR orDEX save. This replaces an Attack Action attack without an attack roll, damage, hit or critical event.',
'An eligible held wand can fall into a legal adjacent space, or the target space if necessary. It is not transferred into custody; implanted claws, worn armor, strapped shields and real nondroppable bonds are not removable held objects by this procedure.'],
'GC-23':[
'Two usable one-hand longswords are permitted despite not being Light. Each uses its one-hand1d8 profile, not the Versatile two-hand1d10; actual hands and ordinary two-weapon action rules remain.',
'Losing one usable wielded weapon immediately removes plus1AC. Holding an unusable Two-Handed greatsword in one hand does not satisfy the pair, and the feat does not restore the omitted positive damage modifier by itself.'],
'GC-24':[
'Actual Elf/half-Elf source qualification and an advantaged eligible-ability attack are premises. Replace the selected4 with mandatory9, then keep max(9,12)=12; this is one replacement, not free choice among all three faces.',
'Any surviving disadvantage cancels advantage before admission. One ordinary d20 therefore supplies no Elven Accuracy trigger; it cannot reroll a later Lucky-added die or STR/CON attack under this feature.'],
'GC-25':[
'After actual hearing and language comprehension, failure against the paidDC14 Action/SR use denies the next future regular-turn Action only. Movement, legal Bonus Action and Reaction remain, while an extra Action cannot bypass the denial; no Stunned/Charmed condition is inferred.',
'An incomprehending creature is ineligible, and the shared source-character/target/encounter hard-denial record blocks a repeated denial. Source identity, real capability and actual encounter boundaries cannot be replaced by a new callback or wording.'],
'GC-26':[
'A seen voluntary outside-to-inside crossing from10 to5 enters the rapier ordinary reach. Resolve the paid opportunity attack after entry and before further movement; actual Finesse melee wielding and remaining capability are required.',
'Forced entry, teleport, initial appearance, owner motion, growing reach or already-inside movement are not the voluntary crossing trigger. Disengage still prevents eligible opportunity attacks, and Lunge does not enlarge a persistent entry boundary.'],
'GC-27':[
'The feat grants actual Simple/Martial proficiency and allows one Bonus Action physical attack after a real personal weapon, natural or unarmed attack that turn. The initial unarmed attack need not be an Attack Action, but the follow-up needs its real weapon, hands and action wallet.',
'A save-only fireball-like effect is neither a physical attack trigger nor a spell the follow-up can cast. The feat does not grant Fighter class features, Extra Attack or exemption from derived-attack causal limits.'],
'GC-28':[
'Fleet adds10 only to walking, giving40 from30 while independentFly30 stays30. Hard Speed0 and movement already spent remain unchanged by this capacity increase.',
'A climb mode expressly derived from walking follows40 once. It does not receive an additional independent10 to become50, and an independent climbing mode would not inherit an unwritten parent.'],
'GC-29':[
'An actual two-handed quarterstaff critical against a meaningful hostile can fund one same-turn Bonus Action two-hand melee attack. Heavy is not required, but actual two-hand use, reach, wallet and causal source are.',
'A one-handed sword critical fails the two-hand predicate. Critical plus drop on one event still produces one entitlement, and a derived follow-up cannot recursively create another grant or bank an off-turn Bonus Action.'],
'GC-30':[
'The actual16-hour mixed trail takes default15+5 for being beyond12 hours+5 mixed=25, absent a source-specific DC. Successful real observation yields only the next local trail direction, not teleport tracking or a live position beacon.',
'Against an actual Beast/Monstrosity the owner direct native event adds one flat2, including on a critical. Companion-owned, periodic or copied events do not silently inherit the owner Hunter bonus.'],
'GC-31':[
'The exact prerequisite is Alertness ownership. Alert alone is a different feat and cannot satisfy it through name similarity, initiative strength or a generic alert Boolean.',
'The real invisible body within5ft can be located through legal line of effect, but this10ft location operation is not effective sight. Consciousness and actual source conditions remain; can-see needs another qualifying sense.'],
'GC-32':[
'The critical fixes actual allies within30ft who see or hear at that moment, including the owner when eligible. The plus1 is to attack through next owner regular start; no later entrant, continuing tether or legacy damage bonus is added.',
'Two owners retain independent deadline records for one plus1 family. The earlier expiry cannot delete the later active record, but simultaneous records never sum to plus2.'],
'GC-33':[
'Opposed Intimidation18 beats Insight14, imposing one next-attack disadvantage through the owner deadline. Declaration consumes it even on miss or cancellation; no ordinary task degree shift, Frightened or Action denial is inferred.',
'Opaque total cover with no audible or visible credible threat fails the communication predicate. Acquisition proficiency is not expertise, and qualifying STR intimidation needs an independent actual permission rather than the feat name.'],
'GC-34':[
'With original disadvantage3/17 and added12, choosing to replace3 yields min(12,17)=12. The holder may retain originals instead, but cannot turn the original disadvantage selection into highest of three; one point applies to one underlying event.',
'Lucky can replace an actual own death-save die before consequences. It cannot retroactively reverse resolved failure/death or modify an automatic no-roll outcome; actual remaining LR points and the die-position rule still apply.'],
'GC-35':[
'The perceived nearby casting completes or is negated before the Reaction attack. A self-buff caster remaining within legal melee reach can be attacked using the actual Reaction; this does not interrupt or erase the spell.',
'A completed teleport to30ft requires a fresh reach/perception/capability check, which fails this ordinary melee attack. No attack can be delivered at the old location or used to retroactively cancel teleport.'],
'GC-36':[
'The permanent Mage curriculum takes two distinct actual Mage rank0 rows and one actual Mage rank1 row, usingINT. It grants the feat route and one rank1 LR charge, not Mage class levels, RP pool or whole repertoire; payload readiness and independent costs remain.',
'NamedWizard and genericWizard share one curriculum entitlement rather than duplicate charges. A separately lawful genericCleric choice is distinct and uses its ownWIS curriculum; generic selection is nonrepeatable and does not waive an earned feat opportunity.'],
'GC-37':[
'Measured Strike and Guarding Deflection are two choices from the finite six feat maneuvers. Either consumes the sole sharedd6, with its own timing and Action/Reaction requirements; until a legal rest the other has no die.',
'Soldier resources and Coordinated Maneuver are separate class sources. The feat neither converts their resources into superiority dice nor grants their procedures through a similarly named maneuver.'],
'GC-38':[
'Advanced requires the actual parent and adds two different choices to the original two, for four of the six. It increases the same pool capacity to2d6; acquisition creates the new die once, and legal rest restores the one capacity.',
'Only one maneuver die may fund the same event. Two owned feats do not make independently recharging pools or allow two dice on one Measured Strike; later refills cannot exceed the shared capacity.'],
'GC-39':[
'A real personal attack, including a missed thrown dagger, records that actual target for this turn movement immunity from that target opportunity attacks. It does not require a hit or suppress another enemy opportunity attack.',
'Save-only areas create no attacked-target receipt. Difficult terrain still charges its actual cost, hard Speed0 remains and no Dash terrain immunity is imported.'],
'GC-40':[
'The real Large mount is larger than the actual unmountedMedium target, so eligible melee attacks gain advantage. The comparison uses mount size, with actual riding and shared EX58 phase/body limits.',
'Large is not smaller than Large, so this feat contributes no advantage. Independently owned Cavalry can apply its broader predicate, but multiple advantage causes still use the ordinary two-die system.'],
'GC-41':[
'The conscious owner is an eligible ally at distance0 if hearing their audible direction. The plus1 applies only to an actual fear/morale save; Silence or Deafened can defeat hearing and no extra roll is created.',
'Voluntary retreat remains a choice. The aura does not force a morale check, manufacture loyalty, suppress movement or replace an ally decision with a saving throw.'],
'GC-42':[
'Acquisition with existing underlying60ft darkvision fixes extension mode; the operative strongest underlying60 plus30 becomes90. It is not a second base vision or a repeatable acquisition choice.',
'When no underlying darkvision is operative, extension mode provides0 rather than30. Returning restores the original extension once; transformation and toggling do not stack another30 or change the recorded acquisition mode.'],
'GC-43':[
'The actual Simple/Martial2d6 weapon adds one base die1d6 for3d6 on this SR declaration after hit and before damage. The entire2d6 expression is not the additional die; real Orc/half-Orc qualification is required.',
'An actual critical doubles the three eligible weapon dice to6d6. The ordinarySTR modifier remains one flat contribution; no extra use, damage roll or attack is granted.'],
'GC-44':[
'The native rapier critical first doubles1d8 to2d8, then the feat adds one separate base die for3d8. That explicitly additional critical die is not doubled a second time to4d8.',
'The selected eligible piercing weapon-pool die must keep its new face, even1 again. The spent actual-turn allowance cannot be recovered by a bad roll or reselecting an abandoned Savage Attacker pool; independent riders are outside this reroll.'],
'GC-45':[
'An actual seen voluntary crossing into the pike ordinary10ft reach can trigger a paid opportunity attack after entry. Only the finite listed weapon types and real usable wielding qualify; no new attack wallet is granted.',
'A quarterstaff retains its actual5ft ordinary reach. Forced movement into it triggers no entry attack, and the feat adds neither a butt-end Bonus Action nor a persistent Lunge reach extension.'],
'GC-46':[
'Choose the entire native weapon pool: original2+6=8 or new5+1=6. Selecting faces across pools to obtain11 is illegal; the special explicit own/off regular-turn allowances remain distinct from generic actual-turn language.',
'The independent poison rider retains its original roll. Only the actual native weapon dice pool, including eligible explicit weapon additions/critical copies, is replaced; flats, external riders and maximized nonrolled pools do not acquire this reroll.'],
'GC-47':[
'An actual opportunity-attack hit, even if damage is0, sets all Speeds to0 until the enclosing actual turn end. It blocks subsequent ordinary movement while retaining spent-cost history; a replacement spell or Mage Slayer Reaction is not an opportunity hit.',
'An independently legal teleport or forced displacement is not ordinary Speed spending. Speed0 alone does not forbid it; actual source restrictions, geometry and falling support are still required.'],
'GC-48':[
'An actual ranged-class longbow attack within its printed maximum removes long-range disadvantage and half/three-quarters cover comparison terms. This does not add range, a damage trade or the same benefit to thrown melee weapons or spells.',
'Total cover can still make the target illegal, while an adjacent seeing non-Incapacitated hostile can still supply proximity disadvantage. Ignoring a cover term does not remove an independent barrier blocking targeting or damage.'],
'GC-49':[
'The legal usable shield can fund an ordinary Bonus Action shove before attacking. Actual5ft reach, size and STR Athletics contest apply; success selects5ft push or Prone, not both, without an added free-hand requirement beyond shield contact.',
'Shield proficiency is not an added feat activation gate. A nonproficient user still suffers the actual shield penalty on theSTR contest; the feat neither grants proficiency nor evasion, damage or a successful contest.'],
'GC-50':[
'Light foliage can permit a real Hide attempt, and an already-Hidden ranged-class weapon miss need not disclose position through that shot alone. This is not automatic Hidden, silence against all observers or a benefit for spells/thrown melee weapons.',
'Entering a clearly visible lit doorway is an independent disclosure event and ends Hidden normally. The earlier miss receipt cannot protect later movement, actual Search results or other revealing actions.'],
'GC-51':[
'The current shared strongest-slow rule makes one minus10 fromSpeed30 equal20. Duplicate Slasher and a different Crippling minus10 retain their own expiries but do not subtract again; the historical additive examples remain preserved as superseded.',
'Independent half-Speed compares15 from the same pre-control30 against the minus10 result20, selecting15. It is not subtract-then-half10 or stacked5; a separate hard Speed0 restriction wins.'],
'GC-52':[
'CR1/2 gives10+ceil(1/2)=11. NormalHP10 of effective max20 is Positive-at-or-below-half, excluding tempHP and exact-value disclosure; the chosen fact must be selected before the actual task.',
'Failure spends the per-owner/actual-target allowance until completed beneficialLR. Disguise, form change or new presentation does not create another target identity; missing facts stay Indeterminate rather than invented stats or protection diagnostics.'],
'GC-53':[
'A genuine own unarmed hit can permit a same-target Bonus Action ordinary grapple if reach, size, free hand and capability still hold. The feat grants proficiency, not an upgraded unarmed base or a guaranteed grapple.',
'A chair hit can use actual improvised proficiency and its legitimate profile but is not an unarmed hit. It therefore does not supply this grapple trigger; separately acquired Brawler has its own broader Bonus Action permission.'],
'GC-54':[
'The NEW partial attack allowance isfloor(4PB/5):PB3 gives2 added to the actual ability. It neither changes damage to80percent nor creates a true weapon proficiency credential or stacked partial bonus.',
'AtPB2 the allowance is1. Weapon Focus still requires actual proficiency, so a numerically useful partial allowance cannot satisfy its acquisition predicate.'],
'GC-55':[
'Focus on the exact proficient dagger type adds1 on its legal melee or Thrown attack. It does not cover every piercing weapon, all weapons in a group or a generic unarmed profile.',
'Distinct paid selections may cover rapier and longbow. Repeating the same type cannot create plus2, and loss of operative proficiency suppresses its benefit without deleting the historical acquisition.'],
'GC-56':[
'Four distinct actual catalog weapon types grant their source proficiency, and the compositeDEX increment caps19 at20. No physical weapon, inventory stock, hand or ability to ignore a Special use restriction is created.',
'Already-owned proficiency does not become expertise or an automatic replacement choice. AtSTR20 this composite half-increase contributes0 while lawful training still applies; it does not lower the score or erase the other grants.'],
'GC-57':[
'At level10 one paid shared owner command can reach two eligible hearing actual companions within60ft. Both may perform independently legal Help, but Attack designates only one shared offensive action; no second independent turn, Reaction or banked attack is created.',
'A real commanded Beast meaningful-hostile positive-to-zero transition can mark the owner next eligible attack within30ft through next future owner end. The eventual roll consumes advantage even on miss/cancellation; a farther attack is ineligible and does not consume it, and no attack is granted.'],
'GC-58':[
'Actual moonlight or a real transformed body gates the paid own-regular-turn howl. Fix heard eligible allies within30ft, including the holder if able to hear, and the actual tracked/personally-damaged target; first eligible attack consumes each receipt without revealing location or granting an attack.',
'A moon-painted lantern is not actual moonlight, and the feat grants no transformation source. A real old trail can satisfy its own tracking predicate without revealing the present target square, creating a new sensory cue or inventing cosmology.']}
ck('58 individually authored pairs',set(notes)=={r['questionId'] for r in selected} and all(len(v)==2 and all(v) for v in notes.values()))
proposal=j(R/'data/director/general_combat_feat_operating_proposal_internal.json'); reviews=[]
for x in cases:
 idx=int(x['sourcePointer'].rsplit('/',1)[1]); value=proposal
 for part in x['sourcePointer'].split('/')[1:]: value=value[int(part)] if isinstance(value,list) else value[part]
 ck(x['id']+' full original retained',value==x['original'])
 ck(x['id']+' full current outcome retained',x['completeExpectedOutcome']==records[x['featId']]['workedCases'][idx])
 reviews.append({'id':x['id'],'featId':x['featId'],'completeOriginalDisposition':deepcopy(x),'reviewResult':'CONSISTENT_WITH_CURRENT_AUTHORING_AND_EXPLICIT_CONDITIONS','reasoning':notes[x['questionId']][idx],'qualification':'Stated-case semantic review. Actual acquisition, actors, senses, geometry, finite resources, custody, route and source provenance remain premises; these examples do not authenticate campaign events.','runtimeExecuted':False,'canonicalApplied':False})
bn={'FA-05':'Slasher and Crippling each evaluate minus10 from the same pre-control30; the result is20. A separately operative half-Speed yields15 and a hard Speed0 yields0. Duplicate or different slow names do not make additive reductions.', 'FA-11':'Cavalry changes actual walking40 to50 and supplies no absent mode. Mounted EX58 uses the same elected shared phase and spent-cost history; dismount pays its actual cost and requires legal body geometry rather than restarting a fresh movement budget.', 'FA-12':'The level10 two-recipient hearing command still pays one shared owner Bonus Action. Two individually legal Help operations are nonoffensive; one Attack command designates only one offensive companion, leaving the other defensive movement/Dodge rather than an extra banked attack.'}
boundary_reviews=[{'id':x['id'],'featId':x['featId'],'completeOriginalDisposition':deepcopy(x),'reviewResult':'CONSISTENT_WITH_CURRENT_AUTHORING_AND_EXPLICIT_CONDITIONS','reasoning':bn[x['id']],'runtimeExecuted':False,'canonicalApplied':False} for x in boundaries]
public={r['id']:r for r in j(R/'data/public/feat_candidates/exact_01/candidate.json')['feats']}; derived={r['id']:r for r in j(D/'data/director/feat_candidates/exact_01/candidate.json')['records']}; dp={r['id']:r for r in j(D/'data/public/feat_candidates/exact_01/candidate.json')['feats']}
chapter=(R/'docs/feats/exact-candidate-01/GENERAL_COMBAT.md').read_text(encoding='utf-8-sig')
for r in selected:
 ck(r['id']+' whole derived record unchanged',r==derived[r['id']])
 ck(r['id']+' public rules and examples exact',all(r[k]==p[r['id']][k] for p in [public,dp] for k in ['operationalRules','workedCases']))
 ck(r['id']+' whole chapter rules and cases',r['operationalRules'] in chapter and all(x in chapter for x in r['workedCases']))
changed=[x['id'] for x in cases if x['original']!=x['completeExpectedOutcome']]
ck('seven prior expectation replacements retained',changed==['GC-16-E01','GC-21-E01','GC-32-E01','GC-41-E01','GC-51-E01','GC-51-E02','GC-58-E01'])
calcs=[]
def C(n,refs,inputs,actual,expected,scope):
 cid='GC99-N'+str(n).zfill(2); ck(cid+' expected result',actual==expected); calcs.append({'id':cid,'originalCaseIds':refs,'inputs':inputs,'calculatedResult':actual,'expectedResult':expected,'scope':scope,'runtimeExecuted':False})
def adv(a,d): return 0 if a and d else 1 if a else -1 if d else 0
C(1,['GC-01-E02','GC-02-E01','GC-02-E02'],{'initiativeBeforeFeats':10,'Alert':5,'Alertness':2,'WIS':2,'PerceptionPB':3},{'initiativeWithBoth':10+5+2,'passiveWithAlertness':10+2+3+2},{'initiativeWithBoth':17,'passiveWithAlertness':17},'Actual new initiative and actual passive perception; no second proficiency or retrospective turn.')
C(2,['GC-01-E01'],{'advantageCauses':[['Hidden'],['Hidden','independentUnseen']],'AlertRemovesOnlyHidden':True},[adv([x for x in cs if x!='Hidden'],[]) for cs in [['Hidden'],['Hidden','independentUnseen']]],[0,1],'Partial roll-cause projection; no location, vision or world target authentication.')
C(3,['GC-03-E01','GC-03-E02'],{'ordinaryLegalTwoWeaponDamageDie':4,'actualAbility':3,'pairLightFlags':[[True,True],[False,False]],'DualWielderOwned':False},{'ordinaryFeatDamage':4+3,'pairPermission':[all(flags) for flags in [[True,True],[False,False]]]},{'ordinaryFeatDamage':7,'pairPermission':[True,False]},'Light check is only one prerequisite; real hands, Attack Action, usable one-hand melee weapons and Bonus Action remain required.')
def hp_convert(old_hp,old_max,new_max):
 assert 0<old_hp<=old_max and old_max>0 and new_max>0
 return max(1,new_max*old_hp//old_max)
C(4,['GC-04-E01'],{'ownerLevel':5,'ownerPB':3,'ordinaryAnimalHP':4,'ordinaryAnimalMaximum':8},{'newMaximum':5+5,'convertedHP':hp_convert(4,8,5+5),'AC':12+3//2},{'newMaximum':10,'convertedHP':5,'AC':13},'Actual eligible living body with required full acquisition/bond transaction. This does not create the animal, heal injuries or grant unstated attacks.')
C(5,['GC-04-E01','GC-04-E02'],{'ordinaryHPMaximumPairs':[[1,20],[19,20],[20,20]],'bondedMaximum':10,'laterOwnerLevel':6},{'initialConversions':[hp_convert(h,m,10) for h,m in [(1,20),(19,20),(20,20)]],'laterMaximum':5+6,'HPAfterMaximumGrowthFrom5':5},{'initialConversions':[1,9,10],'laterMaximum':11,'HPAfterMaximumGrowthFrom5':5},'Positive admission minimum1 and floor ratio; later maximum growth does not heal. Zero/dead body is not an input to positiveHP conversion.')
C(6,['GC-05-E01','GC-05-E02'],{'baselineAC':16,'attackKinds':['polearmEntryOpportunity','mageSlayerReaction','ordinaryFlankingAttack'],'separatelyLawfulTacticalFlankerD6':1},{'comparisonACs':[16+int(k=='polearmEntryOpportunity') for k in ['polearmEntryOpportunity','mageSlayerReaction','ordinaryFlankingAttack']],'remainingFlankerD6':1},{'comparisonACs':[17,16,16],'remainingFlankerD6':1},'Actual attack classifications supplied; no universal flanking rule or suppression of independent damage dice.')
C(7,['GC-06-E01','GC-06-E02'],{'separateBudget':5,'tileFeet':5,'terrainCostFactors':[1,2]},[5*f<=5 for f in [1,2]],[True,False],'Legal complete grid-tile fixture only; nonzero Speed and actual post-hit timing required.')
C(8,['GC-07-E01','GC-07-E02','GC-08-E01','GC-08-E02','GC-31-E02'],{'distances':[5,20,35],'BlindFightRange':30,'BlindFightingRange':10,'openLine':True},{'located':[d<=30 for d in [5,20,35]],'effectiveSeen':[d<=10 for d in [5,20,35]],'closedWallAt10Located':False},{'located':[True,True,False],'effectiveSeen':[True,False,False],'closedWallAt10Located':False},'Bounded range and stipulated line predicates; no visual rendering, arbitrary obstruction or hidden identity simulation.')
C(9,['GC-09-E01','GC-09-E02'],{'unarmedD4Face':3,'STR':2,'freeGraspingHands':[1,0]},{'damage':max(0,3+2),'handGate':[h>0 for h in [1,0]]},{'damage':5,'handGate':[True,False]},'Brawler damage base and free-hand gate only; actual grapple size, reach and contest remain required.')
C(10,['GC-10-E01','GC-10-E02','FA-11'],{'actualIndependentMountSpeeds':{'walk':40},'CavalryHolders':2,'preexistingDisadvantage':[False,True]},{'operativeSpeeds':{k:s+10 for k,s in {'walk':40}.items()},'rollStates':[adv(True,d) for d in [False,True]]},{'operativeSpeeds':{'walk':50},'rollStates':[1,0]},'One family increase and no invented fly key. Actual mounted attacking and an unmounted target are stipulated, not new world actors.')
C(11,['GC-11-E01','GC-11-E02'],{'initialActions':1,'initialBonusActions':1,'dashCosts':['Action','BonusAction']},[{'triggerEligible':kind=='Action','actionAfterDash':1-int(kind=='Action'),'bonusActionAfterDash':1-int(kind=='BonusAction'),'canFundChargerBA':kind=='Action' and (1-int(kind=='BonusAction'))>0} for kind in ['Action','BonusAction']],[{'triggerEligible':True,'actionAfterDash':0,'bonusActionAfterDash':1,'canFundChargerBA':True},{'triggerEligible':False,'actionAfterDash':1,'bonusActionAfterDash':0,'canFundChargerBA':False}],'Assumes each Dash independently legal; a legal Charger follow-up then consumes the one remaining Bonus Action.')
claims=set(); chain=[]
for event,parent_derived in [('originalDrop',False),('cleaveDrop',True),('replayedOriginalDrop',False)]:
 allowed=not parent_derived and 'owner-regular-7' not in claims
 if allowed: claims.add('owner-regular-7')
 chain.append({'event':event,'grant':allowed,'claimsUsed':len(claims)})
C(12,['GC-12-E01','GC-12-E02','GC-29-E02'],{'ownRegularInterval':7,'qualifiedOriginalDrop':True,'rootIdentity':'originalAttack','events':['originalDrop','derivedDrop','replayedOriginalDrop']},chain,[{'event':'originalDrop','grant':True,'claimsUsed':1},{'event':'cleaveDrop','grant':False,'claimsUsed':1},{'event':'replayedOriginalDrop','grant':False,'claimsUsed':1}],'Finite-claim and descendant exclusion projection; real target, damage floors, meaningful-hostile and one-grant choice still required.')
C(13,['GC-13-E01','GC-13-E02'],{'spellShapes':[{'castTime':'Action','targetForm':'oneCreature'},{'castTime':'Action','targetForm':'areaWithOneOccupant'},{'castTime':'Action','targetForm':'Self'},{'castTime':'oneMinute','targetForm':'oneCreature'}]},[time=='Action' and shape=='oneCreature' for time,shape in [('Action','oneCreature'),('Action','areaWithOneOccupant'),('Action','Self'),('oneMinute','oneCreature')]],[True,False,False,False],'Partial cast-shape admission only. Does not create a spell, actual access, paid route, components, Reaction or line legality.')
C(14,['GC-14-E01','GC-14-E02'],{'attackModifier':6,'AC':16,'firstAttackAlreadyUnpenalized':[False,True]},{'activeAttackModifier':6-1,'activeAC':16+1,'activationAllowed':[not x for x in [False,True]]},{'activeAttackModifier':5,'activeAC':17,'activationAllowed':[True,False]},'Commit a legal first attack to activate; miss still leaves fixed interval cost and defense.')
ordinary=1; extra=1; used_events=set(); reactions=[]
for kind,event,choice in [('spend','beforeOwn','ordinary'),('ownRegularStart',None,None),('spend','departureA','ordinary'),('spend','departureA','extra'),('spend','departureB','extra'),('extraTurnStart',None,None)]:
 allowed=None
 if kind=='ownRegularStart': ordinary=1
 elif kind=='spend':
  wallet=ordinary if choice=='ordinary' else extra; allowed=wallet>0 and event not in used_events
  if allowed:
   used_events.add(event)
   if choice=='ordinary': ordinary-=1
   else: extra-=1
 reactions.append({'kind':kind,'event':event,'allowed':allowed,'ordinary':ordinary,'extra':extra})
C(15,['GC-15-E01','GC-15-E02'],{'entryOrdinary':1,'entryRoundExtra':1,'oneNumberedRound':True,'allLegalDistinctTriggersExceptReusedA':True},reactions,[{'kind':'spend','event':'beforeOwn','allowed':True,'ordinary':0,'extra':1},{'kind':'ownRegularStart','event':None,'allowed':None,'ordinary':1,'extra':1},{'kind':'spend','event':'departureA','allowed':True,'ordinary':0,'extra':1},{'kind':'spend','event':'departureA','allowed':False,'ordinary':0,'extra':1},{'kind':'spend','event':'departureB','allowed':True,'ordinary':0,'extra':0},{'kind':'extraTurnStart','event':None,'allowed':None,'ordinary':0,'extra':0}],'One owner ordinary refill and distinct-event extra token in a fixed numbered round. No leave/reenter or extra-turn reset, actual capability otherwise stipulated.')
C(16,['GC-16-E01','GC-16-E02'],{'oneCoordinationReceipt':True,'firstAttackHasDisadvantage':True,'firstAttackMisses':True},{'firstRollState':adv(True,True),'receiptAfterDeclaration':False,'secondAttackFeatAdvantage':False},{'firstRollState':0,'receiptAfterDeclaration':False,'secondAttackFeatAdvantage':False},'Self recipient and actual perceived coordination stipulated; cancellation and miss do not preserve next-attack receipt.')
C(17,['GC-17-E01','GC-17-E02'],{'legalExtraAttackShots':2,'boltsBefore':5,'emptyRepeatingMagazine':0,'reloadActionCost':1},{'boltsAfterTwoShots':5-2,'emptyMagazineShotsBeforeReload':min(2,0),'realReloadActionCost':1},{'boltsAfterTwoShots':3,'emptyMagazineShotsBeforeReload':0,'realReloadActionCost':1},'Hands, actual ordinary weapon loading and shot cadence otherwise legal. Ignoring Loading does not generate ammunition or bypass Repeating.')
C(18,['GC-18-E01','GC-18-E02'],{'ownerSizeOrdinal':2,'targetSizeOrdinals':[2,4],'criticalHit':True},{'pushSizeEligible':[s<=2+1 for s in [2,4]],'criticalDisadvantageEligible':[True,True],'ordinaryPushFeet':5},{'pushSizeEligible':[True,False],'criticalDisadvantageEligible':[True,True],'ordinaryPushFeet':5},'Synthetic ordered real size categories with a native bludgeoning weapon hit. Actual destinations and post-damage state still checked; size restricts push only.')
C(19,['GC-19-E01','GC-19-E02'],{'actualPerceptionFaces':[4,15],'PerceptionModifier':3,'initiativeBefore':10},{'qualifiedActivePerceptionTotal':max(4,15)+3,'initiativeAfter':10+2},{'qualifiedActivePerceptionTotal':18,'initiativeAfter':12},'The real sensory cue is an explicit premise. No passive bonus, automatic detection or save advantage is computed.')
C(20,['GC-20-E01','GC-20-E02'],{'rangedSpellAttackModifier':6,'ordinaryNativeD6Faces':[4],'criticalNativeD6Faces':[4,3]},{'attackModifier':6-1,'ordinaryDamage':sum([4])+2,'criticalDamage':sum([4,3])+2},{'attackModifier':5,'ordinaryDamage':6,'criticalDamage':9},'Actual declared eligible ranged attack; flat2 applies once before defenses, not critical doubled.')
C(21,['GC-21-E01','GC-21-E02'],{'ordinaryReaction':1,'incomingSeparateAttackEvents':['A','B'],'noExtraToken':True},[adv(False,i==0) for i in range(2)],[-1,0],'A paid before-roll intervention for A exhausts the only Reaction. B is a separate event without an available wallet in this fixture.')
C(22,['GC-22-E01','GC-22-E02'],{'PB':3,'actualAttackAbility':3,'targetSaveTotals':[13,14]},{'DC':8+3+3,'failed':[s<8+3+3 for s in [13,14]],'damage':0},{'DC':14,'failed':[True,False],'damage':0},'Actual reachable held removable object and Attack Action replacement stipulated; failure drops rather than transfers or damages it.')
C(23,['GC-23-E01','GC-23-E02'],{'baselineAC':16,'usableWieldedOneHandMeleeCounts':[2,1],'longswordOneHandDieSides':8},{'ACs':[16+int(n==2) for n in [2,1]],'pairedDieSides':[8,8]},{'ACs':[17,16],'pairedDieSides':[8,8]},'Actual two usable weapons in actual hands; no two-hand Versatile damage or authorization of one-handed greatsword.')
C(24,['GC-24-E01','GC-24-E02'],{'initialAdvantageFaces':[4,12],'selectedReplacementIndex':0,'newFace':9,'independentDisadvantage':[False,True]},{'replacementPair':[9,12],'keptFace':max(9,12),'EAAdmission':[adv(True,d)==1 for d in [False,True]]},{'replacementPair':[9,12],'keptFace':12,'EAAdmission':[True,False]},'Actual eligible ancestry and attack ability are stipulated; replacement face mandatory, initial advantage required before the reroll.')
C(25,['GC-25-E01','GC-25-E02'],{'PB':3,'CHA':3,'saveTotal':12,'futureTargetBudgetsBefore':{'Action':1,'BonusAction':1,'movementCostCapacity':30,'Reaction':1}},{'DC':8+3+3,'saveFails':12<8+3+3,'futureBudgets':{'Action':0,'BonusAction':1,'movementCostCapacity':30,'Reaction':1}},{'DC':14,'saveFails':True,'futureBudgets':{'Action':0,'BonusAction':1,'movementCostCapacity':30,'Reaction':1}},'Legal paid Action/SR language operation with no prior hard-denial record; denies Action for the specified future regular turn, not a Stunned condition.')
def entry(start,end,reach,voluntary): return voluntary and start>reach and end<=reach
C(26,['GC-26-E01','GC-26-E02','GC-45-E01','GC-45-E02'],{'crossings':[{'start':10,'end':5,'reach':5,'voluntary':True},{'start':10,'end':5,'reach':5,'voluntary':False},{'start':15,'end':10,'reach':10,'voluntary':True},{'start':15,'end':10,'reach':5,'voluntary':True}]},[entry(*x) for x in [(10,5,5,True),(10,5,5,False),(15,10,10,True),(15,10,5,True)]],[True,False,True,False],'Distance projection of real voluntary boundary crossing, assuming seen hostile, legal weapon, real body path and no Disengage. It is not full3D collision or an added reach grant.')
C(27,['GC-27-E01','GC-27-E02'],{'priorOperations':['unarmedAttack','saveOnlySpell'],'BAWallet':1},[op=='unarmedAttack' for op in ['unarmedAttack','saveOnlySpell']],[True,False],'Partial source-kind gate for the actual finite physical Bonus Action attack; grants no spell or recursive source event.')
C(28,['GC-28-E01','GC-28-E02'],{'walk':30,'independentFly':30,'climbDerivedFrom':'walk'},{'walk':30+10,'fly':30,'climb':30+10},{'walk':40,'fly':30,'climb':40},'Derived parent evaluated once; no refund of previously spent movement or change to independent fly.')
C(29,['GC-29-E01','GC-29-E02'],{'criticalAttacks':[{'actualHands':2,'alsoDrop':False},{'actualHands':1,'alsoDrop':False},{'actualHands':2,'alsoDrop':True}],'BAWallet':1},[min(1,1) if h==2 else 0 for h in [2,1,2]],[1,0,1],'Meaningful hostile, ordinary own-turn source and legal two-hand follow-up assumed. Critical plus drop shares one event entitlement, not two Bonus Actions.')
C(30,['GC-30-E01','GC-30-E02'],{'realTrailAgeHours':16,'mixedTracks':True,'defaultBaseDC':15,'nativeCriticalDamage':12},{'trailDC':15+5+5,'ownerBeforeDefenseDamage':12+2,'companionHunterBonus':0},{'trailDC':25,'ownerBeforeDefenseDamage':14,'companionHunterBonus':0},'No source-specific trail DC in this fixture. Finite local tracking result and actual Beast/Monstrosity direct-owner event remain source conditions.')
C(31,['GC-31-E01'],{'ownedFeatSets':[['alert'],['alertness']]},['alertness' in owned for owned in [['alert'],['alertness']]],[False,True],'Exact prerequisite identity only; all other acquisition gates, costs and earned choices remain required.')
C(32,['GC-32-E01','GC-32-E02'],{'fixedRecipientIds':['owner','allyA'],'laterEntrant':'allyB','independentOwnerExpirySeconds':[6,12],'querySeconds':[5,6,11,12]},{'familyBonuses':[int(any(t<end for end in [6,12])) for t in [5,6,11,12]],'laterEntrantInFixedSet':'allyB' in ['owner','allyA']},{'familyBonuses':[1,1,1,0],'laterEntrantInFixedSet':False},'Real critical and initial sensory/range predicates stipulated. End-exclusive separate expiry records; no plus2 or retroactive recipient membership.')
C(33,['GC-33-E01','GC-33-E02'],{'opposedCHAIntimidation':18,'opposedWISInsight':14,'audibleOrVisibleThreat':[True,False]},{'contestSuccess':18>14,'admittedThreat':[x for x in [True,False]],'firstEligibleAttackState':adv(False,True)},{'contestSuccess':True,'admittedThreat':[True,False],'firstEligibleAttackState':-1},'Actual communication and once-target-interval opportunity required; ordinary contest has no task shifts and creates no Frightened or hard-denial condition.')
C(34,['GC-34-E01','GC-34-E02'],{'disadvantageFaces':[3,17],'LuckyFace':12,'pointsBefore':3,'unresolvedDeathSaveOriginal':1,'deathSaveChosenReplacement':12},{'disadvantageKept':min(12,17),'pointsAfterOneUse':3-1,'ordinaryDeathSaveChosenFace':12},{'disadvantageKept':12,'pointsAfterOneUse':2,'ordinaryDeathSaveChosenFace':12},'Two independent illustration branches, each before consequences. Lucky replacement preserves original die-selection mode; no post-death reversal or event double-spending.')
C(35,['GC-35-E01','GC-35-E02'],{'actualMeleeReach':5,'casterDistanceAfterResolution':[5,30]},[d<=5 for d in [5,30]],[True,False],'Post-spell distance gate only; actual perceived casting, available Reaction, legal physical attack and current capability still required.')
supplements=j(I/'supplements.json'); sup={x['id']:x for x in supplements['groups']}; curricula=sup['SUP-04']['completeAuthoringValue']; catalog=j(R/'data/public/spell_playtests/catalog.json'); spells={s['id']:s for s in catalog['spells']}
chosen_curriculum_rows=[]
for curriculum in ['Mage','Wizard','Cleric']:
 c=curricula[curriculum]; chosen=[next(x for x in c['choices'] if x['id']==name) for name in ['arcane-ward','dispel-minor','shield']]
 ck(curriculum+' full chosen access rows equal catalog',all(x['fullOriginalClassAccessRow']==spells[x['id']]['classAccess'][curriculum] for x in chosen))
 ck(curriculum+' two distinct rank0 and one rank1',len({x['id'] for x in chosen})==3 and [x['rank'] for x in chosen]==[0,0,1])
 ck(curriculum+' declared finite row counts',sum(x['rank']==0 for x in c['choices'])==c['rank0Choices'] and sum(x['rank']==1 for x in c['choices'])==c['rank1Choices'])
 chosen_curriculum_rows.append({'curriculum':curriculum,'featCastingAbility':c['featCastingAbility'],'chosenFullRows':chosen,'scope':'Illustrative lawful selection by existing row identity only; no cast, payload or class acquisition performed.'})
C(36,['GC-36-E01','GC-36-E02'],{'actualCurriculumAbilities':{k:curricula[k]['featCastingAbility'] for k in ['Mage','Wizard','Cleric']},'namedWizardAlreadyOwned':True,'candidateGenericSelections':['Wizard','Cleric']},{'abilities':[curricula[k]['featCastingAbility'] for k in ['Mage','Wizard','Cleric']],'newDistinctCurriculum':[k not in {'Wizard'} for k in ['Wizard','Cleric']]},{'abilities':['INT','INT','WIS'],'newDistinctCurriculum':[False,True]},'Generic choice must still be independently acquired. Duplicate curriculum cannot grant another charge; row-selection checks do not review every spell payload.')
C(37,['GC-37-E01','GC-37-E02'],{'featDiceBefore':1,'firstChosenManeuver':'Measured Strike','independentSoldierResources':3},{'featDiceAfterFirst':1-1,'secondManeuverCanPay':1-1>0,'SoldierResourcesUnchanged':3},{'featDiceAfterFirst':0,'secondManeuverCanPay':False,'SoldierResourcesUnchanged':3},'One actual legal maneuver event with its real timing; class resources cannot substitute for the spent feat die.')
C(38,['GC-38-E01','GC-38-E02'],{'originalDistinctChoices':2,'advancedNewDistinctChoices':2,'originalPoolCapacity':1,'addedCapacity':1,'requestedDiceOnOneEvent':[1,2]},{'knownChoices':2+2,'sharedCapacity':1+1,'oneEventDiceAdmitted':[n<=1 for n in [1,2]],'poolAfterLegalRest':2},{'knownChoices':4,'sharedCapacity':2,'oneEventDiceAdmitted':[True,False],'poolAfterLegalRest':2},'Choices drawn without duplication from actual six maneuver menu; a rest fills one capacity rather than adding a second separately restored pool.')
C(39,['GC-39-E01','GC-39-E02'],{'actualAttackedTarget':'A','attackMissed':True,'otherThreat':'B','saveOnlyTarget':'C','difficultFeet':5},{'OAImmunityByTarget':{t:t in {'A'} for t in ['A','B','C']},'difficultCost':5*2},{'OAImmunityByTarget':{'A':True,'B':False,'C':False},'difficultCost':10},'Current actual-turn identity and personal direct attack are stipulated. No universal Disengage, save-only attack receipt or terrain-cost waiver.')
C(40,['GC-40-E01','GC-40-E02'],{'actualMountSizeOrdinal':3,'unmountedTargetOrdinals':[2,3],'actualMeleeAttacks':True},[s<3 for s in [2,3]],[True,False],'Bounded ordered real size comparison; independently qualifying Cavalry is a separate source and advantage still cannot stack dice.')
C(41,['GC-41-E01','GC-41-E02'],{'baseActualFearSaveTotal':13,'consciousRecipients':[{'distance':0,'hearing':True},{'distance':8,'hearing':True},{'distance':8,'hearing':False},{'distance':11,'hearing':True}]},[13+int(d<=10 and hear) for d,hear in [(0,True),(8,True),(8,False),(11,True)]],[14,14,13,13],'Actual fear/morale save and audible conscious direction are required. Voluntary retreat without a save gets no fabricated roll.')
def darkvision(mode,underlying):
 base=max(underlying,default=0)
 return max(60,base) if mode=='grant' else base+30 if base>0 else 0
C(42,['GC-42-E01','GC-42-E02'],{'permanentlyRecordedMode':'extension','operativeUnderlyingLists':[[60],[],[60],[60,120]],'separateGrantModeLaterUnderlying':[120]},{'extensionRanges':[darkvision('extension',b) for b in [[60],[],[60],[60,120]]],'separateGrantModeRange':darkvision('grant',[120])},{'extensionRanges':[90,0,90,150],'separateGrantModeRange':120},'Mode is fixed at actual acquisition. Suppression/form toggling never earns another30; grant mode chooses strongest rather than adding60.')
C(43,['GC-43-E01','GC-43-E02'],{'nativeGreatswordD6':2,'addedBaseD6':1,'criticalMultiplier':2,'STR':3},{'ordinaryD6':2+1,'criticalD6':(2+1)*2,'flatSTR':3},{'ordinaryD6':3,'criticalD6':6,'flatSTR':3},'Actual paid SR use after hit before damage and actual racial/weapon qualifications stipulated; no whole-expression addition or flat doubling.')
C(44,['GC-44-E01','GC-44-E02'],{'rapierBaseD8':1,'criticalMultiplier':2,'postCriticalAddedD8':1,'oldSelectedFace':1,'replacementFace':1},{'criticalD8':1*2+1,'keptReplacement':1,'allowanceAfter':0},{'criticalD8':3,'keptReplacement':1,'allowanceAfter':0},'Actual native piercing weapon pool and one actual-turn reroll. Replacement is mandatory; the post-critical die is not doubled.')
C(45,['GC-46-E01','GC-46-E02'],{'nativeFirstPool':[2,6],'nativeSecondPool':[5,1],'separatePoisonPool':[4,2]},{'legalNativeTotals':[sum([2,6]),sum([5,1])],'illegalMixedMaximum':max(2,5)+max(6,1),'unchangedPoison':sum([4,2])},{'legalNativeTotals':[8,6],'illegalMixedMaximum':11,'unchangedPoison':6},'Whole-pool choice only. The computed illegal11 is an expressly rejected comparison, not an operative result or rider reroll.')
C(46,['GC-47-E01','GC-47-E02'],{'preHitSpeed':30,'spentOrdinaryCost':10,'enclosingTurnEndsAtSecond':6,'queries':[5,6],'independentTeleportOtherwiseLegal':True},{'speeds':[0 if t<6 else 30 for t in [5,6]],'ordinaryRemainingDuringRestriction':max(0,0-10),'teleportBlockedBySpeedAlone':False},{'speeds':[0,30],'ordinaryRemainingDuringRestriction':0,'teleportBlockedBySpeedAlone':False},'Actual opportunity hit before end marker; restores capacity without refunding spent cost. Other controls and teleport conditions remain external.')
C(47,['GC-48-E01','GC-48-E02'],{'baselineAC':16,'threeQuartersCover':5,'longRangeDisadvantage':True,'proximityDisadvantage':[False,True]},{'comparisonAC':16,'rollStates':[adv(False,d) for d in [False,True]],'totalCoverStillBlocks':True},{'comparisonAC':16,'rollStates':[0,-1],'totalCoverStillBlocks':True},'Legal actual ranged-class shot within printed maximum; removes cover term and long-range cause only, not targeting barriers or proximity.')
C(48,['GC-49-E01','GC-49-E02'],{'rawSTRContestFaces':[16,5],'STRPlusAthletics':5,'opponentTotal':14},{'proficientSingle16Total':16+5,'nonproficientDisadvantageTotal':min(16,5)+5,'successes':[16+5>14,min(16,5)+5>14]},{'proficientSingle16Total':21,'nonproficientDisadvantageTotal':10,'successes':[True,False]},'Two independent illustration branches with otherwise-legal shield shove, actual STR penalty and ordinary opposed contest. No extra Attack Action cost, free hand or automatic Prone.')
hidden=True; hidden_trace=[]
for event in ['missedRangedWeaponShot','enterVisibleLitDoorway']:
 if event=='enterVisibleLitDoorway': hidden=False
 hidden_trace.append({'event':event,'HiddenAfter':hidden})
C(49,['GC-50-E01','GC-50-E02'],{'alreadyHiddenFromActualObserver':True,'SkulkerQualifiedRangedWeaponMiss':True,'laterActualClearView':True},hidden_trace,[{'event':'missedRangedWeaponShot','HiddenAfter':True},{'event':'enterVisibleLitDoorway','HiddenAfter':False}],'Source-scoped Hidden state transition for one observer with actual prior lawful Hide; independent later disclosure remains decisive.')
C(50,['GC-51-E01','GC-51-E02','FA-05'],{'samePreControlSpeed':30,'minus10SourceCount':2,'independentHalfSpeed':True},{'oneSlow':max(0,30-10),'twoMinus10Slows':min(max(0,30-10),max(0,30-10)),'withHalfSpeed':min(max(0,30-10),30//2),'withHardZero':0},{'oneSlow':20,'twoMinus10Slows':20,'withHalfSpeed':15,'withHardZero':0},'Current FS04 evaluates each adverse result from the same base; not subtractive stacking or sequential multiplication.')
def hp_band(h,m): return 'Zero' if h==0 else 'Full' if h==m else 'Positive-at-or-below-half' if 2*h<=m else 'Positive-above-half'
C(51,['GC-52-E01'],{'actualCR':'1/2','normalHP':10,'effectiveMaximum':20,'tempHP':7},{'DC':10+math.ceil(Fraction(1,2)),'disclosedBand':hp_band(10,20)},{'DC':11,'disclosedBand':'Positive-at-or-below-half'},'The selected task result discloses only a band; tempHP ignored and no exact HP payload is supplied.')
target_attempts=set(); attempt_trace=[]
for appearance,actual_identity in [('ordinary','creatureA'),('disguised','creatureA'),('differentCreature','creatureB')]:
 admitted=actual_identity not in target_attempts
 if admitted: target_attempts.add(actual_identity)
 attempt_trace.append({'appearance':appearance,'actualIdentity':actual_identity,'attemptAdmitted':admitted})
C(52,['GC-52-E02'],{'noCompletedLRBetweenEvents':True,'firstActualTaskFails':True},attempt_trace,[{'appearance':'ordinary','actualIdentity':'creatureA','attemptAdmitted':True},{'appearance':'disguised','actualIdentity':'creatureA','attemptAdmitted':False},{'appearance':'differentCreature','actualIdentity':'creatureB','attemptAdmitted':True}],'Durable actual target receipt consumes even on failure; a different real target still needs living/perception/range/line and paid BA eligibility.')
C(53,['GC-53-E01','GC-53-E02'],{'ownSuccessfulAttackKinds':['unarmed','improvisedChair'],'sameActualTargetAndFreeHand':True},[kind=='unarmed' for kind in ['unarmed','improvisedChair']],[True,False],'Partial trigger identity only. Actual finite Bonus Action, reach, size and ordinary grapple contest remain required.')
C(54,['GC-54-E01','GC-54-E02'],{'PBValues':[3,2],'actualAttackAbility':3,'damageBefore':5},{'partialAllowances':[4*pb//5 for pb in [3,2]],'attackModifiers':[3+4*pb//5 for pb in [3,2]],'damageAfter':5,'trueProficiencyGranted':False},{'partialAllowances':[2,1],'attackModifiers':[5,4],'damageAfter':5,'trueProficiencyGranted':False},'Partial attack contribution does not authorize Weapon Focus or alter damage; no stacking with another partial allowance.')
C(55,['GC-55-E01','GC-55-E02'],{'paidDistinctFocusTypes':['rapier','longbow'],'requestedRepeat':'rapier','baseAttackModifier':5},{'rapierModifier':5+1,'longbowModifier':5+1,'newRepeatAllowed':'rapier' not in {'rapier','longbow'}},{'rapierModifier':6,'longbowModifier':6,'newRepeatAllowed':False},'Exact actual proficient types, not all piercing weapons. Distinct separately legitimate attack bonuses remain independent.')
C(56,['GC-56-E01','GC-56-E02'],{'startingScores':[19,20,21],'compositeFeatIncrease':1,'cap':20},{'newScores':[s+min(1,max(0,20-s)) for s in [19,20,21]],'physicalWeaponsCreated':0},{'newScores':[20,20,21],'physicalWeaponsCreated':0},'Existing above-cap21 is a hypothetical actual source state, preserved rather than lowered. Four actual finite catalog choices and all Special restrictions remain required.')
C(57,['GC-57-E01','FA-12'],{'ownerLevel':10,'sharedBonusActions':1,'qualifiedHearingCompanions':2},{'maximumRecipients':2 if 10>=10 else 1,'legalHelpActions':2,'maximumOffensiveActions':min(1,2),'ownerBAAfter':1-1},{'maximumRecipients':2,'legalHelpActions':2,'maximumOffensiveActions':1,'ownerBAAfter':0},'Both Help operations require their actual physical targets/positions. This does not grant a second phase, extra turn, autonomous attack or another command wallet.')
receipt=True; followup=[]
for distance,miss,disadvantage in [(40,False,False),(25,True,True),(20,False,False)]:
 eligible=receipt and distance<=30; state=adv(eligible,disadvantage)
 if eligible: receipt=False
 followup.append({'distance':distance,'miss':miss,'featReceiptUsed':eligible,'rollState':state,'receiptAfter':receipt})
C(58,['GC-57-E02'],{'qualifiedCommandedBeastDropReceipt':True,'allAttacksBeforeOriginalDeadline':True,'distances':[40,25,20]},followup,[{'distance':40,'miss':False,'featReceiptUsed':False,'rollState':0,'receiptAfter':True},{'distance':25,'miss':True,'featReceiptUsed':True,'rollState':0,'receiptAfter':False},{'distance':20,'miss':False,'featReceiptUsed':False,'rollState':0,'receiptAfter':False}],'Existing independently legal attacks only. Out-of-range does not consume; eligible miss/cancellation does. No extra attack or world kill is created.')
C(59,['GC-58-E01','GC-58-E02'],{'actualLightOrBodyStates':[{'moonlight':True,'transformed':False},{'moonlight':False,'transformed':False},{'moonlight':False,'transformed':True}],'recipientFixtures':[{'id':'owner','distance':0,'hears':True},{'id':'allyA','distance':25,'hears':True},{'id':'allyB','distance':25,'hears':False},{'id':'allyC','distance':35,'hears':True}]},{'qualifiedStates':[moon or transformed for moon,transformed in [(True,False),(False,False),(False,True)]],'fixedRecipients':[name for name,d,hear in [('owner',0,True),('allyA',25,True),('allyB',25,False),('allyC',35,True)] if d<=30 and hear]},{'qualifiedStates':[True,False,True],'fixedRecipients':['owner','allyA']},'Actual qualifying light/body and heard howl are stipulated, not determined from cosmology or painted props. Real selected target, paid SR use and future deadline remain required.')
turn_claims=set(); cadence=[]
for actual_turn,operation in [('regular-A','attack1'),('regular-A','extraActionAttack'),('extra-A','attack'),('regular-A','replayedAttack')]:
 key=('bladedancer','owner',actual_turn); eligible=key not in turn_claims
 if eligible: turn_claims.add(key)
 cadence.append(eligible)
C(60,['GC-06-E02','GC-44-E02'],{'events':[['regular-A','attack1'],['regular-A','extraActionAttack'],['actualExtra-A','attack'],['regular-A','replay']]},cadence,[True,False,True,False],'Unqualified final FS06 once-per-turn distinguishes real actual extra turns from extra Actions/replays. Explicit own/off regular Savage Attacker limits are not replaced by this projection.')
C(61,['GC-04-E02'],{'bondEndedAtHour':10,'candidateBeneficialRestCompletionHours':[9,10,11],'actualLivingAnimalAndFreeOwnerSlot':True},{'postEndRestGate':[end>10 for end in [9,10,11]],'deadBodyEligible':False,'restCreatesAnimal':False},{'postEndRestGate':[False,False,True],'deadBodyEligible':False,'restCreatesAnimal':False},'Strictly post-end beneficial rest COMPLETION is the existing acquisition gate. Actual attempts, lawful living source/custody, compatibility and uninterrupted hour are independently required.')
def spend_attempt_then_interrupt():
 state={'attempts':1,'bond':None,'pending':None}; trace=[deepcopy(state)]
 state['attempts']-=1; state['pending']='actualAnimalA'; trace.append(deepcopy(state))
 state['pending']=None; trace.append(deepcopy(state))
 state['attempts']=1; trace.append(deepcopy(state))
 return trace
C(62,['GC-04-E01','GC-04-E02'],{'events':['earnedAcquisitionOneAttempt','legalBondStart','interruptedBeforeHourComplete','actualLaterBeneficialLR'],'realAnimalAlreadyExists':True},spend_attempt_then_interrupt(),[{'attempts':1,'bond':None,'pending':None},{'attempts':0,'bond':None,'pending':'actualAnimalA'},{'attempts':0,'bond':None,'pending':None},{'attempts':1,'bond':None,'pending':None}],'Bounded real-attempt transaction trace: interruption loses paid attempt and work; legal rest sets capacity1 without creating/resurrecting/bonding an animal. No arbitrary scheduler or custody engine executed.')
C(63,['GC-57-E01','FA-12'],{'companionNativeDamageComponents':[3,2],'criticalDiceAlreadyIncluded':True,'duplicateTrainers':2,'ownerSurvivalProficient':True,'ownerPB':3,'ownerExpertiseMultiplier':2,'animalWIS':1,'animalOwnTrackingProficiency':4},{'damageAfterOneFamilyFlat':sum([3,2])+2,'trackingModifier':1+max(3,4),'attackBonusAdded':2},{'damageAfterOneFamilyFlat':7,'trackingModifier':5,'attackBonusAdded':2},'Actual qualified trained Beast event. Flat2 once per native roll, not per component/die/trainer; tracking uses better actual proficiency, not owner expertise or stacking both.')
C(64,['GC-37-E01','GC-38-E02'],{'resolvedDirectDamageComponents':[3,5],'guardingDeflectionD6Face':4,'tempHPBefore':2}, {'afterDeflection':[0,4],'wholeDamageAfter':max(0,3+5-4),'normalHPDamageAfterTemp':max(0,(3+5-4)-2)}, {'afterDeflection':[0,4],'wholeDamageAfter':4,'normalHPDamageAfterTemp':2},'Actual paid Reaction+d6 after passive defenses, stable-order whole event before tempHP; zero prevention does not turn a hit into a miss or erase nondamage effects.')
C(65,['GC-38-E01','GC-38-E02'],{'sharedCapacityAfterAdvanced':2,'diceBeforeRest':0,'restEvents':1},{'diceAfterSingleRest':2,'diceAfterRepeatedSameRestCallback':2},{'diceAfterSingleRest':2,'diceAfterRepeatedSameRestCallback':2},'Rest restoration is a capacity assignment under an authenticated single beneficial-rest receipt, not additive2+2 or two independent feat pools.')
linked={ref for c in calcs for ref in c['originalCaseIds']}; ck('all numeric projections link reviewed case identities',linked<={x['id'] for x in cases+boundaries})
paths=[I/'candidate.json',I/'example_dispositions.json',I/'additional_boundary_expectations.json',I/'shared_rules.json',I/'supplements.json',I/'fex_dispositions.json',R/'data/director/general_combat_feat_operating_proposal_internal.json',R/'data/public/feat_candidates/exact_01/candidate.json',D/'data/director/feat_candidates/exact_01/candidate.json',D/'data/public/feat_candidates/exact_01/candidate.json',R/'docs/feats/exact-candidate-01/GENERAL_COMBAT.md',R/'docs/feats/exact-candidate-01/source-audit/GENERAL_COMBAT.md',R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',R/'docs/mechanics/CONDITIONS_PLAYTEST.md',R/'docs/mechanics/CONDITION_RECOVERY_PLAYTEST.md',R/'docs/mechanics/MAXIMUM_HP_PLAYTEST.md',R/'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md',R/'docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md',R/'docs/mechanics/SPELL_INTEGRATION_RULES.md',R/'docs/playtest/COMPANION_COMMAND_WALKTHROUGH.md',R/'data/public/spell_playtests/catalog.json',A/'FEAT335_RESOLUTION_CASES_85.json',A/'FEAT335_PHYSICAL_SOCIAL_COMPOSITIONS_91.json']
source_bytes={p.relative_to(G).as_posix():p.read_bytes() for p in paths}
report={'id':'FEAT335-GENERAL-COMBAT-ORIGINAL-CASEBOOK-REVIEW-99','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'58_FULL_PROCEDURES116_ORIGINAL_POSITIONS3_BOUNDARIES_REVIEWED_WITH65_BOUNDED_CALCULATIONS_PARENT_PENDING','scope':'Complete general_combat stated-case semantic review. Seven prior full expectation changes and original source text retained. No new mechanics or canonical application.','sourceBindings':[info(p) for p in paths],'completeSelectedRecords':selected,'originalCaseReviews':reviews,'additionalBoundaryReviews':boundary_reviews,'numericAndStateCalculations':calcs,'completeDependencySupplements':[sup[k] for k in ['SUP-01','SUP-02','SUP-03','SUP-04']],'inspectedIllustrativeCurriculumRows':chosen_curriculum_rows,'coverage':{'cohort':'general_combat','fullFeatProcedures':58,'originalCasePositions':116,'additionalBoundaries':3,'boundedCalculations':len(calcs),'originalCasesWithNumericalProjection':sum(x['id'] in linked for x in cases),'additionalCasesWithNumericalProjection':sum(x['id'] in linked for x in boundaries)},'preservedEarlierReplacedExpectations':changed,'reviewFindings':['All116 current outcomes and FA05/11/12 are consistent under the stated source predicates. Complete originals and seven current replacements coexist without treating superseded additive slows or ally-only wording as current.','Companion purchase, actual body admission, paid bonding attempt, interrupted work, beneficial post-end rest, release and replacement are separate operations. No animal, inventory, resurrection or HP restoration is granted by a rest or feat receipt.','One actual mount/companion body retains compatible elected EX58 phase and movement history. Two eligible level10 Help recipients do not grant two offensive actions or independent turns.','Blind Fight30, Blind Fighting10 and Improved Alertness10 are different location/effective-sight operations. Shared names and ranges do not imply can-see permission or merged sensing range.','Ordinary Reaction refresh and numbered-round extra token use separate clocks with a shared one-Reaction-per-trigger gate. Extra Actions, extra turns and repeated callbacks do not reset unspecified wallets.','Current FS04 uses strongest adverse Speed result from the same pre-control base. Final FS06 unqualified once-per-turn follows actual turns; explicitly regular interval and Savage Attacker exceptions retain their text.','Elven Accuracy replaces one initial position; Lucky preserves the original selection mode; Savage Attacker chooses a whole native pool; Piercer rerolls one retained eligible die and adds its critical die after doubling. These are not interchangeable three-die or face-picking mechanics.','SUP01 common companion rules, all three SUP02 templates and all six SUP03 maneuver procedures were read as dependencies. Full SUP04 is preserved, with explicit Mage/Wizard/Cleric three-row selection and finite-count checks; this is not semantic closure of all16 curricula or their spell payloads.','Current self-ally cases still require actual senses, paid actions and fixed or continuous recipient membership as individually specified. No second owner identity, universal hearing, loyalty effect or hidden-location disclosure follows.'],'remainingScope':['After registration222 original positions and13 additional boundaries remain across magic_core, magic_extended and heritage_mutation. Whole parent335 acceptance, all finite-table/full-copy dependencies, acquisition evidence and joint submission remain pending.','Reference arithmetic and narrow finite-state projections are not a production engine, full scheduler, arbitrary body/vision geometry or authenticated campaign event. Actual eligibility and source predicates outside each fixture remain external.','The bestiary replacement remains actively generating at last observation; its interim source claims are not independently accepted. This review does not change bestiary type, CR, cosmology or sealed-content scope.','No runtime testing, human gameplay, numerical balance, whole-game or release approval.'],'checks':checks,'passed':len(checks),'failed':0,'newMechanicsAuthored':0,'canonicalApplied':False,'parent335Accepted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'balanceApproved':False,'cosmologyDecisions':0,'actuallySentToGpt':False}
payload=enc(report); script=Path(__file__).read_bytes(); ROOT.mkdir()
for rel,b in source_bytes.items():
 p=ROOT/'sources'/rel; p.parent.mkdir(parents=True,exist_ok=True); put(p,b)
for p,b in [(SAVED,script),(ROOT/Path(__file__).name,script),(OUT,payload),(ROOT/'REVIEW.json',payload)]: put(p,b)
put(ROOT/'README.txt',b'General combat casebook99:58 complete procedures,116 original positions,3 additional boundaries and65 bounded calculations. All original sources and seven prior changes preserved. Full dependencies carried; Mage/Wizard/Cleric example selections checked. No runtime, parent335, balance, cosmology or release approval. No supplied program needs execution.\n')
files=sorted(p for p in ROOT.rglob('*') if p.is_file()); manifest={'files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files]}; put(ROOT/'MANIFEST.json',enc(manifest))
with zipfile.ZipFile(ZIP,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(p for p in ROOT.rglob('*') if p.is_file()): z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(ZIP) as z:
 assert z.testzip() is None
 names=z.namelist(); assert len(names)==len(set(names)) and all(not n.startswith('/') and '..' not in Path(n).parts for n in names)
 assert all(len(z.read(x['path']))==x['bytes'] and sha(z.read(x['path']))==x['sha256'] for x in manifest['files'])
assert all((G/rel).read_bytes()==b for rel,b in source_bytes.items())
print(json.dumps({'report':info(OUT),'archive':info(ZIP),'coverage':report['coverage'],'checks':len(checks),'failed':0,'fullSourceFiles':len(paths),'archiveMembers':len(manifest['files'])+1},indent=2))
