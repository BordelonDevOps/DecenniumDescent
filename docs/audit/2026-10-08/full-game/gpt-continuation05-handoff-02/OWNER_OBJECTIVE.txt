Continue developing Decennium Descent in `C:\Github\DecenniumDescent` with the user's GPT notebook in Chrome's Calibration Review until every aspect of the game is covered in a source-linked discussion and decision ledger and a coherent, complete authored **video-game campaign-playtest candidate** is ready.

Audit and reconcile each system and content catalog, including all ordinary spells, all class stages, character creation and advancement, combat and conditions, ancestry/background/skills, equipment/feats/crafting/economy, monsters and encounters, exploration/survival/rest, setting/factions/Director logic, onboarding, player-facing presentation, developer/Director tooling, packaging, and companion interfaces.

**Decennium Descent is no longer being developed as a tabletop/TTRPG product.** Do not spend development or review effort making systems manually manageable at a physical table, preserving tabletop bookkeeping convenience, supporting physical dice procedures, or simplifying mechanics merely because a human Game Master would find them difficult to track.

Treat the game as a computer RPG whose engine may directly manage complex state, exact timing, hidden information, body geometry, collision and spatial queries, persistent effects, individual damage/healing provenance, operation snapshots, multiple concurrent clocks, deterministic state transitions, summon and companion lifecycle, resource transactions, and other machine-managed systems.

Preserve tabletop-origin source material as historical/source evidence where relevant, but do not treat tabletop usability as an active design requirement.

For all current and future mechanics, prioritize:

- deterministic software implementation;
- explicit state transitions;
- exact activation and timing;
- operation ordering and interruption;
- costs and resource transactions;
- target and eligibility predicates;
- geometry and body interaction;
- attacks, saves, damage and healing;
- ownership and provenance;
- conditions and lifecycle;
- concentration and persistent effects;
- movement, forced movement and Falling;
- suppression and dispelling;
- Null interactions;
- death and recovery;
- summons and companions;
- faction/alignment predicates;
- teleportation and planar behavior;
- stacking, replacement and conflict arbitration;
- cleanup and expiry;
- machine-testable edge cases.

Separate **engine mechanics** from **player presentation**. Internal rules may be highly detailed while the player-facing UI communicates only the information necessary to understand choices and outcomes.

Continue to preserve all source identities, original text, access records, histories and frozen evidence. Do not silently invent spells, abilities, class features, lore or cosmology. Where implementation requires a rule that the sources and accepted interfaces do not provide, confer with GPT on consequential choices and label the narrowest necessary completion as **NEW scoped authorship**.

Reuse accepted mechanics and interface decisions rather than repeatedly reconstructing them. Treat accepted interfaces as engine contracts unless a new source exposes a concrete contradiction. Accelerate remaining review work through source/hash validation, structural checks, interface inheritance, automated arithmetic/geometry/state validation, semantic-delta review, risk-tiered cohorts and machine-test-oriented examples.

Worked examples should increasingly function as deterministic test vectors containing sufficient initial state, operation inputs, relevant RNG results, intermediate transitions and expected final state for future automated tests. Do not retain cumbersome tabletop-only examples where they provide no engine or gameplay value.

Confer with GPT on consequential mechanics, source conflicts, genuinely unresolved design forks and any proposed change with potentially global engine consequences. Do not escalate questions already conclusively governed by exact sources or accepted interfaces.

Implement and validate agreed provisional decisions, and preserve all source information. Delete historical material only if both file audit and GPT review confirm it obsolete. Superseded history may remain as evidence but must not silently remain operative.

Do not claim broad validation from narrow checks. Distinguish clearly between:

- source preservation;
- structural validation;
- authored semantic review;
- arithmetic/geometry validation;
- engine implementation;
- automated runtime testing;
- human gameplay testing;
- numerical balance approval;
- cosmology-canon decisions;
- whole-game completion;
- publication/release approval.

Treat human gameplay testing, balance approval and publication/release approval as explicitly separate gates and do not claim them complete without evidence.

The final development target is a coherent, source-faithful, deterministic computer RPG candidate whose complexity is handled by software rather than constrained by tabletop administration.