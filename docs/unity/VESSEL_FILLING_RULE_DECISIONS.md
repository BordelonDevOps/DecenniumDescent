# Ordinary water filling proposal

Status: PROPOSED, NOT ADOPTED. Prepared2026-11-03 after the owner-approved ordinary inventory increment. No filling gameplay behavior is authorized by this proposal alone.

## Existing source requirements

- Expedition Player Book FL-05: filling one skin/flask takes60active seconds per worker, sequentially. A partial quantity has no specified proportional-time discount. Retrieval and handover remain separate applicable operations.
- Equipment Acquisition Playtest, Carrying and containers: actual container shape, opening, closure and access matter; ordinary flask capacity1pint and waterskin capacity4pints. The standard waterskin weighs1lb empty and5lb with4pints water. Do not substitute the oil-flask's0.25lb tare for a separately defined1lb ordinary flask/tankard.
- EX58 source contracts EC-02/03: reserve real worker/hands/resources; incompatible concurrent work rejects; maintain access, capacity, constituent identity, custody and original clocks. They do not specify one universal filling hand count or liquid debit timestamp.
- Expedition Director Book FL-03: retain interrupted feasible work progress unless an actual event undoes it. This does not specify how much liquid has already moved.
- The reviewed integrated-flow lighting example books a two-handed refill over108000–108060 and transfers its one pint at108060. Opening, pouring and securing are included in that example. The water-filling example gives28skins across four workers, seven minutes each, without an interrupted-fill boundary.

Primary sources at the pinned rules revision:

- [FL-05](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-05)
- [Equipment containers](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md#carrying-and-containers)
- [EX58 contracts](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EX58_SOURCE_CONTRACTS_CORRECTED.md)
- [Director work](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_DIRECTOR_BOOK.md)
- [Integrated flow](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/data/public/expedition_candidate/integrated_flow.json), `/lighting/refills/0`, `/lighting/transfers/2`, `/nextProcurement/waterFilling`.

## Proposed bounded prototype completion

1. Declare a fixed amount and specific source/destination. Reserve actual source liquid and destination free capacity. Starting the job moves no liquid.
2. Require one capable worker, two usable hands and physically feasible access/support for60active seconds. Include ordinary opening, pouring and securing in that minute. Retrieval and later handover retain their own costs.
3. Manual pause keeps feasible completed progress and the same liquid/capacity reservations, releases future worker/hand bookings and moves no liquid. Resume continues the same60-second requirement.
4. At completion, after applicable endpoint processing and revalidation, atomically transfer the declared amount into traced destination constituents. This is movement, not material consumption or nutrition credit. Mixed histories remain separate lots; age and ownership do not reset.
5. Cancellation releases outstanding material/capacity reservations and closes the job without moving liquid. Completed labor and actual world changes remain. No automatic spill, time refund or restored liquid is inferred.
6. Save/resume retains progress and reservations. There is no universal proportional pour rate, partial output or restart penalty under this proposal.

This first profile covers ordinary water in a supported, stable source/skin-or-flask arrangement with explicit access. It does not settle filling other vessel classes, incompatible liquids, contamination, breakage, hazardous pouring, magical containers or tactical filling. Known unsupported events within a proposed interval must prevent execution beyond the supported boundary; this proposal grants no immunity to them.

## GPT source consultation

Source: [Unity Rules Engine Development](https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206), response `776007e4-9c4a-5bb0-a861-53529196457d`,2026-11-03. GPT confirmed the commitment/interruption boundary is not fully sourced and explicitly marked its completion model as a new owner decision. Exact response follows.

**Not completely.** The sources establish the filling duration, physical access constraints and a general default for retaining feasible work. They do **not** fully specify the liquid-transfer boundary for an interrupted skin/flask fill. Progressive self-consumption does not fill that gap.

I checked the reviewed records at Engine `596aa5c8`.

**What is sourced**

| Question | Existing rule or evidence |
|---|---|
| Duration | [FL-05](https://github.com/BordelonDevOps/DecenniumDescent/blob/596aa5c8/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-05): one active minute per skin/flask, sequentially per worker. No proportional discount is specified. |
| Access and capacity | [Equipment — Carrying and containers](https://github.com/BordelonDevOps/DecenniumDescent/blob/596aa5c8/DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md#carrying-and-containers): actual shape, closure and access matter; ordinary flask capacity is **1 pint**, waterskin **4 pints**. |
| Worker and hands | [EC-02](https://github.com/BordelonDevOps/DecenniumDescent/blob/596aa5c8/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EX58_SOURCE_CONTRACTS_CORRECTED.md#ec-02--clock-assignment-work-and-rest) requires location/access throughout work and actual hand/resource reservations; conflicting assignments reject. It supplies **no universal filling hand count**. |
| Interrupted labor | [Director FL-03](https://github.com/BordelonDevOps/DecenniumDescent/blob/596aa5c8/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_DIRECTOR_BOOK.md#L41): generic interrupted progress remains while physically feasible; actual loss can undo it. This concerns work progress, not an implied quantity of liquid already moved. |
| Material accounting | [EC-03](https://github.com/BordelonDevOps/DecenniumDescent/blob/596aa5c8/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EX58_SOURCE_CONTRACTS_CORRECTED.md#ec-03--physical-lots-supply-and-daily-support) requires conserved constituent identity, nested custody, exact amounts, compatible openings and retained clocks. It does not assign filling’s debit/credit timestamp. |

The equipment guide’s **one-hand consumable-use** default is not a filling rule. Moving liquid between containers does not itself consume it.

**There is a concrete completion-boundary precedent**

In [`integrated_flow.json`](https://github.com/BordelonDevOps/DecenniumDescent/blob/596aa5c8/DescentReviewChanges/ReviewBible/data/public/expedition_candidate/integrated_flow.json):

- `/lighting/refills/0` records `refill-1` over **108000–108060**, with **two hands** for the refiller. Its method includes opening, pouring and securing the flask.
- `/lighting/transfers/2` records `pour-A-1`, moving one pint from `flask-2` to `Lantern-A`, at **108060**, the completion endpoint.
- `/nextProcurement/waterFilling` assigns 28 skins to four workers, seven minutes each, but gives no interrupted-fill or intermediate-liquid state.

Thus **completion-time transfer and two-handed work have reviewed example support**. That lantern example does not establish a universal rule that every interrupted skin fill moves zero liquid, retains a particular fraction, or requires restarting.

**Recommended completion for owner decision — NEW, unadopted**

For the first bounded ordinary-water filling profile, I recommend:

1. **At start:** declare an immutable quantity and specific source/destination; reserve that source quantity and destination capacity. Do not yet debit source contents or credit destination contents.
2. **Work:** require one capable worker, two usable hands and feasible access/support for **60 active seconds**. Include ordinary opening, pouring and securing within that minute, following the lantern precedent. Retrieval and subsequent handover remain separate operations.
3. **Pause:** retain completed feasible labor and the job’s material/capacity reservations; release the worker’s unused labor/hand bookings. No liquid has transferred under this proposed abstraction. Resume the same job toward its original 60-second requirement.
4. **Completion:** after applying relevant endpoint events and revalidating eligibility, atomically subtract the declared quantity from the source and add the traced constituent quantity to the destination. This is a **transfer, not consumption or nutrition credit**.
5. **Cancellation:** release remaining reservations and close the job without moving liquid. Preserve elapsed labor and actual world changes. No automatic spill, refund of time or restoration of damaged contents. Save/resume preserves progress and reservations exactly.

This keeps feasible progress consistent with the general work rule while choosing an explicit liquid commitment boundary. A progressive-pour model is also possible, but would need separately adopted throughput, partial-transfer and interruption semantics. **Neither model is already mandated by FL-05.**
