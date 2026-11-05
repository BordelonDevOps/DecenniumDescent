# Manufacturing control query and discovery — 2026-11-05

## Scope

This C# increment exposes the already implemented Pause, Resume, and Cancel manufacturing commands through shared pure query assessment and same-revision command discovery. The assessment is shared with the existing resolver; the resolver still performs work-ledger changes, cancellation settlement, AwaitingCheck completion, saved clock continuation, and receipt creation. Working orders expose Pause/Cancel; Paused and AwaitingCheck orders expose Resume/Cancel when the resolver's checks allow them. AwaitingChoice retains only its existing quality/catalyst choices and rejects controls. Tactical discovery includes admissible owner controls even when another actor owns the active slot, matching existing resolver behavior.

The authoritative state remains `ManufacturingOrderRecord`, `WorkLedger`, `ManufacturingAdvanceRecord`, snapshot persistence, and command receipts. No costs, lifecycle rules, schema fields, or new settlement behavior were added.

## Acceptance

- Working → Pause and Paused → Resume preserve the existing retained-work and paid-labor semantics.
- Cancel follows the existing input/packaging settlement and is idempotent on replay.
- Pure queries expose zero immediate costs and do not change the snapshot.
- Save/restore reconstructs the same command options and preserves command replay protection.
- AwaitingCheck keeps the existing worker-capability gate; AwaitingChoice blocks controls with the existing rejection code.
- Tactical owner controls are discoverable and queryable while another actor owns the active turn.

## Validation

- Four focused manufacturing acceptances passed **1/1 each**. Their full receipts are included here.
- The full headless suite compiled Core, Persistence, LabModel, and test sources with C# 9 warnings as errors, then reported **1,119/1,127 passed**. Its eight failing schema42 harvest cases and exact exceptions match the preceding saved baseline; this increment adds one passing case. The failures originate while validating fixed harvest manifests against donor anatomy, before manufacturing code runs. See [the preceding baseline](../2026-11-05-open-activity-view/HEADLESS_RESULTS.json) and [the current run](HEADLESS_RESULTS.json).
- Static package checks passed **14/14**.
- No Unity Editor, Edit Mode, Play Mode, build, or gameplay check was run during this C# increment.

`HEADLESS_RESULTS.json` and focused receipts retain test outcomes and source hashes. `PACKAGE_RESULTS.json` retains the static package checks. Generated `engine/artifacts/` files remain ignored build output.
