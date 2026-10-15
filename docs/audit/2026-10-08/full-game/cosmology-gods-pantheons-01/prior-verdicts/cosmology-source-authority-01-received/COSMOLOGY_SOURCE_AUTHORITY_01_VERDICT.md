# COSMOLOGY-SOURCE-AUTHORITY-01 — first post-push authority conference

Baseline: verified progress-backup commit `a3f75a0ce577f51bd39153a872ef05ba9e877642`. Submission: 949,138 bytes, SHA-256 `940c53f11ac3757ad1a7fa9b388103494c5d82cd1104aea3ee15ce819f68d68e`, 40 manifest payloads verified.

## Authority model

1. **recorded-owner-decision** — Controls the exact questions the owner answered; preserve wording and supersession notes; unanswered portions remain open. Sources: `docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md`, `docs/mechanics/LEVEL_97_OLD_GOD_Q6_OPEN.md` Q6 Level-97/endgame became a separately registered canonical Director domain on 2026-08-05. This does not create a general cosmology domain.

2. **registered-domain-authority** — CANON_MANIFEST owns domain routing. Use only the scopes it actually registers; root placement does not promote a source. Sources: `docs/canon/CANON_MANIFEST.json`, `docs/canon/REPOSITORY_PROMOTION.md` Relevant registered domains are locked-baselines and floor-97-old-god-endgame; there is no general cosmology domain.

3. **established-director-truth** — Director-only syntheses may state objective setting truth where consistent with recorded owner decisions and registered domains; they do not override a higher owner lock. Sources: `DescentReviewChanges/ReviewBible/docs/canon/CANON_CORE.md`, `DescentReviewChanges/ReviewBible/docs/canon/PLAYER_DIRECTOR_BOUNDARY.md`, `docs/mechanics/SILENT_ONES_CANON.md`

4. **in-world-belief-or-public-myth** — May be true, incomplete, mistaken, symbolic, or deliberately limited by audience. Do not literalize belief into Director truth. Sources: `docs/mechanics/APPENDIX_B_FOLK_RELIGION.md`, `DescentReviewChanges/ReviewBible/docs/canon/PLAYER_DIRECTOR_BOUNDARY.md`

5. **original-unpromoted-source-document** — Preserved source evidence and wording. Root presence is not automatic canon promotion. Portions become controlling only where later owner/domain authority adopts or explicitly relies on them. Sources: `The Cosmology of Decennium Descent.docx`, `The Decennium Descent and the Matrix of Oblivion.docx`, `The_World_of_Aethel_Lore.docx`

6. **historical-summary-or-status-record** — Evidence of what a prior pass believed/did; useful for chronology, not an independent owner of cosmology facts. Sources: `docs/manuals/CONTINUITY_B_COSMOLOGY.md`, `docs/mechanics/PLAYERBOOK_DMG_ALIGNMENT_2026-07-31.md`, `docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md`

7. **provisional-runtime-presentation** — Rendering/data presentation can expose or summarize source material but does not elevate it to objective canon or change audience classification. Sources: `src/data/cosmology-lore.json`, `src/components/CosmologyViewer.tsx`, `src/app/page.tsx`


## COS-A01–06 dispositions

### COS-A01 — CONFIRMED AUTHORITY GAP — no contradiction; do not invent a general cosmology domain

Keep domain-specific authority. Owner locks control their answered questions; registered floor-97/locked-baseline domains control those scopes; no file in this packet is promoted to general-cosmology owner merely by root/main placement.


**Support:**

- `docs/canon/CANON_MANIFEST.json` (lines=5-11,106-117 and domain entries locked-baselines/floor-97-old-god-endgame): Registry is the single domain-level authority map and has no general cosmology domain.

- `docs/canon/REPOSITORY_PROMOTION.md` (lines=6,21-31,44-48): Root drops are not auto-canonical; promotion requires review and owner approval.

- `docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md` (lines=3-6): Recorded owner wording is locked; unanswered Q6 stayed open at that time.


**Unresolved dependency:** A later deliberate registry decision may create a general cosmology domain, but this conference must not do so.


### COS-A02 — CONFIRMED SOURCE-COMPLETENESS GAP — preserve placeholder; no replacement history

The World of Aethel root DOCX cannot establish Sections I–VI because its own P1 is a placeholder. Its surviving VII+ material is source evidence only and must be checked against later owner/domain authority before use. The runtime itself marks I–VI as an extract gap/draft.


**Support:**

- `The_World_of_Aethel_Lore.docx` (paragraph=1; paragraphSha256=cf8f1a6b0184dabdbca22188835d93f06c4e522e37cae38ba4a2265f37c33dac): [...Existing Sections I–VI remain unchanged...]

- `src/data/cosmology-lore.json` (pointer=/worldSections/0): I–VI is explicitly labeled a draft extract gap requiring re-ingest.

- `The_World_of_Aethel_Lore.docx` (paragraphs=3-13,79-88): The extant document resumes at VII and contains legacy myth/endgame statements, including Binding@97, that cannot silently outrank later Q6 authority.


**Unresolved dependency:** Locate and compare the actual earlier Sections I–VI or their authoritative published counterpart during the history/publication pass.


### COS-A03 — PRESENTATION-BOUNDARY RISK, NOT A COSMOLOGY-FACT CONTRADICTION

The byte-identical unfiltered cosmology JSON is imported by a client component reachable from the current source entrypoint and renders chapter bodies. That is sufficient to flag a source-presentation boundary concern, but not to assert a deployed leak, authentication failure, or certified player build. Do not infer truth from renderability; do not publish or rewrite in this pass.


**Support:**

- `src/data/cosmology-lore.json` (sha256=1cb25a15c5f5adda5683b84ab303967f4d1472037ccacfe95ad29e5d4e5ab7c7): Byte-identical to Director-labeled unfiltered counterpart.

- `src/components/CosmologyViewer.tsx` (lines=8,33-37,360-450): Imports the JSON, labels only some sections as draft, and renders selected bodies.

- `src/app/page.tsx` (lines=12,24-45): CosmologyViewer is reachable through the source entrypoint's my-content tab.

- `DescentReviewChanges/ReviewBible/docs/canon/PLAYER_DIRECTOR_BOUNDARY.md` (lines=18-32): Deep Heartcell/Silent Ones/Matrix truths are Director-only and revelation-gated.


**Unresolved dependency:** Later separate projection audit: map each rendered chapter/glossary/plane row to player-safe, belief, scholarly, revelation-gated, or Director-only classification before any player build is certified.


### COS-A04 — ACTUAL PRESENTATION CONFLICT — owner answer already exists; no new owner choice needed

Lumina/Umbra must not be presented as literal independent primordial beings in objective canon. The owner locked them as theological abstractions in the folk-religion layer. The original cosmology also describes those names as later labels applied to contrary gestures, while the Matrix calls them opposing principles rather than mortal gods. The unqualified runtime glossary summaries therefore overstate ontology and are subordinate/stale presentation text, not a basis to rewrite the First Choir or folk pantheon.


**Support:**

- `docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md` (lines=79-93): Keep Appendix B as mortal folk religion; Lumina/Umbra theological abstractions; do not reconcile literally into Spiral/Choir/Old Ones; First Choir exactly seven.

- `docs/mechanics/APPENDIX_B_FOLK_RELIGION.md` (lines=25-36,42-55): Explicitly says no literal reconciliation; gives exact seven First Choir and hierarchy.

- `The Cosmology of Decennium Descent.docx` (paragraph=4; paragraphSha256=849cd15b1f6ca043bd7bb7b5978cf888c9232244542c134fce8cbf8530f9968d): Later viewers would coax the names Lumina and Umbra from contrary primal gestures; neither gesture possessed shape, limb, or mind.

- `The Decennium Descent and the Matrix of Oblivion.docx` (paragraph=12; paragraphSha256=87dd08ea083b17845e408d083e168267e42d7dd31da1ea82549739529762c833): Lumina and Umbra were not originally gods in the mortal sense; they were opposing principles that manifested will.

- `src/components/CosmologyViewer.tsx` (lines=51-59): Current glossary uses unqualified 'Primordial abyssal depth'/'Primordial radiant counterpart' wording.


**Unresolved dependency:** Any later correction should be a guarded presentation-only change or attribution, preserving original source words and the folk-belief layer.


### COS-A05 — STALE/CONTRADICTORY STATUS NOTE — later records say patch applied; current publication bytes still require separate verification

Within APPENDIX_B_FOLK_RELIGION, line 103 ('TODO, not performed') conflicts with its own later status header/section 6 and with the 2026-07-31 patch report. Treat line 103 as stale historical status, not as evidence that the patch is absent. This packet does not contain the actual Player Rulebook bytes, so do not claim current publication cleanliness solely from reports.


**Support:**

- `docs/mechanics/APPENDIX_B_FOLK_RELIGION.md` (lines=3,86-103): Same file says patch applied and later retains a TODO/not-performed table row.

- `docs/mechanics/PLAYERBOOK_DMG_ALIGNMENT_2026-07-31.md` (lines=28-44,70-74): Historical patch report records Appendix B as fixed and player-side Q-OV-3 implemented.

- `docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md` (lines=189-195): Override tracker says player patch applied 2026-07-31.


**Unresolved dependency:** During public-book comparison, hash/read the actual current Player Rulebook Appendix B and living extract before correcting any status/navigation note.


### COS-A06 — PARTIALLY NARROWED; IDENTITY MERGE STILL OPEN

Do not treat an ordinary political truce or cessation of war as the awakening trigger. The Matrix original explicitly says the dungeon prevents absolute ontological peace, not political peace; later Director material likewise distinguishes true lasting peace from a managed truce. What remains unresolved is the exact operational/metaphysical threshold by which that condition is measured. Separately, Old God ≡ Old Ones ≡ Binding shard ≡ Interstice remains expressly unmerged and must not be inferred.


**Owner-choice boundary:** Only if/when mechanics require it: define the observable/operational condition for 'absolute/true lasting peace' (e.g. a specific resonance-state predicate or leave it narrative/Director-adjudicated). Do NOT ask whether an ordinary political truce counts; existing sources already say it does not. No owner question is needed now for the endgame identity unless a later design step requires choosing among the currently separate identities.


**Support:**

- `The Decennium Descent and the Matrix of Oblivion.docx` (paragraphs=4-7,17,44-50): Explicitly rejects political peace and defines the threat as absolute stillness/elimination of difference.

- `docs/mechanics/SILENT_ONES_CANON.md` (lines=75-81): Old open note asks peace trigger threshold; later Q6 entry remains separate.

- `docs/mechanics/LEVEL_97_OLD_GOD_Q6_OPEN.md` (lines=29-36,80-87): Old God vs Old Ones vs Binding shard vs Interstice identity merge remains forbidden to invent.

- `outside-packet notebook check: The_Directors_Crucible.docx`: Later Director prose says 'true, lasting peace' is the trigger and a managed truce is not an ending. No later explicit owner-chat identity merge was found.


**Unresolved dependency:** Exact peace threshold remains undefined; identity merge G2 remains undefined. Preserve both as separate unresolved fields.


## Relevant original passages read

- `The Cosmology of Decennium Descent.docx` — ['0-19', '58-65', '75-100']. creation/Lumina-Umbra/Spiral/Old Ones/Choir/planes/peace-relevant passages

- `The Decennium Descent and the Matrix of Oblivion.docx` — ['0-55', '138-149', '280-305']. peace definition, Lumina-Umbra, Old Ones, Divine Pact, legacy Old God, resonance/economy

- `The_World_of_Aethel_Lore.docx` — ['0-18', '78-90']. I-VI placeholder, VII myth/history, Binding@97 and timeline

- `docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md` — ['1-162']. 

- `docs/mechanics/APPENDIX_B_FOLK_RELIGION.md` — ['1-105']. 

- `docs/mechanics/LEVEL_97_OLD_GOD_Q6_OPEN.md` — ['1-109']. 

- `docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md` — ['authority/protocol and Q-OV/Q6 sections, including 136-215']. 

- `docs/canon/CANON_MANIFEST.json` — registry structure plus relevant locked-baselines/floor-97 domains. 

- `docs/canon/REPOSITORY_PROMOTION.md` — ['1-48']. 

- `DescentReviewChanges/ReviewBible/docs/canon/CANON_CORE.md` — ['1-38']. 

- `DescentReviewChanges/ReviewBible/docs/canon/PLAYER_DIRECTOR_BOUNDARY.md` — ['1-41']. 

- `src/components/CosmologyViewer.tsx` — ['1-79', '360-450']. 

- `src/app/page.tsx` — ['1-55']. 

- `src/data/cosmology-lore.json` — metadata, planes, section draft/status metadata, targeted Lumina/Umbra/world-outline fields. 


## Not yet semantically reviewed

- The Cosmology of Decennium Descent.docx Chapters VI-XII outside the targeted passages above

- Full plane-by-plane ontology and all plane cross-references

- Soul/death/resurrection doctrine beyond targeted Matrix/project references

- Full historical chronology across player, Director, and original source books

- All divine/class power dependencies and deity-specific class grants

- Full campaign revelation progression beyond the Heartcell/Silent Ones ladder

- Actual current Player Rulebook Appendix B bytes (not present in this packet)

- Any live deployment/authentication/bundle behavior for CosmologyViewer


## Next ordered comparison work

1. **creation/origin** — Compare Cosmology P0-59, Matrix origin/Pact passages, owner Q1-Q3, CANON_CORE, and public myth. Produce fact/belief/revelation table; preserve two-layer Crucible/Heartcell truth.

2. **gods/pantheons** — Compare First Choir exact seven, Calan'thir/Asmodeus, folk Fifteenfold/cultural/ascended layers, runtime glossary, and Player Rulebook Appendix B. Do not literalize worship masks.

3. **planes** — Compare Cosmology Chapter IV onward, runtime plane list, folk Great Wheel, Rift/background/class references. Separate observed realms from mortal diagrams and gameplay access.

4. **souls/death/resurrection** — Inventory soul ontology, soul coins/contracts, resurrection clauses, death mechanics, soulbinding claims, afterlife/patron references. Distinguish mechanics from theology before any reconciliation.

5. **history** — Recover/locate World of Aethel I-VI; compare VII+ chronology and retired god/gate names against owner Q7 and Q6. Preserve false scholarship/legacy myth where intentionally retained.

6. **divine/class powers** — Map Cleric/Paladin/Shaman/Oracle/etc. power sources and deity/plane prerequisites to the authority layers; do not infer patron/god identity from mechanical grants.

7. **campaign revelations** — Compare public myth, scholarly material, Heartcell ladder, Q6 public ceiling, runtime presentation, and Director content. Define revelation-stage visibility separately from objective truth.


## Guardrails

No source replacement, public projection, deletion, new general cosmology authority, completed cosmology claim, whole-game signoff, or balance approval is made by this conference. Later changes must be separate, guarded, source-linked, and consequence-checked.
