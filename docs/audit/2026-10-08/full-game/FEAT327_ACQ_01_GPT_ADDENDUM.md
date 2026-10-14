# FEAT327-ACQ-01 — Controlling prerequisite addendum

**Disposition: ADOPT with explicit profile-classification and per-feat-exception safeguards.** This closes the omitted acquisition bridge. **FS-01 remains unchanged; FS-02 receives the paragraph below.** No existing per-feat operating exception is reversed.

I checked the actual final package’s FS-01/FS-02, the four relevant convention mappings, and the affected register records. The submitted combat acquisition paragraph contains the weapon bridge, but the replacement shared contract omitted it. The independently completed Riposte, Cleaving Momentum, Battle Mage, Weapon Mastery, Weapon Focus and Whip Control directions remain intact. :chatgpt-content-reference{index="0"}[Preserved final source package](sandbox:/mnt/data/DD_Feats_327_Final_Source_Verdict_and_Evidence.zip)

## 1. Exact operative paragraph and insertion point

In the **derived current** `FEAT_SHARED_DIRECTIONS.json`, find the rule with `"id": "FS-02"`—`/rules/1/wording` in the preserved package. Insert the following as a separate paragraph immediately after:

> Existing genuinely authorized legacy grants remain evidenced; no new builder option follows.

Place it before the paragraph beginning “For the six exploration training entries”. Insert the identical paragraph at the corresponding location in the derived `FEAT_SHARED_DIRECTIONS.md` and its complete public/internal shared-contract representations.

**Exact insertion:**

> **Weapon prerequisite bridge.** Apply this bridge only to an actual printed feat prerequisite, subject to any more specific acquisition direction in that feat’s final procedure. Where a prerequisite names a weapon or weapon type, require actual proficiency with that named current weapon profile/type. A generic Melee or Melee Proficiency prerequisite requires actual proficiency with at least one current melee-weapon profile; Ranged or Ranged Proficiency requires actual proficiency with at least one current ranged-weapon profile. Use the weapon profile’s actual classification, not merely the attack’s melee or ranged delivery: throwing a melee-class weapon does not by itself satisfy Ranged acquisition, and making a ranged spell attack supplies no weapon proficiency. An otherwise generic martial-weapon proficiency prerequisite requires proficiency with at least one actual martial-weapon profile, not all martial weapons; an explicitly stricter per-feat prerequisite remains stricter. Two-Handed or 2H Weapon acquisition requires actual proficiency with a weapon whose current profile possesses the Two-Handed property; proficiency with a Versatile-only weapon held in two hands does not satisfy that gate. Record the qualifying proficiency grant and weapon profile/type in the acquisition snapshot. These are acquisition credentials: they neither supply an item or proficiency nor make an otherwise unproficient attack proficient. They do not impose a new requirement to use the acquisition-qualifying weapon for every later feat event. Actual use-time weapon, proficiency where expressly required, grip, body, range, ammunition, action and other predicates remain those of the exact feat and governing procedure. All other printed ability, level, prerequisite-feat, class-access and earned-opportunity requirements remain mandatory. Class, feat, ancestry and item grants with similar names otherwise remain separate permissions.

This paragraph is the controlling completion. **It does not reactivate the historical acquisition paragraph as an independent operative rule.**

## 2. Provenance: what is retained and what is NEW

The **named-weapon, Melee, Ranged and Two-Handed bridges are a carry-forward clarification** of the submitted combat convention. They are not new prerequisite choices for the seven reported records. Explicitly recognizing `2H Weapon` preserves Cleaving Momentum’s already completed acquisition direction.

The distinction between a weapon’s classification and an attack’s delivery preserves the existing final procedures, including Double Tap’s exclusion of thrown melee-class weapons from its ranged-weapon classification.

**One narrowly NEW shared completion is made explicit:** the “at least one actual martial-weapon proficiency” reading becomes the default for otherwise-generic martial-weapon prerequisites. Battle Mage already states that choice expressly; its existing NEW provenance remains. The additional applicable final record is **`eldritch_combat` / CF-41**, whose acquisition sentence requires actual martial-weapon proficiency without specifying an all-martial grant. This addendum settles that quantity as **at least one**, while retaining its actual spellcasting prerequisite and every casting restriction. It does not create a general alias between martial proficiency, a martial class, or a class feature.

## 3. Finite derived-candidate operations

### ACQ-01.1 — Complete FS-02

Perform the insertion above in the current derived shared rule and its matching manuscript/envelope representations. Keep the rest of FS-02, all of FS-01, and all original source objects unchanged.

### ACQ-01.2 — Make the convention references explicit

In the **derived** `FEAT_SHARED_CONVENTION_DISPOSITIONS.json`, append `FEAT327-ACQ-01` to `controllingDecisions`, without removing FS-01 or FS-02, for these four entries:

| Preserved-package pointer | Entry identity |
|---|---|
| `/entries/35` | `combat` — `/sharedProposal/Authority and acquisition` |
| `/entries/42` | `general_combat` — `/sharedProposal/Authority and acquisition` |
| `/entries/50` | `general_combat` — `/proposedCombatConventionDependency/Authority and acquisition` |
| `/entries/84` | `heritage_mutation` — `/proposedCombatDependency/Authority and acquisition` |

Match the entry identity as well as the index. Append this exact sentence to each current `replacement` value:

> For weapon prerequisites, apply FS-02 as completed by FEAT327-ACQ-01. The historical acquisition paragraph is not independently operative; each final per-feat acquisition and use-time exception retains its stated scope.

Preserve each entry’s `original` value and existing disposition.

### ACQ-01.3 — Bind the actual acquisition predicates

The seven reported records receive the following operative prerequisite interpretation through FS-02:

| Exact feat IDs | Weapon-credential predicate at acquisition |
|---|---|
| `bleeding_edge`, `crippling_strike`, `disarming_blow`, `savage_momentum`, `tactical_flanker` | Actual proficiency with at least one current **melee-weapon profile**. |
| `double_tap`, `target_mark` | Actual proficiency with at least one current **ranged-weapon profile**. |

Two further existing printed predicates must also use the completed shared bridge:

| Exact feat ID | Application |
|---|---|
| `sure_shot` / CF-32 | Its printed **Ranged Proficiency** means proficiency with at least one current ranged-weapon profile. |
| `eldritch_combat` / CF-41 | Its generic martial proficiency gate means proficiency with at least one actual martial-weapon profile, alongside actual spellcasting access. |

**No replacement of these feats’ attack, target, duration or other operating prose is required.** Their existing shared-contract reference now resolves the acquisition gate. Where the derived candidate stores expanded acquisition predicates, make those predicates match the table while preserving the exact raw prerequisite strings, including original spacing.

In particular, do not convert `target_mark`’s Ranged acquisition credential into a ranged-only activation restriction: its final procedure expressly permits activation using an actually held usable melee weapon’s reach. Likewise, do not narrow Crippling Strike’s expressly permitted thrown-melee-weapon use.

Keep the already explicit neighboring rules unchanged: `riposte`, `cleaving_momentum`, `battleMage`, `weapon_mastery`, `weaponFocus` and `whip_control`.

### ACQ-01.4 — Preserve authority and history

Record this addendum as a controlling correction beside the original final package. Preserve the original archive, manifest, verdict, register, historical convention text and original hashes. Record measured descendant hashes only after applying the derived changes; do not overwrite historical hashes or claim that the original package contained this paragraph.

No regeneration of unrelated chapters or alteration of an original, reviewed feat, deferred payload or comparison catalog is authorized.

## 4. Finite acceptance cases

These are **expected source-based adjudications, not tests claimed executed here**. Except where a case explicitly tests another gate, assume every other printed and FS-01 acquisition requirement is satisfied.

| Case | Required outcome |
|---|---|
| **ACQ-T01 — Generic Melee** | Actual proficiency covering a current melee-weapon profile satisfies the weapon-credential part of each of the five listed Melee feats. Possessing the physical weapon at selection is not additionally required by this credential bridge. |
| **ACQ-T02 — Generic Ranged** | Actual proficiency covering a current ranged-weapon profile satisfies the weapon-credential part of `double_tap`, `target_mark` and `sure_shot`. |
| **ACQ-T03 — Possession without proficiency** | Merely holding, owning or successfully attacking with an unproficient weapon does not satisfy its weapon-proficiency acquisition gate. A later attack with that weapon still lacks proficiency unless an independent actual grant supplies it. |
| **ACQ-T04 — Versatile-only acquisition** | Proficiency with a profile possessing Versatile but not Two-Handed fails Cleaving Momentum’s Two-Handed acquisition gate, even while that weapon is held in two hands. |
| **ACQ-T05 — Acquired Cleaving Momentum** | After lawful acquisition using a proficient Two-Handed profile, its explicitly permitted melee Versatile two-hand triggering and follow-up attacks may operate the feat. Preserve the original acquisition snapshot; do not retroactively substitute the Versatile profile as the acquisition qualification. |
| **ACQ-T06 — Delivery is not classification** | Throwing a proficient melee-class weapon does not alone satisfy generic Ranged acquisition. A ranged spell attack also supplies no such credential. A profile genuinely classified as ranged is evaluated according to that actual profile. |
| **ACQ-T07 — Named and martial gates** | Proficiency with an unrelated melee weapon does not satisfy Whip Control’s Whip gate. One actual martial-profile proficiency satisfies the otherwise-generic martial component of `battleMage` and `eldritch_combat`, but not their separate spellcasting prerequisite. |
| **ACQ-T08 — Other prerequisites remain** | A qualifying weapon credential cannot compensate for a deficient permanent ability score, unmet level or prerequisite-feat requirement, missing actual class/casting access, or absent earned feat opportunity. |
| **ACQ-T09 — No acquisition-to-use narrowing** | A lawfully acquired `target_mark` may use its final procedure’s permitted melee reach at activation. Weapon Focus retains its own chosen-profile/current-proficiency condition and explicit distinct-profile repeatability; Weapon Mastery remains its separate permanent, nonrepeatable selection. |

**Acceptance boundary:** applying this paragraph, the four convention-reference amendments, the stated prerequisite bindings and these finite checks closes **FEAT327-ACQ-01 only**. It supplies no proficiency, class feature, feat opportunity, item or new use-time permission beyond the retained exact procedures. It grants **no exact approval or promotion of the assembled candidate**, and no runtime, human-balance or whole-game approval.

The preserved delivery order remains **actual final joint whole-game flow agreement → authorized GitHub push → verified remote commit → careful cosmology review**.
