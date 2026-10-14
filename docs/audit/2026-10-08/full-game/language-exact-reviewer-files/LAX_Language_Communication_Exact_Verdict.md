# LAX-EXACT-2026-10-11 — language/communication exact verdict

**Internal exact-candidate review. CONDITIONAL ACCEPT after LAX-01–03.** The complete first submission is not accepted unchanged. Three finite corrections are sufficient; no new general language source conference is required. This is authored-language approval only, not class, spell, feat, runtime, human-trial, balance, expedition or whole-game approval.

## Submission and actual inspection

Archive: `DD_Language_Communication_Exact_Review_v1.zip`; **12,859,675 bytes**; SHA256 **788e1210d28120b5e94a6ddc4d1dcc69e48a2aeb7cfd60f434c9680b30fa2ec1**. All **184 payloads** match `FILE_MANIFEST.json`. All **152 original payloads** and all **14 manifested final source-reviewer files** remain byte-identical to their supplied manifests. The manifest itself is the185th archive entry.

I read the README and manifest, the whole public chapter, all32 worked sequences and the complete internal language application/interface manuscript. Both full JSON envelopes were parsed and their complete relevant subtrees compared, not sampled. Semantic inspection covered every new ordinary language rule and all49 selected/called class interfaces,23 spell comparisons, eight pending feat comparisons, all grant/alias/dialect/mode/choice mappings, the eight record contracts and all32 chronological adjudications. The full40 internal Scribing cards,28 exact public Scribing objects and19 current advanced procedure sections were compared to their actual completed source records; those completed crafting gates were not reopened. Original class records/engine contexts, ancestry procedures, condition/Core/component rules and the actually called Heaven's Decree supplied the governing scope.

The supplied read-only source validator reproduced **460/460** checks, including the selected-source/book/route and reference comparisons. The candidate validator was inspected and run in a separate working copy: **492/496 passed**, with all four failures limited to missing player-chapter link targets. Its **38 executable reference arithmetic/boundary checks passed**. The frozen local all-pass report is retained as historical evidence; its navigation result is not reproducible from this self-contained ZIP. This discrepancy does not establish that its author fabricated the result: those paths may exist in the larger working repository.

An additional independent read-only audit gives **705/711**: the same four missing links plus the two authored consistency problems below. This is overlapping verification, not711 extra independent semantic claims. After applying only the named proposed changes in a reviewer-local working copy, the candidate suite reproduces **496/496**, and **44 focused checks pass:30 static/source comparisons and14 executable reference-contract fixtures**. All32 sequence dispositions below are semantic assessments of authored examples, not executed gameplay passes. These working-copy results do not constitute the owner's fulfillment receipt or change submitted source bytes.

No in-scope candidate or selected controlling record was unreadable. The four missing files are navigation destinations, not missing class/recipe mechanics; replacement links can use the complete public collections already supplied. Large preserved source books/catalogs were used as selected controlling evidence and checked for preservation, not reopened for an unrelated whole-book or whole-game approval.

Paths below are relative to the archive root. `B` means `DescentReviewChanges/ReviewBible` and `A` means `docs/audit/2026-10-08/full-game`. Exact machine-applicable replacement values and original matching paragraphs are in `LAX_CORRECTIONS.json`.

## LAX-01 — Correct the self-contained reading path

**Affected:** `B/docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md`, “Class features and Paladin oaths” (submitted line171) and “Scribing, runes and devices” (line193); the full `/guideText` in `B/data/playtest/language_communication_candidate_public.json`; the regenerated validation/fulfillment record.

The links target absent `CLASS_PLAYTEST_INDEX.md`, `PALADIN_OATHS_AND_OATHBREAKERS.md`, `SCRIBING_CANDIDATE_RECIPE_CARDS.md` and `TINKERING_CANDIDATE_RECIPE_CARDS.md`. Keep the actual complete class and advanced records already in the archive. Replace the two paragraphs as follows:

> Use each acquired feature's complete source card for acquisition and operation. The [selected language interfaces](../../data/playtest/language_communication_candidate_public.json) identify the applicable card IDs without granting them; the included [Paladin cards](../../data/public/class_playtests/paladin.json) supply the oath procedures. The other selected full class collections remain under `data/public/class_playtests/`, with Bard in `data/public/Decennium_Descent_Bard_Playtest_v0_1.json`. These language completions retain every card's existing status.

> The reviewed [advanced operating guide](ADVANCED_CRAFT_CANDIDATE_GUIDE.md), [Scribing cards](../../data/crafting/advanced_craft_recipe_candidate_public.json) and [Tinkering cards](../../data/crafting/advanced_craft_recipe_candidate_public.json) retain their authority. The two card links open the supplied complete public advanced-crafting collection; use the actual recipe ID within it. Reading words does not establish a functional magical payload, caster eligibility or device control.

Resolve all12 active link occurrences from the corrected three-manuscript tree. The Scribing and Tinkering links intentionally open the same complete existing public advanced-crafting JSON, containing the actual recipe IDs. This introduces no private index or new mechanical source. Preserve the original all-pass report and issue a new version-bound report for the actually tested self-contained tree. Update `/guideText` to the entire corrected public manuscript, not a separately maintained summary.

## LAX-02 — Make provenance value presence conditional

**Affected:** both language JSON envelopes, `/recordSchema/definitions/provenance`; the LA-15 application annotation in the internal guide/data; `B/tools/validate_language_candidate.py`'s record-contract assertion; focused LA-T31 contract coverage. Original source objects and the settled LA-15 wording remain unchanged.

The submitted contract universally requires `sourceSpelling` while simultaneously saying it is present only when the source field is present. An absent background field cannot satisfy both. Replace the mandatory list with:

```json
["sourcePath", "sourceSha256", "recordId", "fieldPresence", "authority"]
```

Keep `sourceSpelling` as a declared conditional field. Its complete controlling wording is:

> For `fieldPresence: "absent"`, omit `sourceSpelling` entirely. For `fieldPresence: "null"`, require `sourceSpelling: null`. For `fieldPresence: "value"`, require the exact original non-null JSON value, including an empty string, array or object. Do not substitute a canonical spelling or language ID. Source-path/hash/record/authority evidence must still identify the actual source; satisfying this shape alone does not authenticate it.

The exact replacement object, including five constraints, is in the correction register. All other seven record definitions remain intact. The generic validator must no longer assert that every declared provenance field is universally mandatory. Replace only its named loop as specified, retain the other seven mandatory-field assertions, and exercise the conditional value cases—not merely a looser subset assertion.

The fourteen focused reference fixtures cover absent/omitted acceptance; absent/null and absent/empty rejection; null/null acceptance; null/omitted and null/empty rejection; original-value acceptance; empty string/array/object preservation; value/omitted and value/null rejection; canonical-spelling substitution rejection; and JSON boolean-versus-number distinction. The five actual absent background Languages fields remain absent. No save migration or field-normalization repair is authorized.

## LAX-03 — Restore TI-04's actual scope and noncombat action

**Affected:** the public chapter's “Scribing, runes and devices” paragraph beginning “A crafted device requires” (submitted line205); both `/rules/deviceControl` objects; public `/guideText`; the internal LA-14 clarification; and LA-T30 in `A/LANGUAGE_CANDIDATE_WORKED_ADJUDICATIONS.json`, both `/workedAdjudications` arrays and the worked-sequence manuscript.

The actual completed **TI-04/05/08 and TD-01** distinguish controlled automata from the other24 TI mechanical objects. The submitted blanket sentence incorrectly assigns automaton binding, Bonus Action command and attached-phase execution to every crafted device. It also lacks TI-04's outside-initiative **Action start** for an already programmed wholly noncombat task. The original advanced cards and section objects are correct and must not change.

**Exact replacement player wording:**

**TI-04 controlled automata, not all crafted devices.** A TI-04 automaton requires an actual capable consenting controller with INT 6+ and ten active minutes using actual Tinker's tools at its legitimate accessible interface to register that controller and one compatible simple task. No proficiency is granted or required merely to use a known functioning interface. A previously bound chassis requires actual release by its controller or a separately completed lawful control procedure; ownership does not hack unknown, locked or hostile equipment. A controller may have three active ordinary crafted automata; separately defined special profiles and class devices keep only their own actual limits and exceptions. Traps, manually operated utilities and operator-driven machinery do not acquire this binding or attached-phase protocol merely because they are crafted devices. Use their own arming, direct-operation, activation and servicing procedures.

**In initiative**, an eligible automaton command requires a Bonus Action on the controller's regular turn, the configured visible/audible channel within 60 feet, and the actual shared one-command/one-offensive-companion-or-device allowance per owner per numbered round. Execution follows that controller's whole turn in the attached phase. Failed execution spends committed allowances; transfer, rebinding and extra turns do not refund them. Other item families retain every shared budget that their own controlling procedures expressly apply; this scope correction waives none.

**Outside initiative**, programming or reprogramming one such automaton's actual finite, physically possible noncombat task takes ten active minutes. Do not charge a second programming period for the unchanged task validly registered during initial binding. Starting one already programmed, wholly noncombat task uses an Action, not the combat Bonus Action command. Actual appendages, access, capacity and paid power/service intervals remain necessary. No professional work, autonomous attack, indefinite production or service reset follows from a program or language lesson. Fluency, an interpreter or a telepathic ally supplies neither control authority nor undocumented hardware. Service, repair and controller transfer remain separate and preserve their real histories, costs, HP, charges and custody.

**TD-08 is a separate class-device permission, not limited by this automaton-command scope.** It retains once per short rest, a Bonus Action, and up to two current Dissonance into one own active qualifying device within 30 feet. The completed source's actually armed charged trap, powered automaton, utility in a live eligible task, or aligned operator-driven device can qualify on its own terms. Merely carrying an idle item does not. Keep the original routing disable, clearance, service and resource histories; no class feature is granted here.

The exact replacement `/rules/deviceControl` object records this scope, three ordinary active automata, initial task registration included in binding, ten-minute programming/reprogramming, initiative versus noncombat actions, native limits and unchanged histories/budgets. It deliberately contains no private membership list.

**Internal identity mapping, not a new public list:** ordinary TI-04 automata are **586,587,589,590,593,594,596,600,607,608,611,612,615,616,618,620,622,684**; **686** invokes it only through its own completed special profile. Traps **585,588,592,598,599,601,605,609,610,613,619**, utilities **591,595,597,602,603,604,606,614,617,621,623,685**, and direct-operator **687** do not inherit that generic automaton protocol. All numbers have the `recipe-` prefix. Their original source-specific actions and expressly shared offensive budgets still apply.

LA-T30 must name actual **recipe-684**, rather than an undifferentiated device. Retain the ten-minute genuine controller registration and nonreset histories; regular-turn Bonus Action/shared round20 allowance; attached-phase resolution without refunds; and rejection of a second command or invented telepathic receiver. Add the distinct finite noncombat program/Action-start context, contrast actual manual591 and trap585, and retain TD-08 separately. The replacement complete case object and exact rendering instructions are in the correction register; its original checklist expectation and `runtimePassed:false` stay unchanged.

**Boundary outcomes:** recipe591 requires actual compatible direct work and its utility charge, not a remote automaton command. Recipe585 retains one-minute placement followed by an arming Action/delay and its real trigger/offensive-allowance rule. Recipe687 retains its three distinct direct-operator wind/align/discharge Actions, not an attached companion attack. A newly registered unchanged simple automaton task does not incur a second ten-minute programming fee. Servicing, repair, rest, controller transfer and language learning neither substitute for one another nor reset costs, uses, power or custody.

## LA-01–16 application verdicts

| Direction | Disposition | Exact assessment |
|---|---|---|
| LA-01 | KEEP | Actual 14 base grants; Troll keeps Giant, Mycelian keeps its evidenced regional choice, and Mira gains no Battlefield Medic language. |
| LA-02 | KEEP | Only explicit aliases combine. General Primordial and four dialects remain independent competencies; matching-affinity choice is one grant. Runic and the distinct deep-language labels are not merged. |
| LA-03 | KEEP | All 45 variants retain base-plus-literal-addition behavior; only High Elf and Imperial Human add a language choice. Separate communication traits remain separate. |
| LA-04 | KEEP | Permanent shorthand, actual literacy/script modes, written-only competencies and current physical communication capacity remain distinct. No extra anatomy or temporary-to-permanent conversion. |
| LA-05 | KEEP | Fixed duplicates union actual modes with provenance, without refunds; choices obey their own restriction. Five absent background Languages fields remain absent. |
| LA-06 | KEEP | 320/280-hour full courses, 80/40-hour literacy, 15-minute credited phases, real Tongues loss, actual tuition, occupied tutor time and deterministic included completion implement the settled NEW course. |
| LA-07 | KEEP | Known translation, evidence-limited recognition, eight-hour supported deciphering and formula/Insight procedures remain distinct; Core outcomes and new-evidence retries do not invent meaning. |
| LA-08 | KEEP | Six-second aggregate ordinary communication, real ordered interpretation and ten-minute/six-cue rehearsal do not create off-turn Actions, fluent signing or retroactive receipt. |
| LA-09 | KEEP | Deafened, Silenced, the narrower Silence the Caster, own audible V, other components, overlapping restrictions and source-specific concentration are kept distinct. |
| LA-10 | KEEP | Eight operative spell comparisons and actual ancestry communication/recharge procedures are preserved; Message has no automatic translation/reply and Speak with Dead keeps separate paid inquiries and its clock. |
| LA-11 | KEEP | All fifteen pending spells retain operational:null, their exact source status and existing question IDs; no borrowed procedure or promotion. |
| LA-12 | KEEP | All 48 selected class interfaces plus the called Heaven's Decree match the settled language directions and complete source cards. Bounded semantics, Echo Voice, Hush Descends, temporary donor modes and oath windows are language-layer decisions only. |
| LA-13 | KEEP | All eight pending feat originals remain comparisons, not active benefits, courses, proficiency grants, reductions or telepathy implementations. |
| LA-14 | CORRECT LAX-03; otherwise KEEP | Scribing, Rune and TD-08 boundaries stand. Scope ordinary TI-04 control/attached-phase behavior to its automata and expressly invoking special profiles; retain noncombat Action start and other device families' native procedures. |
| LA-15 | CORRECT LAX-02; otherwise KEEP | All originals, aliases, migration boundaries and eight contracts stand. Make sourceSpelling conditional on actual absent/null/value state; do not fabricate a value to satisfy required fields. LAX-01 completes the reading path. |
| LA-16 | KEEP — RECEIPT ONLY | Literal names, published restrictions and exact deferred questions remain archived without interpretation or an ordinary-language enrollment grant. No setting or cosmology approval. |

## All32 exact checklist dispositions

These are bounded authored judgments of the actual supplied sequences. “KEEP” does not certify a running companion implementation or actual table/campaign facts. LA-T01–29 need no chronological rewrite; the shared navigation correction still applies to their supporting chapter. LA-T30 is replaced; LA-T31 keeps its history with the corrected contract; LA-T32 keeps its audience/receipt outcome with corrected navigation.

| Case | Disposition | Assessment |
|---|---|---|
| LA-T01 | KEEP | Base traits, not population-table descriptions, control Troll/Mycelian/Deep Dwarf and Mira; no retroactive extra grant. |
| LA-T02 | KEEP | The Imperial Human/Seeker example correctly supplies Common plus four choices; all14/45/20 source mappings remain. |
| LA-T03 | KEEP | Orc/Orcish and Mycelic/Sporetongue normalize only in derived views; the Mycelian ancestry label does not. |
| LA-T04 | KEEP | General Primordial, its four dialects and similarly named distinct languages do not confer one another; one affinity choice stays one. |
| LA-T05 | KEEP | Recognizable Dwarvish characters do not supply Gnomish/Orcish semantics; written competencies do not invent speech. |
| LA-T06 | KEEP | Knowledge persists through Deafened/Silenced states; current sensory/voice access still controls actual delivery. |
| LA-T07 | KEEP | Duplicate fixed grants provide no compensation, while an actual unspent choice may select an eligible unsatisfied competency/mode. |
| LA-T08 | KEEP | Closed options, region/affinity premises, secret restrictions and source-field absence remain actual constraints. |
| LA-T09 | KEEP | A qualified instructor/curriculum, usable channel and authentic practice are prerequisites; money, one inscription or Insight alone supplies none. |
| LA-T10 | KEEP | 320/280 hours and40/35gp full-course reference tuition, plus80/40-hour literacy modules, reconcile without discounts from pending feats. |
| LA-T11 | KEEP | Forty actual minutes interrupted in phase three give30 credited minutes and a single9cp invoice. A real ten-minute Tongues loss remains a separate debit. |
| LA-T12 | KEEP | No course/Insight/research/rest overlap or artificial concentration break; tutor and learner time remain occupied. |
| LA-T13 | KEEP | Translate only the actual known or sufficiently evidenced text; no high roll reconstructs nonexistent meaning, missing cipher key or protected content. |
| LA-T14 | KEEP | The declared Core project check, bounded outcome, spent work and genuine new-evidence/method retry remain native to that route. |
| LA-T15 | KEEP | Four seconds plus two exhaust the same round's ordinary allowance; an extra turn does not refresh it. |
| LA-T16 | KEEP | Three-second reception then three-second rendition delivers meaning at second six, never second two; rehearsed cues still require actual perception. |
| LA-T17 | KEEP | Deafened does not itself stop own audible V; Silenced cannot be evaded by mental speech; the named combat restriction remains V-Reaction-only. |
| LA-T18 | KEEP | Independent prohibitions keep independent expiry; playback cannot supply the caster's V and ordinary nonauditory concentration is not automatically ended. |
| LA-T19 | KEEP | Actual perception/touch,30ft, concentration, literal meaning and protected/cipher exclusions remain Comprehend Languages' own procedure. |
| LA-T20 | KEEP | Message creates no reply/translation. Each Speak with Dead inquiry uses its own Action/allowance even if uncomprehended; no new expiration clock. |
| LA-T21 | KEEP | Fungi one/long-rest, Orc animal speech from level3 one/day, and Gnome basic small-beast communication retain different sources and limits. |
| LA-T22 | KEEP | All15 pending spell procedures and exact queues remain isolated, not filled from titles or reviewed neighbors. |
| LA-T23 | KEEP | All49 selected/called class interfaces and their native statuses are retained; language review grants no card acquisition. |
| LA-T24 | KEEP | Receptive Tongues is not speaking; willing Echo Voice conceptual communication is not a V component, mind-reading or device receiver. |
| LA-T25 | KEEP | Only selected effects obtain the settled bounded-meaning bridge; Hush Descends' named acoustic completion is not universal Silenced or thunder immunity. |
| LA-T26 | KEEP | Knowledge Transfer expires with actual donor modes; Silent Smite's after-end and Vow Unbroken's since-beginning windows stay different. |
| LA-T27 | KEEP | No pending feat becomes active or changes the ordinary course. Linguist/Polyglot remain distinct and Prodigy retains its own eligibility question. |
| LA-T28 | KEEP | One genuinely new study at2 Insight reaches3; spend3 plus eight different hours for one supported passage. Copies/saturation create no later credit. |
| LA-T29 | KEEP | Zero-language references remain zero; readable letters do not establish a functional script or casting/Runecarver eligibility, and consultation is not added to casting. |
| LA-T30 | CORRECT LAX-03 | Replace the generic device fixture with actual recipe-684; distinguish combat Bonus Action from noncombat Action start and contrast native591 utility/585 trap use. TD-08 keeps its separate family scope. |
| LA-T31 | KEEP HISTORY; COMPLETE LAX-02 CONTRACT | The old-save sequence correctly preserves Common/Mycelian and unresolved choices. The record contract must also admit an absent value without fabricated sourceSpelling. |
| LA-T32 | KEEP AUDIENCE/RECEIPT; COMPLETE LAX-01 LINKS | The recursive public boundary and LA16 deferral are correct. Four absent navigation destinations must be replaced using supplied public collections before the complete reading path is accepted. |

## Accepted authored-language scope

Except for the exact changes above, KEEP the public chapter, all14 base/45 variant/20 background mappings, alias/dialect/script/mode/choice rules, ordinary learning and information-work procedures, communication/hearing/component rules, and the language-only dispositions of all49 class and23 spell comparisons. Keep the eight contracts with the LAX-02 correction, and the completed Scribing/Rune/device interface with LAX-03. All16 applications and all32 checklist cases have a finite disposition; no language source question is left as an invented new prerequisite queue.

The public envelope is appropriately bounded: it reuses exactly the28 completed public Scribing objects, not raw private projections. All40 full Scribing records and19 completed advanced sections remain internal evidence. Private/restricted Scribing membership, private control-profile membership, donor dossiers and latent metadata do not become player teaching content. Published literal names/restrictions are retained. LA-16 remains receipt-only, including Voice, Resonant Cant, deeper language relationships and other deferred terminology, with no interpretation or implied access.

The15 pending spells retain their original null procedures and actual queue IDs. The8 pending feats retain their complete originals and pending dispositions. All49 class source cards retain their exact statuses, acquisition, costs and nonlanguage rules; accepting this language layer neither promotes those cards nor grants them to a character. Completed crafting and NWX remain fulfilled without another crafting or onboarding conference. Recipe totals stay687/687 and433/433 public.

## Finite conditional fulfillment and permitted labels

The corrected language candidate may receive **reviewed authored language/communication playtest** status, without another generic source conference or another review of unchanged language text, when the following are proved against the actual corrected files:

1. Apply exactly LAX-01–03 to every named manuscript/data/schema/case location. Preserve the frozen v1, final source verdict/package, original152 payloads, original runtime arrays, class/spell/feat records, completed recipes/procedure sections and historical reports. Do not alter an original source to hide either discrepancy.
2. Reproduce the existing source and candidate suites, changing only the provenance assertion as prescribed, and reproduce all44 focused checks with their stated scopes. Retain all38 original executable arithmetic/boundary checks. Validate the32 actual complete sequence objects/manuscript renderings, full public envelope, source statuses and private exclusions, not just counts or effect snippets. The existing matrices and all unmodified assertions must survive.
3. Record corrected file hashes, actual validation outputs, application locations and this conditional authority in a version-bound fulfillment receipt. Distinguish static/reference checks and authored semantic outcomes from gameplay execution. The reviewer-local proposed-copy evidence is supporting evidence, not that owner receipt.
4. Only after those pre-label checks pass, normalize the language candidate's own review labels and, if used, its top-level `exactLanguageApproval` flag. Keep the original source-direction `exactApprovalGranted` values, all source class/spell/feat/recipe statuses, `classSpellFeatPromotion:false`, `runtimeImplemented:false`, `humanBalanceApproved:false` and `wholeGameFlowApproved:false`. Preserve a before/after label-only proof and final hashes. Update stale language-review-pending prose only within that scoped label normalization, not into a whole-game completion claim.

No new review of unaffected sources is required to satisfy these conditions. A deviation from the named correction wording requires review only of that actual deviation and its affected interface, not another blanket preliminary conference. No particular missing source blocks this ordinary authored-language gate. A specific course still needs its real instructor/curriculum and access; a passage its genuine meaning/evidence; and a feature/device its actual acquisition, controller/channel, state and permissions. Those operational premises cannot be supplied by a passing local test or invented boolean.

**Current submitted v1: not accepted unchanged. Corrected scope: conditionally accepted under the finite authority above.** No card/catalog promotion, gameplay-runtime certification, human teaching/balance pass or actual campaign authentication is issued here. DD-01, remaining catalogs, bestiary/expedition/Director integration, companion implementation and final systemic whole-game flow remain open. No deletion, GitHub push or cosmology review occurs. The owner's final joint whole-game flow confirmation precedes an authorized push; verified remote commit precedes careful cosmology review.
