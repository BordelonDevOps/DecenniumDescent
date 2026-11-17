# TAC-10 genuine Dash through combat exit

The missing post-exit Dash boundary now passes on the unchanged corrected C# build. An actual paid hero Dash survives seal suppression, recovered Claw attacks, enemy defeat, paid combat closure, resource management and continued exploration. Retrying that historical command after exit returns Duplicate without charging again; a fresh Dash request is unavailable. This checkpoint does not accept TAC-10 or replace the five-path, compatibility or final-review gates.

## Exact execution bindings

- Runtime: `c8ffee78d5047131317ff923c8e3a575b6c51f3a`; the passing build is `engine/artifacts/ferry-wraith/dash-correction/run-20261117T110451175Z-06a69ef8`.
- Seal/Dash and post-exit drivers: `6cffd7b1e8f7a0b0662847a4a83a705a73e86cf7`.
- Unchanged continuation driver: `e744c04a35cfb94e0f77207e3f35610b77b9868b`.
- Executions: `seal-with-dash-20261117T113456Z`, `dash-closure-20261117T113827Z`, and `after-exit-20261117T114454Z`, under the same local `dash-correction` directory.
- The collector checks all 468 compilation inputs, exact committed/executed driver bytes, report bindings and three runtime DLLs against the [retained corrected build](public-dash-checkpoint/RETENTION.json). No additional compilation is claimed.

## Connected commands and persistence

The authentic first-fire input is revision 351, SHA256 `6a69b36f95e4435705fb175030f7f16aebbfa76bb0752168af65f321d7ab2687`. Fifteen normal public commands tear the physical seal, pay hero Dash on the otherwise unused Start 3 Action, advance through suppression and reach the recovered Claw at revision 366. The original seal expiry remains `344093/2`; the recovered attack deals the actual rolled 3 fire damage. Dash is command `ferry.exit.dash.356`, receipt revision 357, with the exact current turn token. It changes neither clock nor RNG.

The unchanged continuation then submits 97 commands: actual party attacks and two paid Healing Rites, enemy death, paid closure at revision 438/time `344205/2`, ordinary movement, retrieval of the previously dropped owned club, and further exploration. Final revision is 463/time `344239/2`; hero HP is 14/26, companion HP is 18/18 and companion Resonance is 3/7. This is a separate branch containing one additional Dash receipt; it does not replace or alter the original revision-462 main continuation.

Seven selected save/restored pairs are byte-identical. The input/output bindings between all three executions also match. The continuation actually exercises corrupt-primary/valid-backup recovery and retains the displaced three corrupt bytes. Final save SHA256 is `71420605e7a45a2168fac7f1c2dd7a6bacf142242261a6aab5f91d827b185dd8`.

## Actual post-exit controls

The final input has no active encounter, is outside InventoryCombat and retains the defeated source. Its historical Dash command is reconstructed from the real persisted receipt. These normal public requests all preserve authoritative snapshot bytes, revision 463 and the final clock:

| Request | Query | Submit |
| --- | --- | --- |
| Authorized exact historical Dash | AlreadyCommitted | Duplicate |
| Fresh ID after combat | FerryDashRequiresPartyCombat | Unavailable |
| Same ID with conflicting target | CommandIdConflict | CommandIdConflict |
| Exact retry after Player revocation | NotAuthorized | NotAuthorized |
| Exact retry from FerryOpponent | Not queried | NotAuthorized |

The executed driver additionally asserts that the post-exit Player command view and discovery offer no fresh Dash. The report retains the query/response objects above; the view/discovery exclusions are executable assertions, not separately serialized view snapshots. There is no private execution or injected state: reflection reads snapshots only. Final saves before/after the probes and after strict restore equal the original input. No new command or resource payment is committed by these controls.

## Retention and review scope

[RETENTION.json](after-exit-checkpoint/RETENTION.json), [MEMBERS.json](after-exit-checkpoint/MEMBERS.json), and [the archive](after-exit-checkpoint/after-exit.zip) retain 33 members, 652343 compressed bytes, SHA256 `0f56834782b9d7fa5f16649ea85e6fc706dc4101806f3ae2fb5d8aee018f0605`. The collector reopens and rehashes every member. Collector SHA256: `19dc54746bc97e6d6d933eb2f0750c1aacc5024586ca5a6576825bef3ff68498`.

Actual GPT Press/knockout response `4e4fd14a-c98a-5752-9d4a-ef0c90b315c0` and Codex agreement are retained in [GPT_PRESS_KNOCKOUT_REVIEW.json](GPT_PRESS_KNOCKOUT_REVIEW.json). That review finds no bounded execution blocker and explicitly allows the disclosed generic query/discovery omissions in this slice. They remain unfinished reusable-engine API capabilities; public pending views and normal Submit work. No complete discovery or autonomous pending knockout handling is claimed. GPT inspected source and reconciled retained artifacts; it did not compile, execute gameplay/causal restores or observe workers live.

The corrected 1,584-case regression remains the original run `72f6bdda13924fad8eb5b516ec19018b`; this checkpoint does not claim its terminal outcome. Full consumer reconciliation, required ability/boundary controls, authentic 95–113 saves, all five paths and actual final GPT/Codex agreement remain mandatory. No successor is authorized. Whole-engine, P1 and production completion remain open; Unity integration, storage cleanup and GitHub Support remain deferred or on hold.
