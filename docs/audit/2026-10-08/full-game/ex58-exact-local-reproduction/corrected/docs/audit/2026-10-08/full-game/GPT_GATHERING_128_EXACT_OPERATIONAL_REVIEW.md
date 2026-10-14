# Exact gathering-tool verdict: conditional approval of all 128 cards

**The complete handoff has been inspected. Only two guide carry-through corrections, GEX-01 and GEX-02, remain before promotion.** They restore already-settled rules to the active public/shared instructions. They do not reopen source authoring or change any recipe’s printed effect, ingredients, body, price, difficulty, hours or audience classification.

**After those corrections and the specified checks, all 128 candidates may be promoted under this verdict. No additional generic source conference or full 128-card resubmission is required solely for these fixes.**

:chatgpt-content-reference{index="0"}[Complete standalone verdict](sandbox:/mnt/data/DD_Gathering_128_Exact_Operational_Verdict.md) · :chatgpt-content-reference{index="1"}[Exact proposed correction patch](sandbox:/mnt/data/DD_Gathering_128_GEX_01_02.patch) · :chatgpt-content-reference{index="2"}[Reviewer evidence and all-128 coverage](sandbox:/mnt/data/DD_Gathering_128_Reviewer_Evidence.zip)

The patch has been checked for applicability but **has not been applied** to the handoff or a repository.

## 1. Inspection and evidence

I opened `README_EXACT_REVIEW.md` and `FILE_MANIFEST.json`, both complete gathering JSON envelopes, every internal/public card manuscript, the body catalogues, active shared/trade/internal guides, controlling source directions and corrections, and the complete physical sequence casebook.

| Inspection | Result |
|---|---|
| Manifest-listed payloads | All **131** match their recorded byte sizes and SHA-256 hashes |
| Protected conference inputs | All **82** hashes match the included copies |
| Complete original recipe objects | All **128** match the included mechanical V4 originals at their recorded source indices |
| Public operational objects | All **82** equal their internal counterparts |
| Complete instantiated manuscript sections | All **128 internal + 82 public** match the inspected authoring text |
| Original book bindings | All **492 paragraphs** match the included DOCX at their recorded OOXML paragraph indices |
| Body projection | All **17 internal / 15 public** output models reconcile; shared public models are identical across audiences |

There was **no missing or unreadable requested gathering candidate file**. The source-book check included paragraphs inside tables; it was text/binding verification, not publication-layout approval.

I reran the supplied validators in an isolated scratch copy. They reproduced **777 source/register/manuscript checks, 824 guide/projection/arithmetic checks, and 67 worked-example numeric/coverage checks**, all passing. Separately, **1,700 per-card field comparisons** passed, and I independently recomputed all **5,600 supplied arithmetic rows**: 1,536 manufacturing rows, 544 structural inputs, 3,264 structural transitions and 256 quotations, with four additional exhaustive-membership checks.

The **27 worked examples, 14 additional risk dispositions, 17 body boundaries and eight joint seams** were assessed as conditional authored examples. Their dispositions are consistent with the governing directions, subject to the two guide corrections below. They are **not automated gathering-runtime passes or authentication of campaign facts**. The detailed results and per-card coverage are in the :chatgpt-content-reference{index="3"}[reviewer evidence](sandbox:/mnt/data/DD_Gathering_128_Reviewer_Evidence.zip).

This review is bound to the supplied archive:

```text
SHA-256: be4f30ad0ec44e34059849aed59271b6242664c5757758261f13194ff363be1f
```

## 2. Exact scope otherwise cleared

| Trade | Exact recipes covered | Audience counts | Effect coverage |
|---|---|---|---|
| Mining | `recipe-320–358`, `recipe-656–659` | 29 public / 2 restricted / 12 Director-only | A25/B13/C5; all printed effects and all 13 critical-only extraYield1 overlays |
| Skinning | `recipe-507–545`, `recipe-676–679` | 28 public / 2 restricted / 13 Director-only | A27/B12/C4; all printed effects and all 12 critical-only extraYield1 overlays |
| Salvaging | `recipe-433–470`, `recipe-668–671` | 25 public / 2 restricted / 15 Director-only | Six recovery groups: 13/11/6/6/3/3; no extraYield overlay |

The source requirements, body mappings, creation reserves, restoration references, consumption flags and catalyst mappings agree. Component accounting remains **580 occurrences = 193 Mining + 192 Skinning + 195 Salvaging**, with **213 nonconsumed tool rows and 367 consumed rows**, including the **12 consumed-tool rows and ten catalyst rows**. Duplicate fang and marrow occurrences remain separate. The Skinning tally erratum and both GI corrections take precedence over their preserved historical wording.

The substantive operating decisions need no redesign:

**Resolution and scope:** Core harvesting, binary dismantling without natural shifts, the separate total-20 precision qualification, six-band creation, and Core-to-binary restoration/preservation remain distinct. No route improperly inherits another’s assistant, time, XP or critical benefit.

**Matter and lifecycle:** Finite baseline/damaged/reserve allocations, original Fishing F/S partition and fallback, terminal claims, genuinely newly exposed Mining parcels, per-identity Salvaging percentages, nested assemblies and legitimate downstream manufacturing remain intact.

**Bodies and work:** All seventeen manual bodies retain their geometry, required tools, original primary members, actual lead operation, current-state checks, independent comparisons, weaker fallback and real receiving limits. Positive HP does not supply missing members or safe containment.

**Creation and restoration:** Ordered maximum reserves, included fifteen-minute incorporation, original work hours, B5/P0–25–50/flaw/damage-deficit handling and reference arithmetic remain intact. No artisan-only Forge Dwarf benefit, implicit upgrade route, free complete body, catalyst duplication or reverse dismantling is introduced.

**Quality:** Mineral dressing, hide/scale surface preparation and recovered-component preparation remain separate bounded operations. They do not change tier, value, Freshness or HP, and saturation grants no substitute reward.

In particular, recipe-322 still needs six complete pick reserves for Q4; blocked minerals do not become critical reserve; one hide does not duplicate; and **a magical assisting tool does not make a magical or suppressed-magical target eligible for mundane dismantling**.

## 3. GEX-01 — Mining information-task training must appear in the public guide

**Required correction; no new mechanic.**

GT-M02 explicitly applies **no tool PB and disadvantage to untrained Mining attempts**, alongside WIS for information procedures. The active shared guide states that rule only for “unranked extraction.” The Mining guide defines prospecting and assay but does not explicitly carry their untrained terms into the public instructions. The controlling and candidate passages are recorded in the :chatgpt-content-reference{index="4"}[correction evidence](sandbox:/mnt/data/gathering_reviewer_outputs/CORRECTION_EVIDENCE.md).

### Affected recipes

The **26** information-capable cards are:

`recipe-320, recipe-323, recipe-325, recipe-326, recipe-329, recipe-330, recipe-331, recipe-333, recipe-334, recipe-335, recipe-338, recipe-339, recipe-340, recipe-341, recipe-342, recipe-344, recipe-346, recipe-347, recipe-350, recipe-351, recipe-352, recipe-353, recipe-354, recipe-356, recipe-357, recipe-657`.

These are the five Gem Cutters, eight Prospecting Tools and thirteen Mining Tools with an eligible information role. **Eighteen are public.** Picks, Ore Extractors and Drill gain no information role.

### Exact replacement wording

In `GATHERING_TOOL_CANDIDATE_GUIDE.md`, replace the first two sentences of the training paragraph with:

> The ordinary Mining prospecting and mineral-assay procedures, and otherwise permitted unranked extraction, can be attempted untrained with no relevant tool PB and disadvantage. Dismantling and restoration require the actual trade credential.

Retain the paragraph’s remaining creation and finished-item qualifications.

In `MINING_CANDIDATE_GUIDE.md`, before the prospecting/assay resolution paragraph, add:

> For these ordinary Mining information tasks, an untrained lead uses WIS with no Miner's-tools proficiency contribution and disadvantage. No recipe-level or formula gate applies to these unranked tasks. The actual required implements, lawful access, physical suitability and the candidate's genuine qualifying operation remain necessary. Other advantage/disadvantage sources use Core arbitration; this does not add another die for each disadvantage source.

Extraction’s STR/WIS choice and the family whitelist remain unchanged.

**Required regression:** with dice **17/8**, WIS +2, no PB, a genuinely eligible +1 information tool, DC12 and no countervailing advantage, select **8**: total **11, Failure**. Do not select17, add tool PB, impose the formula’s creation level or invent an information role for an incompatible body.

## 4. GEX-02 — Salvaging failed-supply precision must appear in the active guides

**Required operational-guide/public-projection correction; no ingredient change.**

GT-V11 expressly makes **Purification agent and Stabilizer divisible accounting lots to 0.01 of their exact source units** for normal Failed creation recovery. The shared guide explicitly names Skinning supplies but leaves other materials to their governing precision. The internal operational summary likewise omits the express Salvaging binding.

The rule survives in the preserved internal directions, but it needs to appear in the active public/shared instructions because it determines actual returned quantities. **This is an operating rule, not a private donor dossier.** See the :chatgpt-content-reference{index="5"}[source and candidate passages](sandbox:/mnt/data/gathering_reviewer_outputs/CORRECTION_EVIDENCE.md).

### Affected recipes

The **29** Salvaging cards with these consumed supplies are:

`recipe-433, recipe-435, recipe-437, recipe-438, recipe-439, recipe-442, recipe-443, recipe-447, recipe-450, recipe-451, recipe-452, recipe-453, recipe-454, recipe-456, recipe-457, recipe-458, recipe-460, recipe-461, recipe-462, recipe-463, recipe-465, recipe-466, recipe-467, recipe-468, recipe-469, recipe-470, recipe-668, recipe-669, recipe-671`.

The **15 public** affected cards are:

`recipe-433, recipe-435, recipe-437, recipe-438, recipe-439, recipe-442, recipe-443, recipe-447, recipe-450, recipe-451, recipe-452, recipe-453, recipe-454, recipe-456, recipe-668`.

### Exact replacement wording

Replace the shared guide’s sentence naming Skinning supplies and “other materials” with:

> Skinning's actual oils, tanning solution and salts use source-unit precision of 0.01. For Salvaging recipe creation, Purification agent and Stabilizer are likewise divisible accounting lots to 0.01 of their own exact source unit. On Failed creation, recover 25% per exact consumed non-catalyst identity and floor to that identity's allowed precision. Vessels and consumed-tool source units remain indivisible; other ingredients require their own governing physical precision. This is creation-failure recovery, not the finished tool's dismantling recovery percentage.

Carry the same explicit GT-V11 binding into `GATHERING_TOOL_INTERNAL_OPERATIONAL_GUIDE.md` and its generation source. Preserve the surrounding identity, age, condition, containment, catalyst, Mishap and abandonment restrictions.

For quantity \(Q\) and permitted precision \(u\), the existing calculation remains:

\[
u\left\lfloor\frac{0.25Q}{u}\right\rfloor
\]

**Required regressions:** On Failed creation, recipe-433’s five Stabilizer units return **1.25 source units, 0.125 lb**. Its single indivisible fang returns zero; the Weave Filter remains a separate retained tool. Recipe-668’s one Purification agent unit returns **0.25 source unit, 0.025 lb**; its indivisible consumed tools and fused cog return zero under the default source-unit premise. Neither Failed batch produces an enchanted tool. Actual receivers, remaining matter and continuing clocks still apply.

## 5. Public component envelope: accepted, with GEX-02 carried through

**The fail-closed envelope is acceptable for this exact Director-mediated public package. It must not be treated as a complete player-only stock matcher.**

All **285 public component occurrences** retain their ordered membership, printed name, quantity, role and consumed flag. The **82 published supplemental occurrences** resolve to independently public materials and match the associated source requirements in this handoff, including rarity, properties and material category—not merely name, tier, value and mass. Those occurrences represent **50 distinct supplemental profiles**.

The **203 withheld occurrences** comprise **201 tool/process-supply requirements** without the matching supplemental public material authority, plus two printed mentions with restricted dossiers: **recipe-333[1] and recipe-436[2]**.

**Neither restricted dossier needs to be published.** Preserve their printed ingredient mentions and existing approved formula information while withholding the supplemental dossiers. GEX-02 supplies a public recovery procedure, not donor, drop, access or cosmological metadata.

The stable **recipe ID plus component index** identifies the internally preserved requirement for Director stock verification. An absent public tier, value, mass or profile is **not a wildcard, zero cost, cheap ordinary substitute or permission to craft**. A matching name or sufficient money does not establish the required stock.

The current guide already requires exact Director verification before work. That is sufficient audience treatment. Apart from carrying through GEX-02, **no further recipe-critical audience correction or private-profile disclosure is required**.

Keep the full **82 public / 6 restricted / 40 Director-only** boundary, fifteen public output models, public auxiliary dependencies, all492 book paragraphs, and exclusion of the private Drill, Recovery Rig and recipe-671 metadata.

## 6. Conditions for promotion

**All128 candidates may be promoted to reviewed authored-operational status under this verdict once these three conditions are documented:**

1. **Apply GEX-01 and GEX-02.** Preserve v1 and all originals. Version the corrected guides and generation source, regenerate affected derived copies, and record current hashes rather than reusing stale evidence.
2. **Validate the corrected envelope.** Rerun all-card source/register/requirement/manuscript/public-envelope checks, existing arithmetic/reference suites and the named new regressions. Confirm matching public/internal rules and continued withholding of private profiles. Historical aggregate PASS counts alone are insufficient.
3. **Keep the change scope bounded.** Limit the delta to these two corrections, derived regeneration, evidence/version updates and normal operational review-status bookkeeping. Preserve original source statuses, `needsReview`, legacy fields, ingredients, visibility and private research. Record this exact verdict separately from historical source directions.

**No additional generic source conference or full128-card resubmission is required solely for those changes.** A material rule change outside this scope requires a targeted exact-diff review, not reopening unchanged source cohorts.

| Review state | Recipes reviewed | Recipes pending | Public reviewed | Public pending |
|---|---:|---:|---:|---:|
| Until the conditions are satisfied | 392/687 | 295 | 251/433 | 182 |
| After all128 promotions are recorded | **520/687** | **167** | **333/433** | **100** |

Public review is not public release. No promotion was written into the unchanged handoff during this inspection.

Actual acquisition, anatomy, component bills, lawful access, immutable origin, special containment and unsupported targets remain execution prerequisites—not new preliminary gathering conferences. Runtime implementation, campaign authentication, human balance, full bestiary/expedition integration and final whole-game flow remain separate gates.

**Only GEX-01 and GEX-02 prevent promotion of this exact handoff.** The owner’s sequence remains unchanged: complete authored candidate and final joint whole-game flow confirmation, authorized push, verified remote commit, then careful cosmology review.
