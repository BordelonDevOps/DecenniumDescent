# Buried cache excavation prototype policy

Status: schema57 TEST_ONLY behavior on `Engine`, based on delegated Codex and **Unity Rules Engine Development** agreement. This is a new bounded prototype rule; it is not recovered source text or release approval.

## Responsibilities and authoritative records

- `BuriedCacheSiteRecord` binds one authored cache, its exact grid site, one physical shovel ID, and the once-only exposure time.
- `CacheExcavationRecord` stores the assigned worker, site, shovel, start/update times, exact retained labor and Working/Paused/Completed status.
- The existing `ExpeditionWorkAssignmentRecord` owns player intent and links to the procedure. The existing `WorkLedger` reserves the worker only for the active Working interval; pause removes future labor reservation, and resume rechecks availability. `PortableEquipmentRules.HasPendingClaim` prevents the claimed shovel from moving while the job is open, including while paused.
- The existing shared `RuleClock`, activity projection, command receipts, snapshot codec, replay and supply-cache handlers remain authoritative for time, queries, persistence and cache access.

## Adopted prototype behavior

- One explicitly authored, initially buried cache site is available in the TEST_ONLY profile. The procedure targets the existing cache and creates no deposit, tunnel, terrain removal or additional stock.
- A capable worker must be at the site, have two usable hands and access to the actual five-pound shovel assigned to that site. While Working, the worker-time interval and shovel are reserved against incompatible use. While Paused, the worker can take other compatible work if its own authorities permit it; resuming requires the normal capability, site, hands, shovel and worker-availability checks. The shovel remains physically claimed by the open job.
- Under this fixture's explicitly safe conditions, excavation takes **300 active worker seconds** and calls for no check or RNG. Only active labor advances the exact progress.
- Interruption, pause, incapacity or tactical entry retains completed work. The same job may resume when the worker is back at the site, capable, stationary, out of tactical control and has the shovel and both hands available.
- At exactly 300 active seconds the procedure exposes the existing cache once. Its existing lock, contents, inventory lineage and ownership are unchanged; normal cache interactions remain responsible for unlocking, opening and retrieval.
- Buried state gates contextual discovery, direct cache commands and physical inventory access. Exposure removes that burial gate without granting access through unrelated ownership, reach or lock checks.

## Source and fixture boundary

The shovel identity and five-pound source/operational mass are bound to the reviewed-authored PLAYTEST candidate at `DescentReviewChanges/ReviewBible/data/playtest/equipment_acquisition_candidate.json#/items/146`, pinned source blob `afd06198e19409385408ac258be7dc1d0b2600fb`. The operation-specific shovel manifest is separately pinned and does not modify the existing selected manifest digest. The excavation duration, safe-site/no-check procedure, retained progress and exposure outcome are delegated prototype choices; no source excavation rate or universal digging system is claimed.

The first fixture supports one authored site, one shovel, one open excavation and one existing cache. Variable geology, other tools, hazards, structural support, arbitrary terrain change, generated resources, multi-worker labor, cancellation, and production content selection remain unsupported. Earlier snapshot layouts are unchanged; only the opt-in profile uses schema57.

The runnable acceptance is `cache_excavation_assignment_resumes_exact_work_and_exposes_cache_once`, alongside `cache_excavation_requires_assignment_site_and_can_only_be_started_once`. Evidence and exact validation artifacts are linked from the implementation trace and current handoff.

## Cross-review and resume boundary

The implementation excerpts and adopted pause/resume contract were reviewed in **Unity Rules Engine Development** on 2026-11-07. GPT agreed that active worker reservation plus resume-time revalidation satisfies the contract and found no concrete blocker in the supplied summary. The shared invariants are: credit only feasible active labor through the authoritative clock; retain progress and the original assignment across pause; keep progress attached to the physical site; never reset or duplicate it by creating a new assignment identity; release the worker's future interval when paused; keep the physical shovel claimed; and reacquire remaining labor only after the normal worker, site, capability, hands and shovel checks pass. Resume does not interrupt another job.

GPT proposed an additional optional contention regression: pause after 100 seconds, give the worker another job, verify resume rejects atomically, complete or pause that job, then resume the original excavation with 200 seconds left. The current cache-only fixture has no second worker-consuming procedure, so that scenario is not included in this bounded acceptance. The implementation checks both current worker intervals and projected activity before resume; `Simulation.Execute` resolves on a candidate snapshot and commits only after successful validation, so a rejected resume leaves authoritative state unchanged. Add the contention case when this profile has a clean, supported second-job fixture; it is a coverage follow-up, not a rule blocker.
