# FEAT335-COPY-RELEASE-SOURCE-01 — bounded addendum

**Scope:** CRS-01–03 only. No feat exact approval, runtime/balance/whole-game approval, or cosmology interpretation. Original package and source objects remain historical.

## CRS-01 — canonical chronological identity — NEW minimum completion

NEW feat-copy chronological identity. Every paid feat-copy cast records `castFamilyKey = feat-copy::<canonicalSourceEffectId>`. `canonicalSourceEffectId` is the stable identity of the actually witnessed underlying spell/effect from which the bounded profile was captured; for a source-qualified monster ability use that ability's stable source identity. Changing the capture event, owner, Eldritch Echo/Mimicry/Arcane Adaptation permission, bounded profile, selected damage/type component, q, or qualifying casting-ability route does not create a new family. Copies sharing that key use the ordinary chronological Refrain history together. An ordinary cast of the underlying spell uses its ordinary spell family and does not share the feat-copy family; Mirrorsage Echo Release likewise keeps its own class family. A missing stable underlying source identity is ineligible for release rather than being assigned a favorable new key. This key grants no ordinary spell knowledge or access.

## CRS-02 — concentration tags — NEW minimum completion

NEW feat-copy concentration tags. Strike: no. Burst: no. Mend: no. Ward: yes. Hindrance: yes. Boon: yes. Step: no; its movement/teleport resolves instantaneously. A concentration-required copy establishes the releaser's one concentration burden during casting commitment under the ordinary sequence, ending an incompatible existing concentration before the counter window. If that cast is later countered, prior concentration remains ended and no copied lasting effect remains. Loss of concentration ends the Ward/Hindrance/Boon copied effect immediately; their printed earlier deadlines still cap duration. Immediate profiles establish no new concentration burden. Ready is separate: preparation already occupies concentration. On release, an immediate profile resolves and that Ready concentration ends with the released spell; a concentration-required Ward/Hindrance/Boon continues on that same one concentration burden, never a second slot. No witnessed original concentration tag is inherited or used to change these seven profile tags.

## CRS-03 — strain engine and Limit — KEEP FS-09, scoped clarification

COPY-ROUTE STRAIN SCOPE. A paid feat-copy cast under FS-08 is an independent feat-casting route for strain purposes. Use FS-09 exactly: base Dissonance 0 for q/rank 0, 1 for ranks 1-5, and 2 for ranks 6-9; apply ordinary same-family Refrain using CRS-01; and use `Limit = max(4, 2*PB + casting modifier)` for that copy route, including its existing surcharge/block thresholds. The owned route chosen to qualify the copy supplies only the permitted casting ability, rank ceiling and other expressly required source credentials; it does not import that class engine's protected Dissonance reduction, routing, vent, prepared-matrix treatment or proc chain into the feat-copy cast. In particular a Wizard-qualified copy is not a prepared matrix, a Shaman-qualified copy is not an ordinary Shaman spell for the totem vent, and a Mirrorsage-qualified copy is not class Echo Release. The ordinary `max(4, 2 + PB + max(0, modifier))` Limit in SPELL_INTEGRATION_RULES remains controlling for ordinary class spells within its existing scope and is not globally changed here. If the only qualifying route is the feat-only Eldritch Blast grant, it supplies CHA and only its actual rank-0 ceiling; it does not change the copy engine or Limit, create a Warlock/class engine, or qualify a ranked q>0 copy.

## Derived locations

- `DescentReviewChanges/ReviewBible/data/public/feat_candidates/exact_01/shared_rules.json` — FS-08: append CRS-01 family key, CRS-02 concentration tags and CRS-03 copy-route strain scope; preserve existing FS-08 text
- `DescentReviewChanges/ReviewBible/data/public/feat_candidates/exact_01/supplements.json` — SUP-07/value/copyProfileContract: add castFamilyKey contract; add per-profile concentrationRequired fields; correct lifecycle Step shorthand to instantaneous; add strainEngineRef=FS-09/CRS-03
- `DescentReviewChanges/ReviewBible/data/public/feat_candidates/exact_01/candidate.json` — feat IDs eldritch_echo, mimicry, arcane_adaptation: append matching release text to completeOperativeProcedure/payloadOperational/operationalRules representations as present; do not change acquisition predicates or source originals
- `docs/audit/2026-10-08/full-game/FEAT_EXACT_01_ACQUISITION_CONTRACTS.json` — records eldritch_echo, mimicry, arcane_adaptation: append same release integration wording to derived operative procedure only; preserve originalObject and acquisition contract history
- `DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md` — no global replacement: optional cross-reference note only: ordinary class Limit remains unchanged; feat-copy route uses FS-09. Do not replace line-35 formula.

## Finite acceptance expectations

- **CRS01-A** — Two consecutive Eldritch Echo captures of the same underlying spell identity, even from different source events or with different bounded profile/q choices, share one feat-copy family; the second copy receives the next ordinary Refrain step. Capture event ID does not reset history.
- **CRS01-B** — A Mimicry copy and later Arcane Adaptation activation of the same underlying captured spell/effect identity share the same feat-copy family. Changing permission source or casting ability route does not reset Refrain.
- **CRS01-C** — An ordinary personally known cast of the underlying spell followed by a feat-copy cast uses two distinct chronological families. The ordinary cast does not grant the copy and does not pre-load the feat-copy Refrain family.
- **CRS01-D** — Two different underlying source spell/effect identities that both map to Strike remain different feat-copy families; common profile ID alone does not merge history.
- **CRS02-A** — Strike/Burst/Mend/Step do not displace existing concentration merely because they are feat-copy casts; each resolves immediately.
- **CRS02-B** — Ward/Hindrance/Boon displace incompatible prior concentration at commitment. Countering afterward does not restore prior concentration and leaves no copied lasting effect.
- **CRS02-C** — A successful lasting Ward/Hindrance/Boon ends immediately on lost concentration even if its stated two-interval/source deadline has not arrived.
- **CRS02-D** — Ready preparation already holds concentration. Releasing Ward/Hindrance/Boon continues the same one burden; releasing an immediate profile ends the Ready hold after resolution. No second concentration slot exists.
- **CRS03-A** — Wizard-qualified feat copy does not receive Wizard first-prepared-matrix base-Dissonance exemption and is not a prepared matrix.
- **CRS03-B** — Shaman-qualified feat copy inside its own totem aura does not consume or benefit from the ordinary-Shaman-spell vent unless a future source explicitly names feat-copy casts.
- **CRS03-C** — Mirrorsage qualification does not import class Echo Release first-release Refrain waiver; the feat copy still consumes the shared release allowance only where its exact existing source says so.
- **CRS03-D** — At PB3 and casting modifier +3, feat-copy Limit is max(4,6+3)=9. Ordinary class spell Limit under the separate integration formula would be max(4,2+3+3)=8; this difference is intentional scoped authority, not a global correction.
- **CRS03-E** — Feat-only Eldritch Blast route can qualify q0 with CHA; it cannot establish q1+ ceiling, a class engine, Wizard/Mirrorsage/Shaman protections, or another RP pool.


## Scope guard

- No original spell/repertoire grant
- No new copy/capture source
- No new RP pool
- No class proc/vent/protected matrix
- No extra concentration slot
- No changed owner-round release cap
- No promotion of the 335-feat candidate
