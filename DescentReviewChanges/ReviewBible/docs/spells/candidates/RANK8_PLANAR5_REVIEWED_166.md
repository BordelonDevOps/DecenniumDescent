# Rank8 Planar5 — proposed Director Return166

Input authority: **730 applied-reviewed / 118 pending / 0 accepted-unapplied**. Only demiplane, maze, planar-seal, seal-of-banishment, gloom-bind. This manuscript creates no canonical change. See DIRECTOR_DECISION.json for the final static decision.

All sections labelled NEW are spell-local authorship. Exact accepted interface text is in ACCEPTED_INTERFACES.json; the complete source packet is preserved byte-for-byte. Static traces are not runtime, human play, balance, cosmology or release approval.

## demiplane

### Exact native card and all access rows

```json
{
  "id": "demiplane",
  "name": "Demiplane",
  "schools": [
    "Conjuration",
    "Transmutation"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Druid": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Conjuration",
      "baseRpCost": 21
    },
    "Mage": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Conjuration",
      "baseRpCost": 21
    },
    "Wizard": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Conjuration",
      "baseRpCost": 21
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "demiplane",
    "original": {
      "name": "Demiplane",
      "level": 8,
      "resonanceRank": 8,
      "school": "Conjuration",
      "schools": [
        "Conjuration",
        "Transmutation"
      ],
      "placements": [
        {
          "name": "Demiplane",
          "school": "Conjuration",
          "level": 8,
          "summary": "Create a private extradimensional space."
        },
        {
          "name": "Demiplane",
          "school": "Transmutation",
          "level": 8,
          "summary": "Create extradimensional room."
        }
      ],
      "classLevels": {
        "Druid": 8,
        "Mage": 8,
        "Wizard": 8
      },
      "classRanks": {
        "Druid": 8,
        "Mage": 8,
        "Wizard": 8
      },
      "classLearnLevels": {
        "Druid": 15,
        "Mage": 15,
        "Wizard": 15
      },
      "classSchools": {
        "Druid": "Conjuration",
        "Mage": "Conjuration",
        "Wizard": "Conjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Create a private extradimensional space.",
      "alternateSummaries": [
        "Create extradimensional room."
      ],
      "classes": [
        "Druid",
        "Mage",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 188,
        "original": {
          "school": "Conjuration",
          "level": 8,
          "name": "Demiplane",
          "effect": "Create a private extradimensional space.",
          "source_paragraph": 9212,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Planar"
          ],
          "rp_cost": 21
        }
      },
      {
        "index": 813,
        "original": {
          "school": "Transmutation",
          "level": 8,
          "name": "Demiplane",
          "effect": "Create extradimensional room.",
          "source_paragraph": 9987,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Planar"
          ],
          "rp_cost": 21
        }
      }
    ],
    "possibleHistoricalAliases": []
  },
  "reviewFlags": [
    "Core resolution requires an explicit operational interpretation",
    "Not selectable in this spell playtest packet until individual operational review"
  ]
}
```

### authority

NEW authored Planar5 procedures only. Exact input authority is 730 applied-reviewed / 118 pending / 0 accepted-unapplied, 454 standalone procedures. Conference01 525/323 labels are historical. Recorded accepted interfaces are preserved in ACCEPTED_INTERFACES.json; their exact recovered source bytes, not later edited comparisons, control. No canonical index/catalog or closed cohort is changed.

### native

Each native card, Core entry, book placement and class-access row is copied unchanged below. All five are rank 8, Action, range 120 ft, V/S/F, base 21 RP, minimum actual class level 15. Demiplane has two book placements but its actual grants remain Conjuration. Maze uses Wizard Illusion versus Cleric/Mage Universal. Do not create access from a school heading. Original Instantaneous fields remain evidence even where a NEW ongoing component is selected. Gloom Bind retains Core Until dispelled and both conflicting destination names.

### preflight

Use an actually acquired and prepared matrix or an exact class permission. Check remaining Action, usable voice, free gesturing hand and actual focus, rank/RP, target identity, actual range and unobstructed line of effect. A known invalid declaration is rejected before payment. Missing authoritative physical/source prerequisites put the dependent case on hold; a held test is not a successful or paid cast. A lawful declaration defeated only by hidden facts spends its committed costs and produces no diagnostic locating or classifying the hidden fact. Revalidate each component at effect resolution. No retargeting or refund on failure.

### commit

Commit RP, components, source-history and concentration before interruption/save. Cost is 21 plus the exact pre-cast Dissonance surcharge and printed extras only. Limit=max(4,2+PB+max(0,casting modifier)); +1 at limit, +2 at limit+3, ordinary ranked casting blocked at limit+6. First distinct actual Wizard prepared family gives zero BASE strain only; otherwise rank8 base strain is 2. Consecutive same-family Refrain adds 1/2/3 capped at3, idle turns do not reset it. No class perk is assumed without acquisition. An interrupted or resisted cast retains costs and never restores displaced concentration. Exact legal Counterspell/Dispel sources keep their own ranks/costs/checks; Wizard Arch Dispel is rank3/3RP/check INT+PB versus18 for rank8, not rank5 Greater Dispel.

### timing

Use actual elapsed seconds; generated spaces have 1:1 time. An expiry at timestamp t occurs before a newly beginning action at t; already committed atomic crossings finish before an external closure event can settle them. Ordinary Ready commits at preparation, uses held concentration, releases once with a remaining Reaction after its completed trigger, and expires at the next own regular START. Release does not pay/cast/update cadence again; effect deadlines begin on release. A continuing effect retains concentration normally after release. No extra regular START, recharge, rest, recovery, Refrain reset, Hunt pause or resource refresh is created by moving planes.

### transport

Creation of a room/cell is not itself body travel. Door creation is a connection; its use is physical planar crossing. Maze, Seal of Banishment and Gloom Bind admissions are planar displacement, not teleportation. Record ACCEPT versus RESIST separately from save result. Voluntary or forced travel restrictions use their exact predicates, not a generic planar tag. Every creature is separate from gear, including carried unconscious allies, mounts and summons. Check whole-body geometry and actual custody for each. No splitting, duplicating inventories, body-as-cargo target-cap bypass or unprovided portal provider. Record current plane, actual travel provenance, origin anchor and source-character identity separately from native realm, which may remain unknown.

### hardControl

Maze, each Seal of Banishment child and Gloom Bind count as encounter-removal/hard denial and require the shared source-character/target/encounter gate across all that source character’s spells, classes and companions. Spend the gate only on actual establishment, not a resisted or preflight-rejected cast. Prior expenditure or a proved immunity prevents only the applicable control; no new target or refund. No nesting or refresh bypass. Record actual save ability, bonus, DC, die and any chosen lawful reaction/reroll; no generic monster save profile is invented.

### closureExtension

NEW P5-CLOSE extension applies ONLY to true Demiplane room removal, Maze termination and Seal of Banishment child termination. It explicitly reuses BAN-CLOSE-03, BAN-PLACEMENT-HANDOFF-03 and BAN-CONFLICT-04: end the source first, settle every extant identity exactly once to its fixed origin plane/anchor (secondary occupants project their local offset onto the recorded entry/creation anchor), ignore ONLY transport-prevention at the terminal endpoints. Try full body at anchor, legal squeeze, then nearest legal adjacent placement in the same unobstructed region, minimum displacement/greatest overlap/fixed neutral order (south, west, east, north, then SW, SE, NW, NE on the declared grid). Never pass a wall/occupied space or search farther. If none fits, retain a logical-anchor placementConflict with no fabricated footprint, support, falling, movement or new actions; independently legal actions and clocks continue. Normalize only when obstruction is actually removed or lawful relocation resolves it. Loose items retain pending placement/custody, never disappear. Source has ended even while conflict remains. This exception does not permit voluntary entry, internal escape, new portal crossings or Gloom release and does not broaden the pre-existing BAN interfaces.

### custody

Every item has one stable identity, provenance, current holder or ground location, weight, Load and independent deadline. Living bodies, corpses and source-ended absent entities are distinct. Mandatory anatomy/source endings happen first; never delay an expiry to preserve a convenient shape or manufacture a corpse. A generated space supplies only expressly authored floor/boundaries/light/respiration support; no harvestable matter, permanent supplies, inhabitants, treasure, immunity, protected rest, native status, soul rule or automatic Extraction. Preserve cargo danger, taint, claims and Hunt records. Once initiated, Hunt death is normally final except the owner’s extremely rare Divine/Abyssal exception; none of these spells grants that exception.

### qualification

Static proposed authorship and data-only fixtures are not game execution or observed campaign results. Real actor acquisition, creature profiles, destination geometry, native/cosmology facts, environmental needs and equipment not established by a source remain explicit whole-case/branch holds. No runtime, human-play, balance, cosmology or release approval. All closed feat335, completed16/72 and applied spell cohorts remain closed.

### geometry

NEW: create one stable private room identity per source-character, 30 by30 by15 ft internal clear volume with level support at z=0. Walls/ceiling are opaque and impenetrable spell boundaries; ordinary damage does not mine them. Constant ordinary light and sustaining medium accommodate the actual admitted body’s existing respiration only, without healing, supplying food/water, curing hazards or guaranteeing rest. Unsupported/unknown body requirements are held. No canonical named realm or inhabitants are assigned. All objects/furniture other than these bounded supports need their own source.

### entry

NEW: at cast choose CREATE if no extant owned room, otherwise REOPEN that same room. Place one vertical 5-ft-wide by8-ft-high aperture at a perceived supported point within120ft and line of effect, with a legal whole-body exit space. Its room-side aperture is at west wall x=0,y=15,z=0..8, facing +x. Two-way, opaque to sight/sound/line of effect and attacks/projectiles, no viewing window. Each traversal costs5ft actual movement, checks full-body/gear clearance, endpoint blockers, remaining movement and unoccupied arrival. Arrival uses the immediately adjacent room-side/outer-side space selected and recorded at cast, not arbitrary remote placement. No imaginary path is checked. Each entrant must be on the actual cast admission list (owner included); permissions cannot be guessed from a name. All occupants may exit regardless of admission list. The list is fixed for that door; changing it requires a new paid reopen. Failed hidden traversal spends the declared5ft but moves no body and reveals no blocker identity.

### ownership

NEW: one persistent nonconcentrated rank8 generated room, with no elapsed deadline. Each successful cast opens a new60-second nonconcentrated door and closes any previous door to that room after any already atomic transit. Reopening does not move or refresh contents or their independent source deadlines. Failed/countered reopen leaves the old room/door unchanged. No second room, overwriting a nonempty room, inherited ownership by knowing its ID, or changing owner on death/resurrection. Owner death leaves room and contents. NEW owner dismissal requires an Action, perception of the interior within120ft/line of effect, and a genuinely empty room; occupied voluntary dismissal is refused before Action. True dispel can end an occupied room under closureExtension.

### escape

NEW: an occupant may spend its Action to take the internal escape route to its own fixed external entry anchor; a body created inside uses the recorded room-creation external anchor plus its current room-local offset. This is voluntary planar displacement, not teleport, with no cast/RP/proc and no tactical destination choice. Preflight tries full fit at that anchor, legal squeeze, then nearest legal adjacent space in the same unobstructed region, minimum displacement/greatest overlap/neutral order (south, west, east, north, then SW, SE, NW, NE on the declared grid). This explicitly authored escape placement selection grants no far search or voluntary placement-conflict state. Ordinary endpoint travel prevention still applies; all known candidates invalid costs nothing, hidden failure spends the Action. It grants no terminal-blocker exception. It settles the escaping body and actually carried eligible gear only; separate creatures need independent actions or an actual legal transport source. An internal escape never ends the room. Corpses cannot take this action.

### closure

Door suppression makes only that connection unusable while its original60-second clock runs; expiry or actual door dispel/Planar Seal closes it permanently and leaves the nonempty room. Distant owner suppression does not reach the room. NEW room interior/support is one indivisible ongoing generated-space effect: actual suppression of that room component or a successful dispel targeting its perceived interior terminates the room, then P5-CLOSE settles all occupants/corpses/items. The outside doorway gives no remote line of effect to the room. A fixed suppressing field created inside a room that then ceases loses that location and ends; it does not follow returned bodies. Actual room removal clears its registry only after all terminal settlement records are durable; old contents are never recreated by a later new room.

### anatomy

Voluntary growth/entry requires actual full clearance. A mandatory change that no longer fits occurs first and triggers true room termination and P5-CLOSE rather than silently truncating the body or enlarging the fixed room. Actual independent visitors/summons may enter only with proven source access, permission, full fit and recorded closure anchor; they do not become owned creatures.

### Question selections

- **R8PL-SOURCE** — option 1: Retain originals, exact owner corrections and separately scoped accepted mechanics; leave unproved realm identities open. NEW authored Planar5 procedures only. Exact input authority is 730 applied-reviewed / 118 pending / 0 accepted-unapplied, 454 standalone procedures. Conference01 525/323 labels are historical. Recorded accepted interfaces are preserved in ACCEPTED_INTERFACES.json; their exact recovered source bytes, not later edited comparisons, control. No canonical index/catalog or closed cohort is changed.
- **R8PL-TRANSACTIONS** — option 1: Classify each spell operation explicitly: creation, portal connection, physical crossing, planar displacement, tether and mandatory ending. Creation of a room/cell is not itself body travel. Door creation is a connection; its use is physical planar crossing. Maze, Seal of Banishment and Gloom Bind admissions are planar displacement, not teleportation. Record ACCEPT versus RESIST separately from save result. Voluntary or forced travel restrictions use their exact predicates, not a generic planar tag. Every creature is separate from gear, including carried unconscious allies, mounts and summons. Check whole-body geometry and actual custody for each. No splitting, duplicating inventories, body-as-cargo target-cap bypass or unprovided portal provider. Record current plane, actual travel provenance, origin anchor and source-character identity separately from native realm, which may remain unknown.
- **R8PL-CLOCKS** — option 1: Keep actual elapsed deadlines and existing source clocks; label any different spell-local clock as a separately reviewed exception. Use actual elapsed seconds; generated spaces have 1:1 time. An expiry at timestamp t occurs before a newly beginning action at t; already committed atomic crossings finish before an external closure event can settle them. Ordinary Ready commits at preparation, uses held concentration, releases once with a remaining Reaction after its completed trigger, and expires at the next own regular START. Release does not pay/cast/update cadence again; effect deadlines begin on release. A continuing effect retains concentration normally after release. No extra regular START, recharge, rest, recovery, Refrain reset, Hunt pause or resource refresh is created by moving planes.
- **R8PL-DEMI-GEOMETRY** — option 1: Author a bounded persistent room with explicit dimensions, support, environmental behavior and one actual access interface. NEW: create one stable private room identity per source-character, 30 by30 by15 ft internal clear volume with level support at z=0. Walls/ceiling are opaque and impenetrable spell boundaries; ordinary damage does not mine them. Constant ordinary light and sustaining medium accommodate the actual admitted body’s existing respiration only, without healing, supplying food/water, curing hazards or guaranteeing rest. Unsupported/unknown body requirements are held. No canonical named realm or inhabitants are assigned. All objects/furniture other than these bounded supports need their own source.
- **R8PL-DEMI-ENTRY** — option 1: Separate persistent room identity from a finite connection; define full local/remote entry predicates and later reopening. NEW: at cast choose CREATE if no extant owned room, otherwise REOPEN that same room. Place one vertical 5-ft-wide by8-ft-high aperture at a perceived supported point within120ft and line of effect, with a legal whole-body exit space. Its room-side aperture is at west wall x=0,y=15,z=0..8, facing +x. Two-way, opaque to sight/sound/line of effect and attacks/projectiles, no viewing window. Each traversal costs5ft actual movement, checks full-body/gear clearance, endpoint blockers, remaining movement and unoccupied arrival. Arrival uses the immediately adjacent room-side/outer-side space selected and recorded at cast, not arbitrary remote placement. No imaginary path is checked. Each entrant must be on the actual cast admission list (owner included); permissions cannot be guessed from a name. All occupants may exit regardless of admission list. The list is fixed for that door; changing it requires a new paid reopen. Failed hidden traversal spends the declared5ft but moves no body and reveals no blocker identity.
- **R8PL-DEMI-OWNERSHIP** — option 1: Choose a finite active-space ownership rule while preserving exact occupants, objects and lawful transfers; never overwrite a nonempty room. NEW: one persistent nonconcentrated rank8 generated room, with no elapsed deadline. Each successful cast opens a new60-second nonconcentrated door and closes any previous door to that room after any already atomic transit. Reopening does not move or refresh contents or their independent source deadlines. Failed/countered reopen leaves the old room/door unchanged. No second room, overwriting a nonempty room, inherited ownership by knowing its ID, or changing owner on death/resurrection. Owner death leaves room and contents. NEW owner dismissal requires an Action, perception of the interior within120ft/line of effect, and a genuinely empty room; occupied voluntary dismissal is refused before Action. True dispel can end an occupied room under closureExtension.
- **R8PL-DEMI-CLOSURE** — option 1: Choose separate suppression/dispelling behavior for room and connection, with deterministic settlement of every extant identity. Door suppression makes only that connection unusable while its original60-second clock runs; expiry or actual door dispel/Planar Seal closes it permanently and leaves the nonempty room. Distant owner suppression does not reach the room. NEW room interior/support is one indivisible ongoing generated-space effect: actual suppression of that room component or a successful dispel targeting its perceived interior terminates the room, then P5-CLOSE settles all occupants/corpses/items. The outside doorway gives no remote line of effect to the room. A fixed suppressing field created inside a room that then ceases loses that location and ends; it does not follow returned bodies. Actual room removal clears its registry only after all terminal settlement records are durable; old contents are never recreated by a later new room.
- **R8PL-DEMI-CONTENT** — option 1: Use a newly generated spell-space only with bounded privacy and real ongoing creature/effect records. NEW: create one stable private room identity per source-character, 30 by30 by15 ft internal clear volume with level support at z=0. Walls/ceiling are opaque and impenetrable spell boundaries; ordinary damage does not mine them. Constant ordinary light and sustaining medium accommodate the actual admitted body’s existing respiration only, without healing, supplying food/water, curing hazards or guaranteeing rest. Unsupported/unknown body requirements are held. No canonical named realm or inhabitants are assigned. All objects/furniture other than these bounded supports need their own source. Every item has one stable identity, provenance, current holder or ground location, weight, Load and independent deadline. Living bodies, corpses and source-ended absent entities are distinct. Mandatory anatomy/source endings happen first; never delay an expiry to preserve a convenient shape or manufacture a corpse. A generated space supplies only expressly authored floor/boundaries/light/respiration support; no harvestable matter, permanent supplies, inhabitants, treasure, immunity, protected rest, native status, soul rule or automatic Extraction. Preserve cargo danger, taint, claims and Hunt records. Once initiated, Hunt death is normally final except the owner’s extremely rare Divine/Abyssal exception; none of these spells grants that exception.

### Cases and retained holds

P5-DEMI-A, P5-DEMI-B, P5-DEMI-A/permission, P5-DEMI-A/oversize, P5-DEMI-A/second-room, P5-DEMI-A/unknown-owner, P5-DEMI-B/room-dispel, P5-DEMI-B/room-suppression, P5-DEMI-A/owner-death

P5-H-SOURCE, P5-H-ACCESS, P5-H-COSMOLOGY, P5-H-CONTENT, P5-H-PHYSICAL, P5-H-EQUIPMENT, P5-H-LIFECYCLE, P5-H-INFORMATION, P5-H-STRUCTURE, P5-H-VISITOR, P5-H-RUNTIME, P5-H-HUMAN-PLAY, P5-H-BALANCE, P5-H-RELEASE

## maze

### Exact native card and all access rows

```json
{
  "id": "maze",
  "name": "Maze",
  "schools": [
    "Illusion",
    "Universal"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Universal",
      "baseRpCost": 21
    },
    "Mage": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Universal",
      "baseRpCost": 21
    },
    "Wizard": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Illusion",
      "baseRpCost": 21
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "maze",
    "original": {
      "name": "Maze",
      "level": 8,
      "resonanceRank": 8,
      "school": "Illusion",
      "schools": [
        "Illusion",
        "Universal"
      ],
      "placements": [
        {
          "name": "Maze",
          "school": "Illusion",
          "level": 8,
          "summary": "Trap creature in extradimensional labyrinth."
        },
        {
          "name": "Maze",
          "school": "Universal",
          "level": 8,
          "summary": "Trap creature in extradimensional labyrinth."
        }
      ],
      "classLevels": {
        "Cleric": 8,
        "Mage": 8,
        "Wizard": 8
      },
      "classRanks": {
        "Cleric": 8,
        "Mage": 8,
        "Wizard": 8
      },
      "classLearnLevels": {
        "Cleric": 15,
        "Mage": 15,
        "Wizard": 15
      },
      "classSchools": {
        "Cleric": "Universal",
        "Mage": "Universal",
        "Wizard": "Illusion"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Trap creature in extradimensional labyrinth.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Mage",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 604,
        "original": {
          "school": "Illusion",
          "level": 8,
          "name": "Maze",
          "effect": "Trap creature in extradimensional labyrinth.",
          "source_paragraph": 9728,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Utility"
          ],
          "rp_cost": 21
        }
      },
      {
        "index": 917,
        "original": {
          "school": "Universal",
          "level": 8,
          "name": "Maze",
          "effect": "Trap creature in extradimensional labyrinth.",
          "source_paragraph": 10116,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Utility"
          ],
          "rp_cost": 21
        }
      }
    ],
    "possibleHistoricalAliases": []
  },
  "reviewFlags": [
    "Core resolution requires an explicit operational interpretation",
    "Not selectable in this spell playtest packet until individual operational review"
  ]
}
```

### authority

NEW authored Planar5 procedures only. Exact input authority is 730 applied-reviewed / 118 pending / 0 accepted-unapplied, 454 standalone procedures. Conference01 525/323 labels are historical. Recorded accepted interfaces are preserved in ACCEPTED_INTERFACES.json; their exact recovered source bytes, not later edited comparisons, control. No canonical index/catalog or closed cohort is changed.

### native

Each native card, Core entry, book placement and class-access row is copied unchanged below. All five are rank 8, Action, range 120 ft, V/S/F, base 21 RP, minimum actual class level 15. Demiplane has two book placements but its actual grants remain Conjuration. Maze uses Wizard Illusion versus Cleric/Mage Universal. Do not create access from a school heading. Original Instantaneous fields remain evidence even where a NEW ongoing component is selected. Gloom Bind retains Core Until dispelled and both conflicting destination names.

### preflight

Use an actually acquired and prepared matrix or an exact class permission. Check remaining Action, usable voice, free gesturing hand and actual focus, rank/RP, target identity, actual range and unobstructed line of effect. A known invalid declaration is rejected before payment. Missing authoritative physical/source prerequisites put the dependent case on hold; a held test is not a successful or paid cast. A lawful declaration defeated only by hidden facts spends its committed costs and produces no diagnostic locating or classifying the hidden fact. Revalidate each component at effect resolution. No retargeting or refund on failure.

### commit

Commit RP, components, source-history and concentration before interruption/save. Cost is 21 plus the exact pre-cast Dissonance surcharge and printed extras only. Limit=max(4,2+PB+max(0,casting modifier)); +1 at limit, +2 at limit+3, ordinary ranked casting blocked at limit+6. First distinct actual Wizard prepared family gives zero BASE strain only; otherwise rank8 base strain is 2. Consecutive same-family Refrain adds 1/2/3 capped at3, idle turns do not reset it. No class perk is assumed without acquisition. An interrupted or resisted cast retains costs and never restores displaced concentration. Exact legal Counterspell/Dispel sources keep their own ranks/costs/checks; Wizard Arch Dispel is rank3/3RP/check INT+PB versus18 for rank8, not rank5 Greater Dispel.

### timing

Use actual elapsed seconds; generated spaces have 1:1 time. An expiry at timestamp t occurs before a newly beginning action at t; already committed atomic crossings finish before an external closure event can settle them. Ordinary Ready commits at preparation, uses held concentration, releases once with a remaining Reaction after its completed trigger, and expires at the next own regular START. Release does not pay/cast/update cadence again; effect deadlines begin on release. A continuing effect retains concentration normally after release. No extra regular START, recharge, rest, recovery, Refrain reset, Hunt pause or resource refresh is created by moving planes.

### transport

Creation of a room/cell is not itself body travel. Door creation is a connection; its use is physical planar crossing. Maze, Seal of Banishment and Gloom Bind admissions are planar displacement, not teleportation. Record ACCEPT versus RESIST separately from save result. Voluntary or forced travel restrictions use their exact predicates, not a generic planar tag. Every creature is separate from gear, including carried unconscious allies, mounts and summons. Check whole-body geometry and actual custody for each. No splitting, duplicating inventories, body-as-cargo target-cap bypass or unprovided portal provider. Record current plane, actual travel provenance, origin anchor and source-character identity separately from native realm, which may remain unknown.

### hardControl

Maze, each Seal of Banishment child and Gloom Bind count as encounter-removal/hard denial and require the shared source-character/target/encounter gate across all that source character’s spells, classes and companions. Spend the gate only on actual establishment, not a resisted or preflight-rejected cast. Prior expenditure or a proved immunity prevents only the applicable control; no new target or refund. No nesting or refresh bypass. Record actual save ability, bonus, DC, die and any chosen lawful reaction/reroll; no generic monster save profile is invented.

### closureExtension

NEW P5-CLOSE extension applies ONLY to true Demiplane room removal, Maze termination and Seal of Banishment child termination. It explicitly reuses BAN-CLOSE-03, BAN-PLACEMENT-HANDOFF-03 and BAN-CONFLICT-04: end the source first, settle every extant identity exactly once to its fixed origin plane/anchor (secondary occupants project their local offset onto the recorded entry/creation anchor), ignore ONLY transport-prevention at the terminal endpoints. Try full body at anchor, legal squeeze, then nearest legal adjacent placement in the same unobstructed region, minimum displacement/greatest overlap/fixed neutral order (south, west, east, north, then SW, SE, NW, NE on the declared grid). Never pass a wall/occupied space or search farther. If none fits, retain a logical-anchor placementConflict with no fabricated footprint, support, falling, movement or new actions; independently legal actions and clocks continue. Normalize only when obstruction is actually removed or lawful relocation resolves it. Loose items retain pending placement/custody, never disappear. Source has ended even while conflict remains. This exception does not permit voluntary entry, internal escape, new portal crossings or Gloom release and does not broaden the pre-existing BAN interfaces.

### custody

Every item has one stable identity, provenance, current holder or ground location, weight, Load and independent deadline. Living bodies, corpses and source-ended absent entities are distinct. Mandatory anatomy/source endings happen first; never delay an expiry to preserve a convenient shape or manufacture a corpse. A generated space supplies only expressly authored floor/boundaries/light/respiration support; no harvestable matter, permanent supplies, inhabitants, treasure, immunity, protected rest, native status, soul rule or automatic Extraction. Preserve cargo danger, taint, claims and Hunt records. Once initiated, Hunt death is normally final except the owner’s extremely rare Divine/Abyssal exception; none of these spells grants that exception.

### qualification

Static proposed authorship and data-only fixtures are not game execution or observed campaign results. Real actor acquisition, creature profiles, destination geometry, native/cosmology facts, environmental needs and equipment not established by a source remain explicit whole-case/branch holds. No runtime, human-play, balance, cosmology or release approval. All closed feat335, completed16/72 and applied spell cohorts remain closed.

### admission

NEW: select one perceived actual creature within120ft/line of effect. WIS save against the actual class-school DC; ACCEPT may voluntarily fail, RESIST rolls. On failure and a free hard-control gate, displace that body and actual gear into its own generated labyrinth. No unselected carried passenger is silently banished; detach only if independently legal, otherwise the component fails. NEW concentration, maximum60 elapsed seconds from establishment; original Instantaneous remains untouched. One Maze per caster via concentration and one active Maze per primary target. Known active primary or target absent behind planar opacity is invalid preflight, not a refresh. Starting a legal new concentrated spell ends an old concentration before interruption; no refund or restoration.

### topology

NEW: use the exact finite16-node tree in MAZE_TOPOLOGY.json. For the current body footprint width/depth b and height h, module size L=5*ceil((max(b,width,depth)+10)/5); clear corridor width L-5, ceiling H=5*ceil((h+5)/5), room clear width L-0.5. Nodes are centers (L*(x+0.5),L*(y+0.5),0), x/y=0..3. Open listed edges have a centered corridor of width L-5 through each intervening wall; closed edges and exterior boundary are opaque0.5ft-thick spell walls. Accepted grid-metric ordinary movement applies, adjacent center distance L. Entry=(0,0), exit=(3,3). The cast ID and target ID are the stable seed; this revision intentionally uses the same fixed base topology for every seed, recorded unchanged (no random rotation or private reroll). Actual light reveals only ordinary unobstructed sight, not an automatic map. No regeneration invalidates explored routes. Wall material cannot be harvested or conventionally broken; actual independently legal matter/space effects require an explicit scope rather than assumed universal immunity or passage.

### escape

At the actual exit node, the primary may spend an Action touching the visible exit to end the Maze. Normal movement costs/budgets and visibility apply; there is no imported Intelligence roll, species privilege or extra action. Any actual independent lawful exit by the primary also ends it. A supported floor and sustaining medium preserve existing respiration; no safe-rest or immunity promise. Exact unavailable environmental/body needs are held. A same-plane Dimensional Door cannot cross to the original plane; ordinary True Seeing does not erase physical walls. A proved actual Faction Portal or other source may work only with its own access, legal destination, standing and body predicates.

### lifecycle

Concentration loss, deadline, actual suppression of the Maze application, successful perceived-effect dispel, primary death, primary source expiry or a mandatory anatomy that exceeds existing clearance all end this application once. Distant caster suppression alone does not reach it. Ended primaries remain absent; corpses remain dead. P5-CLOSE settles each remaining visitor, corpse and object once. The geometry is never extended just to keep confinement. Secondary visitors require their own exact source/geometry/knowledge and anchor at entry, retain their own source lifetimes and do not automatically become maze primaries. No one gains control of them or free creature content. Persistent placement conflict is external and cannot extend Maze beyond60seconds.

### Question selections

- **R8PL-SOURCE** — option 1: Retain originals, exact owner corrections and separately scoped accepted mechanics; leave unproved realm identities open. NEW authored Planar5 procedures only. Exact input authority is 730 applied-reviewed / 118 pending / 0 accepted-unapplied, 454 standalone procedures. Conference01 525/323 labels are historical. Recorded accepted interfaces are preserved in ACCEPTED_INTERFACES.json; their exact recovered source bytes, not later edited comparisons, control. No canonical index/catalog or closed cohort is changed.
- **R8PL-TRANSACTIONS** — option 1: Classify each spell operation explicitly: creation, portal connection, physical crossing, planar displacement, tether and mandatory ending. Creation of a room/cell is not itself body travel. Door creation is a connection; its use is physical planar crossing. Maze, Seal of Banishment and Gloom Bind admissions are planar displacement, not teleportation. Record ACCEPT versus RESIST separately from save result. Voluntary or forced travel restrictions use their exact predicates, not a generic planar tag. Every creature is separate from gear, including carried unconscious allies, mounts and summons. Check whole-body geometry and actual custody for each. No splitting, duplicating inventories, body-as-cargo target-cap bypass or unprovided portal provider. Record current plane, actual travel provenance, origin anchor and source-character identity separately from native realm, which may remain unknown.
- **R8PL-CLOCKS** — option 1: Keep actual elapsed deadlines and existing source clocks; label any different spell-local clock as a separately reviewed exception. Use actual elapsed seconds; generated spaces have 1:1 time. An expiry at timestamp t occurs before a newly beginning action at t; already committed atomic crossings finish before an external closure event can settle them. Ordinary Ready commits at preparation, uses held concentration, releases once with a remaining Reaction after its completed trigger, and expires at the next own regular START. Release does not pay/cast/update cadence again; effect deadlines begin on release. A continuing effect retains concentration normally after release. No extra regular START, recharge, rest, recovery, Refrain reset, Hunt pause or resource refresh is created by moving planes.
- **R8PL-MAZE-ADMISSION** — option 1: Author a genuine extradimensional captivity application with explicit initial resistance, hard-control admission and duration. NEW: select one perceived actual creature within120ft/line of effect. WIS save against the actual class-school DC; ACCEPT may voluntarily fail, RESIST rolls. On failure and a free hard-control gate, displace that body and actual gear into its own generated labyrinth. No unselected carried passenger is silently banished; detach only if independently legal, otherwise the component fails. NEW concentration, maximum60 elapsed seconds from establishment; original Instantaneous remains untouched. One Maze per caster via concentration and one active Maze per primary target. Known active primary or target absent behind planar opacity is invalid preflight, not a refresh. Starting a legal new concentrated spell ends an old concentration before interruption; no refund or restoration.
- **R8PL-MAZE-TOPOLOGY** — option 1: Define deterministic generated topology/seed and a finite ordinary navigation/escape procedure, including small and large bodies. NEW: use the exact finite16-node tree in MAZE_TOPOLOGY.json. For the current body footprint width/depth b and height h, module size L=5*ceil((max(b,width,depth)+10)/5); clear corridor width L-5, ceiling H=5*ceil((h+5)/5), room clear width L-0.5. Nodes are centers (L*(x+0.5),L*(y+0.5),0), x/y=0..3. Open listed edges have a centered corridor of width L-5 through each intervening wall; closed edges and exterior boundary are opaque0.5ft-thick spell walls. Accepted grid-metric ordinary movement applies, adjacent center distance L. Entry=(0,0), exit=(3,3). The cast ID and target ID are the stable seed; this revision intentionally uses the same fixed base topology for every seed, recorded unchanged (no random rotation or private reroll). Actual light reveals only ordinary unobstructed sight, not an automatic map. No regeneration invalidates explored routes. Wall material cannot be harvested or conventionally broken; actual independently legal matter/space effects require an explicit scope rather than assumed universal immunity or passage.
- **R8PL-MAZE-LIFECYCLE** — option 1: Specify a complete closure/escape lifecycle and real body/object placement with bounded source-specific exceptions. Concentration loss, deadline, actual suppression of the Maze application, successful perceived-effect dispel, primary death, primary source expiry or a mandatory anatomy that exceeds existing clearance all end this application once. Distant caster suppression alone does not reach it. Ended primaries remain absent; corpses remain dead. P5-CLOSE settles each remaining visitor, corpse and object once. The geometry is never extended just to keep confinement. Secondary visitors require their own exact source/geometry/knowledge and anchor at entry, retain their own source lifetimes and do not automatically become maze primaries. No one gains control of them or free creature content. Persistent placement conflict is external and cannot extend Maze beyond60seconds.
- **R8PL-MAZE-COUNTERPLAY** — option 1: Apply each actual escape, information and suppression source by its exact predicate; a real maze remains physically real. At the actual exit node, the primary may spend an Action touching the visible exit to end the Maze. Normal movement costs/budgets and visibility apply; there is no imported Intelligence roll, species privilege or extra action. Any actual independent lawful exit by the primary also ends it. A supported floor and sustaining medium preserve existing respiration; no safe-rest or immunity promise. Exact unavailable environmental/body needs are held. A same-plane Dimensional Door cannot cross to the original plane; ordinary True Seeing does not erase physical walls. A proved actual Faction Portal or other source may work only with its own access, legal destination, standing and body predicates.
- **R8PL-MAZE-MULTIPLE** — option 1: Choose one bounded application/space policy with actual perceived targets and original clocks. NEW: select one perceived actual creature within120ft/line of effect. WIS save against the actual class-school DC; ACCEPT may voluntarily fail, RESIST rolls. On failure and a free hard-control gate, displace that body and actual gear into its own generated labyrinth. No unselected carried passenger is silently banished; detach only if independently legal, otherwise the component fails. NEW concentration, maximum60 elapsed seconds from establishment; original Instantaneous remains untouched. One Maze per caster via concentration and one active Maze per primary target. Known active primary or target absent behind planar opacity is invalid preflight, not a refresh. Starting a legal new concentrated spell ends an old concentration before interruption; no refund or restoration.

### Cases and retained holds

P5-MAZE-A, P5-MAZE-B, P5-MAZE-A/save-success, P5-MAZE-A/shared-hard-guard, P5-MAZE-A/same-plane-door, P5-MAZE-A/death, P5-MAZE-B/visitor, P5-MAZE-B/mandatory-anatomy

P5-H-SOURCE, P5-H-ACCESS, P5-H-COSMOLOGY, P5-H-CONTENT, P5-H-PHYSICAL, P5-H-EQUIPMENT, P5-H-LIFECYCLE, P5-H-INFORMATION, P5-H-STRUCTURE, P5-H-VISITOR, P5-H-RUNTIME, P5-H-HUMAN-PLAY, P5-H-BALANCE, P5-H-RELEASE

## planar-seal

### Exact native card and all access rows

```json
{
  "id": "planar-seal",
  "name": "Planar Seal",
  "schools": [
    "Abjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Abjuration",
      "baseRpCost": 21
    },
    "Druid": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Abjuration",
      "baseRpCost": 21
    },
    "Mage": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Abjuration",
      "baseRpCost": 21
    },
    "Wizard": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Abjuration",
      "baseRpCost": 21
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "planar-seal",
    "original": {
      "name": "Planar Seal",
      "level": 8,
      "resonanceRank": 8,
      "school": "Abjuration",
      "schools": [
        "Abjuration"
      ],
      "placements": [
        {
          "name": "Planar Seal",
          "school": "Abjuration",
          "level": 8,
          "summary": "Close all connections to a specific plane within 1 mile."
        }
      ],
      "classLevels": {
        "Cleric": 8,
        "Druid": 8,
        "Mage": 8,
        "Wizard": 8
      },
      "classRanks": {
        "Cleric": 8,
        "Druid": 8,
        "Mage": 8,
        "Wizard": 8
      },
      "classLearnLevels": {
        "Cleric": 15,
        "Druid": 15,
        "Mage": 15,
        "Wizard": 15
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Druid": "Abjuration",
        "Mage": "Abjuration",
        "Wizard": "Abjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Close all connections to a specific plane within 1 mile.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Mage",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 85,
        "original": {
          "school": "Abjuration",
          "level": 8,
          "name": "Planar Seal",
          "effect": "Close all connections to a specific plane within 1 mile.",
          "source_paragraph": 9084,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Planar"
          ],
          "rp_cost": 21
        }
      }
    ],
    "possibleHistoricalAliases": []
  },
  "reviewFlags": [
    "Core resolution requires an explicit operational interpretation",
    "Not selectable in this spell playtest packet until individual operational review"
  ]
}
```

### authority

NEW authored Planar5 procedures only. Exact input authority is 730 applied-reviewed / 118 pending / 0 accepted-unapplied, 454 standalone procedures. Conference01 525/323 labels are historical. Recorded accepted interfaces are preserved in ACCEPTED_INTERFACES.json; their exact recovered source bytes, not later edited comparisons, control. No canonical index/catalog or closed cohort is changed.

### native

Each native card, Core entry, book placement and class-access row is copied unchanged below. All five are rank 8, Action, range 120 ft, V/S/F, base 21 RP, minimum actual class level 15. Demiplane has two book placements but its actual grants remain Conjuration. Maze uses Wizard Illusion versus Cleric/Mage Universal. Do not create access from a school heading. Original Instantaneous fields remain evidence even where a NEW ongoing component is selected. Gloom Bind retains Core Until dispelled and both conflicting destination names.

### preflight

Use an actually acquired and prepared matrix or an exact class permission. Check remaining Action, usable voice, free gesturing hand and actual focus, rank/RP, target identity, actual range and unobstructed line of effect. A known invalid declaration is rejected before payment. Missing authoritative physical/source prerequisites put the dependent case on hold; a held test is not a successful or paid cast. A lawful declaration defeated only by hidden facts spends its committed costs and produces no diagnostic locating or classifying the hidden fact. Revalidate each component at effect resolution. No retargeting or refund on failure.

### commit

Commit RP, components, source-history and concentration before interruption/save. Cost is 21 plus the exact pre-cast Dissonance surcharge and printed extras only. Limit=max(4,2+PB+max(0,casting modifier)); +1 at limit, +2 at limit+3, ordinary ranked casting blocked at limit+6. First distinct actual Wizard prepared family gives zero BASE strain only; otherwise rank8 base strain is 2. Consecutive same-family Refrain adds 1/2/3 capped at3, idle turns do not reset it. No class perk is assumed without acquisition. An interrupted or resisted cast retains costs and never restores displaced concentration. Exact legal Counterspell/Dispel sources keep their own ranks/costs/checks; Wizard Arch Dispel is rank3/3RP/check INT+PB versus18 for rank8, not rank5 Greater Dispel.

### timing

Use actual elapsed seconds; generated spaces have 1:1 time. An expiry at timestamp t occurs before a newly beginning action at t; already committed atomic crossings finish before an external closure event can settle them. Ordinary Ready commits at preparation, uses held concentration, releases once with a remaining Reaction after its completed trigger, and expires at the next own regular START. Release does not pay/cast/update cadence again; effect deadlines begin on release. A continuing effect retains concentration normally after release. No extra regular START, recharge, rest, recovery, Refrain reset, Hunt pause or resource refresh is created by moving planes.

### transport

Creation of a room/cell is not itself body travel. Door creation is a connection; its use is physical planar crossing. Maze, Seal of Banishment and Gloom Bind admissions are planar displacement, not teleportation. Record ACCEPT versus RESIST separately from save result. Voluntary or forced travel restrictions use their exact predicates, not a generic planar tag. Every creature is separate from gear, including carried unconscious allies, mounts and summons. Check whole-body geometry and actual custody for each. No splitting, duplicating inventories, body-as-cargo target-cap bypass or unprovided portal provider. Record current plane, actual travel provenance, origin anchor and source-character identity separately from native realm, which may remain unknown.

### hardControl

Maze, each Seal of Banishment child and Gloom Bind count as encounter-removal/hard denial and require the shared source-character/target/encounter gate across all that source character’s spells, classes and companions. Spend the gate only on actual establishment, not a resisted or preflight-rejected cast. Prior expenditure or a proved immunity prevents only the applicable control; no new target or refund. No nesting or refresh bypass. Record actual save ability, bonus, DC, die and any chosen lawful reaction/reroll; no generic monster save profile is invented.

### closureExtension

NEW P5-CLOSE extension applies ONLY to true Demiplane room removal, Maze termination and Seal of Banishment child termination. It explicitly reuses BAN-CLOSE-03, BAN-PLACEMENT-HANDOFF-03 and BAN-CONFLICT-04: end the source first, settle every extant identity exactly once to its fixed origin plane/anchor (secondary occupants project their local offset onto the recorded entry/creation anchor), ignore ONLY transport-prevention at the terminal endpoints. Try full body at anchor, legal squeeze, then nearest legal adjacent placement in the same unobstructed region, minimum displacement/greatest overlap/fixed neutral order (south, west, east, north, then SW, SE, NW, NE on the declared grid). Never pass a wall/occupied space or search farther. If none fits, retain a logical-anchor placementConflict with no fabricated footprint, support, falling, movement or new actions; independently legal actions and clocks continue. Normalize only when obstruction is actually removed or lawful relocation resolves it. Loose items retain pending placement/custody, never disappear. Source has ended even while conflict remains. This exception does not permit voluntary entry, internal escape, new portal crossings or Gloom release and does not broaden the pre-existing BAN interfaces.

### custody

Every item has one stable identity, provenance, current holder or ground location, weight, Load and independent deadline. Living bodies, corpses and source-ended absent entities are distinct. Mandatory anatomy/source endings happen first; never delay an expiry to preserve a convenient shape or manufacture a corpse. A generated space supplies only expressly authored floor/boundaries/light/respiration support; no harvestable matter, permanent supplies, inhabitants, treasure, immunity, protected rest, native status, soul rule or automatic Extraction. Preserve cargo danger, taint, claims and Hunt records. Once initiated, Hunt death is normally final except the owner’s extremely rare Divine/Abyssal exception; none of these spells grants that exception.

### qualification

Static proposed authorship and data-only fixtures are not game execution or observed campaign results. Real actor acquisition, creature profiles, destination geometry, native/cosmology facts, environmental needs and equipment not established by a source remain explicit whole-case/branch holds. No runtime, human-play, balance, cosmology or release approval. All closed feat335, completed16/72 and applied spell cohorts remain closed.

### area

NEW: select exactly one established plane identity, not a guessed realm equivalence. Place a fixed point within120ft, perceived and in line of effect. The affected region is a closed radius5280ft area centered there on the caster’s current plane. Use the accepted grid metric: each orthogonal/diagonal neighboring5ft tile costs5ft; the coplanar footprint uses max(abs(dx),abs(dy))<=5280. The conceptual region is a sphere; exact off-grid/vertical3D templates retain the existing geometry hold, not a silently new Euclidean metric. A connection qualifies when any part of its actual local endpoint intersects this region and its other endpoint belongs to the selected different plane. Exactly on the boundary qualifies. Different-plane coordinate charts are never subtracted. ALL qualifying connections are included, even endpoints behind cover or unknown to the caster: this explicitly grants closure through cover within the region, not a locator, remote perception or feedback count.

### connections

NEW: actual live transit apertures, real cross-plane sight/information channels and a source-explicit sustained cross-plane tether are connections. An extant temporarily suppressed connection still qualifies and ends permanently. A portal/window is closed as one whole linked edge, not clipped into a smaller opening. Planar Window vision/native-detection ends with its channel; Faction Portal closes under its actual ending rules; Demiplane loses its door only. A mere past arrival, summoned body, identity/native relationship, Maze/exile confinement with no live channel, Gloom’s local exit restriction, same-plane telepathy, soul claim or realm itself is not a connection. Unknown cross-plane telepathy/tether eligibility stays held until the exact source establishes its live endpoints; no universal telepathy rewrite.

### duration

One-time atomic closure at resolution. No concentration, ongoing prohibition, continuing dispellable seal, future-target detector or new plane. Later independently legal paid opening can succeed. Persisting bodies, cargo, rooms, independent effects and clocks remain. A specific source immunity/end consequence is honored where proved; no invented rank-check, universal dispel or unsummoning is added.

### transit

An already committed crossing finishes atomically before closure. Ordinary Ready releases after the completed trigger and therefore cannot cut a traveler in half. A true interrupt needs its own proved source and exact timing; absent one, no interrupt is invented. Mandatory terminal Banishment returns and the explicitly scoped P5-CLOSE transitions are settlement events, not continuing open connections, and are not stopped by Planar Seal. The new closure does not reopen or amend those older interfaces. Resolve qualifying edges in stable connection-ID order for bookkeeping; no order grants extra actions or half transfers.

### Question selections

- **R8PL-SOURCE** — option 1: Retain originals, exact owner corrections and separately scoped accepted mechanics; leave unproved realm identities open. NEW authored Planar5 procedures only. Exact input authority is 730 applied-reviewed / 118 pending / 0 accepted-unapplied, 454 standalone procedures. Conference01 525/323 labels are historical. Recorded accepted interfaces are preserved in ACCEPTED_INTERFACES.json; their exact recovered source bytes, not later edited comparisons, control. No canonical index/catalog or closed cohort is changed.
- **R8PL-TRANSACTIONS** — option 1: Classify each spell operation explicitly: creation, portal connection, physical crossing, planar displacement, tether and mandatory ending. Creation of a room/cell is not itself body travel. Door creation is a connection; its use is physical planar crossing. Maze, Seal of Banishment and Gloom Bind admissions are planar displacement, not teleportation. Record ACCEPT versus RESIST separately from save result. Voluntary or forced travel restrictions use their exact predicates, not a generic planar tag. Every creature is separate from gear, including carried unconscious allies, mounts and summons. Check whole-body geometry and actual custody for each. No splitting, duplicating inventories, body-as-cargo target-cap bypass or unprovided portal provider. Record current plane, actual travel provenance, origin anchor and source-character identity separately from native realm, which may remain unknown.
- **R8PL-CLOCKS** — option 1: Keep actual elapsed deadlines and existing source clocks; label any different spell-local clock as a separately reviewed exception. Use actual elapsed seconds; generated spaces have 1:1 time. An expiry at timestamp t occurs before a newly beginning action at t; already committed atomic crossings finish before an external closure event can settle them. Ordinary Ready commits at preparation, uses held concentration, releases once with a remaining Reaction after its completed trigger, and expires at the next own regular START. Release does not pay/cast/update cadence again; effect deadlines begin on release. A continuing effect retains concentration normally after release. No extra regular START, recharge, rest, recovery, Refrain reset, Hunt pause or resource refresh is created by moving planes.
- **R8PL-SEAL-AREA** — option 1: Select one actual plane identity plus a fixed local one-mile region, explicitly reconciling120ft placement range. NEW: select exactly one established plane identity, not a guessed realm equivalence. Place a fixed point within120ft, perceived and in line of effect. The affected region is a closed radius5280ft area centered there on the caster’s current plane. Use the accepted grid metric: each orthogonal/diagonal neighboring5ft tile costs5ft; the coplanar footprint uses max(abs(dx),abs(dy))<=5280. The conceptual region is a sphere; exact off-grid/vertical3D templates retain the existing geometry hold, not a silently new Euclidean metric. A connection qualifies when any part of its actual local endpoint intersects this region and its other endpoint belongs to the selected different plane. Exactly on the boundary qualifies. Different-plane coordinate charts are never subtracted. ALL qualifying connections are included, even endpoints behind cover or unknown to the caster: this explicitly grants closure through cover within the region, not a locator, remote perception or feedback count.
- **R8PL-SEAL-CONNECTION** — option 1: Define an exact connection taxonomy and apply ALL qualifying connections to the selected plane; distinguish existing effects from ongoing links. NEW: actual live transit apertures, real cross-plane sight/information channels and a source-explicit sustained cross-plane tether are connections. An extant temporarily suppressed connection still qualifies and ends permanently. A portal/window is closed as one whole linked edge, not clipped into a smaller opening. Planar Window vision/native-detection ends with its channel; Faction Portal closes under its actual ending rules; Demiplane loses its door only. A mere past arrival, summoned body, identity/native relationship, Maze/exile confinement with no live channel, Gloom’s local exit restriction, same-plane telepathy, soul claim or realm itself is not a connection. Unknown cross-plane telepathy/tether eligibility stays held until the exact source establishes its live endpoints; no universal telepathy rewrite.
- **R8PL-SEAL-DURATION** — option 1: One-time atomic closure of qualifying existing connections; later independent opening remains possible. One-time atomic closure at resolution. No concentration, ongoing prohibition, continuing dispellable seal, future-target detector or new plane. Later independently legal paid opening can succeed. Persisting bodies, cargo, rooms, independent effects and clocks remain. A specific source immunity/end consequence is honored where proved; no invented rank-check, universal dispel or unsummoning is added.
- **R8PL-SEAL-TRANSIT** — option 1: Finish committed atomic crossings, then close later use; explicitly adjudicate true interruption sources and mandatory endings. An already committed crossing finishes atomically before closure. Ordinary Ready releases after the completed trigger and therefore cannot cut a traveler in half. A true interrupt needs its own proved source and exact timing; absent one, no interrupt is invented. Mandatory terminal Banishment returns and the explicitly scoped P5-CLOSE transitions are settlement events, not continuing open connections, and are not stopped by Planar Seal. The new closure does not reopen or amend those older interfaces. Resolve qualifying edges in stable connection-ID order for bookkeeping; no order grants extra actions or half transfers.

### Cases and retained holds

P5-SEAL-A, P5-SEAL-B, P5-SEAL-A/unknown-tether, P5-SEAL-A/boundary-touch, P5-SEAL-A/outside-boundary

P5-H-SOURCE, P5-H-ACCESS, P5-H-COSMOLOGY, P5-H-CONTENT, P5-H-PHYSICAL, P5-H-EQUIPMENT, P5-H-LIFECYCLE, P5-H-INFORMATION, P5-H-TETHER, P5-H-RUNTIME, P5-H-HUMAN-PLAY, P5-H-BALANCE, P5-H-RELEASE

## seal-of-banishment

### Exact native card and all access rows

```json
{
  "id": "seal-of-banishment",
  "name": "Seal of Banishment",
  "schools": [
    "Divination"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Divination",
      "baseRpCost": 21
    },
    "Wizard": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Divination",
      "baseRpCost": 21
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "seal-of-banishment",
    "original": {
      "name": "Seal of Banishment",
      "level": 8,
      "resonanceRank": 8,
      "school": "Divination",
      "schools": [
        "Divination"
      ],
      "placements": [
        {
          "name": "Seal of Banishment",
          "school": "Divination",
          "level": 8,
          "summary": "Banish up to 3 extraplanar creatures (CHA save resists)."
        }
      ],
      "classLevels": {
        "Cleric": 8,
        "Wizard": 8
      },
      "classRanks": {
        "Cleric": 8,
        "Wizard": 8
      },
      "classLearnLevels": {
        "Cleric": 15,
        "Wizard": 15
      },
      "classSchools": {
        "Cleric": "Divination",
        "Wizard": "Divination"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Banish up to 3 extraplanar creatures (CHA save resists).",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 291,
        "original": {
          "school": "Divination",
          "level": 8,
          "name": "Seal of Banishment",
          "effect": "Banish up to 3 extraplanar creatures (CHA save resists).",
          "source_paragraph": 9340,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Charisma save",
          "tags": [
            "Planar"
          ],
          "rp_cost": 21
        }
      }
    ],
    "possibleHistoricalAliases": []
  },
  "reviewFlags": [
    "Not selectable in this spell playtest packet until individual operational review"
  ]
}
```

### authority

NEW authored Planar5 procedures only. Exact input authority is 730 applied-reviewed / 118 pending / 0 accepted-unapplied, 454 standalone procedures. Conference01 525/323 labels are historical. Recorded accepted interfaces are preserved in ACCEPTED_INTERFACES.json; their exact recovered source bytes, not later edited comparisons, control. No canonical index/catalog or closed cohort is changed.

### native

Each native card, Core entry, book placement and class-access row is copied unchanged below. All five are rank 8, Action, range 120 ft, V/S/F, base 21 RP, minimum actual class level 15. Demiplane has two book placements but its actual grants remain Conjuration. Maze uses Wizard Illusion versus Cleric/Mage Universal. Do not create access from a school heading. Original Instantaneous fields remain evidence even where a NEW ongoing component is selected. Gloom Bind retains Core Until dispelled and both conflicting destination names.

### preflight

Use an actually acquired and prepared matrix or an exact class permission. Check remaining Action, usable voice, free gesturing hand and actual focus, rank/RP, target identity, actual range and unobstructed line of effect. A known invalid declaration is rejected before payment. Missing authoritative physical/source prerequisites put the dependent case on hold; a held test is not a successful or paid cast. A lawful declaration defeated only by hidden facts spends its committed costs and produces no diagnostic locating or classifying the hidden fact. Revalidate each component at effect resolution. No retargeting or refund on failure.

### commit

Commit RP, components, source-history and concentration before interruption/save. Cost is 21 plus the exact pre-cast Dissonance surcharge and printed extras only. Limit=max(4,2+PB+max(0,casting modifier)); +1 at limit, +2 at limit+3, ordinary ranked casting blocked at limit+6. First distinct actual Wizard prepared family gives zero BASE strain only; otherwise rank8 base strain is 2. Consecutive same-family Refrain adds 1/2/3 capped at3, idle turns do not reset it. No class perk is assumed without acquisition. An interrupted or resisted cast retains costs and never restores displaced concentration. Exact legal Counterspell/Dispel sources keep their own ranks/costs/checks; Wizard Arch Dispel is rank3/3RP/check INT+PB versus18 for rank8, not rank5 Greater Dispel.

### timing

Use actual elapsed seconds; generated spaces have 1:1 time. An expiry at timestamp t occurs before a newly beginning action at t; already committed atomic crossings finish before an external closure event can settle them. Ordinary Ready commits at preparation, uses held concentration, releases once with a remaining Reaction after its completed trigger, and expires at the next own regular START. Release does not pay/cast/update cadence again; effect deadlines begin on release. A continuing effect retains concentration normally after release. No extra regular START, recharge, rest, recovery, Refrain reset, Hunt pause or resource refresh is created by moving planes.

### transport

Creation of a room/cell is not itself body travel. Door creation is a connection; its use is physical planar crossing. Maze, Seal of Banishment and Gloom Bind admissions are planar displacement, not teleportation. Record ACCEPT versus RESIST separately from save result. Voluntary or forced travel restrictions use their exact predicates, not a generic planar tag. Every creature is separate from gear, including carried unconscious allies, mounts and summons. Check whole-body geometry and actual custody for each. No splitting, duplicating inventories, body-as-cargo target-cap bypass or unprovided portal provider. Record current plane, actual travel provenance, origin anchor and source-character identity separately from native realm, which may remain unknown.

### hardControl

Maze, each Seal of Banishment child and Gloom Bind count as encounter-removal/hard denial and require the shared source-character/target/encounter gate across all that source character’s spells, classes and companions. Spend the gate only on actual establishment, not a resisted or preflight-rejected cast. Prior expenditure or a proved immunity prevents only the applicable control; no new target or refund. No nesting or refresh bypass. Record actual save ability, bonus, DC, die and any chosen lawful reaction/reroll; no generic monster save profile is invented.

### closureExtension

NEW P5-CLOSE extension applies ONLY to true Demiplane room removal, Maze termination and Seal of Banishment child termination. It explicitly reuses BAN-CLOSE-03, BAN-PLACEMENT-HANDOFF-03 and BAN-CONFLICT-04: end the source first, settle every extant identity exactly once to its fixed origin plane/anchor (secondary occupants project their local offset onto the recorded entry/creation anchor), ignore ONLY transport-prevention at the terminal endpoints. Try full body at anchor, legal squeeze, then nearest legal adjacent placement in the same unobstructed region, minimum displacement/greatest overlap/fixed neutral order (south, west, east, north, then SW, SE, NW, NE on the declared grid). Never pass a wall/occupied space or search farther. If none fits, retain a logical-anchor placementConflict with no fabricated footprint, support, falling, movement or new actions; independently legal actions and clocks continue. Normalize only when obstruction is actually removed or lawful relocation resolves it. Loose items retain pending placement/custody, never disappear. Source has ended even while conflict remains. This exception does not permit voluntary entry, internal escape, new portal crossings or Gloom release and does not broaden the pre-existing BAN interfaces.

### custody

Every item has one stable identity, provenance, current holder or ground location, weight, Load and independent deadline. Living bodies, corpses and source-ended absent entities are distinct. Mandatory anatomy/source endings happen first; never delay an expiry to preserve a convenient shape or manufacture a corpse. A generated space supplies only expressly authored floor/boundaries/light/respiration support; no harvestable matter, permanent supplies, inhabitants, treasure, immunity, protected rest, native status, soul rule or automatic Extraction. Preserve cargo danger, taint, claims and Hunt records. Once initiated, Hunt death is normally final except the owner’s extremely rare Divine/Abyssal exception; none of these spells grants that exception.

### qualification

Static proposed authorship and data-only fixtures are not game execution or observed campaign results. Real actor acquisition, creature profiles, destination geometry, native/cosmology facts, environmental needs and equipment not established by a source remain explicit whole-case/branch holds. No runtime, human-play, balance, cosmology or release approval. All closed feat335, completed16/72 and applied spell cohorts remain closed.

### predicate

NEW P5-EXTRAPLANAR applies only to this spell: affirmatively qualifies an actual creature with an explicit operative extraplanar source flag, or a recorded most recent successful cross-plane body arrival from a different plane into its current plane. A source-created body also qualifies only if that source explicitly proves foreign-planar provenance. This operational travel predicate may include a returning traveler; it is not proof of native origin or a global definition of outsider. Mere summoned/Fiend/Elemental/plane-themed status is insufficient. Unknown qualification is retained, not resolved to native. A publicly known ineligible target is invalid before payment; a lawfully declared target with hidden unproved qualification gets no effect and no diagnostic. A missing authoritative basis in a proposed positive campaign case is a whole dependent-case hold.

### targets

Select one to three distinct perceived creatures within120ft/line of effect in a fixed declared order. Pay one cast once; each eligible target independently makes the printed CHA save with actual bonuses against the actual class-school DC. ACCEPT/RESIST, immunity, hard-control history, fit and carried separate-creature handling are separate per target. A resisted, unqualified, unavailable or immune component does not substitute another target, refund the cast or undo successful siblings. No child without successful admission; no child refresh on a target already under this spell.

### cells

NEW concentration and a60-second parent deadline from resolution; each successful target owns an independent generated BAN-CELL-03 cell, expressly extending its finite body+clearance topology/support/agency and BAN-ADMIT-03 only to these children. A Medium5x5x6 body gets15x15x15ft; retain exact dimension rules for other actual profiles. No native/home/afterlife destination. Copy actual origin plane/anchor, custody, travel-intent and source identity, not a guessed origin world. Parent concentration begins at commitment, even if no child succeeds; if none succeeds it ends immediately after resolution.

### endings

Each child ends independently on actual application suppression, a successful perceived-effect dispel, primary death/source expiry or actual lawful primary departure. P5-CLOSE settles extant secondaries/items without recreating an ended body. Parent concentration loss or common absolute deadline closes all remaining children once. Last child ended closes parent concentration. A distant suppressed caster does not automatically erase cells. Cell admission/mandatory anatomy follows the exact copied BAN contract: mandatory body event first, expand only indispensable clearance; independent visitors require actual source/fit before any expansion. This is a NEW explicit extension for Seal of Banishment; no general cell power or new cosmology is granted.

### Question selections

- **R8PL-SOURCE** — option 1: Retain originals, exact owner corrections and separately scoped accepted mechanics; leave unproved realm identities open. NEW authored Planar5 procedures only. Exact input authority is 730 applied-reviewed / 118 pending / 0 accepted-unapplied, 454 standalone procedures. Conference01 525/323 labels are historical. Recorded accepted interfaces are preserved in ACCEPTED_INTERFACES.json; their exact recovered source bytes, not later edited comparisons, control. No canonical index/catalog or closed cohort is changed.
- **R8PL-TRANSACTIONS** — option 1: Classify each spell operation explicitly: creation, portal connection, physical crossing, planar displacement, tether and mandatory ending. Creation of a room/cell is not itself body travel. Door creation is a connection; its use is physical planar crossing. Maze, Seal of Banishment and Gloom Bind admissions are planar displacement, not teleportation. Record ACCEPT versus RESIST separately from save result. Voluntary or forced travel restrictions use their exact predicates, not a generic planar tag. Every creature is separate from gear, including carried unconscious allies, mounts and summons. Check whole-body geometry and actual custody for each. No splitting, duplicating inventories, body-as-cargo target-cap bypass or unprovided portal provider. Record current plane, actual travel provenance, origin anchor and source-character identity separately from native realm, which may remain unknown.
- **R8PL-CLOCKS** — option 1: Keep actual elapsed deadlines and existing source clocks; label any different spell-local clock as a separately reviewed exception. Use actual elapsed seconds; generated spaces have 1:1 time. An expiry at timestamp t occurs before a newly beginning action at t; already committed atomic crossings finish before an external closure event can settle them. Ordinary Ready commits at preparation, uses held concentration, releases once with a remaining Reaction after its completed trigger, and expires at the next own regular START. Release does not pay/cast/update cadence again; effect deadlines begin on release. A continuing effect retains concentration normally after release. No extra regular START, recharge, rest, recovery, Refrain reset, Hunt pause or resource refresh is created by moving planes.
- **R8PL-BANISH-PREDICATE** — option 1: Explicitly select a source-local extraplanar predicate and preserve missing/hidden qualification behavior. NEW P5-EXTRAPLANAR applies only to this spell: affirmatively qualifies an actual creature with an explicit operative extraplanar source flag, or a recorded most recent successful cross-plane body arrival from a different plane into its current plane. A source-created body also qualifies only if that source explicitly proves foreign-planar provenance. This operational travel predicate may include a returning traveler; it is not proof of native origin or a global definition of outsider. Mere summoned/Fiend/Elemental/plane-themed status is insufficient. Unknown qualification is retained, not resolved to native. A publicly known ineligible target is invalid before payment; a lawfully declared target with hidden unproved qualification gets no effect and no diagnostic. A missing authoritative basis in a proposed positive campaign case is a whole dependent-case hold.
- **R8PL-BANISH-DESTINATION** — option 1: Explicitly extend the bounded exile-cell contract with a selected duration and three independent records. NEW concentration and a60-second parent deadline from resolution; each successful target owns an independent generated BAN-CELL-03 cell, expressly extending its finite body+clearance topology/support/agency and BAN-ADMIT-03 only to these children. A Medium5x5x6 body gets15x15x15ft; retain exact dimension rules for other actual profiles. No native/home/afterlife destination. Copy actual origin plane/anchor, custody, travel-intent and source identity, not a guessed origin world. Parent concentration begins at commitment, even if no child succeeds; if none succeeds it ends immediately after resolution.
- **R8PL-BANISH-MULTI** — option 1: Resolve independent named targets in stable order after one paid cast, preserving each lawful successful/failed result. Select one to three distinct perceived creatures within120ft/line of effect in a fixed declared order. Pay one cast once; each eligible target independently makes the printed CHA save with actual bonuses against the actual class-school DC. ACCEPT/RESIST, immunity, hard-control history, fit and carried separate-creature handling are separate per target. A resisted, unqualified, unavailable or immune component does not substitute another target, refund the cast or undo successful siblings. No child without successful admission; no child refresh on a target already under this spell. Each child ends independently on actual application suppression, a successful perceived-effect dispel, primary death/source expiry or actual lawful primary departure. P5-CLOSE settles extant secondaries/items without recreating an ended body. Parent concentration loss or common absolute deadline closes all remaining children once. Last child ended closes parent concentration. A distant suppressed caster does not automatically erase cells. Cell admission/mandatory anatomy follows the exact copied BAN contract: mandatory body event first, expand only indispensable clearance; independent visitors require actual source/fit before any expansion. This is a NEW explicit extension for Seal of Banishment; no general cell power or new cosmology is granted.

### Cases and retained holds

P5-BANISH-A, P5-BANISH-B, P5-BANISH-A/shared-hard-child

P5-H-SOURCE, P5-H-ACCESS, P5-H-COSMOLOGY, P5-H-CONTENT, P5-H-PHYSICAL, P5-H-EQUIPMENT, P5-H-LIFECYCLE, P5-H-INFORMATION, P5-H-VISITOR, P5-H-RUNTIME, P5-H-HUMAN-PLAY, P5-H-BALANCE, P5-H-RELEASE

## gloom-bind

### Exact native card and all access rows

```json
{
  "id": "gloom-bind",
  "name": "Gloom Bind",
  "schools": [
    "Necromancy"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Necromancy",
      "baseRpCost": 21
    },
    "Druid": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Necromancy",
      "baseRpCost": 21
    },
    "Wizard": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Necromancy",
      "baseRpCost": 21
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "gloom-bind",
    "original": {
      "name": "Gloom Bind",
      "level": 8,
      "resonanceRank": 8,
      "school": "Necromancy",
      "schools": [
        "Necromancy"
      ],
      "placements": [
        {
          "name": "Gloom Bind",
          "school": "Necromancy",
          "level": 8,
          "summary": "Target permanently bound to the Veiled Expanse unless freed."
        }
      ],
      "classLevels": {
        "Cleric": 8,
        "Druid": 8,
        "Wizard": 8
      },
      "classRanks": {
        "Cleric": 8,
        "Druid": 8,
        "Wizard": 8
      },
      "classLearnLevels": {
        "Cleric": 15,
        "Druid": 15,
        "Wizard": 15
      },
      "classSchools": {
        "Cleric": "Necromancy",
        "Druid": "Necromancy",
        "Wizard": "Necromancy"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Target permanently bound to the Veiled Expanse unless freed.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 711,
        "original": {
          "school": "Necromancy",
          "level": 8,
          "name": "Gloom Bind",
          "effect": "Target permanently bound to the Shadowfell unless freed.",
          "source_paragraph": 9860,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "Until dispelled",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Utility"
          ],
          "rp_cost": 21
        }
      }
    ],
    "possibleHistoricalAliases": []
  },
  "reviewFlags": [
    "Core resolution requires an explicit operational interpretation",
    "Not selectable in this spell playtest packet until individual operational review"
  ]
}
```

### authority

NEW authored Planar5 procedures only. Exact input authority is 730 applied-reviewed / 118 pending / 0 accepted-unapplied, 454 standalone procedures. Conference01 525/323 labels are historical. Recorded accepted interfaces are preserved in ACCEPTED_INTERFACES.json; their exact recovered source bytes, not later edited comparisons, control. No canonical index/catalog or closed cohort is changed.

### native

Each native card, Core entry, book placement and class-access row is copied unchanged below. All five are rank 8, Action, range 120 ft, V/S/F, base 21 RP, minimum actual class level 15. Demiplane has two book placements but its actual grants remain Conjuration. Maze uses Wizard Illusion versus Cleric/Mage Universal. Do not create access from a school heading. Original Instantaneous fields remain evidence even where a NEW ongoing component is selected. Gloom Bind retains Core Until dispelled and both conflicting destination names.

### preflight

Use an actually acquired and prepared matrix or an exact class permission. Check remaining Action, usable voice, free gesturing hand and actual focus, rank/RP, target identity, actual range and unobstructed line of effect. A known invalid declaration is rejected before payment. Missing authoritative physical/source prerequisites put the dependent case on hold; a held test is not a successful or paid cast. A lawful declaration defeated only by hidden facts spends its committed costs and produces no diagnostic locating or classifying the hidden fact. Revalidate each component at effect resolution. No retargeting or refund on failure.

### commit

Commit RP, components, source-history and concentration before interruption/save. Cost is 21 plus the exact pre-cast Dissonance surcharge and printed extras only. Limit=max(4,2+PB+max(0,casting modifier)); +1 at limit, +2 at limit+3, ordinary ranked casting blocked at limit+6. First distinct actual Wizard prepared family gives zero BASE strain only; otherwise rank8 base strain is 2. Consecutive same-family Refrain adds 1/2/3 capped at3, idle turns do not reset it. No class perk is assumed without acquisition. An interrupted or resisted cast retains costs and never restores displaced concentration. Exact legal Counterspell/Dispel sources keep their own ranks/costs/checks; Wizard Arch Dispel is rank3/3RP/check INT+PB versus18 for rank8, not rank5 Greater Dispel.

### timing

Use actual elapsed seconds; generated spaces have 1:1 time. An expiry at timestamp t occurs before a newly beginning action at t; already committed atomic crossings finish before an external closure event can settle them. Ordinary Ready commits at preparation, uses held concentration, releases once with a remaining Reaction after its completed trigger, and expires at the next own regular START. Release does not pay/cast/update cadence again; effect deadlines begin on release. A continuing effect retains concentration normally after release. No extra regular START, recharge, rest, recovery, Refrain reset, Hunt pause or resource refresh is created by moving planes.

### transport

Creation of a room/cell is not itself body travel. Door creation is a connection; its use is physical planar crossing. Maze, Seal of Banishment and Gloom Bind admissions are planar displacement, not teleportation. Record ACCEPT versus RESIST separately from save result. Voluntary or forced travel restrictions use their exact predicates, not a generic planar tag. Every creature is separate from gear, including carried unconscious allies, mounts and summons. Check whole-body geometry and actual custody for each. No splitting, duplicating inventories, body-as-cargo target-cap bypass or unprovided portal provider. Record current plane, actual travel provenance, origin anchor and source-character identity separately from native realm, which may remain unknown.

### hardControl

Maze, each Seal of Banishment child and Gloom Bind count as encounter-removal/hard denial and require the shared source-character/target/encounter gate across all that source character’s spells, classes and companions. Spend the gate only on actual establishment, not a resisted or preflight-rejected cast. Prior expenditure or a proved immunity prevents only the applicable control; no new target or refund. No nesting or refresh bypass. Record actual save ability, bonus, DC, die and any chosen lawful reaction/reroll; no generic monster save profile is invented.

### closureExtension

NEW P5-CLOSE extension applies ONLY to true Demiplane room removal, Maze termination and Seal of Banishment child termination. It explicitly reuses BAN-CLOSE-03, BAN-PLACEMENT-HANDOFF-03 and BAN-CONFLICT-04: end the source first, settle every extant identity exactly once to its fixed origin plane/anchor (secondary occupants project their local offset onto the recorded entry/creation anchor), ignore ONLY transport-prevention at the terminal endpoints. Try full body at anchor, legal squeeze, then nearest legal adjacent placement in the same unobstructed region, minimum displacement/greatest overlap/fixed neutral order (south, west, east, north, then SW, SE, NW, NE on the declared grid). Never pass a wall/occupied space or search farther. If none fits, retain a logical-anchor placementConflict with no fabricated footprint, support, falling, movement or new actions; independently legal actions and clocks continue. Normalize only when obstruction is actually removed or lawful relocation resolves it. Loose items retain pending placement/custody, never disappear. Source has ended even while conflict remains. This exception does not permit voluntary entry, internal escape, new portal crossings or Gloom release and does not broaden the pre-existing BAN interfaces.

### custody

Every item has one stable identity, provenance, current holder or ground location, weight, Load and independent deadline. Living bodies, corpses and source-ended absent entities are distinct. Mandatory anatomy/source endings happen first; never delay an expiry to preserve a convenient shape or manufacture a corpse. A generated space supplies only expressly authored floor/boundaries/light/respiration support; no harvestable matter, permanent supplies, inhabitants, treasure, immunity, protected rest, native status, soul rule or automatic Extraction. Preserve cargo danger, taint, claims and Hunt records. Once initiated, Hunt death is normally final except the owner’s extremely rare Divine/Abyssal exception; none of these spells grants that exception.

### qualification

Static proposed authorship and data-only fixtures are not game execution or observed campaign results. Real actor acquisition, creature profiles, destination geometry, native/cosmology facts, environmental needs and equipment not established by a source remain explicit whole-case/branch holds. No runtime, human-play, balance, cosmology or release approval. All closed feat335, completed16/72 and applied spell cohorts remain closed.

### sourceChoice

NEW spell-local reconciliation selects the current Rulebook/catalog label Veiled Expanse for this spell. Core Shadowfell text and Until dispelled remain verbatim evidence. This does not establish Shadowfell=Veiled Expanse, rename either globally or supply a map. The actual destination needs a separately established plane identity and precise arrival-site receipt with geometry/support/environment; original atmospheric prose supplies none. Both positive destination-dependent main cases remain whole-case held in this return.

### binding

NEW: one perceived actual creature within120ft/line of effect; initial CHA save at actual class-school DC, ACCEPT may elect failure, RESIST rolls, shared hard gate on establishment. Require a proved legal Veiled destination before a positive relocation fixture. Actual admission is immediate planar displacement of the body and legal gear followed by a persistent rank8 body-attached restriction on leaving that established plane; not teleport, not a passive promise of later banishment. Pass actual endpoint blockers, source identity, custody and full fit. Known invalid site fails preflight; hidden obstruction after a lawful sourced declaration spends the cast and establishes neither partial body nor binding. One binding per body, no absent-target/recast refresh or fabricated target knowledge.

### permanence

No concentration and no short timer: bound until a genuine release, body death or finite body-source ending. Caster death does not free it. The restriction blocks attempts to leave the plane, including independent portal/teleport routes whose predicates would otherwise permit departure; it does not stop local movement or erase the destination’s actual laws. Remain subject to real breathing, support, damage, source expiries and elapsed clocks. No blanket realm survival hazard or immunity is authored from poetic imagery.

### release

NEW: a successful actual dispel of the perceived rank8 binding ends it (e.g. acquired Wizard Arch Dispel rank3/3RP, Action,60ft, recharge2, INT+PB vs18). No generic restoration is a release without its exact source. NEW original caster may release with an Action only while perceiving the bound body within120ft and line of effect; no RP/new cast/procs, no remote release by mere name. NEW actual suppression of the binding itself is a freeing event ending it permanently, not a paused application or snapback; distant caster suppression alone does nothing. Freeing lifts the restriction ONLY, with no automatic return or tactical placement. Actual independent travel is still required. P5-CLOSE does not apply to Gloom.

### death

Actual body death ends this creature-only binding; corpse and dropped possessions remain at their genuine destination, with no resurrection, soul relocation, native inference or extra Hunt exception. A finite summoned/body source ending ends that body first and produces only its source-authorized remains, never a reusable corpse/loot. Independently extant gear/companions retain actual custody and location. Any rescue, source-specific mandatory return or resurrection requires its own complete source and actual prerequisites; unresolved priority conflicts stay held, never silently rewrite Hunt.

### Question selections

- **R8PL-SOURCE** — option 1: Retain originals, exact owner corrections and separately scoped accepted mechanics; leave unproved realm identities open. NEW authored Planar5 procedures only. Exact input authority is 730 applied-reviewed / 118 pending / 0 accepted-unapplied, 454 standalone procedures. Conference01 525/323 labels are historical. Recorded accepted interfaces are preserved in ACCEPTED_INTERFACES.json; their exact recovered source bytes, not later edited comparisons, control. No canonical index/catalog or closed cohort is changed.
- **R8PL-TRANSACTIONS** — option 1: Classify each spell operation explicitly: creation, portal connection, physical crossing, planar displacement, tether and mandatory ending. Creation of a room/cell is not itself body travel. Door creation is a connection; its use is physical planar crossing. Maze, Seal of Banishment and Gloom Bind admissions are planar displacement, not teleportation. Record ACCEPT versus RESIST separately from save result. Voluntary or forced travel restrictions use their exact predicates, not a generic planar tag. Every creature is separate from gear, including carried unconscious allies, mounts and summons. Check whole-body geometry and actual custody for each. No splitting, duplicating inventories, body-as-cargo target-cap bypass or unprovided portal provider. Record current plane, actual travel provenance, origin anchor and source-character identity separately from native realm, which may remain unknown.
- **R8PL-CLOCKS** — option 1: Keep actual elapsed deadlines and existing source clocks; label any different spell-local clock as a separately reviewed exception. Use actual elapsed seconds; generated spaces have 1:1 time. An expiry at timestamp t occurs before a newly beginning action at t; already committed atomic crossings finish before an external closure event can settle them. Ordinary Ready commits at preparation, uses held concentration, releases once with a remaining Reaction after its completed trigger, and expires at the next own regular START. Release does not pay/cast/update cadence again; effect deadlines begin on release. A continuing effect retains concentration normally after release. No extra regular START, recharge, rest, recovery, Refrain reset, Hunt pause or resource refresh is created by moving planes.
- **R8PL-GLOOM-NAME** — option 1: Use Veiled Expanse as the spell’s explicit authored destination label while preserving the Core conflict; do not equate realms globally. NEW spell-local reconciliation selects the current Rulebook/catalog label Veiled Expanse for this spell. Core Shadowfell text and Until dispelled remain verbatim evidence. This does not establish Shadowfell=Veiled Expanse, rename either globally or supply a map. The actual destination needs a separately established plane identity and precise arrival-site receipt with geometry/support/environment; original atmospheric prose supplies none. Both positive destination-dependent main cases remain whole-case held in this return.
- **R8PL-GLOOM-BINDING** — option 1: Choose explicit planar relocation plus a persistent escape restriction with full arrival rules. NEW: one perceived actual creature within120ft/line of effect; initial CHA save at actual class-school DC, ACCEPT may elect failure, RESIST rolls, shared hard gate on establishment. Require a proved legal Veiled destination before a positive relocation fixture. Actual admission is immediate planar displacement of the body and legal gear followed by a persistent rank8 body-attached restriction on leaving that established plane; not teleport, not a passive promise of later banishment. Pass actual endpoint blockers, source identity, custody and full fit. Known invalid site fails preflight; hidden obstruction after a lawful sourced declaration spends the cast and establishes neither partial body nor binding. One binding per body, no absent-target/recast refresh or fabricated target knowledge.
- **R8PL-GLOOM-RELEASE** — option 1: Define eligible actual dispel/release predicates, suppression behavior and whether release returns the body or only lifts the restriction. NEW: a successful actual dispel of the perceived rank8 binding ends it (e.g. acquired Wizard Arch Dispel rank3/3RP, Action,60ft, recharge2, INT+PB vs18). No generic restoration is a release without its exact source. NEW original caster may release with an Action only while perceiving the bound body within120ft and line of effect; no RP/new cast/procs, no remote release by mere name. NEW actual suppression of the binding itself is a freeing event ending it permanently, not a paused application or snapback; distant caster suppression alone does nothing. Freeing lifts the restriction ONLY, with no automatic return or tactical placement. Actual independent travel is still required. P5-CLOSE does not apply to Gloom. No concentration and no short timer: bound until a genuine release, body death or finite body-source ending. Caster death does not free it. The restriction blocks attempts to leave the plane, including independent portal/teleport routes whose predicates would otherwise permit departure; it does not stop local movement or erase the destination’s actual laws. Remain subject to real breathing, support, damage, source expiries and elapsed clocks. No blanket realm survival hazard or immunity is authored from poetic imagery.
- **R8PL-GLOOM-DEATH** — option 1: Keep the actual living/dead body, source lifetime and independent Hunt/recovery rules; no soul relocation is inferred. Actual body death ends this creature-only binding; corpse and dropped possessions remain at their genuine destination, with no resurrection, soul relocation, native inference or extra Hunt exception. A finite summoned/body source ending ends that body first and produces only its source-authorized remains, never a reusable corpse/loot. Independently extant gear/companions retain actual custody and location. Any rescue, source-specific mandatory return or resurrection requires its own complete source and actual prerequisites; unresolved priority conflicts stay held, never silently rewrite Hunt.

### Cases and retained holds

P5-GLOOM-A, P5-GLOOM-B, P5-GLOOM-A/corpse-source-expiry, P5-GLOOM-B/actual-freeing

P5-H-SOURCE, P5-H-ACCESS, P5-H-COSMOLOGY, P5-H-CONTENT, P5-H-PHYSICAL, P5-H-EQUIPMENT, P5-H-LIFECYCLE, P5-H-INFORMATION, P5-H-GLOOM-NAME, P5-H-GLOOM-SITE, P5-H-RUNTIME, P5-H-HUMAN-PLAY, P5-H-BALANCE, P5-H-RELEASE
