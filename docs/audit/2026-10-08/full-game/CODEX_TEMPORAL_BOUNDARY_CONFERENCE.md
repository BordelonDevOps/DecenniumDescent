# Time Loop: concrete reconciliation before implementation

Your completed first world-transaction conference is preserved as GPT_TEMPORAL_WORLD_FIRST_REVIEW.md. I agree it is SOURCE-DISCUSSED / DRAFTABLE, not implemented. The attached structural inventory reads70 actual state-holder classes across10 existing reference modules; it does not authorize copying any field. The seven attached geometry passages were verified against unchanged original DOCX bytes, using zero-based XML paragraph indices including tables.

The owner has additionally authorized a final whole-game flow review with you, then a push to BordelonDevOps/DecenniumDescent only once we both confirm the full authored game flows correctly. This remains a final gate; our individual package closures do not satisfy it. No push yet.

Please resolve these12 concrete boundaries. We need explicit choices, not a generic completeSnapshot boolean.

1. **Reward identity counterexample.** Unique fresh event IDs alone do not prevent duplicate XP/treasure: kill the same snapshot foe, collect reward, rewind, kill again under a fresh iteration/event ID. Soul Charges already have conserved owner/body/LR history. Please specify the conserved reward-opportunity identity for XP/loot/harvest entitlements (e.g. original encounter+immutable reward source/opportunity, not deathEventId) and distinguish a genuinely new independent reward. No blanket reward amount is requested.

2. **Restored one-shot effects versus historical consumption.** Agony can exist at snapshot, be consumed by healing, then restore with the SAME effect ID. HealingCommitLedger currently has persistent `committed_event_ids` and `consumed_reducer_ids` keyed only by application ID. Blindly preserving the latter rejects the restored record; blindly deleting history erases audit evidence. Same issue applies to restored form/grant/mark rider state. Proposed: conserve historical events/application identity forever, but store one-shot consumption against (effectId,timelineIteration) / restore the active effect's snapshot consumed state into a new iteration view. This is a privileged restoration, never a new offer/cast/entry. Confirm exact eligibility/state rule, including an already-consumed record at snapshot.

3. **All outstanding Reaction debts.** A loops, B loops before A reaches its legitimate Reaction refresh. Restoring the snapshot and overlaying only B's spent Reaction would refund A's. Proposed: preserve every outstanding TimeLoopReactionDebt across loops, clear an owner's debt only at its actual normal regular-start Reaction refresh, overlay all remaining debts. A debt already legitimately cleared stays cleared through later loops. Verify this matches the earlier class combat scheduler.

4. **Logical turns versus world-time phase.** Existing helpers use numbered rounds/regular markers and the frozen six-second outside-initiative phase; extra turns never refresh a round. Time Loop restarts encounter labels but global elapsed seconds continue. Do the new iteration's round/regular-turn IDs count as fresh actual logical windows for once-per-turn/round feats, while old event IDs and finite reserves remain conserved? For example Empowered Summoning PB once/round, Necrotic Affinity1d6/turn, Lifeleech same original spellRoot across a new iteration, command budgets and actual regular-start Druid recharge. Give explicit iteration-qualified identity and phase-rebase rules; do not accidentally require six extra world seconds before restored round1 is playable or grant additional periodic ticks at the rewind instant.

5. **Concrete clock-policy table.** Please explicitly classify these source-qualified fields: pending living Soul Bind60s; bound dead Soul Bind24h; Necrotic Affinity24h seal; Agony60s; Chef food24h-or-owner-nextLR; Chef/Inspiration recipient-family LR entitlements; Blood self default-LR shield + next-LR save rider; Blood ally1h shield; Field Medic/Empowered/Soul Cage default-LR shield; Core Stable1d4h recovery deadline; ordinary Druid form60s and its dependent shield; transformation five-spell records (already proposed); per-rest resource resets. For a world-absolute expired record, can restoring its containing life/condition state immediately retrigger already-resolved recovery, or must consumed world-event history prevent that replay? Do not infer class solely from numerical duration. A newly introduced unsupported source can still make a specific snapshot unavailable until it has a reviewed policy.

6. **Changed maximum HP/current inventory.** Snapshot maximum/currentHP can depend on equipment that was subsequently destroyed/transferred and must stay absent. Restoring stale maximumHP would retain a benefit of missing gear. Proposed: restore snapshot life/Wounds and rewindable modifiers, retain current conserved character/gear sources, recompute legal maximumHP with the reviewed maxHP rules, and clamp restoredHP without creating damage/healing/Wounds if the legal maximum fell. State how a higher current maximum, Critical ceiling and conserved level/ability-score changes are handled. Level/XP/feat acquisition should not silently rewind or become free duplications.

7. **Off-scene concentration and post-snapshot external effects.** Your dependency closure may contain a nonparticipant caster. Does that authorize rewinding only its recorded concentration slot, or must it be an actual full participant registered at snapshot? I propose no automatic off-scene body/HP/memory rollback from a slot dependency. Also, an unrelated nonparticipant applies a persistent effect after snapshot: wiping the target's effects would erase an external source, but retaining it can alter restored anatomy/placement. Choose a rule: preserve externally owned current records and reconcile, or make an unresolvable external dependency block preflight. Never silently end an unrelated caster's slot.

8. **Derivatives and inventory scope.** A restored corpse/wall has produced a surviving harvested item, mixed crafted item, undead or structure, possibly transferred to a nonparticipant. Specify transitive physical provenance: which surviving derivatives retire as the explicit conservation exception, which unrelated ingredients/payments remain spent, and when unknown/off-scope provenance causes preflight failure. Can a required derivative under a nonparticipant's ownership be retired without changing its unrelated body/state, or must that block? Current inventory ownership is otherwise conserved; do not silently broaden the exception into restoring arbitrary sold loot. Also verify that removing/restoring terrain cannot drop, crush, trap or otherwise force a changed physical state on an external nonparticipant merely because its occupied square is technically nonoverlapping.

9. **Persistent asset membership versus later bindings.** Ranger bond identity and current limited-use resources are conserved but snapshot Beast/body/slot state restores. What if after snapshot a different legal rebond/persistent-asset replacement changed identity? Which actual bond/elite/pet enrollment remains? A new persistent preexisting body is not a genuinely created temporal child and cannot be erased. Similar: snapshot permanent True Polymorph object creature sponsor slot later reused, Wizard-created undead/source corpse lineage, Mirror reserved slots and device deployments. Require source-aware reconciliation/preflight failure rather than double-slot restoration or overwriting a conserved asset identity.

10. **Existing gear on restored forms.** Restore snapshot meld set only as intersection with actual still-existing currently held inventory, as proposed. Current additional external gear has no snapshot meld identity: may it remain usable if compatible, and otherwise drop at the same restored anchor without a fresh entry/recapture hook? Never recreate transferred/lost items. Confirm whether impossible legal drop/placement for conserved items blocks preflight. Suppression restores snapshot state only if the actual restored environment permits it; external ongoing antimagic cannot be bypassed by copying a false suppression flag.

11. **Memory/agency precision.** The source grants allies memory. Your paragraph also says player characters retain their own experience. In a rare player-character enemy/PvP case, is character-level temporal memory still limited to snapshot alliance with the invoking Oracle, while real players retain ordinary table knowledge and agency? Confirm actor/Oracle-specific eligibility, own Oracle memory and cumulative memory across loops; no hidden roster/perception leakage or automatic decision replay.

12. **Authored reference scope and actual adapter work.** The companion's current `src/lib/character-storage.js` normalizes saved character fields; it is not a canonical encounter/world serializer. Existing bounded Python modules have real BufferLedger, ConcentrationLedger, TransformationWorld, CreatureWorld, Lifecycle, RemainingWorld, FeatWorld and resource ledgers (actual fields/method line references attached). I will implement a typed finite TemporalWorld/reference transaction with explicit registered participants, physical/environment provenance, current inventory, source-qualified clock policies, real shared ledger adapters and a total staged plan/atomic commit. Unknown effects/provenance cannot opt in with one unchecked boolean. This can close the authored Time Loop reference after the demonstrated source classes and counterexamples are implemented/reviewed, while the complete web companion runtime remains a separate tracked delivery. Please identify the minimum actual source-specific adapters needed to avoid falsely calling a generic opaque dictionary serializer complete. Do we need further exact class cards beyond the existing reviewed lifecycle/form/feat packages before writing those adapters? If so name them and I will supply them.

Please return12 numbered decisions and distinguish settled NEW rules from additional source evidence still required. This request does not ask you to approve unseen implementation or close the whole game.


## Exact current state-holder inventory

{
  "status": "PREPARED exact code-structure inventory; no fields approved for temporal rewind by this list",
  "scope": "Time Loop must choose restore/conserve/reconcile rules; neither AST field names nor deepcopy authorize copying",
  "files": [
    {
      "path": "tools/core_playtest_rules.py",
      "sha256": "a162117cf2c0c96a77ef5e594ce7247593930c57e6223fc7291ab12fc45c8d7d",
      "stateHolders": [
        {
          "class": "LifeState",
          "line": 48,
          "fields": {
            "maximum_hp": "int",
            "hp": "int",
            "temp_hp": "int",
            "wounds": "tuple",
            "stable": "bool",
            "dead": "bool",
            "death_successes": "int",
            "death_failures": "int",
            "uses_death_saves": "bool",
            "stable_until_seconds": "int | None",
            "last_death_turn": "int"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 62
            }
          ]
        }
      ]
    },
    {
      "path": "tools/control_playtest_rules.py",
      "sha256": "816df3eef6d1f0591de424308ccb48e0998a7b0c8a268f9d0201e971939ac263",
      "stateHolders": [
        {
          "class": "ClockMarker",
          "line": 15,
          "fields": {
            "seconds": "Fraction",
            "phase": "int"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 19
            }
          ]
        },
        {
          "class": "SpeedRecord",
          "line": 71,
          "fields": {
            "application_id": "str",
            "owner": "str",
            "target": "str",
            "group": "str",
            "profile": "str",
            "mode": "str",
            "amount": "int",
            "floor": "int",
            "expires": "ClockMarker | None",
            "active": "bool",
            "suppressed": "bool",
            "slowed_hook": "bool"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 85
            },
            {
              "name": "operative",
              "line": 98
            },
            {
              "name": "result",
              "line": 102
            }
          ]
        },
        {
          "class": "GuidingStarMark",
          "line": 180,
          "fields": {
            "owner": "str",
            "target": "str",
            "expires": "ClockMarker",
            "s": "int",
            "attack_bonus_available": "bool",
            "hit_rider_available": "bool",
            "active": "bool",
            "_identity": "str",
            "_next_token": "int",
            "_pending": "set"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 192
            },
            {
              "name": "begin_ally_attack",
              "line": 196
            },
            {
              "name": "resolve_ally_attack",
              "line": 212
            }
          ]
        },
        {
          "class": "WrathfulBrand",
          "line": 226,
          "fields": {
            "owner": "str",
            "target": "str",
            "expires": "ClockMarker",
            "owner_rider_available": "bool",
            "ally_rider_available": "bool",
            "active": "bool"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 234
            },
            {
              "name": "trigger",
              "line": 237
            }
          ]
        },
        {
          "class": "OneShotRider",
          "line": 254,
          "fields": {
            "trigger_kind": "str",
            "available": "bool"
          },
          "methods": [
            {
              "name": "trigger",
              "line": 258
            }
          ]
        },
        {
          "class": "PerTurnReflection",
          "line": 270,
          "fields": {
            "cleric_level": "int",
            "used_turn_ids": "set"
          },
          "methods": [
            {
              "name": "reflect",
              "line": 274
            }
          ]
        }
      ]
    },
    {
      "path": "tools/healing_playtest_rules.py",
      "sha256": "651cf7191b8619377b236a33470d5461fc92288f173308a5daae96331a8f7320",
      "stateHolders": [
        {
          "class": "HealingReduction",
          "line": 17,
          "fields": {
            "application_id": "str",
            "group": "str",
            "kind": "str",
            "value": "int | Fraction",
            "present": "bool",
            "suppressed": "bool",
            "next_healing": "bool"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 26
            }
          ]
        },
        {
          "class": "SoulBind",
          "line": 116,
          "fields": {
            "identity": "str",
            "stage": "str",
            "expires": "Fraction"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 121
            }
          ]
        },
        {
          "class": "ExhaustionState",
          "line": 403,
          "fields": {
            "level": "int",
            "lethal_collapse": "bool"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 407
            }
          ]
        },
        {
          "class": "RevivalHistory",
          "line": 442,
          "fields": {
            "thousand_petals": "set",
            "grace_reversal": "set"
          },
          "methods": [
            {
              "name": "eligible",
              "line": 447
            },
            {
              "name": "_history",
              "line": 450
            },
            {
              "name": "record_success",
              "line": 455
            },
            {
              "name": "owner_long_rest",
              "line": 460
            }
          ]
        },
        {
          "class": "IdentityReturnLedger",
          "line": 472,
          "fields": {
            "living_identities": "set",
            "eligible_remains": "dict"
          },
          "methods": [
            {
              "name": "true_resurrection",
              "line": 477
            }
          ]
        },
        {
          "class": "HealingCommitLedger",
          "line": 494,
          "fields": {
            "committed_event_ids": "set",
            "consumed_reducer_ids": "set"
          },
          "methods": [
            {
              "name": "commit",
              "line": 498
            }
          ]
        },
        {
          "class": "ExcessLedger",
          "line": 508,
          "fields": {
            "remaining": "int",
            "forbid_temp_hp": "bool",
            "internal_resolved": "bool"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 513
            },
            {
              "name": "convert",
              "line": 515
            }
          ]
        },
        {
          "class": "HealingChain",
          "line": 550,
          "fields": {
            "root_id": "str",
            "visited": "set"
          },
          "methods": [
            {
              "name": "child",
              "line": 554
            }
          ]
        }
      ]
    },
    {
      "path": "tools/healing_pulse_playtest_rules.py",
      "sha256": "49d998839cc34e88dcbf26d7899d05a2c360fb77cb1c49d41236d5dc1002471f",
      "stateHolders": [
        {
          "class": "PulseWallet",
          "line": 13,
          "fields": {
            "rp": "int",
            "rc": "int",
            "bonus_action": "bool"
          },
          "methods": [
            {
              "name": "spend",
              "line": 17
            }
          ]
        },
        {
          "class": "RecipientLedger",
          "line": 29,
          "fields": {
            "claimed": "set"
          },
          "methods": [
            {
              "name": "check",
              "line": 31
            },
            {
              "name": "commit",
              "line": 35
            }
          ]
        },
        {
          "class": "PulseProfile",
          "line": 41,
          "fields": {
            "mode": "str",
            "count": "int",
            "initial": "bool",
            "later_cost": "int",
            "currency": "str",
            "fixed": "bool",
            "target_cap": "int",
            "round_domain": "str",
            "maintenance_bonus_action": "bool"
          },
          "methods": []
        },
        {
          "class": "PulseSeries",
          "line": 89,
          "fields": {
            "instance_id": "str",
            "profile_name": "str",
            "activation": "ClockMarker",
            "future_starts": "tuple",
            "ledger": "RecipientLedger",
            "roster": "tuple",
            "maintenance_ends": "tuple",
            "expires": "ClockMarker | None",
            "states": "list",
            "declarations": "dict",
            "applications": "set",
            "ended_at": "ClockMarker | None",
            "ended_reason": "str | None"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 106
            },
            {
              "name": "domain",
              "line": 139
            },
            {
              "name": "end",
              "line": 143
            },
            {
              "name": "advance",
              "line": 149
            },
            {
              "name": "_targets",
              "line": 177
            },
            {
              "name": "resolve",
              "line": 182
            },
            {
              "name": "fund",
              "line": 226
            },
            {
              "name": "target_start",
              "line": 241
            },
            {
              "name": "command",
              "line": 258
            }
          ]
        },
        {
          "class": "BloomReserve",
          "line": 290,
          "fields": {
            "roster_missing": "dict",
            "consumed": "set"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 293
            },
            {
              "name": "consume",
              "line": 296
            }
          ]
        },
        {
          "class": "FirstContactLedger",
          "line": 307,
          "fields": {
            "profiles": "dict",
            "consumed": "set"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 310
            },
            {
              "name": "claim",
              "line": 313
            }
          ]
        },
        {
          "class": "NativeOccurrenceLedger",
          "line": 330,
          "fields": {
            "consumed": "set"
          },
          "methods": [
            {
              "name": "commit",
              "line": 332
            }
          ]
        }
      ]
    },
    {
      "path": "tools/form_temphp_playtest_rules.py",
      "sha256": "97566962d3eddeca5966b4b58bbb3a5e53dc34d529afb5de033d4358397e2151",
      "stateHolders": [
        {
          "class": "BufferGrant",
          "line": 24,
          "fields": {
            "grant_id": "str",
            "source_id": "str",
            "owner": "str",
            "target": "str",
            "remaining": "int",
            "expiry": "ClockMarker | None",
            "rest_epoch": "int | None",
            "dependencies": "tuple",
            "riders": "set",
            "state": "str"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 37
            }
          ]
        },
        {
          "class": "BufferLedger",
          "line": 53,
          "fields": {
            "grants": "runtime state; see exact code",
            "active": "runtime state; see exact code",
            "rest_epochs": "runtime state; see exact code",
            "damage_events": "runtime state; see exact code",
            "absorptions": "runtime state; see exact code",
            "form_instances": "runtime state; see exact code",
            "spell_anatomies": "runtime state; see exact code"
          },
          "methods": [
            {
              "name": "__init__",
              "line": 60
            },
            {
              "name": "amount",
              "line": 66
            },
            {
              "name": "current",
              "line": 70
            },
            {
              "name": "validate_offer",
              "line": 74
            },
            {
              "name": "offer",
              "line": 85
            },
            {
              "name": "end",
              "line": 103
            },
            {
              "name": "expire",
              "line": 118
            },
            {
              "name": "end_dependency",
              "line": 125
            },
            {
              "name": "completed_long_rest",
              "line": 130
            },
            {
              "name": "consume_linked_reaction",
              "line": 137
            },
            {
              "name": "core_damage",
              "line": 145
            },
            {
              "name": "necrotic_affinity",
              "line": 166
            },
            {
              "name": "finish_necrotic_affinity",
              "line": 183
            }
          ]
        },
        {
          "class": "DruidStats",
          "line": 233,
          "fields": {
            "owner": "str",
            "level": "int",
            "pb": "int",
            "wisdom": "int",
            "scale": "int",
            "modifier": "int"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 241
            }
          ]
        },
        {
          "class": "FormInstance",
          "line": 248,
          "fields": {
            "instance_id": "str",
            "source_id": "str",
            "variant": "str | None",
            "expiry": "ClockMarker",
            "large": "bool",
            "spent": "set",
            "state": "str",
            "entry_open": "bool"
          },
          "methods": []
        },
        {
          "class": "OwnerRechargeClock",
          "line": 269,
          "fields": {
            "mode": "runtime state; see exact code",
            "now": "runtime state; see exact code",
            "next_tick": "runtime state; see exact code",
            "ticks": "runtime state; see exact code",
            "last_regular": "runtime state; see exact code",
            "anchored": "runtime state; see exact code"
          },
          "methods": [
            {
              "name": "__init__",
              "line": 277
            },
            {
              "name": "_time",
              "line": 281
            },
            {
              "name": "_anchor",
              "line": 285
            },
            {
              "name": "regular_start",
              "line": 289
            },
            {
              "name": "leave_initiative",
              "line": 298
            },
            {
              "name": "advance_outside",
              "line": 303
            },
            {
              "name": "enter_initiative",
              "line": 311
            },
            {
              "name": "use",
              "line": 314
            }
          ]
        },
        {
          "class": "DruidState",
          "line": 323,
          "fields": {
            "owner": "runtime state; see exact code",
            "circle": "runtime state; see exact code",
            "buffers": "runtime state; see exact code",
            "cadence": "runtime state; see exact code",
            "creatures": "runtime state; see exact code",
            "current": "runtime state; see exact code",
            "instances": "runtime state; see exact code",
            "long_epoch": "runtime state; see exact code",
            "short_epoch": "runtime state; see exact code",
            "regular_index": "runtime state; see exact code",
            "recharges": "runtime state; see exact code",
            "recharge_clock": "runtime state; see exact code",
            "rest_uses": "runtime state; see exact code",
            "attuned": "runtime state; see exact code"
          },
          "methods": [
            {
              "name": "__init__",
              "line": 331
            },
            {
              "name": "_stats",
              "line": 343
            },
            {
              "name": "_validate_attunement",
              "line": 346
            },
            {
              "name": "_refill",
              "line": 351
            },
            {
              "name": "completed_long_rest",
              "line": 356
            },
            {
              "name": "completed_short_rest",
              "line": 364
            },
            {
              "name": "regular_start",
              "line": 370
            },
            {
              "name": "_active",
              "line": 376
            },
            {
              "name": "_legal_profile",
              "line": 381
            },
            {
              "name": "shift",
              "line": 395
            },
            {
              "name": "_end",
              "line": 432
            },
            {
              "name": "revert",
              "line": 439
            },
            {
              "name": "natural_endpoint",
              "line": 444
            },
            {
              "name": "finalize_damage_state",
              "line": 453
            },
            {
              "name": "profile",
              "line": 461
            },
            {
              "name": "attack",
              "line": 480
            },
            {
              "name": "special",
              "line": 495
            },
            {
              "name": "mooncursed_howl",
              "line": 517
            }
          ]
        }
      ]
    },
    {
      "path": "tools/transformation_spell_playtest_rules.py",
      "sha256": "91697863f6d19043787e17f19b4c127e6c32de32ad3867393566212533081d39",
      "stateHolders": [
        {
          "class": "CastStats",
          "line": 27,
          "fields": {
            "owner": "str",
            "source_class": "str",
            "attack": "int",
            "dc": "int",
            "pb": "int",
            "modifier": "int"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 35
            }
          ]
        },
        {
          "class": "CastPrice",
          "line": 43,
          "fields": {
            "spell_id": "str",
            "rank": "int",
            "base_paid": "int",
            "other_paid": "int",
            "quote": "dict"
          },
          "methods": [
            {
              "name": "from_quote",
              "line": 51
            },
            {
              "name": "total",
              "line": 68
            }
          ]
        },
        {
          "class": "ConcentrationLedger",
          "line": 94,
          "fields": {
            "current": "runtime state; see exact code"
          },
          "methods": [
            {
              "name": "__init__",
              "line": 102
            },
            {
              "name": "end",
              "line": 104
            },
            {
              "name": "start_committed",
              "line": 109
            },
            {
              "name": "detach",
              "line": 114
            }
          ]
        },
        {
          "class": "PhysicalOrigin",
          "line": 119,
          "fields": {
            "identity": "str",
            "kind": "str",
            "size": "str",
            "type_tags": "frozenset",
            "mass": "int | None",
            "value": "int | None"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 127
            }
          ]
        },
        {
          "class": "Body",
          "line": 135,
          "fields": {
            "origin": "PhysicalOrigin",
            "life": "object",
            "size": "str",
            "mass": "int | None",
            "equipment": "set",
            "melded": "set",
            "lost_items": "set",
            "destroyed": "bool",
            "anatomy": "str | None",
            "slot_sponsor": "str | None",
            "controller": "str | None",
            "placement_pending": "bool",
            "placement_conflict": "bool"
          },
          "methods": [
            {
              "name": "identity",
              "line": 157
            }
          ]
        },
        {
          "class": "Selection",
          "line": 161,
          "fields": {
            "target": "str",
            "profile": "str | None",
            "willing": "bool",
            "original_cells": "frozenset",
            "transformed_cells": "frozenset",
            "legal": "bool",
            "object_template": "str | None",
            "object_size": "str | None",
            "object_mass": "int | None",
            "object_value": "int | None",
            "object_input_eligible": "bool",
            "mundane_output_certified": "bool"
          },
          "methods": []
        },
        {
          "class": "Link",
          "line": 179,
          "fields": {
            "identity": "str",
            "cast_id": "str",
            "target": "str",
            "profile": "str | None",
            "willing": "bool",
            "deadline": "int",
            "state": "str",
            "object_template": "str | None",
            "object_size": "str | None",
            "object_mass": "int | None",
            "last_switch": "int | None",
            "suppressed": "bool"
          },
          "methods": []
        },
        {
          "class": "Cast",
          "line": 195,
          "fields": {
            "identity": "str",
            "spell_id": "str",
            "caster": "str",
            "rank": "int",
            "stats": "CastStats",
            "casting_regular_index": "int",
            "links": "list",
            "state": "str"
          },
          "methods": []
        },
        {
          "class": "TransformationWorld",
          "line": 216,
          "fields": {
            "buffers": "runtime state; see exact code",
            "concentration": "runtime state; see exact code",
            "bodies": "runtime state; see exact code",
            "casts": "runtime state; see exact code",
            "links": "runtime state; see exact code",
            "slots": "runtime state; see exact code",
            "druids": "runtime state; see exact code",
            "damage_rounds": "runtime state; see exact code",
            "damage_events": "runtime state; see exact code",
            "regular_ends": "runtime state; see exact code",
            "commands": "runtime state; see exact code",
            "events": "runtime state; see exact code"
          },
          "methods": [
            {
              "name": "__init__",
              "line": 218
            },
            {
              "name": "add_body",
              "line": 227
            },
            {
              "name": "current",
              "line": 236
            },
            {
              "name": "_current_creature",
              "line": 240
            },
            {
              "name": "_validate_selection",
              "line": 245
            },
            {
              "name": "cast",
              "line": 289
            },
            {
              "name": "_apply",
              "line": 327
            },
            {
              "name": "_release_slot",
              "line": 350
            },
            {
              "name": "_end_link",
              "line": 354
            },
            {
              "name": "_end_cast",
              "line": 372
            },
            {
              "name": "_active",
              "line": 379
            },
            {
              "name": "repeat_save",
              "line": 387
            },
            {
              "name": "checkpoint",
              "line": 408
            },
            {
              "name": "reject",
              "line": 422
            },
            {
              "name": "finalize_damage_state",
              "line": 430
            },
            {
              "name": "check_reversion_placement",
              "line": 444
            },
            {
              "name": "clear_geometry_conflict",
              "line": 451
            },
            {
              "name": "dispel",
              "line": 455
            },
            {
              "name": "set_suppressed",
              "line": 459
            },
            {
              "name": "_stats_for",
              "line": 470
            },
            {
              "name": "profile",
              "line": 475
            },
            {
              "name": "healing_target_eligible",
              "line": 500
            },
            {
              "name": "acquire_external_gear",
              "line": 504
            },
            {
              "name": "mark_item_lost",
              "line": 511
            },
            {
              "name": "switch_shapechange",
              "line": 516
            },
            {
              "name": "attack",
              "line": 532
            },
            {
              "name": "_attack_packet",
              "line": 540
            },
            {
              "name": "command",
              "line": 548
            },
            {
              "name": "resolve_command",
              "line": 559
            },
            {
              "name": "uncommanded",
              "line": 572
            }
          ]
        }
      ]
    },
    {
      "path": "tools/device_lifecycle_playtest_rules.py",
      "sha256": "f474ef83e12066aab4325a275e2ae6113f7dee0d446f0c79e25141130f71c451",
      "stateHolders": [
        {
          "class": "Wallet",
          "line": 22,
          "fields": {
            "rp": "int",
            "actions": "int",
            "bonus_action": "bool",
            "reaction": "bool",
            "used": "set"
          },
          "methods": [
            {
              "name": "validate",
              "line": 29
            },
            {
              "name": "pay",
              "line": 42
            }
          ]
        },
        {
          "class": "CommandLedger",
          "line": 52,
          "fields": {
            "owner": "str",
            "rounds": "dict",
            "reservations": "dict"
          },
          "methods": [
            {
              "name": "validate",
              "line": 58
            },
            {
              "name": "reserve",
              "line": 75
            },
            {
              "name": "settle",
              "line": 87
            },
            {
              "name": "activate",
              "line": 95
            }
          ]
        },
        {
          "class": "Entity",
          "line": 105,
          "fields": {
            "instance_id": "str",
            "owner": "str",
            "source_id": "str",
            "kind": "str",
            "maximum_hp": "int | None",
            "hp": "int | None",
            "ac": "int | None",
            "expiry": "ClockMarker | None",
            "slot_kind": "str | None",
            "slot_count": "int",
            "asset_id": "str | None",
            "state": "str",
            "disabled": "bool",
            "disabled_reason": "str | None",
            "temp_hp": "int",
            "parent_id": "str | None",
            "concentration": "str | None",
            "paid_deployment_rp": "int",
            "modules": "tuple",
            "ammunition": "dict",
            "spent_uses": "set",
            "effects": "dict",
            "destruction_history": "list",
            "material_event": "str | None",
            "damaging_profile": "bool",
            "attack_bonus": "int | None",
            "unavailable": "bool",
            "superseded": "bool",
            "no_own_destruction_chain": "bool",
            "is_copy": "bool"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 137
            },
            {
              "name": "active",
              "line": 165
            },
            {
              "name": "functional",
              "line": 169
            },
            {
              "name": "machine_target",
              "line": 172
            },
            {
              "name": "field_repair_target",
              "line": 176
            }
          ]
        },
        {
          "class": "Destruction",
          "line": 185,
          "fields": {
            "event_id": "str",
            "instance_id": "str",
            "enemy_caused": "bool",
            "enemy_hit": "bool",
            "deliberate_sacrifice": "bool",
            "copied_object": "bool",
            "friendly_damage": "bool",
            "secondary_explosion": "bool",
            "flags": "frozenset",
            "hostile_source": "str | None",
            "first_for_instance": "bool",
            "material_available": "bool",
            "material_consumer": "str | None",
            "volatile_settled": "bool",
            "no_replacement": "bool",
            "cinder_settled": "bool",
            "no_own_destruction_chain": "bool",
            "incoming_damage_was_copy": "bool"
          },
          "methods": [
            {
              "name": "hostile_qualifies",
              "line": 205
            }
          ]
        },
        {
          "class": "Lifecycle",
          "line": 242,
          "fields": {
            "capacities": "runtime state; see exact code",
            "entities": "runtime state; see exact code",
            "destructions": "runtime state; see exact code",
            "volatile_rounds": "runtime state; see exact code"
          },
          "methods": [
            {
              "name": "__init__",
              "line": 243
            },
            {
              "name": "entity",
              "line": 251
            },
            {
              "name": "closure",
              "line": 255
            },
            {
              "name": "occupied",
              "line": 261
            },
            {
              "name": "free",
              "line": 266
            },
            {
              "name": "end",
              "line": 269
            },
            {
              "name": "advance",
              "line": 278
            },
            {
              "name": "place",
              "line": 285
            },
            {
              "name": "end_concentration",
              "line": 328
            },
            {
              "name": "retract",
              "line": 334
            },
            {
              "name": "redeploy",
              "line": 339
            },
            {
              "name": "disable",
              "line": 346
            },
            {
              "name": "set_disabled",
              "line": 354
            },
            {
              "name": "tools_clear_disable",
              "line": 360
            },
            {
              "name": "completed_short_rest",
              "line": 368
            },
            {
              "name": "field_repair",
              "line": 372
            },
            {
              "name": "repair_pulse",
              "line": 381
            },
            {
              "name": "damage",
              "line": 396
            },
            {
              "name": "material",
              "line": 422
            },
            {
              "name": "consume_material",
              "line": 429
            },
            {
              "name": "reconstruct",
              "line": 434
            },
            {
              "name": "recycling",
              "line": 448
            },
            {
              "name": "salvage",
              "line": 459
            },
            {
              "name": "settle_volatile",
              "line": 476
            },
            {
              "name": "cinder_destruction",
              "line": 488
            },
            {
              "name": "injection_cost",
              "line": 497
            },
            {
              "name": "reconfigure",
              "line": 504
            },
            {
              "name": "recompute_drone",
              "line": 519
            },
            {
              "name": "long_rest_drone",
              "line": 527
            },
            {
              "name": "configure_drones",
              "line": 548
            }
          ]
        }
      ]
    },
    {
      "path": "tools/creature_lifecycle_playtest_rules.py",
      "sha256": "6ff04cf57ac4083560498e534e0e402f5e000b199999bdf572b403784f9eb31d",
      "stateHolders": [
        {
          "class": "SourceStats",
          "line": 24,
          "fields": {
            "owner": "str",
            "source_class": "str",
            "level": "int",
            "pb": "int",
            "modifier": "int",
            "scale": "int",
            "attack": "int",
            "dc": "int",
            "wisdom": "int"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 35
            }
          ]
        },
        {
          "class": "Creature",
          "line": 63,
          "fields": {
            "instance_id": "str",
            "source_owner": "str",
            "controller": "str",
            "source_class": "str",
            "source_id": "str",
            "profile": "str",
            "life_kind": "str",
            "base_maximum": "int",
            "maximum_hp": "int",
            "hp": "int",
            "ac": "int",
            "speed": "int",
            "expiry": "ClockMarker | None",
            "concentration": "str | None",
            "parent_form": "str | None",
            "command_group": "str | None",
            "asset_id": "str | None",
            "state": "str",
            "temp_hp": "int",
            "temp_expiry": "ClockMarker | None",
            "blocked_round": "int | None",
            "focus": "str | None",
            "movement_mode": "str",
            "keen_sense": "str | None",
            "effects": "dict",
            "spent_uses": "set",
            "recharges": "dict",
            "max_hp_records": "list",
            "round_options": "set",
            "appearance": "str | None",
            "movement_overrides": "dict",
            "death_count": "int",
            "invisible": "bool",
            "invis_resume_marker": "int",
            "last_marker": "int"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 100
            },
            {
              "name": "active",
              "line": 109
            },
            {
              "name": "can_act",
              "line": 112
            },
            {
              "name": "verify_stats",
              "line": 115
            },
            {
              "name": "refresh_maximum",
              "line": 118
            },
            {
              "name": "attack_profile",
              "line": 131
            },
            {
              "name": "regular_end",
              "line": 147
            },
            {
              "name": "offense_event",
              "line": 155
            }
          ]
        },
        {
          "class": "Corpse",
          "line": 162,
          "fields": {
            "body_id": "str",
            "creature_id": "str",
            "creature_type": "str",
            "goblinoid": "bool",
            "real_original": "bool",
            "body_state": "str",
            "consumed_by": "str | None"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 172
            },
            {
              "name": "available",
              "line": 177
            },
            {
              "name": "eligible",
              "line": 179
            }
          ]
        },
        {
          "class": "RaiseReservation",
          "line": 186,
          "fields": {
            "order_id": "str",
            "owner": "str",
            "corpse_id": "str",
            "profile": "str",
            "round_number": "int",
            "checkpoint_id": "str",
            "pact": "bool"
          },
          "methods": []
        },
        {
          "class": "AttachedOrder",
          "line": 197,
          "fields": {
            "order_id": "str",
            "owner": "str",
            "creatures": "tuple",
            "mode": "str",
            "round_number": "int",
            "attacks": "int",
            "settled": "bool"
          },
          "methods": []
        },
        {
          "class": "HardDenialLedger",
          "line": 208,
          "fields": {
            "used": "set"
          },
          "methods": [
            {
              "name": "available",
              "line": 212
            },
            {
              "name": "spend",
              "line": 216
            }
          ]
        },
        {
          "class": "ReflectiveBond",
          "line": 222,
          "fields": {
            "owner": "str",
            "target_id": "str",
            "effect_id": "str",
            "expiry": "ClockMarker",
            "concentration": "str",
            "active": "bool",
            "forced_action_used": "bool",
            "pending": "dict | None"
          },
          "methods": [
            {
              "name": "operative",
              "line": 232
            },
            {
              "name": "cancel",
              "line": 234
            },
            {
              "name": "revalidate_pending",
              "line": 240
            },
            {
              "name": "end",
              "line": 247
            },
            {
              "name": "queue",
              "line": 250
            },
            {
              "name": "resolve",
              "line": 261
            }
          ]
        },
        {
          "class": "EchoLedger",
          "line": 276,
          "fields": {
            "owner": "str",
            "records": "set",
            "released_rounds": "set"
          },
          "methods": []
        },
        {
          "class": "CreatureWorld",
          "line": 283,
          "fields": {
            "creatures": "runtime state; see exact code",
            "corpses": "runtime state; see exact code",
            "reflective": "runtime state; see exact code",
            "reservations": "runtime state; see exact code",
            "auto_used": "runtime state; see exact code",
            "closed_checkpoints": "runtime state; see exact code",
            "orders": "runtime state; see exact code",
            "completed_rests": "runtime state; see exact code",
            "ranger_deaths": "runtime state; see exact code",
            "noncorpse_identities": "runtime state; see exact code"
          },
          "methods": [
            {
              "name": "__init__",
              "line": 284
            },
            {
              "name": "fresh",
              "line": 290
            },
            {
              "name": "register_corpse",
              "line": 294
            },
            {
              "name": "consume_body",
              "line": 303
            },
            {
              "name": "standard_count",
              "line": 308
            },
            {
              "name": "_end_mirror_slot",
              "line": 312
            },
            {
              "name": "summon",
              "line": 318
            },
            {
              "name": "end_dependency",
              "line": 364
            },
            {
              "name": "expire",
              "line": 377
            },
            {
              "name": "damage",
              "line": 387
            },
            {
              "name": "heal",
              "line": 410
            },
            {
              "name": "record_ranger_resurrection",
              "line": 416
            },
            {
              "name": "bond_ranger",
              "line": 437
            },
            {
              "name": "unlock_lich",
              "line": 462
            },
            {
              "name": "soulbound",
              "line": 478
            },
            {
              "name": "completed_long_rest",
              "line": 489
            },
            {
              "name": "_new_standard",
              "line": 501
            },
            {
              "name": "harvest",
              "line": 509
            },
            {
              "name": "dismiss",
              "line": 518
            },
            {
              "name": "auto_raise_trigger",
              "line": 523
            },
            {
              "name": "auto_raise_checkpoint",
              "line": 536
            },
            {
              "name": "command",
              "line": 564
            },
            {
              "name": "resolve_command",
              "line": 586
            },
            {
              "name": "uncommanded",
              "line": 593
            },
            {
              "name": "apply_reflective",
              "line": 597
            },
            {
              "name": "echo_from_beast",
              "line": 608
            },
            {
              "name": "shift_appearance",
              "line": 620
            }
          ]
        }
      ]
    },
    {
      "path": "tools/remaining_lifecycle_playtest_rules.py",
      "sha256": "5025094fbc461e41a72d2018852513823102039cab6fb8e96941ccb94594ff62",
      "stateHolders": [
        {
          "class": "Stats",
          "line": 30,
          "fields": {
            "owner": "str",
            "source_class": "str",
            "level": "int",
            "pb": "int",
            "scale": "int",
            "modifier": "int",
            "attack": "int",
            "dc": "int",
            "constitution": "int",
            "dexterity": "int",
            "charisma": "int"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 43
            }
          ]
        },
        {
          "class": "Points",
          "line": 58,
          "fields": {
            "owner": "str",
            "resource": "str",
            "value": "int"
          },
          "methods": [
            {
              "name": "validate",
              "line": 64
            }
          ]
        },
        {
          "class": "RemainingCreature",
          "line": 71,
          "fields": {
            "position": "object",
            "explosion_settled": "bool",
            "local_modes": "dict"
          },
          "methods": [
            {
              "name": "attack_profile",
              "line": 76
            }
          ]
        },
        {
          "class": "Structure",
          "line": 92,
          "fields": {
            "instance_id": "str",
            "owner": "str",
            "kind": "str",
            "maximum_hp": "int",
            "hp": "int",
            "expiry": "ClockMarker | None",
            "area_resistance": "bool",
            "state": "str",
            "ac": "int"
          },
          "methods": [
            {
              "name": "active",
              "line": 103
            }
          ]
        },
        {
          "class": "Supplies",
          "line": 108,
          "fields": {
            "owner": "str",
            "kits": "int",
            "field_supplies": "int",
            "spare_parts": "int",
            "deployments": "dict",
            "repaired": "set"
          },
          "methods": [
            {
              "name": "validate",
              "line": 116
            },
            {
              "name": "completed_rest",
              "line": 122
            }
          ]
        },
        {
          "class": "IncomingAttacks",
          "line": 129,
          "fields": {
            "closed": "set"
          },
          "methods": [
            {
              "name": "validate",
              "line": 133
            },
            {
              "name": "commit",
              "line": 138
            }
          ]
        },
        {
          "class": "ExistingUndeadBuff",
          "line": 147,
          "fields": {
            "owner": "str",
            "members": "frozenset",
            "expiry": "ClockMarker",
            "first_damage": "set"
          },
          "methods": [
            {
              "name": "operative",
              "line": 153
            },
            {
              "name": "attack_bonus",
              "line": 156
            },
            {
              "name": "first_damage_offer",
              "line": 160
            }
          ]
        },
        {
          "class": "RemainingWorld",
          "line": 168,
          "fields": {
            "physical": "runtime state; see exact code",
            "structures": "runtime state; see exact code",
            "orders": "runtime state; see exact code",
            "choirs": "runtime state; see exact code",
            "choir_healing": "runtime state; see exact code",
            "hit_events": "runtime state; see exact code",
            "unbound_buffs": "runtime state; see exact code",
            "synergy_turns": "runtime state; see exact code"
          },
          "methods": [
            {
              "name": "__init__",
              "line": 169
            },
            {
              "name": "fresh",
              "line": 174
            },
            {
              "name": "create",
              "line": 178
            },
            {
              "name": "choir",
              "line": 182
            },
            {
              "name": "thrall",
              "line": 196
            },
            {
              "name": "unbound",
              "line": 208
            },
            {
              "name": "turrets",
              "line": 227
            },
            {
              "name": "command",
              "line": 237
            },
            {
              "name": "resolve_command",
              "line": 252
            },
            {
              "name": "choir_hit",
              "line": 262
            },
            {
              "name": "burst",
              "line": 275
            },
            {
              "name": "damage",
              "line": 286
            },
            {
              "name": "end_choir",
              "line": 298
            },
            {
              "name": "expire",
              "line": 307
            },
            {
              "name": "sacrifice",
              "line": 318
            },
            {
              "name": "palisade",
              "line": 329
            },
            {
              "name": "quick_deploy",
              "line": 342
            },
            {
              "name": "structure_damage",
              "line": 354
            },
            {
              "name": "repair",
              "line": 361
            },
            {
              "name": "dismantle",
              "line": 369
            },
            {
              "name": "palisade_benefits",
              "line": 375
            },
            {
              "name": "synergy",
              "line": 380
            }
          ]
        },
        {
          "class": "LedgerControl",
          "line": 388,
          "fields": {
            "owner": "str",
            "application_id": "str",
            "expiry": "ClockMarker",
            "targets": "dict",
            "interception_used": "bool",
            "pending": "dict",
            "order_ids": "set",
            "first_damage": "set"
          },
          "methods": [
            {
              "name": "apply",
              "line": 399
            },
            {
              "name": "operative",
              "line": 411
            },
            {
              "name": "issue",
              "line": 414
            },
            {
              "name": "cancel",
              "line": 430
            },
            {
              "name": "resolve",
              "line": 435
            },
            {
              "name": "revalidate",
              "line": 450
            },
            {
              "name": "regular_end",
              "line": 458
            },
            {
              "name": "first_damage_offer",
              "line": 469
            },
            {
              "name": "intercept",
              "line": 474
            }
          ]
        },
        {
          "class": "WeaponProfile",
          "line": 483,
          "fields": {
            "attack": "int",
            "dice": "tuple",
            "flat": "int",
            "damage_type": "str",
            "range_feet": "int"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 490
            },
            {
              "name": "capped_damage",
              "line": 495
            }
          ]
        },
        {
          "class": "FallenEchoes",
          "line": 509,
          "fields": {
            "deaths": "set",
            "uses": "set"
          },
          "methods": [
            {
              "name": "record_death",
              "line": 513
            },
            {
              "name": "invoke",
              "line": 518
            }
          ]
        },
        {
          "class": "SpiritScout",
          "line": 540,
          "fields": {
            "owner": "str",
            "mode": "str",
            "expiry": "ClockMarker",
            "state": "str",
            "delivered_message": "bool",
            "observations": "list"
          },
          "methods": [
            {
              "name": "summon",
              "line": 549
            },
            {
              "name": "arrive_and_perform",
              "line": 555
            },
            {
              "name": "return_report",
              "line": 560
            },
            {
              "name": "expire",
              "line": 566
            }
          ]
        }
      ]
    },
    {
      "path": "tools/buffer_feat_playtest_rules.py",
      "sha256": "7231e190dc4aa6d80a32b293f6d6b7753d3ec2ac0e0b6c280308b58b491cb9c1",
      "stateHolders": [
        {
          "class": "FeatStats",
          "line": 24,
          "fields": {
            "level": "int",
            "pb": "int",
            "charisma_score": "int",
            "charisma_modifier": "int",
            "constitution_score": "int",
            "medicine": "bool",
            "religion": "bool",
            "casting": "dict"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 35
            }
          ]
        },
        {
          "class": "Owner",
          "line": 46,
          "fields": {
            "stats": "FeatStats",
            "feats": "set",
            "acquisition_events": "set",
            "soul_dc_source": "str | None",
            "soul_charges": "int",
            "recovery": "int",
            "recovery_capacity": "int",
            "last_rest": "int"
          },
          "methods": []
        },
        {
          "class": "LongActivity",
          "line": 58,
          "fields": {
            "id": "str",
            "owner": "str",
            "feat": "str",
            "started": "Fraction",
            "ends": "Fraction",
            "targets": "tuple",
            "level": "int",
            "pb": "int",
            "charisma": "int",
            "state": "str"
          },
          "methods": []
        },
        {
          "class": "Kit",
          "line": 72,
          "fields": {
            "item_id": "str",
            "uses": "int"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 76
            }
          ]
        },
        {
          "class": "Rations",
          "line": 81,
          "fields": {
            "inventory_id": "str",
            "servings": "int"
          },
          "methods": [
            {
              "name": "__post_init__",
              "line": 85
            }
          ]
        },
        {
          "class": "Stabilization",
          "line": 90,
          "fields": {
            "event_id": "str",
            "owner": "str",
            "target": "str",
            "episode": "str",
            "pb": "int"
          },
          "methods": []
        },
        {
          "class": "FeatWorld",
          "line": 98,
          "fields": {
            "buffers": "runtime state; see exact code",
            "healing_commits": "runtime state; see exact code",
            "owners": "runtime state; see exact code",
            "activities": "runtime state; see exact code",
            "family_uses": "runtime state; see exact code",
            "blood_uses": "runtime state; see exact code",
            "blood_advantage": "runtime state; see exact code",
            "summon_lineages": "runtime state; see exact code",
            "summon_damage": "runtime state; see exact code",
            "stabilizations": "runtime state; see exact code",
            "stabilization_episodes": "runtime state; see exact code",
            "finished_stabilizations": "runtime state; see exact code",
            "melee_turns": "runtime state; see exact code",
            "seals": "runtime state; see exact code",
            "ended_deaths": "runtime state; see exact code",
            "removed_seals": "runtime state; see exact code",
            "drain_selections": "runtime state; see exact code",
            "drain_used": "runtime state; see exact code",
            "soul_events": "runtime state; see exact code",
            "soul_bodies": "runtime state; see exact code",
            "spends": "runtime state; see exact code",
            "agony": "runtime state; see exact code",
            "agony_generation": "runtime state; see exact code",
            "chef_attempts": "runtime state; see exact code",
            "chef_completed": "runtime state; see exact code",
            "servings": "runtime state; see exact code"
          },
          "methods": [
            {
              "name": "__init__",
              "line": 99
            },
            {
              "name": "register",
              "line": 127
            },
            {
              "name": "epoch",
              "line": 132
            },
            {
              "name": "has",
              "line": 135
            },
            {
              "name": "require_feat",
              "line": 138
            },
            {
              "name": "acquire",
              "line": 142
            },
            {
              "name": "completed_rest",
              "line": 160
            },
            {
              "name": "grant",
              "line": 173
            },
            {
              "name": "family_key",
              "line": 178
            },
            {
              "name": "start_cooking",
              "line": 181
            },
            {
              "name": "finish_cooking",
              "line": 190
            },
            {
              "name": "abort_cooking_rest",
              "line": 204
            },
            {
              "name": "finalize_chef",
              "line": 209
            },
            {
              "name": "serving_potent",
              "line": 222
            },
            {
              "name": "consume_chef",
              "line": 227
            },
            {
              "name": "retire_serving",
              "line": 239
            },
            {
              "name": "start_activity",
              "line": 244
            },
            {
              "name": "interrupt_activity",
              "line": 264
            },
            {
              "name": "finish_activity",
              "line": 269
            },
            {
              "name": "blood_save",
              "line": 301
            },
            {
              "name": "summon_created",
              "line": 308
            },
            {
              "name": "summon_damage_bonus",
              "line": 322
            },
            {
              "name": "record_stabilization",
              "line": 331
            },
            {
              "name": "kit_stabilize",
              "line": 344
            },
            {
              "name": "finish_stabilization",
              "line": 358
            },
            {
              "name": "melee_necrotic",
              "line": 366
            },
            {
              "name": "seal_death",
              "line": 375
            },
            {
              "name": "resurrection_sealed",
              "line": 384
            },
            {
              "name": "remove_seal",
              "line": 392
            },
            {
              "name": "returned_to_life",
              "line": 397
            },
            {
              "name": "select_drain",
              "line": 401
            },
            {
              "name": "drain",
              "line": 409
            },
            {
              "name": "death_checkpoint",
              "line": 445
            },
            {
              "name": "begin_soul_ability",
              "line": 470
            },
            {
              "name": "finish_soul_shield",
              "line": 487
            },
            {
              "name": "finish_agony",
              "line": 497
            },
            {
              "name": "agony_reduction",
              "line": 521
            },
            {
              "name": "commit_healing",
              "line": 527
            },
            {
              "name": "remove_agony",
              "line": 532
            },
            {
              "name": "release_souls",
              "line": 536
            }
          ]
        }
      ]
    }
  ]
}


## Verified original geometry passages

{
  "status": "PREPARED / general mandatory-reversion placement conference not yet submitted",
  "scope": "Verified existing movement/space/squeeze rules; they do not answer involuntary growth overlap by themselves",
  "verifiedPassages": 7,
  "records": [
    {
      "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
      "sourceFileSha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
      "paragraphIndexConvention": "zero-based all XML w:p descendants, including table cells",
      "paragraph": 396,
      "exactText": "Prepare against a charge, leap, forced movement, or door breach.",
      "priorQuotedText": "Prepare against a charge, leap, forced movement, or door breach."
    },
    {
      "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
      "sourceFileSha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
      "paragraphIndexConvention": "zero-based all XML w:p descendants, including table cells",
      "paragraph": 434,
      "exactText": "Combat uses feet or 5-foot spaces. Movement can be split around actions and attacks. Difficult terrain costs 2 feet per foot. Severe terrain costs 3 feet per foot and may require a check.",
      "priorQuotedText": "Combat uses feet or 5-foot spaces. Movement can be split around actions and attacks. Difficult terrain costs 2 feet per foot. Severe terrain costs 3 feet per foot and may require a check."
    },
    {
      "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
      "sourceFileSha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
      "paragraphIndexConvention": "zero-based all XML w:p descendants, including table cells",
      "paragraph": 435,
      "exactText": "Forced movement does not provoke opportunity attacks unless a feature explicitly says it does. Falling, flowing water, conveyor mechanisms, gravity changes, and living dungeon surfaces are common sources of forced movement.",
      "priorQuotedText": "Forced movement does not provoke opportunity attacks unless a feature explicitly says it does. Falling, flowing water, conveyor mechanisms, gravity changes, and living dungeon surfaces are common sources of forced movement."
    },
    {
      "path": "books/player/Decennium_Descent_Player_Rulebook_v6.docx",
      "sourceFileSha256": "a753da2ce935ed29e4f3f14575f3785140821c3f0c43adb760da6149b12e295e",
      "paragraphIndexConvention": "zero-based all XML w:p descendants, including table cells",
      "paragraph": 8138,
      "exactText": "You can move through a nonhostile creature's space (it's difficult terrain). You can only move through a hostile creature's space if it's at least two sizes larger or smaller than you. You cannot willingly end your move in another creature's space.",
      "priorQuotedText": "You can move through a nonhostile creature's space (it's difficult terrain). You can only move through a hostile creature's space if it's at least two sizes larger or smaller than you. You cannot willingly end your move in another creature's space."
    },
    {
      "path": "books/player/Decennium_Descent_Player_Rulebook_v6.docx",
      "sourceFileSha256": "a753da2ce935ed29e4f3f14575f3785140821c3f0c43adb760da6149b12e295e",
      "paragraphIndexConvention": "zero-based all XML w:p descendants, including table cells",
      "paragraph": 8146,
      "exactText": "Creatures occupy space from Tiny (2.5x2.5 ft) to Gargantuan (20x20 ft or larger). Most player races are Medium (5x5 ft). A creature's space is the area it controls in combat.",
      "priorQuotedText": "Creatures occupy space from Tiny (2.5x2.5 ft) to Gargantuan (20x20 ft or larger). Most player races are Medium (5x5 ft). A creature's space is the area it controls in combat."
    },
    {
      "path": "books/player/Decennium_Descent_Player_Rulebook_v6.docx",
      "sourceFileSha256": "a753da2ce935ed29e4f3f14575f3785140821c3f0c43adb760da6149b12e295e",
      "paragraphIndexConvention": "zero-based all XML w:p descendants, including table cells",
      "paragraph": 8148,
      "exactText": "Squeezing",
      "priorQuotedText": "Squeezing"
    },
    {
      "path": "books/player/Decennium_Descent_Player_Rulebook_v6.docx",
      "sourceFileSha256": "a753da2ce935ed29e4f3f14575f3785140821c3f0c43adb760da6149b12e295e",
      "paragraphIndexConvention": "zero-based all XML w:p descendants, including table cells",
      "paragraph": 8150,
      "exactText": "A creature can squeeze into a space one size smaller than itself. While squeezing, movement costs 1 extra foot per foot moved, attack rolls and Dexterity saves have disadvantage, and attacks against the creature have advantage.",
      "priorQuotedText": "A creature can squeeze into a space one size smaller than itself. While squeezing, movement costs 1 extra foot per foot moved, attack rolls and Dexterity saves have disadvantage, and attacks against the creature have advantage."
    }
  ],
  "openQuestions": "MANDATORY_REVERSION_GEOMETRY_PREPARATION.md"
}
