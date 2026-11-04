# Character advancement rule decisions

**Status: TEST_ONLY implementation of one source-bound Soldier 1 → 2 path. This does not complete character advancement.** Sources retain their own provisional playtest status; this record does not approve them for release.

## Source rules implemented

The source set is pinned to Engine's base revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`; exact blobs, hashes, and JSON pointers are in [SOURCE_BINDINGS.json](evidence/2026-11-04-character-advancement/SOURCE_BINDINGS.json).

- Opening-campaign advancement is awarded by announced milestones. Each advancement adds one total level, processes the chosen class level and its acquisition schedule, adds one unspent Hit Die, and applies the class's fixed rounded-up average when that method is selected. Recompute base maximum HP from attained level records and current Constitution; preserve current HP except for a downward clamp. A level-up does not heal or refresh spent resources. See `CHARACTER_CREATION_PLAYTEST.md`, `#gain-a-level`, and `XP_ADVANCEMENT_CANON.md`.
- A class feature is known only when granted or selected. Soldier level 2 selects two Base cards, has no minimum active-card count, and grants no ASI/feat. The two implemented cards are `soldier.base.defensive-positioning` and `soldier.base.tactical-reposition`. See `CLASS_PLAYTEST_RULES.md`, `#reading-a-class-card`, and `soldier.json` `/schedule/1` and `/cards`.
- Defensive Positioning gives +1 AC while adjacent to solid terrain or the character's cover. Tactical Reposition uses a Bonus Action to move up to half Speed without opportunity attacks, with Recharge 2 and an open route; it does not permit teleporting, escaping restraints, or attacks. Exact current card wording is preserved in the pinned Soldier data.
- Soldier's later-level d10 fixed-average base contribution is 6. This slice uses that value for level 2; it does not grant first-level maximum HP again.

## Prototype policies adopted for this slice

The following policies complete gaps in the source interface and remain provisional. They do not change the published source text.

- A trusted host awards a unique, actor-scoped milestone. Consuming that entitlement, adding exactly one level, recording one new unspent d10, granting the two selected cards, recalculating capacity, and writing the audit event happen in one persisted transaction. Repeated milestone IDs for the same actor do not grant twice. Awarding and leveling consume no simulation time.
- This first implementation accepts only a Soldier 1 → 2 actor, a milestone entitlement, and the exact pair Defensive Positioning + Tactical Reposition. There is no ASI, feat, XP threshold, class change, multiclassing, choice rollover, or general card-acquisition behavior in this path.
- Tactical Reposition is available only on the actor's own regular tactical turn in this fixture. Commitment spends the Bonus Action and starts Recharge 2; it grants a separate half-current-walking-Speed route budget. Terrain costs are charged against that budget, ordinary movement is unchanged, opportunity-attack offers are suppressed, and Press responses can still occur. Each step revalidates the route. The resource refreshes from the existing regular-turn schedule; unused movement ends with the turn or combat.
- Defensive Positioning is evaluated against an explicit qualifying cover marker adjacent on the prototype 5-foot grid. This avoids treating arbitrary floor as solid terrain. The current marker model does not implement general walls, terrain material, cover geometry, or line-of-sight.
- Incapacitated, stable, and dead actors retain those life states through the capacity update. Leveling is rejected while tactical control, a pending resolution choice, or that actor's modeled traversal/work is active.

## Implemented boundary

Commands: `AwardCharacterMilestone`, `AdvanceCharacterLevel`, and `ActivateTacticalReposition`. Schema 21 persists milestones, per-level Hit Dice, feature grants/runtime, the advancement audit, and explicit cover markers. Earlier snapshot schema encodings remain versioned. The shared test-only host owns this profile; command payloads do not claim authority.

The mandatory Soldier level-1 Overwatch engine described by the class profile is not implemented here. Nor does the fixture model the other level-1 choices or the complete Soldier 1 build. This advancement path is therefore useful for testing the level-up transaction and two level-2 card effects, but is not a complete Soldier class implementation.

Also outside scope: all other classes and levels; class-entry and multiclass procedures; ASIs, feats and their prerequisites; class-card acquisition/replacement/retraining; class resource maxima and repertoire; general terrain and cover; Overwatch and other class engines; XP-mode advancement; production character/profile acquisition; and release approval. These remain open dependencies in the implementation trace.
