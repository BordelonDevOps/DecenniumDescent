# Decennium Descent — Part 5 copied-feat integration review 01

## Verdict

**CHANGE REQUIRED for the delivered reference integration.** The seven accepted bounded copy contracts and CRS01–03 source choices are retained. Five concrete reference-code/integration findings require **11 full-value operations across four Python files**. The exact proposed copies are supplied and tested in isolation; they have not been applied to a project or GitHub.

**Full Ready, including the proposed cross-round allowance transaction, remains unimplemented both before and after these corrections.** This review does not claim whole335-feat approval or a new ordinary spell acceptance. The owner-supplied applied baseline remains **525 reviewed /323 pending /249 standalone /173 interfaces**;39 accepted-but-unapplied spell identities remain independent of this review.

## Evidence and source precedence

All three requested nested originals match their owner-supplied byte counts/SHA256 values and their actual bytes inside handoff03. Their42/49/66 manifest sources produce **157 verified source-member records and78 unique source paths**. Every overlap is byte-identical, including the common capture, quote, payload and contract files. No competing code version was silently selected.

The complete native CRS01–03 decision/addendum, FS08/FS09/SUP07 contract, actual source-component adapters, acquisition providers, release/payload/class code, their validators/fixtures and relevant imported interfaces are the basis of the review. Complete source files remain in the original input archives. References below bind file bytes and function lines; JSON references bind full pointers in `FINDINGS.json` and `PROFILE_DISPOSITIONS.json`.

The four feat-rule JSON baselines match the exact originals in corrections01. Its13 feat-rule operations remain **proposed and uninstalled**; the prior complete22-operation package is preserved unchanged. Its existing copy Ready choice is copied in full in `evidence/PROPOSED_COPY_READY_DECISION_UNCHANGED.json` and in the Ready matrix. The full Control15 return02 is preserved as actual separate authority, including its now-completed Mental Prison review and its exact conditional Dance terminal. No obsolete pending label reopens that conference. No Control operation is newly applied here.

Companion05 and Illusion13 exact acceptance archives are preserved byte-identically, including all accepted artifact bytes they contain. No one of those artifacts is changed. Source-only status labels such as the release report's historical Shaman/Mirrorsage opening and the class report's historical pending delivery/Ready discussion remain original history; current bounded evidence/disposition is recorded externally.

## Five findings and proposed corrections

### CFI-01 — Echo capture and actual class Reaction were separate budgets

**Classification:** REFERENCE_INTEGRATION_DEFECT.

**Original behavior:** For the same actor, Echo capture decrements CopyCaptures.reactions only. A linked Shaman still has reactions=1, and the Mirrorsage shared action pool still has reaction=True. The old package tests do not test this interaction.

**Proposed correction:** Bind capture to the supplied existing counted Shaman or Boolean Mirrorsage Reaction field before any turn/capture history. Read and debit that same field; query current body/world Reaction legality. Binding never refills or merges histories. A real regular start refreshes, an extra turn does not.

**Boundary:** Eldritch Echo capture Reaction only. Mimicry still consumes no Reaction. No additional Reaction, general scheduler or class-specific capture entitlement is granted.

Primary source: `DescentReviewChanges/ReviewBible/tools/feat335_copy_capture.py` → `CopyCaptures.capture`, lines105–157. Complete supporting source references and exact operation spans are in the JSON records.

### CFI-02 — Reconstructing an adapter with the same canonical ledger resets its local cap

**Classification:** REFERENCE_STATE_OWNERSHIP_DEFECT.

**Original behavior:** An adapted Mend can be committed, then a second CopyPayloadReleases on the same owner/captures/RP/cadence/world/concentration can commit another in the same numbered round because release_rounds is freshly empty. The reproduced RP sequence is44→42→40.

**Proposed correction:** Register one copy engine per owner on the supplied canonical concentration ledger, after successful constructor validation. Reject additional direct/payload/class wrappers using it; reuse the original adapter and its receipts. A failed pool/world constructor does not reserve an owner.

**Boundary:** This is a finite adapter invariant, not serialization, reload recovery or protection against a caller supplying a different falsely labelled canonical ledger. Persistent authoritative owner identities remain a runtime requirement.

Primary source: `DescentReviewChanges/ReviewBible/tools/feat335_copy_release.py` → `CopyReleases.__init__`, lines142–149. Complete supporting source references and exact operation spans are in the JSON records.

### CFI-03 — Postcommit native body/concentration changes were ignored

**Classification:** REFERENCE_LIVE_STATE_DEFECT_WITH_RETAINED_ADAPTER_GAP.

**Original behavior:** The existing class commitment validates native Shaman state, but payload resolution later relies only on the copy-world snapshot. Actual body unconscious after commitment still permits Mend30→32. Direct native concentration displacement after Ward commitment still grants4temporaryHP while native and bridge burdens disagree.

**Proposed correction:** At resolution consult the actual linked body conscious/canAct state in addition to existing world eligibility; a blocked paid payload consumes no RNG and refunds nothing. Before payload/counter cleanup and world-clock mutation, run the bridge existing validate_current() and reject unintegrated concentration drift without overwriting it.

**Boundary:** No automatic synchronization, unknown-source cleanup, actor death transition or general concentration solver is implemented. Rejected concentration drift must be reconciled by the actual source adapter. V/S already performed at commitment are not re-required at payload time.

Primary source: `DescentReviewChanges/ReviewBible/tools/feat335_copy_payloads.py` → `CopyPayloadReleases.resolve`, lines209–237. Complete supporting source references and exact operation spans are in the JSON records.

### CFI-04 — True linked Shaman Step moves only one position view

**Classification:** MISSING_WORLD_POSITION_ADAPTER_GUARD.

**Original behavior:** With actual native totem at5ft and native caster at0, a legal copy-world teleport to[-15,0,0] leaves native caster at0. Native aura querying still qualifies the old5ft relation instead of reflecting the20ft separation.

**Proposed correction:** Fail closed before any commitment/payment for Step specifically when using ShamanConcentrationBridge. Do not guess a mapping from 3-D CopyWorld position to the native scalar position/aura model.

**Boundary:** This blocks an unsupported reference integration path, not the printed Step benefit or Shaman eligibility. All seven bounded contracts remain. The original Shaman/step fixture uses the unlinked finite class pool and remains a valid coordinate-only test; Mirrorsage coordinate-only Step remains likewise limited.

Primary source: `DescentReviewChanges/ReviewBible/tools/feat335_copy_payloads.py` → `CopyPayloadReleases._payload`, lines239–316. Complete supporting source references and exact operation spans are in the JSON records.

### CFI-05 — An extra-turn ID could be reused as a regular-start ID

**Classification:** REFERENCE_EVENT_ID_INVARIANT.

**Original behavior:** start_extra rejects regular and extra history, but start_regular checks only regular_turns. A closed extra-turn event can be replayed as an alleged new regular start, updating ordinal and refreshing Reaction.

**Proposed correction:** The existing regular-start validation also rejects IDs already present in extra_turns, before mutation. Distinct lawful regular and extra events remain legal.

**Boundary:** Defensive identity consistency in the finite timeline. It does not authenticate arbitrary caller assertions of actual turns or supply an extra-turn source.

Primary source: `DescentReviewChanges/ReviewBible/tools/feat335_copy_capture.py` → `CopyCaptures.start_regular`, lines66–78. Complete supporting source references and exact operation spans are in the JSON records.

These changes are enforcement/adapter corrections, not new spell designs. CFI-04 is especially an **implementation guard**, not a new prohibition on Shaman using a legitimately acquired Step copy. The printed personal movement benefit remains due when its actual canonical world adapter exists.

The full observed before/after states for seven adversarial scenarios covering these five findings are retained under `tests/results/*_full_probes.json`, with a portable reproducer. In the identical submitted-operand native-unconscious probe, the proposed resolver rejects stale supplied damage/healing RNG; the separate47-test suite also completes the legally blocked no-RNG result with no heal or refund. This is not automatic handling of every native death/concentration transition.

One additional exploratory observation was deliberately **not** turned into a correction: capture ceiling through a temporarily suppressed but still owned feat credential. Permanent acquisition/learnable-ceiling evidence and current release availability are not the same. The release path already checks operative availability; these sources do not justify inventing a new active-at-capture provider rule.

## Seven profile dispositions

| Profile | Retained scoped behavior and remaining limits |
|---|---|
| Strike | Native Arcane Ray/Lifedraw damage component; own attack; captured numeric bound; no extra critical dice or copied riders. Supplied Core and finite defense pathways are exercised, not every interceptor. |
| Burst | Burning Hands native component; declared point/maximum three original recipients; one bounded damage pool; independent DEX outcomes; later eligibility does not permit retargeting. |
| Mend | Actual eligible Lifedraw healing component; willing living recipient; normal-HP/Critical/prohibition/reducer rules; no revival, Wound cure, resource conversion or external dice benefit. CFI-03 checks later linked caster state. |
| Ward | False Life native component; actual single temp-HP grant ledger; rejected offer wastes the copy; original second future source START and concentration dependency. Unintegrated native concentration drift is rejected, not guessed. |
| Hindrance | Actually expressed Slow component; WIS, Speed−10 and no new Reactions; strongest-slow arbitration and earlier bounded future endpoint; no original hard control or repeat-save rider. |
| Boon | Shield supplies the implemented AC variant only, with strongest copy-family arbitration and source next future END. Printed next-attack and next-save variants remain genuine unimplemented source/consumption adapters. |
| Step | Actual Mist Step teleport supplies only bounded coordinate movement under conditional legal geometry. Original nonteleport movement remains required and open. True linked Shaman pose integration now fails closed before payment instead of leaving native aura queries at the old location. |

`PROFILE_DISPOSITIONS.json` preserves every full profile and the complete common contract, not this summary alone. Native source identity controls chronological family; profile name, capture ID, feat permission or ability route does not replace it. q and bounded native magnitude retain their exact source rules. No critical amplification, proc, secondary rider, resource engine, protected feature or recursive copy permission is added.

## Actual class/provider assessment

The Shaman and Mirrorsage providers use their actual class source files, paid acquisition receipts, Base selections and repertoire evidence. Shaman retains WIS and its actual learnable ceiling; Mirrorsage retains INT and its actual ceiling; an independently paid rank-zero Blast route remains CHA/q0 without inventing an RP pool. No Wizard matrix or unrelated class benefit is substituted. Full training/hero/campaign acquisition histories remain the explicitly disclosed premises, not authenticated live events.

The true linked Shaman test uses the same actual RP/cadence/Action account and paid totem. A feat copy receives no ordinary Shaman vent; a later real ordinary Shaman spell can receive its own valid vent. A lasting copy ends the real prior totem at commitment before a counter result; counter does not restore it. Bloodcaller source restrictions do not delete an independently acquired CHA rank-zero feat route. The new Reaction binding fixes the previously separate capture budget; the new body/concentration/pose guards limit situations the original positive fixtures did not exercise.

The Mirrorsage tests use the actual shared EchoLedger allowance in both directions: feat first can block a later class-bound release, and an actual class summon/command/payment boundary can block the feat copy. An adapted repeated copy uses normal feat strain/Refrain, with no first class-Echo release waiver, and a countered commitment still spends the cap. These tests preserve a genuine prior-record premise: they do not execute complete class Mirrorbind/capture or the full class Echo strain/payload procedure. CFI-01 adds the missing actual capture Reaction debit; CFI-02 prevents a new wrapper on the same canonical ledger from creating a new owner cap.

## Full case/history dispositions

All **19 release histories,27 payload histories and22 class histories** were reviewed and replayed from the original source. Each complete historical object equals the archived object, including the source witnesses/acquisition fields or additional class evidence. Each has an individual disposition and reason below and in `CASE_DISPOSITIONS.json`. The full proposed replay objects are retained beside them; snapshot binding metadata is not silently substituted for history.

The original cases remain coherent at their stated conditional inputs. That does **not** mean the integrated code is accepted as-is: the five adversarial findings expose cases not sampled by those original histories. `resolved=True` in a processed miss, prohibited heal or rejected buffer is not a claim that the requested hit/heal/grant succeeded.

### Release histories

| Full case ID | Disposition and source-specific assessment |
|---|---|
| `seven-profile/strike` | **Retain, scoped.** Actual captured strike commitment preserves its paid source/rank/provider and source-specific concentration tag. This is commitment evidence only, not recipient execution. |
| `seven-profile/burst` | **Retain, scoped.** Actual captured burst commitment preserves its paid source/rank/provider and source-specific concentration tag. This is commitment evidence only, not recipient execution. |
| `seven-profile/mend` | **Retain, scoped.** Actual captured mend commitment preserves its paid source/rank/provider and source-specific concentration tag. This is commitment evidence only, not recipient execution. |
| `seven-profile/ward` | **Retain, scoped.** Actual captured ward commitment preserves its paid source/rank/provider and source-specific concentration tag. This is commitment evidence only, not recipient execution. |
| `seven-profile/hindrance` | **Retain, scoped.** Actual captured hindrance commitment preserves its paid source/rank/provider and source-specific concentration tag. This is commitment evidence only, not recipient execution. |
| `seven-profile/boon` | **Retain, scoped.** Actual captured boon commitment preserves its paid source/rank/provider and source-specific concentration tag. This is commitment evidence only, not recipient execution. |
| `seven-profile/step` | **Retain, scoped.** Actual captured step commitment preserves its paid source/rank/provider and source-specific concentration tag. This is commitment evidence only, not recipient execution. |
| `counter/ward` | **Retain, scoped.** The ward lasting-copy commitment replaces prior concentration before its actual counter result, without refund or restoration. Recipient execution is supplied separately by the payload slice. |
| `counter/hindrance` | **Retain, scoped.** The hindrance lasting-copy commitment replaces prior concentration before its actual counter result, without refund or restoration. Recipient execution is supplied separately by the payload slice. |
| `counter/boon` | **Retain, scoped.** The boon lasting-copy commitment replaces prior concentration before its actual counter result, without refund or restoration. Recipient execution is supplied separately by the payload slice. |
| `actual-adapted-chronology` | **Retain, scoped.** The actual pending copy followed by adapted use shares the underlying family and normal Refrain; permission changes do not reset strain. Owner adapter reuse must obey CFI-02. |
| `actual-different-profile-same-source` | **Retain, scoped.** Lifedraw Strike versus Mend remains one feat-copy source family, not separate profile families. |
| `actual-different-source-same-profile` | **Retain, scoped.** Distinct native sources do not merge simply because both map to Strike. |
| `ordinary-quotation-boundary` | **Retain, scoped.** The ordinary quote/history comparison is valid; this fixture does not execute a full ordinary cast or payload. |
| `Wizard-independent-strain` | **Retain, scoped.** The explicit feat strain contract applies without a prepared-matrix first-use waiver. |
| `counter-outcome-never-rewinds-history` | **Retain, scoped.** Countered paid commitment does not restore RP, consumed permission, cap, Refrain or displaced concentration. |
| `actual-feat-only-route` | **Retain, scoped.** Actual paid rank-zero Blast credential uses CHA and invents no class rank ceiling or RP pool. |
| `rank0-Fractured-history` | **Retain, scoped.** Rank-zero copy remains legally quoted under its zero base/surcharge treatment while chronological family history is retained. |
| `actual-route-change-retains-chronology` | **Retain, scoped.** Changing actual owned ability route does not reset a native source family. |

### Payloads histories

| Full case ID | Disposition and source-specific assessment |
|---|---|
| `Strike-critical-bound` | **Retain, scoped.** A genuine critical attack has the captured numeric cap and no added critical copy dice; actual Core critical classification still reaches Core damage handling. |
| `Strike-miss` | **Retain, scoped.** The attack misses, so no damage dice or Wound operands are consumed. Adapter resolved=True means processed, not that a hit/effect succeeded. |
| `invalid-RNG-retry-no-repayment` | **Retain, scoped.** Malformed RNG is rejected before recipient mutation; retrying the same paid cast does not repay or allow a second completed result. |
| `Strike-zeroHP-critical` | **Retain, scoped.** Core zero-HP/critical handling is exercised using explicit actual roll inputs; not a second damage root or numerical-balance conclusion. |
| `Strike-Wound-and-zero` | **Retain, scoped.** The bounded damage traverses the supplied Core Wound/zero-HP path without replacing canonical LifeState. |
| `Strike-fatal-Wound` | **Retain, scoped.** A fatal Core Wound consequence follows the supplied Wound/Injury dice, not an imported monster-death rule. |
| `Burst-three-recipient-shared-roll` | **Retain, scoped.** One bounded native pool applies through three independent eligible DEX save outcomes; no fourth recipient or reroll per target. |
| `Burst-late-cover` | **Retain, scoped.** Later loss of the original area-to-body line of effect removes that recipient without retargeting or repayment. |
| `Burst-binary-save` | **Retain, scoped.** Binary success/failure defense resolves before the specified half/no-damage outcome; no invented intermediate save degree. |
| `Damage-defense-order` | **Retain, scoped.** The finite typed immunity/resistance and strongest flat reduction path remains valid; no wider vulnerability/interception coverage is inferred. |
| `Mend-Critical-cap` | **Retain, scoped.** Actual Critical ordinary-healing caps apply after bounded output and source reducers; no Wound cure or maximum reset. |
| `Mend-prohibited` | **Retain, scoped.** Actual HP-gain prohibition prevents restoration; processed result is not evidence of a positive heal or resource conversion. |
| `Mend-reduction` | **Retain, scoped.** Supplied ordinary reducers/systemic factors apply without feat dice addons, resource hooks or source-specific next-heal consumption. |
| `Mend-living-zero` | **Retain, scoped.** A genuinely living zero-HP recipient can receive the permitted bounded normal heal; this is not revival of an actual dead creature. |
| `Ward-concentration-cleanup` | **Retain, scoped.** A real accepted temporary-HP dependency is removed by its own lost concentration. |
| `Ward-rejected-4` | **Retain, scoped.** The actual single-grant ledger rejects the equal/weaker offer as recorded; the paid copy is wasted and grants no stacked buffer. |
| `Ward-rejected-6` | **Retain, scoped.** The existing stronger grant remains; processed copy resolution is not acceptance of the offered buffer. |
| `Ward-deadline` | **Retain, scoped.** The existing original second-future-regular-start deadline ends the actual dependency without reset. |
| `Ward-to-other-caster-damage` | **Retain, scoped.** A later distinct caster damage packet spends the real recipient buffer before normal HP under the supplied Core path. |
| `real-buffer-displaced-before-counter` | **Retain, scoped.** Replacing concentration deletes the real old copy buffer before the new counter outcome; counter does not restore it. |
| `Hindrance-arbitration-and-cleanup` | **Retain, scoped.** Speed−10 uses strongest-slow arbitration; no new Reactions is source-local; cleanup preserves unrelated records. |
| `Hindrance-ordered-end-expiry` | **Retain, scoped.** Future target END and second source START produce the earlier exact bound, excluding an in-progress regular end as disclosed. |
| `Boon-multiowner-arbitration` | **Retain, scoped.** Multiple AC copy boons use strongest family arbitration rather than stacking magnitudes; owners retain independent sources. |
| `Boon-end-boundary` | **Retain, scoped.** Source next-future-regular-END timing is retained. This tests the Shield-derived AC variant only. |
| `Step-no-body-or-passenger-copy` | **Retain, scoped.** The caller-qualified Mist Step coordinate update transports no other actor. It does not simulate physical support, Falling, cargo, world observers or native Shaman aura synchronization; CFI-04 bounds the true linked path. |
| `late-invalid-target` | **Retain, scoped.** No new target is chosen when the original target becomes ineligible; paid costs remain and no payload RNG is consumed. |
| `lost-concentration-before-payload` | **Retain, scoped.** An actual integrated concentration callback ends the pending lasting payload. CFI-03 additionally guards native changes that did not traverse that callback. |

### Classes histories

| Full case ID | Disposition and source-specific assessment |
|---|---|
| `Shaman/strike` | **Retain, scoped.** Actual Shaman acquisition, paid ASIs/Base/repertoire qualification and strike payload use its own ability/ceiling and finite resource account; no Wizard substitution or class waiver. The original history used Mimicry and therefore did not test Echo capture spending the shared class Reaction; CFI-01 covers that separate failure. |
| `Shaman/burst` | **Retain, scoped.** Actual Shaman acquisition, paid ASIs/Base/repertoire qualification and burst payload use its own ability/ceiling and finite resource account; no Wizard substitution or class waiver. The original history used Mimicry and therefore did not test Echo capture spending the shared class Reaction; CFI-01 covers that separate failure. |
| `Shaman/mend` | **Retain, scoped.** Actual Shaman acquisition, paid ASIs/Base/repertoire qualification and mend payload use its own ability/ceiling and finite resource account; no Wizard substitution or class waiver. The original history used Mimicry and therefore did not test Echo capture spending the shared class Reaction; CFI-01 covers that separate failure. |
| `Shaman/ward` | **Retain, scoped.** Actual Shaman acquisition, paid ASIs/Base/repertoire qualification and ward payload use its own ability/ceiling and finite resource account; no Wizard substitution or class waiver. The original history used Mimicry and therefore did not test Echo capture spending the shared class Reaction; CFI-01 covers that separate failure. |
| `Shaman/hindrance` | **Retain, scoped.** Actual Shaman acquisition, paid ASIs/Base/repertoire qualification and hindrance payload use its own ability/ceiling and finite resource account; no Wizard substitution or class waiver. The original history used Mimicry and therefore did not test Echo capture spending the shared class Reaction; CFI-01 covers that separate failure. |
| `Shaman/boon` | **Retain, scoped.** Actual Shaman acquisition, paid ASIs/Base/repertoire qualification and boon payload use its own ability/ceiling and finite resource account; no Wizard substitution or class waiver. The original history used Mimicry and therefore did not test Echo capture spending the shared class Reaction; CFI-01 covers that separate failure. |
| `Shaman/step` | **Retain, scoped.** Actual Shaman acquisition, paid ASIs/Base/repertoire qualification and step payload use its own ability/ceiling and finite resource account; no Wizard substitution or class waiver. This seven-profile fixture is not the actual paid-totem Shaman engine. Its coordinate-only result remains valid; it does not close the linked native-position integration gap. The original history used Mimicry and therefore did not test Echo capture spending the shared class Reaction; CFI-01 covers that separate failure. |
| `Mirrorsage/strike` | **Retain, scoped.** Actual Mirrorsage acquisition, paid ASIs/Base/repertoire qualification and strike payload use its own ability/ceiling and finite resource account; no Wizard substitution or class waiver. The original history used Mimicry and therefore did not test Echo capture spending the shared class Reaction; CFI-01 covers that separate failure. |
| `Mirrorsage/burst` | **Retain, scoped.** Actual Mirrorsage acquisition, paid ASIs/Base/repertoire qualification and burst payload use its own ability/ceiling and finite resource account; no Wizard substitution or class waiver. The original history used Mimicry and therefore did not test Echo capture spending the shared class Reaction; CFI-01 covers that separate failure. |
| `Mirrorsage/mend` | **Retain, scoped.** Actual Mirrorsage acquisition, paid ASIs/Base/repertoire qualification and mend payload use its own ability/ceiling and finite resource account; no Wizard substitution or class waiver. The original history used Mimicry and therefore did not test Echo capture spending the shared class Reaction; CFI-01 covers that separate failure. |
| `Mirrorsage/ward` | **Retain, scoped.** Actual Mirrorsage acquisition, paid ASIs/Base/repertoire qualification and ward payload use its own ability/ceiling and finite resource account; no Wizard substitution or class waiver. The original history used Mimicry and therefore did not test Echo capture spending the shared class Reaction; CFI-01 covers that separate failure. |
| `Mirrorsage/hindrance` | **Retain, scoped.** Actual Mirrorsage acquisition, paid ASIs/Base/repertoire qualification and hindrance payload use its own ability/ceiling and finite resource account; no Wizard substitution or class waiver. The original history used Mimicry and therefore did not test Echo capture spending the shared class Reaction; CFI-01 covers that separate failure. |
| `Mirrorsage/boon` | **Retain, scoped.** Actual Mirrorsage acquisition, paid ASIs/Base/repertoire qualification and boon payload use its own ability/ceiling and finite resource account; no Wizard substitution or class waiver. The original history used Mimicry and therefore did not test Echo capture spending the shared class Reaction; CFI-01 covers that separate failure. |
| `Mirrorsage/step` | **Retain, scoped.** Actual Mirrorsage acquisition, paid ASIs/Base/repertoire qualification and step payload use its own ability/ceiling and finite resource account; no Wizard substitution or class waiver. This remains a coordinate-only step, not a complete physical world transition. The original history used Mimicry and therefore did not test Echo capture spending the shared class Reaction; CFI-01 covers that separate failure. |
| `Shaman/actual-totem-copy-then-ordinary-vent` | **Retain, scoped.** The same actual Shaman RP/cadence/Action account and paid totem are used. The feat copy gets no vent; the later qualified ordinary Shaman spell uses its own actual vent. Native position must remain synchronized; the historical test did not include CFI-04 Step. |
| `Shaman/totem-counter/ward` | **Retain, scoped.** The actual paid totem burden is ended at the new lasting copy commitment; counter creates no replacement effect and restores no totem. CFI-03 guards later external concentration changes, not present in this fixture. |
| `Shaman/totem-counter/hindrance` | **Retain, scoped.** The actual paid totem burden is ended at the new lasting copy commitment; counter creates no replacement effect and restores no totem. CFI-03 guards later external concentration changes, not present in this fixture. |
| `Shaman/totem-counter/boon` | **Retain, scoped.** The actual paid totem burden is ended at the new lasting copy commitment; counter creates no replacement effect and restores no totem. CFI-03 guards later external concentration changes, not present in this fixture. |
| `Shaman/Bloodcaller-retains-independent-feat-only-route` | **Retain, scoped.** The transformed source state disables ordinary ranked casting but does not delete the independently paid CHA rank-zero feat credential or invent Wizard access. |
| `Mirror/mutual-cap/feat` | **Retain, scoped.** A feat copy consumes the actual shared EchoLedger allowance and prevents another class-bound release in that numbered round. Prior real-record premise is preserved; no full Mirrorbind/capture/strain/payload implementation is proved. |
| `Mirror/mutual-cap/class-boundary` | **Retain, scoped.** The actual creature summon/command/payment/shared-cap boundary consumes the original shared allowance so the later feat copy cannot commit. The prior class-record qualification remains a premise. |
| `Mirror/repeated-copy-no-class-waiver-countered-cap` | **Retain, scoped.** The adapted repeat uses normal feat Refrain without class first-release waiver; countered repeat still consumes the actual shared cap and payment. |

### Seven Ready-lifecycle histories and thirteen source acceptance examples

Every Ready-lifecycle profile history is retained as **paid-preparation-premise-only** evidence. The helper shows a single concentration burden transitioning to the exact immediate/lasting result. It supplies neither real payment nor the actual legal Reaction/trigger or round-cap transaction.

All13 original CRS acceptance examples and complete prior expectations/dispositions remain in the case register. CRS03-B and CRS03-C now have the later actual Shaman and Mirrorsage finite source-code evidence rather than the release-only report's earlier opening; that does not close full providers/world runtime. CRS01-A still does not execute two Echo captures across a real beneficial rest with varying same-source class ranks. CRS01-C remains a quote/history boundary, not a full ordinary-spell transaction. CRS02-D is not promoted to full Ready support.

## Exact Ready gap

The proposed Ready choice is already explicit: preparation occupies its round's applicable feat and actually owned Mirrorsage allowances and pays RP/components/capture permission/strain/history once. Same-round release reuses its own preparation tokens. Later-round release must atomically check/spend its own round's applicable caps and actual Reaction, without a second payment/counter/history transaction. The real trigger finishes first; release selects current legal targets or geometry. Original Ready and earlier capture deadlines remain. No partial debit follows an invalid/declined/cap-blocked release, and no reload or extra turn refreshes identity or consumed receipts.

None of that complete transaction is implemented by the delivered or proposed code. `CopyReleases.commit`/`ClassCopyCommit.commit` are direct Action paths. `CopyPayloadReleases.declare` freezes direct-cast selection at declaration, and `resolve` properly forbids changing that paid direct selection. `CopyConcentration.committed(ready=True)` assumes prior payment; `release_ready(actual_legal_release=True)` assumes the very legality that a full engine must establish. They cannot be exposed as a complete Ready API by setting a Boolean.

`READY_GAP_MATRIX.json` identifies12 missing integration areas with their exact supplied-code boundary and required proposed-source behavior. The capture Reaction fix is not a release Reaction transaction. The one-adapter invariant is not persistence. The two-round feat-copy allowance rule does not apply to ordinary Ready or class Echo by association.

## Tests, source verification and limits

The unmodified release/payload helper suites reproduce **136 and115** checks. The class suite initially fails the hardcoded `C:/Github/DecenniumDescent` source locator on this host. After an explicitly documented **in-memory path-only rebinding**, it reproduces **205** checks. Source bytes are not changed by this test relocation. Full original history/result/coverage fields match the frozen reports, not only their counts or IDs.

The proposed copies pass all **456 existing helper assertions**. The new isolated suite runs **47 tests, zero failures/errors** on the proposed code, including shared Reaction debits both directions, no refill on binding, genuine regular versus extra-turn refresh, body/source changes after payment, duplicate adapter rejection, atomic rejection before Step payment and source clock mutation, and event-ID reuse.

Against the original code, the same new post-fix invariant suite yields22 assertion failures and10 errors. Some errors are newly introduced guard APIs absent from the original; they are not32 independent gameplay defects. Five root findings are selected. The new tests and seven full adversarial probes are reproducible from the supplied source archives. No prior44 source-spec or prior Control53 tests are falsely counted as rerun here.

The independent read-only verifier separately passes **880 source/structural/full-value/reference/report-consistency checks** before the final return-manifest checks. It imports no project module. It verifies every full forward/reverse file reconstruction, all source bindings, complete histories/profiles, prior unchanged decisions and input/history archive member bindings. Source checks are not gameplay tests.

All Python executions here are isolated delivered/proposed reference-module tests. No running video-game client/server/world engine, human gameplay or numerical-balance test was executed. Fixtures supply actual source completion, geometry/perception/LoE, fit, roll facts and real regular/extra-turn assertions; these are not authenticated campaign events. Wider defense/interception, source-owned next-heal consumption, suppression/dispel/body-end, physics, save/load and class capture remain open.

## Retained external holds and next boundary

Keep Companion's `IN6-09-A`/`IN6-09-B` exact-CR2 Undead holds and Control's `EN5-01-A`/`EN5-01-B` operative-rating/native-profile holds plus `EN6-03-B` actual companion opposed-check hold. No owner-level rating, donor CR, save-PB-to-Athletics substitution or generated monster is introduced. Full Control15/Mental Prison has its separately completed exact substantive acceptance; those old semantic deferrals are not reopened here.

Creation, historical Mind Maze mid-resolution, other scoped conditional cases, full Ready/class/world runtime, human play/balance, cosmology,75-domain closure, whole-game completion and release remain separate. The unsent rank8 packet summaries are not reviewed. The delivered Rank8Damage6 and Rank7IdentityCasting5 conferences remain separate subsequent work.

## Complete code bindings and delivery

Exact operation spans, reasons and symbols are in `CODE_OPERATIONS.json`; complete source files are under `baseline/` and `proposed/`. Reuse accepted artifacts unchanged. The original correction package and complete prior receipts are included as exact archives, not reconstructed from these explanations.

| Repository filename under `DescentReviewChanges/ReviewBible/tools/` | Before bytes | Proposed bytes | Operations |
|---|---:|---:|---:|
| `feat335_copy_capture.py` | 11,062 | 14,023 | 3 |
| `feat335_copy_class_release.py` | 9,978 | 12,386 | 2 |
| `feat335_copy_payloads.py` | 22,515 | 22,991 | 4 |
| `feat335_copy_release.py` | 13,155 | 13,697 | 2 |

Full SHA256 bindings:

`DescentReviewChanges/ReviewBible/tools/feat335_copy_capture.py`

Before: `29b62bb38b61a8f0f774df98782dd3218f53f274a8945dc23d0f6f8cb6cbf8aa`  
Proposed: `29bde67328f494c5232766cabfca769f1c4f2e8e48d1e46852a8f266957a8315`

`DescentReviewChanges/ReviewBible/tools/feat335_copy_class_release.py`

Before: `80a571d5aa76d19d8c4dfb120ebf2bb96c73cd0848556320066d5ed584d183c1`  
Proposed: `6e3a161ff2820b975d1cdec2e64d3455d86f743c0f3de5149cd62e6745eac631`

`DescentReviewChanges/ReviewBible/tools/feat335_copy_payloads.py`

Before: `c53e48e9be34798f9053f07fa55e07169ec3117ad7fd7c8f6731074747455455`  
Proposed: `35e746cfe14b88073539eac763c063c5d05d630bc582ebd0c1187c6aba80f1e3`

`DescentReviewChanges/ReviewBible/tools/feat335_copy_release.py`

Before: `ce41ffeed640e95ba3fae6567002bea09cc646d21a6176a0f99539f7e8cb7f18`  
Proposed: `3ec8f82a4a5075a03fba28d1f08ade59275b343039efede4831940d8516086b8`


Read `CODEX_HANDOFF.md` for verification and new-directory-only staging. Any current working-tree drift requires full-source reconciliation rather than overwriting later work. This receipt preapproves no future canonical/index/registry bytes or engine adaptation. The root manifest binds all return members except itself, and the external SHA256 sidecar binds the finished ZIP.
