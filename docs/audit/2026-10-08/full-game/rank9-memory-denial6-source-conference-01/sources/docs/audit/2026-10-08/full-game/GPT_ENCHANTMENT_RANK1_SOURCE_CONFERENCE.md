# Twelve rank-one Enchantment spells — GPT source conference

Conversation: Calibration Review
Turn: 362fea01-2c60-4427-8fd7-b5b791513e27

I’ve reconciled all twelve against the packet’s exact source records and the supplied control/condition/casting authorities. :chatgpt-content-reference{index="0"} These are **SOURCE-RECONCILED / DRAFTABLE**, not manuscript-approved yet.

### 1. Mesmerize

**Action; 30 ft; one creature perceived with LoE; V/S/F; CHA save; 1 target round; no concentration.**

On failure, apply **Stunned** and a separate **unaware** state until the end of the target’s first future regular turn, excluding the entire current turn if already in progress; outside initiative, 6 seconds.

`Unaware` means the target does not consciously register new ordinary sensory events while it lasts. For a rule expressly asking whether it currently perceives/is aware of a creature or event, treat it as unaware unless another exact sense/effect says otherwise. Unaware itself adds **no** Unconscious, Prone, item dropping, adjacent auto-crit, memory deletion, blindness/deafness condition, or extra attack modifier beyond Stunned.

The Stunned/Incapacitated component uses the shared source-character/target/encounter hard-control allowance. If that hard component is blocked by the guard or a narrow applicable immunity, only that blocked component is suppressed; independently printed unaware remains unless a broader defense blocks it. Narrow Incapacitated/Stunned immunities retain their existing component-level scope.

**NEW:** one-creature target and operational unaware definition.

### 2. Pacify

**Action; 30 ft; one creature you perceive and presently treat as an enemy from ordinary information; V/S/F; NEW WIS save; 1 target round; no concentration.**

Failure: until the end of its first future regular turn, the target cannot voluntarily:

- make an attack; or
- begin/cast a spell whose selected legal mode will deal damage.

This applies regardless of whether that attack/spell would use an Action, Bonus Action, Reaction, or another actual permission. A spell with both damaging and nondamaging modes remains usable only through a selected nondamaging mode.

Delayed damage deliberately created by the cast counts as damaging. Already-committed or already-resolving attacks/spells are not rewound.

The creature retains movement, non-damaging spells, control/utility effects, interactions and other legal permissions. There is **no harm-break clause**. This is an attack/damaging-spell restriction, not automatic whole-Action denial and does not consume the hard whole-Action guard merely because a creature has poor alternative choices.

**NEW:** WIS save and exact prohibited-action scope.

### 3. Sleep

**Action; 30 ft; V/S/F; no save; NEW 1 minute; no concentration.**

Before hidden HP/immunity resolution, designate an ordered list of creatures you perceive within 30 ft and LoE.

Process them in that declared order against a fixed **24-HP budget**. Each attempted creature costs its **current ordinary HP, minimum 1**, ignoring temporary HP. If its cost would exceed the remaining budget, stop; later creatures are not attempted.

A creature consumes that budget when attempted even if an actual immunity, hard-control guard, or other defense ultimately prevents this spell’s Unconscious application. This avoids turning hidden HP/immunity into a free targeting oracle.

A successfully affected creature gains an independent **Sleep-caused Unconscious** application for up to 1 minute. The shared hard-control allowance applies per target. Existing 0-HP or other Unconscious causes remain separate; ending Sleep removes only this spell’s cause.

Sleep ends early for that creature if:

- it receives a **positive post-defense damage packet**;
- another creature within reach spends an **Action** physically rousing it; or
- an exact waking/removal rule applies.

No self-awakening while Unconscious. No healing, stabilization, death-save reset, or rolled sleep dice. Active Undead/Construct creatures are not automatically immune without an actual defense.

**NEW:** ordered 30-ft selection, current-HP/minimum-1 budget, one-minute duration and waking rules.

### 4. Confusing Flash

**Action; 30 ft; one creature perceived with LoE; V/S/F; WIS save.**

On failure, roll a neutral `1d2` immediately:

**1 — Attack:** On its next regular turn, the target must use its ordinary Action to make **one legal ordinary attack** against a randomly selected other legal creature it can perceive and attack. Determine the victim neutrally from all eligible creatures. The target/controller may choose the legal attack method. No extra Action or resource is granted.

**2 — Flee:** On its next regular turn, it must spend as much of its ordinary available movement as reasonably possible moving away from the caster along a route it knows is not immediately self-destructive. It does not automatically Dash and retains its Action/BA/Reactions. This movement is movement under compulsion, not push/pull, and can provoke ordinary opportunity attacks.

If Attack is rolled but no legal victim exists, no attack is compelled. If no safe meaningful fleeing route exists, move only as far as a legal non-self-destructive route permits.

The **Attack branch’s commanded Action** uses/reserves the shared hard-control allowance when the failed save would establish that future command. If unavailable, the Attack command does not apply; invent no fallback. The Flee branch does not create a new Action denial.

No caster-selected branch/victim, deliberate self-harm, known lethal route, or Action recursion.

**NEW:** random branch procedure, victim selection, next-turn execution and hard-control reservation.

### 5. Distract

**Reaction — when an enemy you perceive within 30 ft and LoE begins an Action, after its Action/casting commitments but before its first resolving outcome; V/S/F.**

Only an **Action** qualifies, not a Bonus Action or Reaction.

Target makes a **NEW INT save**.

Failure:

1. attempt to cancel the entire triggering Action; and
2. target cannot make **opportunity attacks** until the current numbered round ends.

The Action cancellation is a hard whole-Action denial and therefore requires the shared hard-control allowance. If the guard/immunity blocks that hard component, the explicitly printed opportunity-attack suppression still applies after the failed save.

For an Attack Action, cancel the whole Action before any attack resolves. For a spell Action, normal cast costs, RP, components, concentration transition, Dissonance/Refrain and beginning hooks already occurred; canceling it refunds nothing and restores no prior concentration.

One creature may make at most one Distract attempt against the same pending Action across ordinary/same-named sources unless an exact feature grants an additional attempt.

No cancellation of completed attacks/outcomes, no blanket Reaction denial, and no Counterspell hard-guard rewrite. Outside numbered initiative there is no useful “this round” Distract trigger.

**NEW:** INT save, Action-start trigger, whole-Action cancellation and current-numbered-round OA suppression.

### 6. Voice of Peace

**Action; 30 ft; one perceived enemy that can hear and understand a language you use; V/S/F; NEW WIS save; 1 minute; no concentration.**

Failure establishes a ceasefire toward **you and creatures the target currently recognizes as your participating allies**.

While active, the target cannot voluntarily initiate an attack or knowingly harmful effect against those ceasefire participants.

The effect ends immediately if you or one of those recognized allies commits an attack or knowingly harmful effect against:

- the target; or
- a creature the target actually recognizes as its ally.

Ending occurs on commitment, before hit/damage resolution. Mere insult, argument, approach, suspicion, or unsupported threat does not itself count as provocation.

Initial hearing/language/range are application gates only; no continuing 30-ft or hearing tether. No treaty, permanent alliance, Charmed, Diplomacy success, forced negotiation, or whole-Action loss.

**NEW:** WIS save, one-minute ceasefire, participant scope and concrete provocation.

### 7. Command

**Action; 30 ft; one creature that can hear and understand the spoken one-word command; V/S/F; NEW WIS save; through its next regular turn.**

On failure, the target must obey one legal one-word command during its next regular turn. This grants no extra Action, movement, interaction, spell slot, RP, or other resource.

Bounded examples:

- **Approach:** spend ordinary movement moving toward caster by a safe legal route.
- **Flee:** spend ordinary movement moving away by a safe legal route.
- **Drop:** release one held object capable of ordinary release; ownership does not transfer.
- **Halt:** refrain from voluntary movement for that turn.
- **Grovel:** become/remain Prone for that turn if physically capable.

The caster does not control route/details beyond what the word necessarily requires; where several legal methods satisfy it, the target/controller chooses.

A command cannot require:

- an attack or knowingly harmful act;
- direct self-harm or movement through a known serious hazard;
- disclosure of a protected/private secret;
- permanent surrender/ownership transfer;
- knowing violation of a binding oath/duty;
- impossible conduct.

An invalid command produces no compelled behavior after the failed save; the caster does not substitute another word.

Any command that actually consumes/denies a whole Action or another shared hard-control component is subject to the hard-control guard when established. Non-hard movement/interaction portions retain their own exact scope. Competing commands never create extra turns/actions.

**NEW:** WIS save, hearing/language gate and bounded command dictionary/limits.

### 8. Hideous Laughter

**Action; 30 ft; one creature perceived with LoE; V/S/F; WIS save; NEW concentration up to 1 minute.**

Failure:

1. immediately apply **Prone**; and
2. apply **Incapacitated** as the laughter’s continuing hard-control component.

The Incapacitated component uses the shared hard-control allowance. If blocked by the guard or a narrow immunity, the independently printed Prone application remains unless separately prevented.

At the end of each affected regular turn, the target repeats the WIS save; success ends the spell. It also ends immediately when the target receives a **positive post-defense damage packet**.

The spell does **not** add Speed 0 or a speech ban beyond actual Incapacitated rules. Prone is an immediate condition application; the spell does not separately forbid standing if the creature later has legal movement with which to do so. Ending the spell does not automatically stand the target or restore concentration that Incapacitated already ended.

No biological/INT/Humanoid gate.

**NEW:** concentration duration, repeat save and damage ending.

### 9. Faction Charm

**Action; 30 ft; one creature perceived with LoE; V/S/F; NEW WIS save; 1 hour; no concentration.**

Choose one exact canonical faction with which you have an **actual current affiliation/membership record** at application. Positive reputation/logo/claimed role alone is insufficient.

Failure gives the target a **strong genuine favorable affinity toward that faction** for 1 hour. This is **not Core Charmed**.

While active:

- the target ordinarily regards the faction favorably rather than neutrally/negatively where no stronger actual fact overrides;
- you have **advantage on Persuasion checks** directed to that target specifically concerning the chosen faction, its interests, or cooperation with it.

It retains agency, beliefs and ordinary risk judgment.

End the effect if you, or a creature the target actually recognizes as acting for that faction, commits an attack or knowingly harmful effect against the target.

Faction affiliation is snapshotted at application; later caster membership/leadership changes neither retarget nor automatically end it. No membership, reputation, credential, loyalty, rights, authority, obedience or permanent attitude is created.

**NEW:** WIS save, affinity procedure, Persuasion advantage and recognized-harm ending.

### 10. Alignment Suggestion

**Action; 30 ft; one creature perceived with LoE; V/S/F; WIS save; concentration up to 1 minute.**

Snapshot the caster’s actual current alignment orientation at successful application.

On failure, apply a temporary **alignment overlay** to the target. For each defined canonical axis, move the target **one step toward the caster’s snapshotted value**:

- Lawful ↔ Neutral ↔ Chaotic
- Good ↔ Neutral ↔ Evil

Examples: Evil→Neutral toward Good; Chaotic→Neutral toward Lawful. Already matching axes do not move. Undefined target/caster axes do not invent a value.

For the duration, exact mechanics that query the target’s **current alignment** use the overlay. This can therefore interact with actual alignment-gated spells/items/effects.

It does **not** compel matching conduct, belief, PvP, oathbreaking, confession, loyalty, or personality.

The overlay does not rewrite the underlying alignment record. If another actual effect changes the target’s underlying alignment while this spell persists, that real change remains underneath; ending Alignment Suggestion removes only its overlay and exposes the then-current underlying record.

One Alignment Suggestion overlay per target; a later successful application replaces the previous overlay. A successful save creates no replacement. Ward tag grants no ward.

**NEW:** temporary one-step canonical alignment overlay and stacking/removal procedure.

### 11. Resonance Influence

**Action; 30 ft; one creature perceived with LoE; V/S/F; NEW 1 minute; no concentration. Choose Ease or Burden.**

**Ease:** willing target; next qualifying spell costs **1 fewer RP**.  
**Burden:** target makes a **NEW WIS save**; failure makes its next qualifying spell cost **1 additional RP**.

Compute that spell’s ordinary legal RP price first using its actual rules, including:

1. rank/base spell price;
2. mandatory printed spell extras;
3. applicable Dissonance surcharge;
4. actual explicit class/source discounts.

Then apply Resonance Influence as the final ±1 modifier, minimum **0 RP**, never generating credit/refund.

Consequences:

- Burden can make a normally free 0-RP cantrip cost 1 RP.
- Ease on an already-0-RP spell remains 0 but is still consumed when that legal spell commits.
- A charge-only/item spell with **no actual RP-price interface** does not acquire an invented RP cost and does not qualify.
- A real spell cast through an item/class source qualifies if its actual procedure has an RP cost.

Consume the rider at the qualifying spell’s **cast commitment**, after legal preflight confirms the adjusted cost can be paid. A countered cast still consumes it. An unaffordable/illegal attempted cast never commits and does not consume it.

For Ready, consumption/payment occurs at preparation, not release. This Resonance Influence cast cannot retroactively alter its own already-paid price.

One pending Resonance Influence per target across casters; successful Ease or failed-save Burden replaces the old record. Successful Burden save does not.

No rank/repertoire access, Fractured, Dissonance/Refrain, surcharge ceiling or spell legality bypass.

**NEW:** mode/save/window and final-price modifier pipeline.

### 12. Enthrall

**Action; 30 ft; V/S/F; NEW concentration up to 1 minute.**

Choose **up to three creatures** you perceive within 30 ft that can hear you. Each makes a **NEW WIS save** independently.

On failure, that creature has disadvantage on **all actual Perception checks** for the duration. Unlike Enthralling Tune, there is no exception for checks concerning the caster/tone because the rank-1 source prints the broader Perception penalty.

No invented passive-Perception `−5`, automatic Search failure, Hidden state, Charmed, Stunned, Action loss, or awareness deletion.

Hearing is required only when the spell is applied; no continuing sound/performance tether is added. Advantage/disadvantage resolves normally. Multiple Enthrall applications do not stack disadvantage.

**NEW:** three-target cap, hearing gate, WIS saves and concentration up to 1 minute.

I chose **three targets** as the minimal fixed plural cap that keeps rank-1 “nearby creatures” materially above the one-target cantrip without silently turning it into the rank-2 source’s explicit “all creatures that can hear you.”

### Numerical / human-balance flags

These are authoring-complete enough to card, but several deserve deliberate table testing:

- **Sleep:** no-save Unconscious against a fixed 24-current-HP budget is potentially encounter-defining at low level even with the hard-control guard.
- **Mesmerize:** Stunned plus separate unaware is powerful for 2 RP.
- **Distract:** Reaction-based full Action cancellation is extremely valuable even with an INT save and hard-control allowance.
- **Command:** exact command vocabulary will determine whether 2 RP is too efficient.
- **Hideous Laughter:** Prone + Incapacitated with concentration/repeat saves remains strong.
- **Faction Charm:** one-hour affinity + Persuasion advantage may dominate social scenes depending on task DCs.
- **Alignment Suggestion:** temporary canonical alignment modification can interact sharply with alignment-gated combat effects.
- **Resonance Influence:** Burden making 0-RP cantrips cost 1 RP materially changes low-resource play.
- **Enthrall:** three targets / one minute / concentration is a deliberately bounded NEW completion and should be tested against Lullaby and Enthralling Tune.

### Rank-2 Enthrall disposition

The separate **Enchantment rank-2 / Core 349 / 3-RP** placement remains:

> **PRESERVED SOURCE FINDING — UNASSIGNED / NOT SELECTABLE**

It is **not** merged into rank-1 Enthrall, not treated as an upcast, and receives no class access from the rank-1 rows. Its explicit “all creatures that can hear you / WIS negates” source remains intact for a later access/identity conflict decision. :chatgpt-content-reference{index="1"}

**Disposition:** all twelve rank-1 Enchantment identities are **SOURCE-RECONCILED / DRAFTABLE**. Catalog remains **210 reviewed / 638 unfinished** until exact cards return for manuscript approval.

