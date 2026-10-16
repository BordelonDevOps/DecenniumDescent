# Decennium Descent — Accelerated High-Fidelity Spell Review Protocol

You are continuing the existing Decennium Descent full-game review. This is not a restart, redesign, simplification pass, or permission to lower the review standard.

The goal is to accelerate review of the remaining ordinary spell catalog **without reducing source fidelity, semantic rigor, worked-example quality, deterministic implementation quality, or preservation requirements**.

The acceleration must come from eliminating duplicated reasoning and repeated proof of already-accepted interfaces, not from skipping difficult interactions.

## 1. Governing Standard

Every reviewed spell must remain suitable for both:

1. tabletop play; and
2. deterministic video-game implementation.

Every operative spell procedure must therefore resolve, where applicable:

- activation and timing;
- resource cost;
- generating rank;
- targets;
- range;
- line of effect;
- perception requirements;
- body/space interaction;
- saves and attacks;
- damage/healing provenance;
- conditions;
- concentration;
- duration and exact expiry;
- movement;
- forced movement;
- Falling;
- terrain;
- summoned or created bodies;
- companion command economy;
- antimagic/suppression;
- dispelling;
- Null interaction;
- death/Stable/Dying interaction;
- teleportation;
- planar/extradimensional movement;
- faction/alignment predicates;
- stacking;
- replacement;
- rerolls;
- operation snapshots;
- cleanup;
- endpoint placement;
- lifecycle;
- cargo;
- edge cases;
- machine-testable state transitions.

Do not silently invent missing source content.

When a source gap requires authorship, label it clearly as:

**NEW scoped authorship**

and keep it as narrow as possible.

Do not convert a spell-specific bridge into a global rule unless the project explicitly approves that promotion.

---

# 2. Source Fidelity Is Absolute

For every spell:

- preserve the exact source identity;
- preserve original access records;
- preserve school/rank placements;
- preserve original spell text/history;
- preserve prior reviewed/current versions;
- preserve current case IDs and their order;
- preserve exact frozen source hashes.

Do not silently rewrite source promises merely because a cleaner design is possible.

If source text and an accepted project interface conflict, surface the conflict explicitly.

Do not infer cosmology, souls, native planes, divine metaphysics, faction metaphysics, or world history from mechanical requirements.

Unresolved lore remains unresolved unless the user explicitly resolves it.

---

# 3. Stop Re-Proving Accepted Interfaces

The largest source of wasted review time has been repeatedly reconstructing rules already resolved in earlier cohorts.

For every new spell, first determine whether each interaction is already governed by an accepted interface.

If an accepted interface fully determines the result, **inherit it**.

Do not reopen it merely because a new spell invokes it.

The review should say, in substance:

> This spell inherits [accepted interface]. No new rule is required.

Only reopen an accepted interface when the new spell creates a genuine contradiction that cannot be resolved within that interface.

Examples of systems that should normally be inherited rather than rebuilt include accepted/current versions of:

- ordinary spell pricing;
- Resonance Nexus pricing;
- Resonance Dampening pricing;
- generating rank versus paid RP;
- Null damage-root ownership;
- Null nonlethal handling;
- Stable / Dying / death-save handling;
- healing at 0 HP;
- concentration;
- Ready;
- Falling;
- body occupancy;
- body-volume intersection;
- companion command economy;
- summoned-body persistence;
- antimagic suppression;
- Greater Dispel;
- Lesser Antimagic;
- immutable operation snapshots;
- Dimensional Anchor;
- Banishment closure;
- endpoint placement;
- planar/extradimensional movement;
- teleportation predicates;
- Faction standing;
- alignment matching;
- rerolls/Fate Coin;
- source-owner provenance;
- cargo persistence.

The exact accepted rule text in the current repository remains authoritative. Do not rely on this summary instead of the actual accepted files.

---

# 4. Build an Accepted Interface Registry

Before processing additional large cohorts, maintain or generate a machine-readable registry of accepted reusable interfaces.

Each interface should contain at minimum:

- stable interface ID;
- name;
- current authoritative source;
- acceptance status;
- scope;
- exact trigger;
- exact inputs;
- exact outputs;
- lifecycle;
- exceptions;
- known source-specific extensions;
- spells/cohorts that currently use it.

Example conceptual form:

```json
{
  "id": "ACCEPTED-FALLING-CURRENT",
  "status": "accepted",
  "scope": "ordinary unsupported body falling",
  "source": "...",
  "usedBy": [
    "Greater Air Pet",
    "Planar Barrier",
    "..."
  ]
}
```

Do not invent interface IDs merely for cosmetic convenience if accepted IDs already exist.

The purpose is to make later spells declare dependencies rather than re-authoring the underlying system.

---

# 5. Use Risk-Tiered Review

Do not give every spell an individual Banishment-style forensic review.

Assign each spell a review risk tier before authoring its full procedure.

## Tier A — Routine / Inherited

Examples:

- ordinary damage spells;
- simple healing;
- straightforward attack spells;
- simple saves;
- simple buffs/debuffs;
- uncomplicated durations;
- ordinary areas;
- spells whose difficult interactions are already fully governed by accepted interfaces.

Tier A spells should usually be reviewed in cohorts of approximately **25–40 unique spell identities**.

They still require:

- complete operative procedures;
- source fidelity;
- appropriate cases;
- exact access;
- exact pricing;
- exact durations;
- structural validation.

They do **not** require pages of repeated explanation for inherited rules.

## Tier B — Interaction Heavy

Examples:

- persistent areas;
- summons;
- companions;
- transformations;
- concentration-sensitive effects;
- unusual forced movement;
- complex body geometry;
- faction/alignment mechanics;
- antimagic-sensitive persistent effects;
- unusual dispel behavior.

Review approximately **15–25 unique spell identities** per cohort where practical.

## Tier C — Systemic / High Risk

Examples:

- planar travel;
- teleportation;
- resurrection;
- souls;
- identity;
- time;
- reality alteration;
- imprisonment;
- antimagic creation;
- deep death interactions;
- spell-family replacement rules;
- effects that modify fundamental engine assumptions.

Review approximately **5–10 identities**, or individually where necessary.

Do not artificially enlarge a Tier C cohort merely to hit a target size.

---

# 6. Produce a Semantic Delta Table Before Deep Review

For every cohort, build a table similar to:

| Spell | Source preserved | Existing interfaces sufficient | NEW authorship required | Risk |
|---|---|---|---|---|
| Spell A | yes | yes | none | A |
| Spell B | yes | mostly | target lifecycle | B |
| Spell C | yes | no | planar endpoint rule | C |

The important column is:

**NEW authorship required**

This should identify the actual unresolved semantic decisions.

Those are the matters that require conference.

Do not create a long conference question list for issues already decided by accepted interfaces.

---

# 7. Conference Only on Genuine New Decisions

Before authoring a new scoped rule, ask:

1. Does an accepted interface already decide this?
2. Does the exact source already decide this?
3. Is the apparent gap only an example-writing problem?
4. Is the gap only structural?
5. Does the issue actually require user ownership?

If the answer can be determined from accepted authority, resolve it without escalating it as an open design question.

Escalate only genuine design forks.

When escalating, present:

- exact source promise;
- relevant accepted interface;
- conflict/gap;
- Option A;
- Option B;
- consequences of each;
- recommended choice;
- whether the choice is local or potentially global.

Do not silently choose major new systemic rules.

---

# 8. Automated Mechanical Preflight Must Come First

Before semantic review, automatically verify objective properties.

At minimum:

### Source Integrity
- archive bytes/hash;
- exact source count;
- exact source hashes;
- missing source files;
- altered source files.

### Identity
- unique spell ID;
- name;
- source identity;
- aliases;
- school;
- rank;
- class access;
- placements.

### Structural Integrity
- JSON parses;
- required fields;
- case IDs;
- current-case order;
- history preservation;
- pointer resolution;
- evidence-manifest bindings.

### Mechanical Arithmetic
Where machine-checkable:

- RP arithmetic;
- damage dice totals;
- healing totals;
- save totals;
- attack totals;
- DCs;
- distances;
- body geometry;
- sphere/cone/cube intersection;
- clocks;
- concentration deadlines;
- Ready deadlines;
- Falling markers;
- duration expiry;
- resource ledgers;
- cargo limits;
- placement dimensions.

Do not ask the semantic reviewer to find arithmetic defects that can be mechanically proven first.

---

# 9. Separate Rule Errors from Example Errors

A bad worked example does not automatically mean the underlying procedure is wrong.

Every finding must be classified as one of:

- SOURCE ERROR;
- PROCEDURE ERROR;
- INTERFACE CONFLICT;
- EXAMPLE ERROR;
- STRUCTURAL ERROR;
- HISTORY/PRESERVATION ERROR;
- OPEN DESIGN QUESTION.

If only an example is wrong, repair the example.

Do not unnecessarily reopen the spell procedure.

---

# 10. Worked Examples Remain Required

Acceleration does **not** mean removing examples.

Each spell still requires enough worked cases to establish its material semantics.

However, examples should focus on actual unresolved or high-risk behaviors rather than repeating trivial inherited mechanics.

Examples must use real legal sources where one is required.

Do not fabricate unnamed attacks, spells, abilities, conditions, or class features merely to make an example work.

If an example requires:

- an interrupt;
- forced movement;
- a projectile;
- a condition;
- a dispel;
- healing;
- a Null packet;
- a class ability;

use an actual project source.

If the proposed example is impossible under the real rules, reject it and replace it with the closest legal fixture while preserving the intended scenario obligation.

---

# 11. Original Scenario Obligations Must Be Preserved

A case ID surviving is not sufficient.

For every prior/current case, preserve the **material scenario obligation**.

Do not replace:

> exact projectile crossing at 20 + 30 feet with no remote caster

with:

> projectile rules work normally.

Do not replace:

> hidden Dimensional Anchor causes atomic paid group failure

with:

> destination restrictions are checked.

Do not replace:

> first attack misses, then Net Bolt interrupts concentration

with:

> concentration may be interrupted.

The actual scenario must remain represented.

Whenever a case is revised:

- preserve its prior version;
- preserve its history chain;
- retain the same ID unless there is a compelling reason not to;
- state exactly what changed.

---

# 12. Do Not Let History Become Current Authority

Historical records must remain exact.

But superseded historical statements must not remain active in current operative rules.

Examples:

- old destruction behavior;
- old AC values;
- old durations;
- old pending labels;
- outdated AC5 status;
- obsolete proposed adjudications.

History is evidence, not current authority.

Current procedures must be clean and self-consistent.

---

# 13. Complete Procedures Must Be Standalone

Every reviewed spell procedure must be usable without having to reconstruct the rule from scattered historical notes.

Where the current project format requires both player-facing and Director-facing procedures, both must contain the complete operative rule appropriate to that chapter.

Do not hide material operative rules solely inside:

- historical records;
- casebooks;
- source comments;
- prior drafts;
- review questions.

Cross-references to accepted interfaces are allowed, but the spell's own required parameters must remain explicit.

---

# 14. Keep Spell-Specific Rules Spell-Specific

If a spell needs a special classification, write:

> For this spell only...

Examples from prior work include local distinctions involving:

- teleportation;
- planar movement;
- physical crossing;
- attack origin;
- body-volume targeting;
- plane-wide temporary alignment effect.

Do not silently generalize these into global engine rules.

If later evidence suggests the rule deserves global promotion, flag that as a separate project-level decision.

---

# 15. Review the Entire Cohort, But Allocate Depth Unevenly

Every spell in the cohort must actually be read.

Do not write:

> all spells reviewed

when only selected examples were deeply inspected.

The final receipt should state actual scope, e.g.:

> All 32 procedures were read. Structural/source checks covered all 32. Detailed manual semantic recomputation was performed for spells X, Y, Z and cases A–H because they contained the cohort's new systemic interactions.

That distinction is required.

---

# 16. Cohort Output Should Be Exception-Focused

For each cohort, provide:

## A. Cohort inventory
- unique identities;
- placements;
- ranks;
- schools;
- classes.

## B. Risk classification
- Tier A count;
- Tier B count;
- Tier C count.

## C. Inherited interfaces
List accepted rules reused unchanged.

## D. Genuine new authored rules
Only rules actually introduced by this cohort.

## E. Findings
Each with:

- ID;
- severity;
- source;
- exact file/pointer;
- disposition;
- evidence;
- replacement text if applicable.

## F. Case coverage
State what scenario each case proves.

## G. Machine validation
State exact pass counts and scope.

## H. Remaining unresolved decisions
Only genuine unresolved questions.

---

# 17. Use Large Cohorts Where Safe

The remaining spell review should no longer default to cohorts of 14–16 spells.

Preferred targets:

- Tier A-heavy cohort: **25–40 identities**
- Tier B-heavy cohort: **15–25 identities**
- Tier C-heavy cohort: **5–10 identities**

Mixed cohorts are acceptable if dependencies make that cleaner.

Do not force arbitrary alphabetical/school boundaries if another grouping would reduce duplicated semantic work.

Prefer grouping by shared engine interaction where useful.

Examples:

- straightforward damage/control;
- healing/recovery;
- summons/companions;
- transformations;
- barriers/zones;
- teleport/planar;
- death/soul;
- time/reality.

---

# 18. Freeze Accepted Cohorts

Once a cohort receives exact acceptance:

- freeze its source manifest;
- freeze its final artifact hashes;
- register its accepted interfaces;
- do not rereview it during later cohorts except at a concrete interface conflict.

Later cohorts may cite it.

A future spell interacting with an accepted spell does not reopen the accepted spell unless the interaction demonstrates an actual contradiction.

---

# 19. Preserve Deterministic Randomness

Whenever randomness matters:

- define candidate set before draw;
- use stable ordering;
- use uniform selection;
- no retry-until-valid;
- apply Fate Coin only when actually permitted;
- preserve hidden/public distinction;
- do not redraw already committed selections because later state changes.

Machine-check candidate arrays where possible.

---

# 20. Geometry Must Be Mechanically Proven

For spells using:

- range;
- bodies with extent;
- walls;
- spheres;
- cones;
- lines;
- portals;
- apertures;
- occupied cells;
- planar receiving spaces;

do not rely on prose like:

> clearly within range.

Record enough coordinates/dimensions to verify the result.

Use the current accepted geometry rules.

Where a spell has a NEW source-specific geometry bridge, label it narrowly.

---

# 21. Resource Transactions Must Be Explicit

Where relevant, record:

- initial RP;
- quoted cost;
- reductions;
- mandatory additions;
- final cost;
- protected principal;
- expenditure time;
- refund status;
- Recharge/encounter/daily consumption.

Do not confuse generating rank with final RP cost.

Do not refund a legal expenditure merely because the resulting operation is suppressed, misses, or fails unless an actual rule permits refund.

---

# 22. Lifecycle Must Be Explicit

Persistent spell-created things require complete lifecycle treatment.

Where applicable specify:

- identity;
- body;
- HP;
- state;
- source;
- ownership;
- command authority;
- deadline;
- concentration;
- suppression;
- death/destruction;
- healing;
- cargo;
- displacement;
- dismissal;
- replacement;
- expiry;
- cleanup.

Do not allow temporary suppression to silently create a new body on resumption unless an accepted rule explicitly says so.

---

# 23. Preserve Source-Compatible Weirdness

Do not normalize unusual source behavior merely because another spell works differently.

Different spells may legitimately classify similar-looking movement differently.

Different summons may have different profiles.

Different barriers may have different geometry.

Different effects may use different origin points.

Consistency means deterministic behavior, not making every spell identical.

---

# 24. No Unsupported Global Canon Claims

The spell review may author mechanical bridges necessary for play.

It does not automatically decide:

- cosmology;
- divine truth;
- soul ontology;
- native-plane identity;
- world-history facts;
- unresolved lore;
- Old God identities;
- Heartcell history;
- First Choir timing;
- other explicitly unresolved project questions.

Keep mechanical rules bounded.

---

# 25. Receipt Standard

At the end of each review, produce exact reproducibility information:

- input archive name;
- input byte count;
- input SHA-256;
- exact current file bindings;
- output archive;
- output byte count;
- output SHA-256;
- individual file bytes/hashes;
- source count;
- source verification result;
- identity count;
- placement count;
- case count;
- pointer count;
- failed pointer count;
- exact review scope;
- dispositions.

Do not say tests passed unless they actually ran.

Distinguish:

- authored structural checks;
- arithmetic checks;
- semantic review;
- runtime execution;
- human playtesting;
- numerical balance testing.

---

# 26. Acceptance Language Must Stay Bounded

Unless specifically instructed otherwise, successful spell-cohort review means only:

> accepted as an authored campaign-playtest candidate.

It does **not** automatically mean:

- spell adoption;
- runtime implementation approval;
- human-playtest approval;
- numerical balance approval;
- cosmology-canon approval;
- whole-game closure;
- publication approval.

---

# 27. Primary Optimization Goal

The goal is to reduce this pattern:

> read everything → reconstruct accepted systems → rewrite them → discover structural bug → repair → reread everything → discover example bug → reread everything

into:

> freeze source → mechanical preflight → inherit accepted interfaces → identify semantic delta → review only genuine new decisions → validate high-risk examples → exact acceptance

Quality must remain equal or better.

Time savings must come from:

- inheritance;
- automation;
- larger safe cohorts;
- focused semantic review;
- exact delta tracking;
- not reopening settled systems.

They must **not** come from:

- deleting examples;
- shortening procedures until ambiguous;
- skipping source verification;
- dropping histories;
- ignoring edge cases;
- treating unresolved questions as solved;
- inventing convenient abilities;
- replacing scenario obligations with generic summaries.

---

# 28. Instructions for the Next Spell Cohort

Before beginning the next cohort:

1. Determine the exact remaining unique ordinary spell identities from the current catalog.
2. Remove identities already exactly accepted/reviewed.
3. Group the next candidates by interaction complexity rather than blindly using a tiny fixed cohort.
4. Assign Tier A/B/C.
5. Build the Accepted Interface Registry from currently accepted work.
6. Run mechanical preflight.
7. Produce the Semantic Delta Table.
8. Identify only genuine unresolved decisions.
9. Confer with me before authoring any substantial new systemic rule.
10. Then build the complete review candidate.

For the next cohort, aim for approximately:

- **25–40 spells** if predominantly Tier A;
- **15–25** if Tier B-heavy;
- **5–10** if Tier C-heavy.

If a larger cohort can be proven mechanically independent and uses existing interfaces, prefer the larger cohort.

Do not sacrifice completeness merely to maximize count.

---

# 29. Current Project Principle

The project has already paid the cost of establishing many difficult interfaces through AC4, ordinary Banishment, AC5, AC6, Null, damage roots, companion handling, antimagic, body geometry, planar movement, Ready, Falling, and lifecycle work.

Treat that accumulated work as reusable infrastructure.

The remaining approximately 383 unique spell identities should **reuse the engine we have built rather than recreate it spell by spell**.

That is how we accelerate the remainder without lowering the standard.