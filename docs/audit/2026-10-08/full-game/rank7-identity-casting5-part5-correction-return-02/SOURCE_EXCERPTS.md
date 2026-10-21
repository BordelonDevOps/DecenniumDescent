# Rank7 bounded correction02 — exact source excerpts

These are excerpts, not substituted sources. Complete bytes are in the preserved input archives and the supplied sources/ files. The local diagnostic script was inspected, not executed.

## sources/DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_CREATION_PLAYTEST.md

Bytes 20258; SHA256 `5c9f9ab4c9b485546a249637a335f56193dd3d58e58c451f9561c4e330c09a84`.

```text
17: 
18: An ancestry/background feature, spell or item that remains mechanically unresolved is a visible unfinished dependency. A checked box or a saved companion character does not resolve that dependency.
19: 
```

```text
42: 1. Record the gained class and new class level. Recalculate total level and PB: +2 at total 1–4, +3 at 5–8, +4 at 9–12, +5 at 13–16, +6 at 17–20.
43: 2. Add one new unspent Hit Die of the gained class’s size. Previously spent Hit Dice remain spent; gaining this die does not refresh any earlier die. For HP, roll that die or use its fixed rounded-up average: d6→4, d8→5, d10→6, d12→7. Record the base result before CON. This includes taking a new class’s first level after character level 1; maximum first-level HP is never granted again.
44: 3. Apply exactly the gained class’s acquisition row, automatic improvements and class-level prerequisites. Complete its choices and any newly reached Arch/Hero gate. Automatic grants, scheduled selections and ASIs are distinct; do not pay a selection twice or grant an extra selection because the same feature appears in a legacy table.
45: 4. At an ASI milestone, increase one score by 2 or two scores by 1, normally no higher than 20, or select one eligible operational feat. Ordinary milestones are class levels 4/8/12/16/19; Oracle uses 4/8/14/19. Follow any already-reviewed specific exception. No starting feat or repeatable feat is implied. [Eight complete feat options](FEAT_PLAYTEST_INDEX.md) do not make the other 327 complete.
46: 5. Update legal repertoire, prepared capacity, class scaling and resource maxima at the gained **class** level. Use class-specific Druid preparation, Wizard spellbook/matrices and other explicit rules before generic acquisition defaults. New capacity does not provide an unnamed spell, an unearned choice, a filled Echo record or an extra prepared spell without the required preparation procedure.
```

## sources/DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md

Bytes 17321; SHA256 `adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81`.

```text
11: An ability is known only if granted or selected by the draft schedule. Satisfy all printed prerequisites, target legality, action availability, recharge and resource costs before spending anything. A failed legal attack/save attempt still pays; an illegal activation spends nothing. No resource goes below 0 or above its cap. A class feature name shared with a spell does not grant both versions; use the version selected, with its own cost and timing. Names and source text are preserved; the current card is the operational draft.
12: 
13: ## Action and timing limits
14: 
15: One regular Action, one Bonus Action if a feature permits it, normal movement and one Reaction between starts of your turns. A free trigger costs no Action only if expressly stated. All grants share **one extra full Action per creature per round**. An extra Action cannot grant another Action, recharge itself, or start another extra-Action grant. It supplies no extra Bonus Action or Reaction. A card granting additional attacks is not permission to repeat all class riders on every hit: obey each rider's frequency.
16: 
17: Recharge N sets a counter to N after use; reduce once at the start of the owner's regular initiative turn, whether able to act or not. Extra turns/Actions do not tick it. Outside combat tick once per 6 elapsed seconds, without double counting. Recharge 2 used on turn 1 is ready on turn 3. A positive counter can be reset/shortened at most once per ability per round. Zero counters are not legal reset targets and expend no reset use. Resets never restore RP or per-rest uses or grant an immediate activation.
```

```text
45: Four classes have no direct Core V 2 pool row. For this pilot, Crimson Agent uses the Cleric curve multiplied by 0.5; Dragoon, Monk and Thief use that curve multiplied by 0.35, rounded to nearest integer with halves upward, minimum 1. These fallback factors come from the preserved `src/data/resonance-economy.js`; they are explicitly distinguished from direct book tables. The generic Core V 2 Oracle RP row is rejected for this class suite because Oracle's protected class contract uses Revelation Charges only. Oracle never receives RP or ordinary spell access. Retune here means one recovery at the end of a completed short rest, not an unrestricted action.
46: 
47: For a reproducible pilot, retain the protected **Dissonance** layer with Core V 2 numeric RP costs. This combination is a new integration decision: do not also roll a second historical Burn/fizzle system on top of it. Limit=max(4, 2+PB+max(0, casting modifier)). Before a ranked cast, Dissonance at limit/limit+3/limit+6 adds 1/2/3 RP respectively; at limit+6 ordinary casters cannot cast rank 1+. At limit+3 ordinary Overcast is unavailable. A cast then adds base Dissonance 0 at rank 0, 1 at ranks 1–5, 2 at ranks 6–9. Immediate repeated casts of the same named spell add 1, 2, then 3 maximum. Another named spell resets the repeat counter but not accumulated strain. Apply the class's exact cadence reduction/vent; never infer a free RP reduction. Printed class techniques pay printed costs and cause no automatic spell Dissonance unless tagged or expressly described as spells, Echo releases or Matrix casts. For a Mage/Wizard class card tagged as a spell, use the rank printed in normalized data; its rank is fixed at acquisition and does not rise with S. Other techniques are not counterspell able unless their card says so.
48: 
49: Retune recovers max(0, round(max RP/4)+casting modifier), never above maximum, and clears Dissonance. A long rest restores RP and clears Dissonance. Optional 10-minute meditation once/day recovers positive casting modifier RP and reduces Dissonance by PB+positive modifier. A regular turn with no spell or magical class ability loses 1 Dissonance; an Action spent Grounding without casting loses PB instead (not both). Merely ending an encounter does not clear accumulated Dissonance. Refrain survives idle/weapon turns unless a class explicitly clears it. Lich/Necromancer may force ranked casts through Fracture; after resolution take direct unpreventable trauma equal to rank×1/2/3 at the three strained states, minimum 1, based on state before casting. This trauma cannot generate resources or trigger damage-sharing. They still pay RP and meet rank gates.
50: 
51: Generic Overcast is excluded from the initial suite configuration until its options are separately fixed; cards such as Overchannel have their own exact costs and gates. Core V 2's original Burn procedures, older rank×2 costs and smaller companion RP tables remain preserved as alternatives, not silently combined. This configuration is suit able for comparing class drafts, not a claim that all historical magic sources already agree.
```

## Wizard source `/engine/11` — first-family exemption and repeats

```text
PROTECTED DISSONANCE INTERFACE. The first cast of each different prepared matrix family during an encounter generates 0 BASE Dissonance. This exemption affects only base strain. Refrain and explicitly printed strain costs still apply; the suite disables generic Overcast and does not layer historical Burn onto Dissonance. Repeating a matrix family follows normal Refrain immediately. Preparing duplicates or differently modified copies of the same underlying spell never refreshes the exemption.
```

## Exact Ready authority — registry06 `/entries/1/exactAuthority`

## Ready

Spend an Action to declare a perceivable trigger and one legal Action-time action or movement. It expires next regular own-turn start. **NEW:** only one pending Ready per creature; replacing it loses the prior setup and any paid held-spell costs. No Bonus Action/Reaction ability, long ritual or multi-minute activity can be prepared by generic Ready.

The trigger happens first, then the readied response immediately follows before later events, unless a specific effect explicitly interrupts. On release spend the normal Reaction and recheck target, range, sight/perception, line of effect, ammunition and other prerequisites. An invalid or declined occurrence spends no release resource; the Ready can wait for another valid occurrence before expiry. This does not undo setup costs. Once released, it is consumed.

For ordinary nonspell actions, feature/ammunition costs are paid on release unless text charges setup. A readied **Attack Action** gets its legally available ordinary attack count; a feature limited to your own turn does not thereby work off-turn. Core Overwatch is explicitly one ranged attack, not that full Attack Action and not Soldier's distinct engine.

A readied spell is actually **cast at preparation**: choose spell/mode, verify legality, pay RP/material/other costs, provide components, resolve Dissonance/Refrain and cast-trigger effects once. Counterspell/cast-interruption opportunity occurs then, not again at release. Every held spell requires concentration, even ordinarily non-concentration spells; incompatible prior concentration ends. Lost concentration loses the held spell and costs. NEW: select the legal target/area point at release and recheck legality without repaying. At release the hold continues as ordinary spell concentration if required, otherwise ends after resolution. Expired/replaced/countered held spells do not refund paid costs.

Ready movement grants a separate current-Speed budget on release, pays terrain costs and can provoke ordinary opportunity attacks. It grants no extra Action, Bonus Action or interaction.

Focused stance's Reaction restriction also blocks an ordinary Ready release; Ready does not create a Counterspell exception. Holding a spell does not waive any current Reaction prohibition.

**Spell-effect duration begins at release.** Its normal duration is anchored when the effect manifests, while Ready expiry and held concentration already run from preparation. A source explicitly tying a particular consequence to casting/preparation retains that consequence's stated clock. No casting cost, Refrain, Dissonance or cast trigger occurs a second time merely from release.


## Complete Metamagic Adept source-directed record — magic_core.json `/records/21`

```json
{
  "featId": "metamagicAdept",
  "procedure": "Keep personal spellcasting and total character level4. NEW grant a separate pool of two feat sorcery points, maximum2, initially full and restored to2only by a beneficial Long Rest. There is no RP/RC/HP/charge exchange, class-resource conversion, overcap or refill from ordinary spell refunds. At acquisition permanently choose two distinct modes from the finite three-mode menu below, based explicitly on the actual Mage Metaspell Access card; this does not acquire that Mage card or its Long-Rest use.\n\nReach: spend1point when committing a personal spell cast to add30feet to its finite positive numeric casting range. Self,Touch,unlimited and a separate effect/command radius do not gain range. Widen: spend1point at commitment to add5feet to one circular/spherical area radius or one cone length of that actual spell; choose the one eligible dimension in advance, not all independent areas/parameters. It does not create an area on a single-target spell. Sculpt: spend1point at commitment to choose up to max(1,actual casting ability modifier) eligible creatures in that spell’s initial area; they automatically succeed on its initial save and take no damage if that success would normally halve damage. Their later saves/ticks and nondamage successful-save consequences follow the original spell; there is no permanent friendly-fire immunity.\n\nNEW one metamagic mode total per cast across this feat and Mage Metaspell Access; declare which actual source pays. You cannot use two points for two modes or duplicate a class mode on the same cast. Other separately applicable feats keep their exact scopes. Spell Sniper doubles the printed numeric range first, then Reach adds30; it does not double Reach’s30. The chosen mode adds no spell rank, RPdiscount, Action, concentration slot or second cast. Commit the point with the legal spell; a later miss, save, counter or interruption refunds neither. Illegal mode/target declarations spend nothing. The spell still needs all its own resources, components and access.",
  "newChoices": "2-point LRpool; two permanent choices from actual three-mode comparison;1point/cast and one mode across class/feat; precise timing/range order.",
  "workedCases": [
    "A caster with Reach and Sculpt spends1point to extend a60-foot ranged spell to90feet. If Spell Sniper legally applies too, range is150feet:120from doubled printed range plus30.",
    "After spending its second point, the caster cannot convertRPinto more sorcery points. Having the Mage card’s own use does not allow an additional mode on a cast already modified through this feat."
  ],
  "dependencies": [
    "Mage Metaspell Access complete card",
    "Action/cast commitment",
    "Spell Sniper proposed range order"
  ],
  "procedureScope": "complete-proposed-feat",
  "questionId": "MF-22",
  "sourceObject": {
    "id": "metamagicAdept",
    "name": "Metamagic Adept",
    "description": "You have learned to modify your spells in subtle ways.",
    "prerequisite": "Spellcasting ability, Level 4",
    "effect": "Learn 2 metamagic options, gain 2 sorcery points",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "sourceObjectSha256": "6789eefb5394fffc5e00aeb163e3ca3428ba6332670027c2c426648730fcf615",
  "originalQuestion": "Preserve two selected metamagic options and two sorcery points, but neither a point-to-RP exchange nor an imported external option list is authorized. Compare the complete provisional Mage Metaspell Access card; explicitly resolve feat option identities, costs, recovery, timing and combining modes. A matching metamagic tag does not grant class acquisition or convert one-per-rest uses into points.",
  "status": "unadopted-feat-interface-proposal",
  "authoredCasesAreRuntimeTests": false,
  "priorReviewedComponentCarried": false,
  "exactCandidateStatus": "Source-authored exact candidate; separate exact review pending. Selection/runtime disabled. Original catalogs unchanged.",
  "sourceVerdictDecision": "Retain the MF-22 complete grant/procedure and boundaries. 2-point LRpool; two permanent choices from actual three-mode comparison;1point/cast and one mode across class/feat; precise timing/range order. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "sourceVerdictId": "FEAT327-SOURCE-2026-10-11",
  "payloadOperational": "Keep personal spellcasting and total character level4. NEW grant a separate pool of two feat sorcery points, maximum2, initially full and restored to2only by a beneficial Long Rest. There is no RP/RC/HP/charge exchange, class-resource conversion, overcap or refill from ordinary spell refunds. At acquisition permanently choose two distinct modes from the finite three-mode menu below, based explicitly on the actual Mage Metaspell Access card; this does not acquire that Mage card or its Long-Rest use.\n\nReach: spend1point when committing a personal spell cast to add30feet to its finite positive numeric casting range. Self,Touch,unlimited and a separate effect/command radius do not gain range. Widen: spend1point at commitment to add5feet to one circular/spherical area radius or one cone length of that actual spell; choose the one eligible dimension in advance, not all independent areas/parameters. It does not create an area on a single-target spell. Sculpt: spend1point at commitment to choose up to max(1,actual casting ability modifier) eligible creatures in that spell’s initial area; they automatically succeed on its initial save and take no damage if that success would normally halve damage. Their later saves/ticks and nondamage successful-save consequences follow the original spell; there is no permanent friendly-fire immunity.\n\nNEW one metamagic mode total per cast across this feat and Mage Metaspell Access; declare which actual source pays. You cannot use two points for two modes or duplicate a class mode on the same cast. Other separately applicable feats keep their exact scopes. Spell Sniper doubles the printed numeric range first, then Reach adds30; it does not double Reach’s30. The chosen mode adds no spell rank, RPdiscount, Action, concentration slot or second cast. Commit the point with the legal spell; a later miss, save, counter or interruption refunds neither. Illegal mode/target declarations spend nothing. The spell still needs all its own resources, components and access.",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

## Operational boundary

The milestone repair makes the teaching actor internally consistent; it does not enable the source record’s false selectionEnabled/exactApproved/runtimeApproved flags. The positive feat branch remains conditional. A failed two-mode declaration remains a negative compatibility example, not implemented feat use.
