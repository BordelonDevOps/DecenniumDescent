# General Combat — complete source/question reconciliation

Source-authored exact candidate; separate exact review pending. Selection/runtime disabled. Original catalogs unchanged.

## GC-01 — Alert

### Original complete object

```json
{
  "id": "alert",
  "name": "Alert",
  "description": "Always on the lookout for danger, you gain the following benefits:",
  "prerequisite": "None",
  "effect": "+5 bonus to initiative, can't be surprised while conscious, creatures don't gain advantage on attack rolls from being hidden",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Retain +5initiative, no Surprise while conscious and denial of attack advantage from being hidden. Distinguish hidden from unseen/invisible, actual locating/sight, ordinary stealth and other advantage sources. Define consciousness checkpoints and stacking with Alertness/Danger Sense; no free action, initiative reroll or automatic detection.

### Final source decision

Retain the complete GC-01 proposal as explicitly NEW where supplied; Exact Hidden-versus-independent-unseen distinction and conscious surprise suppression. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Add+5 to actual new initiative rolls. While conscious, surprise imposes none of its action/movement/reaction restrictions on you; retain any underlying first-turn schedule and all unrelated incapacity, without granting lost actions. Creatures do not gain attack advantage against you solely because their position is Hidden from you. NEW this prevents the unseen-attacker advantage when its sole cause is that specific Hidden state, but does not remove independent darkness/Blinded/Invisible or another source of advantage. It does not locate them, reveal a suspected square, grant sight or end their Hidden record for others. Other feat initiative bonuses may add by the proposed distinct-family rule. No initiative reroll, extra Reaction, or current-combat order change.

### Final authored examples

A hidden sniper gains no advantage from being Hidden from Alert; the victim still does not know the sniper's square before the shot reveals it normally.

Alert+Alertness adds7 to a new initiative roll. Becoming conscious later restores surprise protection but supplies no retroactive turn.

### Preserved submitted procedure

Add+5 to actual new initiative rolls. While conscious, surprise imposes none of its action/movement/reaction restrictions on you; retain any underlying first-turn schedule and all unrelated incapacity, without granting lost actions. Creatures do not gain attack advantage against you solely because their position is Hidden from you. NEW this prevents the unseen-attacker advantage when its sole cause is that specific Hidden state, but does not remove independent darkness/Blinded/Invisible or another source of advantage. It does not locate them, reveal a suspected square, grant sight or end their Hidden record for others. Other feat initiative bonuses may add by the proposed distinct-family rule. No initiative reroll, extra Reaction, or current-combat order change.

### Preserved submitted examples

A hidden sniper gains no advantage from being Hidden from Alert; the victim still does not know the sniper's square before the shot reveals it normally.

Alert+Alertness adds7 to a new initiative roll. Becoming conscious later restores surprise protection but supplies no retroactive turn.

## GC-02 — Alertness

### Original complete object

```json
{
  "id": "alertness",
  "name": "Alertness",
  "description": "You have finely tuned senses.",
  "prerequisite": "None",
  "effect": "+2 bonus to Perception checks and initiative rolls.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Preserve +2Perception checks and +2initiative as distinct roll categories. Define passive Perception interaction and same-source stacking, without importing Alert surprise protection. Bind Alertness Improved to this exact ID, not similarly named Alert.

### Final source decision

Retain the complete GC-02 proposal as explicitly NEW where supplied; Passive-formula inclusion and distinct-category arithmetic; exact prerequisite identity. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Add+2 to your WIS Perception checks and to new initiative rolls. The Perception contribution also enters your actual passive Perception formula when that task uses Perception; do not add it a second time as a generic awareness modifier. Different eligible initiative feats may add, but duplicate Alertness never does. No Surprise immunity, attack advantage denial, new sense or automatic trap discovery is granted. Improved Alertness requires this exact alertness identity, not alert.

### Final authored examples

WIS+2 andPB3 gives passive15; Alertness makes it17, not19.

The same feat adds2 to initiative, but the owner can still be surprised if no other protection applies.

### Preserved submitted procedure

Add+2 to your WIS Perception checks and to new initiative rolls. The Perception contribution also enters your actual passive Perception formula when that task uses Perception; do not add it a second time as a generic awareness modifier. Different eligible initiative feats may add, but duplicate Alertness never does. No Surprise immunity, attack advantage denial, new sense or automatic trap discovery is granted. Improved Alertness requires this exact alertness identity, not alert.

### Preserved submitted examples

WIS+2 andPB3 gives passive15; Alertness makes it17, not19.

The same feat adds2 to initiative, but the owner can still be surprised if no other protection applies.

## GC-03 — Ambidexterity

### Original complete object

```json
{
  "id": "ambidexterity",
  "name": "Ambidexterity",
  "description": "You can use both hands with equal skill.",
  "prerequisite": "Dexterity 15 or higher",
  "effect": "You can fight with two weapons without penalty to either hand.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Specify the actual two-weapon penalties waived under the current combat/equipment rules. Do not infer free offhand attacks, extra Bonus Actions, heavy/non-light eligibility, extra hands or damage-modifier grants absent a decision. Reconcile Dual Wielder and genuine physical wielding requirements.

### Final source decision

Retain the complete GC-03 proposal as explicitly NEW where supplied; Explicit positive two-weapon damage-modifier restoration as the only newly waived hand penalty. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

The current ordinary two-weapon rule has no inherent attack-roll penalty for either hand; retain that absence. NEW completion of without penalty: when you make the ordinary two-weapon Bonus Action attack, add your usual positive ability modifier to its damage instead of omitting it. A negative modifier still applies normally. This specific grant can also restore the positive modifier to Double Tap's BA attack only if that attack is actually the ordinary two-weapon attack under both sources; a lone-crossbow Double Tap is not. The normal Light one-handed melee weapons, two usable hands, Attack Action trigger and real BA still apply unless Dual Wielder independently expands Light eligibility. It waives no proficiency, Heavy, anatomy, injury or improvised penalty and grants no second BA.

### Final authored examples

DEX+3 dual-Light ordinary BA attack adds3 damage with this feat.

Wielding two non-Light weapons still requires Dual Wielder; this feat alone does not authorize that pair.

### Preserved submitted procedure

The current ordinary two-weapon rule has no inherent attack-roll penalty for either hand; retain that absence. NEW completion of without penalty: when you make the ordinary two-weapon Bonus Action attack, add your usual positive ability modifier to its damage instead of omitting it. A negative modifier still applies normally. This specific grant can also restore the positive modifier to Double Tap's BA attack only if that attack is actually the ordinary two-weapon attack under both sources; a lone-crossbow Double Tap is not. The normal Light one-handed melee weapons, two usable hands, Attack Action trigger and real BA still apply unless Dual Wielder independently expands Light eligibility. It waives no proficiency, Heavy, anatomy, injury or improvised penalty and grants no second BA.

### Preserved submitted examples

DEX+3 dual-Light ordinary BA attack adds3 damage with this feat.

Wielding two non-Light weapons still requires Dual Wielder; this feat alone does not authorize that pair.

## GC-04 — Animal Companion

### Original complete object

```json
{
  "id": "animal_companion",
  "name": "Animal Companion",
  "description": "You have formed a bond with an animal.",
  "prerequisite": "Animal Handling proficiency",
  "effect": "You gain an animal companion that follows your commands and fights alongside you.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Complete a finite legal animal profile/selection and acquisition route, number, size/level progression, actual bond/ownership and command economy. Define initiative/actions/reactions, no-command behavior, injury/death/replacement and global creature caps. Existing Ranger companion rules are comparison evidence, not automatic Ranger class access.

### Final source decision

Adopt the bounded proposal with the completed EX58 controller/phase/physical-history interface; no future transport dependency or extra animal turn.

### FEAT327-ACQ-05 controlling lifecycle addendum

The original object, question, final source decision and preserved submitted procedure above/below remain historical source. FEAT327-ACQ-05 separately completes the purchase, attempt, release and receiving-engine boundaries in the current procedure below. Its NEW decisions do not rewrite the original feat, FS-01/FS-06/FS-10, Ranger class sources, EX58, templates or approval/selection flags. The original worked examples remain compatible endpoint examples, not complete attempt/payment histories.

### Complete candidate procedure

NEW ACQ-05 purchase/bond distinction: acquire Animal Companion once by committing one actual earned unspent feat opportunity while meeting its actual Animal Handling proficiency prerequisite and all other acquisition gates. Record that paid grant and its acquisition snapshot atomically. The animal and bonding hour are not conditions of purchasing the feat. Ownership begins at that commitment, with no companion and one unspent bond attempt under FS-06; it grants neither an animal nor an earlier completed Long Rest. Animal identity, matching template and any actually sourced sense choice belong to each bond record, not a permanently locked feat-purchase choice. The retained nonrepeatability/permanent-choice metadata does not prohibit the replacements expressly allowed here. Canceling a proposed purchase before commitment spends no opportunity. A completed purchase is not refunded or repeated because no animal is available, a bond attempt fails, or a bond later ends. Animal Companion ownership alone can satisfy Companion Training's printed parent alternative, but supplies neither its separate feat opportunity nor a creature on which to use it.

NEW ACQ-05 bond attempt: an owner of this feat with actual Animal Handling proficiency, no current feat bond, no other pending bond attempt, an unspent attempt and any required post-bond-ending Long Rest may select one already real, positive-HP living, willing/tamed, noncorrupted Beast with INT<7 fitting one of the three finite templates. The selected animal must have no incompatible existing bond, including another Animal Companion or Ranger bond. Finding, buying or taming it still needs actual lawful access and its real willing/tamed relationship to this owner; no animal, stocked shop, consent or charm is supplied. Preserve its actual identity, ordinary profile, current/maximum HP, conditions, injuries, native movement, breathing, custody and required template choices. In one ordered start event, recheck admission, reserve this owner and animal for the work, spend the one attempt, and begin the hour. Merely proposing a target or rejecting it before that event does not spend an attempt; it never reverses a previously completed feat purchase. Starting costs no RP, second feat opportunity or universal fee. An attempt cannot begin while an existing feat bond is retained; such a rejected proposal does not release or alter that bond.

Spend one uninterrupted hour of actual bonding work together at touch range. Keep the same owner and animal, actual access, the required proficiency and animal eligibility throughout the work and at completion; the owner must remain able to perform it. This is active work, not beneficial rest, and grants no extra work Watch, assistant shortcut, handover or overlapping incompatible task. Loss of required touch-range access, willing/tamed eligibility, qualifying body state, or the owner's ability to continue, including incapacitation, or voluntary abandonment terminates the attempt. Elapsed time, real losses and the spent attempt persist; no partial hour, resumed fraction or same-epoch retry is awarded. The prospective animal remains in its actual current ordinary state; no feat profile or command entitlement was installed. After a full lawful hour, atomically complete the one bond and apply the existing template/HP conversion to the animal's latest lawful ordinary state, using the owner's then-current governing statistics. No new bond check or success chance is added. Admission alone or an incomplete hour cannot establish a companion.

The initial allowance is one attempt at feat purchase. Each genuinely completed beneficial owner Long Rest thereafter sets the allowance to one, never adds a stored second attempt. Apply FS-06's actual rest limits and one elapsed clock: no reset from Short Rest, debt-only Rest, a repeated rest receipt, a scene, a new target, a new controller, a new day label or level growth. Do not credit active bonding or release work as rest. An invalid claimed completion record is evidence rejection, not an attempt or feat-payment refund: reconcile the real start/interruption/rest history. Missing history cannot be replaced by an assumed unspent allowance. One feat bond at a time. Use the template corresponding to the real animal's body/native movement; do not turn a dog into a bird or grant a new breathing mode. AC12+floor(ownerPB/2), maximumHP5+total owner level; template attack/ability/movement values are explicit NEW. At initial bond convert existing HP proportionally max(1,floor(newMax×oldHP/oldMax)); preserve actual conditions/injuries. Later maximum growth never heals, decreases clamp without damage. Ordinary legal healing works, but no Hit Dice/rest-refill is invented. Use one shared BA command within60ft while the animal can perceive you: in its attached phase after your regular turn, move and make its one attack or Dash/Disengage/Help/Dodge. No independent turn/Reaction; uncommanded move defensively and Dodge. The animal's HP-only chassis dies at0, producing its one actual corpse and ending the bond, with no Wound/death-save sequence; this is a feat-specific NEW rule, not generic animal law. NEW ACQ-05 replacement boundary: when an established feat bond ends through release or death, record that actual ending event. Before this owner begins any later feat bond, require a genuinely beneficial owner Long Rest whose completion is ordered after that event, as well as an available attempt, a real eligible living target and the full new hour. A rest completed before the ending event or an unused prior allowance cannot satisfy that replacement gate. A qualifying completion after the event is sufficient; no additional rule requires the whole rest to have started after it. Existing active-work/rest restrictions still apply. Replacement is a use of the already-owned nonrepeatable feat, not a second purchase. NEW explicit rebond interpretation: a previously released living animal may be selected again if it genuinely qualifies; it is a new bond to the same physical individual, not a new or refreshed animal. A dead animal never becomes eligible merely through rest, release, purchase or this procedure. Voluntary release requires the owner's one uninterrupted hour of actual release work. NEW ACQ-05 release boundary: record its start, but end the bond only on lawful completion; interruption or abandonment grants no partial-hour credit and leaves the existing bond intact unless an independent event already ended it. A fresh release hour may be begun while the bond still exists. Release consumes no bond attempt, feat opportunity or RP. It does not require a second target or borrow the bonding hour's touch-range requirement; actual owner capacity and uninterrupted work remain mandatory. At completion restore the same living animal's saved ordinary profile with the existing positive-current-HP ratio conversion, preserving its current conditions, injuries and actual custody without healing or refilling it. End the outgoing bond's control entitlement and unexecuted commands; preserve all already-spent body/actor allowances. No automatic transfer of custody or command occurs. Record this end for the post-ending Long-Rest gate. A creature cannot simultaneously have this and a Ranger bond, or two owners' Animal Companion bonds. NEW ACQ-05 correction of 'new paid acquisition': a transfer requires the outgoing bond to end through its actual lawful release/death/termination procedure, real lawful access/custody for the receiver, and the receiver's independently authorized new bond. An existing Animal Companion feat owner does not buy that nonrepeatable feat again; they spend their own available attempt and full hour and satisfy their own post-ending Long-Rest gate, if any. The sender's rest, feat ownership or spent attempt neither transfers nor resets the receiver's history. A receiver without this feat must first acquire it through their own actual eligible unspent opportunity, or use an independently acquired receiving engine; receiving the animal grants no feat or class feature. An actual Ranger Beast Companion route retains its own acquired Warder/class-level/selection gates, eligible-beast limits, 4 RP, one-hour touch procedure, once-per-beneficial-owner-Long-Rest allowance and native profile/lifecycle. This feat's no-RP route, release hour and attempt rules do not waive or redefine that class engine. A Ranger bond cannot be ended by invoking another engine's feat-release permission. No universal transfer payment, new animal, healing, additive chassis, second controller, extra phase or refunded body/resource budget is granted. Owner death ends the bond and, if the animal remains alive, restores its saved ordinary profile using the same positive-HP ratio conversion as release; a dead animal remains its actual corpse. Temporary owner incapacity prevents new commands but does not cancel a previously committed legal command; after that command, uncommanded phases remain defensive. This never supplies autonomous attacks.
NEW explicit EX58 interface: retain one real creature identity and one current control/phase record. Riding, bonding or transferring custody does not clone a turn, movement budget, Reaction, attack allowance, body or resource pool. An attached companion acts in its source-defined phase after the owner’s regular turn; a controlled mount uses EX58’s actual mounted-phase procedure. A body fitting both roles elects one compatible route before that round’s work, preserves all already-spent allowances and cannot switch routes to gain a second phase. Its actual load, tack, rider geometry, mounting/dismounting cost and ordinary independent temperament remain. One shared Bonus Action command and one offensive companion action per owner per numbered round apply where those source engines impose them. This feat supplies no blanket override of a specific engine’s attack or no-resource restrictions.
The three supplied body templates are NEW complete feat chassis, not evidence that such a Beast is available. Use only the corresponding real body/native mode. Saved ordinary maximum/currentHP and original constituent identity are required before bonding; no missing oldHP record is replaced by invented full health. The feat’s0HP-death rule applies only to this feat chassis; an independently governed mount/Ranger chassis retains its own rules rather than taking both.

### Final authored examples

A ground companion bonded by level5 has max10HP. A real animal at half of its oldHP converts to5HP, not full10.

At0HP it dies and leaves its actual body. Taking a rest alone neither revives it nor creates another beast.

### Preserved submitted procedure

NEW acquisition: with actual Animal Handling proficiency, select one already real willing/tamed Beast, noncorrupted, INT<7, that fits one of the three finite body templates below. Finding, buying or taming it requires actual campaign access/consent; the feat creates no animal, stocked shop or universal charm. Spend one uninterrupted hour together at touch range; one bond attempt per completedLR, noRP. One feat bond at a time. Use the template corresponding to the real animal's body/native movement; do not turn a dog into a bird or grant a new breathing mode. AC12+floor(ownerPB/2), maximumHP5+total owner level; template attack/ability/movement values are explicit NEW. At initial bond convert existing HP proportionally max(1,floor(newMax×oldHP/oldMax)); preserve actual conditions/injuries. Later maximum growth never heals, decreases clamp without damage. Ordinary legal healing works, but no Hit Dice/rest-refill is invented. Use one shared BA command within60ft while the animal can perceive you: in its attached phase after your regular turn, move and make its one attack or Dash/Disengage/Help/Dodge. No independent turn/Reaction; uncommanded move defensively and Dodge. The animal's HP-only chassis dies at0, producing its one actual corpse and ending the bond, with no Wound/death-save sequence; this is a feat-specific NEW rule, not generic animal law. Death/release never creates replacement: after a new completedLR, a new real animal and full hour are required. Voluntary release takes one uninterrupted hour and ends the bond without healing; preserve the same physical animal and restore its prior ordinary profile with the same current-HP fraction, not a fresh full animal. A creature cannot have this and a Ranger bond simultaneously; transferring requires actual release and new paid acquisition, not additive statistics. Owner death ends the bond and, if the animal remains alive, restores its saved ordinary profile using the same positive-HP ratio conversion as release; a dead animal remains its actual corpse. Temporary owner incapacity prevents new commands but does not cancel a previously committed legal command; after that command, uncommanded phases remain defensive. This never supplies autonomous attacks.

### Preserved submitted examples

A ground companion bonded by level5 has max10HP. A real animal at half of its oldHP converts to5HP, not full10.

At0HP it dies and leaves its actual body. Taking a rest alone neither revives it nor creates another beast.

## GC-05 — Battle Awareness

### Original complete object

```json
{
  "id": "battle_awareness",
  "name": "Battle Awareness",
  "description": "A combatant reads pressure at the flank and shifts clear before an opening becomes a strike.",
  "prerequisite": "Level 5",
  "effect": "Enemies do not gain advantage merely for flanking you, and you gain +1 AC against opportunity attacks.",
  "type": "General",
  "legacyEffect": "+10% evasion vs flanking",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

Retain current no advantage merely from flanking and +1AC against opportunity attacks; preserve legacy10percent evasion as historical conflict. Define the exact attack window, actual flanking procedure and unrelated advantage, no broad all-attack AC or blanket immunity.

### Final source decision

Retain the complete GC-05 proposal as explicitly NEW where supplied; Compatibility protection for absent universal flanking advantage; attack-specific AC window. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

At total level5, opponents receive no attack advantage against you merely because they flank you. Current reviewed combat supplies no universal flanking advantage, and the proposed Tactical Flanker geometry grants only its explicit damage rider; this protection creates no penalty for other defenders and does not erase that separate damage rider. Any independently sourced flanking-advantage rule is suppressed only as an advantage source against you; other advantage still works and ordinary cancellation applies. Gain+1AC only against an actual opportunity attack while that one attack resolves, including a legal feat-specific entry opportunity attack. No lasting AC, immunity or protection from a Reaction attack that is not actually an opportunity attack.

### Final authored examples

A normal attack from a flanking foe has no new benefit to remove; Tactical Flanker's lawful1d6 remains separate.

An entry-trigger polearm opportunity attack compares against+1AC. Mage Slayer's non-opportunity Reaction attack does not.

### Preserved submitted procedure

At total level5, opponents receive no attack advantage against you merely because they flank you. Current reviewed combat supplies no universal flanking advantage, and the proposed Tactical Flanker geometry grants only its explicit damage rider; this protection creates no penalty for other defenders and does not erase that separate damage rider. Any independently sourced flanking-advantage rule is suppressed only as an advantage source against you; other advantage still works and ordinary cancellation applies. Gain+1AC only against an actual opportunity attack while that one attack resolves, including a legal feat-specific entry opportunity attack. No lasting AC, immunity or protection from a Reaction attack that is not actually an opportunity attack.

### Preserved submitted examples

A normal attack from a flanking foe has no new benefit to remove; Tactical Flanker's lawful1d6 remains separate.

An entry-trigger polearm opportunity attack compares against+1AC. Mage Slayer's non-opportunity Reaction attack does not.

## GC-06 — Bladedancer

### Original complete object

```json
{
  "id": "bladedancer",
  "name": "Bladedancer",
  "description": "You move with deadly grace in combat.",
  "prerequisite": "Dexterity 15+",
  "effect": "When you hit with a finesse weapon, you can move 5 feet without provoking opportunity attacks.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Define5ft movement after a finesse-weapon hit, actual action/cadence, movement budget versus extra movement, legal mode/path and timing before riders or new attacks. Bound multi-hit chains and opportunity-attack immunity to this movement. No teleport, free Dash or fabricated hit-farming against nonthreats.

### Final source decision

Retain the complete GC-06 proposal as explicitly NEW where supplied; Once-per-turn meaningful-hostile cap, separate5-point budget and post-hit sequencing. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

NEW once per turn, immediately after your direct attack with an actual Finesse weapon hits a meaningful hostile, you may move using a separate5ft movement-cost budget, with no Action/BA/Reaction. The attack may be melee or a legal thrown Finesse weapon. Resolve its damage and immediate source riders first; if still capable, perform the move before any later attack. This movement provokes no opportunity attacks from anyone but retains terrain, hazards, usable Speed and legal endpoints. One hit cannot bank a move for later; multiple hits that turn do not each create5ft. A copied/periodic hit or harmless training target cannot create movement. No teleport or restoration of ordinary movement.

### Final authored examples

After a dagger hit, move5ft on normal ground without opportunity attacks.

A second hit in the same turn grants no additional move. A difficult5ft tile costs10 and is beyond this5-point budget.

### Preserved submitted procedure

NEW once per turn, immediately after your direct attack with an actual Finesse weapon hits a meaningful hostile, you may move using a separate5ft movement-cost budget, with no Action/BA/Reaction. The attack may be melee or a legal thrown Finesse weapon. Resolve its damage and immediate source riders first; if still capable, perform the move before any later attack. This movement provokes no opportunity attacks from anyone but retains terrain, hazards, usable Speed and legal endpoints. One hit cannot bank a move for later; multiple hits that turn do not each create5ft. A copied/periodic hit or harmless training target cannot create movement. No teleport or restoration of ordinary movement.

### Preserved submitted examples

After a dagger hit, move5ft on normal ground without opportunity attacks.

A second hit in the same turn grants no additional move. A difficult5ft tile costs10 and is beyond this5-point budget.

## GC-07 — Blind Fight

### Original complete object

```json
{
  "id": "blind_fight",
  "name": "Blind Fight",
  "description": "You can fight without relying on sight.",
  "prerequisite": "Wisdom 13+",
  "effect": "You don't suffer disadvantage on attack rolls due to being blinded, and you can pinpoint the location of creatures within 30 feet.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Reconcile no attack disadvantage due to Blinded with pinpointing creatures within30ft. Define senses, barriers, invisibility/hidden positions and actual perception permission; pinpointing does not automatically count as sight. Compare distinct Blind Fighting10ft blindsight without silently merging ranges or granting every unseen-target exception.

### Final source decision

Retain the complete GC-07 proposal as explicitly NEW where supplied; Explicit nonvisual30ft location sense, line/cover/blockers and no true sight grant. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Ignore only attack disadvantage directly imposed by your Blinded condition. Other independent unseen-target, darkness, long-range or condition disadvantages remain. NEW pinpointing is a nonvisual spatial sense: while conscious, automatically know the occupied location of an actual creature within30ft with line of effect, unless it is behind total cover or protected by an explicit anti-detection effect. It needs no hearing or sight and so works while Deafened/Blinded; those bodily consequences otherwise remain. This specific sense defeats a Hidden location within range for you but does not supply visual sight, colors, text, identity/type or perceive objects as creatures. An invisible creature's located position follows the current Invisible known-position exception; separate darkness can still impose unseen penalties. A creature you can see spell still needs actual qualifying sight, not this pinpoint. Leaving range loses live localization; remembered last position is not a new exact current one.

### Final authored examples

A Blinded owner pinpoints a creature20ft away through open air; it still cannot satisfy a spell's can-see requirement using this sense alone.

A creature behind a closed solid wall is not pinpointed, even within10ft; known location outside30 does not remain automatically tracked.

### Preserved submitted procedure

Ignore only attack disadvantage directly imposed by your Blinded condition. Other independent unseen-target, darkness, long-range or condition disadvantages remain. NEW pinpointing is a nonvisual spatial sense: while conscious, automatically know the occupied location of an actual creature within30ft with line of effect, unless it is behind total cover or protected by an explicit anti-detection effect. It needs no hearing or sight and so works while Deafened/Blinded; those bodily consequences otherwise remain. This specific sense defeats a Hidden location within range for you but does not supply visual sight, colors, text, identity/type or perceive objects as creatures. An invisible creature's located position follows the current Invisible known-position exception; separate darkness can still impose unseen penalties. A creature you can see spell still needs actual qualifying sight, not this pinpoint. Leaving range loses live localization; remembered last position is not a new exact current one.

### Preserved submitted examples

A Blinded owner pinpoints a creature20ft away through open air; it still cannot satisfy a spell's can-see requirement using this sense alone.

A creature behind a closed solid wall is not pinpointed, even within10ft; known location outside30 does not remain automatically tracked.

## GC-08 — Blind Fighting

### Original complete object

```json
{
  "id": "blindFighting",
  "name": "Blind Fighting",
  "description": "You can fight effectively without sight.",
  "prerequisite": "Wisdom 13 or higher",
  "effect": "You have blindsight with a range of 10 feet. You can effectively see anything within this range that isn't behind total cover.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Bind the actual10ft blindsight range and no seeing through total cover. Define hidden/invisible creatures, hearing or other sense restrictions, fog/darkness, actual sight requirements and beyond-range attacks. Compare Blind Fight as a separate source identity until explicitly resolved.

### Final source decision

Retain the complete GC-08 proposal as explicitly NEW where supplied; Nonvisual10ft physical blindsight, can-see permission and explicit limits versus30ft location-only feat. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

NEW interpret the literal10ft effectively-see clause as a nonvisual blindsight sense while conscious. Within10ft and line of effect, you can effectively see actual creatures/objects regardless of ordinary darkness, fog, Blinded or invisibility; total cover and explicit blindsight/anti-detection blockers still prevent it. Hearing is not required. It meets an ordinary can-see targeting requirement within that range but cannot read colors, printed text or visual illusion details that require actual eyes; it perceives physical shapes/presence, not a secret true identity or magical aura. Hidden creatures with an exposed physical body in this range are seen by you and therefore not Hidden from you. A purely visual illusion without a physical body is not a real body to this sense; this does not grant other observers automatic disbelief. Beyond10ft use normal senses. Blind Fight's30ft pinpoint range does not extend this10ft effective sight.

### Final authored examples

A creature5ft away in opaque fog can be effectively seen for a can-see spell if line of effect remains.

Owning both feats locates an enemy20ft away but does not extend blindsight or can-see permission to20ft.

### Preserved submitted procedure

NEW interpret the literal10ft effectively-see clause as a nonvisual blindsight sense while conscious. Within10ft and line of effect, you can effectively see actual creatures/objects regardless of ordinary darkness, fog, Blinded or invisibility; total cover and explicit blindsight/anti-detection blockers still prevent it. Hearing is not required. It meets an ordinary can-see targeting requirement within that range but cannot read colors, printed text or visual illusion details that require actual eyes; it perceives physical shapes/presence, not a secret true identity or magical aura. Hidden creatures with an exposed physical body in this range are seen by you and therefore not Hidden from you. A purely visual illusion without a physical body is not a real body to this sense; this does not grant other observers automatic disbelief. Beyond10ft use normal senses. Blind Fight's30ft pinpoint range does not extend this10ft effective sight.

### Preserved submitted examples

A creature5ft away in opaque fog can be effectively seen for a can-see spell if line of effect remains.

Owning both feats locates an enemy20ft away but does not extend blindsight or can-see permission to20ft.

## GC-09 — Brawler

### Original complete object

```json
{
  "id": "brawler",
  "name": "Brawler",
  "description": "You excel at unarmed combat.",
  "prerequisite": "Strength 13 or higher",
  "effect": "Your unarmed strikes deal 1d4 + Strength modifier bludgeoning damage and you can grapple as a bonus action.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Preserve unarmed1d4+STR bludgeoning and Bonus Action grapple without the hit prerequisite printed in Tavern Brawler. Define actual hands/reach/target-size/check, replacement versus stacking with larger unarmed dice and natural-weapon/form attacks. It grants no extra Bonus Action or automatic grapple.

### Final source decision

Retain the complete GC-09 proposal as explicitly NEW where supplied; Replacement unarmed base and unconditional BA Grapple under actual ordinary contests. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Your ordinary unarmed strike base becomes1d4+STR bludgeoning, minimum0. NEW it is a replacement profile, not an added die; choose a separately legal stronger unarmed profile when available without stacking their base dice. It does not replace a form's natural weapon or grant hands/anatomy. You may spend BA for one ordinary Grapple without needing a prior hit or Attack Action. Use actual usable free grasping hand/appendage, reach, target at most one size larger, STR Athletics versus target STR Athletics/DEX Acrobatics, tie preserves state. Normal hold/escape/drag rules remain. This supplies no extra BA or damage with the grapple.

### Final authored examples

An unarmed hit atSTR+2 deals1d4+2; a Monk's larger legal base can be used instead, not added.

Before attacking, a free-handed owner can BA grapple. A weapon in every usable hand still prevents that ordinary grapple.

### Preserved submitted procedure

Your ordinary unarmed strike base becomes1d4+STR bludgeoning, minimum0. NEW it is a replacement profile, not an added die; choose a separately legal stronger unarmed profile when available without stacking their base dice. It does not replace a form's natural weapon or grant hands/anatomy. You may spend BA for one ordinary Grapple without needing a prior hit or Attack Action. Use actual usable free grasping hand/appendage, reach, target at most one size larger, STR Athletics versus target STR Athletics/DEX Acrobatics, tie preserves state. Normal hold/escape/drag rules remain. This supplies no extra BA or damage with the grapple.

### Preserved submitted examples

An unarmed hit atSTR+2 deals1d4+2; a Monk's larger legal base can be used instead, not added.

Before attacking, a free-handed owner can BA grapple. A weapon in every usable hand still prevents that ordinary grapple.

## GC-10 — Cavalry

### Original complete object

```json
{
  "id": "cavalry",
  "name": "Cavalry",
  "description": "You are trained in mounted warfare.",
  "prerequisite": "Animal Handling proficiency",
  "effect": "You have advantage on attacks against unmounted creatures while mounted, and your mount gains +10 feet movement speed.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Retain source mounted advantage against unmounted creatures and mount+10ft Speed. Define attack types, target sizes, legal riding/control and which movement modes increase. Compare Mounted Combatant narrower melee/smaller-target clause; no automatic mount, shared action pool or stacking from multiple riders.

### Final source decision

Adopt the bounded proposal with the completed EX58 controller/phase/physical-history interface; no future transport dependency or extra animal turn.

### Complete candidate procedure

While legally riding a real mount under actual mounted/control/custody rules, your attacks have advantage against actual unmounted creatures. Retain the broad source: melee/ranged weapon, unarmed/natural and spell attacks qualify, with no target-size restriction. Save-only effects do not. Other disadvantage still cancels. The ridden mount's existing Speed modes each gain10ft while you remain its actual rider; NEW derive any mode explicitly equal to another Speed from that modified value rather than adding10 twice. No new mode is created, and Speed0 restrictions override the increase. Multiple Cavalry riders give one+10 family bonus, not one per passenger. The feat creates no mount, control permission, mount attack, shared Action pool or extra turn. Mounted Combatant remains a separate narrower feat with no double advantage. Exact mounting, load and shared-space procedures follow the completed EX58 transport verdict now, not a future placeholder.
NEW explicit EX58 interface: retain one real creature identity and one current control/phase record. Riding, bonding or transferring custody does not clone a turn, movement budget, Reaction, attack allowance, body or resource pool. An attached companion acts in its source-defined phase after the owner’s regular turn; a controlled mount uses EX58’s actual mounted-phase procedure. A body fitting both roles elects one compatible route before that round’s work, preserves all already-spent allowances and cannot switch routes to gain a second phase. Its actual load, tack, rider geometry, mounting/dismounting cost and ordinary independent temperament remain. One shared Bonus Action command and one offensive companion action per owner per numbered round apply where those source engines impose them. This feat supplies no blanket override of a specific engine’s attack or no-resource restrictions.
Apply the one+10 to each independently existing mount Speed before its normal encumbrance/systemic/strongest-slow stages. A derived Speed uses its parent once. It does not modify a vehicle’s unrelated printed route speed, grant a mode, change carrying capacity or count mount displacement as the rider’s self-powered movement for a different feat.

### Final authored examples

A mounted archer attacks an unmounted giant: Cavalry advantage applies despite its size, subject to other disadvantage.

Two Cavalry passengers do not give a horse+20Speed; no flying Speed appears on a walking-only mount.

### Preserved submitted procedure

While legally riding a real mount under actual mounted/control/custody rules, your attacks have advantage against actual unmounted creatures. Retain the broad source: melee/ranged weapon, unarmed/natural and spell attacks qualify, with no target-size restriction. Save-only effects do not. Other disadvantage still cancels. The ridden mount's existing Speed modes each gain10ft while you remain its actual rider; NEW derive any mode explicitly equal to another Speed from that modified value rather than adding10 twice. No new mode is created, and Speed0 restrictions override the increase. Multiple Cavalry riders give one+10 family bonus, not one per passenger. The feat creates no mount, control permission, mount attack, shared Action pool or extra turn. Mounted Combatant remains a separate narrower feat with no double advantage. Exact mounting, load and shared-space procedures must follow the actual expedition/transport verdict when returned.

### Preserved submitted examples

A mounted archer attacks an unmounted giant: Cavalry advantage applies despite its size, subject to other disadvantage.

Two Cavalry passengers do not give a horse+20Speed; no flying Speed appears on a walking-only mount.

## GC-11 — Charger

### Original complete object

```json
{
  "id": "charger",
  "name": "Charger",
  "description": "You can make devastating charge attacks.",
  "prerequisite": "Strength 13 or higher",
  "effect": "When you use the Dash action, you can make one melee weapon attack or shove as a bonus action.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Define source Dash Action versus a Bonus Action Dash or movement grant, same-turn timing and one Bonus Action attack or shove choice. Clarify movement/path requirements if added as NEW, weapon/reach checks, and no imported extra damage or push distance from similarly named external feats.

### Final source decision

Retain the complete GC-11 proposal as explicitly NEW where supplied; Action Dash only and no imported approach/damage bonus. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

After taking Dash as an Action on your own turn, you may use your available BA that turn for either one melee weapon attack or one ordinary Shove. NEW a BA Dash, Reaction movement or merely moving far does not trigger this feat. There is no required approach distance/straight path in its printed source, and no extra damage or push distance is added. The attack needs legal reach/weapon/target; Shove uses ordinary reach, one-size-larger cap and Athletics opposed by Athletics/Acrobatics, with success choosing5ft away or Prone. Actual Speed0 can prevent Dash movement but does not create an attack permission if Dash itself is illegal under your condition; a legal Dash with no movement still meets the Action trigger. No second BA.

### Final authored examples

A legal Action Dash followed by BA spear attack pays both actions; moving10ft is not required by this feat.

A Thief's BA Dash does not trigger Charger and has already spent the ordinary BA anyway.

### Preserved submitted procedure

After taking Dash as an Action on your own turn, you may use your available BA that turn for either one melee weapon attack or one ordinary Shove. NEW a BA Dash, Reaction movement or merely moving far does not trigger this feat. There is no required approach distance/straight path in its printed source, and no extra damage or push distance is added. The attack needs legal reach/weapon/target; Shove uses ordinary reach, one-size-larger cap and Athletics opposed by Athletics/Acrobatics, with success choosing5ft away or Prone. Actual Speed0 can prevent Dash movement but does not create an attack permission if Dash itself is illegal under your condition; a legal Dash with no movement still meets the Action trigger. No second BA.

### Preserved submitted examples

A legal Action Dash followed by BA spear attack pays both actions; moving10ft is not required by this feat.

A Thief's BA Dash does not trigger Charger and has already spent the ordinary BA anyway.

## GC-12 — Cleave

### Original complete object

```json
{
  "id": "cleave",
  "name": "Cleave",
  "description": "Your attacks can strike multiple foes.",
  "prerequisite": "Strength 13+",
  "effect": "When you reduce a creature to 0 hit points with a melee attack, you can make another attack against a different creature within reach.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Complete action cost, once-per-turn/round limits and legitimate hostile-kill trigger for a melee attack reducing a creature to0HP. Require a different legal target within actual reach, settle weapon/attack type and nonrecursive chain interactions with Great Weapon Master/other extra attacks. No RP/Action refund or corpse/friendly farming.

### Final source decision

Retain the complete GC-12 proposal as explicitly NEW where supplied; One own-turn free attack, meaningful drop, nonspell melee modes and one selected derived-attack grant per drop. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

NEW once on your own turn, after your direct melee attack reduces a meaningful hostile from positiveHP to0, you may make one immediate additional melee weapon, natural or unarmed attack against a different creature within the actual reach of the selected legal attack. It costs no separate Action/BA but is exactly one attack, not Attack Action/Extra Attack. No melee spell may be cast through this grant. Death is unnecessary; an actually prevented drop gives no trigger. A different second target need not be hostile, but no staged friendly drop can generate the first trigger. Use current weapon/hands and normal attack/damage; no free draw. Mark the attack as derived under the shared causal cap so it cannot spawn Cleave, Frenzied Rage, Great Weapon Master or analogous further attack grants. If multiple extra-attack sources trigger on the same drop, NEW choose one grant for that event, pay its actual cost, and do not bank the others.

### Final authored examples

A melee hit downs a hostile: make one immediate unarmed or weapon attack against another legal target.

That derived attack downs the next foe; it cannot spawn another Cleave or a Great Weapon Master entitlement.

### Preserved submitted procedure

NEW once on your own turn, after your direct melee attack reduces a meaningful hostile from positiveHP to0, you may make one immediate additional melee weapon, natural or unarmed attack against a different creature within the actual reach of the selected legal attack. It costs no separate Action/BA but is exactly one attack, not Attack Action/Extra Attack. No melee spell may be cast through this grant. Death is unnecessary; an actually prevented drop gives no trigger. A different second target need not be hostile, but no staged friendly drop can generate the first trigger. Use current weapon/hands and normal attack/damage; no free draw. Mark the attack as derived under the shared causal cap so it cannot spawn Cleave, Frenzied Rage, Great Weapon Master or analogous further attack grants. If multiple extra-attack sources trigger on the same drop, NEW choose one grant for that event, pay its actual cost, and do not bank the others.

### Preserved submitted examples

A melee hit downs a hostile: make one immediate unarmed or weapon attack against another legal target.

That derived attack downs the next foe; it cannot spawn another Cleave or a Great Weapon Master entitlement.

## GC-13 — Combat Casting

### Original complete object

```json
{
  "id": "combatCasting",
  "name": "Combat Casting",
  "description": "You have learned to cast spells in the heat of battle.",
  "prerequisite": "Spellcasting ability",
  "effect": "Advantage on Constitution saving throws to maintain concentration, can cast spells as opportunity attacks",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Preserve concentration CON-save advantage and opportunity spell substitution. Define exact spell eligibility, casting time/rank/target restrictions, components/RP and reaction timing; it grants no extra Reaction or slot system. Reconcile War Caster/Battle Mage full source clauses and actual classless casting access.

### Final source decision

Retain the complete GC-13 proposal as explicitly NEW where supplied; Spell-only concentration, full paid Action-spell substitution, exactly one target and event-type boundary. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Gain advantage on CON saves specifically to maintain actual spell concentration, including concentration holding a readied spell. Other CON saves, nonspell concentration and generic Strain/Wounds gain nothing. War Caster's same advantage does not add another die; actual disadvantage cancels normally. When an actual opportunity-attack trigger would let you spend Reaction against one creature, you may instead cast one legally available Action-time spell whose actual target selection is exactly that creature. NEW any accessible rank is permitted, with no other creature/object target, area, self-only effect, long casting time, BA or Reaction spell. Recheck spell range/line/perception at the opportunity window; original movement-trigger timing remains before exit. The spell retains its own attack/save, actual casting route/rank/RP or charge, components/hands/focus, concentration, Dissonance/Refrain and cast interruption. The spell resolves instead of the weapon attack and spends the same Reaction; no spell knowledge or cost waiver. For Sentinel and Battle Awareness it is a spell substitution, not an actual opportunity attack hit, so those weapon-attack event benefits do not automatically transfer.

### Final authored examples

A foe begins leaving reach. A legal single-target Action cantrip can replace the opportunity attack, provided its own range/line and components are legal.

An area burst or Self spell cannot qualify merely because only one enemy would be affected; neither can a1minute ritual.

### Preserved submitted procedure

Gain advantage on CON saves specifically to maintain actual spell concentration, including concentration holding a readied spell. Other CON saves, nonspell concentration and generic Strain/Wounds gain nothing. War Caster's same advantage does not add another die; actual disadvantage cancels normally. When an actual opportunity-attack trigger would let you spend Reaction against one creature, you may instead cast one legally available Action-time spell whose actual target selection is exactly that creature. NEW any accessible rank is permitted, with no other creature/object target, area, self-only effect, long casting time, BA or Reaction spell. Recheck spell range/line/perception at the opportunity window; original movement-trigger timing remains before exit. The spell retains its own attack/save, actual casting route/rank/RP or charge, components/hands/focus, concentration, Dissonance/Refrain and cast interruption. The spell resolves instead of the weapon attack and spends the same Reaction; no spell knowledge or cost waiver. For Sentinel and Battle Awareness it is a spell substitution, not an actual opportunity attack hit, so those weapon-attack event benefits do not automatically transfer.

### Preserved submitted examples

A foe begins leaving reach. A legal single-target Action cantrip can replace the opportunity attack, provided its own range/line and components are legal.

An area burst or Self spell cannot qualify merely because only one enemy would be affected; neither can a1minute ritual.

## GC-14 — Combat Expertise

### Original complete object

```json
{
  "id": "combatExpertise",
  "name": "Combat Expertise",
  "description": "You can trade accuracy for defense.",
  "prerequisite": "Intelligence 13+",
  "effect": "You can take a -1 penalty to attack rolls to gain +1 AC until your next turn.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Define when the optional−1attack/+1AC tradeoff is declared, which attacks bear the penalty, exact next-turn endpoint and whether it can be toggled repeatedly. Bind to actual attack and selected AC rules, no retroactive defense, source stacking or unprinted scaling penalty.

### Final source decision

Retain the complete GC-14 proposal as explicitly NEW where supplied; Committed pre-first-attack activation, all-attack penalty and fixed interval. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

NEW once during your regular own turn, before your first attack roll that turn, declare the−1attack/+1AC trade. You must actually commit a legal attack at that declaration; merely announcing Expertise while making no attack grants no defense. All your attack rolls from that commitment through your next original regular start take−1, including spell, off-turn and linked extra-turn attacks. Gain+1AC for exactly that same interval, including if the first attack misses. No repeated toggling, mid-interval opt-out, scalable penalty or retroactive defense. It is not a stance, so a separately chosen stance remains subject to its rules; duplicate Expertise never stacks.

### Final authored examples

The owner declares before a sword attack; even a miss leaves−1 on later attacks and+1AC until next regular start.

After already making an unpenalized attack, the owner cannot turn Expertise on to obtain defense for that interval.

### Preserved submitted procedure

NEW once during your regular own turn, before your first attack roll that turn, declare the−1attack/+1AC trade. You must actually commit a legal attack at that declaration; merely announcing Expertise while making no attack grants no defense. All your attack rolls from that commitment through your next original regular start take−1, including spell, off-turn and linked extra-turn attacks. Gain+1AC for exactly that same interval, including if the first attack misses. No repeated toggling, mid-interval opt-out, scalable penalty or retroactive defense. It is not a stance, so a separately chosen stance remains subject to its rules; duplicate Expertise never stacks.

### Preserved submitted examples

The owner declares before a sword attack; even a miss leaves−1 on later attacks and+1AC until next regular start.

After already making an unpenalized attack, the owner cannot turn Expertise on to obtain defense for that interval.

## GC-15 — Combat Reflexes

### Original complete object

```json
{
  "id": "combat_reflexes",
  "name": "Combat Reflexes",
  "description": "Your quick reflexes allow you to react swiftly in combat.",
  "prerequisite": "Dexterity 14+",
  "effect": "Gain 1 extra reaction per round",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Complete extra Reaction timing under owner-turn recharge versus shared-round ledger, initial initiative state, one-event multiple reactions and unused carryover. Define whether both Reactions can use the same ability, and how Incapacitated/Reaction denial applies. No repeated initiative entry or extra-turn reset farming.

### Final source decision

Retain the complete GC-15 proposal as explicitly NEW where supplied; Separate numbered-round token matching the printed per-round phrase, canonical entry/boundary state and one-reaction-per-event cap. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

NEW grant one additional general-purpose Reaction token per numbered encounter round, separate from the ordinary regular-start Reaction. It begins available on actual encounter entry unless prohibited, refreshes at the next global numbered-round start, and never carries over as a second extra token. The ordinary token still refreshes at owner regular start. Leaving/reentering initiative retains the same encounter/round ledger; an extra turn refreshes neither extra token nor numbered round. Outside initiative one extra token per actual6second global interval, with no duplicated boundary on transition. You may choose which eligible token to spend, but NEW at most one Reaction from you on the same triggering event; the extra token cannot respond twice to one spell/attack or produce a self-recursive Reaction chain. A later distinct event may use the same named ability if its own cadence allows. Surprise, Incapacitated, Focused and source Reaction prohibitions affect both tokens. No free action or ability knowledge.

### Final authored examples

Before a late initiative slot, spend the ordinary token; after own start it refreshes. The independent extra token remains at most one for that numbered round.

Two different foes leave reach on distinct events: ordinary and extra tokens may fund one attack each. One foe leaving once cannot be attacked twice from that one trigger.

### Preserved submitted procedure

NEW grant one additional general-purpose Reaction token per numbered encounter round, separate from the ordinary regular-start Reaction. It begins available on actual encounter entry unless prohibited, refreshes at the next global numbered-round start, and never carries over as a second extra token. The ordinary token still refreshes at owner regular start. Leaving/reentering initiative retains the same encounter/round ledger; an extra turn refreshes neither extra token nor numbered round. Outside initiative one extra token per actual6second global interval, with no duplicated boundary on transition. You may choose which eligible token to spend, but NEW at most one Reaction from you on the same triggering event; the extra token cannot respond twice to one spell/attack or produce a self-recursive Reaction chain. A later distinct event may use the same named ability if its own cadence allows. Surprise, Incapacitated, Focused and source Reaction prohibitions affect both tokens. No free action or ability knowledge.

### Preserved submitted examples

Before a late initiative slot, spend the ordinary token; after own start it refreshes. The independent extra token remains at most one for that numbered round.

Two different foes leave reach on distinct events: ordinary and extra tokens may fund one attack each. One foe leaving once cannot be attacked twice from that one trigger.

## GC-16 — Coordinator

### Original complete object

```json
{
  "id": "coordinator",
  "name": "Coordinator",
  "description": "You excel at directing others in combat.",
  "prerequisite": "Charisma 13 or higher",
  "effect": "As a bonus action, you can grant an ally within 30 feet advantage on their next attack roll.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Retain Bonus Action, ally30ft and advantage on next attack. Define sensing/hearing/communication, willingness, target self inclusion, expiration, target cap and reapplication. No extra attack or forced ally action; ordinary advantage cancellation still applies.

### Final source decision

Keep actual source ally wording including self, with original target/sensory/budget conditions; no generalized automatic self-target for inherently two-person effects.

### Complete candidate procedure

BA: choose one willing ally within30ft that can perceive and understand your brief audible or visible direction. NEW gain advantage on its next attack roll before your next original regular start; the first attack consumes it whether hit or miss, with no replacement if disadvantage cancels it. One recipient per activation, no extra attack or forced action. Reapplication from the same feat family preserves one advantage entitlement per recipient and the latest expiry, not a stack of future attacks. Multiple applicable next-attack advantage grants consume on that same next attack according to their own rules; they do not queue by name. Actual communication can fail through silence/obstruction, though a mutually understood visible signal is sufficient. You may target yourself, paying the same Bonus Action and retaining the same first-attack deadline.
SOURCE SCOPE CORRECTION: “allies” includes the feat owner unless the actual clause says “other.” The owner must still meet the same hearing/perception, range, willing-target and action/resource predicates. No second body, observer or extra action is created by self-eligibility. This sentence supersedes any narrower owner-exclusion in the submitted proposal, not the preserved original.
For a legal self-targeted instruction, the owner deliberately coordinates their own next attack while paying the Bonus Action; it needs no fictitious second speaker. The original deadline and first-attack consumption remain.

### Final authored examples

The holder spends a Bonus Action to coordinate their own next attack before their next regular start. That first attack consumes the advantage entitlement even if disadvantage cancels it; no extra attack is granted.

If independent disadvantage cancels the benefit, that first attack still consumes the Coordinator entitlement.

### Preserved submitted procedure

BA: choose one other willing ally within30ft that can perceive and understand your brief audible or visible direction. NEW gain advantage on its next attack roll before your next original regular start; the first attack consumes it whether hit or miss, with no replacement if disadvantage cancels it. One recipient per activation, no extra attack or forced action. Reapplication from the same feat family preserves one advantage entitlement per recipient and the latest expiry, not a stack of future attacks. Multiple applicable next-attack advantage grants consume on that same next attack according to their own rules; they do not queue by name. Actual communication can fail through silence/obstruction, though a mutually understood visible signal is sufficient. You cannot target yourself.

### Preserved submitted examples

An ally receives the signal and misses its next attack; the advantage is spent.

If independent disadvantage cancels the benefit, that first attack still consumes the Coordinator entitlement.

## GC-17 — Crossbow Expert

### Original complete object

```json
{
  "id": "crossbowExpert",
  "name": "Crossbow Expert",
  "description": "You have mastered crossbow combat.",
  "prerequisite": "Dexterity 13 or higher",
  "effect": "You ignore the loading property of crossbows and can attack with a hand crossbow as a bonus action.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Define which actual crossbow Loading restriction is waived, while preserving ammunition, actual hands, reload actions not named Loading and weapon support. Complete Bonus Action hand-crossbow trigger/timing and valid wielding state. Do not import close-range disadvantage immunity absent source text.

### Final source decision

Retain the complete GC-17 proposal as explicitly NEW where supplied; Unconditional legal BA hand-crossbow attack and exact Loading-only waiver. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Ignore the actual Loading property's limit of one ammunition attack per Action/BA/Reaction when using a crossbow; Extra Attack can then make its legal number with real bolts. This does not waive Ammunition's free loading hand, Two-Handed support, magazine contents or the separate Repeating5 reload Action. NEW you may spend your BA on your own turn for one attack with an actually wielded usable hand crossbow, without a prior Attack Action requirement. Use its ordinary attack and damage modifiers. A preloaded bolt permits that shot under actual inventory; further loading needs a genuine available hand unless a separate sourced exception applies. No second BA, extra bolt, proficiency or nearby-hostile disadvantage immunity. A shield/buckler does not become a free loading hand.

### Final authored examples

An Attack Action with Extra Attack can fire an ordinary crossbow twice if hands and two bolts are available.

An empty repeating-crossbow magazine still needs its real reload Action; Crossbow Expert does not refill it or erase Repeating5.

### Preserved submitted procedure

Ignore the actual Loading property's limit of one ammunition attack per Action/BA/Reaction when using a crossbow; Extra Attack can then make its legal number with real bolts. This does not waive Ammunition's free loading hand, Two-Handed support, magazine contents or the separate Repeating5 reload Action. NEW you may spend your BA on your own turn for one attack with an actually wielded usable hand crossbow, without a prior Attack Action requirement. Use its ordinary attack and damage modifiers. A preloaded bolt permits that shot under actual inventory; further loading needs a genuine available hand unless a separate sourced exception applies. No second BA, extra bolt, proficiency or nearby-hostile disadvantage immunity. A shield/buckler does not become a free loading hand.

### Preserved submitted examples

An Attack Action with Extra Attack can fire an ordinary crossbow twice if hands and two bolts are available.

An empty repeating-crossbow magazine still needs its real reload Action; Crossbow Expert does not refill it or erase Repeating5.

## GC-18 — Crusher

### Original complete object

```json
{
  "id": "crusher",
  "name": "Crusher",
  "description": "You are adept at dealing bludgeoning damage.",
  "prerequisite": "Strength 13 or higher",
  "effect": "When you hit with a bludgeoning weapon, you can move the target 5 feet and critical hits cause the target to have disadvantage on attack rolls.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Define5ft movement on bludgeoning-weapon hit: declaration, once cadence, size/save/direction/path/collision and order. Complete critical-hit attack disadvantage duration/targets. Preserve source weapon-type scope rather than all bludgeoning spell damage and prevent recursive forced-movement triggers.

### Final source decision

Retain the complete GC-18 proposal as explicitly NEW where supplied; Once-turn movement, one-size cap, no save, legal horizontal direction and exact critical-disadvantage endpoint. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

NEW once per turn, after your direct attack with a weapon whose native damage includes bludgeoning hits, you may move the target5ft to a legal unoccupied destination, subject to a target size no more than one category larger than you. Choose direction; this is forced displacement along a real unobstructed path, not teleport. No save is added. It cannot lift into unsupported air or through a wall; ordinary falling applies if moved over a real edge. Resolve hit damage before movement; an actual hit with0resolved damage can still qualify. Separately, a critical hit with that bludgeoning weapon imposes disadvantage on all the target's attack rolls through your next original regular start, no size limit. Repeated critical records retain independent deadlines but disadvantage is applied once. This source is weapon-qualified, not any bludgeoning spell or added rider on a nonbludgeoning weapon. A real natural weapon qualifies only if its profile is a bludgeoning weapon; ordinary unarmed is not one without an express rule.

### Final authored examples

A mace hit can move a similarly sized foe5ft sideways into an open square; it cannot phase through an occupied wall.

A critical with that mace gives disadvantage through next owner start even if the target is too large to move.

### Preserved submitted procedure

NEW once per turn, after your direct attack with a weapon whose native damage includes bludgeoning hits, you may move the target5ft to a legal unoccupied destination, subject to a target size no more than one category larger than you. Choose direction; this is forced displacement along a real unobstructed path, not teleport. No save is added. It cannot lift into unsupported air or through a wall; ordinary falling applies if moved over a real edge. Resolve hit damage before movement; an actual hit with0resolved damage can still qualify. Separately, a critical hit with that bludgeoning weapon imposes disadvantage on all the target's attack rolls through your next original regular start, no size limit. Repeated critical records retain independent deadlines but disadvantage is applied once. This source is weapon-qualified, not any bludgeoning spell or added rider on a nonbludgeoning weapon. A real natural weapon qualifies only if its profile is a bludgeoning weapon; ordinary unarmed is not one without an express rule.

### Preserved submitted examples

A mace hit can move a similarly sized foe5ft sideways into an open square; it cannot phase through an occupied wall.

A critical with that mace gives disadvantage through next owner start even if the target is too large to move.

## GC-19 — Danger Sense

### Original complete object

```json
{
  "id": "danger_sense",
  "name": "Danger Sense",
  "description": "At level 3, alert awareness grants the listed initiative bonus and easier trap detection.",
  "prerequisite": "Level 3",
  "effect": "Gain +2 to initiative and advantage on Perception checks made to notice traps or immediate ambush signs.",
  "type": "General",
  "legacyEffect": "+4 to initiative, detect traps easier",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

Explicitly reconcile legacy+4initiative with current+2 plus Perception advantage for traps/immediate ambush signs. Define active/passive Perception, real evidence and sensing, no automatic detection, Surprise immunity or extra save advantage; level3 uses actual character-level authority.

### Final source decision

Retain the complete GC-19 proposal as explicitly NEW where supplied; Explicit current+2 versus preserved legacy+4 and evidence-bound active Perception. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

At total character level3, add the current effect's+2 to new initiative rolls; preserve legacy+4 only as historical text. Gain advantage on actual Perception checks to notice traps or signs of an immediate ambush when real relevant evidence is perceivable by your working senses. It does not invent evidence, auto-detect danger, reveal a hidden identity or grant surprise immunity/DEX-save advantage. Ordinary passive Perception has no invented±5 advantage adjustment; an explicitly called active Perception roll uses advantage. Distinct Alert/Alertness initiative bonuses may add, but no reroll or retroactive initiative change.

### Final authored examples

Hearing suspicious movement immediately around a corner can qualify for an advantaged actual Perception roll.

A completely undetectable trap with no available cue is not automatically found; initiative remains+2 from this source, not+4.

### Preserved submitted procedure

At total character level3, add the current effect's+2 to new initiative rolls; preserve legacy+4 only as historical text. Gain advantage on actual Perception checks to notice traps or signs of an immediate ambush when real relevant evidence is perceivable by your working senses. It does not invent evidence, auto-detect danger, reveal a hidden identity or grant surprise immunity/DEX-save advantage. Ordinary passive Perception has no invented±5 advantage adjustment; an explicitly called active Perception roll uses advantage. Distinct Alert/Alertness initiative bonuses may add, but no reroll or retroactive initiative change.

### Preserved submitted examples

Hearing suspicious movement immediately around a corner can qualify for an advantaged actual Perception roll.

A completely undetectable trap with no available cue is not automatically found; initiative remains+2 from this source, not+4.

## GC-20 — Deadly Aim

### Original complete object

```json
{
  "id": "deadlyAim",
  "name": "Deadly Aim",
  "description": "You can trade accuracy for damage with ranged weapons.",
  "prerequisite": "Dexterity 13+",
  "effect": "You can take a -1 penalty to ranged attack rolls to deal +2 damage.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Declare optional−1 ranged-attack/+2damage before the roll and define duration, ranged weapon versus spell scope, packets/crit treatment and stacking with similar feats. No uncapped scaling or retroactive trade after seeing the die.

### Final source decision

Retain the complete GC-20 proposal as explicitly NEW where supplied; Broad ranged-attack scope, per-attack declaration and one flat native component. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Before any actual ranged attack roll, optionally accept−1 on that one roll to add+2flat damage if it hits. NEW the source says ranged attacks, so this includes ranged weapon, thrown, natural and spell attacks, but not save-only effects. The+2 joins one native damage component of that attack, chosen if multiple types, and is not doubled by a critical. It does not create damage for an attack with no native damage. Each attack makes its own pre-roll choice, no persistent stance or rest limit. Duplicate same feat cannot scale the trade; no retroactive selection after the die. Independently eligible feat modifiers may add unless their actual family forbids it.

### Final authored examples

A ranged spell attack accepts−1 before rolling and adds2 to native fire damage on a hit.

A critical doubles the attack's dice as usual but keeps Deadly Aim at+2, not+4.

### Preserved submitted procedure

Before any actual ranged attack roll, optionally accept−1 on that one roll to add+2flat damage if it hits. NEW the source says ranged attacks, so this includes ranged weapon, thrown, natural and spell attacks, but not save-only effects. The+2 joins one native damage component of that attack, chosen if multiple types, and is not doubled by a critical. It does not create damage for an attack with no native damage. Each attack makes its own pre-roll choice, no persistent stance or rest limit. Duplicate same feat cannot scale the trade; no retroactive selection after the die. Independently eligible feat modifiers may add unless their actual family forbids it.

### Preserved submitted examples

A ranged spell attack accepts−1 before rolling and adds2 to native fire damage on a hit.

A critical doubles the attack's dice as usual but keeps Deadly Aim at+2, not+4.

## GC-21 — Defender

### Original complete object

```json
{
  "id": "defender",
  "name": "Defender",
  "description": "You excel at protecting others.",
  "prerequisite": "Constitution 13 or higher",
  "effect": "When an ally within 5 feet is attacked, you can use your reaction to impose disadvantage on the attack roll.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Define Reaction declaration before the attack result, eligible attacker/ally sensing and physical restrictions if any, and exact5ft ally range snapshot. Apply disadvantage to that one attack, not an entire multiattack; no damage interception, movement, extra Reaction or negation of all advantage.

### Final source decision

Keep actual source ally wording including self, with original target/sensory/budget conditions; no generalized automatic self-target for inherently two-person effects.

### Complete candidate procedure

When an allied creature, including yourself, within5ft of you is targeted by an attack, spend Reaction before its attack roll to impose disadvantage on that one roll. NEW you must perceive the ally and the attacker's actual attack; no can-see requirement, shield or free hand is added, but you must be capable of a deliberate physical distraction/intervention with line of effect to the ally. It does not require reaching the attacker, so a visible incoming ranged shot can qualify. Range is checked at declaration and no movement is granted. Advantage cancels normally; later attacks in a multiattack need their own actual triggers/resources. This grants no damage transfer, interception, AC bonus or reroll after the result.
SOURCE SCOPE CORRECTION: “allies” includes the feat owner unless the actual clause says “other.” The owner must still meet the same hearing/perception, range, willing-target and action/resource predicates. No second body, observer or extra action is created by self-eligibility. This sentence supersedes any narrower owner-exclusion in the submitted proposal, not the preserved original.

### Final authored examples

An eligible incoming attack targets the holder. Before its roll, the holder may spend their own Reaction to impose disadvantage through a real defensive intervention; no shield/free hand or second ally is required by this feat.

A second attack in the same multiattack is unaffected unless a separate legal Reaction is available on that distinct event.

### Preserved submitted procedure

When another allied creature within5ft of you is targeted by an attack, spend Reaction before its attack roll to impose disadvantage on that one roll. NEW you must perceive the ally and the attacker's actual attack; no can-see requirement, shield or free hand is added, but you must be capable of a deliberate physical distraction/intervention with line of effect to the ally. It does not require reaching the attacker, so a visible incoming ranged shot can qualify. Range is checked at declaration and no movement is granted. Advantage cancels normally; later attacks in a multiattack need their own actual triggers/resources. This grants no damage transfer, interception, AC bonus or reroll after the result.

### Preserved submitted examples

An adjacent ally faces a visible archer's shot: spend Reaction before the roll for disadvantage.

A second attack in the same multiattack is unaffected unless a separate legal Reaction is available on that distinct event.

## GC-22 — Disarm

### Original complete object

```json
{
  "id": "disarm",
  "name": "Disarm",
  "description": "You can disarm opponents in combat.",
  "prerequisite": "Dexterity 13+",
  "effect": "You can attempt to disarm an opponent as an attack. The target makes a Strength or Dexterity save (DC 8 + proficiency + ability modifier).",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Preserve an attack replacement and target STRorDEX save against8+PB+ability modifier. Define whose choice, attacking ability, reach/weapon/hands, target-size/item constraints and failed-save item landing/custody. No automatic theft, destruction, disarm of implanted body parts or free replacement attack.

### Final source decision

Retain the complete GC-22 proposal as explicitly NEW where supplied; Actual Attack Action replacement, melee implement/ability, target choice and no damage/custody grant. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Replace one attack of your Attack Action with this attempt against a held reachable object of a creature in your current melee reach. NEW choose either an actually wielded melee weapon or a usable free grasping hand as the implement; use that weapon's actual attack ability orSTR for an unarmed attempt. Target choosesSTR orDEX save DC8+PB+that actual ability modifier. No attack roll, damage, critical or on-hit trigger. Failure drops one declared object to a legal adjacent unoccupied space you choose, otherwise its own space; success keeps it. No size limit is added by the source, but physical reach, graspability and real non-droppable bonds remain. Implanted body parts, worn armor and strapped shields are not freely held droppable objects. You do not gain custody automatically; retrieving costs normal interaction/time. No special proficiency requirement grants missing weapon PB on other attacks.

### Final authored examples

ADEX+3 proficient dagger implement atPB3 setsDC14; target chooses itsSTR orDEX save.

A failed save can drop a held wand, but cannot sever an implanted claw or instantly transfer ownership to the attacker.

### Preserved submitted procedure

Replace one attack of your Attack Action with this attempt against a held reachable object of a creature in your current melee reach. NEW choose either an actually wielded melee weapon or a usable free grasping hand as the implement; use that weapon's actual attack ability orSTR for an unarmed attempt. Target choosesSTR orDEX save DC8+PB+that actual ability modifier. No attack roll, damage, critical or on-hit trigger. Failure drops one declared object to a legal adjacent unoccupied space you choose, otherwise its own space; success keeps it. No size limit is added by the source, but physical reach, graspability and real non-droppable bonds remain. Implanted body parts, worn armor and strapped shields are not freely held droppable objects. You do not gain custody automatically; retrieving costs normal interaction/time. No special proficiency requirement grants missing weapon PB on other attacks.

### Preserved submitted examples

ADEX+3 proficient dagger implement atPB3 setsDC14; target chooses itsSTR orDEX save.

A failed save can drop a held wand, but cannot sever an implanted claw or instantly transfer ownership to the attacker.

## GC-23 — Dual Wielder

### Original complete object

```json
{
  "id": "dualWielder",
  "name": "Dual Wielder",
  "description": "You master fighting with two weapons.",
  "prerequisite": "Dexterity 13+",
  "effect": "You can use two-weapon fighting with non-light weapons and gain +1 AC while wielding two weapons.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Define non-light two-weapon eligibility using actual one/two-handed, heavy and size properties; neither extra hands nor dual two-handed wielding is implied. Preserve +1AC while actually wielding two eligible weapons, selected formula/stacking and loss when dropping one. Compare Ambidexterity separately.

### Final source decision

Retain the complete GC-23 proposal as explicitly NEW where supplied; Actual one-handed melee pairing, Versatile one-hand profile and AC dependency. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

For ordinary two-weapon fighting, each weapon may be a non-Light one-handed melee weapon that you can actually wield in its own usable hand. NEW Versatile works using its one-hand profile; Two-Handed cannot occupy one hand, and Heavy/size penalties still apply even if an unusual legal one-hand profile has Heavy. Do not dual-wield a weapon requiring two hands with another weapon absent an actual specific hand exception. Gain+1AC while actually wielding two such usable melee weapons, one in each of two hands; a Broken, stowed, dropped or anatomy-incompatible weapon cannot supply the bonus. No extra draw/stow, BA or positive offhand damage modifier: Ambidexterity or another explicit grant supplies that separately. The ordinary Attack Action and two-weapon BA trigger remain.

### Final authored examples

Two usable longswords can form a legal pair, each using1d8 rather than its two-hand1d10.

Dropping one sword immediately ends+1AC. A greatsword held with one hand does not become a legal paired weapon.

### Preserved submitted procedure

For ordinary two-weapon fighting, each weapon may be a non-Light one-handed melee weapon that you can actually wield in its own usable hand. NEW Versatile works using its one-hand profile; Two-Handed cannot occupy one hand, and Heavy/size penalties still apply even if an unusual legal one-hand profile has Heavy. Do not dual-wield a weapon requiring two hands with another weapon absent an actual specific hand exception. Gain+1AC while actually wielding two such usable melee weapons, one in each of two hands; a Broken, stowed, dropped or anatomy-incompatible weapon cannot supply the bonus. No extra draw/stow, BA or positive offhand damage modifier: Ambidexterity or another explicit grant supplies that separately. The ordinary Attack Action and two-weapon BA trigger remain.

### Preserved submitted examples

Two usable longswords can form a legal pair, each using1d8 rather than its two-hand1d10.

Dropping one sword immediately ends+1AC. A greatsword held with one hand does not become a legal paired weapon.

## GC-24 — Elven Accuracy

### Original complete object

```json
{
  "id": "elvenAccuracy",
  "name": "Elven Accuracy",
  "description": "Your elven heritage grants supernatural accuracy.",
  "prerequisite": "Elf or half-elf",
  "effect": "When you have advantage on an attack roll using Dexterity, Intelligence, Wisdom, or Charisma, you can reroll one of the dice.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Preserve Elf or half-elf eligibility without inventing an absent half-elf ancestry alias. For an advantaged DEX/INT/WIS/CHA attack define optional reroll of one die, timing, must-use-new result, number of rerolls and advantage cancellation. No automatic third die on disadvantage, STR attacks or repeated same-die chains.

### Final source decision

Retain the complete GC-24 proposal as explicitly NEW where supplied; Actual ancestry receipt, replace-one-die procedure, before-outcome timing and no reroll loop. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Require an actual Elf ancestry receipt or a genuine independently sourced half-elf receipt; do not create or alias an absent half-elf base. On an attack actually made with advantage usingDEX,INT,WIS orCHA, after seeing the two original d20s and before final hit/outcome declaration, you may reroll one chosen die once and must use its new face in that position. Then keep the higher of the two resulting dice. NEW at most one Elven Accuracy reroll per attack; it cannot reroll the same die again through this feature or create a third independent kept die. If any disadvantage cancels advantage, there is one ordinary die and this feature is ineligible. STR/CON attacks, saves and checks do not qualify. Keep actual natural-face provenance for criticals. Lucky's separate die replacement may affect this attack only under its own one-event procedure; no Elven reroll of that additional Lucky die.

### Final authored examples

An advantagedDEX attack rolls4 and12. Reroll4 to9, then keep12; rerolling does not guarantee improvement.

Advantage canceled by disadvantage yields one d20, so Elven Accuracy cannot trigger.

### Preserved submitted procedure

Require an actual Elf ancestry receipt or a genuine independently sourced half-elf receipt; do not create or alias an absent half-elf base. On an attack actually made with advantage usingDEX,INT,WIS orCHA, after seeing the two original d20s and before final hit/outcome declaration, you may reroll one chosen die once and must use its new face in that position. Then keep the higher of the two resulting dice. NEW at most one Elven Accuracy reroll per attack; it cannot reroll the same die again through this feature or create a third independent kept die. If any disadvantage cancels advantage, there is one ordinary die and this feature is ineligible. STR/CON attacks, saves and checks do not qualify. Keep actual natural-face provenance for criticals. Lucky's separate die replacement may affect this attack only under its own one-event procedure; no Elven reroll of that additional Lucky die.

### Preserved submitted examples

An advantagedDEX attack rolls4 and12. Reroll4 to9, then keep12; rerolling does not guarantee improvement.

Advantage canceled by disadvantage yields one d20, so Elven Accuracy cannot trigger.

## GC-25 — Fast Talker

### Original complete object

```json
{
  "id": "fast_talker",
  "name": "Fast Talker",
  "description": "You can talk your way out of trouble.",
  "prerequisite": "Charisma 15+",
  "effect": "You can attempt to distract or confuse enemies with rapid speech, potentially causing them to lose their action.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

The source has no action, range, skill contest/save, duration or cadence for enemy action loss. Complete each with actual speech/language/hearing and hard-control guard. Distinguish conversation from combat action denial, define immunity/repeats and no automatic consent or unlimited stun-lock.

### Final source decision

Retain the complete GC-25 proposal as explicitly NEW where supplied; Action/SR/30ft/language/WIS-save procedure, next-regular-turn Action denial and shared hard-control guard. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

NEW complete combat procedure: Action, once per SR, choose one hostile creature within30ft that can hear your rapid speech and understands the language you actually speak. Spend the use at declaration; it makesWIS save DC8+PB+CHA. Failure prevents it taking an Action during its next future regular turn; movement, BA and Reaction are not otherwise removed, and an extra-Action grant cannot bypass that turn's denial. The source-character/target/encounter hard-denial guard applies jointly with class/spell/companion/other feat denial; a target already affected by your hard denial in this encounter cannot suffer this rider again. NEW hearing/language comprehension and a capacity to process speech are required; explicit immunity to this mental action-denial effect blocks it, but the feat does not automatically impose Charmed, Frightened or Stunned. It neither forces beliefs nor commands a particular act. Outside combat it can support an ordinary social attempt but does not automatically win agreement or impose a recurring lost-time penalty.

### Final authored examples

A hearing language-sharing foe failsDC14: it can move and use a legalBA on its next regular turn, but cannot take an Action.

A foe unable to understand the speech is ineligible, and a previously denied target is protected by the shared encounter guard.

### Preserved submitted procedure

NEW complete combat procedure: Action, once per SR, choose one hostile creature within30ft that can hear your rapid speech and understands the language you actually speak. Spend the use at declaration; it makesWIS save DC8+PB+CHA. Failure prevents it taking an Action during its next future regular turn; movement, BA and Reaction are not otherwise removed, and an extra-Action grant cannot bypass that turn's denial. The source-character/target/encounter hard-denial guard applies jointly with class/spell/companion/other feat denial; a target already affected by your hard denial in this encounter cannot suffer this rider again. NEW hearing/language comprehension and a capacity to process speech are required; explicit immunity to this mental action-denial effect blocks it, but the feat does not automatically impose Charmed, Frightened or Stunned. It neither forces beliefs nor commands a particular act. Outside combat it can support an ordinary social attempt but does not automatically win agreement or impose a recurring lost-time penalty.

### Preserved submitted examples

A hearing language-sharing foe failsDC14: it can move and use a legalBA on its next regular turn, but cannot take an Action.

A foe unable to understand the speech is ineligible, and a previously denied target is protected by the shared encounter guard.

## GC-26 — Fencer

### Original complete object

```json
{
  "id": "fencer",
  "name": "Fencer",
  "description": "You are skilled with finesse weapons.",
  "prerequisite": "Dexterity 13 or higher",
  "effect": "When wielding a finesse weapon, you gain +1 AC and can make opportunity attacks when enemies enter your reach.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Define actual finesse-weapon wielding for+1AC, one/two hands, shields and source stacking. Complete entry-into-reach opportunity attack trigger, movement/teleport/forced-movement exceptions and Reaction cost. Do not grant an extra Reaction or import a new reach beyond the weapon.

### Final source decision

Retain the complete GC-26 proposal as explicitly NEW where supplied; Usable Finesse melee-weapon AC and voluntary entry opportunity trigger with actual immunity rules. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

While actually wielding a usable Finesse melee weapon, gain+1AC as one feat modifier. NEW a second empty hand is not required and a lawful shield may coexist; the weapon must remain wielded with actual anatomy and cannot be Broken/stowed. When a seen hostile creature voluntarily crosses from outside to inside that weapon's ordinary current melee reach, you may spend Reaction for one opportunity attack with that same weapon immediately after entry and before further movement. It must be a legal melee target in reach then. Forced displacement, teleport, newly appearing, your movement/reach expansion and the target merely starting within reach do not trigger. Disengage/opportunity immunity suppresses it. Lunge's single-attack extension creates no persistent entry boundary. No additional Reaction or perpetual threatened range.

### Final authored examples

A seen enemy walks from10ft to5ft from a rapier wielder: the entry attack may spendReaction.

Pushing an enemy into5ft or extending reach around it does not trigger this feat.

### Preserved submitted procedure

While actually wielding a usable Finesse melee weapon, gain+1AC as one feat modifier. NEW a second empty hand is not required and a lawful shield may coexist; the weapon must remain wielded with actual anatomy and cannot be Broken/stowed. When a seen hostile creature voluntarily crosses from outside to inside that weapon's ordinary current melee reach, you may spend Reaction for one opportunity attack with that same weapon immediately after entry and before further movement. It must be a legal melee target in reach then. Forced displacement, teleport, newly appearing, your movement/reach expansion and the target merely starting within reach do not trigger. Disengage/opportunity immunity suppresses it. Lunge's single-attack extension creates no persistent entry boundary. No additional Reaction or perpetual threatened range.

### Preserved submitted examples

A seen enemy walks from10ft to5ft from a rapier wielder: the entry attack may spendReaction.

Pushing an enemy into5ft or extending reach around it does not trigger this feat.

## GC-27 — Fighter

### Original complete object

```json
{
  "id": "fighter",
  "name": "Fighter",
  "description": "You have trained extensively in combat.",
  "prerequisite": "Strength or Dexterity 13 or higher",
  "effect": "You gain proficiency with all simple and martial weapons and can use a bonus action to make an additional attack.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Preserve all simple/martial weapon proficiency and Bonus Action extra attack. Complete trigger, cadence, weapon/unarmed/natural/spell eligibility and actual wielding conditions. The feat name is not a new Fighter class, extra class level, unrestricted Extra Attack stack or second Bonus Action.

### Final source decision

Retain the complete GC-27 proposal as explicitly NEW where supplied; Any lawful personal physical-attack trigger, oneBA nonspell attack and no class alias. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Gain proficiency with all actual Simple and Martial weapon profiles; no armor, shield, class level or item is granted. NEW after making at least one personal weapon, natural or unarmed attack on your own turn through a legal source, you may spendBA for one additional personal weapon, natural or unarmed attack. It is not a spell cast and cannot substitute a spell attack that needs casting. No Attack Action is specifically required, but a save-only technique is not a prior attack. Actual weapon/ammunition/hands/reach and physical capability remain. One availableBA, no Extra Attack multiplier. The additional attack is derived and cannot create another feat-granted extra-attack entitlement in its causal root. The feat's name is not a Fighter class or permission to take an external class's features.

### Final authored examples

After one unarmed attack, the owner canBA attack with a legally wielded martial weapon using its newly granted proficiency.

A fireball-like save-only spell supplies no prior physical attack, and the feat cannot cast a second spell as its BA attack.

### Preserved submitted procedure

Gain proficiency with all actual Simple and Martial weapon profiles; no armor, shield, class level or item is granted. NEW after making at least one personal weapon, natural or unarmed attack on your own turn through a legal source, you may spendBA for one additional personal weapon, natural or unarmed attack. It is not a spell cast and cannot substitute a spell attack that needs casting. No Attack Action is specifically required, but a save-only technique is not a prior attack. Actual weapon/ammunition/hands/reach and physical capability remain. One availableBA, no Extra Attack multiplier. The additional attack is derived and cannot create another feat-granted extra-attack entitlement in its causal root. The feat's name is not a Fighter class or permission to take an external class's features.

### Preserved submitted examples

After one unarmed attack, the owner canBA attack with a legally wielded martial weapon using its newly granted proficiency.

A fireball-like save-only spell supplies no prior physical attack, and the feat cannot cast a second spell as its BA attack.

## GC-28 — Fleet of Foot

### Original complete object

```json
{
  "id": "fleet_of_foot",
  "name": "Fleet of Foot",
  "description": "An agile character gains the listed movement-speed increase.",
  "prerequisite": "Agility 14+",
  "effect": "Increase your walking speed by 10 feet.",
  "type": "General",
  "legacyEffect": "+10% movement speed",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

Reconcile legacy+10percent movement with current+10ft walking Speed. Bind Agility14+ through the actual ability authority without inventing a seventh ability or silent substitution. Define other movement-mode derivations and source stacking under reviewed Speed arbitration.

### Final source decision

Retain the complete GC-28 proposal as explicitly NEW where supplied; Explicit Agility→DEX and current+10ft versus legacypercent, walking-only derivation. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

NEW interpret this feat's legacy Agility14 as permanentDEX14, without adding a seventh ability. Increase current walkingSpeed by10ft; preserve its older+10% wording only as historical source. No direct addition to independent flying/swimming/climbing modes. A mode explicitly defined as equal to walkingSpeed derives from the increased walking value once; if another rule independently increases both, do not count the same derivation twice. Actual conditions settingSpeed0 and other lawful reductions still apply, and changingSpeed never refunds spent movement. Distinct fixed Speed feat bonuses may add once each; duplicate Fleet does not.

### Final authored examples

Walk30 becomes40; an independentFly30 remains30.

A climbingSpeed expressly equal to walking becomes40 too, but not50 from adding Fleet a second time.

### Preserved submitted procedure

NEW interpret this feat's legacy Agility14 as permanentDEX14, without adding a seventh ability. Increase current walkingSpeed by10ft; preserve its older+10% wording only as historical source. No direct addition to independent flying/swimming/climbing modes. A mode explicitly defined as equal to walkingSpeed derives from the increased walking value once; if another rule independently increases both, do not count the same derivation twice. Actual conditions settingSpeed0 and other lawful reductions still apply, and changingSpeed never refunds spent movement. Distinct fixed Speed feat bonuses may add once each; duplicate Fleet does not.

### Preserved submitted examples

Walk30 becomes40; an independentFly30 remains30.

A climbingSpeed expressly equal to walking becomes40 too, but not50 from adding Fleet a second time.

## GC-29 — Great Weapon Master

### Original complete object

```json
{
  "id": "greatWeaponMaster",
  "name": "Great Weapon Master",
  "description": "You have mastered two-handed weapons.",
  "prerequisite": "Strength 13 or higher",
  "effect": "When you score a critical hit or reduce a creature to 0 hit points, you can make another attack as a bonus action.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Source grants a Bonus Action attack after a critical hit or reducing a creature to0HP; it does not print−5/+10. Define qualifying attack/weapon types versus two-handed description, same-turn timing, hostile-threat requirement and nonrecursive limits; no extra Bonus Action or external-feat imports.

### Final source decision

Retain the complete GC-29 proposal as explicitly NEW where supplied; Explicit two-handed melee completion from description, same-own-turnBA and no imported damage trade. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Preserve the two-handed mastery description as a qualification to the broad effect: NEW while using a melee weapon actually wielded in two hands, after your direct attack critically hits a meaningful hostile or reduces it from positiveHP to0, you may spend your availableBA before the same own turn ends for one attack with a melee weapon wielded in two hands. A Versatile two-hand use qualifies; no separate Heavy property is required. A legal ranged/thrown hit cannot qualify after releasing the weapon because it was not a melee two-handed attack. No−5/+10 is printed or added. If the attack both crits and drops, it still creates one entitlement; no extraBA. If Cleave/Frenzied Rage/Cleaving Momentum also trigger on that same event, use the proposed choose-one-derived-grant rule and pay the chosen cost. The derived attack cannot spawn further attack grants in its root. Off-turn criticals cannot bank a futureBA.

### Final authored examples

A two-handed quarterstaff critical can fund oneBA melee attack with a lawful two-hand weapon.

A one-handed sword critical does not qualify under this proposed description-bound scope; a crit-and-drop never grants twoBAs.

### Preserved submitted procedure

Preserve the two-handed mastery description as a qualification to the broad effect: NEW while using a melee weapon actually wielded in two hands, after your direct attack critically hits a meaningful hostile or reduces it from positiveHP to0, you may spend your availableBA before the same own turn ends for one attack with a melee weapon wielded in two hands. A Versatile two-hand use qualifies; no separate Heavy property is required. A legal ranged/thrown hit cannot qualify after releasing the weapon because it was not a melee two-handed attack. No−5/+10 is printed or added. If the attack both crits and drops, it still creates one entitlement; no extraBA. If Cleave/Frenzied Rage/Cleaving Momentum also trigger on that same event, use the proposed choose-one-derived-grant rule and pay the chosen cost. The derived attack cannot spawn further attack grants in its root. Off-turn criticals cannot bank a futureBA.

### Preserved submitted examples

A two-handed quarterstaff critical can fund oneBA melee attack with a lawful two-hand weapon.

A one-handed sword critical does not qualify under this proposed description-bound scope; a crit-and-drop never grants twoBAs.

## GC-30 — Hunter

### Original complete object

```json
{
  "id": "hunter",
  "name": "Hunter",
  "description": "You are skilled at tracking and hunting prey.",
  "prerequisite": "Wisdom 13+",
  "effect": "You gain proficiency in Survival and can track creatures across any terrain. You deal +2 damage to beasts and monstrosities.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Preserve Survival proficiency, tracking across terrain and+2damage to Beasts/Monstrosities. Bind independently documented creature types, eligible damage packets/attacks and crit behavior. Complete actual tracking evidence, time and DC without revealing hidden creature identity or inventing unsupported ecology.

### Final source decision

Retain the complete GC-30 proposal as explicitly NEW where supplied; Finite tracking method across real terrain, actual evidence/no-teleport rule and native-event damage scope. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Gain Survival proficiency, not expertise if already proficient. You may attempt tracking across any terrain when a real trail exists; NEW difficult medium, bare stone, water or air does not automatically make an actual passage untrackable, but no trail is created across teleportation or a source explicitly leaving none. Spend1minute at a real last-known trail location, WIS Survival DC15 for a trail within24hours, +5 if older than12hours and +5 if genuinely mixed/obscured; an explicitly sourced trail DC replaces this default. Success finds the next local direction/evidence, not the target's present location, identity or whole route. No unchanged free retry; changed evidence, new route segment or actual aid can support a new attempt. Add+2flat once per own direct damage event against an actual Beast or Monstrosity, of one native damage type before defenses; not per die, critical doubling, periodic/copy/transfer/reflection or companion-owned event. Actual target typing is decided from source facts without automatically disclosing it. This is distinct from Tracker/Wilderness features and grants no terrain movement immunity.

### Final authored examples

A real mixed trail16hours old usesDC25 under the default; success yields the next local direction, not a live target beacon.

A critical against a Beast adds2flat once. A summoned companion's own hit does not acquire its owner's Hunter damage.

### Preserved submitted procedure

Gain Survival proficiency, not expertise if already proficient. You may attempt tracking across any terrain when a real trail exists; NEW difficult medium, bare stone, water or air does not automatically make an actual passage untrackable, but no trail is created across teleportation or a source explicitly leaving none. Spend1minute at a real last-known trail location, WIS Survival DC15 for a trail within24hours, +5 if older than12hours and +5 if genuinely mixed/obscured; an explicitly sourced trail DC replaces this default. Success finds the next local direction/evidence, not the target's present location, identity or whole route. No unchanged free retry; changed evidence, new route segment or actual aid can support a new attempt. Add+2flat once per own direct damage event against an actual Beast or Monstrosity, of one native damage type before defenses; not per die, critical doubling, periodic/copy/transfer/reflection or companion-owned event. Actual target typing is decided from source facts without automatically disclosing it. This is distinct from Tracker/Wilderness features and grants no terrain movement immunity.

### Preserved submitted examples

A real mixed trail16hours old usesDC25 under the default; success yields the next local direction, not a live target beacon.

A critical against a Beast adds2flat once. A summoned companion's own hit does not acquire its owner's Hunter damage.

## GC-31 — Improved Alertness

### Original complete object

```json
{
  "id": "alertness_improved",
  "name": "Improved Alertness",
  "description": "Your senses are incredibly sharp.",
  "prerequisite": "Alertness feat",
  "effect": "You gain blindsense 10 feet and cannot be surprised while conscious.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Require exact Alertness feat, not Alert. Define blindsense10ft versus actual sight/blindsight, barriers/hidden detection and senses; preserve no Surprise while conscious. Resolve overlap with Blind Fight/Blind Fighting without silently treating all three named senses as identical.

### Final source decision

Retain the complete GC-31 proposal as explicitly NEW where supplied; Exact prerequisite,10ft location-only sense and conscious surprise suppression. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Requires the exact Alertness feat. NEW blindsense10ft is nonvisual location awareness: while conscious you pinpoint actual creature locations within10ft and line of effect, excluding total cover and explicit anti-detection blockers. It is not blindsight and does not meet can-see requirements, read objects/text, reveal type or identify illusions without an actual body. Hearing is not required under this explicit feat-only sense proposal. Actual Hidden location ends for you within that range, with Invisible's current known-position exception but unrelated darkness/unseen modifiers retained. While conscious, surprise restrictions are suppressed as in Alert; no extra actions or previous-turn recovery. Blind Fight may supply a broader30ft location sense independently, but no addition of their ranges and no promotion to sight.

### Final authored examples

Alert without Alertness cannot acquire this feat merely because their names resemble each other.

An invisible body5ft away is located, but a can-see spell remains unavailable without another qualifying sense.

### Preserved submitted procedure

Requires the exact Alertness feat. NEW blindsense10ft is nonvisual location awareness: while conscious you pinpoint actual creature locations within10ft and line of effect, excluding total cover and explicit anti-detection blockers. It is not blindsight and does not meet can-see requirements, read objects/text, reveal type or identify illusions without an actual body. Hearing is not required under this explicit feat-only sense proposal. Actual Hidden location ends for you within that range, with Invisible's current known-position exception but unrelated darkness/unseen modifiers retained. While conscious, surprise restrictions are suppressed as in Alert; no extra actions or previous-turn recovery. Blind Fight may supply a broader30ft location sense independently, but no addition of their ranges and no promotion to sight.

### Preserved submitted examples

Alert without Alertness cannot acquire this feat merely because their names resemble each other.

An invisible body5ft away is located, but a can-see spell remains unavailable without another qualifying sense.

## GC-32 — Inspiring Presence

### Original complete object

```json
{
  "id": "inspiring_presence",
  "name": "Inspiring Presence",
  "description": "After a critical hit, Charisma 14+ inspires allies with the listed damage increase for 10 seconds.",
  "prerequisite": "Charisma 14+",
  "effect": "When you score a critical hit, allies within 30 feet who can see or hear you gain +1 to attack rolls until the start of your next turn.",
  "type": "General",
  "legacyEffect": "+5% ally damage for 10s after crit",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

Reconcile legacy+5percent ally damage for10seconds with current+1attack rolls after a crit until owner next turn starts. Define genuine crit, ally30ft sight/hearing snapshot, reapplication, self inclusion and off-turn clocks. No damage multiplier or duplicated aura from multiple triggers unless explicitly approved.

### Final source decision

Keep actual source ally wording including self, with original target/sensory/budget conditions; no generalized automatic self-target for inherently two-person effects.

### Complete candidate procedure

After your direct attack critically hits a meaningful hostile, allied creatures within30ft that can actually see or hear you at that instant gain+1 to their attack rolls through your next original regular start. NEW recipients are fixed at the trigger, with no continuing range/hearing tether; allies entering later do not gain the old inspiration. No common language is required. You may be your own recipient when you meet the same actual seeing-or-hearing predicate. Any genuine critical-if-hit result qualifies, not just natural20; automatic-hit wording without a critical does not. Same-feat overlapping records never add beyond+1, and independent expiry records remain. Another legitimate critical can renew eligible allies but cannot duplicate the number. Preserve older+5%damage/10seconds as history; current effect is+1attack, not damage.
SOURCE SCOPE CORRECTION: “allies” includes the feat owner unless the actual clause says “other.” The owner must still meet the same hearing/perception, range, willing-target and action/resource predicates. No second body, observer or extra action is created by self-eligibility. This sentence supersedes any narrower owner-exclusion in the submitted proposal, not the preserved original.

### Final authored examples

A genuine personal critical fixes its actual eligible ally recipients, including the owner if they can see or hear the triggering presence. Each gains the single+1attack bonus until the owner’s next regular start; later entrants do not receive it retroactively.

Two inspiring owners grant one+1family layer to an ally; a later expiry can preserve that layer without making it+2.

### Preserved submitted procedure

After your direct attack critically hits a meaningful hostile, other allied creatures within30ft that can actually see or hear you at that instant gain+1 to their attack rolls through your next original regular start. NEW recipients are fixed at the trigger, with no continuing range/hearing tether; allies entering later do not gain the old inspiration. No common language is required. You are not your own recipient. Any genuine critical-if-hit result qualifies, not just natural20; automatic-hit wording without a critical does not. Same-feat overlapping records never add beyond+1, and independent expiry records remain. Another legitimate critical can renew eligible allies but cannot duplicate the number. Preserve older+5%damage/10seconds as history; current effect is+1attack, not damage.

### Preserved submitted examples

An adjacent ally who hears an off-turn critical keeps+1 until the owner's next regular start even after moving40ft away.

Two inspiring owners grant one+1family layer to an ally; a later expiry can preserve that layer without making it+2.

## GC-33 — Intimidating

### Original complete object

```json
{
  "id": "intimidating",
  "name": "Intimidating",
  "description": "Your presence strikes fear into others.",
  "prerequisite": "Charisma 13+ or Strength 15+",
  "effect": "You gain proficiency in Intimidation and can demoralize enemies in combat, causing them to have disadvantage on their next attack.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Preserve Intimidation proficiency and complete in-combat demoralization action, range, check/save, language/hearing/sight, duration and cadence. The source disadvantage applies to next attack; define expiration and repeats without adding universal Frightened or an unlimited action denial.

### Final source decision

Retain the complete GC-33 proposal as explicitly NEW where supplied; BA/30ft/contest, credible perceived threat, next-attack endpoint and no invented Frightened. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Gain Intimidation proficiency, not expertise if already proficient. NEW in combat spendBA to demoralize one hostile within30ft who perceives your audible or visible credible threat. Oppose your normal CHA Intimidation (STR only if an independently legal actual source permits that substitution) with targetWIS Insight. Higher wins, ties preserve state; no natural task shift. Success imposes disadvantage on its next attack roll before your next original regular start, consumed by that attack even if canceled or missed. One attempt per target per owner regular-turn interval; new successful applications refresh one family record, not a queue. No SR cap beyond realBA/cadence. Shared language is unnecessary for a plainly understood physical threat; an unperceivable or incomprehensible threat is ineligible. This is a distinct demoralization rider, not Frightened, forced loyalty, Charmed or whole-turn denial; immunity to fear alone does not automatically block it unless it expressly covers demoralization/intimidation.

### Final authored examples

Intimidation18 defeats Insight14: the foe's next attack has disadvantage, then the rider ends.

A creature behind opaque total cover with no audible/visible threat cannot be demoralized through this feature.

### Preserved submitted procedure

Gain Intimidation proficiency, not expertise if already proficient. NEW in combat spendBA to demoralize one hostile within30ft who perceives your audible or visible credible threat. Oppose your normal CHA Intimidation (STR only if an independently legal actual source permits that substitution) with targetWIS Insight. Higher wins, ties preserve state; no natural task shift. Success imposes disadvantage on its next attack roll before your next original regular start, consumed by that attack even if canceled or missed. One attempt per target per owner regular-turn interval; new successful applications refresh one family record, not a queue. No SR cap beyond realBA/cadence. Shared language is unnecessary for a plainly understood physical threat; an unperceivable or incomprehensible threat is ineligible. This is a distinct demoralization rider, not Frightened, forced loyalty, Charmed or whole-turn denial; immunity to fear alone does not automatically block it unless it expressly covers demoralization/intimidation.

### Preserved submitted examples

Intimidation18 defeats Insight14: the foe's next attack has disadvantage, then the rider ends.

A creature behind opaque total cover with no audible/visible threat cannot be demoralized through this feature.

## GC-34 — Lucky

### Original complete object

```json
{
  "id": "lucky",
  "name": "Lucky",
  "description": "You have inexplicable luck that seems to kick in at just the right moment.",
  "prerequisite": "None",
  "effect": "You have 3 luck points. Whenever you make an attack roll, ability check, or saving throw, you can spend one luck point to roll an additional d20",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Complete all missing procedures for three luck points: recovery, declaration before/after die/result, additional-d20 selection, interactions with advantage/disadvantage/replacements and one-event maximum. Source permits own attack/check/save only; no enemy reroll or guaranteed best-die rule is imported silently.

### Final source decision

Retain the complete GC-34 proposal as explicitly NEW where supplied; LR recovery, before-outcome window, optional one-position replacement with original selection rule and finite interaction ordering. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

NEW gain3luck points, initially full and restored to3 only on a completedLR; no overcap or conversion. On your own attack, ability/skill/tool check or save, after the initial d20 die/dice are visible but before the outcome and consequences are declared, spend at most1point to roll one additionald20. Choose either to keep the original dice unchanged or to replace one original die with the new face; then apply the roll's original normal/advantage/disadvantage selection over its original one/two positions. The added die is not a third freely best-kept die under disadvantage. Actual natural face is the final kept face; no source allows inventing an automatic result. It may affect an opposed check or death save because those are your checks/saves; it cannot reroll an enemy, a damage die, a flat result or a no-roll automatic failure. NEW one Lucky intervention per underlying roll event even if another rule later rerolls it. Resolve Elven Accuracy on initial eligible dice first, then Lucky; Elven Accuracy cannot reroll the added Lucky die. Other mandatory whole-roll replacements preserve their own order and consume the same event entitlement.

### Final authored examples

Disadvantage rolls3 and17; Lucky rolls12 and replaces3. Final disadvantage keeps12, not17.

An ordinary death save shows1 before its consequences. Lucky may replace it with the added die; it cannot be invoked after the failure/death has already resolved.

### Preserved submitted procedure

NEW gain3luck points, initially full and restored to3 only on a completedLR; no overcap or conversion. On your own attack, ability/skill/tool check or save, after the initial d20 die/dice are visible but before the outcome and consequences are declared, spend at most1point to roll one additionald20. Choose either to keep the original dice unchanged or to replace one original die with the new face; then apply the roll's original normal/advantage/disadvantage selection over its original one/two positions. The added die is not a third freely best-kept die under disadvantage. Actual natural face is the final kept face; no source allows inventing an automatic result. It may affect an opposed check or death save because those are your checks/saves; it cannot reroll an enemy, a damage die, a flat result or a no-roll automatic failure. NEW one Lucky intervention per underlying roll event even if another rule later rerolls it. Resolve Elven Accuracy on initial eligible dice first, then Lucky; Elven Accuracy cannot reroll the added Lucky die. Other mandatory whole-roll replacements preserve their own order and consume the same event entitlement.

### Preserved submitted examples

Disadvantage rolls3 and17; Lucky rolls12 and replaces3. Final disadvantage keeps12, not17.

An ordinary death save shows1 before its consequences. Lucky may replace it with the added die; it cannot be invoked after the failure/death has already resolved.

## GC-35 — Mage Slayer

### Original complete object

```json
{
  "id": "mage_slayer",
  "name": "Mage Slayer",
  "description": "You have practiced techniques for fighting spellcasters.",
  "prerequisite": "None",
  "effect": "When a creature within 5 feet casts a spell, you can use your reaction to make a melee weapon attack against that creature.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Define Reaction timing around an actually cast spell within5ft, awareness, reach, components and cast completion/interruption. Resolve reaction spells, teleporting caster and trigger visibility under source-qualified timing. No unprinted spell disruption, concentration disadvantage or save advantage.

### Final source decision

Retain the complete GC-35 proposal as explicitly NEW where supplied; Post-spell timing, actual perception and legal target recheck; no unprinted counterspell. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

When a creature within5ft actually casts a spell and you can perceive the casting event, you may spendReaction for one legal melee weapon attack against it. NEW this reaction occurs after that spell fully resolves or is negated, not in its interruption window. Range/reach/line/perception and your capability must still hold at reaction resolution. A caster that teleports away, becomes untargetable, incapacitates you, or kills you can leave no legal attack. V/S or another actually perceptible magical cue can reveal casting; no automatic detection of fully imperceptible casting is granted. Reaction spells qualify as real casts, but the attack does not itself repeat casting or grant a newReaction. Readied spells trigger at actual preparation/casting, not a second time on held release. A damaging hit can cause ordinary concentration consequences afterward but does not retroactively negate the completed spell. No generic spell-save advantage or concentration disadvantage.

### Final authored examples

A nearby caster completes a self-buff and remains in reach: an availableReaction can attack afterward.

A nearby teleport resolves to30ft away. The caster is no longer in melee reach, so Mage Slayer cannot deliver the attack or cancel the teleport.

### Preserved submitted procedure

When a creature within5ft actually casts a spell and you can perceive the casting event, you may spendReaction for one legal melee weapon attack against it. NEW this reaction occurs after that spell fully resolves or is negated, not in its interruption window. Range/reach/line/perception and your capability must still hold at reaction resolution. A caster that teleports away, becomes untargetable, incapacitates you, or kills you can leave no legal attack. V/S or another actually perceptible magical cue can reveal casting; no automatic detection of fully imperceptible casting is granted. Reaction spells qualify as real casts, but the attack does not itself repeat casting or grant a newReaction. Readied spells trigger at actual preparation/casting, not a second time on held release. A damaging hit can cause ordinary concentration consequences afterward but does not retroactively negate the completed spell. No generic spell-save advantage or concentration disadvantage.

### Preserved submitted examples

A nearby caster completes a self-buff and remains in reach: an availableReaction can attack afterward.

A nearby teleport resolves to30ft away. The caster is no longer in melee reach, so Mage Slayer cannot deliver the attack or cancel the teleport.

## GC-36 — Magic Initiate

### Original complete object

```json
{
  "id": "magicInitiate",
  "name": "Magic Initiate",
  "description": "Choose a class: bard, cleric, druid, sorcerer, warlock, or wizard. You learn magic from that class.",
  "prerequisite": "None",
  "effect": "Learn two cantrips and one 1st-level spell from chosen class. You can cast the spell once per long rest",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Reconcile generic class-choice feat with six separately named Magic Initiate sources. Bind two cantrips and one class-rank1 spell, ability/DC/PB, acquisition/components and once-Long-Rest free or paid resource treatment. Actual Sorcerer/Warlock lists are absent; do not alias Mage or grant unrestricted repertoire/casting slots.

### Final source decision

Explicitly adopt the finite16 curricula, including separately labeled feat-only Sorcerer/Warlock choices; retain actual class placement and one curriculum across generic/named feats, no class or RP grant.

### Complete candidate procedure

NEW expand the original six-name curriculum choice to the finite16-option table below; this conference explicitly adopts that NEW bounded expansion for candidate authorship. At acquisition choose permanently one curriculum:14 actual current class-rank0/rank1 lists or the explicitly NEW Sorcerer/Warlock feat-only lists retained from Core Magic. Choose two distinct rank0 identities and one rank1 identity from that curriculum, preserving exact class placement/school/mode. Source1st-level means rank1 here, not another game's spell slot. Use the table's explicit casting ability, normal totalPB, spell attackPB+ability andDC8+PB+ability. The feat supplies these named grant ranks independently of class level but no class features, ordinary repertoire/prepared slot, RPpool, class level or RC. Rank0 uses actual action/cadence with no generic scaling; rank1 gets one charge per completedLR. Use the final FS-09 classless feat-casting contract: normal rankRPprice waived, independent effect/material costs retained, real components/focus/hands, concentration/interruption, shared Dissonance/Refrain and rankedLimit+6block, and total character level only for an explicitly numeric spell-payload class-level variable. Unfinished chosen spell payloads stay inactive pending their actual review. NEW one copy of each curriculum across generic and named Magic Initiate identities; acquiring genericBard when namedBard is owned is invalid, rather than a second daily charge. Generic feat itself is nonrepeatable; separately named other curricula may be selected with actual separate feat choices. No class alias is created by the two legacy labels.

### Final authored examples

GenericMage selects two actual Mage rank0 rows and one Mage rank1 row, usingINT without acquiring Mage class levels orRP.

A namedWizard initiate cannot add genericWizard for a duplicate rank1charge; genericCleric is a different curriculum if legally selected instead.

### Preserved submitted procedure

NEW expand the original six-name curriculum choice to the finite16-option table below; this expansion requires explicit joint approval. At acquisition choose permanently one curriculum:14 actual current class-rank0/rank1 lists or the explicitly NEW Sorcerer/Warlock feat-only lists retained from Core Magic. Choose two distinct rank0 identities and one rank1 identity from that curriculum, preserving exact class placement/school/mode. Source1st-level means rank1 here, not another game's spell slot. Use the table's explicit casting ability, normal totalPB, spell attackPB+ability andDC8+PB+ability. The feat supplies these named grant ranks independently of class level but no class features, ordinary repertoire/prepared slot, RPpool, class level or RC. Rank0 uses actual action/cadence with no generic scaling; rank1 gets one charge per completedLR. Retain Core Magic's entire proposed classless casting contract: normal rankRPprice waived, independent effect/material costs retained, real components/focus/hands, concentration/interruption, shared Dissonance/Refrain and rankedLimit+6block, and total character level only for an explicitly numeric spell-payload class-level variable. Unfinished chosen spell payloads stay inactive pending their actual review. NEW one copy of each curriculum across generic and named Magic Initiate identities; acquiring genericBard when namedBard is owned is invalid, rather than a second daily charge. Generic feat itself is nonrepeatable; separately named other curricula may be selected with actual separate feat choices. No class alias is created by the two legacy labels.

### Preserved submitted examples

GenericMage selects two actual Mage rank0 rows and one Mage rank1 row, usingINT without acquiring Mage class levels orRP.

A namedWizard initiate cannot add genericWizard for a duplicate rank1charge; genericCleric is a different curriculum if legally selected instead.

## GC-37 — Martial Adept

### Original complete object

```json
{
  "id": "martialAdept",
  "name": "Martial Adept",
  "description": "You have martial training that allows you to perform special combat maneuvers.",
  "prerequisite": "None",
  "effect": "Learn two maneuvers from the Battle Master archetype, gain one superiority die (d6)",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Source invokes Battle Master archetype and one superiority d6 without a supplied maneuver menu or recovery. Establish actual current class/source identity, finite two-choice maneuver definitions, action/trigger/DC/target/range and consumption/recharge. Do not import external5e maneuvers or assume the Soldier card is the same resource.

### Final source decision

Retain the complete GC-37 proposal as explicitly NEW where supplied; Explicit NEW six-maneuver feat menu, two permanent choices and oneSRd6 pool. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

The literal Battle Master archetype/superiority-die source has no matching current class-card menu. NEW use the six feat-only maneuver definitions below, each fully specified from existing ordinary actions with a finite die spend. At acquisition permanently choose two different maneuverIDs; gain a separate pool of one superiorityd6, initially available and recovered on completedSR orLR. One die can fund only one declared maneuver on one event; noRP/RC/class-resource exchange or conversion. All maneuvers pay their own actual Action/BA/Reaction or attack-replacement timing, with ordinary target/body legality. A committed attempt spends its die even on miss/failure/countering; illegal attempts spend nothing. The rolled result is used only as the selected maneuver states, not free damage on every maneuver. It grants no Soldier Coordinated Maneuver, class levels or Battle Master subclass. Choices cannot be changed for free at rest.

### Final authored examples

Choose Measured Strike and Guarding Deflection; spending the one die on either leaves none for the other before a legal rest.

A Soldier's independent resource cannot be spent as this superiority die, nor does the feat acquire Coordinated Maneuver.

### Preserved submitted procedure

The literal Battle Master archetype/superiority-die source has no matching current class-card menu. NEW use the six feat-only maneuver definitions below, each fully specified from existing ordinary actions with a finite die spend. At acquisition permanently choose two different maneuverIDs; gain a separate pool of one superiorityd6, initially available and recovered on completedSR orLR. One die can fund only one declared maneuver on one event; noRP/RC/class-resource exchange or conversion. All maneuvers pay their own actual Action/BA/Reaction or attack-replacement timing, with ordinary target/body legality. A committed attempt spends its die even on miss/failure/countering; illegal attempts spend nothing. The rolled result is used only as the selected maneuver states, not free damage on every maneuver. It grants no Soldier Coordinated Maneuver, class levels or Battle Master subclass. Choices cannot be changed for free at rest.

### Preserved submitted examples

Choose Measured Strike and Guarding Deflection; spending the one die on either leaves none for the other before a legal rest.

A Soldier's independent resource cannot be spent as this superiority die, nor does the feat acquire Coordinated Maneuver.

## GC-38 — Martial Adept (Advanced)

### Original complete object

```json
{
  "id": "martial_adept_advanced",
  "name": "Martial Adept (Advanced)",
  "description": "You have advanced martial training.",
  "prerequisite": "Martial Adept feat",
  "effect": "You learn two additional maneuvers and gain one more superiority die.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Require exact Martial Adept and its completed maneuver/die procedure. Define two distinct extra choices, one additional die size and common recovery/cap, duplicate choices and retraining. Do not make this missing dependency playable by inventing an unrelated class archetype.

### Final source decision

Retain the complete GC-38 proposal as explicitly NEW where supplied; Exact dependency, four distinct choices, common2d6 capacity and one-maneuver-per-event. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Require exact martialAdept. Choose two additional distinct entries from that same six-maneuver menu, excluding the two already known; permanent choices. Increase the common feat superiority pool capacity by one die of the same sized6, for two total; NEW the newly granted die begins available on actual acquisition, not each rest or retarget. CompletedSR/LR restores the shared pool to its current capacity once. Known maneuver count becomes four, not four copies of one option. No larger die, additional class resource, extraAction, simultaneous multiple-die payment or free retraining. Same underlying event may still use at most one superiority maneuver unless a future expressly priced source overrides it.

### Final authored examples

Adept knew two maneuvers; Advanced chooses two others and now has four with a two-die shared pool.

It cannot spend two dice to double Measured Strike's bonus on one attack or recharge each feat as independent extra pools.

### Preserved submitted procedure

Require exact martialAdept. Choose two additional distinct entries from that same six-maneuver menu, excluding the two already known; permanent choices. Increase the common feat superiority pool capacity by one die of the same sized6, for two total; NEW the newly granted die begins available on actual acquisition, not each rest or retarget. CompletedSR/LR restores the shared pool to its current capacity once. Known maneuver count becomes four, not four copies of one option. No larger die, additional class resource, extraAction, simultaneous multiple-die payment or free retraining. Same underlying event may still use at most one superiority maneuver unless a future expressly priced source overrides it.

### Preserved submitted examples

Adept knew two maneuvers; Advanced chooses two others and now has four with a two-die shared pool.

It cannot spend two dice to double Measured Strike's bonus on one attack or recharge each feat as independent extra pools.

## GC-39 — Mobile

### Original complete object

```json
{
  "id": "mobile",
  "name": "Mobile",
  "description": "You are exceptionally speedy and agile.",
  "prerequisite": "None",
  "effect": "Your speed increases by 10 feet and you don't provoke opportunity attacks from creatures you've attacked this turn.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Define which Speed increases by10ft under current movement-mode rules and exact same-turn attacks that prevent opportunity attacks from that target. Does hit/miss, spell/weapon, melee/ranged or forced targeting matter? Preserve the source wording pending decision; no automatic Dash terrain immunity or teleport.

### Final source decision

Retain the complete GC-39 proposal as explicitly NEW where supplied; Existing-mode Speed completion, broad actual-attack scope and per-target current-turn immunity. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

NEW add10ft to each existing Speed mode, except a mode expressly derived as equal to another uses that already-modified value and gets no second addition. Grant no new movement mode. Each creature you personally attack on your own turn cannot make opportunity attacks provoked by your voluntary movement for the rest of that actual turn, whether your attack hit or missed. Retain the source's broad attack wording: weapon/natural/unarmed/spell and melee/ranged attacks qualify; a save-only effect does not. Source attack must actually be directed at that creature, not an arbitrary empty-square guess proven empty, copied hit or companion attack. No action cost beyond the actual attack/movement; maintain a set of actual attacked identities, not only one. It suppresses only those creatures' opportunity attacks, not other Reactions or later-turn attacks. No Dash terrain immunity or teleport.

### Final authored examples

A missed thrown dagger attack still protects this turn's movement from that actual target's opportunity attacks.

A fireball-like save effect is not an attack, so it creates no Mobile target immunity; difficult terrain still costs extra.

### Preserved submitted procedure

NEW add10ft to each existing Speed mode, except a mode expressly derived as equal to another uses that already-modified value and gets no second addition. Grant no new movement mode. Each creature you personally attack on your own turn cannot make opportunity attacks provoked by your voluntary movement for the rest of that actual turn, whether your attack hit or missed. Retain the source's broad attack wording: weapon/natural/unarmed/spell and melee/ranged attacks qualify; a save-only effect does not. Source attack must actually be directed at that creature, not an arbitrary empty-square guess proven empty, copied hit or companion attack. No action cost beyond the actual attack/movement; maintain a set of actual attacked identities, not only one. It suppresses only those creatures' opportunity attacks, not other Reactions or later-turn attacks. No Dash terrain immunity or teleport.

### Preserved submitted examples

A missed thrown dagger attack still protects this turn's movement from that actual target's opportunity attacks.

A fireball-like save effect is not an attack, so it creates no Mobile target immunity; difficult terrain still costs extra.

## GC-40 — Mounted Combatant

### Original complete object

```json
{
  "id": "mounted_combatant",
  "name": "Mounted Combatant",
  "description": "You are a dangerous foe to face while mounted.",
  "prerequisite": "None",
  "effect": "You have advantage on melee attack rolls against unmounted creatures smaller than your mount.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Preserve advantage only on melee attack rolls against unmounted creatures smaller than actual mount. Define legal mount/rider control, size snapshot and attack eligibility, with no unprinted mount protection, damage redirection or immunity. Compare Cavalry broader source without automatic identity merging.

### Final source decision

Adopt the bounded proposal with the completed EX58 controller/phase/physical-history interface; no future transport dependency or extra animal turn.

### Complete candidate procedure

While you are actually legally mounted, gain advantage on your melee attack rolls against creatures that are unmounted and smaller than the actual ridden mount at resolution. Include melee weapon, natural, unarmed and actual melee spell attacks; no ranged or save-only effect. Use real mount/target sizes, not rider size, names or desired posture. Other disadvantage cancels normally. This grants no mount, proficiency/control, target redirection, mount save evasion, immunity, extra action or shared turn. Cavalry's broader advantage is separate, but two sources still roll only two dice. The completed EX58 transport rules govern actual mounting, movement, custody and eligibility.
NEW explicit EX58 interface: retain one real creature identity and one current control/phase record. Riding, bonding or transferring custody does not clone a turn, movement budget, Reaction, attack allowance, body or resource pool. An attached companion acts in its source-defined phase after the owner’s regular turn; a controlled mount uses EX58’s actual mounted-phase procedure. A body fitting both roles elects one compatible route before that round’s work, preserves all already-spent allowances and cannot switch routes to gain a second phase. Its actual load, tack, rider geometry, mounting/dismounting cost and ordinary independent temperament remain. One shared Bonus Action command and one offensive companion action per owner per numbered round apply where those source engines impose them. This feat supplies no blanket override of a specific engine’s attack or no-resource restrictions.

### Final authored examples

On a Large mount, melee attacks against an unmountedMedium foe have advantage.

An unmountedLarge foe is not smaller than that mount; this feat gives no advantage, even though Cavalry might independently do so.

### Preserved submitted procedure

While you are actually legally mounted, gain advantage on your melee attack rolls against creatures that are unmounted and smaller than the actual ridden mount at resolution. Include melee weapon, natural, unarmed and actual melee spell attacks; no ranged or save-only effect. Use real mount/target sizes, not rider size, names or desired posture. Other disadvantage cancels normally. This grants no mount, proficiency/control, target redirection, mount save evasion, immunity, extra action or shared turn. Cavalry's broader advantage is separate, but two sources still roll only two dice. Pending full transport rules govern mounting, movement, custody and actual eligibility.

### Preserved submitted examples

On a Large mount, melee attacks against an unmountedMedium foe have advantage.

An unmountedLarge foe is not smaller than that mount; this feat gives no advantage, even though Cavalry might independently do so.

## GC-41 — Natural Leader

### Original complete object

```json
{
  "id": "natural_leader",
  "name": "Natural Leader",
  "description": "A Charisma 13+ leader steadies nearby allies with the feat's listed +1 morale.",
  "prerequisite": "Charisma 13+",
  "effect": "Allies within 10 feet who can hear you gain +1 on morale and fear saves while you are conscious.",
  "type": "General",
  "legacyEffect": "+1 morale to nearby allies",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

Define conscious aura, allies within10ft who hear, self inclusion, and exact morale/fear save procedures. No new save is created merely to apply+1. Resolve continuous versus snapshot eligibility, multiple leaders and hard-control/compulsion boundaries without forced loyalty.

### Final source decision

Keep actual source ally wording including self, with original target/sensory/budget conditions; no generalized automatic self-target for inherently two-person effects.

### Complete candidate procedure

While conscious and capable of audible direction, allied creatures within10ft who can actually hear you gain+1 on real morale saves and saves against effects that actually impose fear/Frightened. NEW no common language is required for this rallying presence, but silence, Deafened and sound-blocking barriers can prevent hearing. Check current radius/hearing when each save occurs; leaving ends the benefit without an expiry timer. It applies only to saves the actual source calls for: do not invent a morale save, turn an ordinary persuasion check into one, compel loyalty or prevent voluntary withdrawal. Same-feat multiple leaders give at most+1; a separately sourced actual bonus follows its own family. You are an eligible ally when you can actually hear your own rallying presence.
SOURCE SCOPE CORRECTION: “allies” includes the feat owner unless the actual clause says “other.” The owner must still meet the same hearing/perception, range, willing-target and action/resource predicates. No second body, observer or extra action is created by self-eligibility. This sentence supersedes any narrower owner-exclusion in the submitted proposal, not the preserved original.

### Final authored examples

A conscious holder able to hear their own rallying presence gains the same+1 on an actual fear/morale save as a qualifying ally within10ft. Silence or Deafened can defeat hearing; no morale save is invented.

An ally decides to retreat voluntarily: the aura does not force a morale check or take away that decision.

### Preserved submitted procedure

While conscious and capable of audible direction, other allied creatures within10ft who can actually hear you gain+1 on real morale saves and saves against effects that actually impose fear/Frightened. NEW no common language is required for this rallying presence, but silence, Deafened and sound-blocking barriers can prevent hearing. Check current radius/hearing when each save occurs; leaving ends the benefit without an expiry timer. It applies only to saves the actual source calls for: do not invent a morale save, turn an ordinary persuasion check into one, compel loyalty or prevent voluntary withdrawal. Same-feat multiple leaders give at most+1; a separately sourced actual bonus follows its own family. You are not your own ally for this feature.

### Preserved submitted examples

An ally8ft away hearing the leader adds1 to a genuine fear save.

An ally decides to retreat voluntarily: the aura does not force a morale check or take away that decision.

## GC-42 — Night Hunter

### Original complete object

```json
{
  "id": "night_hunter",
  "name": "Night Hunter",
  "description": "A watchful hunter with Wisdom 12+ gains or extends darkvision as the feat lists.",
  "prerequisite": "Wisdom 12+",
  "effect": "Gain darkvision to 60 feet. If you already have darkvision, increase its range by 30 feet.",
  "type": "General",
  "legacyEffect": "Gain darkvision or extend it",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

Retain60ft darkvision or+30ft existing range. Define acquisition versus dynamic current-source range, multiple darkvision sources, actual form senses and suppression. Do not grant magical-darkness sight, color/detail beyond normal darkvision or additive stacking from repeatedly changing form.

### Final source decision

Retain the complete GC-42 proposal as explicitly NEW where supplied; Fixed acquisition mode, dynamic underlying-range extension and ordinary visual limits. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

At acquisition record whether the character has an actual independent darkvision source. NEW if none, this feat grants60ft ordinary darkvision. If one exists, instead record a permanent+30ft extension to the current strongest operative independent darkvision range; that mode adds no vision when every underlying source is suppressed/absent. Preserve the acquisition mode when forms/sources later change; no repeated+30 from toggling forms, reacquisition or multiple base ranges. A60ft-grant mode and later independent120ft darkvision use the strongest base120, not180; extension mode on120 becomes150. Ordinary darkvision sees dim light as bright and darkness as dim within range, without color in darkness; eyes/anatomy and Blinded still matter. Magical darkness, total cover and explicit blockers remain unless a separate source defeats them. It is not blindsight or general invisibility detection.

### Final authored examples

A character already possessing60ft darkvision acquires extension mode and reaches90ft.

Changing to a form with no usable underlying darkvision does not manufacture30ft in extension mode or bank another+30 on returning.

### Preserved submitted procedure

At acquisition record whether the character has an actual independent darkvision source. NEW if none, this feat grants60ft ordinary darkvision. If one exists, instead record a permanent+30ft extension to the current strongest operative independent darkvision range; that mode adds no vision when every underlying source is suppressed/absent. Preserve the acquisition mode when forms/sources later change; no repeated+30 from toggling forms, reacquisition or multiple base ranges. A60ft-grant mode and later independent120ft darkvision use the strongest base120, not180; extension mode on120 becomes150. Ordinary darkvision sees dim light as bright and darkness as dim within range, without color in darkness; eyes/anatomy and Blinded still matter. Magical darkness, total cover and explicit blockers remain unless a separate source defeats them. It is not blindsight or general invisibility detection.

### Preserved submitted examples

A character already possessing60ft darkvision acquires extension mode and reaches90ft.

Changing to a form with no usable underlying darkvision does not manufacture30ft in extension mode or bank another+30 on returning.

## GC-43 — Orcish Fury

### Original complete object

```json
{
  "id": "orcish_fury",
  "name": "Orcish Fury",
  "description": "Your orcish blood burns with fury.",
  "prerequisite": "Half-orc or orc",
  "effect": "When you hit with an attack using a simple or martial weapon, you can roll one of the weapon's damage dice one additional time.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Preserve Half-orc or Orc prerequisite without silently inventing a half-orc base. Define one additional actual weapon die on a simple/martial weapon hit, declaration, cadence/use recovery, critical interaction and multi-die weapons. No added ability modifier, entire damage reroll or unlimited presumed off-turn uses without decision.

### Final source decision

Retain the complete GC-43 proposal as explicitly NEW where supplied; OneSR charge, on-hit pre-damage commitment, base-die selection and critical treatment. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Require actual Orc or independently sourced half-orc ancestry; no missing half-orc alias is invented. NEW once perSR, after your personal attack with a Simple or Martial weapon hits and before rolling damage, spend the use to add one die of that actual weapon's base damage expression. A2d6 weapon adds1d6; use the actual one/two-handed Versatile die selected for the hit. Critical doubles this added attack die with other noncritical-only weapon dice. No ability modifier is added again, and fixed/no-die profiles cannot provide a die. Thrown use qualifies if the weapon is actually Simple/Martial. Natural/unarmed attacks qualify only if independently classified as a Simple/Martial weapon. Source immunity or0damage does not refund the committed use; no additional ancestry endurance or attack is granted.

### Final authored examples

A2d6 greatsword ordinary hit gains1d6, totaling3d6 before modifiers.

On a critical with that weapon, the added die doubles too for6d6 total; the STR modifier is still added only once.

### Preserved submitted procedure

Require actual Orc or independently sourced half-orc ancestry; no missing half-orc alias is invented. NEW once perSR, after your personal attack with a Simple or Martial weapon hits and before rolling damage, spend the use to add one die of that actual weapon's base damage expression. A2d6 weapon adds1d6; use the actual one/two-handed Versatile die selected for the hit. Critical doubles this added attack die with other noncritical-only weapon dice. No ability modifier is added again, and fixed/no-die profiles cannot provide a die. Thrown use qualifies if the weapon is actually Simple/Martial. Natural/unarmed attacks qualify only if independently classified as a Simple/Martial weapon. Source immunity or0damage does not refund the committed use; no additional ancestry endurance or attack is granted.

### Preserved submitted examples

A2d6 greatsword ordinary hit gains1d6, totaling3d6 before modifiers.

On a critical with that weapon, the added die doubles too for6d6 total; the STR modifier is still added only once.

## GC-44 — Piercer

### Original complete object

```json
{
  "id": "piercer",
  "name": "Piercer",
  "description": "You are adept at dealing piercing damage.",
  "prerequisite": "Dexterity 13 or higher",
  "effect": "When you hit with a piercing weapon, you can reroll one damage die and critical hits add an extra damage die.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Define one piercing-weapon damage-die reroll and mandatory/optional new result, timing/cadence and critical additional die selection. Distinguish weapon base die from riders, natural attacks and spells; avoid reroll loops or copying a single die into separate packets.

### Final source decision

Retain the complete GC-44 proposal as explicitly NEW where supplied; Once-turn mandatory-result reroll, actual weapon pool and one post-critical additional die. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

NEW once per turn, after rolling damage for a personal hit with a weapon whose native type includes piercing, you may reroll one actual piercing base-weapon die and must keep its new face. Choose from native weapon dice including critical copies and expressly additional weapon dice, not poison/Smite/spell rider dice. One Piercer reroll per event/turn; no repeated loop. Separately, every critical hit with that piercing weapon adds one additional die of its actual base weapon expression after ordinary critical doubling; this critical-specific die is not doubled again. For a2d6 weapon choose one d6. A natural weapon requires an actual piercing weapon profile; save-only spells and a nonpiercing weapon with an attached piercing rider do not qualify. NEW if Savage Attacker also applies, resolve its whole-pool choice first, then Piercer on one die of the kept pool; no return to a discarded pool. All source-specific reroll limits remain.

### Final authored examples

A rapier critical normally rolls2d8; Piercer adds one mored8 for3d8, not4d8.

A rerolled1 that becomes1 must remain1; the feat cannot reroll again until another qualifying turn allowance.

### Preserved submitted procedure

NEW once per turn, after rolling damage for a personal hit with a weapon whose native type includes piercing, you may reroll one actual piercing base-weapon die and must keep its new face. Choose from native weapon dice including critical copies and expressly additional weapon dice, not poison/Smite/spell rider dice. One Piercer reroll per event/turn; no repeated loop. Separately, every critical hit with that piercing weapon adds one additional die of its actual base weapon expression after ordinary critical doubling; this critical-specific die is not doubled again. For a2d6 weapon choose one d6. A natural weapon requires an actual piercing weapon profile; save-only spells and a nonpiercing weapon with an attached piercing rider do not qualify. NEW if Savage Attacker also applies, resolve its whole-pool choice first, then Piercer on one die of the kept pool; no return to a discarded pool. All source-specific reroll limits remain.

### Preserved submitted examples

A rapier critical normally rolls2d8; Piercer adds one mored8 for3d8, not4d8.

A rerolled1 that becomes1 must remain1; the feat cannot reroll again until another qualifying turn allowance.

## GC-45 — Polearm Master

### Original complete object

```json
{
  "id": "polearm_master",
  "name": "Polearm Master",
  "description": "You have mastered polearms and similar weapons.",
  "prerequisite": "Strength 13 or higher",
  "effect": "When you wield a glaive, halberd, pike, or quarterstaff, you can make opportunity attacks when creatures enter your reach.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Use exact source glaive,halberd,pike,quarterstaff list. Complete entry-into-reach opportunity Reaction timing, actual weapon wielding/reach and voluntary/forced/teleport movement rules. Preserve pike inclusion; do not import an unprinted butt-end Bonus Action attack or extra Reaction.

### Final source decision

Retain the complete GC-45 proposal as explicitly NEW where supplied; Exact four-weapon list and voluntary seen-hostile entry timing, without external BA attack. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

While actually wielding a usable glaive, halberd, pike or quarterstaff with its required hands, when a seen hostile creature voluntarily crosses from outside to inside that weapon's ordinary current melee reach, you may spendReaction for one opportunity attack with that weapon immediately after entry. Retain pike explicitly. No creature appears/teleports/is forced into reach trigger, no trigger from your own movement or reach growth, and no trigger for merely beginning inside. Disengage and other actual opportunity immunity apply. Use the chosen weapon's real reach, not a universal10ft; quarterstaff ordinarily remains5ft. It grants no butt-end BA attack, damage die, new proficiency or additionalReaction. Multiple entry-trigger feats offer one eligible attack on the same event under the proposed extra-Reaction event guard.

### Final authored examples

A seen hostile walks into a pike's real10ft reach; an availableReaction can attack.

A quarterstaff wielder does not gain10ft reach merely from this feat, and a forced push into5ft does not trigger.

### Preserved submitted procedure

While actually wielding a usable glaive, halberd, pike or quarterstaff with its required hands, when a seen hostile creature voluntarily crosses from outside to inside that weapon's ordinary current melee reach, you may spendReaction for one opportunity attack with that weapon immediately after entry. Retain pike explicitly. No creature appears/teleports/is forced into reach trigger, no trigger from your own movement or reach growth, and no trigger for merely beginning inside. Disengage and other actual opportunity immunity apply. Use the chosen weapon's real reach, not a universal10ft; quarterstaff ordinarily remains5ft. It grants no butt-end BA attack, damage die, new proficiency or additionalReaction. Multiple entry-trigger feats offer one eligible attack on the same event under the proposed extra-Reaction event guard.

### Preserved submitted examples

A seen hostile walks into a pike's real10ft reach; an availableReaction can attack.

A quarterstaff wielder does not gain10ft reach merely from this feat, and a forced push into5ft does not trigger.

## GC-46 — Savage Attacker

### Original complete object

```json
{
  "id": "savage_attacker",
  "name": "Savage Attacker",
  "description": "You fight with primal ferocity.",
  "prerequisite": "None",
  "effect": "Once per turn when you roll damage for a melee weapon attack, you can reroll the damage dice and use either total.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Define once-per-turn scope on/off owner turn and reroll of melee-weapon damage dice, choosing either whole total. Identify which base/rider/critical dice are in the pool, timing before damage consequences and no mixing best individual dice or repeat rerolls.

### Final source decision

Retain the complete GC-46 proposal as explicitly NEW where supplied; Explicit weapon-only full-pool scope, whole-result choice, per-type provenance and reroll ordering. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Once per turn when you roll damage for your actual melee weapon attack, after seeing that roll but before consequences, reroll the entire eligible native weapon-dice pool once and choose either the complete original total or complete new total. NEW eligible pool includes base weapon dice, their critical copies and expressly additional weapon dice from feats such as Draw Cut, Orcish Fury or Piercer; exclude separate spell/Smite/poison/elemental rider dice and flat modifiers. Preserve each die's native type and apply the chosen corresponding per-type totals, not a pooled total reassigned to a preferred type. Never mix the best die from each pool or reroll only unfavorable dice through this feature. Roll once for each original die identity in the chosen pool, not new attacks or damage events. Maximized/fixed numeric damage has no rolled pool to reroll. Resolve Savage Attacker before Piercer's one-die adjustment if both are used; after selecting a pool you cannot return to a discarded pool to optimize a later modifier. Own and off-turn regular-turn allowances follow the shared cadence.

### Final authored examples

A2d6 pool rolls2+6=8 and rerolls5+1=6. Choose8 or6, never6+5=11.

A separate poison2d6 rider remains its original roll; Savage Attacker does not reroll it just because it accompanied the melee hit.

### Preserved submitted procedure

Once per turn when you roll damage for your actual melee weapon attack, after seeing that roll but before consequences, reroll the entire eligible native weapon-dice pool once and choose either the complete original total or complete new total. NEW eligible pool includes base weapon dice, their critical copies and expressly additional weapon dice from feats such as Draw Cut, Orcish Fury or Piercer; exclude separate spell/Smite/poison/elemental rider dice and flat modifiers. Preserve each die's native type and apply the chosen corresponding per-type totals, not a pooled total reassigned to a preferred type. Never mix the best die from each pool or reroll only unfavorable dice through this feature. Roll once for each original die identity in the chosen pool, not new attacks or damage events. Maximized/fixed numeric damage has no rolled pool to reroll. Resolve Savage Attacker before Piercer's one-die adjustment if both are used; after selecting a pool you cannot return to a discarded pool to optimize a later modifier. Own and off-turn regular-turn allowances follow the shared cadence.

### Preserved submitted examples

A2d6 pool rolls2+6=8 and rerolls5+1=6. Choose8 or6, never6+5=11.

A separate poison2d6 rider remains its original roll; Savage Attacker does not reroll it just because it accompanied the melee hit.

## GC-47 — Sentinel

### Original complete object

```json
{
  "id": "sentinel",
  "name": "Sentinel",
  "description": "You excel at locking down enemies.",
  "prerequisite": "None",
  "effect": "When you hit a creature with an opportunity attack, the creature's speed becomes 0 for the rest of the turn.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Preserve source opportunity-hit sets target Speed0 for rest of that turn. Bind actual hit, movement modes, earliest endpoint, forced movement/falling and other speed priorities. Do not import bypass-Disengage or attacks on allies absent from this source; no automatic full-turn action denial.

### Final source decision

Retain the complete GC-47 proposal as explicitly NEW where supplied; All-mode0 and current-enclosing-turn endpoint; ordinary opportunity-hit identity. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

When your actual opportunity attack hits a creature, set all its current Speed modes to0 for the rest of the actual turn containing that event. NEW the endpoint is that enclosing turn's end, including an actual extra-turn end, not the target's next future turn; outside initiative use the remainder of the current6second interval. The hit qualifies even if damage is0. This overrides ordinary positive Speed additions during the interval and preserves spent movement cost; ending it restores otherwise-current Speed without refunding cost. It stops subsequent voluntary Speed expenditure, but not independently legal forced movement or teleport. A flying creature withSpeed0 follows existing Falling/hover/support rules, not immediate invented fall damage. Disengage still prevents the opportunity trigger. A Reaction attack that is not an opportunity attack, or Combat Casting's replacement spell, does not qualify. No ally-attack trigger, extraReaction or bypass of condition defenses is granted.

### Final authored examples

An opportunity hit during an enemy's movement setsSpeed0 through that enemy turn's end, preventing later ordinary movement.

An independently legal teleport can still move the target; Sentinel does not turn0Speed into a teleport prohibition.

### Preserved submitted procedure

When your actual opportunity attack hits a creature, set all its current Speed modes to0 for the rest of the actual turn containing that event. NEW the endpoint is that enclosing turn's end, including an actual extra-turn end, not the target's next future turn; outside initiative use the remainder of the current6second interval. The hit qualifies even if damage is0. This overrides ordinary positive Speed additions during the interval and preserves spent movement cost; ending it restores otherwise-current Speed without refunding cost. It stops subsequent voluntary Speed expenditure, but not independently legal forced movement or teleport. A flying creature withSpeed0 follows existing Falling/hover/support rules, not immediate invented fall damage. Disengage still prevents the opportunity trigger. A Reaction attack that is not an opportunity attack, or Combat Casting's replacement spell, does not qualify. No ally-attack trigger, extraReaction or bypass of condition defenses is granted.

### Preserved submitted examples

An opportunity hit during an enemy's movement setsSpeed0 through that enemy turn's end, preventing later ordinary movement.

An independently legal teleport can still move the target; Sentinel does not turn0Speed into a teleport prohibition.

## GC-48 — Sharpshooter

### Original complete object

```json
{
  "id": "sharpshooter",
  "name": "Sharpshooter",
  "description": "You have mastered ranged weapons.",
  "prerequisite": "Dexterity 13 or higher",
  "effect": "Your ranged weapon attacks ignore half and three-quarters cover and don't have disadvantage at long range.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Define ranged-weapon attacks ignoring half/three-quarters cover and long-range disadvantage, preserving total cover and normal maximum range. No−5/+10, melee-range disadvantage immunity, automatic line of sight or spell-attack expansion is printed.

### Final source decision

Retain the complete GC-48 proposal as explicitly NEW where supplied; Actual ranged-weapon classification and cover-term-only scope including magic cover without defeating barriers themselves. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Your attacks made with actual ranged-class weapons ignore the target's half and three-quarters cover for the attack comparison and ignore disadvantage solely from being beyond normal range but within that weapon's actual long range. Total cover, sight/perception, line of effect, ammunition, maximum range and all independent disadvantage remain. A thrown melee-class weapon is not automatically a ranged-class weapon; spell attacks do not qualify. A magical barrier that supplies only half/three-quarters cover is ignored for that cover term because the source makes no mundane restriction; a barrier's independent untargetability or damage prevention remains. No−5/+10, nearby-hostile disadvantage immunity, extra range or ability-score increase.

### Final authored examples

A longbow shot inside its long maximum ignores long-range disadvantage and three-quarters cover.

A fully enclosing wall still prevents targeting, and an adjacent hostile can still impose proximity disadvantage.

### Preserved submitted procedure

Your attacks made with actual ranged-class weapons ignore the target's half and three-quarters cover for the attack comparison and ignore disadvantage solely from being beyond normal range but within that weapon's actual long range. Total cover, sight/perception, line of effect, ammunition, maximum range and all independent disadvantage remain. A thrown melee-class weapon is not automatically a ranged-class weapon; spell attacks do not qualify. A magical barrier that supplies only half/three-quarters cover is ignored for that cover term because the source makes no mundane restriction; a barrier's independent untargetability or damage prevention remains. No−5/+10, nearby-hostile disadvantage immunity, extra range or ability-score increase.

### Preserved submitted examples

A longbow shot inside its long maximum ignores long-range disadvantage and three-quarters cover.

A fully enclosing wall still prevents targeting, and an adjacent hostile can still impose proximity disadvantage.

## GC-49 — Shield Master

### Original complete object

```json
{
  "id": "shield_master",
  "name": "Shield Master",
  "description": "You use shields not just for protection but also for offense.",
  "prerequisite": "None",
  "effect": "You can use a bonus action to shove a creature within 5 feet of you with your shield.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Preserve Bonus Action shield shove within5ft; define actual shield wielding/proficiency, target-size/reach, governing shove check/save and choice of push/Prone. No unprinted Attack-action prerequisite, extra Bonus Action, save bonus or damage evasion is assumed.

### Final source decision

Retain the complete GC-49 proposal as explicitly NEW where supplied; Usable shield as contact implement, ordinary contest and retained nonproficiency effects. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

While actually wielding a usable shield, spendBA for one ordinary Shove against a creature within5ft. No prior Attack Action/hit is required. UseSTR Athletics opposed by defenderSTR Athletics/DEX Acrobatics, target at most one size larger, tie preserves state; on success choose5ft directly away or Prone. NEW the shield itself supplies the physical contact, so no separate empty grasping hand is required beyond actually wielding it. Shield proficiency is not a new acquisition requirement, but actual nonproficient-shield disadvantage applies to theSTR check and is not waived. A Broken shield cannot supply this maneuver. Buckler qualifies only while its actual body can be deliberately used to shove under current anatomy; no free extra hand is created. No damage, save bonus, evasion or extraBA.

### Final authored examples

A proficient shield user mayBA shove before any Attack Action; a successful contest can chooseProne.

A nonproficient shield user still makes theSTR Athletics contest with the actual shield disadvantage.

### Preserved submitted procedure

While actually wielding a usable shield, spendBA for one ordinary Shove against a creature within5ft. No prior Attack Action/hit is required. UseSTR Athletics opposed by defenderSTR Athletics/DEX Acrobatics, target at most one size larger, tie preserves state; on success choose5ft directly away or Prone. NEW the shield itself supplies the physical contact, so no separate empty grasping hand is required beyond actually wielding it. Shield proficiency is not a new acquisition requirement, but actual nonproficient-shield disadvantage applies to theSTR check and is not waived. A Broken shield cannot supply this maneuver. Buckler qualifies only while its actual body can be deliberately used to shove under current anatomy; no free extra hand is created. No damage, save bonus, evasion or extraBA.

### Preserved submitted examples

A proficient shield user mayBA shove before any Attack Action; a successful contest can chooseProne.

A nonproficient shield user still makes theSTR Athletics contest with the actual shield disadvantage.

## GC-50 — Skulker

### Original complete object

```json
{
  "id": "skulker",
  "name": "Skulker",
  "description": "You excel at hiding and moving unseen.",
  "prerequisite": "Dexterity 13 or higher",
  "effect": "You can hide when lightly obscured and missing with a ranged weapon attack doesn't reveal your position.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Define Hide while lightly obscured under actual sight/observation rules and missing ranged-weapon attack preserving position. Distinguish weapon noises, visible traces, automatic discovery and later attacks; no inherent invisibility, sight in darkness or spell-miss exemption.

### Final source decision

Retain the complete GC-50 proposal as explicitly NEW where supplied; Light-obscuration Hide permission and narrowly preserved position after a ranged-weapon miss. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

You may attempt Hide when only lightly obscured, provided an actual source of light obscuration affects that observer's view; use the normal observer-specific Stealth/passive procedure. This is an express permission to try, not automatic Hidden, invisibility or an ability to hide in plainly unobscured sight. When your ranged-class weapon attack misses, suppress the ordinary attack-rule automatic position reveal caused by that missed shot for observers from whom you were Hidden. Do not end your Hidden record merely for the shot's normal firing noise/trajectory. NEW independent clear observation, a successful Search, movement into unobscured sight, communication revealing your position or another actual disclosure can still locate you; they are not negated by missing. A hit reveals normally. Spell misses and thrown melee-class weapons are outside this ranged-weapon clause. It neither improves vision in darkness nor suppresses all evidence permanently.

### Final authored examples

A hidden archer misses from light foliage; the miss alone does not reveal the archer's position.

Stepping into a plainly visible lit doorway afterward still ends Hidden, regardless of the prior miss.

### Preserved submitted procedure

You may attempt Hide when only lightly obscured, provided an actual source of light obscuration affects that observer's view; use the normal observer-specific Stealth/passive procedure. This is an express permission to try, not automatic Hidden, invisibility or an ability to hide in plainly unobscured sight. When your ranged-class weapon attack misses, suppress the ordinary attack-rule automatic position reveal caused by that missed shot for observers from whom you were Hidden. Do not end your Hidden record merely for the shot's normal firing noise/trajectory. NEW independent clear observation, a successful Search, movement into unobscured sight, communication revealing your position or another actual disclosure can still locate you; they are not negated by missing. A hit reveals normally. Spell misses and thrown melee-class weapons are outside this ranged-weapon clause. It neither improves vision in darkness nor suppresses all evidence permanently.

### Preserved submitted examples

A hidden archer misses from light foliage; the miss alone does not reveal the archer's position.

Stepping into a plainly visible lit doorway afterward still ends Hidden, regardless of the prior miss.

## GC-51 — Slasher

### Original complete object

```json
{
  "id": "slasher",
  "name": "Slasher",
  "description": "You are adept at dealing slashing damage.",
  "prerequisite": "Strength or Dexterity 13 or higher",
  "effect": "When you hit with a slashing weapon, you can reduce the target's speed by 10 feet and critical hits cause disadvantage on attack rolls.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Define slashing-weapon hit−10ft Speed with exact cadence,duration and movement-mode arbitration. Complete critical-hit attack disadvantage duration and eligible target, repeated refresh versus stacking and timing. No unprinted ability-score increase or spell damage trigger.

### Final source decision

Remove additive hostile-slow exception; retain source slashing-weapon attack trigger and critical attack-disadvantage rider.

### Complete candidate procedure

NEW once per turn, after your personal attack with a weapon whose native damage includes slashing hits, reduce each of the target's Speed modes by10ft, minimum0, through your next original regular start. A hit with0damage still qualifies. Same feat identity across owners applies one−10layer with independent expiries; Crippling Strike and other hostile slows compete under the reviewed strongest-hostile-slow rule. Two−10 reductions do not add; a stronger half-Speed effect wins instead. Separate systemic movement stages and hard Speed0 restrictions remain controlling. Separately, any critical hit with that slashing weapon imposes disadvantage on all target attack rolls through your next original regular start. Same-name disadvantage never stacks extra dice. Reapplication can preserve later deadlines but grants no new condition beyond these explicit riders. No ability-score increase or trigger from a slashing spell/rider on a non-slashing weapon. Actual natural-weapon qualification requires its real profile.

### Final authored examples

One Slasher hit changes Speed30 to20; another Slasher or Crippling Strike−10 still leaves20.

With an independently applicable half-Speed hostile slow, Speed30 becomes15, not10 or5 from adding/multiplying the−10 effects. A genuine hard Speed0 restriction still produces0.

### Preserved submitted procedure

NEW once per turn, after your personal attack with a weapon whose native damage includes slashing hits, reduce each of the target's Speed modes by10ft, minimum0, through your next original regular start. A hit with0damage still qualifies. Same feat identity across owners applies one−10layer with independent expiries; distinct Crippling Strike can add a separate−10 under the proposed feat-family rule, before applicable halving/Speed0 overrides. Separately, any critical hit with that slashing weapon imposes disadvantage on all target attack rolls through your next original regular start. Same-name disadvantage never stacks extra dice. Reapplication can preserve later deadlines but grants no new condition beyond these explicit riders. No ability-score increase or trigger from a slashing spell/rider on a non-slashing weapon. Actual natural-weapon qualification requires its real profile.

### Preserved submitted examples

One Slasher hit changesSpeed30 to20; another owner's Slasher does not lower it again.

If independently proposed Crippling Strike also applies, the two distinct−10layers yield10 before a separate halving; both proposals still need joint approval.

## GC-52 — Tactical Insight

### Original complete object

```json
{
  "id": "tactical_insight",
  "name": "Tactical Insight",
  "description": "Intelligence 13+ supports the listed reveal of hidden enemy information.",
  "prerequisite": "Intelligence 13+",
  "effect": "As a bonus action, make an Investigation or Insight check against DC 10 + the target’s challenge rating. On a success, learn its current HP band, highest save, or lowest save. Once per target.",
  "type": "General",
  "legacyEffect": "Reveal hidden enemy info",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

Preserve Bonus Action Investigation or Insight versusDC10+CR, choice of currentHP band/highest/lowest save and once-per-target. Define CRless targets, fractional DC rounding, range/sensing, when to choose information, ties and ledger reset. No hidden-stat disclosure on failure or automatic creature identification.

### Final source decision

Retain the complete GC-52 proposal as explicitly NEW where supplied; 60ft/perception, roundedDC/default, preselected information, precise bands/ties and per-targetLR attempt ledger. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

BA: observe one actual perceived living creature within60ft and line of effect. Choose currentHP band, highest ordinary save modifier or lowest ordinary save modifier before rollingINT Investigation orWIS Insight againstDC10+ceil(actualCR); NEW useDC15 if the source supplies noCR. Apply ordinary fixed-DC task degrees/natural shifts; Success/Critical Success returns only the selected fact, failure none. NEW one attempt per actual target identity per completedLR, spent on the legal attempt even on failure; changing form/name or leaving initiative does not reset it. HP bands are Full, Positive-above-half, Positive-at-or-below-half, and Zero; effective maximum and normalHP govern, tempHP excluded. Highest/lowest uses actual six ordinary save modifiers including current unconditional proficiency/stat/item modifiers, not situational advantage or a specific opponent's conditional bonus; report all tied abilities. If complete actual data is unavailable or explicit information protection blocks it, return Indeterminate without fabricating a stat/type or diagnosing the protection. It is a specific information permission, not a general creature identification or exactHP read. MissingCR uses the fixed default without proving a hidden classification.

### Final authored examples

CR1/2 givesDC11. HP10/max20 reports Positive-at-or-below-half rather than an exactHP number.

A failed attempt spends that target's allowance until a completedLR; a disguised version of the same individual is not a fresh target.

### Preserved submitted procedure

BA: observe one actual perceived living creature within60ft and line of effect. Choose currentHP band, highest ordinary save modifier or lowest ordinary save modifier before rollingINT Investigation orWIS Insight againstDC10+ceil(actualCR); NEW useDC15 if the source supplies noCR. Apply ordinary fixed-DC task degrees/natural shifts; Success/Critical Success returns only the selected fact, failure none. NEW one attempt per actual target identity per completedLR, spent on the legal attempt even on failure; changing form/name or leaving initiative does not reset it. HP bands are Full, Positive-above-half, Positive-at-or-below-half, and Zero; effective maximum and normalHP govern, tempHP excluded. Highest/lowest uses actual six ordinary save modifiers including current unconditional proficiency/stat/item modifiers, not situational advantage or a specific opponent's conditional bonus; report all tied abilities. If complete actual data is unavailable or explicit information protection blocks it, return Indeterminate without fabricating a stat/type or diagnosing the protection. It is a specific information permission, not a general creature identification or exactHP read. MissingCR uses the fixed default without proving a hidden classification.

### Preserved submitted examples

CR1/2 givesDC11. HP10/max20 reports Positive-at-or-below-half rather than an exactHP number.

A failed attempt spends that target's allowance until a completedLR; a disguised version of the same individual is not a fresh target.

## GC-53 — Tavern Brawler

### Original complete object

```json
{
  "id": "tavern_brawler",
  "name": "Tavern Brawler",
  "description": "You excel at fighting with improvised weapons.",
  "prerequisite": "None",
  "effect": "You are proficient with improvised weapons and unarmed strikes, and can grapple as a bonus action after hitting with an unarmed strike.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Preserve improvised/unarmed proficiency and Bonus Action grapple after an unarmed hit. Define same-turn/target requirement, actual free hand/reach, damage dice under existing profiles and no extra attack. Compare Brawler unconditional Bonus Action grapple and1d4 base without importing an ability increase.

### Final source decision

Retain the complete GC-53 proposal as explicitly NEW where supplied; Same-turn/same-target unarmed-hit gate and actual existing object/unarmed profiles. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Gain actual improvised-weapon and unarmed-strike proficiency. Use the reviewed improvised object profile: an actually similar existing weapon can use its agreed full profile, otherwise1d4 appropriate physical type and20/60 throwing range. Ordinary unarmed damage is unchanged by this feat unless another actual source, such as Brawler, changes it. After your unarmed strike hits a creature on your own turn, you may spendBA that same turn for one ordinary Grapple of that same creature. NEW target must still be within actual reach and no more than one size larger, with a usable free grasping hand; use ordinary Athletics opposed by Athletics/Acrobatics. No damage or automatic success from the grapple. An improvised-weapon hit is not an unarmed hit for this trigger. Brawler's independently unconditionalBAgrapple remains broader; neither grants a secondBA or unprinted ability increase.

### Final authored examples

An unarmed hit can enableBAgrapple of that same nearby foe if a free hand remains.

Hitting with a chair uses improvised proficiency but does not enable this feat's unarmed-hit grapple trigger.

### Preserved submitted procedure

Gain actual improvised-weapon and unarmed-strike proficiency. Use the reviewed improvised object profile: an actually similar existing weapon can use its agreed full profile, otherwise1d4 appropriate physical type and20/60 throwing range. Ordinary unarmed damage is unchanged by this feat unless another actual source, such as Brawler, changes it. After your unarmed strike hits a creature on your own turn, you may spendBA that same turn for one ordinary Grapple of that same creature. NEW target must still be within actual reach and no more than one size larger, with a usable free grasping hand; use ordinary Athletics opposed by Athletics/Acrobatics. No damage or automatic success from the grapple. An improvised-weapon hit is not an unarmed hit for this trigger. Brawler's independently unconditionalBAgrapple remains broader; neither grants a secondBA or unprinted ability increase.

### Preserved submitted examples

An unarmed hit can enableBAgrapple of that same nearby foe if a free hand remains.

Hitting with a chair uses improvised proficiency but does not enable this feat's unarmed-hit grapple trigger.

## GC-54 — Versatile Grip

### Original complete object

```json
{
  "id": "versatile_grip",
  "name": "Versatile Grip",
  "description": "Dexterity 12+ supports the listed use of a non-proficient weapon at 80% effectiveness.",
  "prerequisite": "Dexterity 12+",
  "effect": "Use non-proficient weapon at 80% effectiveness.",
  "type": "General",
  "legacyEffect": "Use non-proficient weapon at 80% effectiveness",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

Source80percent effectiveness is unresolved. Specify what quantity is multiplied, rounding and meaning relative to ordinary nonproficient attacks without PB. Define weapon eligibility and no automatic proficiency, extra hands, property waiver or multiplicative damage scaling chosen without discussion.

### Final source decision

Retain the complete GC-54 proposal as explicitly NEW where supplied; Explicit NEW80%-of-PB attack allowance rather than undefined effectiveness; no proficiency credential. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

NEW explicit completion of the unresolved80%: when making an otherwise legal weapon attack with a weapon in which you lack proficiency, add floor(0.8×your currentPB) to that attack roll as a feat-specific training allowance instead of the ordinary zero proficiency contribution. Use exact4×PB//5 arithmetic. Damage remains normal; do not multiply the weapon's damage or whole attack total by80%, and do not claim this is the original source's recovered definition. If genuinely proficient, use normalPB and no extra allowance. This is not proficiency for acquisition/prerequisite, tool, save, maneuver or class gates. Actual Simple/Martial/Special profile, hands, anatomy, Heavy/size, ammunition and property restrictions remain. The allowance replaces rather than adds to another partial-proficiency contribution for that attack. No repeat stacking or new weapon item.

### Final authored examples

AtPB3 the allowance isfloor2.4=2, added to the actual attack ability; damage is unchanged.

AtPB2 it is1. The owner still cannot choose that unproficient weapon as Weapon Focus's prerequisite.

### Preserved submitted procedure

NEW explicit completion of the unresolved80%: when making an otherwise legal weapon attack with a weapon in which you lack proficiency, add floor(0.8×your currentPB) to that attack roll as a feat-specific training allowance instead of the ordinary zero proficiency contribution. Use exact4×PB//5 arithmetic. Damage remains normal; do not multiply the weapon's damage or whole attack total by80%, and do not claim this is the original source's recovered definition. If genuinely proficient, use normalPB and no extra allowance. This is not proficiency for acquisition/prerequisite, tool, save, maneuver or class gates. Actual Simple/Martial/Special profile, hands, anatomy, Heavy/size, ammunition and property restrictions remain. The allowance replaces rather than adds to another partial-proficiency contribution for that attack. No repeat stacking or new weapon item.

### Preserved submitted examples

AtPB3 the allowance isfloor2.4=2, added to the actual attack ability; damage is unchanged.

AtPB2 it is1. The owner still cannot choose that unproficient weapon as Weapon Focus's prerequisite.

## GC-55 — Weapon Focus

### Original complete object

```json
{
  "id": "weaponFocus",
  "name": "Weapon Focus",
  "description": "You have specialized training with a particular weapon type.",
  "prerequisite": "Proficiency with chosen weapon",
  "effect": "+1 to attack rolls with chosen weapon type",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Choose one exact current weapon type with actual proficiency; define repeatability, type versus family, attack scope, natural/unarmed support and persistent eligibility. Preserve+1attack only, no damage bonus or broader Weapon Mastery adoption. Resolve source bonus family explicitly.

### Final source decision

Retain the complete GC-55 proposal as explicitly NEW where supplied; Repeatable distinct types, current proficiency condition and exact profile versus family. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

Choose one exact current weapon type/profile for which you have actual proficiency. NEW this feat may be selected again only for a different type, spending a real feat choice each time. Gain+1 on attack rolls actually using that chosen profile while that proficiency remains operative; no damage bonus. Melee/thrown use of that actual weapon qualifies if it retains the chosen profile; improvised use that changes it to a generic object does not. A specific natural-weapon profile or unarmed-strike profile can be chosen only with an actual proficiency receipt for that profile; do not select all weapons, all natural attacks or a damage type as one choice. Losing the usable profile/proficiency suppresses the bonus without erasing the record. Distinct eligible Precision Throw can add+1, while duplicate Focus on the same type cannot.

### Final authored examples

Focus dagger adds1 to its legal melee or Thrown attack, not to every piercing weapon.

Two paid Focus selections can cover rapier and longbow; selecting rapier twice does not create+2.

### Preserved submitted procedure

Choose one exact current weapon type/profile for which you have actual proficiency. NEW this feat may be selected again only for a different type, spending a real feat choice each time. Gain+1 on attack rolls actually using that chosen profile while that proficiency remains operative; no damage bonus. Melee/thrown use of that actual weapon qualifies if it retains the chosen profile; improvised use that changes it to a generic object does not. A specific natural-weapon profile or unarmed-strike profile can be chosen only with an actual proficiency receipt for that profile; do not select all weapons, all natural attacks or a damage type as one choice. Losing the usable profile/proficiency suppresses the bonus without erasing the record. Distinct eligible Precision Throw can add+1, while duplicate Focus on the same type cannot.

### Preserved submitted examples

Focus dagger adds1 to its legal melee or Thrown attack, not to every piercing weapon.

Two paid Focus selections can cover rapier and longbow; selecting rapier twice does not create+2.

## GC-56 — Weapon Master

### Original complete object

```json
{
  "id": "weapon_master",
  "name": "Weapon Master",
  "description": "You have practiced extensively with a variety of weapons.",
  "prerequisite": "None",
  "effect": "You gain proficiency with four weapons of your choice and increase your Strength or Dexterity score by 1.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

Preserve four actual weapon choices and+1STRorDEX. Define score cap, duplicate/already proficient choices, exact eligible weapon catalog including special weapons and training availability. It grants no automatic item or generalized simple/martial proficiency beyond chosen types.

### Final source decision

Retain the complete GC-56 proposal as explicitly NEW where supplied; Four distinct catalog profiles, permitted existing special profiles, capped composite ability and no invented acquisition tax. Apply the final shared cadence, actual-action, proficiency, stacking and causal-root decisions; no class or equipment profile is imported by name.

### Complete candidate procedure

At acquisition choose four distinct actual weapon types/profiles from the current equipment catalog and gain proficiency with them; an already-proficient choice gives no additionalPB/expertise and is not replaceable for free later. NEW catalog Special weapons may be selected if their complete real profile exists, but proficiency does not waive actual attunement, anatomy, size, Two-Handed, loading or source-specific use permissions. Natural/unarmed attacks are not catalog weapon choices here. Increase permanentSTR orDEX by1, cap20 under the existing composite-grant rule. Choose the ability once; if already capped, the increase is0 but the four training choices remain. This grants no four items, blanket Simple/Martial proficiency, free retraining or extra class level. Actual feat-acquisition time/cost is governed by advancement, not an invented additional lesson requirement here.

### Final authored examples

Choose four actual weapon types andDEX19→20; no physical weapons appear in inventory.

Choosing a weapon already proficient does not make it expertise. STR20 remains20 while the other training grants still apply.

### Preserved submitted procedure

At acquisition choose four distinct actual weapon types/profiles from the current equipment catalog and gain proficiency with them; an already-proficient choice gives no additionalPB/expertise and is not replaceable for free later. NEW catalog Special weapons may be selected if their complete real profile exists, but proficiency does not waive actual attunement, anatomy, size, Two-Handed, loading or source-specific use permissions. Natural/unarmed attacks are not catalog weapon choices here. Increase permanentSTR orDEX by1, cap20 under the existing composite-grant rule. Choose the ability once; if already capped, the increase is0 but the four training choices remain. This grants no four items, blanket Simple/Martial proficiency, free retraining or extra class level. Actual feat-acquisition time/cost is governed by advancement, not an invented additional lesson requirement here.

### Preserved submitted examples

Choose four actual weapon types andDEX19→20; no physical weapons appear in inventory.

Choosing a weapon already proficient does not make it expertise. STR20 remains20 while the other training grants still apply.

## GC-57 — Companion Training

### Original complete object

```json
{
  "id": "companion_training",
  "name": "Companion Training",
  "description": "Your beasts do not merely follow—they fight as extensions of your will across Aethel's wild tiers, answering whistle and gesture like soldiers who never learned fear. Prestige lineage: Beastmaster. completed from the existing development record.)",
  "prerequisite": "Animal Companion feat or proficiency in Animal Handling",
  "effect": "Beast companions you command gain +2 to attack and damage rolls and inherit your Survival proficiency for tracking. As a bonus action, command one companion to attack, dash, disengage, or help; at level 10+, you may issue the same command to two companions that can hear you. When a companion reduces a foe to 0 HP, you gain advantage on your next attack against a creature within 30 feet before the end of your next turn.",
  "type": "General",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "Beast companions you command gain +2 to attack and damage rolls and inherit your Survival proficiency for tracking. As a bonus action, command one companion to attack, dash, disengage, or help; at level 10+, you may issue the same command to two companions that can hear you. When a companion reduces a foe to 0 HP, you gain advantage on your next attack against a creature within 30 feet before the end of your next turn.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

Complete every clause against actual persistent companion ownership/control: Beast eligibility,+2attack/damage, whose Survival proficiency and ability; Bonus Action commands at10+two audible companions; structural/phase caps and no free extra activations. Define genuine companion kill and owner next attack30ft before next-turn-end, target snapshot/cadence, refresh and no trivial/friendly farming.

### Final source decision

Adopt the bounded proposal with the completed EX58 controller/phase/physical-history interface; no future transport dependency or extra animal turn.

### Complete candidate procedure

Require the exact Animal Companion feat OR actual Animal Handling proficiency. Your genuinely bound/tamed Beast companions under your lawful current command gain+2 to their attack rolls and+2flat once per native attack damage roll, not per die/type or critical doubling. NEW no benefit to an ordinary allied Beast, non-Beast construct/undead/familiar, or a body you have no actual companion/control relation with. Original source-owner stats remain; add this feat layer once across overlapping trainers. For real tracking checks, if you are proficient in Survival, the companion uses its ownWIS plus your currentPB as the inherited proficiency contribution; expertise is not inherited, and a better real own contribution can replace it, not add twice. If you lack Survival proficiency, nothing is inherited. During your regular turn spend the sharedBAcommand within60ft to one companion that can hear you, selecting attack, Dash, Disengage or Help. At total level10+, the same command can name two audible owned companions taking that same action in their attached phases. This changes command recipient count only: one shared offensive companion action per owner numbered round remains. For attack, designate at most one to spend that offense; the other may move defensively and Dodge, not bank an attack. Two pure support actions can both resolve if legal. Command fails without refund if eligibility is lost; no extra independent turns/Reactions. When one of your actually commanded Beast companions reduces a meaningful hostile from positiveHP to0, you gain one advantage entitlement for your next attack against a creature within30ft of you before your next future regular end. NEW only an attack meeting30ft consumes it; a farther attack does not. Same-family reapplication refreshes one entitlement/deadline, never queues multiple. Death is not required, source floors/copy/no-reward restrictions apply.
NEW explicit EX58 interface: retain one real creature identity and one current control/phase record. Riding, bonding or transferring custody does not clone a turn, movement budget, Reaction, attack allowance, body or resource pool. An attached companion acts in its source-defined phase after the owner’s regular turn; a controlled mount uses EX58’s actual mounted-phase procedure. A body fitting both roles elects one compatible route before that round’s work, preserves all already-spent allowances and cannot switch routes to gain a second phase. Its actual load, tack, rider geometry, mounting/dismounting cost and ordinary independent temperament remain. One shared Bonus Action command and one offensive companion action per owner per numbered round apply where those source engines impose them. This feat supplies no blanket override of a specific engine’s attack or no-resource restrictions.

### Final authored examples

At level10, two companions can each perform a legal Help from the one shared command; an Attack command still permits only one shared offensive action.

A commanded Beast downs a hostile: the owner's next attack within30ft gains advantage before the deadline; no extra attack is granted.

### Preserved submitted procedure

Require the exact Animal Companion feat OR actual Animal Handling proficiency. Your genuinely bound/tamed Beast companions under your lawful current command gain+2 to their attack rolls and+2flat once per native attack damage roll, not per die/type or critical doubling. NEW no benefit to an ordinary allied Beast, non-Beast construct/undead/familiar, or a body you have no actual companion/control relation with. Original source-owner stats remain; add this feat layer once across overlapping trainers. For real tracking checks, if you are proficient in Survival, the companion uses its ownWIS plus your currentPB as the inherited proficiency contribution; expertise is not inherited, and a better real own contribution can replace it, not add twice. If you lack Survival proficiency, nothing is inherited. During your regular turn spend the sharedBAcommand within60ft to one companion that can hear you, selecting attack, Dash, Disengage or Help. At total level10+, the same command can name two audible owned companions taking that same action in their attached phases. This changes command recipient count only: one shared offensive companion action per owner numbered round remains. For attack, designate at most one to spend that offense; the other may move defensively and Dodge, not bank an attack. Two pure support actions can both resolve if legal. Command fails without refund if eligibility is lost; no extra independent turns/Reactions. When one of your actually commanded Beast companions reduces a meaningful hostile from positiveHP to0, you gain one advantage entitlement for your next attack against a creature within30ft of you before your next future regular end. NEW only an attack meeting30ft consumes it; a farther attack does not. Same-family reapplication refreshes one entitlement/deadline, never queues multiple. Death is not required, source floors/copy/no-reward restrictions apply.

### Preserved submitted examples

At level10, two companions can each perform a legal Help from the one shared command; an Attack command still permits only one shared offensive action.

A commanded Beast downs a hostile: the owner's next attack within30ft gains advantage before the deadline; no extra attack is granted.

## GC-58 — Primal Instinct

### Original complete object

```json
{
  "id": "primal_instinct",
  "name": "Primal Instinct",
  "description": "The beast inside listens before the mind does. You trust that older voice. Prestige lineage: Mooncursed. completed from the existing development record.)",
  "prerequisite": "Wisdom 13+, proficiency in Survival",
  "effect": "You have advantage on Wisdom (Perception) checks relying on hearing or smell. You cannot be surprised while conscious. You can track creatures across difficult terrain without penalty. Under moonlight or while transformed, you gain +2 to initiative and once per short rest you may howl or roar as a free action: allies within 30 feet who can hear you gain advantage on their next attack against a creature you are tracking or have damaged this encounter.",
  "type": "General",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You have advantage on Wisdom (Perception) checks relying on hearing or smell. You cannot be surprised while conscious. You can track creatures across difficult terrain without penalty. Under moonlight or while transformed, you gain +2 to initiative and once per short rest you may howl or roar as a free action: allies within 30 feet who can hear you gain advantage on their next attack against a creature you are tracking or have damaged this encounter.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

Preserve hearing/smell Perception advantage, conscious surprise protection and terrain tracking. Define actual moonlight/transformed condition for+2initiative and once-Short-Rest free howl/roar, own/off-turn timing, audible30ft allies, eligible tracked/damaged foe and advantage expiration. No new transformation, compulsory ally attack or cosmology/astronomy decision.

### Final source decision

Keep actual source ally wording including self, with original target/sensory/budget conditions; no generalized automatic self-target for inherently two-person effects.

### Complete candidate procedure

Gain advantage on actualWIS Perception checks relying on working hearing or smell, without a passive±5 adjustment. While conscious, surprise restrictions are suppressed as in Alert, with no retroactive actions. When actually tracking a real trail, ignore penalties caused solely by difficult terrain; preserve absent evidence, concealment, age, weather and source-specific no-trace restrictions. NEW the moonlight/transformed clause qualifies both the+2initiative and howl: at the actual initiative roll, if physically illuminated by real existing moonlight or in an actual body-transforming form, add2. It does not establish an astronomical calendar, count a moon-themed spell as moonlight, or treat an illusion/disguise as body transformation. Once perSR while that predicate holds, on your own regular turn without an Action cost, audibly howl/roar and choose one actual creature you are currently tracking through a legal source or personally damaged during this encounter. Allies, including yourself, within30ft who hear at the moment gain advantage on their next attack against that chosen creature before your next future regular end. NEW recipient list and target are fixed, no continuing range tether and no extra attack; one family entitlement per ally, consumed by its first eligible attack hit/miss/cancellation. The body must actually be able to howl or roar; articulated speech or a shared language is not required. Silence or an anatomy unable to make that sound prevents it. Conditions otherwise permit this brief free communication but do not grantActions. Tracking alone does not reveal a target's present location for an attack.
SOURCE SCOPE CORRECTION: “allies” includes the feat owner unless the actual clause says “other.” The owner must still meet the same hearing/perception, range, willing-target and action/resource predicates. No second body, observer or extra action is created by self-eligibility. This sentence supersedes any narrower owner-exclusion in the submitted proposal, not the preserved original.

### Final authored examples

During actual qualifying moonlight/transformation, the holder’s paid howl fixes its heard ally recipients, including the holder if hearing is available. Their first eligible attack against the chosen tracked/damaged creature uses the entitlement, without revealing its location or granting an extra attack.

A moon-painted lantern is not actual moonlight. The feat creates neither transformation access nor current location knowledge from an old trail.

### Preserved submitted procedure

Gain advantage on actualWIS Perception checks relying on working hearing or smell, without a passive±5 adjustment. While conscious, surprise restrictions are suppressed as in Alert, with no retroactive actions. When actually tracking a real trail, ignore penalties caused solely by difficult terrain; preserve absent evidence, concealment, age, weather and source-specific no-trace restrictions. NEW the moonlight/transformed clause qualifies both the+2initiative and howl: at the actual initiative roll, if physically illuminated by real existing moonlight or in an actual body-transforming form, add2. It does not establish an astronomical calendar, count a moon-themed spell as moonlight, or treat an illusion/disguise as body transformation. Once perSR while that predicate holds, on your own regular turn without an Action cost, audibly howl/roar and choose one actual creature you are currently tracking through a legal source or personally damaged during this encounter. Other allies within30ft who hear at the moment gain advantage on their next attack against that chosen creature before your next future regular end. NEW recipient list and target are fixed, no continuing range tether and no extra attack; one family entitlement per ally, consumed by its first eligible attack hit/miss/cancellation. The body must actually be able to howl or roar; articulated speech or a shared language is not required. Silence or an anatomy unable to make that sound prevents it. Conditions otherwise permit this brief free communication but do not grantActions. Tracking alone does not reveal a target's present location for an attack.

### Preserved submitted examples

A transformed owner howls on its turn for a foe it actually damaged; hearing allies receive one next-attack advantage through the owner's next regular end.

A moon-painted lantern is not actual moonlight. The feat creates neither transformation access nor current location knowledge from an old trail.
