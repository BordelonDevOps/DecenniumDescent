# Map Route work prototype policy

**Status:** Codex/GPT consensus implemented as an opt-in schema59 TEST_ONLY procedure. It closes the bounded labor/check gap for one authored route profile. It is not verbatim source text, production content, or release approval.

## Source authority and open source gaps

The Player Book pin is `EX58-EXACT-2026-10-11`, revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, SHA-256 `4c58b9f7063e562b785b8db6006699d3c4f68edd0e697d06db69662ba9b7e480`, `DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md`.

- FL-02 requires actual participant assignments, locations, lead/helpers and work intervals; a person cannot perform incompatible work during the same seconds. Generic expedition assistants who can meaningfully help must be trained; each contributes +1, with at most three.
- FL-03 supplies 480 active minutes for a generic Watch task before its completion check and permits feasible unfinished work to continue. That work interval is distinct from the route segment's nominal travel effort.
- FL-10 gives Mapping outcomes: one mark on success, two on critical success, and one Mapping step after `max(1, recorded Risk)` marks. Mapping normally affects a later segment. Unknown passage still needs successful reconnaissance or resolved Forced March before ordinary travel.
- FL-11's WIS (Survival), tier DC +6 procedure is **Forced March**. Its modifier is not imported into ordinary Map Route.
- `docs/mechanics/GAMEPLAY_LOOP_CANON.md` §2 defines tier-standard DCs and the generic team-check shape (SHA-256 `deefa5a4df2060d4f9c91adc32bb787ff5080c23180089a0537a02a5052c7590`). `DescentReviewChanges/ReviewBible/docs/mechanics/CORE_RESOLUTION_PLAYTEST.md` defines check degrees and natural shifts (SHA-256 `69d0e64394de58c4d86a3ec57cf282978d131a1a9c1eaa21632bb7d3b72562da`).

These sources do not settle ordinary Map Route's exact approach/skill, the completion-time method, failure/retry cost, or the participant's precise physical work position. The policy below records explicit prototype choices for those gaps.

## Adopted TEST_ONLY procedure

- The worker performs one stationary Map Route task for **480 active minutes** (28,800 seconds). Its interval is reserved in the shared `WorkLedger` and accrued by the existing `RuleClock`; it is not folded into route travel's 480 nominal minutes.
- The lead makes a **WIS (Survival)** check against the route's **tier-standard DC**. The finite fixture uses the standard tier table: I 12, II 13, III 15, IV 16, V 18, VI 19. The lead may be untrained. Existing ability/check derivation applies the lead's actual recorded rank if trained.
- Each trained assistant who participates for the complete work interval contributes +1, up to three. Every participant reserves the same actual 480 active minutes. Incompatible existing labor reservations reject the command. The helpers' time cannot be spent on another job during those seconds.
- Pause retains completed seconds and closes the participants' future reservations at the current clock. Resume reserves only the remaining seconds. One check is rolled from the existing deterministic RNG when the full interval completes.
- Completion ordering uses the shared clock boundary: credit the final work first, process due boundary effects, then revalidate the lead and resolve one check. Currently represented Poisoned state imposes disadvantage on this ability check; both d20 results and selection mode are retained with the check evidence. The record also stores the exact condition-journal operation count used at resolution, so a later operation at the same paused timestamp cannot rewrite the historical check during validation or replay. If the lead is incapable after boundary processing, the attempt remains `AwaitingCheck` with all labor retained and no roll or Mapping result; a later valid Resume resolves the check without more work. This uses existing supported condition/capability state, not a general modifier aggregator.
- One-second synchronous inventory/vessel handling cannot cross an active Map Route completion boundary. It fails with `TimedHandlingBoundaryUnsupported`; advancing through the shared clock processes the exact route-work endpoint and its completion check.
- A successful check gives one Mapping mark; a critical success gives two. The existing `ExpeditionRouteMappingRules.Apply` consumes at most one `max(1, recorded Risk)` threshold for that distinct result and retains any surplus. Failure/critical failure gives no Mapping change. Each retry is a separate immutable attempt requiring a fresh full 480 active minutes; it cannot reuse a previous failure's work or roll.
- The authored route remains immutable. Mapping results do not create a passage-feasibility record. An Unknown route continues to reject ordinary travel with `RouteRequiresReconnaissance` until a separate supported reconnaissance procedure establishes feasibility.
- A task binds to one authored route. Reservations apply to the named workers only; the route remains available to unrelated travelers while they work. The task does not advance route travel or create a group-wide route closure.

## Bounded fixture assumptions

`TestOnlyExpeditionRouteMappingWorkFixture` pins finite task tiers and Survival ranks, the existing authored route fingerprint and this policy fingerprint. Workers must be stationary within one cardinal five-foot grid cell of the route mouth. The fixture supplies the hero/companion party relationship so ordinary exploration does not interpret their approach as hostile encounter entry. That relationship, physical radius, authored grid, characters, skill facts, route, and task tiers are fixture data; they are not universal character, geography, or encounter rules.

The profile does not consume inventory, resolve reconnaissance, change route Risk/Pressure, model physical obstructions or tools, train a skill, or authorize passage. It is a narrow reusable work/check adapter over TEST_ONLY content.

## Responsibilities and authoritative records

- `ExpeditionRouteMappingWorkAttemptRecord` stores route, lead, assistants, revisions, exact work progress/status and optional immutable result evidence.
- `ExpeditionRouteMappingWorkCheckRecord` stores the completion command receipt, ability/training/assistant/DC inputs, natural and total, degree, deterministic RNG before/after and the before/after Mapping marks.
- `WorkLedger.WorkerInterval` is authoritative for each participant's reserved labor. `Snapshot.RuleClock` and the shared advance pipeline are authoritative for elapsed work.
- Existing command receipt/revision history, `DiceStream`/`RuleDice`, `ExpeditionRouteMappingRules`, immutable authored route Mapping, `SnapshotCodec`, `CommandHistory`, save/restore and replay remain authoritative. The procedure has no private clock, RNG, inventory ledger or mutable global state.

Schema59 appends route-work records after schema58. Older snapshot layouts remain unchanged. Route travel's schema53 spatial authority remains present for any active traveler in the schema59 layered profile; the existing authored route positions provide its discrete physical binding when no continuous motion fixture is selected.

## Runnable acceptance

- `route_mapping_work_uses_reserved_team_time_rng_and_persists`: pure query and full time cost; trained assistant with untrained lead; invalid self-assistance and over-cap team; shared participant intervals; 120-second pause; no passive paused work; save/restore; exact resume; natural-20 result; Unknown passage remains blocked; canonical command replay and RNG evidence.
- `route_mapping_work_applies_poisoned_disadvantage_and_persists_both_dice` and `route_mapping_work_uses_post_boundary_condition_state_at_completion`: Poisoned chooses and persists both dice, while expiration exactly at completion is processed before the check.
- `route_mapping_work_check_uses_condition_history_at_its_causal_point`: a Poisoned event dispatched after a normal check at the same game time leaves that earlier check and its RNG result unchanged through validation, save/restore and replay.
- `route_mapping_work_check_rejects_negative_condition_prefix`: malformed check evidence cannot claim a negative condition-journal prefix; record construction and state validation reject it.
- `route_mapping_work_synchronous_handling_cannot_cross_fractional_completion`: synchronous inventory handling is rejected half a second before the work endpoint, and a half-second shared-clock advance resolves the check at the exact fractional timestamp.
- `route_mapping_work_does_not_stop_an_unrelated_route_traveler`: separate traveler and mapper work concurrently against one route; after 300 seconds both show progress; the mapper finishes its 480-minute task and the traveler completes using the measured carried-load walking speed and route-quality rate.
- `failed_route_mapping_retry_requires_a_fresh_480_minutes`: natural-1 failure preserves Unknown Mapping; the next attempt starts at zero work, remains unresolved at 28,799 seconds and resolves only on its full 28,800th active second.

The synthetic pre-resolved result adapter remains a separate profile and is deliberately disabled in this work profile. Neither adapter implements reconnaissance, makes unknown passage feasible, completes all expedition rules, or establishes release behavior.
