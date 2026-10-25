# Rank8 Resource6 recheck for Codex

**Verdict: the delivered return requires correction. Do not accept or apply it.**

Authority remains **689 reviewed/applied, 159 pending, zero accepted-unapplied**, with 413 complete accepted reviewed standalone procedures. This recheck concerns only spell-absorption-shield, resonance-nullification, resonance-furnace, resonance-matrix, resonance-mastery and leyline-flow. No applied cohort, feat, canonical index or catalog was changed.

All six proposed procedures, all 24 conference and six original identity question dispositions, all eight future obligations, all 57 case containers and their 536 events were inspected. The 30 questions already have explicit answers; this handoff does not ask the user to answer them again. Eleven case branches retain their existing holds. Six confirmed defect categories and five verification/coverage gaps are detailed below. They overlap: 23 case containers have a confirmed defect; 28 are referenced by at least one finding. This is a finite package review, not a guarantee that no further defect can exist.

## Integrity that passes

The original ZIP is 34,967,175 bytes, SHA-256 `e4f640bbbda6ef51217ddcdaf90328ddaffe358c119e7b49c0d7814d4fc60919`. All 154 archive members are canonical; 153 are bound by the self-excluding manifest. ZIP central directory, CRC, exact member set and every member SHA-256 pass. No hidden/temp members are present in that ZIP.

Fresh, independent data checks pass 9,623 structural assertions, including all 536 before/after state hashes, continuity, 2,144 event forward/inverse test/replace operations, six proposed catalog-operation round trips, and mirrors. Another 300 source/coverage assertions and 146 price arithmetic checks pass. Price arithmetic uses recorded eligibility flags; it cannot establish whether those flags are legal when concentration or geometry is wrong. The original package's 16,886 validation claims are retained as historical return data, not treated as a semantic correctness certificate.

Exact native cards/access rows, selected Wizard cards, source records, original questions and comparisons match the bound source packet. The candidate remains 929,673 bytes / `d9c56f0c29e980deffda422857b7ebd76c888ceb091bd027a71ebd38902cb3f0`; the source archive remains 3,271,044 bytes / `c99aaaa456709f3f7b78fbfdff6f5ada0eeb15d7969addd4a189ead4e0237dca`. The newly attached DOCX has historical spell-slot wording and is preserved separately, without replacing live source authority.

## Confirmed defects and verification gaps

### D01 — Live concentration effects remain after their owner concentration is cleared

Classification: confirmed-defect.

Thirteen concentration-dependent applications in ten case containers have ended=false but their actual owner concentration is null. The first contradictory transition is listed for each application in CONCENTRATION_FINDINGS.json. Later effects must not be treated as operative solely because the application row remains present. Furnace denied-credit additionally omits the damage concentration save after this erroneous clear.

Required repair: Repair only the incorrect source/owner transition. Application or replacement on one recipient must not clear an unrelated actor concentration. A genuine ending must mark the exact application ended and clear only its actual owner link. Reconcile every affected downstream before/after state, missing concentration roll, mirror and reversible operation. Add an explicit bidirectional concentration/application invariant.

Cases: `RR142-FURNACE-A/denied-credit-spends-allowance`, `RR142-MATRIX-A/native-well-kindle`, `RR142-MATRIX-A/null-plus-later-charge`, `RR142-MATRIX-A/protected-and-mandatory`, `RR142-NULL-A/conduit-late-denial`, `RR142-NULL-A/known-conduit-denial`, `RR142-SHIELD-A/mirror-priority`, `RR142-SHIELD-A/suppression-and-expiry`, `RR142-SHIELD-B/free-cast-no-credit`, `RR142-SHIELD-B/shared-root-two-recipients`

### D02 — Mirror-priority setup bypasses mandatory Shield interception

Classification: confirmed-defect.

A has an operative 100-unit Shield at 0.2. B casts beneficial rank-3 Soul Mirror on A at 1.1, but event 6 creates Soul Mirror without intercepting that incoming initial recipient branch. Under the proposed Shield procedure, beneficial ordinary spells are automatically eligible. With no prior Mirror, Shield must intercept Soul Mirror before it can attach. The later claimed reflected Arcane Bolt is therefore not established by this history.

Required repair: Retain the selected mandatory beneficial-spell rule. Establish a source-qualified history in which both wards can actually coexist before testing their priority, or hold the entire claimed coexistence/return branch. Do not silently exempt Soul Mirror. Also explicitly establish that the chosen returned payload falls within LR-G14 ordinary-spell scope; do not infer that scope from a generic class-power name.

Cases: `RR142-SHIELD-A/mirror-priority`

### D03 — Two voluntary moves end in occupied spaces

Classification: confirmed-defect.

RR142-MASTERY-B event 8 moves A to [20,0,0], already occupied by E. RR142-MATRIX-A/ready-inside-leave event 7 moves B to [25,0,0], already occupied by F. Both narratives call the movement lawful/clear. All actors remain present and alive.

Required repair: Choose and document a legal unoccupied route/end position within the real movement budget. Preserve the intended inside-to-outside field comparison and actual spell range. Account for difficult terrain if passing through nonhostile occupied spaces. Update only dependent states/quotes/outcomes.

Cases: `RR142-MASTERY-B`, `RR142-MATRIX-A/ready-inside-leave`

### D04 — Five native support deadlines use the wrong clock

Classification: confirmed-defect.

The two Conduit instances record 60.2 rather than the tenth future caster start at 60. Influence records 61.2 and 67.2 in MASTERY-A rather than 61 and 67, and 64.2 in MATRIX protected-and-mandatory rather than 64. These accepted support cards retain regular-start clocks. The NEW absolute-60-second rule is scoped to the six Rank8 identities. Well correctly records 61 and is not an error.

Required repair: Use each native source deadline exactly. Correct the five application deadlines in every affected full-state copy/mirror, preserving original phase, source ID and event time. Do not globally convert accepted support clocks to absolute application+60.

Cases: `RR142-MASTERY-A`, `RR142-MATRIX-A/protected-and-mandatory`, `RR142-NULL-A/conduit-late-denial`, `RR142-NULL-A/known-conduit-denial`

### D05 — Limited uses are not committed atomically with their casts

Classification: confirmed-defect.

Nine Leyline cast-commitment after-states have RP/action/cadence spent and a committed cast with its counter window open, while all three LeylineReceipt flags remain true. A separate event 0.01 seconds later consumes them. The Well and Kindle casts similarly leave their own native creation/use flag unspent at cast commitment. Labels asserting atomicity do not make these separate full-state transitions atomic.

Required repair: Commit each required use/reservation in the same logical test/replace transition as action, payment and cast beginning. Alternatively encode a genuinely indivisible transaction boundary with no exposed counter window until completion. Preserve countered-use loss and all existing no-refund choices. Update subsequent states/inverses consistently.

Cases: `RR142-LEYLINE-A`, `RR142-LEYLINE-A/countered-receipts`, `RR142-LEYLINE-A/depleted-but-possessed`, `RR142-LEYLINE-A/late-nullification`, `RR142-LEYLINE-A/overflow-and-lower-reference`, `RR142-LEYLINE-A/shield-intercepts-one-recovery`, `RR142-LEYLINE-B`, `RR142-LEYLINE-B/distinct-later-recipients`, `RR142-MATRIX-A/native-well-kindle`

### D06 — Two resolved misses retain committed status in the final cast record

Classification: confirmed-defect.

RR142-NULL-A and RR142-MATRIX-A each record an actual Arcane Bolt miss in their final ledger, while the same cast status remains committed. The three Ready releases flagged by the broad diagnostic were inspected: their damage resolves in the release event, so they are not being reported as missing outcomes.

Required repair: Set the two affected final cast lifecycle records to the actual resolved-miss result in the resolution event and dependent state copies. Do not reroll or change attack/HP/resource outcomes.

Cases: `RR142-MATRIX-A`, `RR142-NULL-A`

### G01 — Area geometry and body-volume anchoring are not fully bound

Classification: verification-gap.

SHIELD-B places B at [5,0,0] with A [0,0,0] and C [10,0,0], then claims both in one 15-foot Burning Hands cone without an origin/orientation/template proof. Other Burning Hands traces also omit a complete area footprint. Separately, the NEW Matrix test requires positive-volume body intersection, but foot plus bodyFeet does not state whether horizontal foot coordinates are body center or a corner, nor give explicit bounds. C at x=10 on a radius-10 boundary can change eligibility with that interpretation.

Required repair: Bind actual cone origin, direction, dimensions and complete affected-body set. Specify the fixture coordinate convention/body bounds and source-specific membership computation as a local data convention. Use legal placements that demonstrate the intended branch. Do not claim the current opposite-side cone is valid merely because scalar range checks pass.

Cases: `RR142-MATRIX-A/null-plus-later-charge`, `RR142-MATRIX-A/protected-and-mandatory`, `RR142-SHIELD-B`, `RR142-SHIELD-B/free-cast-no-credit`, `RR142-SHIELD-B/shared-root-two-recipients`

### G02 — Evocation area exclusion is omitted from all three area-cast traces

Classification: verification-gap.

The actual W16 source includes the Evocation school passive: exclude one creature from the initial damaging area; it automatically succeeds and takes no damage if success normally halves. None of the three Burning Hands traces declares the excluded creature or reconciles that selection with Shield interception and remaining damage.

Required repair: Record the actual native school-passive selection and its exact timing/recipient result in every area case. Explain how it interacts with the existing Shield branch contract using spell-local authorship if genuinely missing; do not silently remove the acquired passive or infer an unsupported waiver.

Cases: `RR142-SHIELD-B`, `RR142-SHIELD-B/free-cast-no-credit`, `RR142-SHIELD-B/shared-root-two-recipients`

### G03 — Conduit late-denial Ready lacks an established perceivable trigger

Classification: verification-gap.

The declared Ready trigger is B commits Conduit transfer. The source transfer creates a debit/pending ledger but supplies no intrinsic visible/audible commitment cue. This case records no actual communication or sensory event for D at that checkpoint. Generic Ready requires a perceivable trigger and responds after it happens. A database commitment alone does not establish perception.

Required repair: Bind a genuine permitted observable trigger and exact post-commit/pre-credit interruption window, preserving speech/action/cadence. If the supplied sources cannot establish that window, retain the whole late-interrupt branch as conditional rather than claiming a real completed interruption.

Cases: `RR142-NULL-A/conduit-late-denial`

### G04 — Temporary-HP grants lack explicit current grant provenance

Classification: verification-gap.

Three Harmonic Bulwark resolutions assign a scalar tempHP=25 without a current grant/source link or recorded native long-rest/depletion/replacement endpoint on that buffer. Cast history exists, so the numerical offer is traceable by reconstruction; the current state does not itself identify which magical grant owns the surviving buffer for suppression, replacement and ending.

Required repair: Record the exact retained temp-HP grant identity, original source/cast, amount/remaining balance, suppression state and native ending rule. Preserve the actual 25-point offer, paid-base calculation and losses; do not convert it into prevention or a second bank.

Cases: `RR142-FURNACE-A/tempHP-funded`, `RR142-LEYLINE-A/depleted-but-possessed`, `RR142-SHIELD-A/capacity100`

### G05 — Some distinct authored boundaries are asserted without a discriminating full-state trace

Classification: verification-gap.

No case demonstrates a genuine multi-hit initial recipient payload absorbed once in full; no Furnace case crosses an epoch boundary after spending the prior PB cap to prove the next-epoch reset; no Matrix case discriminates mere surface contact from positive-volume overlap. The known-Conduit-denial branch starts C at full 60/60 RP and names no positive amount, so it fails the native missing-RP gate independently of Nullification and does not isolate that selected restriction. These are case coverage gaps, not unanswered source questions. All 11 existing held branches remain held.

Required repair: Add only minimal source-qualified data traces for these selected rules, using actual accessible native profiles. Preserve source/physical holds where facts are absent. Give known-Conduit denial a genuinely missing-RP recipient and legal positive amount if it is meant to isolate Nullification. Do not ask the user to answer the already selected 30 dispositions again.

Cases: `RR142-FURNACE-A/shared-epoch-replacement`, `RR142-MATRIX-A`, `RR142-NULL-A/known-conduit-denial`, `RR142-SHIELD-A`

## Scope of the handoff

The original return ZIP and delivery JSON are included byte-exactly under `original/`. They have not been silently replaced or corrected. Every finding remains open. This handoff ZIP is an audit/repair packet, not a corrected Director return and not an acceptance receipt. It contains data and source evidence only; the fresh audit scripts used to inspect bytes/JSON are not supplied as runnable deliverables. No supplied/historical program or game runtime was executed. No runtime, human-play, balance, cosmology, release or domain-closure approval is made.

Read `CODEX_HANDOFF.md` for the exact requested repair boundary, `FINDINGS.json` for machine-readable findings, and `CASE_REVIEW_MATRIX.json` for all 57 case dispositions. A case with no additional finding is not thereby accepted. Preserve existing holds; do not turn a held operand into a campaign event.

Direct Codex delivery was attempted through the available connected-browser route, which returned “Browser control was not allowed.” No message or artifact has been confirmed sent to an external Codex session. This packet is ready for that handoff.
