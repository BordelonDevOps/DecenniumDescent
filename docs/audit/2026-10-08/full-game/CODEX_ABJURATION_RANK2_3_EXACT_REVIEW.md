# Exact thirteen-card Abjuration manuscript review

All13 source-reconciled identities are now authored in a candidate excluded from the loader.13 IDs/18 placements/18 Core blocks and every class-access row are preserved exactly; required fields and types pass local source/structure checks. Current selectable catalog remains107/848 with741 unfinished. This requests manuscript review, not runtime/balance/whole-game approval.

Please review the COMPLETE playable fields below and the following concrete clarifications. Approve or provide exact repairs. The candidate physical SHA256 is fd0732751436b018e0a35e4297d550dededa8723adbb6ab9ace4f755b463750e.

1. COUNTERSPELL SOURCE CORRECTION. Your first proposal used a binary non-task check. The EXISTING approved Core overlay, quoted verbatim below, explicitly uses four degrees/natural shifts for fixed-DC ability/task checks, collapsing upper/lower degrees where only success/failure is printed. The separate Wizard/Mage class cards say ability check and supply no exception. Candidate therefore preserves the existing rule rather than inventing a new ordinary-spell exception: actual spellcasting ability+PB vs10+2*rank, existing degree/natural rules, then binary outcomes. Confirm this evidence-based correction. Examples: natural20+0 vsDC22 is Failure improved to Success; natural1+9 vsDC10 is Success worsened to Failure; natural1+20 vsDC10 is Critical Success worsened to Success. No extra counter power or malfunction attaches to critical degrees. Prefer coherent existing roll semantics across ordinary/class Counterspell. The one-attempt-per-creature/pending-cast rule should apply across that creature's ordinary and class Counterspell attempts, not reset by switching namespaces; class acquisitions/costs/ranks/recharge stay distinct. Confirm.
2. COUNTER TIMING. Every interruptible cast commits costs, concentration transition and its actual Dissonance/Refrain/class beginning hooks once BEFORE nested reactions, preserving nested cast chronological history. Later success/effect hooks keep exact source timing. I will align SPELL_INTEGRATION_RULES step order with this agreed manuscript rule after approval; no claim of runtime implementation. Ready opens at preparation only. One negated counter resumes its parent without recast/payment/history overwrite; no hard-denial ledger expenditure.
3. FALLING/OVERLAP. A vertical type wall cannot provide a perch. If permitted ordinary Falling leaves a matching creature straddling Barrier of Faith/Magic Circle, candidate allows it to finish leaving the overlap to either side by normal paid/legal movement, then ordinary boundary rules resume. No free movement, added fall distance, damage or relocation. This replaces the otherwise ambiguous same-side wording when a body descends from above the wall with no preexisting legal side. Confirm or give a complete alternative.
4. CORRUPTION CLEANSE. Keep your ordinary Corrupted-condition eligibility. An environmental source must explicitly be minor/cleanseable; its entire active extent must fit the10ft-radius/10ft-high area, unless it explicitly supports localized cleansing, in which case only the bounded portion is removed. This prevents cleansing an entire continent by selecting a small overlapping circle. No numeric tracks or original causal major source removal.
5. BARRIER FIELD. Direct damaging casts trace caster-to-target/initial-area-origin, so choosing the damaging area center on the far side is not an automatic bypass. Damage blocking does not depend on a friendly label or recipient consent. Independent preexisting effects use actual source origin. Creature/nonattack movement and nondamaging magic remain allowed; separable legal nondamaging parts resolve. No global antimagic or no-attack privilege from inside. Confirm this full origin rule or repair precisely.
6. REMOVE CURSE. A perceived creature/object is the legal target regardless of whether the caster has found its curse. Pay before the Director resolves hidden removable curses. With no eligible curse, no removal/refund or separate diagnostic report. This distinguishes ordinary legal-target validation from free probing of hidden metadata. Known identifiable curse can be selected; otherwise Director selects one actual removable hidden curse. Existing special-cure and Oracle exceptions retained.
7. RESONANCE ANCHOR. Own-concentration-dependent target is explicitly ineligible at preflight, avoiding payment for a known target that its necessary concentration transition would end. Other casters maintain their own concentration. Proposed fix-in-place meaning fixes spatial origin/recentering, without freezing otherwise source-authorized radius/shape evolution; duration/pulses/resources continue. It cannot target another Anchor and remains dispellable itself. Confirm location-versus-shape scope.
8. ALIGNMENT SANCTUARY. Your attempt/turn phrase needs one clock. Candidate records one entry save result until target's next regular START (virtual marker, or+6seconds outsideinitiative); result applies to all voluntary/forced/carried/teleport entries in that window. No reroll after failure via repeated pushes or recasts by same source. Different caster wards remain independent. Success on one ward never bypasses another. Rank6 Conj requires caster's BOTH actual canonical axes before casting, rather than letting unknown caster alignment create an admits-no-one ward. Both actual class modes are complete; unassigned Abjrank6 benefits remain preserved/unavailable. Confirm these precise completions.
9. Protection from Energy retains your eight-type immunity list, not resistance, withoutconcentration; oneall-casterapplication. Corruption damage is expressly not in the selectable list either. Protection from Scrying retains your explicit information-gathering interpretation, not blanket immunity to arbitrary damage from a school. Both source descriptions remain preserved.

## Existing Core roll source

## Rolls

Choose the roll type before rolling. Use the actual ability modifier, including negative values, and normal proficiency only when applicable. Existing advantage/disadvantage chooses the higher/lower of two d20s; multiple sources do not stack, and any advantage plus disadvantage cancels. Add other legal modifiers once. Fractions round down unless a rule specifies otherwise. One tile is 5 feet. Class L, S and effect M retain their definitions in the shared class rules.

**Attack:** roll d20 plus the appropriate attack modifier against AC. Meeting AC hits. Natural 1 always misses; natural 20 always hits and critically doubles damage dice, not flat modifiers. Beating AC by 10 is not a critical hit. An explicit broader critical range does not stack with another; use the broadest eligible range. In this overlay, a natural result below 20 in that range must still meet AC unless the feature expressly says it always hits.

**Task, skill or tool check against a fixed DC:** total at least DC+10 is Critical Success; at least DC is Success; at most DC-10 is Critical Failure; other totals below DC are Failure. Natural 20 then improves one degree and natural 1 worsens one, bounded at either end. A task printing only success/failure collapses the two upper degrees to success and two lower degrees to failure; no extra consequence is invented. A natural 20 can still fail an otherwise impossible check, and a natural 1 with sufficient modifiers can still succeed.

**Saving throw:** total at least DC succeeds; otherwise it fails. Natural 1 and 20 have no generic special outcome. A printed failure by 5 or 10 compares the final total with the DC; it does not add an unprinted critical-save system. Death saves are the specific exception below.

**Opposed check, new provisional tie rule:** compare final totals. Higher wins; an exact tie leaves the existing state unchanged, so the initiating creature fails to change it. Do not turn task natural shifts into hidden numeric modifiers. A maneuver explicitly printing degree outcomes must specify how those apply.


## Exact playable cards

```json
[
  {
    "id": "dispel-magic-lesser",
    "activation": "Action",
    "rangeFeet": 30,
    "targets": "One individually perceptible ongoing magical effect within range and line of effect, generated by a spell of actual recorded rank 0, 1 or 2.",
    "duration": "Instantaneous",
    "concentration": false,
    "components": [
      "V",
      "S",
      "F"
    ],
    "resolution": "Automatic for an eligible effect; no saving throw or check.",
    "effect": "End only the selected effect and invoke its ordinary ending procedure and dependencies. Its original generating spell rank controls, using its caster's class placement when class-cast; RP cost, discount, caster level and the dispeller's access do not change that rank.",
    "scaling": "None.",
    "limitations": "No permanent enchantment or magic-item removal, class-engine or creature-trait removal, mass purge, retroactive healing/resource repair, or guessing an unknown spell rank. A curse qualifies only when it is itself an otherwise eligible ongoing spell effect within the rank ceiling and is not specially protected. Mere binary awareness of nearby magic does not identify a selectable individual effect. Apply SPELL_INTEGRATION_RULES.md for actual class access and repertoire, costs before resolution, components, concentration, Dissonance/Refrain and exact source cadence. No automatic scaling or generic upcast.",
    "designNotes": "PRESERVED: Action, 30 feet, V/S/F, instantaneous and low-level dispelling. NEW CONFLICT RULING: ambiguous plural effects means one selected effect per cast; Core Tier 2 is reconciled to spell rank at most 2, not a broader character tier."
  },
  {
    "id": "protection-from-energy",
    "activation": "Action",
    "rangeFeet": 30,
    "targets": "One willing creature you can perceive within range and line of effect, including yourself.",
    "duration": "If cast in initiative, expires at the caster's tenth future regular-start marker; preserve that virtual marker through order changes or departure. If cast outside initiative, expires 60 seconds after application; entering initiative preserves that absolute deadline. An already-passed start does not count.",
    "concentration": false,
    "components": [
      "V",
      "S",
      "F"
    ],
    "resolution": "Automatic after legal casting.",
    "effect": "Choose acid, cold, fire, lightning, thunder, force, necrotic or radiant. The target is immune to damage of that one type for the duration.",
    "scaling": "None.",
    "limitations": "Bludgeoning, piercing, slashing, poison, psychic and Corruption are not selectable energy types here. One Protection from Energy per target across all casters: a later application replaces the old type and owns its own deadline; stale cleanup cannot erase the replacement. Immunity blocks only the selected damage, not attached conditions or riders unless those independently require positive damage. It does not undo resolved damage or protect against a transferred post-defense branch expressly skipping a second mitigation/prevention stage. A magical weapon's physical damage remains physical. Apply SPELL_INTEGRATION_RULES.md for actual class access and repertoire, costs before resolution, components, concentration, Dissonance/Refrain and exact source cadence. No automatic scaling or generic upcast.",
    "designNotes": "PRESERVED: immunity, Action, 30 feet, V/S/F and 1 minute without concentration. NEW: eight-type energy list, willing target, one all-caster application and explicit damage-only boundaries."
  },
  {
    "id": "barrier-of-faith",
    "activation": "Action",
    "rangeFeet": 10,
    "targets": "A fixed 10-foot-long, 10-foot-high, negligible-thickness vertical wall on solid ground or a suitable approximately horizontal immobile surface. Its entire wall must fit in legal space within range and line of effect.",
    "duration": "Concentration, up to 1 minute. If cast in initiative, expires at the caster's tenth future regular-start marker; preserve that virtual marker through order changes or departure. If cast outside initiative, expires 60 seconds after application; entering initiative preserves that absolute deadline. An already-passed start does not count. Ends earlier if concentration ends.",
    "concentration": true,
    "components": [
      "V",
      "S",
      "F"
    ],
    "resolution": "Choose one exact current source-authorized creature type or tag. No saving throw. The initial wall cannot intersect a matching creature's occupied space.",
    "effect": "Matching creatures cannot physically cross the wall in either direction; being carried does not bypass their restriction. Creatures can start on either side. Nonmatching creatures, objects, attacks, spells, gas and sound pass normally. Teleportation or planar relocation does not physically cross it and is not blocked.",
    "scaling": "None.",
    "limitations": "No inferred taxonomy from appearance, name, ancestry, faction or lore. No HP, floor, platform, structural support, cover, collision damage or Action denial. Unsupported ordinary Falling is not arrested and gains no extra distance or lateral displacement. NEW GEOMETRY CLARIFICATION PROPOSAL: if permitted Falling leaves a creature straddling the wall, it may finish leaving the overlap to either side using ordinary legal movement; once clear, normal crossing restrictions resume. This grants no free movement or return crossing. Apply SPELL_INTEGRATION_RULES.md for actual class access and repertoire, costs before resolution, components, concentration, Dissonance/Refrain and exact source cadence. No automatic scaling or generic upcast.",
    "designNotes": "PRESERVED: 10-foot wall, Action, 10-foot range, V/S/F, concentration 1 minute and chosen-type blocking. NEW: height/thickness, full placement legality, exact type/tag, two-way crossing, carriage and no-support limits. The permitted-Falling overlap exit procedure awaits exact review."
  },
  {
    "id": "corruption-cleanse",
    "activation": "Action",
    "rangeFeet": 30,
    "targets": "Either one willing creature you perceive within range and line of effect, or a fixed 10-foot-radius, 10-foot-high area centered on a point you perceive within range and line of effect.",
    "duration": "Instantaneous",
    "concentration": false,
    "components": [
      "V",
      "S",
      "F"
    ],
    "resolution": "No saving throw. Select one actual qualifying condition or environmental effect; this is removal, not HP healing.",
    "effect": "Creature mode removes one ordinary Corrupted condition record without explicit special protection. The reviewed ordinary Corrupted condition counts as a minor corruption effect for this spell. Area mode removes one environmental Corruption effect whose actual source explicitly calls it minor and permits cleansing. NEW SCOPE CLARIFICATION PROPOSAL: that environmental effect's entire active extent must fit within the selected area, unless its own source expressly permits cleansing just the bounded portion; in that case cleanse only the portion inside.",
    "scaling": "None.",
    "limitations": "Does not invent minor status for unknown effects, reduce Unity Exposure or any numeric Corruption/Exposure track, restore former alignment or undo a historical shift, heal HP/Wounds/death, or remove an intrinsic Oracle Curse/Burden. Removing a symptom does not end its major/protected cause. No immunity to a later legal reapplication is granted. If a source continuously reapplies Corrupted, its own timing continues without a fabricated grace period. Apply SPELL_INTEGRATION_RULES.md for actual class access and repertoire, costs before resolution, components, concentration, Dissonance/Refrain and exact source cadence. No automatic scaling or generic upcast.",
    "designNotes": "PRESERVED: Action, 30 feet, V/S/F and instantaneous minor-corruption cleansing on creature/area. NEW: ordinary Corrupted as one eligible minor effect, willing creature, one effect per casting, bounded environmental area and explicit no numeric-track reduction."
  },
  {
    "id": "faction-ward",
    "activation": "Action",
    "rangeFeet": 30,
    "targets": "One fixed 10-foot-radius, 10-foot-high area centered on a point on suitable approximately horizontal immobile ground or surface within range and line of effect.",
    "duration": "Concentration, up to 1 minute. If cast in initiative, expires at the caster's tenth future regular-start marker; preserve that virtual marker through order changes or departure. If cast outside initiative, expires 60 seconds after application; entering initiative preserves that absolute deadline. An already-passed start does not count. Ends earlier if concentration ends.",
    "concentration": true,
    "components": [
      "V",
      "S",
      "F"
    ],
    "resolution": "At casting choose one canonical factionId permitted to you under Faction Seal's reviewed procedure: the Director records actual source or explicit campaign invocation permission. Naming a faction is not permission.",
    "effect": "A creature whose actual reputation record for the chosen faction is -3, -2 or -1 cannot willingly enter from outside. Creatures already inside can remain or leave freely. Missing standing is unknown and does not qualify. Forced movement, unsupported ordinary Falling and teleportation are not blocked.",
    "scaling": "None.",
    "limitations": "This is a behavioral ward, not a physical wall: it grants no AC/save bonus, attack immunity, detection signal, disguise-breaking, morality judgment, membership, credentials, legal authority, institutional protection or standing change. The visible ward may identify its invoked faction; observers can draw ordinary conclusions from visible behavior. Willingly using a carrier or ordinary movement into the area is voluntary entry; no forced movement is invented. Apply SPELL_INTEGRATION_RULES.md for actual class access and repertoire, costs before resolution, components, concentration, Dissonance/Refrain and exact source cadence. No automatic scaling or generic upcast.",
    "designNotes": "PRESERVED: Action, 30 feet, concentration 1 minute and negative-standing faction protection; M/F uses the class focus. NEW: fixed dimensions, permitted faction, willing-entry restriction, existing-occupant and forced/teleport exceptions."
  },
  {
    "id": "counterspell",
    "activation": "Reaction — when another creature you can perceive within range and line of effect begins casting a spell, after its casting costs and cadence are committed but before its effect resolves",
    "rangeFeet": 60,
    "targets": "One pending spell cast by the triggering creature. The spell needs an actual recorded rank; the Director may know that rank without revealing it to you.",
    "duration": "Instantaneous",
    "concentration": false,
    "components": [
      "V",
      "S",
      "F"
    ],
    "resolution": "PROPOSED SOURCE CORRECTION: make a spellcasting-ability check using the actual ability for the class through which you cast Counterspell, adding PB once, against DC 10 + twice the triggering spell's actual rank (rank 0 contributes 0). Use CORE_RESOLUTION_PLAYTEST.md's fixed-DC task degrees and natural shifts: at least DC+10 Critical Success, at least DC Success, at most DC-10 Critical Failure, otherwise Failure; natural 20 improves one degree and natural 1 worsens one. Collapse both upper degrees to success and both lower degrees to failure; invent no additional critical effect. This is not a spell attack or saving throw.",
    "effect": "Success negates the selected pending spell after its costs were committed; failure lets it continue. Every interruptible cast first commits its RP/material/other costs, components, concentration transition, Dissonance/Refrain and exact beginning/casting hooks once, then opens the interruption window. A surviving cast later resolves its effect and outcome-dependent hooks. Negation gives no refund, no successful-effect trigger and no restoration of old concentration. Counterspell is itself a spell and can be countered. Resolve nested counters last-in, first-out; if a counter is negated, the earlier pending spell resumes without paying or casting again. Resuming a parent never rewrites the later nested cast's Refrain/Dissonance history.",
    "scaling": "None. No automatic success against lower ranks and no generic upcast.",
    "limitations": "One attempt per creature against a particular pending cast, even with an additional Reaction. After a failed attempt another eligible creature may react; once negated, the spell supplies no further interruption trigger. All reactions need their own legal remaining resource, components, range and current source permissions. Attempting does not reveal spell identity/rank; never treat an unassigned rank as 0 or estimate it from RP. Ready opens its cast-interruption window at preparation, not release. Countering is not whole-Action/turn hard denial and does not spend that ledger. Ordinary Counterspell requires ordinary repertoire/class access and rank-3 cost; Wizard/Mage same-named class cards keep their own separate acquisition, printed costs, ranks, recharge and text. Apply SPELL_INTEGRATION_RULES.md for actual class access and repertoire, costs before resolution, components, concentration, Dissonance/Refrain and exact source cadence. No automatic scaling or generic upcast.",
    "designNotes": "PRESERVED: both Abjuration/Universal rank-3 placements, Reaction, 60 feet, V/S/F and instantaneous interruption. NEW: actual casting ability+PB against DC 10+2*rank, one attempt per pending cast, hidden-rank handling and nested timing. SOURCE ISSUE: conference proposed binary check, but existing Core overlay expressly uses four-degree task checks collapsed when only success/failure is printed; this exact candidate proposes retaining that established rule."
  },
  {
    "id": "magic-circle",
    "activation": "Action",
    "rangeFeet": 10,
    "targets": "One fixed center point on suitable approximately horizontal immobile ground or surface you can perceive within range and line of effect, with space for a 10-foot-radius circle.",
    "duration": "Concentration, up to 1 minute. If cast in initiative, expires at the caster's tenth future regular-start marker; preserve that virtual marker through order changes or departure. If cast outside initiative, expires 60 seconds after application; entering initiative preserves that absolute deadline. An already-passed start does not count. Ends earlier if concentration ends.",
    "concentration": true,
    "components": [
      "V",
      "S",
      "F"
    ],
    "resolution": "Choose one exact current source-authorized creature type/tag. No saving throw. The initial lateral boundary cannot intersect a matching creature's occupied space.",
    "effect": "Create a visible 10-foot-radius circle with a 10-foot-high lateral cylindrical boundary. Matching creatures outside cannot physically cross that lateral boundary inward. Matching creatures already inside may remain or leave freely; once outside, their re-entry is blocked. Carriage does not bypass the restriction. Both actual Abjuration and Universal class placements use this same procedure.",
    "scaling": "None.",
    "limitations": "No inferred taxonomy, reverse trapping mode, Action denial, antimagic, HP, damage or structural support. Objects, attacks, spells, sound, gas and nonmatching creatures are not blocked. No magical roof or floor: travel over the top or legitimately beneath the wall is outside it. Teleportation/planar relocation is not physical crossing and is not prevented. Unsupported ordinary Falling is not arrested or given extra movement. NEW GEOMETRY CLARIFICATION PROPOSAL: if permitted Falling ends with a matching creature straddling the boundary, it may leave that overlap to either side by ordinary legal movement; once clear the entry rule resumes, without free movement or return crossing. Apply SPELL_INTEGRATION_RULES.md for actual class access and repertoire, costs before resolution, components, concentration, Dissonance/Refrain and exact source cadence. No automatic scaling or generic upcast.",
    "designNotes": "PRESERVED: both rank-3 placements, Action, 10-foot cast range and 10-foot-radius circle/cylinder; M/F uses F. NEW CONFLICT RULING: concentration 1 minute replaces Instantaneous metadata. NEW: 10-foot height, one exact type, inward-only side boundary, existing occupants, teleport and no-support rules."
  },
  {
    "id": "dispel-magic",
    "activation": "Action",
    "rangeFeet": 60,
    "targets": "One individually perceptible ongoing magical effect within range and line of effect, generated by a spell of actual recorded rank 0 through 3.",
    "duration": "Instantaneous",
    "concentration": false,
    "components": [
      "V",
      "S",
      "F"
    ],
    "resolution": "Automatic for an eligible effect; no saving throw or check.",
    "effect": "End only the selected effect and invoke its ordinary ending procedure and dependencies. Its original generating spell rank controls, using its caster's class placement when class-cast; RP cost, discount, caster level and the dispeller's access do not alter it. Both actual Abjuration and Universal placements use this rank ceiling.",
    "scaling": "None.",
    "limitations": "No permanent enchantment or magic-item removal, class-engine or creature-trait removal, mass purge, retroactive healing/resource repair, or guessing an unknown spell rank. A curse qualifies only when it is itself an otherwise eligible ongoing spell effect within the rank ceiling and is not specially protected. Mere binary awareness of nearby magic does not identify a selectable individual effect. Apply SPELL_INTEGRATION_RULES.md for actual class access and repertoire, costs before resolution, components, concentration, Dissonance/Refrain and exact source cadence. No automatic scaling or generic upcast.",
    "designNotes": "PRESERVED: Action, 60 feet, V/S/F, instantaneous and both rank-3 placements. NEW CONFLICT RULING: Core Tier 3 means spell rank at most 3; the Universal generic description grants neither unlimited-rank dispelling nor a mass purge. One selected effect per cast."
  },
  {
    "id": "barrier-field",
    "activation": "Action",
    "rangeFeet": 15,
    "targets": "One fixed center point on suitable approximately horizontal immobile ground or surface within range and line of effect, with space for a 15-foot-radius hemisphere.",
    "duration": "Concentration, up to 1 minute. If cast in initiative, expires at the caster's tenth future regular-start marker; preserve that virtual marker through order changes or departure. If cast outside initiative, expires 60 seconds after application; entering initiative preserves that absolute deadline. An already-passed start does not count. Ends earlier if concentration ends.",
    "concentration": true,
    "components": [
      "V",
      "S",
      "F"
    ],
    "resolution": "Automatic after legal placement. Creation neither displaces nor damages creatures. The field is faintly visible.",
    "effect": "Create a 15-foot-radius hemisphere, 15 feet high, with no floor. In both directions its curved boundary blocks attack rolls whose attack/effect path crosses it, including melee reach, and blocks the directly damaging portion of harmful effects crossing it, including save-based or automatic magical damage. Damage from an area on one side does not propagate through the boundary to the other. NEW ORIGIN CLARIFICATION PROPOSAL: for a cast that directly deals damage, trace from its caster to the target or initial area origin; merely choosing the area center beyond the field does not bypass it. A damaging part that must cross is blocked regardless of friendly intent or recipient willingness. Other legal, separable non-damaging parts resolve normally.",
    "scaling": "None.",
    "limitations": "Creatures and ordinary nonattack movement cross freely. The field does not block ordinary light, sound or gas, nondamaging control or information magic, teleportation, or effects genuinely originating and resolving entirely on the same side. A previously established independent effect uses its actual source origin and is not ended by field creation. It grants no one-way attacks, HP, item identity, cover item, entrapment, floor, platform or structural support. Unsupported Falling crosses normally without extra movement. It does not erase resolved damage or negate an entire spell merely because its damage across the boundary is blocked. Apply SPELL_INTEGRATION_RULES.md for actual class access and repertoire, costs before resolution, components, concentration, Dissonance/Refrain and exact source cadence. No automatic scaling or generic upcast.",
    "designNotes": "PRESERVED: Action, 15-foot cast range, 15-foot hemisphere, V/S/F, concentration 1 minute and physical/magical attack protection. NEW: fixed visible hemisphere, two-way attack/direct-damage boundary, no floor, free creature passage and explicit nondamaging exceptions. Direct-damage origin/intent wording awaits exact review."
  },
  {
    "id": "remove-curse",
    "activation": "Action",
    "rangeFeet": 60,
    "targets": "One creature or object you can perceive within range and line of effect. No willingness or prior curse-detection requirement.",
    "duration": "Instantaneous",
    "concentration": false,
    "components": [
      "V",
      "S",
      "F"
    ],
    "resolution": "Pay and cast against the legal creature/object target before resolving its hidden afflictions. No saving throw. Select a known distinguishable curse; if eligible curse identities are hidden and more than one actual removable curse exists, the Director selects one without revealing unrelated metadata. If none is eligible, no curse ends and no paid cost is refunded; the spell grants no separate diagnostic report.",
    "effect": "End one actual inflicted affliction record classified as a curse that affects the selected target, invoking that curse's own ending procedure. No general spell-rank ceiling applies: this is curse removal rather than dispelling.",
    "scaling": "None.",
    "limitations": "Explicit non-removability, required special cures, protected information and source-specific restrictions override this generic removal. A name containing curse is not an affliction classification. Oracle intrinsic Curse, Burden, Boons and Manifestation cannot be removed or suspended. Ending a curse does not undo historical HP damage, alignment/reputation changes, resource payments, Wounds, death or other consequences unless that curse's actual ending rule explicitly does so. Ordinary observations of a real change remain possible. Apply SPELL_INTEGRATION_RULES.md for actual class access and repertoire, costs before resolution, components, concentration, Dissonance/Refrain and exact source cadence. No automatic scaling or generic upcast.",
    "designNotes": "PRESERVED: Action, 60 feet, V/S/F, instantaneous and ending one curse on creature/object. NEW: actual inflicted curse metadata, hidden-curse selection without prior detection, no fabricated rank cap or willingness, and distinct legal-target/payment versus hidden-effect-result timing."
  },
  {
    "id": "protection-from-scrying",
    "activation": "Action",
    "rangeFeet": 60,
    "targets": "One willing creature you can perceive within range and line of effect, including yourself.",
    "duration": "1 hour: expires 3,600 elapsed seconds after application; entering, leaving or reordering initiative does not change that deadline.",
    "concentration": false,
    "components": [
      "V",
      "S",
      "F"
    ],
    "resolution": "Automatic after legal casting. Check an information-gathering effect's actual generating source classification, using its real casting-class school placement where applicable.",
    "effect": "The target supplies no new information to effects explicitly classified as Divination or Scrying that attempt to perceive, locate, inspect, read, identify or otherwise obtain information about it. Apply this protection equally against hostile, neutral and beneficial information gathering. A multi-subject or area effect may still obtain permitted information about other subjects.",
    "scaling": "None.",
    "limitations": "No ordinary invisibility, concealment, false identity, attack defense, memory erasure, record deletion or retroactive protection. A class sense is blocked only insofar as its actual source classifies it as Divination/Scrying; the underlying class engine remains intact. Theme or guessed purpose is not classification. Known information remains known. Independent applications do not stack extra power and each retains its own endpoint. Apply SPELL_INTEGRATION_RULES.md for actual class access and repertoire, costs before resolution, components, concentration, Dissonance/Refrain and exact source cadence. No automatic scaling or generic upcast.",
    "designNotes": "PRESERVED: Action, 60 feet, V/S/F and divination/scrying immunity. NEW CONFLICT RULING: ongoing 1 hour without concentration replaces Instantaneous metadata; immunity is operationally defined as prevention of new information about one willing target, not a blanket damage/benefit immunity against a school name."
  },
  {
    "id": "resonance-anchor",
    "activation": "Action",
    "rangeFeet": 60,
    "targets": "One perceptible ongoing magical effect with a discrete spatial origin/area within range and line of effect, created by you or explicitly permitted for anchoring by its current source owner/controller. It cannot be Resonance Anchor, an effect permanently attached to a creature/carried object, or an effect currently dependent on your own existing concentration.",
    "duration": "Concentration, up to 1 minute. If cast in initiative, expires at the caster's tenth future regular-start marker; preserve that virtual marker through order changes or departure. If cast outside initiative, expires 60 seconds after application; entering initiative preserves that absolute deadline. An already-passed start does not count. Ends earlier if concentration ends. Also ends when the anchored target effect ends.",
    "concentration": true,
    "components": [
      "V",
      "S",
      "F"
    ],
    "resolution": "Automatic after legal casting. Check the own-concentration exclusion before committing this cast: it forbids targeting an effect that beginning Anchor would itself end.",
    "effect": "Fix the selected effect's spatial origin in its current position; a movable/recenterable zone loses that relocation permission while anchored. Ordinary dispelling cannot end the target, including otherwise eligible Dispel Minor, Dispel Resonance, Dispel Magic (Lesser) or Dispel Magic. Anchor itself remains normally dispellable at its own actual rank. NEW CLARIFICATION PROPOSAL: anchoring fixes location, not the target's unrelated source-authorized evolution of radius, shape or nonspatial effects; it neither freezes nor manufactures those source changes.",
    "scaling": "None.",
    "limitations": "Cannot target itself or another Resonance Anchor. No duration extension, replacement of the target's concentration, use/cost reset, revival, restored pulse, frozen expiry or retroactive Counterspell protection. The target can still end by its own concentration, duration, destruction, source conditions, special removal or explicit anchor-bypassing effect. Its original owner/controller can still exercise a printed ending permission. Another caster's anchored concentration spell still requires that caster's concentration. No class engine or full Time Loop implementation is granted. Apply SPELL_INTEGRATION_RULES.md for actual class access and repertoire, costs before resolution, components, concentration, Dissonance/Refrain and exact source cadence. No automatic scaling or generic upcast.",
    "designNotes": "PRESERVED: Action, 60 feet, V/S/F, fixing a magical effect and preventing ordinary dispel. NEW CONFLICT RULING: concentration 1 minute replaces Instantaneous metadata. NEW: spatial eligibility/controller permission, own-concentration exclusion, Anchor's removability and no mutual anchoring. Location-versus-size clarification awaits exact review."
  },
  {
    "id": "alignment-sanctuary",
    "activation": "Action",
    "rangeFeet": 60,
    "targets": "One fixed 10-foot-radius, 10-foot-high area centered on suitable approximately horizontal immobile ground or surface within range and line of effect. Your casting class selects Abjuration rank 3 or Shaman Conjuration rank 6; rank-6 Conjuration requires both of your canonical alignment axes explicitly recorded before casting.",
    "duration": "Concentration, up to 1 minute. If cast in initiative, expires at the caster's tenth future regular-start marker; preserve that virtual marker through order changes or departure. If cast outside initiative, expires 60 seconds after application; entering initiative preserves that absolute deadline. An already-passed start does not count. Ends earlier if concentration ends.",
    "concentration": true,
    "components": [
      "V",
      "S",
      "F"
    ],
    "resolution": "Snapshot the caster's actual canonical alignment at application; do not infer it from ancestry, faction, reputation, faith, appearance or conduct. Abjuration rank 3 uses Wisdom saves against your spell DC for opposed entrants. Conjuration rank 6 uses exact matching admission with no save. The snapshot is fixed for this application.",
    "effect": "Abjuration rank 3: a creature is opposed if at least one explicitly known axis is exact opposite to the snapshot (Lawful/Chaotic or Good/Evil). Neutral is never opposite; an unknown axis supplies no opposition, and does not erase a known opposite on the other axis. On an opposed creature's attempted entry from outside, roll its Wisdom save before entry, including forced movement, carriage or teleportation. NEW CADENCE CLARIFICATION PROPOSAL: record that success or failure for this source character, mode and target until the target's next regular-start marker; the current in-progress start never counts. A success permits entries during that window; failure blocks all non-Falling entry attempts during it without repeat rolls. Same-caster replacement/recasting does not reset this window. Outside initiative, use a fixed 6-second window and preserve its deadline if initiative starts. A failed physical entry stops before the boundary; a failed teleport leaves the creature at its origin without refunding committed teleport costs. Conjuration rank 6: only a creature with both explicit canonical axes exactly matching both snapshotted axes may enter from outside. Unknown is not matching. Nonmatching physical entry, forced movement and carriage stop before entry; a teleport attempt to place a nonmatching creature inside leaves it at origin after costs are committed.",
    "scaling": "None. Shaman's preserved Conjuration rank-6 access costs 13 RP before ordinary surcharges; extra RP or character level cannot select another placement.",
    "limitations": "Both modes allow existing occupants to remain or leave; once outside, entry restrictions apply. Unsupported ordinary Falling is not arrested, supplies no platform and adds no movement; it can place a creature inside. No AC/save bonus, healing, rest guarantee, resource recovery, attack immunity, concealment, morality compulsion or alignment change. The ward denies entry rather than Actions and does not consume the shared hard-denial ledger. Multiple casters' wards retain independent source permissions and save windows; no single ward's success bypasses another ward. The preserved rank-6 Abjuration aligned-benefits placement has no actual class-access grant and stays unassigned/unavailable; its vague benefits are not imported. Apply SPELL_INTEGRATION_RULES.md for actual class access and repertoire, costs before resolution, components, concentration, Dissonance/Refrain and exact source cadence. No automatic scaling or generic upcast.",
    "designNotes": "PRESERVED: Action, 60 feet, V/S/F, Abjuration rank-3 opposed-entry Wisdom save and Shaman Conjuration rank-6 same-alignment safe haven. NEW CONFLICT RULINGS: fixed 10-foot-radius/height and concentration 1 minute replace Instantaneous metadata; actual modes stay separate, unassigned rank-6 Abjuration benefits remain blocked. NEW: snapshots, entry/teleport/Falling handling and exact two-axis Conjuration matching. Proposed save-window/recast and rank-6 snapshot-validity completions await exact review."
  }
]
```
