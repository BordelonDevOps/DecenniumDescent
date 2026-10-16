# Director Review — AC4 Current Review 01

Use this with `SPELLS_MODEL.json`, the 70 frozen source bindings, and current accepted EPI-01–17 interfaces. The prose below is review guidance; the complete source/access records are structured in the model.

## Module decisions
**Spell Shield.** Pure redirection. Original cast/dealer/root/Null flag/concentration remain; no reflected-root creation.

**Alignment.** AC4-ALIGN-01 is NEW and scoped only to Alignment Lock/Anchor. Reviewed AP-AS-01 remains untouched and source-specific.

**Dampening price.** The field's +2 is a mandatory spell-price component before final Resonance Influence. It creates an RP payment interface only for actual spell casts, never for nonspell RC/class powers.

**Faction.** Use exact canonical faction identity, standing-v1 separately, actual membership separately, and reviewed invocation permission separately. Never infer one from another.

**Finite summons and Null.** Water Pet/Envoy use current finite-summon Null Disabled0 on qualifying Null damage; independent concentration/expiry/replacement still removes them.

## Original AC4 questions
### AC4-02 — Greater Warding
**AGREE.** Greater Warding preserves the printed +2 AC/+2 saves and spell resistance by defining the ambiguous resistance as spell-origin damage resistance; current damage/sharing ordering is retained.

Preserve +2 AC and saves, resistance to spells, Action/60ft and concentration up to1minute. Define recipient/willingness and the exact resistance scope: spell-origin damage, effects or another finite meaning must be decided explicitly. Distinguish flat save modifier from advantage; apply current strongest-stat families and damage ordering with Warding Bond, Shield and Elemental Resistance. It grants no automatic immunity, extra armor formula or absorption/reflection unless expressly authored as NEW. Specify suppress/return/end and multiple-source handling without healing or resource refresh.

### AC4-03 — Spell Shield
**REVISE.** Spell Shield keeps the printed reflection promise but is operationally a one-use pending ward and pure redirection of one eligible single-target rank-0..3 spell; this resolves level/Tier wording and current Null root identity.

Preserve reflection of spells of3rd level or lower in the catalog and Tier3 or lower in Core, with printed Action/60ft/Instantaneous. Resolve that exact terminology conflict and whether an Action establishes protection, readies a later reflection or has another finite source-compatible operation. Define eligible actual spell events, protected recipient, lifetime, trigger/commit timing, destination/range, attack/save/caster ownership, concentration and effect identity. Reflection must preserve real costs and a finite causal history; no new free cast, arbitrary nonspell-power reflection, area immunity or endless mirror loop. Compare Counterspell and pending Soul Mirror/Spell Mirror without merging their identities.

### AC4-04 — Dimensional Anchor
**AGREE.** Dimensional Anchor is a fixed 60-foot-radius concentration sphere using origin/destination endpoint tests only; no imagined-path test or new topology is created.

Preserve prevention of teleportation and planar travel in a60ft radius, Action/60ft/Instantaneous. Resolve radius versus casting range, actual center/shape and duration/concentration for this prevention. Define origin,destination,path/boundary eligibility, preflight and committed failures, willing/hostile travel, ongoing portals and suppression/ending under existing spell-event ownership. Do not invent a new plane or alter existing topology; only evaluate already established location/transport records. It supplies no physical cage, movement prohibition, resource refund or generic immunity to unrelated displacement by its name.

### AC4-05 — Corruption Barrier
**AGREE.** Corruption Barrier uses actual Corrupted eligibility, finite selective geometry and bounded contact damage without becoming a universal solid wall/detector.

Preserve a wall that both blocks and damages corrupted creatures, Action/60ft and concentration up to1minute. Supply finite geometry, eligible support/placement, sight/line/cover, damage/type/resolution, trigger cadence and entry/forced-movement cases. Corrupted eligibility must reference current mechanically established corruption records, not donor names, appearance, morality or a new cosmological category. Determine nonmatching creatures, objects, attacks and caster crossing without silently making a universal solid wall or automatic corruption detector. Preserve both printed functions and actual material/creature identity.

### AC4-06 — Resonance Dampening Field
**REVISE.** Resonance Dampening Field receives a scoped NEW mandatory +2-RP spell-price interface, including otherwise free/charge-only spell casts, ordered before final Resonance Influence.

Preserve all spellcasting in the area costing +2 RP, Action/60ft/Instantaneous. Define finite area/center/lifetime/concentration, qualifying caster position and final-price checkpoint, including cantrips, reactions, rituals, item activations and effects that merely continue. Resolve duplicate fields and interaction with reviewed Resonance Influence without silently dropping the printed surcharge. Apply current affordability-before-payment and actual-cast identity; no partial payments, repeated child-effect charges, retroactive drain/refund or extra cost on noncasting powers inferred from a tag.

### AC4-07 — Faction Sanctuary
**REVISE.** Faction Sanctuary keeps finite benefits but now explicitly uses reviewed faction invocation permission and actual membership; standing-v1 or temporary affiliation does not substitute.

Preserve an area sacred to a faction with benefits for members, Action/60ft/Instantaneous. Author a finite mechanical benefit menu and area/lifetime/concentration, actual faction choice and membership evidence, entry/exit/suppression, overlap and visitors. Distinguish membership from reputation and from opposing alignment; compare Faction Ward, Faction Seal and Greater Faction Emblem. The word sacred supplies no new deity, ownership, legal immunity, cosmology or automatic change in allegiance/reputation. Retain any unresolved faction identity/membership facts as explicit dependencies rather than fabricating a roster.

### AC4-08 — Alignment Lock
**REVISE.** Alignment Lock retains a 24-hour effective-axis freeze and gains explicit AC4-ALIGN-01 interaction with reviewed Purge/Suggestion without deleting underlying records.

Preserve preventing a target from changing alignment for24hours, Action/60ft. Resolve target/save/willingness, scope of prevented transitions, existing masks versus true underlying records, suppression and ending. Use current alignment record distinctions and reviewed Alignment Suggestion/Revelation/Sanctuary. No new axis, moral doctrine, cosmic influence or prediction of player choices is requested. Preventing a state change does not itself grant behavioral compulsion, reveal alignment or erase an existing effect; specify the actual rule at each attempted transition without refund/reset.

### AC4-09 — Alignment Anchor
**REVISE.** Both Alignment Anchor placements remain separate; the Conjuration zone and Cleric rank-7 creature placement use separate procedures and AC4-ALIGN-01. The conduct clause remains bounded by established predicates and the hard-denial guard.

Preserve both placements: Abjuration rank7/17RP/120ft/seven days fixes one creature alignment and prevents acting against it; Conjuration rank4/7RP/60ft/Instantaneous creates a zone preventing alignment change. Decide identity and placement-specific procedures explicitly; never grant Cleric the global minimum rank/cost or silently merge the two promises. Define target/zone/save/willingness, finite duration for the zone, actual recorded alignment, masks versus underlying changes, and handling of the rank7 behavior clause under current compulsion rules. Preserve player agency boundaries without deleting the printed clause. This is a mechanical source question, not a new moral axis, cosmological force or theology review.

### AC4-10 — Summon Water Pet
**REVISE.** Summon Water Pet keeps its printed body values and heal/attack, gains a complete command profile, a scoped shared support/offense allowance for healing, and current Null Disabled-at-0 handling.

Preserve HP35, AC14 and a choice of healing an ally for2d6 or attacking for1d10 cold, Action/60ft and concentration up to1minute. Supply finite body/size/speed/senses/saves, attack modifier/reach and healing range/target requirements, placement, initiative/commands and the shared offensive-action budget. Resolve whether heal and attack are mutually exclusive uses of its ordinary action and healing of Downed targets using current procedures. Preserve one body, damage/custody history, ending/return placement and no-resource remains. No aquatic adaptation, free water, unlimited independent actions or cosmetic elemental name expands its profile without explicit NEW authoring.

### AC4-11 — Crystalline Barrier
**AGREE.** Crystalline Barrier uses one opaque 30x10x1 wall with one AC18/40HP pool; suppression/occupied-return and no-material-stock rules make it runnable.

Preserve a wall of elemental glass with AC18, HP40 and blocked line of sight, Core Action/range Sight/concentration up to1minute. Define finite dimensions/sections, orientation/support, sight to the casting location, occupancy/escape, line of effect/cover, passage, structural damage and section loss. Resolve whether HP40 applies to one whole wall or sections explicitly; do not silently multiply the pool. Appearance as glass does not erase printed sight blocking. No unbounded length, indestructible force-wall traits, duplicated cargo, permanent raw materials or unsupported building support follows from the name.

### AC4-12 — Elemental Drain
**REVISE.** Elemental Drain preserves the 2-vs-5 source conflict and adopts Core's 5-RP loss for this candidate, with one random element draw and active-creature RP-holder eligibility.

Preserve the exact conflict: catalog target loses2 RP, Core target loses5 RP; both retain3d6 damage of a random element, Action/60ft/Instantaneous. Resolve the drain amount explicitly without rewriting either original. Define attack/save and branch ordering, finite random-element table and one committed draw, current RP floor/target eligibility, damage resolution, suppression and repeat casting. Losing RP does not say the caster gains it. Do not silently create a transfer, draw extra elements on rerolls, let prevention of one component erase the other, or import familiar external-game damage types.

### AC4-13 — Bind Element
**AGREE.** Bind Element preserves Paralyzed for two rounds, adds one early repeat save and uses the current shared hard-denial guard without replacing the condition.

Preserve one elemental creature, WIS save or Paralyzed for2rounds, Action/60ft/Instantaneous. Bind elemental eligibility to an actual established creature-type/profile record, not any elemental-tagged spell or ingredient. Specify initial success/failure, source-clock endpoints, any repeat saves, parent lifetime/concentration and interaction with the current hard-denial cap and Paralyzed condition. Keep the two-round source clause visible while resolving any cap conflict explicitly; no silent replacement with Restrained, Stunned or arbitrary immunity. Physical position, support and actual custody remain separately governed.

### AC4-14 — Dimensional Door
**AGREE.** Dimensional Door is self plus actual carried gear to one known same-plane destination within 500 feet, with atomic failure and ordinary support/falling.

Preserve teleporting up to500ft to a known location, Core Action/range500ft/Instantaneous. Define who travels, what knowledge establishes the destination, legal space/support, source/destination geometry, actual gear/cargo and willingness/contested cases. Distinguish this Conjuration identity from the separate Universal Dimension Door record. Actual clocks, falling, custody, existing transport-prevention effects and spent resources survive the transit. No bonus passenger, off-map knowledge, interplanar destination or missing-item recreation is inferred from a familiar external spell.

### AC4-15 — Resonance Beacon
**AGREE.** Resonance Beacon is a finite fixed destination with enrolled allies and a separate Action/2-RP nonspell transit activation; support destruction and transport wards remain real.

Preserve a created point that allies can teleport to using RP, Action/60ft/Instantaneous. Define the actual point/body, finite lifetime/concentration, destination capacity, eligible allies, access/range, trigger action, participant RP cost and one transfer transaction. Distinguish initial7RP casting cost from any explicit later traveler payment. Decide anchoring/movement, occupancy, obstruction, hostile custody, suppression/destruction/ending and whether multiple travelers can use it, without free repeated movement, duplicate payment, child-triggered refill or invented planar connections. Compare existing Resonance Conduit/Well and Faction Portal, not an automatic stronger copy.

### AC4-16 — Faction Ally
**REVISE.** Faction Ally uses one finite summon-only Envoy profile, actual faction permission/membership evidence, shared command/offense limits and current Null Disabled-at-0 handling.

Preserve summoning one CR3 creature aligned with the caster faction, Action/60ft/concentration up to1minute. Define an actual finite eligible source roster or explicit missing-profile dependency, faction evidence, body, initiative/commands/offense budget, summon count/replacement and ending. CR3 alone is not a complete combat profile and must not authorize arbitrary unpublished traits, copied Director secrets or a free adaptable stat block. Faction alignment is not automatically moral alignment. Preserve actual cargo and no-resource summon history, and do not grant faction knowledge, legal access or reputation through the temporary body.

## Current interface questions
### AC4-R01 — Reflection and transfer identity
**AGREE.** Spell Shield is pure redirection, not a new reflected/retaliatory root. Original cast/dealer/root/nullNonlethal/concentration identity is preserved; the reflector supplies only the return origin.

The old shared arbitration sentence treats all copies/reflections as preserving a causal root. The current Null rules distinguish pure transfer/redirection from an explicitly new reflected/retaliatory damage root. Spell Shield currently proposes redirecting the single original payload before attack/save, retaining original caster ownership/stats/concentration. Independently decide this exact mechanism and record cast identity, damage dealer/root creation, Null flag, return targeting, ongoing target branch, concentration, source rank and no-copy/recursive-reflection limits. Do not grant universal root semantics to other reflection sources.

### AC4-R02 — Alignment Lock/Anchor against current Purge and Suggestion
**REVISE.** Add NEW scoped AC4-ALIGN-01: Lock/Anchor snapshots apply after the reviewed Suggestion/Purge result for effective reads; lower overlays remain live, and new Suggestion baseline excludes AC4 locks to prevent ratcheting.

The seven DI7 cards are now reviewed, including the named AP-AS-01 exception. It is not a universal priority taxonomy. Define this new lock family’s exact interaction with Purge and Suggestion in both cast orders, underlying changes, suppression and zone exit/reentry; no fabricated undefined axes or cast-order staircase. Preserve both Alignment Anchor placements and the rank7 conduct clause with its bounded hard-denial guard. Any additional exception must be explicit NEW authorship, not attributed to old accepted text.

### AC4-R03 — Faction history and actual permissions
**AGREE.** Use standing-v1 and actual membership/affiliation/invocation records. Positive standing, null fields, information access, disguise and temporary Envoy affiliation are not membership or permission.

The expedition/reputation review is now complete within its own authored scope; the old statement that it is pending is historical. Use the actual preserved standing policy/version and independently established membership/affiliation/invocation records. Do not invent permissions or treat favorable standing, null fields, a temporary summoned affiliation or DI7 information access as membership.

### AC4-R04 — Finite summons and Null zero
**REVISE.** Water Pet and Faction Envoy use the accepted finite-summon Null Disabled-at-0 branch for qualifying Null damage. Water Pet healing deliberately spends the owner's one shared support/offense activation as a scoped NEW exception.

Water Pet and Faction Envoy need the current Null Disabled override for qualifying damage at0; independent expiry, replacement, dismissal and concentration ending still end their bodies. Separate source owner from controller, source type from humanoid appearance, no-resource lifecycle and actual gear custody. Decide whether Water Pet healing deliberately spends the offensive allowance as a scoped NEW exception; ordinary pure support only spends the shared command. Supply complete profiles and control timing, not nominal CR alone.

### AC4-R05 — Legal casting and the new RP surcharge
**REVISE.** Accept the Dampening Field's NEW +2-RP bridge as a mandatory spell-price component before final Influence. No-pool actors cannot pay; nonspell RC/features remain outside.

Review Dampening Field’s proposed new RP-price interface for otherwise charge-only/free spells explicitly, including no-pool actors, waivers, class reductions/minimums, mandatory extras, Dissonance/Refrain and final Influence. This is proposed NEW behavior, not already established by Influence. Preserve all class access, current caster engine and item-source requirements; a nonspell technique or Oracle RC feature is not automatically a spell.

### AC4-R06 — Timing, invalid eligibility and suppression
**AGREE.** Use source-specific virtual/absolute deadlines; suppression never resets them. Hidden ineligibility is adjudicated after commitment without free information. Suppressed bodies/conditions keep identity and clocks.

Resolve exact endpoints for every one-minute/ten-minute/24-hour/seven-day procedure and the distinct two-turn Bind Element. Keep fixed virtual markers or absolute deadlines as the chosen source requires; no restart through extra turns, initiative reorder or absence. Distinguish known illegal choices from hidden eligibility; do not reveal alignment, faction, type or obstruction through free validation. Fully specify suppressed bodies, conditions and occupied return geometry.

### AC4-R07 — Source conflicts and full effect fidelity
**REVISE.** Spell Shield trigger uses actual generating rank 0-3 to reconcile level3/Tier3. Elemental Drain uses 5 RP for this candidate while preserving catalog 2 and Core 5 as an explicit conflict.

Explicitly disposition Spell Shield’s level3/Tier3 language and Elemental Drain’s catalog2RP/Core5RP conflict. Retain both originals. Check every printed effect/placement, geometry, save, lifetime, current HP/life consequence, cost and rejection path for all15 cards; no global rank collapse, missing effect or shortcut to achieve acceptance.

### AC4-R08 — Spatial and local-module integrations
**AGREE.** Endpoint-based Dimensional Anchor, selective Corruption Barrier, whole-pool Crystalline Barrier and current Xi/Null interfaces remain bounded; no epilogue machine becomes a generic spell rule.

Check Dimensional Anchor endpoints/atomic group travel versus Dimensional Door and Beacon; Corruption Barrier forced crossing/carried bodies/falling; opaque Crystalline Barrier whole40HP and support. Apply the exact current Xi spell-target branch and Null rules without turning bounded epilogue machines into universal spells. Accepted campaign arcs do not grant generic climate, planar or soul authority.

### AC4-R09 — Banishment historical sequencing hold
**AGREE.** Banishment remains outside the fifteen. The old pre-push hold is historical; its current status is source-only next-authoring obligation under reviewed planes/souls.

The owner-authorized progress push and careful cosmology review have occurred. Banishment is still a source-only receipt because no complete procedure has yet been authored, not because the push is pending. Preserve its full receipt and original source; do not count it among these15 or silently approve it. It remains a separate next-authoring obligation using the current planes/souls sources, with no erased identity or permanent procedural block.

## Source-conflict preservation
- Spell Shield: both original phrasings remain in structured evidence; adopted trigger is actual generating rank 0–3.
- Elemental Drain: both 2-RP and 5-RP loss records remain; candidate operational branch uses 5 RP.

## Banishment
Do not count or approve it here. Preserve its exact source-only receipt. The owner-authorized push/cosmology review occurred; the remaining reason for deferral is simply that no complete current Banishment procedure has yet been authored.

## AC4-C01 through AC4-C08 correction dispositions

- **AC4-C01 — AGREE (correction):** Spell Shield now has a fixed nonconcentration tenth-future-caster-start / +60s deadline preserved through suppression, absence and caster death.
- **AC4-C02 — AGREE (correction):** Faction Ally requires actual membership in one canonical faction **and** actual invocation permission. Standing/affiliation alone never qualifies.
- **AC4-C03 — AGREE (correction):** Spell Shield does not allocate or advance a damage root. Preserve an already-created root; otherwise create/evaluate it only at the original source checkpoint under the original dealer.
- **AC4-C04 — AGREE (accepted-interface clarification):** qualifying Null at positive→0 and repeated qualifying Null at Disabled0 preserve the same body; independent expiry/concentration/dismissal/replacement still end it.
- **AC4-C05 — AGREE (presentation):** the Player chapter now contains the full Envoy profile. Structured authority remains `SPELLS_MODEL.json#/factionAllyProfile`; nominal CR3 is provisional.
- **AC4-C06 — AGREE (NEW scoped authorship):** `AC4-SUMMON-TARGET-01` classifies only Water Pet and Faction Envoy mechanically for living/active-creature targeting while their body exists. It makes no natural-origin, soul, corpse or generic creature-type claim. Beacon uses active-creature identity rather than biological living status.
- **AC4-C07 — AGREE (correction):** X09 now uses actual `summon-spectral-steed` and its complete Planar Crossing transaction.
- **AC4-C08 — AGREE (corrections + NEW scoped authorship):** X03/X08/X13 are concretized from existing source cards. `AC4-BEACON-01` is a Beacon-only pre-relocation state revalidation checkpoint; it grants no generic interrupt or Reaction.

### Faction Envoy profile reference
Use the complete player-visible profile in `PLAYER_CHAPTER.md` and the structured exact record at `SPELLS_MODEL.json#/factionAllyProfile`. No hidden extra action, defense, faction knowledge, soul/natural-origin fact or certified CR is implied.
